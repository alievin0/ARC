# ARC-2 Architecture

## Why the layers are separated this way

The separation is not decoration. Each boundary exists to make one specific
mistake impossible.

| Boundary | The mistake it prevents |
|---|---|
| simulation ↔ control | The agent reading ground truth instead of sensing it |
| sensors ↔ perception | Sensor limits being bypassed by the mapping code |
| world ↔ simulation | The belief being seeded with facts nobody observed |
| planning ↔ world | Plans made against reality instead of against belief |
| control ↔ everything | An agent that cannot be run on hardware later |

## Import direction

Strictly downward. Nothing in `perception/`, `memory/`, `planning/`, `agent/`
imports `arc2.simulation`. This is enforced by test
(`test_the_agent_never_imports_the_simulation_layer`) rather than by
convention, because conventions erode.

```
agent ──> control ──> sensors ──> simulation
  │           └──────> robot ────────┘
  ├──> perception ──> world
  ├──> memory
  ├──> planning ──> world
  └──> telemetry

benchmark ──> everything (it is the only layer allowed to read ground truth,
              because judging success against belief would be meaningless)
tasks     ──> simulation (success criteria are ground-truth by definition)
```

## The layers

### 1. `simulation/`
Ground truth and the only mutable world state.

- `geometry.py` — AABBs, circle/box collision, exact slab-method raycasting.
  One implementation of "can the robot be here?" and "what does this ray hit?"
- `world_spec.py` — the arena, written down exactly once. The agent never
  imports it.
- `physics.py` — sub-stepped motion resolution (0.04 m slices, so a fast move
  cannot tunnel through a 0.5 m wall), step-height gating, push resolution.
- `simulator.py` — owns the clock, the RNG, and the robot's true state.

### 2. `robot/`
Embodiment: chassis envelope, four limbs, mast/head mounting, per-mode
capabilities. All dimensions are **provisional placeholders** except the mast
mounting, which is a stated requirement and is asserted by test.

### 3. `sensors/`
Abstract `Sensor` interface plus five implementations, and the dataclasses
that are the hardware seam for perception. `SensorSuite` bundles a reading
into one `Observation` and maintains odometry drift — drift belongs here
because it is a property of sensing, not of the world.

### 4. `control/`
`RobotAPI` (abstract) + `SimulatedRobotAPI` + `HardwareRobotAPI` (raises).
The whole of the sim-to-real transition at this layer is swapping the backend.

### 5. `world/`
`OccupancyBelief` (tri-state grid) and `WorldModel` (object beliefs, failure
records, pose estimate, home). Beliefs, never facts.

### 6. `perception/`
The only writer of sensed knowledge. Walks each LiDAR ray marking free space
up to the return and blocked at it, and writes **nothing** past a beam that
saw nothing.

### 7. `memory/`
Episodic record keyed by `(action, coarse cell, heading sector)`. This is what
makes replanning different from retrying: without it, an agent that re-derives
the same plan from the same belief drives into the same wall forever.

### 8. `planning/`
- `path.py` — A\* over the belief, with `UNKNOWN` optimistically traversable
  at a cost penalty. Chassis clearance is a **hard** constraint, not a
  penalty; as a penalty the planner produced paths the robot could not drive.
- `action_planner.py` — path → bounded `turn`/`move` primitives, plus
  `Plan.invalidated_by()`, the proactive half of failure detection.
- `task_planner.py` — the `Phase` × `Strategy` machine. Phase is *where we are
  in the task*; strategy is *how we are currently attempting it*. A failure
  changes the strategy and never undoes progress.

### 9. `agent/`
The deliberative loop. Scripted on purpose.

### 10. `telemetry/`, `benchmark/`, `tasks/`
Log, metrics, and goal definition. Named `telemetry` so it never shadows the
standard library's `logging`.

## The control cycle

```
observe()                     ← RobotAPI
   │
integrate()                   ← perception writes ONLY what was sensed
   │
task.decide()                 ← phase + strategy from belief and memory
   │
plan_route()                  ← A* over belief; UNKNOWN is a hypothesis
   │
execute one primitive         ← RobotAPI; at most one turn or one bounded move
   │
observe() again               ← the world gets to answer
   │
   ├── result reports BLOCKED/REFUSED/FAILED ──┐
   ├── result claims progress but pose barely  │
   │   moved (measured stall)                  ├──> failure
   └── new blockages intersect the remaining   │
       route (inferred, before contact)     ───┘
                                                 │
                        memory.record + world_model.force_blocked
                                                 │
                        task.on_failure() → a DIFFERENT strategy
                                                 │
                                            replan / unwedge
```

## Three independent failure detectors

They are genuinely different and all three fire in a normal episode:

1. **Reported** — the `ActionResult` says so. Depends entirely on the API's
   honesty contract.
2. **Measured stall** — the result claims progress but the pose moved less
   than 0.05 m. Catches a backend that lies.
3. **Inferred** — cells newly discovered to be blocked intersect the remaining
   route, so the plan is dead before the robot drives into it.

The reference episode logs 68 reported, 8 measured-stall, and 3 inferred.

## Failure → adaptation mapping

The mapping from *physical reason* to *kind of adaptation* is the point. A
step is not a wall, and a crate is not a dead end.

| Reason | Strategy | Why |
|---|---|---|
| `step_too_high` | `CHANGE_MOBILITY` | The route is fine; the body is wrong |
| collision with a **seen** movable | `CLEAR_OBSTRUCTION` | Change the world |
| any other collision | `ALTERNATE_ROUTE` | The route is wrong |
| 3 consecutive failures here | `EXPLORE_FRONTIER` + abandon region | The area is written off |

`CLEAR_OBSTRUCTION` requires the contact id to correspond to an object the
agent has actually **perceived and classified**. Trusting a raw contact id
would leak ground truth into the plan through the collision report — a test
asserts an unseen contact id never selects it.

## Defects found and fixed during the build

Kept here because each was a real bug with a measured signature, and each is
now guarded by a test.

| Defect | Signature | Fix |
|---|---|---|
| Perception integrated from the chassis centre while sensors ray from the mast | Free space written inside walls; phantom frontiers | Integrate from `sensor_head_position()` |
| Goal re-derived every iteration | 445 replans for 5.6 m travelled | Keep a plan until it completes or is falsified |
| Recovery strategy discarded in the SEARCH phase | 767 identical failures against one crate | `_effective_strategy()` applied in every phase |
| Escalation unreachable behind the movable-contact branch | 728 identical pushes against a wedged crate | Check escalation first, unconditionally |
| Clearance was a soft penalty (0.25 m) vs a 0.40 m chassis | 345 blocked moves against one pillar | Hard constraint, sized to keep the 1.1 m passage open |
| `plan_route` fell back to the raw unreachable goal | 879 moves into one wall | Return `None`; a fake plan is worse than no plan |
| Frontier goals the chassis cannot occupy | Goal inside a wall | Frontier candidates must pass the clearance test |
| Forward-only motion cannot un-wedge | 388 blocked moves in a doorway corner | A\* start-relaxation + an explicit escape manoeuvre |
| `explored_fraction` divided two independently counted quantities | Reported 1.00 with 1257 cells unknown | Set intersection against ground-truth reachable cells |

One change was tried and **reverted as a measured regression**: writing off
the pursued goal whenever the robot wedged took the suite from 4/7 to 3/7
seeds. Being wedged says the approach was wrong, not that the destination is
unreachable. The comment recording that is left in `agent/loop.py`.
