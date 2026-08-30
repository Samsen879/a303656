from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from contraction import (  # noqa: E402
    Event,
    beta_two_multishell_example,
    branching_pair_example,
    exhaustive_universal_order_check,
    first_density_saturation_without_coverage,
    first_exact_cover_without_beta_one_pair,
    semantic_contraction_trace,
    semantic_eliminate_max,
)


class ContractionReferenceTests(unittest.TestCase):
    def test_density_saturation_is_not_coverage(self) -> None:
        ce = first_density_saturation_without_coverage()
        self.assertEqual(ce["coordinate_size"], 3)
        self.assertEqual(ce["budget"], [1, 1])
        self.assertEqual(len(ce["uncovered_digits"]), 1)

    def test_exact_cover_without_beta_one_pair(self) -> None:
        ce = first_exact_cover_without_beta_one_pair()
        self.assertEqual(ce["coordinate_size"], 3)
        self.assertIsNone(ce["dynamic_center"])
        self.assertEqual(ce["rigid_digits"], [0, 1, 2])

    def test_beta_two_requires_multiple_rigid_singletons(self) -> None:
        ex = beta_two_multishell_example()
        self.assertTrue(ex["covered"])
        self.assertEqual(ex["rigid_count"], 3)
        self.assertFalse(ex["single_rigid_closes_center"])

    def test_semantic_contraction_soundness(self) -> None:
        moduli, events, _ = branching_pair_example()
        trace = semantic_contraction_trace(moduli, events)
        self.assertTrue(trace["initial_complete"])
        self.assertTrue(trace["root_covered"])
        self.assertTrue(trace["sound_and_complete"])
        self.assertEqual(trace["depth"], 2)

    def test_branch_local_reuse_and_naive_nonconfluence(self) -> None:
        _, _, data = branching_pair_example()
        self.assertTrue(data["original_complete"])
        self.assertEqual(data["branch_local_residual"], [0, 1])
        self.assertNotEqual(
            data["naive_global_consume_R0_then_R1"],
            data["naive_global_consume_R1_then_R0"],
        )
        self.assertTrue(data["both_naive_results_incomplete"])

    def test_semantic_residual_need_not_be_single_admitted_shape(self) -> None:
        events = [
            Event(f"r{y}{z}", 1, frozenset({(y, z)}), "rigid")
            for y in (0, 2)
            for z in range(3)
        ]
        lower_moduli, next_events, trace = semantic_eliminate_max([5, 3], events)
        self.assertEqual(lower_moduli, [5])
        macro = next(e for e in next_events if e.kind == "semantic_macro")
        self.assertEqual(macro.prefixes, frozenset({(0,), (2,)}))
        self.assertTrue(trace["identity_verified"])

    def test_universal_projection_order_invariance_exhaustive(self) -> None:
        result = exhaustive_universal_order_check([2, 3, 2], keep=0)
        self.assertTrue(result["PASS"])
        self.assertEqual(result["subsets_checked"], 4096)

    def test_chain_normal_form_tree(self) -> None:
        events = [
            Event("p=11", 0, frozenset((x,) for x in range(1, 11)), "dynamic"),
            Event("p=67", 1, frozenset((0, y) for y in range(1, 67)), "dynamic"),
            Event("p=20771", 1, frozenset({(0, 0)}), "rigid"),
        ]
        trace = semantic_contraction_trace([11, 67], events)
        self.assertTrue(trace["root_covered"])
        self.assertEqual(trace["levels"][0]["saturated_fiber_count"], 1)
        self.assertEqual(trace["levels"][1]["saturated_fiber_count"], 1)


if __name__ == "__main__":
    unittest.main()
