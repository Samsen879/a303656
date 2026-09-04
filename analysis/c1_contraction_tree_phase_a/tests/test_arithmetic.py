from __future__ import annotations

import sys
import unittest
from math import gcd, lcm
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from model import (  # noqa: E402
    OddRow,
    TwoAdicRow,
    coarse_fatal_by_enumeration,
    corrupted_coarse_fatal_zero_as_last_shell,
    direct_system_evaluation,
    factorint,
    first_witness_on_progression,
    multiplicative_order_prime,
    odd_fatal,
    odd_row_data,
    odd_status,
    system_period,
    two_adic_unsafe,
)


def direct_order(a: int, modulus: int) -> int:
    phi = modulus
    for p in factorint(modulus):
        phi = phi // p * (p - 1)
    order = phi
    for q in factorint(phi):
        while order % q == 0 and pow(a, order // q, modulus) == 1:
            order //= q
    return order


class ArithmeticReferenceTests(unittest.TestCase):
    def test_lifting_formula_against_direct_orders(self) -> None:
        for p in (3, 7, 11, 31, 67):
            w = multiplicative_order_prime(5, p)
            probe = OddRow(p, 4, 0, (1, 3), f"p={p}")
            s = odd_row_data(probe)["s"]
            for K in range(1, 5):
                expected = w * p ** max(0, K - s)
                self.assertEqual(direct_order(5, p**K), expected)

    def test_chain_full_period_and_saturated_cylinder(self) -> None:
        rows = [
            OddRow(11, 2, 4, (1,), "p=11"),
            OddRow(67, 2, 4, (1,), "p=67"),
            OddRow(20771, 2, 20775, (1,), "p=20771"),
        ]
        L = system_period(rows)
        self.assertEqual(L, 228470)
        full = direct_system_evaluation(rows, 1, period=L)
        self.assertEqual(full["safe_count"], 176698)
        cylinder = first_witness_on_progression(rows, 1, 310, 0, L)
        self.assertEqual(
            cylinder["first_witness_counts"],
            {"p=11": 670, "p=67": 66, "p=20771": 1, "safe": 0},
        )

    def test_aligned_and_misaligned_same_lower_residual(self) -> None:
        p, q, anchor = 67, 20771, 1
        dynamic = OddRow(p, 2, 4, (1,), "p=67")
        q2 = q * q
        aligned = OddRow(q, 2, (3 + 1 + q) % q2, (1,), "aligned")
        misaligned = OddRow(q, 2, (3 + pow(5, 155, q2) + q) % q2, (1,), "misaligned")
        lower_modulus = lcm(22, 10385 // 67)
        self.assertEqual(lower_modulus, 3410)

        def masks(row: OddRow) -> tuple[set[int], set[int], set[int]]:
            pd, qr, zero = set(), set(), set()
            for t in range(67):
                d = lower_modulus * t
                pstatus = odd_status(dynamic, anchor, d)[0]
                if pstatus == "fatal":
                    pd.add(t)
                elif pstatus == "zero":
                    zero.add(t)
                if odd_fatal(row, anchor, d):
                    qr.add(t)
            return pd, qr, zero

        pd_a, qr_a, zero_a = masks(aligned)
        pd_m, qr_m, zero_m = masks(misaligned)
        self.assertEqual(pd_a, pd_m)
        self.assertEqual(zero_a, zero_m)
        self.assertEqual(zero_a, {0})
        self.assertEqual(qr_a, {0})
        self.assertEqual(qr_m, {64})
        self.assertEqual(len(pd_a | qr_a), 67)
        self.assertEqual(len(pd_m | qr_m), 66)

    def test_local_zero_fail_closed_and_corruption(self) -> None:
        row = OddRow(3, 2, 2, (1,), "p=3")
        statuses = [odd_status(row, 0, d)[0] for d in (0, 2, 4)]
        self.assertEqual(statuses, ["zero", "fatal", "fatal"])
        self.assertFalse(coarse_fatal_by_enumeration(row, 0, 0, 2, 6))
        self.assertTrue(corrupted_coarse_fatal_zero_as_last_shell(row, 0, 0, 2, 6))

    def test_k2_boundaries(self) -> None:
        odd = OddRow(11, 2, 0, (1,), "p=11")
        none = direct_system_evaluation([odd], 0)
        safe = direct_system_evaluation([odd], 0, TwoAdicRow(2, 0, "two"))
        unsafe = direct_system_evaluation([odd], 0, TwoAdicRow(2, 1, "two"))
        genuine = direct_system_evaluation([odd], 0, TwoAdicRow(3, 0, "two"))
        self.assertEqual(none["safe_count"], 55)
        self.assertEqual(safe["safe_count"], 55)
        self.assertEqual(unsafe["safe_count"], 0)
        self.assertEqual(genuine["period"], 110)
        self.assertEqual(genuine["safe_count"], 55)


    def test_two_anchor_two_adic_lemma_through_K10(self) -> None:
        from fractions import Fraction
        for K in range(2, 11):
            modulus = 2 ** K
            period = 1 if K == 2 else 2 ** (K - 2)
            worst = Fraction(0, 1)
            for r in range(modulus):
                row = TwoAdicRow(K, r, "two")
                densities = [
                    Fraction(sum(two_adic_unsafe(row, c, d) for d in range(period)), period)
                    for c in (0, 1)
                ]
                worst = max(worst, min(densities))
            if K == 2:
                self.assertEqual(worst, 0)
            else:
                self.assertLessEqual(worst, Fraction(1, 2))

    def test_reverse_crt_escape_equivalence_small_system(self) -> None:
        rows = [OddRow(3, 2, 2, (1,), "p=3"), OddRow(7, 2, 4, (1,), "p=7")]
        U = lcm(*(odd_row_data(r)["w"] for r in rows))
        L = system_period(rows)
        self.assertEqual(U, 6)
        self.assertEqual(L % U, 0)
        for x in range(U):
            no_coarse_fatal = not any(coarse_fatal_by_enumeration(r, 0, x, U, L) for r in rows)
            safe_lift_exists = any(
                not any(odd_fatal(r, 0, x + U * k) for r in rows)
                for k in range(L // U)
            )
            self.assertEqual(no_coarse_fatal, safe_lift_exists)


if __name__ == "__main__":
    unittest.main()
