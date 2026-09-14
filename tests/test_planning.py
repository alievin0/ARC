"""Planner. The clearance trade-off is proven in BOTH directions: the 1.1 m
narrow passage must stay open and a 0.5 m gap must be refused. A clearance
rule that only ever refuses would be an outage, not a safety margin."""
import math
import unittest

from arc2.memory.episodic import EpisodicMemory
from arc2.planning.action_planner import (ARRIVAL_TOLERANCE_M, MAX_LEG_M,
                                          next_steps, plan_route)
from arc2.planning.path import (astar, choose_frontier, is_occupiable,
                                simplify)
from arc2.planning.task_planner import Phase, Strategy, TaskPlanner
from arc2.types import Pose, Vec2
from arc2.world.belief import OccupancyBelief
from arc2.world.model import WorldModel


def wall_column(bel, cx, y0=0, y1=None):
    for cy in range(y0, y1 if y1 is not None else bel.ny):
        bel.mark_blocked(cx, cy)


class TestAStar(unittest.TestCase):
    def test_plans_optimistically_through_unknown_space(self):
        """This is what makes the first plan a real hypothesis."""
        b = OccupancyBelief(24, 16, 0.25)
        self.assertIsNotNone(astar(b, (4, 4), (60, 40)))

    def test_refuses_when_a_full_wall_separates_start_from_goal(self):
        b = OccupancyBelief(24, 16, 0.25)
        for cx in (40, 41, 42):
            wall_column(b, cx)
        self.assertIsNone(astar(b, (4, 4), (60, 40)))

    def test_finds_the_door_when_one_exists(self):
        b = OccupancyBelief(24, 16, 0.25)
        for cx in (40, 41, 42):
            wall_column(b, cx, 0, 28)
            wall_column(b, cx, 34, b.ny)
        path = astar(b, (4, 4), (60, 40))
        self.assertIsNotNone(path)
        self.assertTrue(any(c[0] in (40, 41, 42) for c in path))

    def test_result_is_deterministic_for_identical_beliefs(self):
        def build():
            b = OccupancyBelief(24, 16, 0.25)
            for cx in (30, 31):
                wall_column(b, cx, 0, 20)
            return b
        self.assertEqual(astar(build(), (4, 4), (60, 40)),
                         astar(build(), (4, 4), (60, 40)))

    def test_simplify_preserves_the_endpoints(self):
        p = astar(OccupancyBelief(24, 16, 0.25), (4, 4), (40, 30))
        s = simplify(p)
        self.assertEqual((s[0], s[-1]), (p[0], p[-1]))
        self.assertLessEqual(len(s), len(p))


class TestClearance(unittest.TestCase):
    """Both halves of the trade-off."""

    def _passage(self, clear_width_m):
        b = OccupancyBelief(24, 16, 0.25)
        left_edge, right_edge = 10.0, 10.0 + clear_width_m
        for cy in range(24, 36):
            for cx in range(int((left_edge - 0.5) / 0.25), int(left_edge / 0.25)):
                b.mark_blocked(cx, cy)
            for cx in range(int(right_edge / 0.25),
                            int((right_edge + 0.5) / 0.25)):
                b.mark_blocked(cx, cy)
        return b, (left_edge + right_edge) / 2.0

    def test_the_narrow_passage_stays_open(self):
        b, mid = self._passage(1.1)
        self.assertTrue(is_occupiable(b, *b.to_cell(mid, 7.5)))
        self.assertIsNotNone(astar(b, b.to_cell(mid, 5.0), b.to_cell(mid, 9.8)))

    def test_a_gap_narrower_than_the_chassis_is_refused(self):
        b, mid = self._passage(0.5)
        self.assertFalse(is_occupiable(b, *b.to_cell(mid, 7.5)))

    def test_a_cell_can_be_empty_yet_not_occupiable(self):
        b = OccupancyBelief(24, 16, 0.25)
        b.mark_blocked(20, 20)
        self.assertIsNot(b.get(21, 20), b.get(20, 20))   # 21 is not BLOCKED
        self.assertFalse(is_occupiable(b, 21, 20))       # but the disc won't fit

    def test_the_planner_can_still_escape_a_grazing_start_pose(self):
        """Otherwise a robot that stops ON contact can never plan its way out."""
        b = OccupancyBelief(24, 16, 0.25)
        for cy in range(0, 40):
            b.mark_blocked(20, cy)
        self.assertFalse(is_occupiable(b, 21, 20))
        self.assertIsNotNone(astar(b, (21, 20), (60, 20)))


