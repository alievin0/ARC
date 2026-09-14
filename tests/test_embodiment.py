"""The embodiment. The mast-mount requirement is asserted explicitly because
it is a stated requirement, not a placeholder dimension."""
import math
import unittest

from arc2.robot import embodiment as emb
from arc2.robot.state import RobotState, update_joint_kinematics
from arc2.types import MobilityMode, Pose, Vec2


class TestMastMounting(unittest.TestCase):
    def test_mast_is_on_the_front_third_not_the_middle(self):
        front_third_start = emb.BODY_LENGTH / 2 - emb.BODY_LENGTH / 3
        front_edge = emb.BODY_LENGTH / 2
        self.assertGreaterEqual(emb.MAST_MOUNT.x, front_third_start)
        self.assertLessEqual(emb.MAST_MOUNT.x, front_edge)
        # And explicitly NOT at the chassis centre.
        self.assertNotAlmostEqual(emb.MAST_MOUNT.x, 0.0, places=3)

    def test_mast_is_on_the_longitudinal_centreline(self):
        self.assertEqual(emb.MAST_MOUNT.y, 0.0)

    def test_sensor_head_moves_with_heading(self):
        p0 = emb.sensor_head_position(Pose(5, 5, 0.0))
        self.assertAlmostEqual(p0.x, 5 + emb.MAST_MOUNT.x, places=6)
        self.assertAlmostEqual(p0.y, 5.0, places=6)
        p90 = emb.sensor_head_position(Pose(5, 5, math.pi / 2))
        self.assertAlmostEqual(p90.x, 5.0, places=6)
        self.assertAlmostEqual(p90.y, 5 + emb.MAST_MOUNT.x, places=6)

    def test_sensor_head_is_above_the_chassis(self):
        self.assertGreater(emb.sensor_head_height(Pose(0, 0, 0)),
                           emb.BODY_HEIGHT)


class TestModes(unittest.TestCase):
    def test_leg_mode_climbs_higher_but_moves_slower(self):
        w = emb.MODE_CAPABILITIES[MobilityMode.WHEEL]
        l = emb.MODE_CAPABILITIES[MobilityMode.LEG]
        self.assertGreater(l.max_step_height_m, w.max_step_height_m)
        self.assertLess(l.max_speed_mps, w.max_speed_mps)
        self.assertGreater(l.energy_per_metre, w.energy_per_metre)

    def test_four_limbs_each_with_a_wheel(self):
        self.assertEqual(len(emb.LIMBS), 4)
        for limb in emb.LIMBS:
            self.assertIn("wheel", limb.joints)
            self.assertIn("knee", limb.joints)

    def test_joint_names_include_mast_dofs(self):
        self.assertIn("mast.pan", emb.JOINT_NAMES)
        self.assertIn("mast.tilt", emb.JOINT_NAMES)
        self.assertEqual(len(emb.JOINT_NAMES), 4 * 3 + 2)


class TestJointKinematics(unittest.TestCase):
    def test_wheel_mode_spins_wheels_and_locks_knees(self):
        s = RobotState(pose=Pose(0, 0, 0), mode=MobilityMode.WHEEL)
        update_joint_kinematics(s, 1.0)
        self.assertNotEqual(s.joint_positions["front_left.wheel"], 0.0)
        self.assertEqual(s.joint_positions["front_left.knee"], 0.0)

    def test_leg_mode_cycles_knees_and_stops_wheels(self):
        s = RobotState(pose=Pose(0, 0, 0), mode=MobilityMode.LEG)
        s.distance_travelled_m = 1.0
        update_joint_kinematics(s, 1.0)
        self.assertNotEqual(s.joint_positions["front_left.knee"], 0.0)
        self.assertEqual(s.joint_velocities["front_left.wheel"], 0.0)


if __name__ == "__main__":
    unittest.main()
