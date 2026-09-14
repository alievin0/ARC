"""A* over the BELIEF grid, plus frontier selection.

The design choice that makes failure emergent rather than scripted:

    UNKNOWN cells are treated as traversable, at a cost penalty.

That is what a real explorer must do -- you cannot route only through proven
space or you can never leave the room. It also means the first plan through
an unexplored corridor is a genuine hypothesis that the world is free to
falsify. The dead-end corridor in the Milestone-1 arena is not flagged for
the agent; the agent plans into it because it looks like a route, and finds
out otherwise. That is the behaviour the benchmark measures.
"""
from __future__ import annotations

import heapq
import math

from arc2.world.belief import CellState, OccupancyBelief

#: Multiplier on the cost of entering an unexplored cell. >1 so a proven route
#: is preferred when one exists, but finite so exploration is possible.
UNKNOWN_COST = 1.8
UNCERTAIN_COST = 2.6
#: The chassis is a 0.40 m disc on a 0.25 m grid, so a cell whose centre is
#: within one grid step (0.25 m orthogonal, 0.354 m diagonal) of a BLOCKED
#: cell cannot physically be occupied. This is a HARD constraint, not a
#: penalty: as a penalty the planner produced paths that grazed obstacles and
#: the robot then collided while following the plan correctly -- measured as
#: 345 consecutive blocked moves against one pillar.
#:
#: One cell of inflation is the largest value that keeps the 1.1 m narrow
#: passage open (its two central cells sit 0.5 m from either wall);
#: tests/test_planning.py asserts both halves of that trade-off.
CLEARANCE_CELLS = 1

_NEIGHBOURS = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
               (1, 1, 1.41421356), (1, -1, 1.41421356),
               (-1, 1, 1.41421356), (-1, -1, 1.41421356)]


def _passable(bel: OccupancyBelief, cx: int, cy: int) -> bool:
    """Can the CHASSIS occupy this cell -- not merely, is the cell empty."""
    if not bel.in_bounds(cx, cy) or bel.get(cx, cy) is CellState.BLOCKED:
        return False
    return not _near_blocked(bel, cx, cy)


def _near_blocked(bel: OccupancyBelief, cx: int, cy: int) -> bool:
    r = CLEARANCE_CELLS
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if bel.get(cx + dx, cy + dy) is CellState.BLOCKED:
                return True
    return False


def cell_cost(bel: OccupancyBelief, cx: int, cy: int) -> float:
    s = bel.get(cx, cy)
    return {CellState.FREE: 1.0, CellState.UNKNOWN: UNKNOWN_COST,
            CellState.UNCERTAIN: UNCERTAIN_COST}.get(s, math.inf)


def _escape_zone(start: tuple[int, int], radius: int = 2) -> set[tuple[int, int]]:
    """Cells near the start that bypass the clearance test.

    The robot stops ON contact, which can leave it inside the inflated zone of
    the thing it touched. Without this relaxation the planner cannot route out
    of the position the robot is actually in, and the agent wedges permanently
    -- measured as 388 consecutive blocked moves in a doorway corner.
    """
    return {(start[0] + dx, start[1] + dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)}


def astar(bel: OccupancyBelief, start: tuple[int, int], goal: tuple[int, int],
          max_expansions: int = 60000) -> list[tuple[int, int]] | None:
    """Shortest belief-cost path. None if unreachable within the budget.

    Deterministic: ties are broken by the cell coordinate, so two runs with
    identical beliefs produce byte-identical paths.
    """
    escape = _escape_zone(start)

    def passable(c: tuple[int, int]) -> bool:
        if c in escape:
            # Near the start, only true occupancy matters -- not clearance.
            return bel.in_bounds(*c) and bel.get(*c) is not CellState.BLOCKED
        return _passable(bel, *c)

    if not passable(goal):
        goal = _nearest_passable(bel, goal)
        if goal is None:
            return None
    if start == goal:
        return [start]

    def h(c):
        return math.hypot(c[0] - goal[0], c[1] - goal[1])

    open_heap = [(h(start), 0.0, start)]
    came: dict[tuple[int, int], tuple[int, int]] = {}
    gscore = {start: 0.0}
    closed: set[tuple[int, int]] = set()
    expansions = 0

    while open_heap:
        _, g, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        expansions += 1
        if expansions > max_expansions:
            return None
        if cur == goal:
            return _reconstruct(came, cur)
        for dx, dy, step in _NEIGHBOURS:
            nb = (cur[0] + dx, cur[1] + dy)
            if nb in closed or not passable(nb):
                continue
            if dx and dy:  # no corner cutting
                if not (passable((cur[0] + dx, cur[1]))
                        and passable((cur[0], cur[1] + dy))):
                    continue
            c = cell_cost(bel, *nb)
            if c is math.inf:
                continue
            ng = g + step * c
            if ng < gscore.get(nb, math.inf):
                gscore[nb] = ng
                came[nb] = cur
                heapq.heappush(open_heap, (ng + h(nb), ng, nb))
    return None


def _reconstruct(came, cur):
    path = [cur]
    while cur in came:
        cur = came[cur]
        path.append(cur)
    path.reverse()
    return path


def _nearest_passable(bel: OccupancyBelief, goal: tuple[int, int],
                      radius: int = 6) -> tuple[int, int] | None:
    best, best_d = None, math.inf
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            c = (goal[0] + dx, goal[1] + dy)
            if _passable(bel, *c):
                d = dx * dx + dy * dy
                if d < best_d:
                    best, best_d = c, d
    return best


def is_occupiable(bel: OccupancyBelief, cx: int, cy: int) -> bool:
    """Public form of the chassis-clearance test, for goal selection."""
    return _passable(bel, cx, cy)


def choose_frontier(bel: OccupancyBelief, from_cell: tuple[int, int],
                    penalise=None, min_distance_cells: int = 3
                    ) -> tuple[int, int] | None:
    """Pick where to explore next.

    Nearest-frontier, with two corrections that matter:
      * a caller-supplied `penalise(world_x, world_y) -> float` lets memory
        push the agent away from places it has already disproved;
      * frontiers closer than `min_distance_cells` are skipped so the agent
        does not nibble at its own shoulder.
    """
    frontiers = bel.frontier_cells()
    if not frontiers:
        return None
    best, best_score = None, math.inf
    for f in sorted(frontiers):
        # A frontier cell the chassis cannot occupy is not somewhere to go.
        # Selecting one produced a goal inside a wall, which the agent then
        # drove at 879 consecutive times.
        if not _passable(bel, *f):
            continue
        d = math.hypot(f[0] - from_cell[0], f[1] - from_cell[1])
        if d < min_distance_cells:
            continue
        score = d
        if penalise is not None:
            wx, wy = bel.to_world(*f)
            score += penalise(wx, wy)
        if score < best_score:
            best, best_score = f, score
    return best


def simplify(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Collapse collinear runs into waypoints."""
    if len(path) < 3:
        return list(path)
    out = [path[0]]
    for i in range(1, len(path) - 1):
        ax, ay = path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]
        bx, by = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
        if (ax, ay) != (bx, by):
            out.append(path[i])
    out.append(path[-1])
    return out
