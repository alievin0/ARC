"""Placeholder for the physical ARC-2 backend. NOT IMPLEMENTED.

This file exists to make the sim-to-real seam concrete and checkable rather
than aspirational: it enumerates exactly what a hardware implementation owes
the rest of the system, and every method raises so that nobody can mistake
a stub for a working driver.

EXPLICITLY OUT OF SCOPE FOR MILESTONE 1: real motor control, real LiDAR
drivers, ROS2 integration. Do not implement them here. The value of this file
today is the checklist, not the code.

What a hardware implementation must provide
-------------------------------------------
observe()      Populate the same Observation dataclass. Ranges in metres,
               bearings in the sensor frame, `max_range` meaning "no return".
               Pose estimate from onboard state estimation, never a mocap
               ground truth.
move()         MUST measure achieved distance (wheel odometry fused with IMU)
               and MUST report BLOCKED when motor current or a bumper says the
               chassis stopped early. Returning SUCCESS because the command
               was accepted by the motor controller is the exact failure mode
               this architecture is built to prevent.
push()         Same, plus a means of deciding an object actually displaced
               (force/torque, or re-observation). If it cannot be measured,
               return FAILED, not SUCCESS.
interact()     Whatever manipulator exists. Absent one, return INVALID.
change_mobility_mode()
               Must confirm the transition completed before reporting SUCCESS.
"""
from __future__ import annotations

from arc2.control.api import ActionResult, RobotAPI
from arc2.sensors.base import Observation
from arc2.types import MobilityMode


class HardwareNotAvailable(NotImplementedError):
    pass


def _todo(what: str):
    raise HardwareNotAvailable(
        f"ARC-2 hardware backend not implemented: {what}. "
        "Milestone 1 is simulation only; see docs/HARDWARE_TRANSITION.md.")


class HardwareRobotAPI(RobotAPI):
    """Every method raises. Deliberately."""

    def __init__(self, transport: object | None = None) -> None:
        self.transport = transport

    def observe(self) -> Observation: _todo("observe")
    def get_robot_state(self) -> dict: _todo("get_robot_state")
    def move(self, distance_m: float) -> ActionResult: _todo("move")
    def turn(self, delta_rad: float) -> ActionResult: _todo("turn")
    def stop(self) -> ActionResult: _todo("stop")
    def change_mobility_mode(self, mode: MobilityMode) -> ActionResult:
        _todo("change_mobility_mode")
    def look(self, pan_rad: float, tilt_rad: float = 0.0) -> ActionResult:
        _todo("look")
    def push(self, distance_m: float) -> ActionResult: _todo("push")
    def interact(self, verb: str, target_id: str) -> ActionResult: _todo("interact")
    def capabilities(self) -> dict: _todo("capabilities")
