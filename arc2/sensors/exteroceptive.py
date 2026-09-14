"""LiDAR, depth and RGB. All three ray from the mast head, not the chassis."""
from __future__ import annotations

import math

from arc2.robot import embodiment as emb
from arc2.sensors.base import (DepthFrame, Detection, LidarScan, RgbFrame,
                               Sensor)
from arc2.simulation.geometry import raycast, segment_blocked
from arc2.simulation.physics import blocking_boxes
from arc2.types import Vec2, wrap_angle

LIDAR_BEAMS = 72              # 5-degree spacing
LIDAR_MAX_RANGE = 5.0
LIDAR_SIGMA = 0.02

DEPTH_COLS = 32
DEPTH_FOV = math.radians(70.0)
DEPTH_MAX_RANGE = 5.0
DEPTH_SIGMA = 0.015

RGB_FOV = math.radians(70.0)
RGB_MAX_RANGE = 6.5
#: Beyond this range the classifier stops committing to a specific label.
RGB_CONFIDENT_RANGE = 3.2


class Lidar360(Sensor):
    """360-degree planar scan from the sensor head.

    Limited range is the primary source of partial observability: beyond
    LIDAR_MAX_RANGE the world is not "empty", it is UNOBSERVED, and the
    perception layer is required to preserve that distinction.
    """

    name = "lidar_360"

    def read(self, sim) -> LidarScan:
        pose = sim.state.pose
        origin = emb.sensor_head_position(pose)
        boxes = blocking_boxes(sim.spec)
        bearings, ranges = [], []
        for i in range(LIDAR_BEAMS):
            b = -math.pi + (2 * math.pi) * i / LIDAR_BEAMS
            dist, _ = raycast(origin, wrap_angle(pose.heading + b),
                              boxes, LIDAR_MAX_RANGE)
            if sim.config.sensor_noise and dist < LIDAR_MAX_RANGE:
                dist = max(0.0, dist + sim.rng.gauss(0.0, LIDAR_SIGMA))
            bearings.append(b)
            ranges.append(min(dist, LIDAR_MAX_RANGE))
        return LidarScan(bearings, ranges, LIDAR_MAX_RANGE,
                         emb.sensor_head_height(pose))


class DepthCamera(Sensor):
    """Forward-facing depth. Narrower and denser than the LiDAR."""

    name = "depth_front"

    def read(self, sim) -> DepthFrame:
        pose = sim.state.pose
        origin = emb.sensor_head_position(pose)
        boxes = blocking_boxes(sim.spec)
        aim = pose.heading + sim.state.mast_pan
        bearings, ranges = [], []
        for i in range(DEPTH_COLS):
            frac = (i + 0.5) / DEPTH_COLS - 0.5
            b = frac * DEPTH_FOV
            dist, _ = raycast(origin, wrap_angle(aim + b), boxes, DEPTH_MAX_RANGE)
            if sim.config.sensor_noise and dist < DEPTH_MAX_RANGE:
                dist = max(0.0, dist + sim.rng.gauss(0.0, DEPTH_SIGMA))
            bearings.append(b)
            ranges.append(min(dist, DEPTH_MAX_RANGE))
        return DepthFrame(bearings, ranges, DEPTH_FOV, DEPTH_MAX_RANGE)


class RgbCamera(Sensor):
    """Semantic front camera.

    Returns detections, not pixels -- see sensors/base.py for why. Two honest
    limitations are modelled because they change what the agent can conclude:

      * occlusion -- a thing behind a wall is not detected at all;
      * label uncertainty -- past RGB_CONFIDENT_RANGE the classifier degrades
        to "unknown_object" with low confidence, so the world model gets an
        UNCERTAIN entry rather than a fact.
    """

    name = "rgb_front"

    def read(self, sim) -> RgbFrame:
        pose = sim.state.pose
        origin = emb.sensor_head_position(pose)
        aim = wrap_angle(pose.heading + sim.state.mast_pan)
        occluders = blocking_boxes(sim.spec)
        dets: list[Detection] = []

        candidates = []
        for o in sim.spec.obstacles:
            if o.kind != "wall":
                candidates.append((o.oid, o.box.center, o.label))
        for m in sim.spec.movables:
            candidates.append((m.oid, m.position, m.label))
        for p in sim.spec.payloads:
            if not p.carried:
                candidates.append((p.oid, p.position, p.label))

        for oid, pos, label in candidates:
            d = origin.distance_to(pos)
            if d > RGB_MAX_RANGE or d < 1e-6:
                continue
            bearing = wrap_angle(math.atan2(pos.y - origin.y, pos.x - origin.x) - aim)
            if abs(bearing) > RGB_FOV / 2.0:
                continue
            if segment_blocked(origin, pos,
                               [(i, b) for i, b in occluders if i != oid]):
                continue

            if d <= RGB_CONFIDENT_RANGE:
                conf = max(0.55, 0.97 - 0.10 * d)
                seen_label = label
            else:
                conf = max(0.20, 0.60 - 0.06 * (d - RGB_CONFIDENT_RANGE))
                seen_label = "unknown_object"
            if sim.config.sensor_noise:
                conf = max(0.05, min(0.99, conf + sim.rng.gauss(0.0, 0.03)))
            dets.append(Detection(oid, seen_label, bearing, d, conf))

        dets.sort(key=lambda x: (x.range_m, x.object_id))
        return RgbFrame(dets, RGB_FOV, RGB_MAX_RANGE)
