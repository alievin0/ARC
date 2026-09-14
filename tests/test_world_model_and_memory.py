"""Belief store and episodic memory."""
import math
import unittest

from arc2.control.api import ActionResult
from arc2.memory.episodic import EpisodicMemory, failure_key
from arc2.types import ActionStatus, Pose, Vec2
from arc2.world.belief import CellState, OccupancyBelief
from arc2.world.model import Knowledge, WorldModel


class TestTriState(unittest.TestCase):
    def setUp(self):
        self.b = OccupancyBelief(24, 16, 0.25)

    def test_everything_starts_unknown(self):
        counts = self.b.counts()
        self.assertEqual(counts[CellState.UNKNOWN.value], self.b.nx * self.b.ny)
        self.assertEqual(counts[CellState.FREE.value], 0)

    def test_first_observation_is_new_information_and_a_repeat_is_not(self):
        self.assertTrue(self.b.mark_free(10, 10))
        self.assertFalse(self.b.mark_free(10, 10))

    def test_conflicting_returns_produce_uncertain_not_last_writer_wins(self):
        self.b.mark_free(4, 4)
        self.b.mark_blocked(4, 4)
        self.assertIs(self.b.get(4, 4), CellState.UNCERTAIN)

    def test_consistent_returns_resolve_to_a_definite_state(self):
        for _ in range(3):
            self.b.mark_blocked(5, 5)
        self.assertIs(self.b.get(5, 5), CellState.BLOCKED)
        for _ in range(4):
            self.b.mark_free(6, 6)
        self.assertIs(self.b.get(6, 6), CellState.FREE)

    def test_a_failed_action_overrides_range_returns(self):
        for _ in range(5):
            self.b.mark_free(7, 7)
        self.assertIs(self.b.get(7, 7), CellState.FREE)
        self.b.force_blocked(7, 7)
        self.assertIs(self.b.get(7, 7), CellState.BLOCKED)

    def test_outside_the_arena_is_solid_by_definition(self):
        self.assertIs(self.b.get(-1, 0), CellState.BLOCKED)
        self.assertIs(self.b.get(self.b.nx, 0), CellState.BLOCKED)

    def test_frontiers_are_free_cells_adjacent_to_unknown(self):
        self.assertEqual(self.b.frontier_cells(), [])
        self.b.mark_free(20, 20)
        self.assertIn((20, 20), self.b.frontier_cells())

    def test_cell_and_world_coordinates_round_trip(self):
        cx, cy = self.b.to_cell(7.3, 11.9)
        wx, wy = self.b.to_world(cx, cy)
        self.assertLess(abs(wx - 7.3), self.b.resolution)
        self.assertLess(abs(wy - 11.9), self.b.resolution)


class TestWorldModel(unittest.TestCase):
    def setUp(self):
        self.m = WorldModel(24, 16)

    def test_home_is_recorded_from_the_first_pose_and_never_moves(self):
        self.m.set_pose(Pose(2, 2, 0), 1.0)
        self.m.set_pose(Pose(9, 9, 0), 1.0)
        self.assertEqual(self.m.home.as_tuple(), (2.0, 2.0))

    def test_unobserved_space_reports_unknown(self):
        self.assertIs(self.m.knowledge_of(20, 14), Knowledge.UNKNOWN)

    def test_collision_marks_the_chassis_width_not_a_point(self):
        marked = self.m.mark_blocked_ahead(Vec2(5, 5), 0.0, 0.55)
        self.assertGreaterEqual(marked, 2)
        self.assertIs(self.m.occupancy.at(5.55, 5.0), CellState.BLOCKED)

    def test_a_confident_second_sighting_promotes_an_uncertain_belief(self):
        self.m.observe_object("o", "unknown_object", Vec2(4, 4), 0.3, 1)
        self.assertIs(self.m.objects["o"].knowledge, Knowledge.UNCERTAIN)
        self.m.observe_object("o", "crate", Vec2(4.1, 4.0), 0.9, 3)
        self.assertIs(self.m.objects["o"].knowledge, Knowledge.KNOWN)

    def test_failures_and_successes_are_both_recorded(self):
        self.m.record_failure("collision", Vec2(1, 1), 0.0, 5, "wall")
        self.m.record_success("move", Vec2(2, 2), 6)
        self.assertEqual(len(self.m.failures), 1)
        self.assertEqual(len(self.m.successes), 1)
        self.assertEqual(self.m.summary()["failures"], 1)


class TestEpisodicMemory(unittest.TestCase):
    def setUp(self):
        self.mem = EpisodicMemory()
        self.here = Pose(2, 2, 1.57)

    def _blocked(self):
        return ActionResult("move", ActionStatus.BLOCKED, 2.0, 0.0, "collision")

    def _ok(self):
        return ActionResult("move", ActionStatus.SUCCESS, 1.0, 1.0, "reached")

    def test_failure_is_remembered_at_that_place_and_heading(self):
        self.mem.record(1, self._blocked(), self.here)
        self.assertTrue(self.mem.has_failed("move", self.here))

    def test_failure_does_not_generalise_to_elsewhere(self):
        self.mem.record(1, self._blocked(), self.here)
        self.assertFalse(self.mem.has_failed("move", Pose(20, 14, 0.0)))

    def test_failure_does_not_generalise_to_the_opposite_heading(self):
        self.mem.record(1, self._blocked(), self.here)
        self.assertFalse(self.mem.has_failed("move", Pose(2, 2, -1.57)))

    def test_first_failure_is_informative_repeats_are_not(self):
        self.mem.record(1, self._blocked(), self.here)
        self.assertEqual(self.mem.unnecessary_actions(), 0,
                         "discovering a blockage is information, not waste")
        self.mem.record(2, self._blocked(), self.here)
        self.assertEqual(self.mem.unnecessary_actions(), 1)

    def test_successful_actions_are_never_unnecessary(self):
        for i in range(3):
            self.mem.record(i, self._ok(), self.here, info_gain=5)
        self.assertEqual(self.mem.unnecessary_actions(), 0)
        self.assertEqual(self.mem.failed_actions, 0)
        self.assertEqual(self.mem.total_actions, 3)

    def test_abandoned_regions_are_local_not_global(self):
        self.mem.abandon_region(Vec2(5, 5), "dead end")
        self.assertTrue(self.mem.is_abandoned(Vec2(5.5, 5.5)))
        self.assertFalse(self.mem.is_abandoned(Vec2(18, 12)))


if __name__ == "__main__":
    unittest.main()
