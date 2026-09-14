"""Ground truth for the Milestone-1 arena.

This module is the ONLY place the true layout is written down. The agent
never imports it. Perception and the world model only ever learn about the
contents of this file through sensor returns.

Layout (x right, y up, metres). Arena is 24 x 16.

  y=16 +--------------------------------------------------------------+
       |                                                              |
       |   ROOM C  (upper)          [TARGET at 7.5,13.2]              |
       |                                                              |
       |         +-----+            (obstacles: pillars)              |
  y=9  |         |dead |    +-------+            +--------+           |
       |         | end |    |narrow |            | stairs |           |
       |         |cor- |    |passage|            | up/down|           |
  y=6  +---------+ridor+----+--[X]--+------------+--------+-----------+
       |          (sealed)          ^crate                            |
       |   ROOM A  (start)   [START/RETURN at 2.0,2.2]                |
  y=0  +--------------------------------------------------------------+
       x=0                                                        x=24

Three routes leave ROOM A through the dividing wall:

  D1 dead-end corridor  x in [3.0,4.8]  -- looks like a route, is sealed
  D2 narrow passage     x in [10.2,11.3] -- 1.1 m wide, blocked by a crate
                                            that CAN be pushed out
  D3 stair door         x in [17.8,20.2] -- a 0.18 m step staircase that
                                            WHEEL mode cannot climb

None of these facts are given to the agent. All three must be discovered,
and each one fails in a different way, requiring a different adaptation:
re-route, clear the obstruction, or change mobility mode.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from arc2.simulation.geometry import AABB
from arc2.types import Vec2

ARENA_W = 24.0
ARENA_H = 16.0
WALL_T = 0.5

START_POSITION = Vec2(2.0, 2.2)
START_HEADING = 1.5707963267948966  # +y, facing the dividing wall
RETURN_TOLERANCE_M = 1.0

TARGET_ID = "target_canister"
CRATE_ID = "crate_01"


@dataclass(frozen=True)
class StaticObstacle:
    oid: str
    box: AABB
    kind: str              # "wall" | "pillar" | "barrier"
    label: str             # what a perfect classifier would call it


@dataclass
class MovableObject:
    """An object whose pose changes when the robot pushes it."""

    oid: str
    position: Vec2
    size: float            # square footprint edge length
    mass_factor: float     # >1 means harder to shift; used by push physics
    label: str

    @property
    def box(self) -> AABB:
        return AABB.centered(self.position.x, self.position.y, self.size, self.size)


@dataclass
class Payload:
    """The retrieval target. Not an obstacle -- the robot drives over it."""

    oid: str
    position: Vec2
    size: float
    label: str
    carried: bool = False

    @property
    def box(self) -> AABB:
        return AABB.centered(self.position.x, self.position.y, self.size, self.size)


@dataclass(frozen=True)
class StairStep:
    """One tread of the staircase: a y-band at a fixed elevation."""

    box: AABB
    elevation: float


@dataclass
class WorldSpec:
    obstacles: list[StaticObstacle]
    movables: list[MovableObject]
    payloads: list[Payload]
    steps: list[StairStep]
    start: Vec2
    start_heading: float
    arena: AABB

    def static_boxes(self) -> list[tuple[str, AABB]]:
        return [(o.oid, o.box) for o in self.obstacles]


def _perimeter() -> list[StaticObstacle]:
    t, W, H = WALL_T, ARENA_W, ARENA_H
    return [
        StaticObstacle("wall_south", AABB(0.0, 0.0, W, t), "wall", "wall"),
        StaticObstacle("wall_north", AABB(0.0, H - t, W, H), "wall", "wall"),
        StaticObstacle("wall_west", AABB(0.0, 0.0, t, H), "wall", "wall"),
        StaticObstacle("wall_east", AABB(W - t, 0.0, W, H), "wall", "wall"),
    ]


def build_world() -> WorldSpec:
    """Construct the ground-truth arena. Pure function -- no randomness."""
    obs: list[StaticObstacle] = _perimeter()

    # --- dividing wall between ROOM A and the upper half, with three gaps ---
    y0, y1 = 5.5, 6.0
    for i, (a, b) in enumerate([(0.5, 3.0), (4.8, 10.2), (11.3, 17.8), (20.2, 23.5)]):
        obs.append(StaticObstacle(f"divider_{i}", AABB(a, y0, b, y1), "wall", "wall"))

    # --- D1: the dead end. Two side walls and a sealed cap. ---------------
    obs.append(StaticObstacle("deadend_w", AABB(2.5, 6.0, 3.0, 10.6), "wall", "wall"))
    obs.append(StaticObstacle("deadend_e", AABB(4.8, 6.0, 5.3, 10.6), "wall", "wall"))
    obs.append(StaticObstacle("deadend_cap", AABB(2.5, 10.6, 5.3, 11.1), "barrier",
                              "blockage"))

    # --- D2: the narrow passage, 1.1 m clear between the side walls -------
    obs.append(StaticObstacle("passage_w", AABB(9.7, 6.0, 10.2, 9.0), "wall", "wall"))
    obs.append(StaticObstacle("passage_e", AABB(11.3, 6.0, 11.8, 9.0), "wall", "wall"))

    # --- D3: the stair shaft ----------------------------------------------
    obs.append(StaticObstacle("stair_w", AABB(17.3, 6.0, 17.8, 9.6), "wall", "wall"))
    obs.append(StaticObstacle("stair_e", AABB(20.2, 6.0, 20.7, 9.6), "wall", "wall"))

    # --- scattered obstacles, both rooms ----------------------------------
    for i, (cx, cy, w, h) in enumerate([
        (7.0, 3.2, 1.2, 1.2),
        (15.5, 2.4, 1.6, 0.9),
        (20.0, 3.6, 1.0, 1.0),
        (16.0, 12.0, 1.4, 1.4),
        # Kept well clear of the narrow passage's mouth at (10.75, 9.0): a
        # pillar closer than the crate's push corridor wedges the crate across
        # the exit and traps the robot inside the passage.
        (13.6, 11.2, 0.9, 2.2),
    ]):
        obs.append(StaticObstacle(f"pillar_{i}", AABB.centered(cx, cy, w, h),
                                  "pillar", "obstacle"))

    # --- staircase: up to a landing, then back down ------------------------
    sx0, sx1 = 17.8, 20.2
    steps = [
        StairStep(AABB(sx0, 6.2, sx1, 6.9), 0.18),
        StairStep(AABB(sx0, 6.9, sx1, 7.6), 0.36),
        StairStep(AABB(sx0, 7.6, sx1, 8.2), 0.54),   # landing
        StairStep(AABB(sx0, 8.2, sx1, 8.7), 0.36),
        StairStep(AABB(sx0, 8.7, sx1, 9.2), 0.18),
    ]

    movables = [
        MovableObject(CRATE_ID, Vec2(10.75, 7.4), 0.70, 1.0, "crate"),
    ]
    payloads = [
        Payload(TARGET_ID, Vec2(7.5, 13.2), 0.30, "canister"),
    ]

    return WorldSpec(
        obstacles=obs,
        movables=movables,
        payloads=payloads,
        steps=steps,
        start=START_POSITION,
        start_heading=START_HEADING,
        arena=AABB(0.0, 0.0, ARENA_W, ARENA_H),
    )


def elevation_at(spec: WorldSpec, p: Vec2) -> float:
    """Ground height under a point. Flat everywhere except the staircase."""
    for s in spec.steps:
        if s.box.contains_point(p):
            return s.elevation
    return 0.0
