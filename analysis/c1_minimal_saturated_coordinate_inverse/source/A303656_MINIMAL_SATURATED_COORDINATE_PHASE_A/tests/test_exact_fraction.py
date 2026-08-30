from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import event_mass, fraction_record
from fiber_cover_checker import counterexamples


class ExactFractionTests(unittest.TestCase):
    def test_fraction_records_are_reduced(self) -> None:
        for item in counterexamples().values():
            budget = item.get("budget")
            if budget:
                value = Fraction(budget["numerator"], budget["denominator"])
                self.assertEqual(fraction_record(value), budget)

    def test_no_float_in_fraction_record(self) -> None:
        record = fraction_record(Fraction(2, 3))
        self.assertEqual(record, {"numerator": 2, "denominator": 3, "text": "2/3"})
        self.assertFalse(any(isinstance(v, float) for v in record.values()))


if __name__ == "__main__":
    unittest.main()
