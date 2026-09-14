"""RobotAPI implemented against the simulator.

Everything this class does is translate a command into simulator calls and
then TRANSLATE THE MEASURED OUTCOME BACK into an ActionStatus. The mapping
from stop-reason to status is the whole point and is deliberately explicit:
there is no default branch that quietly returns SUCCESS.
"""
from __future__ import annotations

import math

from arc2.control.api import ActionResult, RobotAPI
from arc2.robot import embodiment as emb
from arc2.sensors.base import Observation
from arc2.sensors.suite import SensorSuite
from arc2.simulation.physics import StopReason
from arc2.simulation.simulator import Simulator
from arc2.types import ActionStatus, MobilityMode

#: How close the chassis must be to a payload to manipulate it.
REACH_M = 0.85
#: Fraction of the commanded distance below which a move counts as no progress.
PROGRESS_EPS = 0.02

_STOP_REASON_STATUS = {
    StopReason.REACHED: ActionStatus.SUCCESS,
    StopReason.COLLISION: ActionStatus.BLOCKED,
    StopReason.STEP_TOO_HIGH: ActionStatus.BLOCKED,
    StopReason.OUT_OF_BOUNDS: ActionStatus.BLOCKED,
    StopReason.PUSHED_OBJECT_STUCK: ActionStatus.BLOCKED,
}


