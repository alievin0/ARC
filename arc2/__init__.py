"""ARC-2 Digital Twin -- Milestone 1 testbed.

Layer boundaries (enforced by import direction, documented in docs/ARCHITECTURE.md):

    simulation  <- ground truth. Nothing above it may import it except sensors
                   and control.sim_backend.
    robot       <- embodiment: geometry, mounts, mobility-mode capabilities.
    sensors     <- read simulation, emit structured Observations.
    control     <- RobotAPI. The ONLY surface the agent is allowed to touch.
    world       <- the robot's belief. Tri-state. Never ground truth.
    perception  <- Observation -> world belief updates.
    memory      <- what was tried and what happened.
    planning    <- task strategy + action/path planning over the belief.
    agent       <- the deliberative loop.
    tasks       <- task definitions and success criteria.
    benchmark   <- metrics.
    telemetry   <- machine-readable episode log.
"""

__version__ = "0.1.0"
SCHEMA_VERSION = 1
