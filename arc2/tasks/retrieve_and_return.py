"""Benchmark task 1: find the target, retrieve it, bring it back.

What the agent is given
-----------------------
    * the LABEL of the thing to find ("canister")
    * the fact that "home" is wherever it started

What the agent is NOT given
---------------------------
    * the target's coordinates
    * the map, or which of the three routes work
    * which obstacle is movable
    * that the stairs need leg mode

Success is evaluated against GROUND TRUTH, not against the agent's belief.
An agent that thinks it delivered the payload but did not, fails.
"""
from __future__ import annotations

from dataclasses import dataclass

from arc2.simulation.simulator import Simulator
from arc2.simulation.world_spec import (RETURN_TOLERANCE_M, START_POSITION,
                                        TARGET_ID)
from arc2.types import Vec2

TASK_ID = "retrieve_and_return_v1"
TARGET_LABEL = "canister"


@dataclass
class TaskOutcome:
    success: bool
    reason: str
    target_delivered: bool
    target_carried: bool
    distance_from_home_m: float

    def as_dict(self) -> dict:
        return {"success": self.success, "reason": self.reason,
                "target_delivered": self.target_delivered,
                "target_carried": self.target_carried,
                "distance_from_home_m": round(self.distance_from_home_m, 3)}


def brief() -> dict:
    """Exactly what the agent is told at episode start."""
    return {
        "task_id": TASK_ID,
        "instruction": ("Locate an object labelled 'canister', pick it up, "
                        "and return it to the area where you started."),
        "target_label": TARGET_LABEL,
        "return_tolerance_m": RETURN_TOLERANCE_M,
        "given_target_coordinates": False,
        "given_map": False,
    }


def evaluate(sim: Simulator) -> TaskOutcome:
    """Ground-truth verdict. Called by the benchmark, never by the agent."""
    payload = next((p for p in sim.spec.payloads if p.oid == TARGET_ID), None)
    if payload is None:
        return TaskOutcome(False, "target_missing_from_world", False, False, 0.0)

    home = START_POSITION
    carried = payload.carried
    obj_pos = Vec2(sim.state.pose.x, sim.state.pose.y) if carried else payload.position
    d_home = obj_pos.distance_to(home)

    # Delivered means: the payload itself is in the start area. Carrying it
    # while standing at home also counts -- the robot brought it back.
    delivered = d_home <= RETURN_TOLERANCE_M
    if delivered:
        return TaskOutcome(True, "payload_returned_to_start_area", True,
                           carried, d_home)
    if carried:
        return TaskOutcome(False, "payload_acquired_but_not_returned", False,
                           True, d_home)
    return TaskOutcome(False, "payload_not_acquired", False, False, d_home)
