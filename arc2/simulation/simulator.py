"""The simulator: sole owner of ground truth, the clock, and the RNG.

Determinism contract
--------------------
Every stochastic value in the whole system is drawn from `self.rng`, a single
`random.Random` seeded at construction. Nothing else may call the `random`
module. Reset restores the seed, so `reset()` then replaying the same action
sequence reproduces the episode exactly.

Nothing above the `sensors` and `control` layers may hold a reference to this
object. The agent gets a RobotAPI and nothing else.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

from arc2.robot import embodiment as emb
from arc2.robot.state import RobotState, update_joint_kinematics
from arc2.simulation import physics
from arc2.simulation.world_spec import (WorldSpec, build_world, elevation_at)
from arc2.types import MobilityMode, Pose, Vec2, wrap_angle


@dataclass
class SimConfig:
    seed: int = 20260914
    sensor_noise: bool = True
    #: Seconds of simulated time charged per tick of pure overhead
    #: (an action that does nothing still costs the robot something).
    overhead_s: float = 0.05


class Simulator:
    def __init__(self, config: SimConfig | None = None) -> None:
        self.config = config or SimConfig()
        self.spec: WorldSpec = build_world()
        self.rng = random.Random(self.config.seed)
        self.tick = 0
        self.state = RobotState(
            pose=Pose(self.spec.start.x, self.spec.start.y,
                      self.spec.start_heading,
                      elevation_at(self.spec, self.spec.start)))

    # -- lifecycle ---------------------------------------------------------
    def reset(self) -> None:
        """Restore the world, the robot and the RNG to their initial state."""
        self.spec = build_world()
        self.rng = random.Random(self.config.seed)
        self.tick = 0
        self.state = RobotState(
            pose=Pose(self.spec.start.x, self.spec.start.y,
                      self.spec.start_heading,
                      elevation_at(self.spec, self.spec.start)))

    def advance(self, seconds: float) -> None:
        self.tick += 1
        self.state.elapsed_s += seconds + self.config.overhead_s

    # -- motion ------------------------------------------------------------
    def translate(self, distance: float, allow_push: bool = False
                  ) -> physics.MoveOutcome:
        cap = self.state.capability
        push_strength = 1.0 if allow_push else 0.0
        out = physics.attempt_move(self.spec, self.state.pose, self.state.mode,
                                   distance, emb.COLLISION_RADIUS,
                                   allow_push, push_strength)
        self.state.pose = out.final_pose
        self.state.distance_travelled_m += out.travelled
        self.state.energy_used += out.travelled * cap.energy_per_metre
        update_joint_kinematics(self.state, out.travelled)
        self.advance(out.travelled / cap.max_speed_mps if cap.max_speed_mps else 0.0)
        return out

    def rotate(self, delta: float) -> float:
        cap = self.state.capability
        p = self.state.pose
        new_heading = wrap_angle(p.heading + delta)
        candidate = Pose(p.x, p.y, new_heading, p.z)
        # Rotation in place cannot collide -- the footprint is a disc.
        self.state.pose = candidate
        self.advance(abs(delta) / cap.max_turn_rate_rps if cap.max_turn_rate_rps else 0.0)
        return delta

    def set_mode(self, mode: MobilityMode) -> bool:
        if mode is self.state.mode:
            self.advance(0.0)
            return False
        self.state.mode = mode
        self.advance(emb.MODE_CHANGE_SECONDS)
        return True

    def aim_head(self, pan: float, tilt: float) -> tuple[float, float]:
        pan = max(-emb.HEAD_PAN_LIMIT, min(emb.HEAD_PAN_LIMIT, pan))
        tilt = max(-emb.HEAD_TILT_LIMIT, min(emb.HEAD_TILT_LIMIT, tilt))
        travel = abs(pan - self.state.mast_pan) + abs(tilt - self.state.mast_tilt)
        self.state.mast_pan, self.state.mast_tilt = pan, tilt
        self.state.joint_positions["mast.pan"] = pan
        self.state.joint_positions["mast.tilt"] = tilt
        self.advance(travel / 1.8)
        return pan, tilt

    # -- objects -----------------------------------------------------------
    def payload_within(self, oid: str, reach: float) -> bool:
        p = self._payload(oid)
        if p is None or p.carried:
            return False
        return Vec2(self.state.pose.x, self.state.pose.y).distance_to(p.position) <= reach

    def pick_up(self, oid: str) -> bool:
        p = self._payload(oid)
        if p is None or p.carried:
            return False
        p.carried = True
        self.state.carrying.append(oid)
        self.advance(1.5)
        return True

    def place(self, oid: str) -> bool:
        p = self._payload(oid)
        if p is None or not p.carried:
            return False
        p.carried = False
        p.position = Vec2(self.state.pose.x, self.state.pose.y)
        self.state.carrying.remove(oid)
        self.advance(1.5)
        return True

    def _payload(self, oid: str):
        return next((p for p in self.spec.payloads if p.oid == oid), None)

    # -- ground-truth queries, for the BENCHMARK only ----------------------
    def truth_snapshot(self) -> dict:
        return {
            "tick": self.tick,
            "robot": self.state.as_dict(),
            "movables": {m.oid: [round(m.position.x, 3), round(m.position.y, 3)]
                         for m in self.spec.movables},
            "payloads": {p.oid: {"pos": [round(p.position.x, 3),
                                         round(p.position.y, 3)],
                                 "carried": p.carried}
                         for p in self.spec.payloads},
        }
