from __future__ import annotations

import copy
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from model import (  # noqa: E402
    AuditError, LocalSystem, OddRow, order_mod_prime, two_square_mod_2k,
    valuation_below,
)


SAMPLE = {
    "C": 1,
    "two_adic": {"K": 3, "r": 0},
    "primes": [
        {"p": 3, "K": 4, "r": 7, "odd_valuations": [1, 3]},
        {"p": 7, "K": 2, "r": 11, "odd_valuations": [1]},
        {"p": 19, "K": 2, "r": 17, "odd_valuations": [1]},
    ],
}


class ModelTests(unittest.TestCase):
    def test_zero_is_unresolved(self):
        self.assertIsNone(valuation_below(0, 20771, 2))

    def test_two_adic_formula(self):
        for K in range(2, 10):
            modulus = 2**K
            squares = {x * x % modulus for x in range(modulus)}
            direct = {(x + y) % modulus for x in squares for y in squares}
            formula = {x for x in range(modulus) if two_square_mod_2k(x, K)}
            self.assertEqual(direct, formula)

    def test_known_nonregular_geometry(self):
        p, w = 20771, order_mod_prime(5, 20771)
        self.assertEqual(w, 10385)
        self.assertEqual(pow(5, w, p * p), 1)
        self.assertNotEqual(pow(5, w, p * p * p), 1)

    def test_entangled_formula_matches_full_period(self):
        system = LocalSystem.build(copy.deepcopy(SAMPLE))
        self.assertEqual((system.U, system.L), (18, 7182))
        result = system.audit()
        self.assertTrue(result["PASS"])
        row3 = next(row for row in system.rows if row.p == 3)
        beta3 = 0
        value = system.U
        while value % 3 == 0:
            beta3 += 1
            value //= 3
        self.assertEqual((beta3, row3.a), (2, 3))

    def test_local_rigid_and_dynamic_cases(self):
        p, K, cap = 20771, 3, 300_000_000
        w = order_mod_prime(5, p)
        modulus = p**K
        rigid_target = (1 + p) % modulus
        rigid = OddRow.build(p, K, rigid_target + 1, [1], cap)
        self.assertTrue(rigid.fatal_closed(0, 0, w))
        generator = pow(5, w, modulus)
        dynamic_target = pow(generator, 123, modulus)
        dynamic = OddRow.build(p, K, dynamic_target + 1, [1], cap)
        self.assertFalse(dynamic.fatal_closed(0, 0, w))

    def test_duplicate_prime_rejected(self):
        obj = copy.deepcopy(SAMPLE)
        obj["primes"].append(copy.deepcopy(obj["primes"][0]))
        with self.assertRaises(AuditError):
            LocalSystem.build(obj)

    def test_even_valuation_rejected(self):
        obj = copy.deepcopy(SAMPLE)
        obj["primes"][0]["odd_valuations"] = [2]
        with self.assertRaises(AuditError):
            LocalSystem.build(obj)

    def test_wrong_C_rejected(self):
        obj = copy.deepcopy(SAMPLE)
        obj["C"] = 2
        with self.assertRaises(AuditError):
            LocalSystem.build(obj)

    def test_unknown_field_rejected(self):
        obj = copy.deepcopy(SAMPLE)
        obj["note"] = "ignored?"
        with self.assertRaises(AuditError):
            LocalSystem.build(obj)

    def test_period_cap_rejected(self):
        with self.assertRaises(AuditError):
            LocalSystem.build(copy.deepcopy(SAMPLE), cap=100)


if __name__ == "__main__":
    unittest.main()
