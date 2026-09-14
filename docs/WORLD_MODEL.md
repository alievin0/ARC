# ARC-2 World Model

`arc2/world/`. The robot's belief. Never ground truth.

## The rule

Everything here was written by the perception layer from an actual sensor
return, or by the agent from an actual action outcome. Nothing is seeded from
`world_spec.py`. If the agent has not seen the target, `find_by_label`
returns `None` — not an approximate location.

## Tri-state occupancy

`OccupancyBelief` — a 0.25 m grid over the arena (96 × 64 = 6144 cells).

| State | Meaning |
|---|---|
| `UNKNOWN` | Never sensed. The default, and the majority for most of an episode |
| `FREE` | Sensed, traversable |
| `BLOCKED` | Sensed, something solid |
| `UNCERTAIN` | Conflicting returns, or low-confidence classification |

### Contested cells do not go to the last writer

Free and blocked hits are counted separately:

- blocked hits `== 0` → `FREE`
- free hits `== 0` → `BLOCKED`
- blocked ≥ 2 × free → `BLOCKED`
- free ≥ 2 × blocked → `FREE`
- otherwise → **`UNCERTAIN`**

A single noisy return therefore cannot flip a well-observed cell, and a
genuinely ambiguous cell is *labelled* ambiguous instead of being guessed.

### A failed action outranks any number of range returns

`force_blocked()` adds 8 block-hits and sets the state directly. A motion that
physically stopped is the strongest evidence available — stronger than a
LiDAR beam, which can be noisy or mis-registered.

A collision marks **three cells across the chassis width**, not one: a chassis
that stopped proves something solid spans its width. Marking a single cell
left the planner free to route around it into the same obstacle.

### Outside the arena is solid by definition

`get()` returns `BLOCKED` for out-of-bounds cells, so the planner cannot route
off the edge of the map.

## Object beliefs

```python
ObjectBelief(object_id, label, position, confidence,
             first_seen_tick, last_seen_tick, observation_count, labels_seen)
```

`knowledge` is derived, not stored:

- `KNOWN` — confidence ≥ 0.60 **and** seen at least twice
- `UNCERTAIN` — label is `unknown_object`, or confidence < 0.45, or seen once

The "seen at least twice" clause matters: one confident-looking glimpse is
still one glimpse. The threshold is not tuned to make the demo succeed — it is
what stops the agent committing to a 0.3-confidence guess, and it is why the
task planner has an `INSPECT` strategy to close in and confirm.

Position is fused with weight 0.65 toward newer, higher-confidence sightings.
A specific label replaces `unknown_object`; the reverse never happens.

## Failure and success records

```python
FailureRecord(kind, position, heading, tick, detail)
```

Kept in the world model (spatial: *there is a blockage there*) and, keyed
differently, in episodic memory (procedural: *that action from that place
does not work*). Both are needed — the first informs the planner, the second
stops the agent repeating itself.

## Episodic memory

`arc2/memory/episodic.py`. Failures are keyed by

```
(action, floor(x / 0.6), floor(y / 0.6), heading_sector_of_16)
```

Coarse enough that "I failed here going that way" generalises a little,
specific enough that an unrelated action elsewhere is not suppressed. Tests
assert a failure does **not** generalise to a different place or to the
opposite heading.

### `unnecessary_actions` — the precise definition

An action is unnecessary iff:

- it **repeated** an action already recorded as failing from the same
  `(action, cell, heading sector)`; **or**
- it succeeded but achieved effectively nothing and revealed nothing.

Crucially, a **first-time failure is not unnecessary** — discovering a
blockage is information. Without that clause the metric is just a synonym for
`failed_actions`, which is exactly what it measured in its first version.

## What "explored" means

`explored_fraction` = |reachable ∩ known| / |reachable|, where `reachable` is
the ground-truth flood fill from the start over the true world at the belief's
resolution, using the robot's actual clearance.

The denominator is *what could have been known*. Measuring against the whole
arena would punish the agent for space it can never legally occupy.

The first version of this metric divided "cells believed free" by "cells
reachable" — two independently counted quantities — so it could exceed 1.0 and
be clamped, reporting **full exploration while 1,257 cells were still
`UNKNOWN`**. It is now a set intersection and cannot do that.

## What the model must never do

- Contain an object never detected.
- Mark a cell no ray reached.
- Report `KNOWN` for a single low-confidence sighting.
- Claim complete knowledge — at the end of the reference episode 1,257 cells
  remain `UNKNOWN`, and a test asserts the count is greater than zero.
