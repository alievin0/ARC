"""Observation -> world-model update. The only writer of sensed knowledge.

The invariant this module is responsible for:

    A cell is written ONLY if a ray actually reached it. Everything past a
    ray's terminal range stays UNKNOWN. An empty return at max range means
    "I could not see that far", not "it is clear out to 5 m and empty beyond".

tests/test_perception.py proves this in the direction that matters: that
cells beyond the LiDAR horizon remain UNKNOWN after a scan.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from arc2.robot import embodiment as emb
from arc2.sensors.base import Observation
from arc2.types import Vec2, wrap_angle
from arc2.world.model import WorldModel

#: Step along a ray when marking free space. Half the grid resolution so no
#: cell is skipped.
RAY_STEP = 0.12
#: Confidence below which a detection is folded in but never promoted.
MIN_DETECTION_CONF = 0.18


@dataclass
class PerceptionReport:
    new_cells: int
    new_objects: list[str]
    updated_objects: list[str]
    blocked_marks: int
    slope_detected: bool

    def as_dict(self) -> dict:
        return {"new_cells": self.new_cells, "new_objects": self.new_objects,
                "updated_objects": self.updated_objects,
                "blocked_marks": self.blocked_marks,
                "slope_detected": self.slope_detected}


def integrate(model: WorldModel, obs: Observation) -> PerceptionReport:
    """Fold one observation into the belief. Returns what it changed."""
    model.set_pose(obs.pose_estimate, obs.pose_confidence)
    # Rays leave the sensor head, which is on the mast at the front third of
    # the chassis -- NOT the chassis centre. Integrating from the wrong origin
    # writes free space into walls.
    origin = emb.sensor_head_position(obs.pose_estimate)

    new_cells = 0
    blocked = 0

    for bearing, rng in zip(obs.lidar.bearings, obs.lidar.ranges):
        world_bearing = wrap_angle(obs.pose_estimate.heading + bearing)
        c, s = math.cos(world_bearing), math.sin(world_bearing)
        hit = rng < obs.lidar.max_range - 1e-6

        # Free space along the ray, stopping just short of the return.
        span = rng - (RAY_STEP if hit else 0.0)
        steps = int(span / RAY_STEP)
        for k in range(steps):
            d = (k + 0.5) * RAY_STEP
            cx, cy = model.occupancy.to_cell(origin.x + c * d, origin.y + s * d)
            if model.occupancy.mark_free(cx, cy):
                new_cells += 1

        if hit:
            cx, cy = model.occupancy.to_cell(origin.x + c * rng, origin.y + s * rng)
            if model.occupancy.mark_blocked(cx, cy):
                new_cells += 1
            blocked += 1
        # No `else`. A beam that saw nothing writes NOTHING past its horizon.

    new_objs, upd_objs = [], []
    for det in obs.rgb.detections:
        if det.confidence < MIN_DETECTION_CONF:
            continue
        wb = wrap_angle(obs.pose_estimate.heading + det.bearing)
        pos = Vec2(origin.x + math.cos(wb) * det.range_m,
                   origin.y + math.sin(wb) * det.range_m)
        is_new = model.observe_object(det.object_id, det.label, pos,
                                      det.confidence, obs.tick)
        (new_objs if is_new else upd_objs).append(det.object_id)

    model.revealed_cells += new_cells
    return PerceptionReport(new_cells, sorted(new_objs), sorted(upd_objs),
                            blocked, abs(obs.imu.ground_slope) > 0.12)
