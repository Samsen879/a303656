"""Exact boundary examples and conservative authority wording, not a proof of MF-R."""

from fractions import Fraction as F
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
PKG = ROOT / "analysis" / "multisource_rational_fusion_no_go"


def square(z):
    a, b = z
    return a * a - b * b, 2 * a * b


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


class BoundaryExamples(unittest.TestCase):
    def test_complex_coefficient_escape(self):
        for s in map(F, (-7, 0, 1, 3, 11)):
            u = ((s + 1) / 2, F(0))
            v = (F(0), -(s - 1) / 2)  # (s-1)/(2i)
            self.assertEqual(add(square(u), square(v)), (s, F(0)))

    def test_two_source_norm_one_rotation(self):
        # A_1=0, A_2=4, X=5; both coordinate pairs satisfy their conics.
        a1, b1, a2, b2 = map(F, (1, 2, 1, 0))
        x = F(5)
        c = (a1 * a1 - b1 * b1) / (x - 0)
        d = 2 * a1 * b1 / (x - 0)
        u, v = c * a2 - d * b2, d * a2 + c * b2
        self.assertEqual(c * c + d * d, 1)
        self.assertEqual(u * u + v * v, x - 4)
        self.assertNotEqual(d, 0)

    def test_proper_locus_midpoint(self):
        a1, b1, a2, b2 = map(F, (1, 2, 1, 0))
        x = F(5)
        self.assertEqual(a1 * a1 + b1 * b1, x)
        self.assertEqual(a2 * a2 + b2 * b2, x - 4)
        self.assertEqual((a1 - a2) ** 2 + (b1 - b2) ** 2, 4)
        self.assertEqual(((a1 + a2) / 2) ** 2 + ((b1 + b2) / 2) ** 2, x - 3)
        self.assertNotIn(3, (0, 4))

    def test_converse_sources_and_repeated_offsets(self):
        for offsets, x, sources in (
            ((0, 4), F(5), ((F(1), F(2)), (F(1), F(0)))),
            ((0, 0), F(5), ((F(1), F(2)), (F(2), F(1)))),
        ):
            for offset, (a, b) in zip(offsets, sources):
                self.assertEqual(a * a + b * b, x - offset)


class AuthorityScope(unittest.TestCase):
    def test_theorem_bindings_and_escapes(self):
        theorem = (PKG / "THEOREM.md").read_text()
        scope = " ".join((PKG / "SCOPE.md").read_text().split())
        for phrase in (
            "fixed finite source number", "full generic independent product",
            "original Q-function field", "U,V in K", "monic linear residual",
            "X-T", "Repeated offsets", "arbitrary rational degree and poles",
        ):
            self.assertIn(phrase, theorem)
        for phrase in (
            "arithmetic selection of witnesses", "proper algebraic compatibility loci",
            "rational decoders valid only on such loci", "non-rational operations",
            "growing source complexity", "arbitrary multi-witness methods",
            "nonlinear target norms", "Boolean/support recursion", "U,V in K(i)",
        ):
            self.assertIn(phrase, scope)

    def test_authority_has_one_narrow_entry_and_preserves_status(self):
        index = (ROOT / "docs/POST_FREEZE_THEOREM_AND_ROUTE_INDEX.md").read_text()
        status = (ROOT / "STATUS.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertEqual(index.count("| PF-N-005 |"), 1)
        self.assertIn("full generic independent product", index)
        self.assertIn("original `Q`-function field", index)
        self.assertIn("proper compatibility loci", index)
        self.assertIn("A303656: UNRESOLVED", status)
        self.assertIn("ACTIVE PROMOTED ROUTE: NONE", status)
        self.assertIn("status: UNRESOLVED", readme)

    def test_no_unqualified_authority_overclaim(self):
        paths = [ROOT / p for p in (
            "README.md", "STATUS.md", "docs/POST_FREEZE_THEOREM_AND_ROUTE_INDEX.md",
        )] + list(PKG.glob("*.md"))
        forbidden = (
            r"all multi-witness methods (?:are )?impossible",
            r"all rational multi-source (?:construction|decoders) impossible",
            r"multi-witness route (?:is )?closed",
            r"proper compatibility loci excluded",
            r"complex coefficient field allowed",
            r"A303656 (?:solved|disproved)",
            r"A303656:\s*(?:SOLVED|DISPROVED|PROVED)",
        )
        for path in paths:
            body = path.read_text()
            for pattern in forbidden:
                self.assertIsNone(re.search(pattern, body, re.I), (path, pattern))


if __name__ == "__main__":
    unittest.main()
