# ARC-2 Digital Twin — Milestone 1

A minimal simulated testbed in which an AI agent perceives an unfamiliar
environment through simulated sensors, reasons about a task, acts through a
clean robot API, observes the consequences, detects that its plan has failed,
updates its model of the world, and replans.

**This is a testbed, not a robot.** Nothing here is claimed to be novel. The
mechanical design is not final, the dimensions are provisional placeholders,
and the agent is a deliberately simple scripted planner. The question this
milestone answers is narrow and structural:

> Does the architecture actually support
> `OBSERVE → UNDERSTAND → PLAN → ACT → OBSERVE RESULT → DETECT FAILURE →
> UPDATE MODEL → REPLAN`, with real failures rather than scripted ones?

Measured answer: yes — 9 of 9 seeds complete the benchmark, each requiring at
least one route falsified by the world and one physical limit overcome by
changing the robot's own configuration.

---

## Quick start

No dependencies. Python 3.10+ (developed on 3.14), standard library only.

```bash
cd arc2
python3 run_tests.py                 # 148 tests
python3 run_benchmark.py             # one episode, default seed
```

Run the full suite of seeds:

```bash
python3 run_benchmark.py --seeds 1 2 3 7 11 42 101 777 20260914
```

Other flags: `--seed N`, `--max-actions N`, `--no-noise`, `--quiet-log`.

Every run writes `logs/episode_seed<N>.jsonl` (one JSON event per line) and
`logs/benchmark_summary.json`.

---

## Architecture

Ten layers, separated so that the simulation can be replaced by hardware
without touching anything above the control layer.

```
                    ┌───────────────────────────────┐
                    │  agent/    deliberative loop  │  ← replaceable: LLM, RL,
                    └───────────────┬───────────────┘     human teleop
        ┌───────────────┬───────────┼───────────┬────────────────┐
        ▼               ▼           ▼           ▼                ▼
   perception/      memory/    planning/     world/          tasks/
   obs → belief     what was   task strat.   belief store    goal + success
                    tried      + A* path     KNOWN/UNCERTAIN/
                                             UNKNOWN
        └───────────────┴───────────┬───────────┴────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │  control/     RobotAPI        │  ◄── THE HARDWARE SEAM
                    │  observe move turn stop push  │
                    │  look interact change_mode    │
                    └───────┬───────────────┬───────┘
                sim_backend │               │ hardware_backend (stub)
                            ▼               ▼
              ┌─────────────────────┐   ┌──────────────────┐
              │ sensors/  robot/    │   │  real drivers    │
              │ simulation/         │   │  (later)         │
              └─────────────────────┘   └──────────────────┘

   benchmark/  metrics, runner        telemetry/  JSONL episode log
```

| Directory | Responsibility |
|---|---|
| `arc2/simulation/` | Ground truth: geometry, physics, the arena, the clock, the RNG |
| `arc2/robot/` | Embodiment: chassis, four limbs, mast/head mounts, mode capabilities |
| `arc2/sensors/` | Five sensor interfaces + their simulated implementations |
| `arc2/control/` | `RobotAPI` — the only surface the agent touches |
| `arc2/world/` | The robot's **belief**: tri-state occupancy + object beliefs |
| `arc2/perception/` | Observation → belief updates. The only writer of sensed knowledge |
| `arc2/memory/` | Episodic record of what was tried, where, and how it went |
| `arc2/planning/` | Task strategy machine + A\* action planner over the belief |
| `arc2/agent/` | The deliberative loop |
| `arc2/tasks/` | Task definition + ground-truth success criteria |
| `arc2/benchmark/` | Metrics and the episode runner |
| `arc2/telemetry/` | Machine-readable episode log |

`telemetry/` rather than `logging/` so it never shadows the standard library.

Detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Physical-vehicle counterpart: the ARC-2B engineering feasibility study in
[docs/feasibility/](docs/feasibility/README.md) and the CAD-ready master architecture in
[docs/architecture/](docs/architecture/README.md), and the amphibious transformation study in
[docs/amphibious/](docs/amphibious/README.md) (corner-module mechanism,
failure analysis, interlocks, drivetrain, ski/track, marine, structures,
battery, manufacturing plan, patents, and a "DO NOT BUILD YET" list; every
number traces to `docs/feasibility/calc/params.py`).

