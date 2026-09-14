"""End-to-end integration: the nine checks the milestone brief asks for.

Each test states what it PROVES in its name and docstring. "The episode ran"
is not the same claim as "the agent adapted", so they are separate tests.
"""
import json
import os
import tempfile
import unittest

from arc2.agent.loop import AgentConfig, DeliberativeAgent
from arc2.benchmark.runner import run_episode
from arc2.control.api import RobotAPI
from arc2.control.sim_backend import SimulatedRobotAPI
from arc2.sensors.base import Observation
from arc2.sensors.suite import SensorSuite
from arc2.simulation.simulator import SimConfig, Simulator
from arc2.telemetry.episode_log import EVENT_TYPES, EpisodeLog
from arc2.types import MobilityMode
from arc2.world.belief import CellState

SEED = 20260914
_EPISODE = None


def _episode():
    """Run the reference episode ONCE and share it across every check.

    Determinism is what makes this safe: the same seed gives the same episode,
    so one run can back every assertion instead of six identical runs.
    """
    global _EPISODE
    if _EPISODE is None:
        tmp = tempfile.mkdtemp(prefix="arc2-test-")
        path = os.path.join(tmp, "episode.jsonl")
        res = run_episode(seed=SEED, log_path=path)
        with open(path, encoding="utf-8") as fh:
            ev = [json.loads(l) for l in fh if l.strip()]
        _EPISODE = (res, path, ev)
    return _EPISODE


class EpisodeFixture(unittest.TestCase):
    """One full episode, shared by the checks below."""

    @classmethod
    def setUpClass(cls):
        cls.res, cls.path, cls.ev = _episode()


class TestCheck3_BenchmarkTask(EpisodeFixture):
    def test_the_benchmark_task_is_completed(self):
        self.assertTrue(self.res.outcome.success, self.res.outcome.reason)
        self.assertTrue(self.res.outcome.target_delivered)

    def test_success_is_judged_against_ground_truth_not_belief(self):
        truth = self.ev[-1]["truth"]["payloads"]["target_canister"]
        self.assertLessEqual(
            ((truth["pos"][0] - 2.0) ** 2 + (truth["pos"][1] - 2.2) ** 2) ** 0.5,
            1.0)

    def test_metrics_cover_every_quantity_the_brief_asks_for(self):
        m = self.res.metrics.as_dict()
        for field in ("success", "sim_time_s", "distance_travelled_m",
                      "failed_actions", "replans", "explored_fraction",
                      "unnecessary_actions", "actions"):
            self.assertIn(field, m)

    def test_no_composite_intelligence_score_is_reported(self):
        for k in self.res.metrics.as_dict():
            self.assertNotIn("score", k.lower())
            self.assertNotIn("intelligence", k.lower())


class TestCheck4_ObservationsReachTheAgent(EpisodeFixture):
    def test_the_agent_receives_structured_observations(self):
        obs = [e for e in self.ev if e["type"] == "observation"]
        self.assertGreater(len(obs), 10)
        first = obs[0]
        for key in ("lidar", "depth", "rgb", "imu", "joints", "pose_estimate"):
            self.assertIn(key, first)
        self.assertEqual(first["lidar"]["n_beams"], 72)

    def test_an_observation_is_a_typed_object_not_a_dict(self):
        sim = Simulator(SimConfig(seed=1))
        self.assertIsInstance(SimulatedRobotAPI(sim, SensorSuite()).observe(),
                              Observation)


class TestCheck5_ActionsGoThroughTheApi(EpisodeFixture):
    def test_every_logged_action_is_a_declared_api_verb(self):
        verbs = {"move", "turn", "stop", "change_mobility_mode", "look",
                 "push", "interact"}
        acted = {e["action"] for e in self.ev if e["type"] == "action"}
        self.assertTrue(acted)
        self.assertTrue(acted <= verbs, f"non-API actions logged: {acted - verbs}")

    def test_the_agent_holds_only_a_RobotAPI_and_never_the_simulator(self):
        sim = Simulator(SimConfig(seed=1))
        agent = DeliberativeAgent(SimulatedRobotAPI(sim, SensorSuite()),
                                  EpisodeLog(), AgentConfig(max_actions=1))
        self.assertIsInstance(agent.api, RobotAPI)
        for attr in vars(agent).values():
            self.assertNotIsInstance(attr, Simulator)

    def test_the_agent_never_imports_the_simulation_layer(self):
        import arc2.agent.loop as loop
        with open(loop.__file__, encoding="utf-8") as fh:
            src = fh.read()
        for banned in ("from arc2.simulation", "import arc2.simulation",
                       "world_spec", "truth_snapshot"):
            self.assertNotIn(banned, src,
                             f"agent reaches into ground truth via {banned!r}")


