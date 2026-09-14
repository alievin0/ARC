# ARC-2 Robot API

`arc2/control/api.py`. The complete surface an agent may use. Anything not
here must be composed from these — the check that keeps the interface honest.

## The contract

> **Every call returns an `ActionResult` whose `status` was earned by a
> measured outcome.**

`move(2.0)` that covers 0.3 m before a wall returns
`status=BLOCKED, achieved=0.3, reason="collision", contact_id="divider_0"`.
It does not return `SUCCESS` because nothing raised.

```python
@dataclass
class ActionResult:
    action: str              # which verb
    status: ActionStatus
    commanded: float         # what was asked for
    achieved: float          # what actually happened
    reason: str              # "reached" | "collision" | "step_too_high" | ...
    contact_id: str | None   # what stopped us, if anything
    detail: dict
    duration_s: float

    ok          -> status is SUCCESS
    progressed  -> status in (SUCCESS, PARTIAL)
```

### Statuses

| Status | Meaning |
|---|---|
| `SUCCESS` | Commanded effect achieved within tolerance |
| `PARTIAL` | Some progress, stopped early by the world (or a clamped request) |
| `BLOCKED` | The world physically prevented it |
| `REFUSED` | The robot's own capabilities forbid it |
| `INVALID` | Malformed request |
| `FAILED` | Attempted, no effect, reason unknown |

`PARTIAL` and `BLOCKED` are distinguished by `PROGRESS_EPS = 0.02 m`.

## Methods

### `observe() -> Observation`
Fresh reading from all five sensors. Moves nothing. The only way to learn
anything about the world.

### `get_robot_state() -> dict`
Proprioceptive self-report:

```python
{"mode", "carrying", "distance_travelled_m", "energy_used",
 "elapsed_s", "mast_pan", "mast_tilt", "ground_elevation_m"}
```

**No `x`, no `y`, no `pose`.** Elevation is legitimately proprioceptive (leg
extension / suspension travel); planar position is not — the agent must use
the estimate from `observe()`, which carries drift. A test asserts the leak
cannot reappear.

### `move(distance_m) -> ActionResult`
Drive forward along the current heading. Stops at the first thing that
physically stops it. Integrated in 0.04 m slices so it cannot tunnel. Negative
distance is `INVALID`.

Stops for: `collision`, `step_too_high`, `out_of_bounds`, `reached`.

### `turn(delta_rad) -> ActionResult`
Rotate in place. Always succeeds — the footprint is a disc, so rotation cannot
collide.

### `stop() -> ActionResult`
Command a halt. Always valid, including when already stopped.

### `change_mobility_mode(mode) -> ActionResult`
`MobilityMode.WHEEL` ⇄ `MobilityMode.LEG`. Costs 4 s.

| | WHEEL | LEG |
|---|---|---|
| max speed | 0.90 m/s | 0.32 m/s |
| **max step height** | **0.06 m** | **0.25 m** |
| max turn rate | 1.20 rad/s | 0.70 rad/s |
| energy per metre | 1.0 | 3.4 |

The staircase has 0.18 m steps: impassable in wheel mode, passable in leg
mode. Requesting the mode you are already in returns `PARTIAL` /
`already_in_mode` — not `SUCCESS`, because nothing changed.

### `look(pan_rad, tilt_rad=0.0) -> ActionResult`
Aim the mast head. Limits ±120° pan, ±35° tilt. **Clamping is reported as
`PARTIAL` / `clamped_to_limits`**, never silently accepted — an agent that
believes it is looking somewhere it is not will misattribute everything it
sees.

### `push(distance_m) -> ActionResult`
Drive forward, displacing a movable object instead of stopping at it.
`detail["displaced"]` lists what actually moved, computed by comparing
positions before and after — not by assuming the push worked.

- Object shifts → `SUCCESS`/`PARTIAL`, `displaced` non-empty
- Object wedged → `BLOCKED` / `pushed_object_stuck`, `displaced` empty
- A wall → `BLOCKED` / `collision`, `displaced` empty

Plain `move` against the same object stops instead. That difference is tested
in both directions.

### `interact(verb, target_id) -> ActionResult`
Verbs: `pick_up`, `place`, `inspect`. Reach is 0.85 m.

| Situation | Result |
|---|---|
| In reach | `SUCCESS` / `grasped` |
| Too far | `BLOCKED` / `out_of_reach` |
| No such object | `BLOCKED` / `out_of_reach` |
| `place` while carrying nothing | `FAILED` / `not_carried` |
| Unknown verb | `INVALID` / `unknown_verb` |

### `capabilities() -> dict`
Embodiment, sensor list, reach, verbs. An agent may consult it, but must still
verify outcomes — **a capability claim is not a result.**

## Writing a different agent

```python
from arc2.control.api import RobotAPI
from arc2.world.model import WorldModel

class MyAgent:
    def __init__(self, api: RobotAPI, log, config):
        self.api = api
        self.model = WorldModel(24, 16)

    def run(self) -> dict:
        obs = self.api.observe()
        ...
        return {"actions_taken": n, "replans": r, ...}
```

Hold a `RobotAPI`. Do not import `arc2.simulation`.
