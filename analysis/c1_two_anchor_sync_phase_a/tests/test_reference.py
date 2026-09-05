"""Small adversarial regressions for the independent reference laboratory."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import reference as r


class RegressionTests(unittest.TestCase):
    def test_01_rectangular_complete_without_same_coordinate(self):
        ans = r.validate(*r.rectangular(3, 5), detailed=True)
        self.assertEqual(ans['complete'], [True, True])
        self.assertFalse(ans['H2'])
        self.assertFalse(ans['H1'])
        self.assertTrue(ans['all_rows_active_at_both_anchors'])
        self.assertTrue(ans['simultaneously_row_irredundant'])
        self.assertEqual(ans['minimal_global_row_covers'],
                         [[['A0', 'A1', 'A2']], [['B0', 'B1', 'B2', 'B3', 'B4']]])

    def test_02_same_coordinate_not_same_lower(self):
        ans = r.validate(*r.nested(3, 5, 0, 2), detailed=True)
        self.assertEqual(ans['complete'], [True, True])
        self.assertTrue(ans['H2'])
        self.assertFalse(ans['H1'])
        self.assertEqual(ans['original_rank_saturation'][0]['1'], [[0]])
        self.assertEqual(ans['original_rank_saturation'][1]['1'], [[2]])

    def test_03_all_three_lower_separations(self):
        diffs = set()
        for a in range(3):
            for b in range(3):
                ans = r.validate(*r.nested(3, 5, a, b))
                self.assertEqual(ans['H1'], a == b)
                diffs.add((a - b) % 3)
        self.assertEqual(diffs, {0, 1, 2})

    def test_04_local_zero_corruption_rejected(self):
        dims, es = r.dynamic_switch()
        e = es[2]
        es[2] = r.Event(e.row, e.anchor, e.rank, e.guard,
                        e.mask | e.zero_mask, e.kind, e.zero_mask)
        with self.assertRaises(AssertionError):
            r.validate(dims, es)

    def test_05_non_coprime_crt(self):
        self.assertEqual(r.crt_pair(0, 22, 0, 155), (0, 3410))
        self.assertEqual(r.crt_pair(1, 4, 3, 6), (9, 12))
        self.assertIsNone(r.crt_pair(0, 4, 1, 6))
        self.assertIsNone(r.meet_guards([((0, 4, 0),), ((0, 2, 1),)]))

    def test_06_mass_saturation_does_not_imply_coverage(self):
        es = [r.Event(f'q{i}', 0, 0, (), 1) for i in range(3)]
        ans = r.validate((3,), es)
        self.assertEqual(ans['covered_cells'][0], 1)
        self.assertEqual(ans['original_rank_saturation'][0]['0'], [])
        self.assertFalse(r.contraction((3,), es, 0)['root_covered'])

    def test_07_actual_first_stop_can_be_split(self):
        ans = r.actual_first_split()
        self.assertEqual(ans['anchor_coverage_sizes'], [66, 1])
        self.assertEqual(ans['pooled_coverage_size'], 67)
        self.assertFalse(ans['complete_certificate'])

    def test_08_unchanged_U15_nonrealizability(self):
        ans = r.arithmetic_nonrealizability()
        self.assertEqual(ans['rigid_resources'], 0)
        self.assertEqual([d['q'] for d in ans['all_possible_admitted_primes']], [11, 31, 71])

    def test_09_two_adic_common_safe_exactly_even(self):
        for rec in r.two_adic_audit():
            self.assertEqual(rec['explicit_even_residue_witnesses'], 2 ** (rec['K'] - 1))
            self.assertTrue(rec['no_common_exactly_odd_r'])

    def test_10_pooled_coverage_is_not_simultaneous_coverage(self):
        dims = (2, 3)
        es = [r.Event('q0', 0, 0, (), 1), r.Event('q0', 1, 0, (), 2)]
        ans = r.validate(dims, es)
        self.assertEqual(ans['complete'], [False, False])
        self.assertTrue(all(any(e.covers(x) for e in es) for x in r.points(dims)))


if __name__ == '__main__':
    unittest.main()