class TestFrontiers(unittest.TestCase):
    def test_no_frontier_in_a_wholly_unknown_map(self):
        self.assertIsNone(choose_frontier(OccupancyBelief(24, 16, 0.25), (4, 4)))

    def test_a_frontier_is_chosen_once_free_space_exists(self):
        b = OccupancyBelief(24, 16, 0.25)
        for cx in range(4, 20):
            for cy in range(4, 20):
                b.mark_free(cx, cy)
        self.assertIsNotNone(choose_frontier(b, (10, 10)))

    def test_an_unoccupiable_frontier_is_never_offered(self):
        """A goal the chassis cannot stand in is not a goal."""
        b = OccupancyBelief(24, 16, 0.25)
        for cy in range(4, 20):
            b.mark_blocked(10, cy)
        for cy in range(4, 20):
            b.mark_free(11, cy)
        f = choose_frontier(b, (30, 30))
        if f is not None:
            self.assertTrue(is_occupiable(b, *f))

    def test_penalty_steers_selection_away_from_a_region(self):
        b = OccupancyBelief(24, 16, 0.25)
        for cx in range(4, 40):
            for cy in range(4, 40):
                b.mark_free(cx, cy)
        plain = choose_frontier(b, (20, 20))
        steered = choose_frontier(
            b, (20, 20),
            penalise=lambda wx, wy: 5000.0 if abs(wx - b.to_world(*plain)[0]) < 2
            else 0.0)
        self.assertNotEqual(plain, steered)


class TestActionPlanner(unittest.TestCase):
    def test_turn_is_emitted_when_misaligned(self):
        steps = next_steps(Pose(0, 0, 0.0), Vec2(0, 3))
        self.assertEqual(steps[0].kind, "turn")
        self.assertAlmostEqual(steps[0].value, math.pi / 2, places=5)

    def test_move_is_emitted_when_aligned_and_is_bounded(self):
        steps = next_steps(Pose(0, 0, 0.0), Vec2(30, 0))
        self.assertEqual(steps[0].kind, "move")
        self.assertLessEqual(steps[0].value, MAX_LEG_M)

    def test_no_step_is_emitted_on_arrival(self):
        self.assertEqual(next_steps(Pose(0, 0, 0.0),
                                    Vec2(ARRIVAL_TOLERANCE_M / 2, 0)), [])

    def test_an_unreachable_goal_yields_no_plan_rather_than_a_fake_one(self):
        m = WorldModel(24, 16)
        for cx in range(m.occupancy.nx):
            for cy in range(m.occupancy.ny):
                m.occupancy.mark_blocked(cx, cy)
        self.assertIsNone(plan_route(m, Pose(2, 2, 0), Vec2(20, 14), "x", 0))

    def test_a_plan_is_invalidated_by_a_blockage_found_on_its_route(self):
        m = WorldModel(24, 16)
        for cx in range(m.occupancy.nx):
            for cy in range(m.occupancy.ny):
                m.occupancy.mark_free(cx, cy)
        plan = plan_route(m, Pose(2, 2, 0), Vec2(20, 14), "x", 0)
        self.assertIsNotNone(plan)
        self.assertIsNone(plan.invalidated_by(m))
        for cx, cy in plan.cells:
            m.occupancy.force_blocked(cx, cy)
        self.assertIsNotNone(plan.invalidated_by(m))


