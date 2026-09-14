"""The robot's model of the world. Beliefs, never facts.

Everything here was put here by the perception layer from an actual sensor
return, or by the agent from an actual action outcome. Nothing is seeded from
ground truth. If the agent has not seen the target, `target_belief()` returns
None -- it does not return an approximate location.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

from arc2.types import Pose, Vec2
from arc2.world.belief import CellState, OccupancyBelief


class Knowledge(str, Enum):
    """Epistemic status of a single belief. Required by the spec, and load
    bearing: the planner treats UNCERTAIN differently from KNOWN."""

    KNOWN = "known"
    UNCERTAIN = "uncertain"
    UNKNOWN = "unknown"


@dataclass
class ObjectBelief:
    object_id: str
    label: str
    position: Vec2
    confidence: float
    first_seen_tick: int
    last_seen_tick: int
    observation_count: int = 1
    labels_seen: dict = field(default_factory=dict)

    @property
    def knowledge(self) -> Knowledge:
        """A label seen once at low confidence is UNCERTAIN, not KNOWN.

        The threshold is deliberately not tuned to make the demo succeed --
        it is what stops the agent from committing to a 0.3-confidence guess.
        """
        if self.confidence >= 0.60 and self.observation_count >= 2:
            return Knowledge.KNOWN
        if self.label == "unknown_object" or self.confidence < 0.45:
            return Knowledge.UNCERTAIN
        return Knowledge.UNCERTAIN if self.observation_count < 2 else Knowledge.KNOWN

    def as_dict(self) -> dict:
        return {"object_id": self.object_id, "label": self.label,
                "position": [round(self.position.x, 3), round(self.position.y, 3)],
                "confidence": round(self.confidence, 3),
                "knowledge": self.knowledge.value,
                "observations": self.observation_count,
                "last_seen_tick": self.last_seen_tick}


@dataclass
class FailureRecord:
    """A place where an action physically did not work."""

    kind: str                 # "collision" | "step_too_high" | ...
    position: Vec2
    heading: float
    tick: int
    detail: str = ""

    def as_dict(self) -> dict:
        return {"kind": self.kind,
                "position": [round(self.position.x, 3), round(self.position.y, 3)],
                "heading": round(self.heading, 3), "tick": self.tick,
                "detail": self.detail}


class WorldModel:
    def __init__(self, width_m: float, height_m: float, resolution: float = 0.25):
        self.occupancy = OccupancyBelief(width_m, height_m, resolution)
        self.objects: dict[str, ObjectBelief] = {}
        self.failures: list[FailureRecord] = []
        self.successes: list[dict] = []
        self.pose_estimate: Pose | None = None
        self.pose_confidence: float = 0.0
        self.home: Vec2 | None = None
        self.visited: set[tuple[int, int]] = set()
        self.revealed_cells: int = 0

    # -- pose --------------------------------------------------------------
    def set_pose(self, pose: Pose, confidence: float) -> None:
        self.pose_estimate = pose
        self.pose_confidence = confidence
        self.visited.add(self.occupancy.to_cell(pose.x, pose.y))
        if self.home is None:
            self.home = Vec2(pose.x, pose.y)

    # -- objects -----------------------------------------------------------
    def observe_object(self, object_id: str, label: str, position: Vec2,
                       confidence: float, tick: int) -> bool:
        """Fold one detection in. Returns True if this was a NEW object."""
        b = self.objects.get(object_id)
        if b is None:
            b = ObjectBelief(object_id, label, position, confidence, tick, tick)
            b.labels_seen[label] = 1
            self.objects[object_id] = b
            return True
        # Higher-confidence observations dominate; a confident specific label
        # replaces a low-confidence "unknown_object".
        b.observation_count += 1
        b.last_seen_tick = tick
        b.labels_seen[label] = b.labels_seen.get(label, 0) + 1
        if confidence >= b.confidence or b.label == "unknown_object":
            w = 0.65
            b.position = Vec2(b.position.x * (1 - w) + position.x * w,
                              b.position.y * (1 - w) + position.y * w)
            if label != "unknown_object":
                b.label = label
            b.confidence = max(b.confidence, confidence)
        return False

    def find_by_label(self, label: str) -> ObjectBelief | None:
        hits = [b for b in self.objects.values() if b.label == label]
        if not hits:
            return None
        return max(hits, key=lambda b: (b.confidence, b.observation_count))

    # -- outcomes ----------------------------------------------------------
    def record_failure(self, kind: str, position: Vec2, heading: float,
                       tick: int, detail: str = "") -> None:
        self.failures.append(FailureRecord(kind, position, heading, tick, detail))

    def record_success(self, action: str, position: Vec2, tick: int) -> None:
        self.successes.append({"action": action, "tick": tick,
                               "position": [round(position.x, 3),
                                            round(position.y, 3)]})

    def mark_blocked_ahead(self, position: Vec2, heading: float,
                           standoff: float, half_width: float = 0.30) -> int:
        """Write the blockage a stopped motion just proved into the grid.

        A chassis that stopped proves something solid spans its WIDTH, not a
        single point, so three samples across the front are marked. Marking
        one cell left the planner free to route around it into the same
        obstacle.
        """
        c, s = math.cos(heading), math.sin(heading)
        nx, ny = -s, c                       # lateral unit vector
        marked = 0
        for lateral in (-half_width, 0.0, half_width):
            px = position.x + c * standoff + nx * lateral
            py = position.y + s * standoff + ny * lateral
            cx, cy = self.occupancy.to_cell(px, py)
            if self.occupancy.in_bounds(cx, cy):
                self.occupancy.force_blocked(cx, cy)
                marked += 1
        return marked

    # -- summaries ---------------------------------------------------------
    def knowledge_of(self, x: float, y: float) -> Knowledge:
        s = self.occupancy.at(x, y)
        if s is CellState.UNKNOWN:
            return Knowledge.UNKNOWN
        if s is CellState.UNCERTAIN:
            return Knowledge.UNCERTAIN
        return Knowledge.KNOWN

    def summary(self) -> dict:
        counts = self.occupancy.counts()
        return {
            "cells": counts,
            "known_cells": self.occupancy.known_cells(),
            "frontiers": len(self.occupancy.frontier_cells()),
            "objects": {k: v.as_dict() for k, v in sorted(self.objects.items())},
            "failures": len(self.failures),
            "visited_cells": len(self.visited),
            "pose_confidence": round(self.pose_confidence, 3),
        }
