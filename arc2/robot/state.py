"""The robot's own physical state, as ARC-2 itself would report it."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from arc2.robot import embodiment as emb
from arc2.types import MobilityMode, Pose


@dataclass
class RobotState:
    pose: Pose
    mode: MobilityMode = MobilityMode.WHEEL
    joint_positions: dict[str, float] = field(default_factory=dict)
    joint_velocities: dict[str, float] = field(default_factory=dict)
    mast_pan: float = 0.0
    mast_tilt: float = 0.0
    carrying: list[str] = field(default_factory=list)
    distance_travelled_m: float = 0.0
    energy_used: float = 0.0
    elapsed_s: float = 0.0
    moving: bool = False

    def __post_init__(self) -> None:
        if not self.joint_positions:
            self.joint_positions = {n: 0.0 for n in emb.JOINT_NAMES}
        if not self.joint_velocities:
            self.joint_velocities = {n: 0.0 for n in emb.JOINT_NAMES}

    @property
    def capability(self) -> emb.ModeCapability:
        return emb.MODE_CAPABILITIES[self.mode]

    def as_dict(self) -> dict:
        return {
            "pose": self.pose.as_dict(),
            "mode": self.mode.value,
            "mast_pan": round(self.mast_pan, 4),
            "mast_tilt": round(self.mast_tilt, 4),
            "carrying": list(self.carrying),
            "distance_travelled_m": round(self.distance_travelled_m, 4),
            "energy_used": round(self.energy_used, 3),
            "elapsed_s": round(self.elapsed_s, 3),
            "moving": self.moving,
        }


def update_joint_kinematics(state: RobotState, travelled: float) -> None:
    """Advance a plausible joint signature for the distance just covered.

    This is a kinematic stand-in, NOT a gait controller. Its only job is to
    give proprioception something structured and mode-dependent to report, so
    that a downstream consumer of joint state has a real signal to read.
    """
    if state.mode is MobilityMode.WHEEL:
        wheel_radius = 0.11
        d_theta = travelled / wheel_radius
        for limb in emb.LIMBS:
            state.joint_positions[f"{limb.name}.wheel"] = (
                state.joint_positions[f"{limb.name}.wheel"] + d_theta) % (2 * math.pi)
            state.joint_velocities[f"{limb.name}.wheel"] = d_theta
            state.joint_positions[f"{limb.name}.knee"] = 0.0
            state.joint_velocities[f"{limb.name}.knee"] = 0.0
    else:
        stride = 0.34
        phase = (state.distance_travelled_m / stride) * 2 * math.pi
        for i, limb in enumerate(emb.LIMBS):
            offset = math.pi * (i % 2)
            state.joint_positions[f"{limb.name}.hip"] = 0.35 * math.sin(phase + offset)
            state.joint_positions[f"{limb.name}.knee"] = 0.55 + 0.25 * math.cos(
                phase + offset)
            state.joint_velocities[f"{limb.name}.hip"] = 0.35 * math.cos(phase + offset)
            state.joint_velocities[f"{limb.name}.wheel"] = 0.0
    state.joint_positions["mast.pan"] = state.mast_pan
    state.joint_positions["mast.tilt"] = state.mast_tilt