class TestTaskPlanner(unittest.TestCase):
    def setUp(self):
        self.tp = TaskPlanner("canister", 1.0)
        self.m = WorldModel(24, 16)
        self.mem = EpisodicMemory()

    def test_starts_by_exploring_because_nothing_is_known(self):
        d = self.tp.decide(self.m, self.mem, Vec2(2, 2), [])
        self.assertIs(d.phase, Phase.SEARCH)
        self.assertIs(d.strategy, Strategy.EXPLORE_FRONTIER)

    def test_a_step_failure_selects_a_mobility_change(self):
        self.tp.on_failure("step_too_high", None, self.m, self.mem, Vec2(19, 6))
        self.assertIs(self.tp.strategy, Strategy.CHANGE_MOBILITY)

    def test_a_wall_collision_selects_a_reroute_not_a_mode_change(self):
        self.tp.on_failure("collision", "wall_x", self.m, self.mem, Vec2(3, 10))
        self.assertIs(self.tp.strategy, Strategy.ALTERNATE_ROUTE)

    def test_a_collision_with_a_SEEN_movable_selects_clearing_it(self):
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 1)
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 2)
        self.tp.on_failure("collision", "crate_01", self.m, self.mem,
                           Vec2(10.7, 6.9))
        self.assertIs(self.tp.strategy, Strategy.CLEAR_OBSTRUCTION)

    def test_an_UNSEEN_contact_id_is_never_assumed_movable(self):
        """Otherwise the collision report leaks ground truth into the plan."""
        self.tp.on_failure("collision", "crate_01", self.m, self.mem,
                           Vec2(10.7, 6.9))
        self.assertIs(self.tp.strategy, Strategy.ALTERNATE_ROUTE)

    def test_repeated_failure_escalates_to_abandoning_the_region(self):
        for _ in range(TaskPlanner.ESCALATE_AFTER):
            self.tp.on_failure("collision", "wall_x", self.m, self.mem, Vec2(3, 10))
        self.assertIs(self.tp.strategy, Strategy.EXPLORE_FRONTIER)
        self.assertTrue(self.mem.is_abandoned(Vec2(3, 10)))

    def test_escalation_is_reachable_even_for_a_movable_contact(self):
        """The bug this guards: the movable branch used to short-circuit the
        escalation, so a wedged crate was re-pushed 728 times."""
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 1)
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 2)
        for _ in range(TaskPlanner.ESCALATE_AFTER):
            self.tp.on_failure("collision", "crate_01", self.m, self.mem,
                               Vec2(10.7, 6.9))
        self.assertIs(self.tp.strategy, Strategy.EXPLORE_FRONTIER)

    def test_a_recovery_outranks_the_phase_default_in_the_search_phase(self):
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 1)
        self.m.observe_object("crate_01", "crate", Vec2(10.7, 7.4), 0.9, 2)
        self.tp.on_failure("collision", "crate_01", self.m, self.mem,
                           Vec2(10.7, 6.9))
        d = self.tp.decide(self.m, self.mem, Vec2(10.7, 6.9), [])
        self.assertIs(d.strategy, Strategy.CLEAR_OBSTRUCTION)

    def test_progress_clears_the_recovery(self):
        self.tp.on_failure("collision", "wall_x", self.m, self.mem, Vec2(3, 10))
        self.tp.on_progress()
        self.assertNotIn(self.tp.strategy, TaskPlanner.RECOVERY)

    def test_phases_advance_only_on_real_progress(self):
        # Home is established by the FIRST pose the model ever sees, exactly
        # as it is in a real episode. Without it "home" defaults to wherever
        # the robot currently stands and the agent is trivially already there.
        self.m.set_pose(Pose(2, 2, 0.0), 1.0)
        self.m.observe_object("t", "canister", Vec2(7.5, 13.2), 0.95, 1)
        self.m.observe_object("t", "canister", Vec2(7.5, 13.2), 0.95, 2)
        self.assertIs(self.tp.decide(self.m, self.mem, Vec2(2, 2), []).phase,
                      Phase.APPROACH)
        self.tp.decide(self.m, self.mem, Vec2(7.5, 12.8), [])
        self.assertIs(self.tp.decide(self.m, self.mem, Vec2(7.5, 12.8),
                                     ["t"]).phase, Phase.RETURN)

    def test_a_failure_while_returning_does_not_undo_the_acquisition(self):
        self.tp.phase = Phase.RETURN
        self.m.set_pose(Pose(2, 2, 0), 1.0)
        self.tp.on_failure("collision", "wall_x", self.m, self.mem, Vec2(9, 9))
        d = self.tp.decide(self.m, self.mem, Vec2(9, 9), ["t"])
        self.assertIs(d.phase, Phase.RETURN)


if __name__ == "__main__":
    unittest.main()
