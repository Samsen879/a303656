#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "analysis/fifth_prime_marginal_coverage/tools"
sys.path.insert(0, str(TOOLS))

import enumerator_a
import enumerator_b
from brute_force_oracle import literal_score
from common import load_bases, load_pairs, load_prime_authority, mask_int


class ExactLandscapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _eligible, cls.candidates, cls.authority = load_prime_authority(ROOT)
        cls.pairs = load_pairs(ROOT)
        cls.bases = load_bases(ROOT)

    def test_authorities(self):
        self.assertEqual(len(self.candidates), 524)
        self.assertEqual(self.authority["excluded_intersection"], [7, 11, 23])
        self.assertFalse(self.authority["prime_3_in_authority"])
        self.assertEqual(len(self.pairs), 407)
        self.assertEqual([(x["c"], x["d"]) for x in self.pairs if x["shift"] == 28], [(1, 2), (3, 0)])
        self.assertEqual(len(self.bases), 13)

    def test_independent_enumerators_and_literal_oracle(self):
        for q in (19, 31, 43):
            a = enumerator_a.enumerate_compressed(q, self.pairs)
            b = enumerator_b.enumerate_compressed(q, self.pairs)
            self.assertEqual(a, b)
            self.assertEqual(a["empty_lift_count"] + sum(x["full_lift_count"] + len(x["exclusions"]) for x in a["buckets"]), q*q)
            for base in self.bases:
                value = mask_int(base["coverage_mask_hex"])
                sa = enumerator_a.score(a, value, base["base_mask_digest"])
                sb = enumerator_b.score(b, value, base["base_mask_digest"])
                self.assertEqual(sa, sb)
                self.assertEqual(sa, literal_score(q, self.pairs, value, base["base_mask_digest"]))


if __name__ == "__main__":
    unittest.main()
