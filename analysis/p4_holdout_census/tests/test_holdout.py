#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "analysis/p4_holdout_census/tools"
sys.path.insert(0, str(TOOLS))

from holdout_common import (  # noqa: E402
    A, B, L, N0, canonical_pairs, coverage_mask, evenly_spaced_indices,
    load_candidates, load_prior_t_points, tuple_class_residue, verify_protected,
)


class HoldoutSourceTests(unittest.TestCase):
    def test_corrected_manifest_is_exact_extension(self) -> None:
        with (ROOT / "analysis/p4_weighted_transferability/results/candidate_manifest.json").open(encoding="utf-8") as stream:
            old = json.load(stream)
        with (ROOT / "analysis/p4_weighted_transferability/results/candidate_manifest_holdout_v2.json").open(encoding="utf-8") as stream:
            new = json.load(stream)
        with (ROOT / "analysis/p4_weighted_transferability/results/weighted_maxima.json").open(encoding="utf-8") as stream:
            maxima = json.load(stream)
        self.assertEqual(new["candidates"][:12], old["candidates"])
        self.assertEqual(len(new["candidates"]), 13)
        self.assertEqual(len({item["coverage_mask_hex"] for item in new["candidates"]}), 13)
        optimum = maxima["maxima"]["t3eq2"]["pool"]
        self.assertEqual(new["candidates"][12]["coverage_mask_hex"], optimum["coverage_mask_hex"])
        self.assertEqual(new["candidates"][12]["lexicographically_first_t3eq2_representative"], [2, 13, 32, 13])
        self.assertEqual(new["candidates"][12]["G"], 222)

    def test_candidate_contract_and_representatives(self) -> None:
        candidates = load_candidates(ROOT)
        self.assertEqual(len(candidates), 13)
        pairs = canonical_pairs(ROOT)
        for candidate in candidates:
            representative = candidate["lexicographically_first_t3eq2_representative"]
            if representative is not None:
                self.assertEqual(coverage_mask(tuple(representative), pairs), candidate["coverage_mask_int"])

    def test_duplicate_shift_is_two_pairs(self) -> None:
        pairs = canonical_pairs(ROOT)
        self.assertEqual([(pair["c"], pair["d"]) for pair in pairs if pair["shift"] == 28], [(1, 2), (3, 0)])

    def test_crt_and_even_spacing_boundaries(self) -> None:
        residue = tuple_class_residue((2, 13, 32, 13))
        self.assertEqual(residue % 40, N0 % 40)
        self.assertTrue(0 <= residue < L)
        for count in (3, 5, 17, 140):
            for r in range(3, min(5, count) + 1):
                indices = evenly_spaced_indices(count, r)
                self.assertEqual(indices[0], 0)
                self.assertEqual(indices[-1], count - 1)
                self.assertEqual(len(indices), len(set(indices)))

    def test_prior_panels_and_protected_hashes(self) -> None:
        verify_protected(ROOT)
        points, classes, metadata = load_prior_t_points(ROOT)
        self.assertEqual(metadata["distinct_prior_T_integer_count"], len(points))
        self.assertEqual(metadata["distinct_excluded_CRT_class_count"], len(classes))
        self.assertGreater(len(points), 300000)


if __name__ == "__main__":
    unittest.main()
