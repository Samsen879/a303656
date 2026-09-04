from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from arithmetic_realizability_checker import fatal_at_precision_two
from common import clipped_valuation


class LocalZeroTests(unittest.TestCase):
    def test_zero_is_unresolved_and_not_accepted(self) -> None:
        p, residue, anchor, d = 67, 4, 1, 0
        self.assertIsNone(clipped_valuation(residue - 3**anchor - pow(5, d, p * p), p, 2))
        self.assertFalse(fatal_at_precision_two(p, residue, anchor, d))

    def test_rigid_row_fills_dynamic_center(self) -> None:
        self.assertTrue(fatal_at_precision_two(20771, 20775, 1, 0))


if __name__ == "__main__":
    unittest.main()
