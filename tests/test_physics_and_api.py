"""Physics and the RobotAPI contract.

The five-case discipline is applied to every gate: a VALID input must PASS,
malformed input must fail, the wrong mode must fail, the wrong target must
fail, and the effect must be readable back. A wall of refusals proves nothing.
"""
import math
import unittest

from arc2.control.api import ActionResult, RobotAPI
from arc2.control.hardware_backend import HardwareNotAvailable, HardwareRobotAPI
from arc2.control.sim_backend import SimulatedRobotAPI
from arc2.sensors.suite import SensorSuite
from arc2.simulation import physics
from arc2.simulation.simulator import SimConfig, Simulator
from arc2.simulation.world_spec import CRATE_ID, TARGET_ID, build_world
from arc2.types import ActionStatus, MobilityMode, Pose, Vec2


def fresh(seed=1):
    sim = Simulator(SimConfig(seed=seed))
    return sim, SimulatedRobotAPI(sim, SensorSuite())


class TestMovementHonesty(unittest.TestCase):
    def test_open_move_succeeds_fully(self):
        """MUST-PASS: the door still opens."""
        sim, api = fresh()
        # (3.5, 3.5) heading east is verified-clear floor: the nearest
        # obstacle, pillar_0, spans x in [6.4, 7.6].
        sim.state.pose = Pose(3.5, 3.5, 0.0, 0.0)
        r = api.move(1.0)
        self.assertIs(r.status, ActionStatus.SUCCESS)
        self.assertAlmostEqual(r.achieved, 1.0, places=6)

    def test_move_into_wall_reports_actual_distance_not_commanded(self):
        sim, api = fresh()
        r = api.move(6.0)                       # start faces the divider wall
        self.assertIn(r.status, (ActionStatus.BLOCKED, ActionStatus.PARTIAL))
        self.assertLess(r.achieved, r.commanded)
        self.assertEqual(r.reason, physics.StopReason.COLLISION)
        self.assertIsNotNone(r.contact_id)

    def test_zero_progress_move_is_blocked_not_success(self):
        sim, api = fresh()
        api.move(6.0)                            # drive up against the wall
        r = api.move(1.0)                        # and again from contact
        self.assertIs(r.status, ActionStatus.BLOCKED)
        self.assertAlmostEqual(r.achieved, 0.0, places=6)

    def test_negative_distance_is_invalid(self):
        _, api = fresh()
        self.assertIs(api.move(-1.0).status, ActionStatus.INVALID)

    def test_motion_cannot_tunnel_through_a_wall(self):
        sim, api = fresh()
        before = sim.state.pose.y
        api.move(50.0)
        self.assertLess(sim.state.pose.y, 5.5)   # never past the divider
        self.assertGreater(sim.state.pose.y, before)


class TestStaircaseGate(unittest.TestCase):
    """The gate must REFUSE in wheel mode and ADMIT in leg mode."""

    def _at_stairs(self, seed=1):
        sim, api = fresh(seed)
        sim.state.pose = Pose(19.0, 5.9, math.pi / 2, 0.0)
        return sim, api

    def test_wheel_mode_cannot_climb(self):
        sim, api = self._at_stairs()
        r = api.move(2.0)
        self.assertIn(r.status, (ActionStatus.BLOCKED, ActionStatus.PARTIAL))
        self.assertEqual(r.reason, physics.StopReason.STEP_TOO_HIGH)

    def test_leg_mode_can_climb(self):
        sim, api = self._at_stairs()
        api.change_mobility_mode(MobilityMode.LEG)
        r = api.move(2.0)
        self.assertIs(r.status, ActionStatus.SUCCESS)
        self.assertAlmostEqual(r.achieved, 2.0, places=6)
        self.assertGreater(sim.state.pose.z, 0.0)   # actually ascended

    def test_mode_change_costs_time_and_is_idempotent(self):
        sim, api = fresh()
        t0 = sim.state.elapsed_s
        self.assertIs(api.change_mobility_mode(MobilityMode.LEG).status,
                      ActionStatus.SUCCESS)
        self.assertGreater(sim.state.elapsed_s - t0, 1.0)
        again = api.change_mobility_mode(MobilityMode.LEG)
        self.assertIs(again.status, ActionStatus.PARTIAL)
        self.assertEqual(again.reason, "already_in_mode")