class TestCheck6_WorldModelUpdates(EpisodeFixture):
    def test_the_belief_grows_over_the_episode(self):
        per = [e for e in self.ev if e["type"] == "perception"]
        self.assertGreater(sum(e["new_cells"] for e in per), 500)

    def test_objects_are_discovered_rather_than_given(self):
        wm = self.ev[-1]["agent"]["world_model"]
        self.assertGreater(len(wm["objects"]), 1)
        self.assertIn("canister", [o["label"] for o in wm["objects"].values()])

    def test_the_agent_does_not_claim_to_know_the_whole_world(self):
        """Partial observability must survive to the end of the episode."""
        wm = self.ev[-1]["agent"]["world_model"]
        self.assertGreater(wm["cells"][CellState.UNKNOWN.value], 0)

    def test_all_three_epistemic_states_are_actually_used(self):
        wm = self.ev[-1]["agent"]["world_model"]["cells"]
        for state in (CellState.UNKNOWN, CellState.FREE, CellState.BLOCKED):
            self.assertGreater(wm[state.value], 0, state.value)

    def test_a_failed_action_writes_a_blockage_into_the_belief(self):
        self.assertTrue([e for e in self.ev if e["type"] == "world_update"
                         and e["source"] == "action_failure"])


class TestCheck7_FailureCausesReplanning(EpisodeFixture):
    def test_the_world_falsified_at_least_one_plan(self):
        self.assertGreater(len([e for e in self.ev if e["type"] == "failure"]), 0)

    def test_failure_is_followed_by_replanning(self):
        self.assertGreater(self.res.metrics.replans, 0)
        causes = {e["cause"].split(":")[0]
                  for e in self.ev if e["type"] == "replan"}
        self.assertIn("failure", causes)

    def test_failure_is_detected_in_more_than_one_way(self):
        """Reported status is not the only detector; a stalled move and an
        inferred route conflict are independent evidence."""
        modes = {e["detection"] for e in self.ev if e["type"] == "failure"}
        self.assertIn("reported", modes)
        causes = {e["cause"].split(":")[0]
                  for e in self.ev if e["type"] == "replan"}
        self.assertTrue({"inferred", "goal_changed"} & causes)

    def test_the_agent_changed_strategy_not_merely_retried(self):
        self.assertGreater(self.res.metrics.strategy_changes, 0)
        strategies = {e["strategy"] for e in self.ev if e["type"] == "replan"}
        self.assertGreater(len(strategies), 1, f"only used {strategies}")

    def test_a_physical_limit_was_overcome_by_changing_the_body(self):
        """The staircase gate: adaptation by embodiment, not by re-routing."""
        self.assertGreaterEqual(self.res.metrics.mode_changes, 1)
        self.assertTrue([e for e in self.ev if e["type"] == "task_progress"
                         and e["event"] == "mobility_mode_changed"])

    def test_the_full_observe_plan_act_detect_replan_cycle_is_present(self):
        order = [e["type"] for e in self.ev]
        for t in ("observation", "perception", "decision", "plan", "action",
                  "action_result", "failure", "replan", "task_progress"):
            self.assertIn(t, order, t)


class TestCheck8_EpisodeIsLogged(EpisodeFixture):
    def test_the_log_is_newline_delimited_json_and_fully_parseable(self):
        with open(self.path) as fh:
            lines = [l for l in fh if l.strip()]
        self.assertGreater(len(lines), 100)
        for l in lines:
            json.loads(l)

    def test_every_event_carries_the_common_envelope(self):
        for e in self.ev:
            for key in ("schema_version", "seq", "tick", "sim_time_s", "type"):
                self.assertIn(key, e)
            self.assertIn(e["type"], EVENT_TYPES)

    def test_sequence_numbers_are_contiguous(self):
        self.assertEqual([e["seq"] for e in self.ev],
                         list(range(1, len(self.ev) + 1)))

    def test_the_log_opens_and_closes_the_episode(self):
        self.assertEqual(self.ev[0]["type"], "episode_start")
        self.assertEqual(self.ev[-1]["type"], "episode_end")
        self.assertIn("seed", self.ev[0])
        self.assertIn("outcome", self.ev[-1])

    def test_the_task_brief_records_what_the_agent_was_NOT_told(self):
        brief = self.ev[0]["task"]
        self.assertFalse(brief["given_target_coordinates"])
        self.assertFalse(brief["given_map"])

    def test_an_unknown_event_type_is_rejected(self):
        with self.assertRaises(ValueError):
            EpisodeLog().emit("not_a_real_event", 0, 0.0)

    def test_the_summary_counts_every_required_quantity(self):
        end = self.ev[-1]["agent"]
        self.assertIn("replans", end)
        self.assertIn("failed_actions", end["memory"])
        self.assertIn("unnecessary_actions", end["memory"])


class TestCheck9_ResetAndReplay(unittest.TestCase):
    def test_an_episode_can_be_rerun_from_scratch_in_one_process(self):
        a = run_episode(seed=31, max_actions=150)
        b = run_episode(seed=31, max_actions=150)
        self.assertEqual(a.metrics.log_digest, b.metrics.log_digest)

    def test_the_simulator_can_be_reset_and_driven_again(self):
        sim = Simulator(SimConfig(seed=31))
        api = SimulatedRobotAPI(sim, SensorSuite())
        api.move(2.0)
        api.change_mobility_mode(MobilityMode.LEG)
        sim.reset()
        self.assertIs(sim.state.mode, MobilityMode.WHEEL)
        self.assertEqual(sim.state.distance_travelled_m, 0.0)
        self.assertTrue(api.move(0.5).progressed)


if __name__ == "__main__":
    unittest.main()
