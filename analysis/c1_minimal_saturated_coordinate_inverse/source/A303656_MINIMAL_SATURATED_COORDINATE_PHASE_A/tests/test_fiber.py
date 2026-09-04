from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from fiber_cover_checker import (
    brute_irredundant_signatures,
    counterexamples,
    dynamic_templates,
    generated_signatures,
    rigid_only_templates,
)


class FiberClassificationTests(unittest.TestCase):
    def test_budget_one_can_leave_center_hole(self) -> None:
        item = counterexamples()["budget_not_cover"]
        self.assertEqual(item["budget"]["text"], "1/1")
        self.assertEqual(item["uncovered_cells"], [0])

    def test_strict_budget_can_still_leave_holes(self) -> None:
        item = counterexamples()["strict_budget_not_cover"]
        self.assertEqual(item["budget"]["text"], "29/27")
        self.assertTrue(item["uncovered_cells"])

    def test_rigid_only_cover_without_beta_pair(self) -> None:
        item = counterexamples()["covered_without_beta_one_pair"]
        self.assertEqual(item["uncovered_cells"], [])
        self.assertTrue(item["row_minimal"])
        self.assertEqual(len(item["rows"]), 3)

    def test_proper_unresolved_center_refinement(self) -> None:
        item = counterexamples()["proper_unresolved_center_refinement"]
        self.assertEqual(item["uncovered_cells"], [])
        self.assertTrue(item["row_minimal"])
        self.assertFalse(item["contains_depth_one_center_row"])

    def test_duplicate_rigid_mass_is_not_union_coverage(self) -> None:
        item = counterexamples()["duplicate_rigid_mass_not_cover"]
        self.assertEqual(item["budget"]["text"], "1/1")
        self.assertEqual(item["uncovered_cells"], [2])
        self.assertFalse(item["row_minimal"])

    def test_admitted_overlap_tail(self) -> None:
        item = counterexamples()["minimal_overlap"]
        self.assertEqual(item["uncovered_cells"], [])
        self.assertTrue(item["row_minimal"])
        self.assertEqual(item["budget"]["text"], "29/27")
        self.assertEqual(item["multiplicity_histogram"], {"1": 25, "2": 2})

    def test_beta_two_symbolic_counts(self) -> None:
        for l in (3, 5):
            self.assertEqual(len(rigid_only_templates(l, 2)), 2**l)
            self.assertEqual(len(dynamic_templates(l, 2, 2, 1, (0,))), 2)
            self.assertEqual(len(dynamic_templates(l, 2, 2, 0, (1,))), 2 ** (l - 1))

    def test_independent_bruteforce_l3_beta2(self) -> None:
        for accepted, m in [((), 0), ((0,), 1), ((0,), 2), ((1,), 2)]:
            self.assertEqual(
                generated_signatures(3, 2, m, accepted),
                brute_irredundant_signatures(3, 2, m, accepted),
            )

    def test_generated_multiplicity_never_exceeds_two(self) -> None:
        records = dynamic_templates(3, 3, 3, 1, (0, 2))
        self.assertTrue(records)
        for record in records:
            self.assertLessEqual(max(map(int, record["multiplicity_histogram"])), 2)
            self.assertEqual(
                record["budget"]["numerator"] == record["budget"]["denominator"],
                not record["overlap_tail_j"],
            )


if __name__ == "__main__":
    unittest.main()
