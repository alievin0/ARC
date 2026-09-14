"""Run one episode end to end and produce metrics + logs."""
from __future__ import annotations

import time
from dataclasses import dataclass

from arc2.agent.loop import AgentConfig, DeliberativeAgent
from arc2.benchmark import metrics as M
from arc2.control.sim_backend import SimulatedRobotAPI
from arc2.robot import embodiment as emb
from arc2.sensors.suite import SensorSuite
from arc2.simulation.simulator import SimConfig, Simulator
from arc2.simulation.world_spec import ARENA_H, ARENA_W, START_POSITION
from arc2.tasks import retrieve_and_return as task
from arc2.telemetry.episode_log import EpisodeLog


@dataclass
class EpisodeResult:
    metrics: M.EpisodeMetrics
    outcome: task.TaskOutcome
    agent_report: dict
    log: EpisodeLog


def run_episode(seed: int = 20260914, log_path: str | None = None,
                max_actions: int = 1500, sensor_noise: bool = True,
                full_observations: bool = True,
                keep_log_in_memory: bool = True) -> EpisodeResult:
    t0 = time.perf_counter()

    sim = Simulator(SimConfig(seed=seed, sensor_noise=sensor_noise))
    suite = SensorSuite()
    api = SimulatedRobotAPI(sim, suite)
    log = EpisodeLog(log_path, keep_in_memory=keep_log_in_memory,
                     full_observations=full_observations)

    log.emit("episode_start", 0, 0.0, seed=seed, task=task.brief(),
             arena={"w": ARENA_W, "h": ARENA_H},
             sensor_noise=sensor_noise)
    log.emit("capabilities", 0, 0.0, **api.capabilities())

    agent = DeliberativeAgent(api, log, AgentConfig(
        arena_w=ARENA_W, arena_h=ARENA_H, max_actions=max_actions,
        target_label=task.TARGET_LABEL))
    report = agent.run()

    outcome = task.evaluate(sim)
    reachable = M.reachable_cells(sim.spec, agent.model.occupancy,
                                  START_POSITION, emb.COLLISION_RADIUS)
    log.emit("episode_end", sim.tick, sim.state.elapsed_s,
             outcome=outcome.as_dict(), agent=report,
             truth=sim.truth_snapshot())

    m = M.build(task.TASK_ID, seed, outcome, sim, agent, log,
                time.perf_counter() - t0, reachable)
    log.close()
    return EpisodeResult(m, outcome, report, log)