---

## The one rule everything rests on

> **A status must be earned by a measured outcome, never by the absence of an
> exception.**

`move(2.0)` that covers 0.3 m before a wall returns
`status=BLOCKED, achieved=0.3, reason="collision"`. It does **not** return
success because nothing raised. Every failure the agent detects, every
blockage it writes into its map, and every replan it triggers is downstream of
that single property.

The same rule is why `HardwareRobotAPI` raises on every method instead of
returning plausible stubs.

---

## The robot API

The agent calls these and nothing else. It never touches physics, never reads
ground truth, never sees an object it has not perceived.

```python
observe()                        -> Observation      # all five sensors
get_robot_state()                -> dict             # proprioception only
move(distance_m)                 -> ActionResult
turn(delta_rad)                  -> ActionResult
stop()                           -> ActionResult
change_mobility_mode(mode)       -> ActionResult     # WHEEL | LEG
look(pan_rad, tilt_rad)          -> ActionResult
push(distance_m)                 -> ActionResult     # displaces movable objects
interact(verb, target_id)        -> ActionResult     # pick_up | place | inspect
capabilities()                   -> dict
```

`ActionResult.status` ∈ `SUCCESS · PARTIAL · BLOCKED · REFUSED · INVALID ·
FAILED`, always with `commanded`, `achieved`, `reason`, and `contact_id`.

`get_robot_state()` deliberately omits x/y: position is something the robot
*estimates*, not something it *knows*. A test asserts the leak cannot
reappear.

Full reference: [docs/ROBOT_API.md](docs/ROBOT_API.md).

---

## Sensors

| Sensor | Output | Modelled limitation |
|---|---|---|
| 360° LiDAR | 72 beams, 5.0 m range, σ=0.02 m | Exact occlusion; beyond range is **unobserved**, not empty |
| Depth camera | 32 columns, 70° FOV, 5.0 m | Forward only |
| RGB camera | **Detections, not pixels** | Occlusion; past 3.2 m the label degrades to `unknown_object` at low confidence |
| IMU | Attitude + ground slope | Noise; slope reveals the staircase before a motion fails |
| Proprioception | 14 joints, mode-dependent | — |

All exteroceptive sensors ray from the **mast head**, which sits on the front
third of the chassis on the longitudinal centreline (`MAST_MOUNT = (0.30, 0)`
in body frame, chassis spanning ±0.45 m) — not from the chassis centre. This
is asserted by test, and integrating perception from the wrong origin was a
real bug during development: it wrote free space into walls.

Pixels are deliberately not rendered. Detections are what a real camera plus
an onboard detector would hand a planner, and photorealism would prove nothing
at this milestone. Details: [docs/SENSORS.md](docs/SENSORS.md).

---

## World model

Three epistemic states, never merged:

- **KNOWN** — sensed, and consistent
- **UNCERTAIN** — conflicting returns, or a low-confidence classification
- **UNKNOWN** — never sensed

Perception writes a cell only if a ray actually reached it. A beam that
returns nothing at maximum range writes **nothing** past its horizon. At the
end of the reference episode 1,257 cells are still `UNKNOWN` — the agent does
not claim to have mapped the world, and a test asserts it never does.

A *failed action* is stronger evidence than any number of range returns, so a
collision overrides the hit counts and marks a blockage across the chassis
width. Details: [docs/WORLD_MODEL.md](docs/WORLD_MODEL.md).

---

## The environment

24 × 16 m, deliberately small, with three ways out of the starting room. None
of this is given to the agent.

```
 y=16 ┌────────────────────────────────────────────────────────┐
      │   ROOM C          ● target (7.5, 13.2)                 │
      │        ┌────┐                    ▓ pillar              │
  y=9 │        │dead│      ┌────┐          ┌──────┐            │
      │        │ end│      │1.1m│          │stairs│            │
      │        │    │      │pass│          │▲ ▲ ▼ │            │
  y=6 ├────────┘    └──────┘ ▪  └──────────┘      └────────────┤
      │      D1 ↑           D2 ↑ crate          D3 ↑           │
      │   ROOM A        ▓            ▓                  ▓      │
  y=0 └────────── ★ start/return (2.0, 2.2) ───────────────────┘
     x=0                                                    x=24
```

