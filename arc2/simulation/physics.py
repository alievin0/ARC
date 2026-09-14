"""Movement resolution. Deterministic, sub-stepped, and honest about failure.

The single rule this module exists to enforce:

    An attempted motion reports the distance it ACTUALLY covered and why it
    stopped. It never reports the distance that was commanded.

Everything the agent later learns about the world's blockages is downstream
of that one property.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from arc2.robot import embodiment as emb
from arc2.simulation.geometry import AABB, circle_intersects_aabb
from arc2.simulation.world_spec import WorldSpec, elevation_at
from arc2.types import MobilityMode, Pose, Vec2

#: Motion is integrated in fixed slices so a fast move cannot tunnel through
#: a thin wall. Small enough that 0.04 m << wall thickness 0.5 m.
SUBSTEP_M = 0.04


class StopReason:
    REACHED = "reached"
    COLLISION = "collision"
    STEP_TOO_HIGH = "step_too_high"
    OUT_OF_BOUNDS = "out_of_bounds"
    PUSHED_OBJECT_STUCK = "pushed_object_stuck"


@dataclass
class MoveOutcome:
    travelled: float
    final_pose: Pose
    stop_reason: str
    contact_id: str | None = None
    pushed: list[str] | None = None


def blocking_boxes(spec: WorldSpec, ignore: set[str] | None = None
                   ) -> list[tuple[str, AABB]]:
    """Every solid thing, static or movable. Payloads are NOT solid."""
    ignore = ignore or set()
    out = [(o.oid, o.box) for o in spec.obstacles if o.oid not in ignore]
    out += [(m.oid, m.box) for m in spec.movables if m.oid not in ignore]
    return out


def _colliding(spec: WorldSpec, p: Vec2, radius: float,
               ignore: set[str] | None = None) -> str | None:
    for oid, box in blocking_boxes(spec, ignore):
        if circle_intersects_aabb(p, radius, box):
            return oid
    return None


def step_height_ok(spec: WorldSpec, frm: Vec2, to: Vec2, mode: MobilityMode) -> bool:
    """Can this mode negotiate the elevation change between two points?"""
    rise = abs(elevation_at(spec, to) - elevation_at(spec, frm))
    return rise <= emb.MODE_CAPABILITIES[mode].max_step_height_m + 1e-9


def attempt_move(spec: WorldSpec, pose: Pose, mode: MobilityMode,
                 distance: float, radius: float = emb.COLLISION_RADIUS,
                 allow_push: bool = False, push_strength: float = 0.0
                 ) -> MoveOutcome:
    """Translate along the current heading, stopping at the first thing that
    physically stops us.

    `allow_push` is what distinguishes `push()` from `move()` at the API
    level: an ordinary move that meets the crate simply stops.
    """
    if distance <= 0:
        return MoveOutcome(0.0, pose, StopReason.REACHED)

    c, s = math.cos(pose.heading), math.sin(pose.heading)
    cur = Vec2(pose.x, pose.y)
    travelled = 0.0
    pushed: list[str] = []
    n = max(1, int(math.ceil(distance / SUBSTEP_M)))
    slice_len = distance / n

    for _ in range(n):
        nxt = Vec2(cur.x + c * slice_len, cur.y + s * slice_len)

        if not (radius <= nxt.x <= spec.arena.x1 - radius
                and radius <= nxt.y <= spec.arena.y1 - radius):
            return MoveOutcome(travelled, _pose_at(spec, cur, pose.heading),
                               StopReason.OUT_OF_BOUNDS)

        if not step_height_ok(spec, cur, nxt, mode):
            return MoveOutcome(travelled, _pose_at(spec, cur, pose.heading),
                               StopReason.STEP_TOO_HIGH)

        hit = _colliding(spec, nxt, radius)
        if hit is not None:
            movable = next((m for m in spec.movables if m.oid == hit), None)
            if allow_push and movable is not None:
                if not _shift_movable(spec, movable, c, s, slice_len,
                                      push_strength, radius):
                    return MoveOutcome(travelled, _pose_at(spec, cur, pose.heading),
                                       StopReason.PUSHED_OBJECT_STUCK, hit, pushed)
                if movable.oid not in pushed:
                    pushed.append(movable.oid)
            else:
                return MoveOutcome(travelled, _pose_at(spec, cur, pose.heading),
                                   StopReason.COLLISION, hit)

        cur = nxt
        travelled += slice_len

    return MoveOutcome(travelled, _pose_at(spec, cur, pose.heading),
                       StopReason.REACHED, None, pushed)


def _pose_at(spec: WorldSpec, p: Vec2, heading: float) -> Pose:
    return Pose(p.x, p.y, heading, elevation_at(spec, p))


def _shift_movable(spec: WorldSpec, mv, c: float, s: float, dist: float,
                   push_strength: float, robot_radius: float) -> bool:
    """Try to displace a movable. False if it is wedged against something."""
    if push_strength < mv.mass_factor:
        return False
    cand = Vec2(mv.position.x + c * dist, mv.position.y + s * dist)
    half = mv.size / 2.0
    if not (half <= cand.x <= spec.arena.x1 - half
            and half <= cand.y <= spec.arena.y1 - half):
        return False
    cand_box = AABB.centered(cand.x, cand.y, mv.size, mv.size)
    for oid, box in blocking_boxes(spec, ignore={mv.oid}):
        if _boxes_overlap(cand_box, box):
            return False
    mv.position = cand
    return True


def _boxes_overlap(a: AABB, b: AABB) -> bool:
    return not (a.x1 <= b.x0 or b.x1 <= a.x0 or a.y1 <= b.y0 or b.y1 <= a.y0)


def pose_is_valid(spec: WorldSpec, pose: Pose,
                  radius: float = emb.COLLISION_RADIUS) -> bool:
    return _colliding(spec, Vec2(pose.x, pose.y), radius) is None
