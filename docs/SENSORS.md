# ARC-2 Sensors

`arc2/sensors/`. Five sensors, each an abstract interface with a simulated
implementation. The dataclasses in `base.py` are the hardware seam: a real
driver must populate the same fields with the same conventions.

## Mounting

All exteroceptive sensors ray from the **sensor head**, on the mast:

```
body frame: +x forward, +y left, origin at the chassis centroid

   chassis spans x ∈ [-0.45, +0.45]        MAST_MOUNT = (0.30, 0.0)
   front third   x ∈ [+0.15, +0.45]        MAST_HEIGHT = 0.62 m
                          ▲
   ┌──────────────────────╫──────┐
   │  rear          front ╫ mast │   →  +x
   └──────────────────────╨──────┘
                          ↑
                  0.30 m forward of centre,
                  on the longitudinal centreline
```

This has a real consequence, not a cosmetic one: the head reaches 0.30 m
around a corner before the chassis does. It is also a real hazard — during
development, perception integrated rays from the chassis centre while the
sensors emitted them from the mast, a systematic 0.30 m offset that wrote free
space into walls and manufactured frontiers inside them.

`test_embodiment.py` asserts the mount lies in the front third, is on the
centreline, and is **not** at the chassis centre.

## 1. 360° LiDAR — `Lidar360`

```python
LidarScan(bearings, ranges, max_range, origin_height)
```

72 beams at 5°, 5.0 m range, σ = 0.02 m Gaussian range noise.

**The primary source of partial observability.** Occlusion is exact — the
nearest hit wins, so anything behind it is invisible. A beam that returns
`max_range` means *"I could not see that far"*, **not** *"it is clear out to
5 m and empty beyond"*. The perception layer is required to preserve that
distinction, and `test_sensors_and_perception.py` asserts cells beyond the
horizon stay `UNKNOWN` after a scan.

## 2. Depth camera — `DepthCamera`

```python
DepthFrame(bearings, ranges, fov, max_range)   # .min_ahead
```

32 columns over 70°, 5.0 m, σ = 0.015 m. Follows the mast pan. Denser and
narrower than the LiDAR.

## 3. RGB camera — `RgbCamera`

```python
RgbFrame(detections, fov, max_range)
Detection(object_id, label, bearing, range_m, confidence)
```

**Returns detections, not pixels.** This is a deliberate abstraction: a real
RGB camera plus an onboard detector produces exactly this, and photorealistic
rendering would consume the milestone while proving nothing about whether the
architecture supports the perceive-plan-act cycle.

70° FOV, 6.5 m. Two limitations are modelled because they change what the
agent can legitimately conclude:

- **Occlusion** — an object behind a wall is not detected at all.
- **Range-dependent classification** — within 3.2 m the label is specific and
  confidence is 0.55–0.97; beyond it the label degrades to `unknown_object`
  with confidence 0.20–0.60.

That second one is what puts `UNCERTAIN` entries into the world model instead
of facts, and is why the task planner has an `INSPECT` strategy: close in and
confirm before committing.

## 4. IMU — `Imu`

```python
ImuReading(heading, pitch, roll, angular_velocity,
           linear_acceleration, ground_slope)
```

σ = 0.008 rad heading. `ground_slope` probes the elevation 0.35 m ahead, so a
staircase is **measurable before a motion fails** — the agent can see the
slope coming rather than only learning from a blocked move.

## 5. Proprioception — `Proprioception`

```python
JointStateReading(positions, velocities, mode)
```

14 DOF: 4 limbs × (hip, knee, wheel) + mast pan/tilt. Mode-dependent — wheel
mode spins wheels and locks knees, leg mode cycles hips and knees and stops
the wheels. A kinematic stand-in, **not** a gait controller; its job is to
give a downstream consumer a real structured signal.

## The bundled Observation

```python
Observation(tick, sim_time_s, pose_estimate, pose_confidence,
            lidar, depth, rgb, imu, joints, mobility_mode, carrying)
```

`pose_estimate` is the robot's **belief** about where it is. Odometry drift
accumulates at 0.004 m per metre travelled, and `pose_confidence` degrades
with it. The agent is never handed a true pose; tests assert the estimate
diverges from ground truth after movement and that confidence decays.

## Adding a real sensor later

Implement `Sensor.read()` and return the same dataclass. Conventions a driver
must honour:

- ranges in **metres**, bearings in **radians** in the **sensor frame**;
- `max_range` means **no return**, not "clear";
- a detection the pipeline is not confident about must carry a low
  `confidence`, not be dropped and not be upgraded;
- the pose estimate must come from onboard state estimation — never from a
  motion-capture ground truth, which would silently remove the hardest part of
  the problem.
