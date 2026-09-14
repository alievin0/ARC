# ARC-2 Benchmark

## Task 1 — `retrieve_and_return_v1`

> *"Locate an object labelled 'canister', pick it up, and return it to the
> area where you started."*

### What the agent is given

- the **label** to look for (`"canister"`)
- the return tolerance (1.0 m)
- that "home" is wherever it started

### What the agent is not given

- the target's coordinates
- the map
- which of the three routes works
- which obstacle is movable
- that the staircase requires leg mode

Recorded in the episode log as `given_target_coordinates: false` and
`given_map: false`, so the claim is auditable rather than asserted.

### Success

Judged against **ground truth** in `tasks/retrieve_and_return.py`:

```
delivered ⟺ the payload is within 1.0 m of the start position
```

An agent that believes it delivered the payload but did not, fails. The three
outcomes are distinguished:

| Reason | Meaning |
|---|---|
| `payload_returned_to_start_area` | Success |
| `payload_acquired_but_not_returned` | Found it, did not get it home |
| `payload_not_acquired` | Never got it |

Distinguishing the last two matters: they are very different failures, and
collapsing them would hide which half of the task is the problem.

## Metrics

`arc2/benchmark/metrics.py`. Every number is read from ground truth or counted
from the log. None is estimated.

| Metric | Definition |
|---|---|
| `success` | Ground-truth task completion |
| `failure_reason` | Empty on success |
| `sim_time_s` | Simulated elapsed time |
| `wall_time_s` | Host time. **Not** part of the episode; the only field allowed to vary between identical runs |
| `ticks` | Simulator steps |
| `distance_travelled_m` | Ground-truth path length |
| `energy_used` | Distance × per-mode cost. Leg mode costs 3.4× wheel |
| `actions` | API calls that changed or attempted to change state |
| `failed_actions` | Actions whose status was not SUCCESS or PARTIAL |
| `unnecessary_actions` | Repeats of known-bad actions + pure no-ops (see below) |
| `replans` | Route recomputations after a plan already existed |
| `strategy_changes` | Times the task planner switched strategy |
| `explored_fraction` | \|reachable ∩ known\| / \|reachable\| |
| `objects_discovered` | Distinct object beliefs formed |
| `mode_changes` | Successful wheel ⇄ leg transitions |
| `log_events` | Event count |
| `log_digest` | SHA-256 of the whole event stream — the determinism witness |

### No composite score

There is deliberately no "intelligence score". A weighted blend would hide the
trade-off worth seeing: seed 3 succeeds by wandering 254 m with 371 failed
actions; seed 20260914 succeeds in 131 m with 75. Those are different
behaviours and should not average to the same number.

### `unnecessary_actions`, precisely

An action is unnecessary iff it **repeated** an action already recorded as
failing from the same `(action, coarse cell, heading sector)`, **or** it
succeeded while achieving effectively nothing and revealing nothing.

A **first-time failure is not unnecessary** — discovering a blockage is
information. Its first implementation lacked that clause and reported
`unnecessary == failed` exactly, which is a metric that measures nothing new.

### `explored_fraction`, precisely

`reachable` is a ground-truth flood fill from the start over the true world at
the belief's resolution, using the robot's real clearance — i.e. *what could
have been known*. The fraction is a set intersection with the non-`UNKNOWN`
cells of the belief.

## Results

9 seeds, default budget of 1500 actions, sensor noise on.

