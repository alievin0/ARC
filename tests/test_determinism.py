"""Determinism and replay.

A seeded run must reproduce exactly. This is tested by comparing the SHA-256
digest of the whole event stream, not by spot-checking a few numbers -- a
partial check would pass on a run that diverged in an unchecked field.
"""
import unittest

from arc2.benchmark.runner import run_episode
from arc2.sensors.suite import SensorSuite
from arc2.simulation.simulator import SimConfig, Simulator
from arc2.types import MobilityMode


class TestSimulatorReset(unittest.TestCase):
    def test_reset_restores_pose_clock_and_world(self):
        sim = Simulator(SimConfig(seed=3))
        start = sim.state.pose.as_dict()
        crate0 = sim.spec.movables[0].position.as_tuple()
        sim.translate(2.0, allow_push=True)
        sim.rotate(1.0)
        sim.set_mode(MobilityMode.LEG)
        self.assertNotEqual(sim.state.pose.as_dict(), start)
        sim.reset()
        self.assertEqual(sim.state.pose.as_dict(), start)
        self.assertEqual(sim.spec.movables[0].position.as_tuple(), crate0)
        self.assertEqual(sim.tick, 0)
        self.assertEqual(sim.state.elapsed_s, 0.0)
        self.assertIs(sim.state.mode, MobilityMode.WHEEL)

    def test_reset_rewinds_the_random_stream(self):
        sim = Simulator(SimConfig(seed=3))
        first = [sim.rng.random() for _ in range(5)]
        sim.reset()
        self.assertEqual([sim.rng.random() for _ in range(5)], first)

    def test_replaying_the_same_commands_after_reset_gives_the_same_state(self):
        sim = Simulator(SimConfig(seed=9))
        suite = SensorSuite()

        def play():
            out = []
            for _ in range(6):
                out.append(suite.read(sim).lidar.ranges)
                sim.translate(0.4)
                sim.rotate(0.3)
            return out, sim.state.as_dict()

        a_obs, a_state = play()
        sim.reset()
        suite.reset()
        b_obs, b_state = play()
        self.assertEqual(a_obs, b_obs)
        self.assertEqual(a_state, b_state)


class TestEpisodeDeterminism(unittest.TestCase):
    def test_the_same_seed_reproduces_the_episode_exactly(self):
        a = run_episode(seed=4242, max_actions=120)
        b = run_episode(seed=4242, max_actions=120)
        self.assertEqual(a.metrics.log_digest, b.metrics.log_digest)
        # wall_time_s measures THIS MACHINE, not the episode, and is the one
        # field that legitimately varies between identical runs. Everything
        # else -- including simulated time and the full event digest -- must
        # match exactly.
        da, db = a.metrics.as_dict(), b.metrics.as_dict()
        da.pop("wall_time_s"), db.pop("wall_time_s")
        self.assertEqual(da, db)
        self.assertEqual(a.metrics.sim_time_s, b.metrics.sim_time_s)

    def test_a_different_seed_produces_a_different_episode(self):
        """Otherwise 'deterministic' would be indistinguishable from
        'ignores the seed'."""
        a = run_episode(seed=4242, max_actions=120)
        b = run_episode(seed=99, max_actions=120)
        self.assertNotEqual(a.metrics.log_digest, b.metrics.log_digest)

    def test_disabling_noise_changes_the_outcome(self):
        noisy = run_episode(seed=4242, max_actions=120)
        clean = run_episode(seed=4242, max_actions=120, sensor_noise=False)
        self.assertNotEqual(noisy.metrics.log_digest, clean.metrics.log_digest)

    def test_a_noiseless_run_is_also_reproducible(self):
        a = run_episode(seed=7, max_actions=120, sensor_noise=False)
        b = run_episode(seed=7, max_actions=120, sensor_noise=False)
        self.assertEqual(a.metrics.log_digest, b.metrics.log_digest)


if __name__ == "__main__":
    unittest.main()
