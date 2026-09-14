"""Task-level strategy: what should ARC-2 be trying to do right now, and what
should it try INSTEAD when the current attempt is disproved.

Two separate ideas live here and are deliberately not merged:

  PHASE    -- where we are in the task. Only real progress advances it.
  STRATEGY -- how we are currently attempting the phase. A failure changes
              the strategy; it does not undo progress.

Conflating them is how an agent "recovers" from a blocked corridor by
forgetting it already found the target.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

from arc2.memory.episodic import EpisodicMemory
from arc2.types import Pose, Vec2
from arc2.world.model import Knowledge, WorldModel


class Phase(str, Enum):
    SEARCH = "search_for_target"
    APPROACH = "approach_target"
    ACQUIRE = "acquire_target"
    RETURN = "return_home"
    DELIVER = "deliver"
    DONE = "done"
    UNRECOVERABLE = "unrecoverable"


class Strategy(str, Enum):
    EXPLORE_FRONTIER = "explore_frontier"
    DIRECT_ROUTE = "direct_route"
    ALTERNATE_ROUTE = "alternate_route"
    CLEAR_OBSTRUCTION = "clear_obstruction"
    CHANGE_MOBILITY = "change_mobility_mode"
    INSPECT = "inspect"


@dataclass
class Decision:
    phase: Phase
    strategy: Strategy
    goal: Vec2 | None
    rationale: str
    target_id: str | None = None

    def as_dict(self) -> dict:
        return {"phase": self.phase.value, "strategy": self.strategy.value,
                "goal": None if self.goal is None else
                        [round(self.goal.x, 3), round(self.goal.y, 3)],
                "rationale": self.rationale, "target_id": self.target_id}


class TaskPlanner:
    """Decides phase and strategy from the belief and the memory ONLY."""

    def __init__(self, target_label: str, home_tolerance: float) -> None:
        self.target_label = target_label
        self.home_tolerance = home_tolerance
        self.phase = Phase.SEARCH
        self.strategy = Strategy.EXPLORE_FRONTIER
        self.consecutive_failures = 0
        self.strategy_changes = 0

    # -- failure handling --------------------------------------------------
    def on_failure(self, reason: str, contact_id: str | None,
                   model: WorldModel, memory: EpisodicMemory,
                   position: Vec2) -> str:
        """Choose a DIFFERENT strategy. Returns a human-readable rationale.

        The mapping from physical reason to adaptation is the whole point:
        a step is not a wall, and a crate is not a dead end.
        """
        self.consecutive_failures += 1
        previous = self.strategy

        # Escalation is checked FIRST and unconditionally. Previously the
        # "this might be pushable" branch short-circuited it, so a wedged
        # crate was re-pushed indefinitely -- measured: 728 identical
        # failures. A recovery that keeps failing is not a recovery.
        if self.consecutive_failures >= self.ESCALATE_AFTER:
            memory.abandon_region(position, reason)
            self.strategy = Strategy.EXPLORE_FRONTIER
            self.consecutive_failures = 0
            note = "repeated failure here; abandoning region and re-exploring"
        elif reason == "step_too_high":
            self.strategy = Strategy.CHANGE_MOBILITY
            note = "elevation change exceeds current mode's step limit"
        elif (contact_id is not None
              and self._is_movable_candidate(contact_id, model)
              and not memory.has_failed("push", Pose(position.x, position.y, 0.0))):
            # ...and only while pushing HERE has not already been disproved.
            self.strategy = Strategy.CLEAR_OBSTRUCTION
            note = f"obstruction {contact_id} may be displaceable"
        else:
            self.strategy = Strategy.ALTERNATE_ROUTE
            note = "route disproved; seeking another"

        if self.strategy is not previous:
            self.strategy_changes += 1
        return f"{previous.value} -> {self.strategy.value}: {note}"

    def on_progress(self) -> None:
        self.consecutive_failures = 0
        if self.strategy in self.RECOVERY:
            self.strategy = Strategy.DIRECT_ROUTE

    #: Strategies that are RECOVERIES -- chosen because something failed, and
    #: therefore outranking whatever the phase would normally do.
    RECOVERY = (Strategy.ALTERNATE_ROUTE, Strategy.CLEAR_OBSTRUCTION,
                Strategy.CHANGE_MOBILITY)

    #: Consecutive failures in one place before the region is written off.
    ESCALATE_AFTER = 3

    def _effective_strategy(self, default: Strategy) -> Strategy:
        """A live recovery outranks the phase default, in EVERY phase."""
        return self.strategy if self.strategy in self.RECOVERY else default

    @staticmethod
    def _is_movable_candidate(contact_id: str, model: WorldModel) -> bool:
        """Only a thing we have actually SEEN and classified as moveable-ish.

        We must not assume a contact id we have never perceived is a crate --
        that would be reading ground truth through the collision report.
        """
        b = model.objects.get(contact_id)
        return b is not None and b.label in ("crate", "unknown_object")

    # -- phase machine -----------------------------------------------------
    def decide(self, model: WorldModel, memory: EpisodicMemory,
               position: Vec2, carrying: list[str]) -> Decision:
        target = model.find_by_label(self.target_label)
        home = model.home or position

        if self.phase is Phase.SEARCH:
            if target is not None and target.knowledge is Knowledge.KNOWN:
                self.phase = Phase.APPROACH
            elif target is not None:
                return Decision(Phase.SEARCH, Strategy.INSPECT, target.position,
                                "candidate seen but not confirmed; close in to "
                                "confirm before committing", target.object_id)

        if self.phase is Phase.APPROACH:
            if target is None:
                self.phase = Phase.SEARCH
            else:
                if position.distance_to(target.position) <= 0.80:
                    self.phase = Phase.ACQUIRE
                else:
                    return Decision(Phase.APPROACH,
                                    self._effective_strategy(Strategy.DIRECT_ROUTE),
                                    target.position, "target located; routing to it",
                                    target.object_id)

        if self.phase is Phase.ACQUIRE:
            if carrying:
                self.phase = Phase.RETURN
            elif target is not None:
                return Decision(Phase.ACQUIRE, Strategy.INSPECT, target.position,
                                "within reach; grasping", target.object_id)
            else:
                self.phase = Phase.SEARCH

        if self.phase is Phase.RETURN:
            if position.distance_to(home) <= self.home_tolerance:
                self.phase = Phase.DELIVER
            else:
                return Decision(Phase.RETURN,
                                self._effective_strategy(Strategy.DIRECT_ROUTE),
                                home, "carrying payload; returning to start area")

        if self.phase is Phase.DELIVER:
            return Decision(Phase.DELIVER, Strategy.INSPECT, home,
                            "in the start area; placing payload",
                            carrying[0] if carrying else None)

        if self.phase is Phase.DONE:
            return Decision(Phase.DONE, Strategy.INSPECT, None, "task complete")

        # Default: keep exploring -- UNLESS a recovery is live. This is the
        # branch that used to discard CLEAR_OBSTRUCTION and re-derive the same
        # blocked route indefinitely.
        strat = self._effective_strategy(Strategy.EXPLORE_FRONTIER)
        return Decision(Phase.SEARCH, strat, None,
                        "clearing an obstruction on the route"
                        if strat is Strategy.CLEAR_OBSTRUCTION else
                        "target not yet located; expanding the known map")
