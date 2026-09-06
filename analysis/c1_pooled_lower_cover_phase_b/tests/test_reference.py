"""Adversarial regressions. Run: python3 -m unittest discover -s tests -v"""
from pathlib import Path
import copy
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import reference as r


class ReferenceTests(unittest.TestCase):
    def test_01_local_zero_is_never_fatal(self):
        self.assertFalse(r.accept(0, 3, 3, frozenset({1, 3})))
        self.assertTrue(r.accept(3, 3, 3, frozenset({1})))
        self.assertFalse(r.accept(9, 3, 3, frozenset({1})))

    def test_02_six_demands_exhaustive(self):
        self.assertEqual(r.audit_demands()["truth_evaluations"], 8160)

    def test_03_either_does_not_become_fixed_anchor(self):
        word = (1, 2, 1)
        self.assertEqual(r.residual_demand(r.DEMANDS["EITHER"], word), r.DEMANDS["TRUE"])
        self.assertEqual(r.residual_demand(r.DEMANDS["A0"], word), r.DEMANDS["A0"])
        self.assertEqual(r.residual_demand(r.DEMANDS["A1"], word), r.DEMANDS["A1"])
        self.assertEqual(r.residual_demand(r.DEMANDS["BOTH"], word), r.DEMANDS["BOTH"])

    def test_04_non_coprime_crt(self):
        self.assertEqual(r.crt_pair(1, 6, 3, 8), (19, 24))
        self.assertIsNone(r.crt_pair(1, 6, 2, 8))
        self.assertEqual(r.crt_pair(0, 22, 0, 155), (0, 3410))

    def test_05_global_state_conflict_rejected(self):
        self.assertIsNone(r.join_tokens(frozenset({(7, 0)}), frozenset({(7, 1)})))

    def test_06_branch_local_reuse_not_a_new_prime(self):
        s = frozenset({(7, 0)})
        self.assertEqual(r.join_tokens(s, s, s), s)

    def test_07_positive_both_root_fixture(self):
        # Source #14's abstract 2x2 three-row pattern, frozen one state per row.
        data = [(0, 0, (1, 3)), (0, 1, (2, 3)),
                (1, 0, (2, 1)), (1, 1, (1, 1)),
                (2, 0, (2, 2)), (2, 1, (1, 2))]
        atoms = [(c, r.Clause(m, frozenset({(q, 0)}), (f"{q}:{c}",))) for q, c, m in data]
        for c in (0, 1):
            root = r.root_clauses([a for cc, a in atoms if cc == c], (2, 2))
            self.assertTrue(root)
        self.assertTrue(r.root_clauses([a for _, a in atoms], (2, 2)))

    def test_08_actual_split_not_joint_full(self):
        obj = r.actual_split()
        self.assertEqual(obj["safe_counts"], [218219, 218218])
        self.assertEqual(obj["E0"], [0])
        self.assertEqual(len(obj["E1"]), 66)

    def test_09_two_cylinders_can_share_one_actual_prime(self):
        cases = r.paired_rigid_examples()["cases"]
        self.assertEqual(cases[1]["top_positions"], [50, 547])
        self.assertEqual(cases[1]["lower_classes"], [0, 0])

    def test_10_independent_lucas_certificate_verification(self):
        self.assertEqual(r.audit_cyclotomic()["primality_nodes_verified"], 44)

    def test_11_corrupt_factor_certificate_rejected(self):
        data = json.loads((r.ROOT / "results/primality_certificates.json").read_text())
        corrupt = copy.deepcopy(data)
        corrupt["certificates"]["4861"]["base"] = 1
        with self.assertRaises(AssertionError):
            r.verify_lucas_certificates(corrupt)

    def test_12_sparse_subclass_not_prime_cutoff(self):
        result = r.audit_sparse_subclass()
        self.assertEqual(result["budget_3"], "89/108")
        self.assertEqual(result["slack_3"], "19/108")

    def test_13_full_depth_is_not_first_digit(self):
        # A full-depth forbidden point does not forbid its entire first branch.
        from fractions import Fraction
        self.assertLess(Fraction(3, 4) + Fraction(2, 27), 1)
        self.assertGreater(Fraction(3, 4) + Fraction(2, 3), 1)

    def test_14_ancestor_sensitive_prefix_frontier(self):
        result = r.prefix_maximal([(1, 0), (2, 0), (2, 3), (2, 6)], 3, 2)
        self.assertEqual(result, [(1, 0)])

    def test_15_boundary_and_seed_scope(self):
        result = r.audit_boundary_and_skeleton()
        self.assertTrue(result["boundary_counterexample"]["pooled_complete"])
        self.assertFalse(result["s1_boundary_example"]["both_complete"])
        self.assertEqual(result["regular_skeleton"]["common_escapes"], [0, 651])
        self.assertIsNone(result["regular_skeleton"]["terminal_nonregular_seed"])

    def test_16_configuration_fractional_is_not_integral(self):
        obj = r.audit_false_potentials()
        self.assertEqual(obj["configuration_integrality"]["complete_assignments"], 0)
        self.assertTrue(obj["configuration_integrality"]["fractional_half_each_option_feasible"])

    def test_17_anchor_specific_mixed_row_classification(self):
        obj = r.audit_mixed_row()
        self.assertEqual(obj["anchor0_type"], "dynamic")
        self.assertEqual(obj["anchor1_type"], "rigid, valuation 1")
        self.assertNotEqual(obj["anchor0_guard"], obj["anchor1_guard"])


if __name__ == "__main__":
    unittest.main()
