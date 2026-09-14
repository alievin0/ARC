"""Bundles the five sensors into one Observation and maintains odometry.

Pose estimate drift is modelled here rather than in the simulator because it
is a property of the SENSING, not of the world. The agent is never handed a
true pose; it is handed an estimate with a confidence.
"""
from __future__ import annotations

import math

from arc2.sensors.base import Observation, Sensor
from arc2.sensors.exteroceptive import DepthCamera, Lidar360, RgbCamera
from arc2.sensors.proprioceptive import Imu, Proprioception
from arc2.types import Pose

#: Metres of position error accumulated per metre travelled.
ODOMETRY_DRIFT_PER_M = 0.004


class SensorSuite:
    def __init__(self) -> None:
        self.lidar = Lidar360()
        self.depth = DepthCamera()
        self.rgb = RgbCamera()
        self.imu = Imu()
        self.joints = Proprioception()
        self._drift_x = 0.0
        self._drift_y = 0.0
        self._last_distance = 0.0

    def reset(self) -> None:
        self._drift_x = self._drift_y = 0.0
        self._last_distance = 0.0

    def sensors(self) -> list[Sensor]:
        return [self.lidar, self.depth, self.rgb, self.imu, self.joints]

    def read(self, sim) -> Observation:
        travelled = sim.state.distance_travelled_m - self._last_distance
        self._last_distance = sim.state.distance_travelled_m
        if travelled > 0 and sim.config.sensor_noise:
            self._drift_x += sim.rng.gauss(0.0, ODOMETRY_DRIFT_PER_M * travelled)
            self._drift_y += sim.rng.gauss(0.0, ODOMETRY_DRIFT_PER_M * travelled)

        imu = self.imu.read(sim)
        true = sim.state.pose
        estimate = Pose(true.x + self._drift_x, true.y + self._drift_y,
                        imu.heading, true.z)
        drift = math.hypot(self._drift_x, self._drift_y)
        confidence = max(0.30, 1.0 - drift / 2.0)

        return Observation(
            tick=sim.tick,
            sim_time_s=sim.state.elapsed_s,
            pose_estimate=estimate,
            pose_confidence=confidence,
            lidar=self.lidar.read(sim),
            depth=self.depth.read(sim),
            rgb=self.rgb.read(sim),
            imu=imu,
            joints=self.joints.read(sim),
            mobility_mode=sim.state.mode.value,
            carrying=list(sim.state.carrying),
        )

    def describe(self) -> list[dict]:
        return [s.describe() for s in self.sensors()]
