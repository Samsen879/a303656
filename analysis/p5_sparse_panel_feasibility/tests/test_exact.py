#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "analysis/p5_sparse_panel_feasibility/tools"))

from common import (  # noqa: E402
    CELL_HIGH, CELL_LOW, build_class, class_member, evenly_spaced_indices,
    load_pairs, merge_intervals,
)


class ExactContractTests(unittest.TestCase):
    def test_interval_normalization(self):
        self.assertEqual(merge_intervals([(5, 8), (1, 2), (3, 4), (10, 12), (11, 15)]), [[1, 8], [10, 15]])

    def test_even_spacing(self):
        self.assertEqual(evenly_spaced_indices(9, 5), [0, 2, 4, 6, 8])
        self.assertEqual(evenly_spaced_indices(5, 1), [0])

    def test_crt_congruences_and_cell_bound(self):
        tuple4, q, t = (2, 7, 50, 17), 19, 12
        residue, modulus = build_class(tuple4, q, t)
        for value, mod in zip((*tuple4, t, 34), (9, 49, 121, 529, q*q, 40)):
            self.assertEqual(residue % mod, value)
        members = class_member(residue, modulus)
        self.assertLessEqual(len(members), 1)
        self.assertTrue(all(CELL_LOW <= n <= CELL_HIGH for n in members))

    def test_pair_domain_retains_shift_28_identities(self):
        pairs = load_pairs(ROOT)
        self.assertEqual([(p["c"], p["d"]) for p in pairs if p["shift"] == 28], [(1, 2), (3, 0)])

    def test_no_forbidden_executable_imports(self):
        tools = ROOT / "analysis/p5_sparse_panel_feasibility/tools"
        forbidden = (
            "src/search_twosquares", "src/p4_census_direct_oracle", "src/k4_ap_backend",
            "src/search_factor", "src/tn_", "Backend A", "Backend B",
        )
        for path in tools.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"forbidden evaluator token in {path.name}: {token}")


if __name__ == "__main__":
    unittest.main()
