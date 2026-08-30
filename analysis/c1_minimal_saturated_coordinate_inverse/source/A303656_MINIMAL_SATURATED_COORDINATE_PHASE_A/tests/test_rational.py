from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rational_template_enumerator import (
    brute_minimal_candidates,
    build_catalog,
    is_atom_minimal,
    total_mass,
)


class RationalClassificationTests(unittest.TestCase):
    def test_beta_one_two_atom_equality(self) -> None:
        for l in (3, 5, 7, 11):
            self.assertEqual(Fraction(l - 1, l) + Fraction(1, l), 1)
            self.assertTrue(is_atom_minimal(l, (1,), (1,)))

    def test_unique_two_atom_equality_bounded_symbolic(self) -> None:
        for l in (3, 5, 7):
            found = []
            dynamic = [Fraction(l - 1, l**e) for e in range(1, 6)]
            rigid = [Fraction(1, l**e) for e in range(1, 6)]
            atoms = [("D", e + 1, x) for e, x in enumerate(dynamic)] + [("R", e + 1, x) for e, x in enumerate(rigid)]
            for i, a in enumerate(atoms):
                for b in atoms[i + 1 :]:
                    if a[2] + b[2] == 1:
                        found.append((a[:2], b[:2]))
            self.assertEqual(found, [(('D', 1), ('R', 1))])

    def test_no_strict_excess_genuine_atoms(self) -> None:
        check = brute_minimal_candidates(3, 3, 4)
        self.assertEqual(check["strict_excess_count"], 0)

    def test_repeated_dynamic_depth_breaks_theorem(self) -> None:
        for l in (3, 5, 7):
            atom = Fraction(l - 1, l)
            total = 2 * atom
            self.assertGreater(total, 1)
            self.assertLess(total - atom, 1)

    def test_depth_bound(self) -> None:
        catalog = build_catalog()
        for group in catalog["groups"]:
            for record in group["templates"]:
                self.assertLessEqual(record["max_depth"], record["atom_count"] - 1)
                self.assertEqual(record["mass"]["text"], "1/1")

    def test_bundled_two_row_equality_and_parity(self) -> None:
        for l in (3, 5):
            for r in range(1, 5):
                full = sum((Fraction(l - 1, l**e) for e in range(1, r + 1)), Fraction()) + Fraction(1, l**r)
                self.assertEqual(full, 1)
                if r >= 2:
                    # An admitted odd-valuation row cannot accept consecutive j=e-1.
                    depths = list(range(1, r + 1))
                    for s_parity in (0, 1):
                        allowed = [e for e in depths if (s_parity + e - 1) % 2 == 1]
                        self.assertNotEqual(allowed, depths)


if __name__ == "__main__":
    unittest.main()