Each route fails differently, and each demands a **different kind** of
adaptation:

| Route | What happens | Required adaptation |
|---|---|---|
| **D1** dead-end corridor | Looks like a route; sealed 4.6 m in | Re-route |
| **D2** narrow passage | 1.1 m wide, blocked by a pushable crate | Change the world (`push`) |
| **D3** staircase | 0.18 m steps; wheel mode lifts 0.06 m | Change the body (`change_mobility_mode`) |

None of these is scripted. The dead end is discovered because the planner
treats `UNKNOWN` space as optimistically traversable — which a real explorer
must, or it can never leave the room — so the first plan through an unexplored
corridor is a genuine hypothesis the world is free to falsify.

**Uncertainty sources:** limited LiDAR range, exact occlusion, range and IMU
noise, odometry drift with degrading pose confidence, range-dependent
classification, and a movable object whose position changes after interaction.

---

## The benchmark task

> *"Locate an object labelled 'canister', pick it up, and return it to the
> area where you started."*

The agent is **not** given the target's coordinates, the map, which route
works, which obstacle is movable, or that the stairs need leg mode. Success is
judged against **ground truth**, not against the agent's belief: an agent that
thinks it delivered the payload but did not, fails.

### Results — 9 seeds, all successful

| seed | actions | failed | unnecessary | replans | strategy changes | distance | explored | sim time | mode changes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1041 | 302 | 234 | 232 | 202 | 210.8 m | 0.95 | 1535 s | 1 |
| 2 | 709 | 138 | 86 | 122 | 101 | 197.9 m | 0.95 | 1066 s | 1 |
| 3 | 1294 | 371 | 300 | 288 | 252 | 254.2 m | 0.99 | 1900 s | 1 |
| 7 | 704 | 183 | 120 | 147 | 123 | 161.7 m | 0.95 | 1042 s | 1 |
| 11 | 607 | 95 | 47 | 103 | 74 | 185.9 m | 0.93 | 919 s | 1 |
| 42 | 726 | 106 | 48 | 122 | 88 | 224.7 m | 0.99 | 1190 s | 1 |
| 101 | 1076 | 246 | 177 | 212 | 173 | 269.8 m | 1.00 | 1621 s | 1 |
| 777 | 916 | 224 | 153 | 186 | 156 | 206.1 m | 0.95 | 1373 s | 1 |
| 20260914 | 458 | 75 | 42 | 80 | 59 | 131.5 m | 0.90 | 653 s | 1 |

**9/9 success.** Median 726 actions, 206 m, 147 replans, 95 % explored.

No composite "intelligence score" is produced, by design — a blend would hide
exactly the trade-off worth seeing, namely that seed 3 succeeds by wandering
254 m and seed 20260914 succeeds in 131 m.

Metric definitions, including the precise definition of an *unnecessary
action*: [docs/BENCHMARK.md](docs/BENCHMARK.md).

---

## Where the AI agent connects

`arc2/agent/loop.py` holds a `RobotAPI` and a `WorldModel` and nothing else.
To substitute a different policy — an LLM, a learned controller, a human —
replace that class. The contract is:

```python
class YourAgent:
    def __init__(self, api: RobotAPI, log: EpisodeLog, config): ...
    def run(self) -> dict: ...
```

A test asserts `arc2/agent/loop.py` contains no import of `arc2.simulation`
and no reference to `world_spec` or `truth_snapshot`, so the boundary cannot
quietly erode.

The current agent is scripted **on purpose**: with a learned policy it would
be impossible to tell whether the architecture worked or whether the policy
had memorised the arena.

---

## Connecting to real hardware later

`arc2/control/hardware_backend.py` enumerates exactly what a physical backend
owes the rest of the system, and every method raises so a stub can never be
mistaken for a driver. See [docs/HARDWARE_TRANSITION.md](docs/HARDWARE_TRANSITION.md).

Explicitly **out of scope** for Milestone 1: real motor control, real LiDAR
drivers, ROS 2, final dimensions, outer shell, dashboards, RL, foundation
models.

---

## Determinism

