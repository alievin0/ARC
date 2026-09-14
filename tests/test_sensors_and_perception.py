"""Sensors and the perception pipeline.

The load-bearing assertion in this file is that perception NEVER writes what
was not sensed: cells beyond the LiDAR horizon must remain UNKNOWN. An agent
whose map quietly fills in unobserved space is not solving the task we set.
"""
import math
import unittest

from arc2.perception.pipeline import integrate
from arc2.robot import embodiment as emb
from arc2.sensors.exteroceptive import (LIDAR_BEAMS, LIDAR_MAX_RANGE,
                                        RGB_CONFIDENT_RANGE, Lidar360,
                                        RgbCamera)
from arc2.sensors.suite import SensorSuite
from arc2.simulation.simulator import SimConfig, Simulator
from arc2.simulation.world_spec import TARGET_ID
from arc2.types import Pose, Vec2
from arc2.world.belief import CellState
from arc2.world.model import Knowledge, WorldModel


class TestLidar(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator(SimConfig(seed=5, sensor_noise=False))

    def test_scan_shape_and_range_bounds(self):
        scan = Lidar360().read(self.sim)
        self.assertEqual(len(scan.ranges), LIDAR_BEAMS)
        self.assertEqual(len(scan.bearings), LIDAR_BEAMS)
        self.assertTrue(all(0.0 <= r <= LIDAR_MAX_RANGE for r in scan.ranges))

    def test_some_beams_see_nothing_so_the_world_stays_partial(self):
        scan = Lidar360().read(self.sim)
        unreturned = sum(1 for r in scan.ranges if r >= LIDAR_MAX_RANGE - 1e-9)
        self.assertGreater(unreturned, 0,
                           "a scan that sees everything is not partial "
                           "observability")

    def test_scan_originates_from_the_mast_not_the_chassis_centre(self):
        scan = Lidar360().read(self.sim)
        self.assertAlmostEqual(scan.origin_height,
                               emb.sensor_head_height(self.sim.state.pose),
                               places=6)

    def test_noise_is_reproducible_for_a_given_seed(self):
        a = Simulator(SimConfig(seed=11, sensor_noise=True))
        b = Simulator(SimConfig(seed=11, sensor_noise=True))
        self.assertEqual(Lidar360().read(a).ranges, Lidar360().read(b).ranges)

    def test_noise_actually_perturbs_the_readings(self):
        clean = Lidar360().read(Simulator(SimConfig(seed=11, sensor_noise=False)))
        noisy = Lidar360().read(Simulator(SimConfig(seed=11, sensor_noise=True)))
        self.assertNotEqual(clean.ranges, noisy.ranges)


class TestRgb(unittest.TestCase):
    def test_close_object_gets_a_specific_label(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        sim.state.pose = Pose(7.5, 11.5, math.pi / 2, 0.0)   # ~1.7 m from target
        dets = RgbCamera().read(sim).detections
        hit = next((d for d in dets if d.object_id == TARGET_ID), None)
        self.assertIsNotNone(hit, "target must be visible from 1.7 m ahead")
        self.assertEqual(hit.label, "canister")
        self.assertGreater(hit.confidence, 0.55)

    def test_distant_object_degrades_to_unknown_with_low_confidence(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        sim.state.pose = Pose(7.5, 8.5, math.pi / 2, 0.0)    # ~4.7 m away
        dets = RgbCamera().read(sim).detections
        hit = next((d for d in dets if d.object_id == TARGET_ID), None)
        self.assertIsNotNone(hit)
        self.assertGreater(hit.range_m, RGB_CONFIDENT_RANGE)
        self.assertEqual(hit.label, "unknown_object")

    def test_object_behind_a_wall_is_not_detected(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        sim.state.pose = Pose(7.5, 4.5, math.pi / 2, 0.0)    # divider between
        dets = RgbCamera().read(sim).detections
        self.assertIsNone(next((d for d in dets if d.object_id == TARGET_ID), None))

    def test_object_outside_the_field_of_view_is_not_detected(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        sim.state.pose = Pose(7.5, 11.5, -math.pi / 2, 0.0)  # facing away
        dets = RgbCamera().read(sim).detections
        self.assertIsNone(next((d for d in dets if d.object_id == TARGET_ID), None))


class TestImuAndProprioception(unittest.TestCase):
    def test_imu_reports_slope_on_the_stairs_and_none_on_the_floor(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        suite = SensorSuite()
        self.assertAlmostEqual(suite.read(sim).imu.ground_slope, 0.0, places=6)
        sim.state.pose = Pose(19.0, 6.0, math.pi / 2, 0.0)
        self.assertGreater(abs(suite.read(sim).imu.ground_slope), 0.1)

    def test_joint_state_reports_every_declared_dof(self):
        sim = Simulator(SimConfig(seed=5))
        obs = SensorSuite().read(sim)
        self.assertEqual(set(obs.joints.positions), set(emb.JOINT_NAMES))


class TestOdometryDrift(unittest.TestCase):
    def test_pose_estimate_is_not_ground_truth_after_moving(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=True))
        suite = SensorSuite()
        suite.read(sim)
        sim.translate(3.0)
        est = suite.read(sim).pose_estimate
        self.assertNotEqual((est.x, est.y), (sim.state.pose.x, sim.state.pose.y))

    def test_confidence_degrades_as_drift_accumulates(self):
        sim = Simulator(SimConfig(seed=5, sensor_noise=True))
        suite = SensorSuite()
        first = suite.read(sim).pose_confidence
        for _ in range(6):
            sim.translate(0.5)
            last = suite.read(sim).pose_confidence
        self.assertLessEqual(last, first)


class TestPerceptionHonesty(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator(SimConfig(seed=5, sensor_noise=False))
        self.model = WorldModel(24, 16)
        self.report = integrate(self.model, SensorSuite().read(self.sim))

    def test_a_single_scan_reveals_only_a_small_part_of_the_arena(self):
        total = self.model.occupancy.nx * self.model.occupancy.ny
        self.assertLess(self.model.occupancy.known_cells() / total, 0.25)

    def test_space_beyond_the_lidar_horizon_stays_unknown(self):
        """THE load-bearing assertion of the perception layer."""
        for x, y in ((22.0, 14.0), (19.0, 12.0), (2.0, 14.0)):
            self.assertIs(self.model.occupancy.at(x, y), CellState.UNKNOWN,
                          f"({x},{y}) is far beyond the {LIDAR_MAX_RANGE} m "
                          "horizon and must not be claimed as known")

    def test_space_along_a_returning_ray_becomes_free(self):
        self.assertIs(self.model.occupancy.at(2.0, 4.0), CellState.FREE)

    def test_the_wall_that_returned_the_ray_becomes_blocked(self):
        row = [self.model.occupancy.at(x / 10.0, 5.7)
               for x in range(10, 60)]
        self.assertIn(CellState.BLOCKED, row)

    def test_reintegrating_the_same_scan_reveals_nothing_new(self):
        second = integrate(self.model, SensorSuite().read(self.sim))
        self.assertGreater(self.report.new_cells, 0)
        self.assertLess(second.new_cells, self.report.new_cells)

    def test_unseen_target_is_absent_not_approximated(self):
        self.assertIsNone(self.model.find_by_label("canister"))

    def test_low_confidence_detection_lands_as_uncertain(self):
        m = WorldModel(24, 16)
        m.observe_object("x", "unknown_object", Vec2(7, 13), 0.30, 1)
        self.assertIs(m.objects["x"].knowledge, Knowledge.UNCERTAIN)
        m.observe_object("x", "canister", Vec2(7.2, 13.1), 0.92, 4)
        self.assertIs(m.objects["x"].knowledge, Knowledge.KNOWN)
        self.assertEqual(m.objects["x"].label, "canister")


if __name__ == "__main__":
    unittest.main()
