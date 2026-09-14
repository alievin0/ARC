"""Sensor interfaces and the structured Observation the agent receives.

DESIGN INTENT: these dataclasses are the hardware seam. A real 360 LiDAR
driver has to produce a `LidarScan` with the same fields and the same
conventions (bearings in the SENSOR frame, ranges in metres, `max_range`
meaning "nothing detected"), and everything above this line is unchanged.

We deliberately do not render pixels. `RgbFrame` carries detections, which is
what a real RGB camera plus an on-board detector would hand to a planner.
Pixel rendering is a later milestone's problem and would prove nothing now.
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from arc2.types import Pose


class Sensor(ABC):
    """Common contract. `read()` must be pure with respect to world state."""

    name: str = "sensor"

    @abstractmethod
    def read(self, sim) -> object:  # pragma: no cover - interface
        ...

    def describe(self) -> dict:
        return {"name": self.name, "type": type(self).__name__}


@dataclass
class LidarScan:
    bearings: list[float]      # radians, sensor frame, ascending
    ranges: list[float]        # metres
    max_range: float
    origin_height: float

    def as_dict(self) -> dict:
        return {"max_range": self.max_range,
                "origin_height": round(self.origin_height, 3),
                "n_beams": len(self.ranges),
                "ranges": [round(r, 3) for r in self.ranges]}


@dataclass
class DepthFrame:
    bearings: list[float]
    ranges: list[float]
    fov: float
    max_range: float

    @property
    def min_ahead(self) -> float:
        return min(self.ranges) if self.ranges else self.max_range

    def as_dict(self) -> dict:
        return {"fov": round(self.fov, 4), "max_range": self.max_range,
                "n_cols": len(self.ranges),
                "min_ahead": round(self.min_ahead, 3),
                "ranges": [round(r, 3) for r in self.ranges]}


@dataclass
class Detection:
    """One thing the camera believes it can see.

    `object_id` is present because this is a simulation; a real pipeline would
    supply a tracker id. `label` may be wrong or coarse -- that is the point.
    """

    object_id: str
    label: str
    bearing: float          # radians relative to robot heading
    range_m: float
    confidence: float

    def as_dict(self) -> dict:
        return {"object_id": self.object_id, "label": self.label,
                "bearing": round(self.bearing, 4),
                "range_m": round(self.range_m, 3),
                "confidence": round(self.confidence, 3)}


@dataclass
class RgbFrame:
    detections: list[Detection]
    fov: float
    max_range: float

    def as_dict(self) -> dict:
        return {"fov": round(self.fov, 4), "max_range": self.max_range,
                "detections": [d.as_dict() for d in self.detections]}


@dataclass
class ImuReading:
    heading: float
    pitch: float
    roll: float
    angular_velocity: float
    linear_acceleration: float
    ground_slope: float

    def as_dict(self) -> dict:
        return {k: round(v, 4) for k, v in vars(self).items()}


@dataclass
class JointStateReading:
    positions: dict[str, float]
    velocities: dict[str, float]
    mode: str

    def as_dict(self) -> dict:
        return {"mode": self.mode,
                "positions": {k: round(v, 4) for k, v in sorted(self.positions.items())},
                "velocities": {k: round(v, 4) for k, v in sorted(self.velocities.items())}}


@dataclass
class Observation:
    """Everything ARC-2 perceives at one instant. The agent sees ONLY this.

    `pose_estimate` is the robot's own belief about where it is -- it carries
    drift. It is not, and must never be, ground truth.
    """

    tick: int
    sim_time_s: float
    pose_estimate: Pose
    pose_confidence: float
    lidar: LidarScan
    depth: DepthFrame
    rgb: RgbFrame
    imu: ImuReading
    joints: JointStateReading
    mobility_mode: str
    carrying: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "tick": self.tick,
            "sim_time_s": round(self.sim_time_s, 3),
            "pose_estimate": self.pose_estimate.as_dict(),
            "pose_confidence": round(self.pose_confidence, 3),
            "mobility_mode": self.mobility_mode,
            "carrying": list(self.carrying),
            "lidar": self.lidar.as_dict(),
            "depth": self.depth.as_dict(),
            "rgb": self.rgb.as_dict(),
            "imu": self.imu.as_dict(),
            "joints": {"mode": self.joints.mode,
                       "n_joints": len(self.joints.positions)},
        }
