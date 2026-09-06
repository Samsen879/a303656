"""Regression tests; all arithmetic universality claims still depend on the written proofs."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import reference as r


class ReferenceTests(unittest.TestCase):
    def test_exact_center_hole(self):
        self.assertFalse(r.centered_full(3, 3, 0, (0, 2), (), []))
        self.assertTrue(r.centered_full(3, 3, 0, (0, 2), (), [r.Cylinder(1, 0)]))

    def test_position_translation(self):
        for p, beta in ((3, 2), (5, 2)):
            full = (1 << p**beta) - 1
            for center in range(p**beta):
                for J in r.allowed_shell_sets(beta):
                    cs = [r.Cylinder(2, center), r.Cylinder(1, center + 1)]
                    mask = r.shell_mask(p, beta, center, J)
                    for c in cs:
                        mask |= r.cylinder_mask(p, beta, c)
                    self.assertEqual(r.centered_full(p, beta, center, J, (), cs), mask == full)

    def test_parity_flexible_boundary(self):
        self.assertEqual(r.boundary_audit(6)['mismatches'], 0)

    def test_helper_inventories(self):
        out = r.descended_resource_audit()
        self.assertEqual(out['shallow_three_union_upper_bound'], '8/9')

    def test_full_tree_depth_tax(self):
        for p in (3, 5, 7):
            for leaves in range(1, 10):
                for v in r.frontier_profiles(p, leaves, 5):
                    deepest = max(i for i, n in enumerate(v) if n)
                    self.assertGreaterEqual(sum(v), 1 + (p - 1)*deepest)
                    self.assertEqual(sum(Fraction(n, p**d) for d, n in enumerate(v)), 1)

    def test_linear_origin_preservation(self):
        seeds = [r.Seed('qA', ((3, 1, 1), (7, 1, 0))),
                 r.Seed('qB', ((7, 1, 1),))]
        ds = [r.Dynamic(7, ((2, 1, 0), (3, 1, 1)), 0, 1, (0,))]
        out, _ = r.linear_step(7, seeds, ds)
        self.assertEqual([s.origin for s in out], ['qA'])
        self.assertEqual(out[0].lineage, (7,))
        self.assertIn((3, 1, 1), out[0].guard)

    def test_incompatible_lower_guard_dies(self):
        seeds = [r.Seed('qA', ((3, 1, 0), (7, 1, 0)))]
        ds = [r.Dynamic(7, ((3, 1, 1),), 0, 1, (0,))]
        out, _ = r.linear_step(7, seeds, ds)
        self.assertEqual(out, [])

    def test_abstract_core_extraction(self):
        ss = [r.Seed('abstract'+str(a), ((3, 1, a),)) for a in range(3)]
        out = r.core_extract({3: 1}, ss, [])
        self.assertEqual((out['rank'], out['rigid_count']), (3, 3))

    def test_local_zero_rejected(self):
        _, dom, events, _ = r.normal_events_K2([67, 20771], {67: 2, 20771: 20775})
        zero = {p: 0 for p in dom}
        self.assertFalse(any(e.origin == 67 and r.event_fatal(e, zero) for e in events))
        self.assertTrue(any(e.origin == 20771 and e.anchor == 1 and r.event_fatal(e, zero) for e in events))

    def test_actual_split_does_not_stop_one_anchor_escape(self):
        _, dom, events, _ = r.normal_events_K2([67, 20771], {67: 2, 20771: 20775})
        prefix = {p: 0 for p in dom if p != 67}
        self.assertIsNotNone(r.ascending_game(dom, events, forced_prefix=prefix)['witness'])
        self.assertIsNone(r.ascending_game(dom, events, forced_prefix=prefix, common_only=True)['witness'])

    def test_temporal_and_configuration_gap(self):
        out = r.dual_and_temporal_audit()
        self.assertEqual(out['mixed_anchor_blocker_regression']['result']['coords'][7], 1)
        self.assertEqual(out['configuration_gap']['integral_covers'], 0)

    def test_invalid_blocker_rejected(self):
        _, dom, events, _ = r.normal_events_K2([67, 20771], {67: 2, 20771: 20775})
        with self.assertRaises(ValueError):
            r.blocker_greedy(dom, events, {20771: 2})

    def test_ancestor_accounting(self):
        C = r.Cylinder(1, 0)
        B = r.Cylinder(2, 0)
        self.assertEqual(r.intersection_measure(3, B, [C]), Fraction(1, 9))

    def test_resultant_known_values(self):
        self.assertEqual(abs(r.resultant(3, 0)), 2**3*7*13)
        self.assertEqual(abs(r.resultant(5, 0)), 2**5*11**3*31*41)

    def test_resultant_nonzero_Y_exact(self):
        for Y in (1, 2):
            A = 5**(3*Y)
            self.assertEqual(r.resultant(3, Y), -216*A*A - 512)


if __name__ == '__main__':
    unittest.main()
