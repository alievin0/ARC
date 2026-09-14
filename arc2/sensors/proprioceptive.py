"""IMU and joint state -- what ARC-2 knows about itself without looking."""
from __future__ import annotations

import math

from arc2.sensors.base import ImuReading, JointStateReading, Sensor
from arc2.simulation.world_spec import elevation_at
from arc2.types import Vec2

IMU_HEADING_SIGMA = 0.008
IMU_ACC_SIGMA = 0.02


class Imu(Sensor):
    """Attitude plus the local ground slope under the wheels.

    `ground_slope` is the signal that tells the agent it is on a staircase
    before a motion has failed -- it is measured, not announced.
    """

    name = "imu"

    def read(self, sim) -> ImuReading:
        pose = sim.state.pose
        probe = 0.35
        ahead = Vec2(pose.x + math.cos(pose.heading) * probe,
                     pose.y + math.sin(pose.heading) * probe)
        rise = elevation_at(sim.spec, ahead) - pose.z
        slope = math.atan2(rise, probe)

        heading = pose.heading
        acc = 0.0
        if sim.config.sensor_noise:
            heading += sim.rng.gauss(0.0, IMU_HEADING_SIGMA)
            acc += sim.rng.gauss(0.0, IMU_ACC_SIGMA)
        return ImuReading(heading=heading, pitch=slope, roll=0.0,
                          angular_velocity=0.0, linear_acceleration=acc,
                          ground_slope=slope)


class Proprioception(Sensor):
    name = "joint_state"

    def read(self, sim) -> JointStateReading:
        return JointStateReading(positions=dict(sim.state.joint_positions),
                                 velocities=dict(sim.state.joint_velocities),
                                 mode=sim.state.mode.value)
