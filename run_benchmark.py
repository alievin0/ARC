#!/usr/bin/env python3
"""ARC-2 Milestone-1 benchmark entry point.

    python3 run_benchmark.py                    # one episode, default seed
    python3 run_benchmark.py --seed 7           # a different world/episode
    python3 run_benchmark.py --seeds 1 2 3 4 5  # a suite, with a summary
    python3 run_benchmark.py --no-noise         # noiseless sensors
    python3 run_benchmark.py --quiet-log        # digest observations only
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys

from arc2.benchmark.runner import run_episode
from arc2.telemetry.episode_log import write_summary

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run the ARC-2 benchmark task.")
    ap.add_argument("--seed", type=int, default=20260914)
    ap.add_argument("--seeds", type=int, nargs="+",
                    help="run several seeds and summarise")
    ap.add_argument("--max-actions", type=int, default=1500)
    ap.add_argument("--no-noise", action="store_true",
                    help="disable sensor and odometry noise")
    ap.add_argument("--quiet-log", action="store_true",
                    help="log observation digests instead of full arrays")
    ap.add_argument("--log-dir", default=LOG_DIR)
    args = ap.parse_args(argv)

    seeds = args.seeds or [args.seed]
    rows = []
    for seed in seeds:
        path = os.path.join(args.log_dir, f"episode_seed{seed}.jsonl")
        res = run_episode(seed=seed, log_path=path,
                          max_actions=args.max_actions,
                          sensor_noise=not args.no_noise,
                          full_observations=not args.quiet_log)
        m = res.metrics.as_dict()
        m["log_path"] = path
        rows.append(m)
        print(f"seed {seed:>9}  success={str(m['success']):<5} "
              f"actions={m['actions']:<4} failed={m['failed_actions']:<4} "
              f"replans={m['replans']:<4} dist={m['distance_travelled_m']:>7.1f}m "
              f"explored={m['explored_fraction']:.2f}  -> {path}")
        if not m["success"]:
            print(f"                 reason: {m['failure_reason']}")

    summary = {
        "episodes": len(rows),
        "successes": sum(1 for r in rows if r["success"]),
        "success_rate": round(sum(1 for r in rows if r["success"]) / len(rows), 4),
        "median_actions": statistics.median(r["actions"] for r in rows),
        "median_distance_m": round(
            statistics.median(r["distance_travelled_m"] for r in rows), 3),
        "median_replans": statistics.median(r["replans"] for r in rows),
        "median_explored_fraction": round(
            statistics.median(r["explored_fraction"] for r in rows), 4),
        "episodes_detail": rows,
    }
    out = os.path.join(args.log_dir, "benchmark_summary.json")
    write_summary(out, summary)
    print(f"\n{summary['successes']}/{summary['episodes']} succeeded "
          f"({summary['success_rate']:.0%})   summary -> {out}")
    return 0 if summary["successes"] == summary["episodes"] else 1


if __name__ == "__main__":
    sys.exit(main())