One `random.Random`, seeded at construction, owned by the simulator. Nothing
else calls `random`. `reset()` restores the world, the robot, the clock and
the RNG stream.

Verified by comparing the **SHA-256 digest of the entire event stream** — a
spot check would pass on a run that diverged in an unchecked field. Tests
assert that the same seed reproduces the digest, that a *different* seed does
not (otherwise "deterministic" is indistinguishable from "ignores the seed"),
and that `wall_time_s` is the only field allowed to vary.

---

## Testing

```bash
python3 run_tests.py        # 148 tests, ~9 s
```

| File | Tests | Covers |
|---|---:|---|
| `test_geometry.py` | 11 | Collision, raycasting, occlusion |
| `test_embodiment.py` | 9 | Mast mounting, mode capabilities, joints |
| `test_physics_and_api.py` | 24 | Movement honesty, stair gate, push, interact |
| `test_sensors_and_perception.py` | 20 | Sensor limits, perception honesty |
| `test_world_model_and_memory.py` | 19 | Tri-state belief, failure memory |
| `test_planning.py` | 29 | A\*, clearance, frontiers, strategy machine |
| `test_determinism.py` | 7 | Reset, replay, seed reproduction |
| `test_integration.py` | 29 | The nine end-to-end checks |

**Guards are proven in both directions.** A guard that refuses everything is
an outage wearing security's clothes, so every gate is tested with a valid
input that must **pass** as well as inputs that must fail:

- wheel mode is refused at the stairs **and** leg mode succeeds;
- a 0.5 m gap is refused **and** the 1.1 m passage stays open;
- `push` displaces the crate **and** plain `move` does not;
- an under-powered push leaves the object exactly where it was.

**The suite is proven able to fail.** Five invariants were deliberately broken
and the suite caught all five:

| Mutation | Result |
|---|---|
| Mast moved to the chassis centre | caught (1 failure) |
| `move` always reports SUCCESS | caught (4 failures) |
| Perception fills in unobserved space | caught (2 failures) |
| RNG ignores the seed | caught (5 failures) |
| Planner ignores chassis clearance | caught (5 failures) |

---

## Known limitations

Stated plainly, because each is a real constraint on what these results mean.

1. **The agent is inefficient.** It travels 130–270 m for a task whose optimal
   path is roughly 30 m, because nearest-frontier exploration maps most of the
   arena before the target enters the camera's field of view. The architecture
   is the deliverable here; the policy is not.
2. **Physics is 2.5-D and kinematic.** Circle-vs-AABB collision, elevation as
   a step function, no dynamics, no mass, no friction, no leg contact
   modelling. Traversability is one well-defined question, which is what makes
   the results legible — and also what stops them from telling you anything
   about real locomotion.
3. **Success is not guaranteed in general.** The robot can wedge itself, and
   the escape manoeuvre is a heuristic, not a proof. 9/9 is a measurement on
   nine seeds, not a theorem.
4. **The action budget is measured, not derived.** 1500 sits above the
   observed maximum of 1294 with margin. An earlier arbitrary value of 900 cut
   off three seeds *after* they had already acquired the payload.
5. **RGB returns detections, not images.** No perception research is being
   done here; a real detector's failure modes are not modelled.
6. **One task, one arena.** Generalisation is untested by construction.
7. **Object-permanence is shallow.** Beliefs never decay, so a moved object
   leaves a stale belief until it is re-observed.
8. **The mast's forward mounting is modelled only in 2-D** — it shifts the ray
   origin, but there is no modelling of what the height buys.

---

## What the next milestone should investigate

In rough priority order:

1. **Replace the scripted agent** with a policy that reasons over the world
   model — the interface is already the right shape, and the metrics here are
   the baseline to beat.
2. **Information-directed exploration.** Nearest-frontier is the single
   largest source of waste; expected-information-gain would be measurable
   against exactly these numbers.
3. **Introduce dynamics.** Mass, friction, and real leg contact — starting
   with whether the crate should resist proportionally to mass.
4. **A second task and a second arena**, to find out how much of this
   generalises and how much is fitted to one map.
5. **Belief decay and object permanence**, so a stale belief is distinguished
   from a current one.
6. **Only then**: sensor realism, hardware drivers, and the mechanical design
   this testbed exists to inform.
