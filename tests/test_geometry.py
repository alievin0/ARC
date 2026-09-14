"""Geometry primitives. Everything else trusts these, so they are tested
in both directions: the hit cases AND the miss cases."""
import math
import unittest

from arc2.simulation.geometry import (AABB, circle_intersects_aabb,
                                      penetration_depth, ray_aabb, raycast,
                                      segment_blocked)
from arc2.types import Vec2


class TestAABB(unittest.TestCase):
    def test_degenerate_box_rejected(self):
        with self.assertRaises(ValueError):
            AABB(1, 1, 1, 2)
        with self.assertRaises(ValueError):
            AABB(1, 1, 2, 1)

    def test_centered_and_dimensions(self):
        b = AABB.centered(5, 5, 2, 4)
        self.assertEqual((b.x0, b.y0, b.x1, b.y1), (4, 3, 6, 7))
        self.assertEqual((b.width, b.height), (2, 4))
        self.assertEqual(b.center.as_tuple(), (5.0, 5.0))


class TestCircleBox(unittest.TestCase):
    def setUp(self):
        self.b = AABB(1, 1, 2, 2)

    def test_overlapping_disc_detected(self):
        self.assertTrue(circle_intersects_aabb(Vec2(1.5, 1.5), 0.1, self.b))
        self.assertTrue(circle_intersects_aabb(Vec2(0.6, 1.5), 0.5, self.b))

    def test_clear_disc_not_detected(self):
        # MUST-PASS direction: a guard that refuses everything is not a guard.
        self.assertFalse(circle_intersects_aabb(Vec2(0.4, 1.5), 0.5, self.b))
        self.assertFalse(circle_intersects_aabb(Vec2(5, 5), 1.0, self.b))

    def test_penetration_depth_zero_when_clear(self):
        self.assertEqual(penetration_depth(Vec2(0.0, 1.5), 0.5, self.b), 0.0)
        self.assertAlmostEqual(
            penetration_depth(Vec2(0.6, 1.5), 0.5, self.b), 0.1, places=6)


class TestRaycast(unittest.TestCase):
    def setUp(self):
        self.b = AABB(1, 1, 2, 2)

    def test_direct_hit_distance(self):
        d, oid = raycast(Vec2(0, 1.5), 0.0, [("w", self.b)], 10.0)
        self.assertAlmostEqual(d, 1.0, places=9)
        self.assertEqual(oid, "w")

    def test_miss_returns_max_range_and_no_id(self):
        d, oid = raycast(Vec2(0, 5.0), 0.0, [("w", self.b)], 10.0)
        self.assertEqual(d, 10.0)
        self.assertIsNone(oid)

    def test_nearest_hit_occludes_further_one(self):
        far = AABB(3, 1, 4, 2)
        d, oid = raycast(Vec2(0, 1.5), 0.0,
                         [("far", far), ("near", self.b)], 10.0)
        self.assertEqual(oid, "near")
        self.assertAlmostEqual(d, 1.0, places=9)

    def test_hit_beyond_max_range_is_not_reported(self):
        d, oid = raycast(Vec2(0, 1.5), 0.0, [("w", self.b)], 0.5)
        self.assertEqual(d, 0.5)
        self.assertIsNone(oid)

    def test_axis_parallel_ray_outside_slab(self):
        self.assertIsNone(ray_aabb(Vec2(0, 5), 1.0, 0.0, self.b, 10.0))

    def test_segment_blocked_both_ways(self):
        self.assertTrue(segment_blocked(Vec2(0, 1.5), Vec2(3, 1.5),
                                        [("w", self.b)]))
        self.assertFalse(segment_blocked(Vec2(0, 5.0), Vec2(3, 5.0),
                                         [("w", self.b)]))


if __name__ == "__main__":
    unittest.main()
