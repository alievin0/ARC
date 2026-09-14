"""The occupancy belief: a tri-state grid over the arena.

The rule this file enforces, and the reason it is separate from the world
spec: a cell is UNKNOWN until a sensor return says otherwise. "Not observed"
and "observed to be free" are different values and are never merged. An agent
that plans through UNKNOWN space is taking a real risk, and the benchmark
measures what happens when that risk does not pay off.
"""
from __future__ import annotations

from enum import Enum


class CellState(str, Enum):
    UNKNOWN = "unknown"        # never sensed
    FREE = "free"              # sensed, traversable
    BLOCKED = "blocked"        # sensed, something solid is there
    UNCERTAIN = "uncertain"    # conflicting or low-confidence returns


class OccupancyBelief:
    """Uniform grid. Coarse on purpose -- planning resolution, not mapping."""

    def __init__(self, width_m: float, height_m: float, resolution: float = 0.25):
        self.resolution = resolution
        self.nx = int(round(width_m / resolution))
        self.ny = int(round(height_m / resolution))
        self._cells: list[CellState] = [CellState.UNKNOWN] * (self.nx * self.ny)
        #: How many times a cell has been reported free vs blocked. Used to
        #: promote a contested cell to UNCERTAIN rather than letting the last
        #: writer win.
        self._free_hits: dict[int, int] = {}
        self._block_hits: dict[int, int] = {}

    # -- indexing ----------------------------------------------------------
    def to_cell(self, x: float, y: float) -> tuple[int, int]:
        return (int(x // self.resolution), int(y // self.resolution))

    def to_world(self, cx: int, cy: int) -> tuple[float, float]:
        return ((cx + 0.5) * self.resolution, (cy + 0.5) * self.resolution)

    def in_bounds(self, cx: int, cy: int) -> bool:
        return 0 <= cx < self.nx and 0 <= cy < self.ny

    def _idx(self, cx: int, cy: int) -> int:
        return cy * self.nx + cx

    # -- reading -----------------------------------------------------------
    def get(self, cx: int, cy: int) -> CellState:
        if not self.in_bounds(cx, cy):
            return CellState.BLOCKED      # outside the arena is solid by definition
        return self._cells[self._idx(cx, cy)]

    def at(self, x: float, y: float) -> CellState:
        return self.get(*self.to_cell(x, y))

    # -- writing -----------------------------------------------------------
    def mark_free(self, cx: int, cy: int) -> bool:
        """Returns True if this observation revealed something new."""
        return self._mark(cx, cy, free=True)

    def mark_blocked(self, cx: int, cy: int) -> bool:
        return self._mark(cx, cy, free=False)

    def _mark(self, cx: int, cy: int, free: bool) -> bool:
        if not self.in_bounds(cx, cy):
            return False
        i = self._idx(cx, cy)
        was = self._cells[i]
        if free:
            self._free_hits[i] = self._free_hits.get(i, 0) + 1
        else:
            self._block_hits[i] = self._block_hits.get(i, 0) + 1

        f, b = self._free_hits.get(i, 0), self._block_hits.get(i, 0)
        if b == 0:
            new = CellState.FREE
        elif f == 0:
            new = CellState.BLOCKED
        elif b >= f * 2:
            new = CellState.BLOCKED
        elif f >= b * 2:
            new = CellState.FREE
        else:
            new = CellState.UNCERTAIN
        self._cells[i] = new
        return was is CellState.UNKNOWN

    def force_blocked(self, cx: int, cy: int) -> None:
        """Assert a blockage from a FAILED ACTION rather than from a ray.

        A motion that physically stopped is stronger evidence than any number
        of range returns, so it overrides the hit counts.
        """
        if not self.in_bounds(cx, cy):
            return
        i = self._idx(cx, cy)
        self._block_hits[i] = self._block_hits.get(i, 0) + 8
        self._cells[i] = CellState.BLOCKED

    # -- summaries ---------------------------------------------------------
    def counts(self) -> dict[str, int]:
        out = {s.value: 0 for s in CellState}
        for c in self._cells:
            out[c.value] += 1
        return out

    def known_cells(self) -> int:
        return sum(1 for c in self._cells if c is not CellState.UNKNOWN)

    def frontier_cells(self) -> list[tuple[int, int]]:
        """FREE cells that touch UNKNOWN space -- the boundary of knowledge."""
        out = []
        for cy in range(self.ny):
            for cx in range(self.nx):
                if self._cells[self._idx(cx, cy)] is not CellState.FREE:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx_, ny_ = cx + dx, cy + dy
                    if self.in_bounds(nx_, ny_) and \
                            self._cells[self._idx(nx_, ny_)] is CellState.UNKNOWN:
                        out.append((cx, cy))
                        break
        return out
