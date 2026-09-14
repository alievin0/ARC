"""Exact 2-D geometry primitives. No approximation, no randomness.

Everything the simulator needs to answer "can the robot be here?" and
"what does a ray hit?" lives here so those two questions have exactly one
implementation and can be unit-tested in isolation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from arc2.types import Vec2

EPS = 1e-9


@dataclass(frozen=True)
class AABB:
    """Axis-aligned box. min corner inclusive, max corner exclusive-ish (EPS)."""

    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self) -> None:
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise ValueError(f"degenerate AABB {self}")

    @property
    def center(self) -> Vec2:
        return Vec2((self.x0 + self.x1) / 2.0, (self.y0 + self.y1) / 2.0)

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    def contains_point(self, p: Vec2) -> bool:
        return self.x0 <= p.x <= self.x1 and self.y0 <= p.y <= self.y1

    def translated(self, dx: float, dy: float) -> "AABB":
        return AABB(self.x0 + dx, self.y0 + dy, self.x1 + dx, self.y1 + dy)

    @staticmethod
    def centered(cx: float, cy: float, w: float, h: float) -> "AABB":
        return AABB(cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)


def closest_point_on_aabb(box: AABB, p: Vec2) -> Vec2:
    return Vec2(min(max(p.x, box.x0), box.x1), min(max(p.y, box.y0), box.y1))


def circle_intersects_aabb(center: Vec2, radius: float, box: AABB) -> bool:
    """True if the disc of `radius` about `center` overlaps `box`."""
    q = closest_point_on_aabb(box, center)
    return (center.x - q.x) ** 2 + (center.y - q.y) ** 2 < radius * radius - EPS


def penetration_depth(center: Vec2, radius: float, box: AABB) -> float:
    """How deep the disc is inside the box. 0.0 if not overlapping."""
    q = closest_point_on_aabb(box, center)
    d = math.hypot(center.x - q.x, center.y - q.y)
    return max(0.0, radius - d)


def ray_aabb(origin: Vec2, dx: float, dy: float, box: AABB,
             max_range: float) -> float | None:
    """Slab method. Returns distance along the ray to the first hit, or None.

    A ray starting inside the box returns 0.0 -- callers must decide whether
    that is a hit or a degenerate self-collision.
    """
    tmin, tmax = 0.0, max_range

    for o, d, lo, hi in ((origin.x, dx, box.x0, box.x1),
                         (origin.y, dy, box.y0, box.y1)):
        if abs(d) < EPS:
            if o < lo or o > hi:
                return None
            continue
        inv = 1.0 / d
        t0, t1 = (lo - o) * inv, (hi - o) * inv
        if t0 > t1:
            t0, t1 = t1, t0
        tmin = max(tmin, t0)
        tmax = min(tmax, t1)
        if tmin > tmax:
            return None

    if tmin > max_range:
        return None
    return tmin


def raycast(origin: Vec2, heading: float, boxes: list[tuple[str, AABB]],
            max_range: float) -> tuple[float, str | None]:
    """Cast one ray. Returns (distance, id_of_thing_hit).

    Occlusion is exact: the nearest hit wins, so anything behind it is
    invisible. This is what makes partial observability real rather than
    a rule the agent is asked to obey.
    """
    dx, dy = math.cos(heading), math.sin(heading)
    best_t, best_id = max_range, None
    for oid, box in boxes:
        t = ray_aabb(origin, dx, dy, box, max_range)
        if t is not None and t < best_t:
            best_t, best_id = t, oid
    return best_t, best_id


def segment_blocked(a: Vec2, b: Vec2, boxes: list[tuple[str, AABB]]) -> bool:
    """True if the straight segment a->b passes through any box."""
    d = b - a
    dist = d.length()
    if dist < EPS:
        return False
    heading = math.atan2(d.y, d.x)
    t, _ = raycast(a, heading, boxes, dist)
    return t < dist - EPS
