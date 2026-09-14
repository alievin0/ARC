"""Measured physical-task performance. No composite "intelligence score".

Every number here is either read from ground truth or counted from the
episode log. None of them is estimated, and none of them is a weighted blend
of other metrics -- a blend would hide exactly the trade-offs we want to see
(an agent that succeeds by brute-force wandering should look different from
one that succeeds efficiently, not average out to the same number).
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

from arc2.simulation.geometry import circle_intersects_aabb
from arc2.simulation.physics import blocking_boxes
from arc2.simulation.world_spec import WorldSpec
from arc2.types import Vec2
from arc2.world.belief import CellState, OccupancyBelief


@dataclass
class EpisodeMetrics:
    task_id: str
    seed: int
    success: bool
    failure_reason: str
    sim_time_s: float
    wall_time_s: float
    ticks: int
    distance_travelled_m: float
    energy_used: float
    actions: int
    failed_actions: int
    unnecessary_actions: int
    replans: int
    strategy_changes: int
    explored_fraction: float
    explored_cells_known: int
    reachable_cells_total: int
    objects_discovered: int
    mode_changes: int
    log_events: int
    log_digest: str

    def as_dict(self) -> dict:
        return asdict(self)


def reachable_cells(spec: WorldSpec, bel: OccupancyBelief,
                    start: Vec2, radius: float) -> set[tuple[int, int]]:
    """Ground-truth denominator for exploration: how much COULD be known.

    Flood fill over the true world at the belief's resolution, from the start,
    using the same clearance the robot has. Measuring explored fraction
    against the whole arena would silently punish the agent for space it can
    never legally occupy.
    """
    boxes = blocking_boxes(spec)

    def free(cx: int, cy: int) -> bool:
        if not bel.in_bounds(cx, cy):
            return False
        wx, wy = bel.to_world(cx, cy)
        p = Vec2(wx, wy)
        return not any(circle_intersects_aabb(p, radius, b) for _, b in boxes)

    start_cell = bel.to_cell(start.x, start.y)
    if not free(*start_cell):
        return set()
    seen = {start_cell}
    stack = [start_cell]
    while stack:
        cx, cy = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (cx + dx, cy + dy)
            if n not in seen and free(*n):
                seen.add(n)
                stack.append(n)
    return seen


def explored_fraction(bel: OccupancyBelief,
                      reachable: set[tuple[int, int]]) -> float:
    """Of the space the robot COULD have reached, how much does it know?

    Computed as a set intersection, not a ratio of two independently counted
    quantities. The earlier form divided "cells believed free" (which includes
    cells seen across a room but never occupiable) by "cells reachable", and
    so could exceed 1.0 and be clamped -- reporting full exploration while
    1257 cells were still UNKNOWN.
    """
    if not reachable:
        return 0.0
    known = sum(1 for c in reachable if bel.get(*c) is not CellState.UNKNOWN)
    return known / len(reachable)


def build(task_id: str, seed: int, outcome, sim, agent, log,
          wall_time_s: float, reachable: set[tuple[int, int]]) -> EpisodeMetrics:
    mode_changes = sum(1 for e in log.of_type("action_result")
                       if e["action"] == "change_mobility_mode"
                       and e["status"] == "success")
    return EpisodeMetrics(
        task_id=task_id,
        seed=seed,
        success=outcome.success,
        failure_reason="" if outcome.success else outcome.reason,
        sim_time_s=round(sim.state.elapsed_s, 3),
        wall_time_s=round(wall_time_s, 3),
        ticks=sim.tick,
        distance_travelled_m=round(sim.state.distance_travelled_m, 3),
        energy_used=round(sim.state.energy_used, 3),
        actions=agent.memory.total_actions,
        failed_actions=agent.memory.failed_actions,
        unnecessary_actions=agent.memory.unnecessary_actions(),
        replans=agent.replans,
        strategy_changes=agent.task.strategy_changes,
        explored_fraction=round(
            explored_fraction(agent.model.occupancy, reachable), 4),
        explored_cells_known=sum(
            1 for c in reachable
            if agent.model.occupancy.get(*c) is not CellState.UNKNOWN),
        reachable_cells_total=len(reachable),
        objects_discovered=len(agent.model.objects),
        mode_changes=mode_changes,
        log_events=len(log.events),
        log_digest=log.digest(),
    )
