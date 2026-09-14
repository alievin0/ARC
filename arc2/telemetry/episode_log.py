"""Machine-readable episode log: newline-delimited JSON, one event per line.

Every line is a complete, independently parseable JSON object with the same
envelope: {schema_version, seq, tick, sim_time_s, type, ...payload}. That
makes the log streamable and greppable, and means a truncated file is still
readable up to the truncation.

The event vocabulary is closed and declared in EVENT_TYPES so a consumer can
assert it has handled all of them.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field

from arc2 import SCHEMA_VERSION

EVENT_TYPES = (
    "episode_start",
    "capabilities",
    "observation",
    "perception",
    "decision",
    "plan",
    "replan",
    "action",
    "action_result",
    "world_update",
    "failure",
    "task_progress",
    "note",
    "episode_end",
)


class EpisodeLog:
    def __init__(self, path: str | None = None, keep_in_memory: bool = True,
                 full_observations: bool = True) -> None:
        self.path = path
        self.events: list[dict] = []
        self.keep_in_memory = keep_in_memory
        self.full_observations = full_observations
        self._seq = 0
        self._fh = None
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            self._fh = open(path, "w", encoding="utf-8")

    def emit(self, etype: str, tick: int, sim_time_s: float, **payload) -> dict:
        if etype not in EVENT_TYPES:
            raise ValueError(f"unknown event type {etype!r}")
        self._seq += 1
        ev = {"schema_version": SCHEMA_VERSION, "seq": self._seq, "tick": tick,
              "sim_time_s": round(sim_time_s, 3), "type": etype, **payload}
        if self.keep_in_memory:
            self.events.append(ev)
        if self._fh:
            self._fh.write(json.dumps(ev, sort_keys=True, separators=(",", ":")))
            self._fh.write("\n")
        return ev

    def close(self) -> None:
        if self._fh:
            self._fh.close()
            self._fh = None

    # -- analysis helpers --------------------------------------------------
    def of_type(self, etype: str) -> list[dict]:
        return [e for e in self.events if e["type"] == etype]

    def counts(self) -> dict[str, int]:
        out = {t: 0 for t in EVENT_TYPES}
        for e in self.events:
            out[e["type"]] += 1
        return out

    def digest(self) -> str:
        """Stable hash of the whole episode.

        Used by the determinism test: same seed must give the same digest.
        Wall-clock fields are excluded because they are not part of the
        simulated episode.
        """
        h = hashlib.sha256()
        for e in self.events:
            clean = {k: v for k, v in e.items() if k not in ("wall_time", "log_path")}
            h.update(json.dumps(clean, sort_keys=True, separators=(",", ":"))
                     .encode("utf-8"))
        return h.hexdigest()


def write_summary(path: str, summary: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")
