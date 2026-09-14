"""ARC-2 abstract embodiment for Milestone 1.

DIMENSIONS HERE ARE PROVISIONAL. They are a functional test platform, not a
mechanical design. Nothing downstream may treat them as validated hardware
specification -- they exist so the simulation has a body with a size, a
footprint, and sensor mounting points.

The one geometric fact that IS a requirement rather than a placeholder:
the sensor mast sits on the FRONT THIRD of the chassis, on the longitudinal
centreline. Not the middle. `MAST_MOUNT` encodes that and
tests/test_embodiment.py asserts it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from arc2.types import MobilityMode, Pose, Vec2

# --- provisional chassis envelope (metres) --------------------------------
BODY_LENGTH = 0.90
BODY_WIDTH = 0.60
BODY_HEIGHT = 0.28
GROUND_CLEARANCE = 0.16

#: Collision radius. A disc is a deliberate simplification: it makes
#: traversability a single well-defined question at this milestone.
COLLISION_RADIUS = 0.40

# --- sensor mast ----------------------------------------------------------
#: Body frame: +x forward, +y left, origin at the chassis centroid.
#: The chassis spans x in [-0.45, +0.45]; its front third is [+0.15, +0.45];
#: the centre of that front third is +0.30.
MAST_MOUNT = Vec2(0.30, 0.0)
MAST_HEIGHT = 0.62
HEAD_PAN_LIMIT = math.radians(120.0)
HEAD_TILT_LIMIT = math.radians(35.0)


@dataclass(frozen=True)
class ModeCapability:
    """What a mobility mode can physically do.

    These are the numbers that make the staircase a real gate rather than a
    scripted refusal: WHEEL simply cannot lift 0.18 m.
    """

    max_speed_mps: float
    max_step_height_m: float
    max_turn_rate_rps: float
    energy_per_metre: float


MODE_CAPABILITIES: dict[MobilityMode, ModeCapability] = {
    MobilityMode.WHEEL: ModeCapability(
        max_speed_mps=0.90, max_step_height_m=0.06,
        max_turn_rate_rps=1.20, energy_per_metre=1.0),
    MobilityMode.LEG: ModeCapability(
        max_speed_mps=0.32, max_step_height_m=0.25,
        max_turn_rate_rps=0.70, energy_per_metre=3.4),
}

MODE_CHANGE_SECONDS = 4.0


@dataclass(frozen=True)
class LimbSpec:
    """One of four locomotion limbs. Each carries a wheel at its foot."""

    name: str
    mount: Vec2            # body frame
    joints: tuple[str, ...] = ("hip", "knee", "wheel")


LIMBS: tuple[LimbSpec, ...] = (
    LimbSpec("front_left", Vec2(0.32, 0.26)),
    LimbSpec("front_right", Vec2(0.32, -0.26)),
    LimbSpec("rear_left", Vec2(-0.32, 0.26)),
    LimbSpec("rear_right", Vec2(-0.32, -0.26)),
)

#: Every articulated DOF, in a stable order. Proprioception reports these.
JOINT_NAMES: tuple[str, ...] = tuple(
    f"{limb.name}.{j}" for limb in LIMBS for j in limb.joints
) + ("mast.pan", "mast.tilt")


def body_to_world(pose: Pose, body_point: Vec2) -> Vec2:
    """Transform a point from body frame into world frame."""
    c, s = math.cos(pose.heading), math.sin(pose.heading)
    return Vec2(pose.x + body_point.x * c - body_point.y * s,
                pose.y + body_point.x * s + body_point.y * c)


def sensor_head_position(pose: Pose) -> Vec2:
    """World-frame planar position of the sensor head.

    Every exteroceptive sensor rays from HERE, not from the chassis centre.
    Because the mast is forward of centre, the robot can see slightly around
    a corner it has not yet driven its body into -- a real consequence of the
    mounting choice, not a cosmetic detail.
    """
    return body_to_world(pose, MAST_MOUNT)


def sensor_head_height(pose: Pose) -> float:
    return pose.z + GROUND_CLEARANCE + BODY_HEIGHT + MAST_HEIGHT


def describe() -> dict:
    """Machine-readable summary of the embodiment, for the episode log."""
    return {
        "provisional": True,
        "body_length_m": BODY_LENGTH,
        "body_width_m": BODY_WIDTH,
        "collision_radius_m": COLLISION_RADIUS,
        "mast_mount_body_frame": {"x": MAST_MOUNT.x, "y": MAST_MOUNT.y},
        "mast_mount_note": "front third of chassis, longitudinal centreline",
        "mast_height_m": MAST_HEIGHT,
        "limbs": [l.name for l in LIMBS],
        "joints": list(JOINT_NAMES),
        "modes": {m.value: vars(c) for m, c in MODE_CAPABILITIES.items()},
    }
