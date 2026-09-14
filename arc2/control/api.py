"""The ARC-2 robot control interface.

THIS IS THE HARDWARE SEAM. An AI agent talks to ARC-2 only through this
abstract class. It never sees the simulator, the ground-truth world, object
identities it has not perceived, or any physics function. Swapping
`SimulatedRobotAPI` for a driver-backed implementation is therefore the whole
of the sim-to-real transition at this layer.

The contract that makes the rest of the system possible:

    Every call returns an ActionResult whose `status` was EARNED BY A MEASURED
    OUTCOME. `move(2.0)` that covers 0.3 m before a wall returns
    status=BLOCKED, achieved=0.3, reason="collision". It does NOT return
    SUCCESS merely because nothing raised.

Failure detection in the agent is built entirely on that guarantee.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from arc2.sensors.base import Observation
from arc2.types import ActionStatus, MobilityMode


@dataclass
class ActionResult:
    action: str
    status: ActionStatus
    commanded: float = 0.0
    achieved: float = 0.0
    reason: str = ""
    contact_id: str | None = None
    detail: dict = field(default_factory=dict)
    duration_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status is ActionStatus.SUCCESS

    @property
    def progressed(self) -> bool:
        """Did the world actually change in the commanded direction?"""
        return self.status in (ActionStatus.SUCCESS, ActionStatus.PARTIAL)

    def as_dict(self) -> dict:
        return {"action": self.action, "status": self.status.value,
                "commanded": round(self.commanded, 4),
                "achieved": round(self.achieved, 4),
                "reason": self.reason, "contact_id": self.contact_id,
                "duration_s": round(self.duration_s, 3),
                "detail": self.detail}


class RobotAPI(ABC):
    """The complete Milestone-1 command surface.

    Deliberately small. Anything an agent wants that is not here must be
    composed from these, which is the check that keeps the interface honest.
    """

    # -- sensing -----------------------------------------------------------
    @abstractmethod
    def observe(self) -> Observation:
        """Take a fresh reading from every sensor. Does not move anything."""

    @abstractmethod
    def get_robot_state(self) -> dict:
        """Proprioceptive self-report: mode, carried items, odometry totals.

        Contains the robot's ESTIMATE of its pose, never ground truth.
        """

    # -- locomotion --------------------------------------------------------
    @abstractmethod
    def move(self, distance_m: float) -> ActionResult:
        """Drive forward along the current heading. Stops at the first
        obstruction and reports how far it got."""

    @abstractmethod
    def turn(self, delta_rad: float) -> ActionResult:
        """Rotate in place."""

    @abstractmethod
    def stop(self) -> ActionResult:
        """Command a halt. Always valid, including when already stopped."""

    @abstractmethod
    def change_mobility_mode(self, mode: MobilityMode) -> ActionResult:
        """Switch between wheel and articulated-limb contact. Costs time."""

    # -- sensor aiming -----------------------------------------------------
    @abstractmethod
    def look(self, pan_rad: float, tilt_rad: float = 0.0) -> ActionResult:
        """Aim the mast head. Clamped to the head's limits; clamping is
        reported as PARTIAL, not silently accepted."""

    # -- interaction -------------------------------------------------------
    @abstractmethod
    def push(self, distance_m: float) -> ActionResult:
        """Drive forward, displacing a movable object rather than stopping at
        it. Returns BLOCKED if the object will not shift."""

    @abstractmethod
    def interact(self, verb: str, target_id: str) -> ActionResult:
        """Manipulation verbs: 'pick_up', 'place', 'inspect'."""

    # -- introspection -----------------------------------------------------
    @abstractmethod
    def capabilities(self) -> dict:
        """What this body can do. An agent may consult it, but must still
        verify outcomes -- a capability claim is not a result."""
