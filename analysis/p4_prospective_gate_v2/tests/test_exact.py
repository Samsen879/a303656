#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from common import L4, class_members, fixed_p4_class, live_authority, pair_domain


class ExactTests(unittest.TestCase):
    def test_pair_and_live_authorities(self):
        pairs = pair_domain()
        self.assertEqual(len(pairs), 407)
        self.assertEqual([(c,d) for c,d,s in pairs if s == 28], [(1,2),(3,0)])
        self.assertEqual(len(live_authority()[0]), 300)

    def test_crt(self):
        tup=(2,13,50,5); r=fixed_p4_class(tup)
        self.assertEqual(r % 40, 34)
        self.assertEqual(tuple(r % m for m in (9,49,121,529)), tup)
        self.assertTrue(all(183968950234 <= n <= 246731069451 for n in class_members(r)))

    def test_exposure_interval_covers_all_classes(self):
        self.assertGreaterEqual(241600000000 - 240000000001 + 1, L4)


if __name__ == "__main__": unittest.main()