class SimulatedRobotAPI(RobotAPI):
    def __init__(self, sim: Simulator, suite: SensorSuite | None = None) -> None:
        self._sim = sim
        self._suite = suite or SensorSuite()
        self.command_count = 0

    # -- sensing -----------------------------------------------------------
    def observe(self) -> Observation:
        self.command_count += 1
        return self._suite.read(self._sim)

    def get_robot_state(self) -> dict:
        self.command_count += 1
        obs_pose = self._sim.state.pose
        return {
            "mode": self._sim.state.mode.value,
            "carrying": list(self._sim.state.carrying),
            "distance_travelled_m": round(self._sim.state.distance_travelled_m, 4),
            "energy_used": round(self._sim.state.energy_used, 3),
            "elapsed_s": round(self._sim.state.elapsed_s, 3),
            "mast_pan": round(self._sim.state.mast_pan, 4),
            "mast_tilt": round(self._sim.state.mast_tilt, 4),
            # Elevation is proprioceptive (leg extension / pressure), so it is
            # legitimate to report; x/y are NOT reported here -- the agent must
            # use its own estimate from observe().
            "ground_elevation_m": round(obs_pose.z, 3),
        }

    # -- locomotion --------------------------------------------------------
    def move(self, distance_m: float) -> ActionResult:
        self.command_count += 1
        if distance_m < 0:
            return ActionResult("move", ActionStatus.INVALID, distance_m, 0.0,
                                "negative_distance")
        t0 = self._sim.state.elapsed_s
        out = self._sim.translate(distance_m, allow_push=False)
        status = _STOP_REASON_STATUS[out.stop_reason]
        if status is ActionStatus.BLOCKED and out.travelled > PROGRESS_EPS:
            status = ActionStatus.PARTIAL
        return ActionResult("move", status, distance_m, out.travelled,
                            out.stop_reason, out.contact_id,
                            {"mode": self._sim.state.mode.value},
                            self._sim.state.elapsed_s - t0)

    def turn(self, delta_rad: float) -> ActionResult:
        self.command_count += 1
        t0 = self._sim.state.elapsed_s
        applied = self._sim.rotate(delta_rad)
        return ActionResult("turn", ActionStatus.SUCCESS, delta_rad, applied,
                            "reached", None, {},
                            self._sim.state.elapsed_s - t0)

    def stop(self) -> ActionResult:
        self.command_count += 1
        self._sim.state.moving = False
        self._sim.advance(0.0)
        return ActionResult("stop", ActionStatus.SUCCESS, 0.0, 0.0, "halted")

    def change_mobility_mode(self, mode: MobilityMode) -> ActionResult:
        self.command_count += 1
        if not isinstance(mode, MobilityMode):
            return ActionResult("change_mobility_mode", ActionStatus.INVALID,
                                reason="unknown_mode")
        t0 = self._sim.state.elapsed_s
        changed = self._sim.set_mode(mode)
        return ActionResult(
            "change_mobility_mode",
            ActionStatus.SUCCESS if changed else ActionStatus.PARTIAL,
            0.0, 1.0 if changed else 0.0,
            "mode_changed" if changed else "already_in_mode",
            None, {"mode": mode.value},
            self._sim.state.elapsed_s - t0)

    # -- sensor aiming -----------------------------------------------------
    def look(self, pan_rad: float, tilt_rad: float = 0.0) -> ActionResult:
        self.command_count += 1
        t0 = self._sim.state.elapsed_s
        pan, tilt = self._sim.aim_head(pan_rad, tilt_rad)
        clamped = (abs(pan - pan_rad) > 1e-6) or (abs(tilt - tilt_rad) > 1e-6)
        return ActionResult(
            "look", ActionStatus.PARTIAL if clamped else ActionStatus.SUCCESS,
            pan_rad, pan, "clamped_to_limits" if clamped else "aimed", None,
            {"pan": round(pan, 4), "tilt": round(tilt, 4)},
            self._sim.state.elapsed_s - t0)

    # -- interaction -------------------------------------------------------
    def push(self, distance_m: float) -> ActionResult:
        self.command_count += 1
        if distance_m <= 0:
            return ActionResult("push", ActionStatus.INVALID, distance_m, 0.0,
                                "non_positive_distance")
        t0 = self._sim.state.elapsed_s
        before = {m.oid: (m.position.x, m.position.y) for m in self._sim.spec.movables}
        out = self._sim.translate(distance_m, allow_push=True)
        after = {m.oid: (m.position.x, m.position.y) for m in self._sim.spec.movables}
        moved = sorted(oid for oid in before if before[oid] != after[oid])
        status = _STOP_REASON_STATUS[out.stop_reason]
        if status is ActionStatus.BLOCKED and out.travelled > PROGRESS_EPS:
            status = ActionStatus.PARTIAL
        return ActionResult("push", status, distance_m, out.travelled,
                            out.stop_reason, out.contact_id,
                            {"displaced": moved}, self._sim.state.elapsed_s - t0)

    def interact(self, verb: str, target_id: str) -> ActionResult:
        self.command_count += 1
        t0 = self._sim.state.elapsed_s
        if verb == "pick_up":
            if not self._sim.payload_within(target_id, REACH_M):
                return ActionResult("interact", ActionStatus.BLOCKED, 0.0, 0.0,
                                    "out_of_reach", target_id, {"verb": verb})
            ok = self._sim.pick_up(target_id)
            return ActionResult("interact",
                                ActionStatus.SUCCESS if ok else ActionStatus.FAILED,
                                0.0, 1.0 if ok else 0.0,
                                "grasped" if ok else "grasp_failed", target_id,
                                {"verb": verb}, self._sim.state.elapsed_s - t0)
        if verb == "place":
            ok = self._sim.place(target_id)
            return ActionResult("interact",
                                ActionStatus.SUCCESS if ok else ActionStatus.FAILED,
                                0.0, 1.0 if ok else 0.0,
                                "placed" if ok else "not_carried", target_id,
                                {"verb": verb}, self._sim.state.elapsed_s - t0)
        if verb == "inspect":
            obs = self._suite.read(self._sim)
            hit = next((d for d in obs.rgb.detections if d.object_id == target_id), None)
            self._sim.advance(0.8)
            return ActionResult("interact",
                                ActionStatus.SUCCESS if hit else ActionStatus.FAILED,
                                0.0, 1.0 if hit else 0.0,
                                "inspected" if hit else "not_visible", target_id,
                                {"verb": verb,
                                 "detection": hit.as_dict() if hit else None},
                                self._sim.state.elapsed_s - t0)
        return ActionResult("interact", ActionStatus.INVALID, 0.0, 0.0,
                            "unknown_verb", target_id, {"verb": verb})

    # -- introspection -----------------------------------------------------
    def capabilities(self) -> dict:
        return {
            "embodiment": emb.describe(),
            "sensors": self._suite.describe(),
            "reach_m": REACH_M,
            "verbs": ["pick_up", "place", "inspect"],
        }
