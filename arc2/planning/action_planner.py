"""Turns a belief-space path into RobotAPI primitives, and knows when the
plan it produced has been falsified.

`Plan.invalidated_by(model)` is the proactive half of failure detection: the
agent does not have to physically bump into the newly-discovered wall to
abandon a route through it. The reactive half lives in the agent loop.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from arc2.planning.path import astar, simplify
from arc2.types import Pose, Vec2, angle_diff
from arc2.world.belief import CellState
from arc2.world.model import WorldModel

#: Longest single forward command. Short legs mean the agent re-observes
#: often, which is what lets it notice the world changing under a plan.
MAX_LEG_M = 1.1
ARRIVAL_TOLERANCE_M = 0.45
HEADING_TOLERANCE_RAD = 0.12


@dataclass
class Step:
    kind: str                # "turn" | "move"
    value: float
    note: str = ""

    def as_dict(self) -> dict:
        return {"kind": self.kind, "value": round(self.value, 4), "note": self.note}


@dataclass
class Plan:
    goal: Vec2
    purpose: str
    waypoints: list[Vec2]
    cells: list[tuple[int, int]]
    created_tick: int
    cursor: int = 0

    @property
    def done(self) -> bool:
        return self.cursor >= len(self.waypoints)

    @property
    def current(self) -> Vec2 | None:
        return None if self.done else self.waypoints[self.cursor]

    def advance(self) -> None:
        self.cursor += 1

    def invalidated_by(self, model: WorldModel) -> str | None:
        """Has anything learned since planning made this route impossible?"""
        for cx, cy in self.cells[self._cell_cursor():]:
            if model.occupancy.get(cx, cy) is CellState.BLOCKED:
                return f"route_cell_blocked:{cx},{cy}"
        return None

    def _cell_cursor(self) -> int:
        if not self.waypoints or self.done:
            return 0
        frac = self.cursor / max(1, len(self.waypoints))
        return int(frac * len(self.cells))

    def as_dict(self) -> dict:
        return {"purpose": self.purpose,
                "goal": [round(self.goal.x, 3), round(self.goal.y, 3)],
                "waypoints": [[round(w.x, 3), round(w.y, 3)] for w in self.waypoints],
                "n_cells": len(self.cells), "created_tick": self.created_tick,
                "cursor": self.cursor}


def plan_route(model: WorldModel, start: Pose, goal: Vec2, purpose: str,
               tick: int) -> Plan | None:
    bel = model.occupancy
    s = bel.to_cell(start.x, start.y)
    g = bel.to_cell(goal.x, goal.y)
    cells = astar(bel, s, g)
    if cells is None or len(cells) < 2:
        return None
    waypoints = [Vec2(*bel.to_world(cx, cy)) for cx, cy in simplify(cells)]
    if waypoints and waypoints[0].distance_to(Vec2(start.x, start.y)) < 0.2:
        waypoints = waypoints[1:]
    if not waypoints:
        # NO FALLBACK. Substituting the raw goal here manufactured a waypoint
        # inside a wall and the agent drove at it until the action budget ran
        # out. "I could not plan a route" is a real answer; a fake plan is not.
        return None
    # The effective goal is where the route actually ENDS, which may be a
    # snapped-to-reachable neighbour of what was asked for.
    effective = Vec2(*bel.to_world(*cells[-1]))
    return Plan(effective, purpose, waypoints, cells, tick)


def next_steps(pose: Pose, waypoint: Vec2) -> list[Step]:
    """Primitive commands taking the robot toward one waypoint.

    Emits at most one turn and one bounded move, so the caller re-observes
    between every pair -- the loop is deliberately not allowed to execute a
    long open-loop sequence.
    """
    dx, dy = waypoint.x - pose.x, waypoint.y - pose.y
    dist = math.hypot(dx, dy)
    if dist < ARRIVAL_TOLERANCE_M:
        return []
    desired = math.atan2(dy, dx)
    err = angle_diff(desired, pose.heading)
    if abs(err) > HEADING_TOLERANCE_RAD:
        return [Step("turn", err, "align")]
    return [Step("move", min(dist, MAX_LEG_M), "advance")]