class TestPush(unittest.TestCase):
    def _at_crate(self, seed=1):
        sim, api = fresh(seed)
        sim.state.pose = Pose(10.75, 6.6, math.pi / 2, 0.0)
        return sim, api

    def test_push_displaces_the_crate(self):
        sim, api = self._at_crate()
        y0 = next(m for m in sim.spec.movables if m.oid == CRATE_ID).position.y
        r = api.push(1.2)
        y1 = next(m for m in sim.spec.movables if m.oid == CRATE_ID).position.y
        self.assertTrue(r.progressed)
        self.assertGreater(y1, y0)
        self.assertIn(CRATE_ID, r.detail["displaced"])

    def test_plain_move_does_NOT_displace_the_crate(self):
        sim, api = self._at_crate()
        y0 = next(m for m in sim.spec.movables if m.oid == CRATE_ID).position.y
        r = api.move(1.2)
        y1 = next(m for m in sim.spec.movables if m.oid == CRATE_ID).position.y
        self.assertEqual(y0, y1)
        self.assertEqual(r.contact_id, CRATE_ID)

    def test_push_against_a_wall_is_blocked_and_moves_nothing(self):
        sim, api = fresh()
        r = api.push(6.0)                        # wall, not a crate
        self.assertIn(r.status, (ActionStatus.BLOCKED, ActionStatus.PARTIAL))
        self.assertEqual(r.detail["displaced"], [])

    def test_underpowered_push_leaves_the_object_where_it_was(self):
        spec = build_world()
        crate = spec.movables[0]
        y0 = crate.position.y
        out = physics.attempt_move(spec, Pose(10.75, 6.6, math.pi / 2, 0.0),
                                   MobilityMode.WHEEL, 1.2,
                                   allow_push=True, push_strength=0.4)
        self.assertEqual(out.stop_reason, physics.StopReason.PUSHED_OBJECT_STUCK)
        self.assertEqual(crate.position.y, y0)

    def test_non_positive_push_is_invalid(self):
        _, api = fresh()
        self.assertIs(api.push(0.0).status, ActionStatus.INVALID)


class TestInteract(unittest.TestCase):
    def test_pick_up_in_reach_succeeds_and_is_readable_back(self):
        sim, api = fresh()
        sim.state.pose = Pose(7.5, 12.8, math.pi / 2, 0.0)
        r = api.interact("pick_up", TARGET_ID)
        self.assertIs(r.status, ActionStatus.SUCCESS)
        self.assertIn(TARGET_ID, api.get_robot_state()["carrying"])   # round trip

    def test_pick_up_out_of_reach_is_blocked(self):
        _, api = fresh()
        r = api.interact("pick_up", TARGET_ID)
        self.assertIs(r.status, ActionStatus.BLOCKED)
        self.assertEqual(r.reason, "out_of_reach")

    def test_pick_up_of_a_nonexistent_object_fails(self):
        sim, api = fresh()
        sim.state.pose = Pose(7.5, 12.8, math.pi / 2, 0.0)
        self.assertIs(api.interact("pick_up", "no_such_thing").status,
                      ActionStatus.BLOCKED)

    def test_place_without_carrying_anything_fails(self):
        _, api = fresh()
        self.assertIs(api.interact("place", TARGET_ID).status, ActionStatus.FAILED)

    def test_unknown_verb_is_invalid(self):
        _, api = fresh()
        self.assertIs(api.interact("teleport", TARGET_ID).status,
                      ActionStatus.INVALID)


class TestLookAndStop(unittest.TestCase):
    def test_in_range_aim_succeeds(self):
        _, api = fresh()
        r = api.look(0.5, 0.1)
        self.assertIs(r.status, ActionStatus.SUCCESS)

    def test_out_of_range_aim_is_reported_as_clamped_not_silently_accepted(self):
        _, api = fresh()
        r = api.look(99.0)
        self.assertIs(r.status, ActionStatus.PARTIAL)
        self.assertEqual(r.reason, "clamped_to_limits")

    def test_stop_always_succeeds(self):
        _, api = fresh()
        self.assertIs(api.stop().status, ActionStatus.SUCCESS)


class TestApiSurface(unittest.TestCase):
    def test_simulated_backend_implements_the_whole_interface(self):
        _, api = fresh()
        for name in ("observe", "get_robot_state", "move", "turn", "stop",
                     "change_mobility_mode", "look", "push", "interact",
                     "capabilities"):
            self.assertTrue(callable(getattr(api, name)), name)

    def test_robot_state_does_not_leak_ground_truth_position(self):
        """get_robot_state is PROPRIOCEPTIVE. x/y must not appear."""
        _, api = fresh()
        st = api.get_robot_state()
        self.assertNotIn("x", st)
        self.assertNotIn("y", st)
        self.assertNotIn("pose", st)

    def test_hardware_backend_refuses_rather_than_pretending(self):
        hw = HardwareRobotAPI()
        self.assertIsInstance(hw, RobotAPI)
        for call in (hw.observe, hw.get_robot_state, hw.stop, hw.capabilities):
            with self.assertRaises(HardwareNotAvailable):
                call()


if __name__ == "__main__":
    unittest.main()