| seed | success | actions | failed | unnecessary | replans | strategy changes | distance | explored | sim time | mode changes |
|---:|:--|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | ✅ | 1041 | 302 | 234 | 232 | 202 | 210.8 m | 0.95 | 1535 s | 1 |
| 2 | ✅ | 709 | 138 | 86 | 122 | 101 | 197.9 m | 0.95 | 1066 s | 1 |
| 3 | ✅ | 1294 | 371 | 300 | 288 | 252 | 254.2 m | 0.99 | 1900 s | 1 |
| 7 | ✅ | 704 | 183 | 120 | 147 | 123 | 161.7 m | 0.95 | 1042 s | 1 |
| 11 | ✅ | 607 | 95 | 47 | 103 | 74 | 185.9 m | 0.93 | 919 s | 1 |
| 42 | ✅ | 726 | 106 | 48 | 122 | 88 | 224.7 m | 0.99 | 1190 s | 1 |
| 101 | ✅ | 1076 | 246 | 177 | 212 | 173 | 269.8 m | 1.00 | 1621 s | 1 |
| 777 | ✅ | 916 | 224 | 153 | 186 | 156 | 206.1 m | 0.95 | 1373 s | 1 |
| 20260914 | ✅ | 458 | 75 | 42 | 80 | 59 | 131.5 m | 0.90 | 653 s | 1 |

**9/9.** Median: 726 actions, 206 m, 147 replans, 95 % explored.

### On the action budget

1500 is **measured, not chosen**. The first value used was an arbitrary 900,
which cut off three of these seeds *after they had already acquired the
payload* — they complete in 1041, 1076 and 1294. 1500 sits above the observed
maximum with margin. It is a budget, not a target.

### What the numbers do and do not show

**Do:** the architecture supports the full cycle. Every seed requires at least
one route falsified by the world and one physical limit overcome by
reconfiguring the body, and every seed recovers.

**Do not:** that the agent is good. It travels 130–270 m for a task whose
optimal path is roughly 30 m, because nearest-frontier exploration maps most
of the arena before the target enters the camera's field of view. That is the
baseline the next milestone should beat.

## Episode log

One JSON object per line, common envelope
`{schema_version, seq, tick, sim_time_s, type, ...}`. A truncated file is
still readable up to the truncation.

| Event | Payload |
|---|---|
| `episode_start` | seed, task brief, arena, noise setting |
| `capabilities` | embodiment + sensor descriptors |
| `observation` | full sensor bundle (or a digest under `--quiet-log`) |
| `perception` | new cells, new/updated objects, blocked marks |
| `decision` | phase, strategy, goal, rationale |
| `plan` | goal, waypoints, cell count |
| `replan` | cause, rationale, strategy, whether a route was found |
| `action` | verb, params, pose estimate before |
| `action_result` | full `ActionResult` |
| `world_update` | belief change from an action failure |
| `failure` | action, status, reason, contact, detection mode |
| `task_progress` | acquisition, delivery, mode change, obstruction cleared |
| `note` | escape manoeuvres, terminations |
| `episode_end` | outcome, agent report, ground-truth snapshot |

The vocabulary is **closed**: `EpisodeLog.emit` raises on an unknown type, so
a consumer can assert it has handled all of them.

### Reading a log

```python
import json, collections
ev = [json.loads(l) for l in open("logs/episode_seed20260914.jsonl")]

print(collections.Counter(e["reason"] for e in ev if e["type"] == "failure"))
print([e["event"] for e in ev if e["type"] == "task_progress"])
print(ev[-1]["outcome"])
```

Reference episode (seed 20260914): 2,697 events; **76 `failure` events**
(68 reported / 8 measured-stall) but **75 `failed_actions`**; 80 replans
across 4 distinct causes (`failure`, `goal_changed`, `inferred`, `new_goal`);
4 distinct strategies used.

The 76 / 75 gap is not a rounding error. The two numbers count different
things, and the exact decomposition for this episode is:

```
  75 failed_actions  = 75 BLOCKED move results (nothing else ever failed)
  76 failure events  = 68 of those BLOCKED moves
                     +  8 PARTIAL moves that crawled < 0.05 m
                       (detected as stalls, not by their status)
   7 BLOCKED moves raised no failure event: they are the escape manoeuvre's
     own moves, which are not assessed -- a failed escape simply retries in
     the opposite direction rather than triggering another adaptation.
```

`failed_actions` is a property of *outcomes*; `failure` events are a property
of the agent's *interpretation* of them. Reporting one number for both would
hide that the agent detects some failures the status field does not report,
and deliberately ignores some it does.
