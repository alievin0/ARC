# From simulated ARC-2 to physical ARC-2

```
   agent / perception / memory / planning / world / tasks / benchmark
                              │
                              │   unchanged
                              ▼
                   ┌────────────────────┐
                   │      RobotAPI      │   ← the seam
                   └─────────┬──────────┘
                 ┌───────────┴───────────┐
                 ▼                       ▼
       SimulatedRobotAPI          HardwareRobotAPI
       (works today)              (stub; every method raises)
```

**Nothing above the seam changes.** A test asserts the agent contains no
import of `arc2.simulation` and no reference to `world_spec` or
`truth_snapshot`, so the boundary cannot quietly erode while nobody is
looking.

## Why the stub raises instead of returning plausible values

A stub that returns `SUCCESS` is indistinguishable from a working driver until
something goes wrong in the field. `HardwareRobotAPI` raises
`HardwareNotAvailable` on every method, and a test asserts it — so a stub can
never be mistaken for an implementation.

## What a hardware backend owes the system

### `observe()`
Populate the same `Observation` dataclass:

- ranges in **metres**, bearings in **radians** in the **sensor frame**;
- `max_range` means **no return**, not "clear";
- `pose_estimate` from **onboard state estimation**. Never from motion
  capture — substituting ground truth removes the hardest part of the problem
  while appearing to work.

`pose_confidence` should reflect the estimator's actual covariance.

### `move()` — the one that matters
Must **measure** achieved distance (wheel odometry fused with IMU) and must
report `BLOCKED` when motor current, a bumper, or a stall detector says the
chassis stopped early.

> Returning `SUCCESS` because the motor controller accepted the command is the
> exact failure mode this architecture exists to prevent. The agent's entire
> failure-detection path is built on `achieved` being a measurement.

The agent's second detector — a result claiming progress while the pose barely
moved — exists precisely because a backend might get this wrong. Do not rely
on it.

### `push()`
Same, plus a way to decide an object **actually displaced**: force/torque
sensing, or re-observation. If displacement cannot be measured, return
`FAILED` — not `SUCCESS`.

### `change_mobility_mode()`
Confirm the transition **completed** (joint positions, limit switches) before
reporting `SUCCESS`.

### `interact()`
Whatever manipulator exists. Absent one, return `INVALID` for `pick_up` and
`place`. `inspect` can be served by the camera alone.

### `look()`
Report clamping as `PARTIAL`. An agent that believes it is looking somewhere
it is not will misattribute everything it sees.

## Suggested order

1. **`observe()` only.** Run the perception and world-model layers on real
   sensor data with a human driving. Nothing else changes; the episode log is
   the same format, so simulated and real maps can be compared directly.
2. **Add `turn()` and `stop()`.** Lowest-risk actuation.
3. **Add `move()` with real stall detection.** This is the milestone that
   matters — validate `achieved` against a tape measure before trusting it.
4. **Add `change_mobility_mode()`**, if the hardware has two modes.
5. **`push()` and `interact()` last.** They need force sensing and a
   manipulator.

## Calibration the simulation currently assumes

Every one of these is a placeholder to be replaced with a measurement, not a
specification:

| Quantity | Placeholder | How to obtain |
|---|---|---|
| Collision radius | 0.40 m | Measure the real footprint; a disc may stop being adequate |
| Max step height, wheel | 0.06 m | Measure |
| Max step height, leg | 0.25 m | Measure |
| Max speed | 0.90 / 0.32 m/s | Measure |
| Mode-change time | 4.0 s | Measure |
| Odometry drift | 0.004 m/m | Measure on a known course |
| LiDAR range / noise | 5.0 m / σ 0.02 m | Datasheet, then verify |
| Detection confidence vs range | 3.2 m threshold | Characterise the real detector |
| Manipulator reach | 0.85 m | There is no manipulator yet |

## Not in scope now

Real motor control, real LiDAR drivers, ROS 2, final dimensions, the outer
shell. The value of this document today is the checklist, not the code.
