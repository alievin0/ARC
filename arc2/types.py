"""Shared value types. Deliberately small and dependency-free."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum


class MobilityMode(str, Enum):
    """How ARC-2 is currently contacting the ground.

    WHEEL is fast and efficient but cannot negotiate steps.
    LEG is slow but can climb. Switching costs time.
    """

    WHEEL = "wheel"
    LEG = "leg"


class ActionStatus(str, Enum):
    """Outcome of a robot API call.

    A status must be earned by a measured outcome, never by the absence of an
    exception. `move` that hits a wall returns BLOCKED with the distance it
    actually travelled -- it does not return SUCCESS because nothing threw.
    """

    SUCCESS = "success"       # commanded effect achieved within tolerance
    PARTIAL = "partial"       # some progress, stopped early by the world
    BLOCKED = "blocked"       # world physically prevented the action
    REFUSED = "refused"       # robot's own capabilities forbid it (e.g. wrong mode)
    INVALID = "invalid"       # malformed request
    FAILED = "failed"         # attempted, produced no effect, reason unknown


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def __add__(self, o: "Vec2") -> "Vec2":
        return Vec2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vec2") -> "Vec2":
        return Vec2(self.x - o.x, self.y - o.y)

    def scaled(self, k: float) -> "Vec2":
        return Vec2(self.x * k, self.y * k)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def distance_to(self, o: "Vec2") -> float:
        return math.hypot(self.x - o.x, self.y - o.y)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass(frozen=True)
class Pose:
    """Planar pose plus ground height. z is terrain elevation, not a DOF."""

    x: float
    y: float
    heading: float  # radians, 0 = +x, CCW positive
    z: float = 0.0

    @property
    def position(self) -> Vec2:
        return Vec2(self.x, self.y)

    def as_dict(self) -> dict:
        return {"x": round(self.x, 4), "y": round(self.y, 4),
                "heading": round(self.heading, 4), "z": round(self.z, 4)}


def wrap_angle(a: float) -> float:
    """Wrap to (-pi, pi]."""
    a = math.fmod(a + math.pi, 2 * math.pi)
    if a <= 0:
        a += 2 * math.pi
    return a - math.pi


def angle_diff(a: float, b: float) -> float:
    """Signed smallest rotation taking b to a."""
    return wrap_angle(a - b)
