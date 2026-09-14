"""What was tried, where, and what happened.

This is what separates replanning from retrying. Without it an agent that
re-derives the same plan from the same belief will drive into the same wall
forever; the failure key below is what lets the planner refuse a route it has
already disproved.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

from arc2.control.api import ActionResult
from arc2.types import Pose, Vec2

#: Failures are keyed by coarse cell + coarse heading so that "I failed HERE
#: going THAT WAY" generalises a little, but not so much that an unrelated
#: action elsewhere is suppressed.
FAIL_CELL_M = 0.6
FAIL_HEADING_SECTORS = 16


def failure_key(action: str, pose: Pose) -> tuple:
    cx = int(pose.x // FAIL_CELL_M)
    cy = int(pose.y // FAIL_CELL_M)
    sector = int(((pose.heading + math.pi) / (2 * math.pi)) * FAIL_HEADING_SECTORS) \
        % FAIL_HEADING_SECTORS
    return (action, cx, cy, sector)


@dataclass
class ActionRecord:
    tick: int
    action: str
    params: dict
    pose_before: Pose
    status: str
    reason: str
    achieved: float
    info_gain: int = 0

    def as_dict(self) -> dict:
        return {"tick": self.tick, "action": self.action, "params": self.params,
                "pose_before": self.pose_before.as_dict(), "status": self.status,
                "reason": self.reason, "achieved": round(self.achieved, 4),
                "info_gain": self.info_gain}


class EpisodicMemory:
    def __init__(self) -> None:
        self.records: list[ActionRecord] = []
        self.failure_counts: dict[tuple, int] = defaultdict(int)
        self.success_counts: dict[tuple, int] = defaultdict(int)
        self.abandoned_regions: list[tuple[float, float, str]] = []
        self.visit_counts: dict[tuple[int, int], int] = defaultdict(int)

    def record(self, tick: int, result: ActionResult, pose_before: Pose,
               params: dict | None = None, info_gain: int = 0) -> ActionRecord:
        rec = ActionRecord(tick, result.action, params or {}, pose_before,
                           result.status.value, result.reason, result.achieved,
                           info_gain)
        self.records.append(rec)
        key = failure_key(result.action, pose_before)
        if result.progressed:
            self.success_counts[key] += 1
        else:
            self.failure_counts[key] += 1
        self.visit_counts[(int(pose_before.x // FAIL_CELL_M),
                           int(pose_before.y // FAIL_CELL_M))] += 1
        return rec

    def has_failed(self, action: str, pose: Pose) -> bool:
        return self.failure_counts.get(failure_key(action, pose), 0) > 0

    def failures_at(self, action: str, pose: Pose) -> int:
        return self.failure_counts.get(failure_key(action, pose), 0)

    def abandon_region(self, centre: Vec2, reason: str) -> None:
        """Mark an area as disproved so the planner stops proposing it."""
        self.abandoned_regions.append((centre.x, centre.y, reason))

    def is_abandoned(self, p: Vec2, radius: float = 2.2) -> bool:
        return any(math.hypot(p.x - ax, p.y - ay) <= radius
                   for ax, ay, _ in self.abandoned_regions)

    # -- metrics -----------------------------------------------------------
    @property
    def failed_actions(self) -> int:
        return sum(1 for r in self.records
                   if r.status not in ("success", "partial"))

    @property
    def total_actions(self) -> int:
        return len(self.records)

    def unnecessary_actions(self) -> int:
        """Actions that neither changed the world nor revealed anything.

        Defined narrowly and computed from the record, not estimated: an
        action counts as unnecessary when it achieved (effectively) nothing
        AND produced no new cells, or when it repeated an action already
        recorded as failing from the same place and heading.
        """
        seen_failures: dict[tuple, int] = defaultdict(int)
        n = 0
        for r in self.records:
            key = failure_key(r.action, r.pose_before)
            failed = r.status not in ("success", "partial")
            # A failure the FIRST time proves a blockage -- that is information,
            # not waste. Repeating it after the world model already recorded it
            # is waste. This distinction is why the metric is not just a
            # synonym for failed_actions.
            repeated_known_bad = failed and seen_failures[key] > 0
            pure_noop = (not failed and abs(r.achieved) < 1e-3
                         and r.info_gain == 0)
            if repeated_known_bad or pure_noop:
                n += 1
            if failed:
                seen_failures[key] += 1
        return n

    def summary(self) -> dict:
        return {"actions": self.total_actions,
                "failed_actions": self.failed_actions,
                "unnecessary_actions": self.unnecessary_actions(),
                "abandoned_regions": len(self.abandoned_regions)}
