from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


periodic = load("periodic_verifier", ROOT / "tools" / "periodic_verifier.py")
method_a = load("method_a", ROOT / "tools" / "method_a.py")


class ExactTests(unittest.TestCase):
    def test_direct_s2_small(self):
        N = 500
        table, _ = method_a.direct_s2(N)
        expected = bytearray(N + 1)
        for a in range(math.isqrt(N) + 1):
            for b in range(math.isqrt(N - a * a) + 1):
                expected[a * a + b * b] = 1
        self.assertEqual(bytes(table.astype("uint8")), bytes(expected))

    def test_c0_mod4_certificate_passes(self):
        obj = {"C": 0, "two_adic": {"K": 2, "r": 1}, "primes": []}
        result = periodic.verify_certificate(obj)
        self.assertTrue(result["PASS"])
        self.assertEqual(result["cell_count"], 1)

    def test_zero_at_precision_is_unresolved(self):
        self.assertIsNone(periodic.valuation_below_precision(0, 3, 2))

    def test_duplicate_shift(self):
        self.assertEqual(3**1 + 5**2, 3**3 + 5**0)


if __name__ == "__main__":
    unittest.main()
