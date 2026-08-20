#!/usr/bin/env python3
"""Independent closed-form model for the bounded C=1 coarse-fatal audit."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


class AuditError(ValueError):
    pass


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        value = pow(base, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(s - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


def factor(n: int) -> dict[int, int]:
    result: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            result[divisor] = result.get(divisor, 0) + 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def order_mod_prime(base: int, p: int) -> int:
    if not is_prime(p) or math.gcd(base, p) != 1:
        raise AuditError("order requires a prime modulus and a unit")
    value = p - 1
    for q, exponent in factor(value).items():
        for _ in range(exponent):
            if pow(base, value // q, p) != 1:
                break
            value //= q
    return value


def valuation_below(value: int, p: int, K: int) -> int | None:
    value %= p**K
    if value == 0:
        return None
    exponent = 0
    while value % p == 0:
        exponent += 1
        value //= p
    return exponent


def valuation_integer(value: int, p: int) -> int:
    if value == 0:
        raise AuditError("integer valuation of zero is not finite")
    exponent = 0
    while value % p == 0:
        exponent += 1
        value //= p
    return exponent


def clipped_s(p: int, w: int, K: int) -> int:
    """Return min(v_p(5^w-1), K) using modular powers only."""
    for exponent in range(1, K):
        if pow(5, w, p ** (exponent + 1)) != 1:
            return exponent
    return K


def two_square_mod_2k(value: int, K: int) -> bool:
    value %= 2**K
    if value == 0:
        return True
    while value % 2 == 0:
        value //= 2
    return value % 4 == 1


@dataclass(frozen=True)
class OddRow:
    p: int
    K: int
    residue: int
    accepted: frozenset[int]
    w: int
    s: int
    a: int
    period: int
    modulus: int
    coarse_logs: dict[int, int]
    dynamic_logs: dict[int, int]

    @classmethod
    def build(
        cls, p: int, K: int, residue: int, accepted: Iterable[int], cap: int
    ) -> "OddRow":
        accepted_set = frozenset(accepted)
        if not is_prime(p) or p % 4 != 3 or p == 5 or K < 2:
            raise AuditError("invalid odd row")
        if not accepted_set or any(
            type(e) is not int or e <= 0 or e >= K or e % 2 == 0
            for e in accepted_set
        ):
            raise AuditError("accepted valuations must be positive odd and below K")
        w = order_mod_prime(5, p)
        s = clipped_s(p, w, K)
        a = max(0, K - s)
        period = w * p**a
        if w > cap or p**a > cap or period > cap:
            raise AuditError("row exceeds bounded audit cap")
        modulus = p**K
        coarse_logs = {pow(5, b, p): b for b in range(w)}
        generator = pow(5, w, modulus)
        dynamic_logs = {pow(generator, q, modulus): q for q in range(p**a)}
        if len(coarse_logs) != w or len(dynamic_logs) != p**a:
            raise AuditError("unexpected subgroup collision")
        return cls(
            p, K, residue % modulus, accepted_set, w, s, a, period,
            modulus, coarse_logs, dynamic_logs,
        )

    def safe(self, c: int, d: int) -> bool:
        exponent = valuation_below(
            self.residue - 3**c - pow(5, d, self.modulus), self.p, self.K
        )
        return exponent not in self.accepted

    def fatal_closed(self, c: int, x: int, U: int) -> bool:
        target = (self.residue - 3**c) % self.modulus
        b = self.coarse_logs.get(target % self.p)
        if b is None or x % self.w != b:
            return False
        normalized = target * pow(pow(5, b, self.modulus), -1, self.modulus)
        normalized %= self.modulus
        h = self.K if normalized == 1 else valuation_integer(
            (normalized - 1) % self.modulus, self.p
        )
        if h < min(self.s, self.K):
            return h in self.accepted
        if self.K <= self.s and h == self.K:
            return False
        if not (self.s < self.K and h >= self.s):
            raise AuditError("local trichotomy did not close")
        q0 = self.dynamic_logs.get(normalized)
        if q0 is None:
            raise AuditError("dynamic logarithm is missing")
        beta = valuation_integer(U, self.p) if U % self.p == 0 else 0
        qx = (x - b) // self.w
        dynamic_modulus = self.p**self.a
        difference = (qx - q0) % dynamic_modulus
        if beta < self.a and (qx - q0) % (self.p**beta) == 0:
            return False
        if difference == 0:
            return False
        fixed_valuation = self.s + valuation_integer(difference, self.p)
        return fixed_valuation in self.accepted


@dataclass(frozen=True)
class LocalSystem:
    rows: tuple[OddRow, ...]
    two_K: int | None
    two_residue: int | None
    U: int
    L: int

    @classmethod
    def build(cls, obj: dict, cap: int = 100_000) -> "LocalSystem":
        if set(obj) - {"C", "two_adic", "primes"} or obj.get("C") != 1:
            raise AuditError("system must have exactly C=1")
        raw_rows = obj.get("primes")
        if not isinstance(raw_rows, list):
            raise AuditError("primes must be a list")
        rows: list[OddRow] = []
        seen: set[int] = set()
        for raw in raw_rows:
            if not isinstance(raw, dict) or set(raw) != {
                "p", "K", "r", "odd_valuations"
            }:
                raise AuditError("invalid row fields")
            if raw["p"] in seen:
                raise AuditError("duplicate prime")
            seen.add(raw["p"])
            rows.append(OddRow.build(
                raw["p"], raw["K"], raw["r"], raw["odd_valuations"], cap
            ))
        two = obj.get("two_adic")
        two_K = two_residue = None
        two_period = 1
        if two is not None:
            if not isinstance(two, dict) or set(two) != {"K", "r"}:
                raise AuditError("invalid two-adic row")
            if type(two["K"]) is not int or two["K"] < 2:
                raise AuditError("two-adic K must be at least two")
            two_K = two["K"]
            two_residue = two["r"] % (2**two_K)
            two_period = 1 if two_K == 2 else 2 ** (two_K - 2)
        U = math.lcm(two_period, *(row.w for row in rows))
        L = math.lcm(two_period, *(row.period for row in rows))
        if L > cap:
            raise AuditError("full period exceeds bounded audit cap")
        return cls(tuple(rows), two_K, two_residue, U, L)

    def two_safe(self, c: int, d: int) -> bool:
        if self.two_K is None or self.two_residue is None:
            return True
        return two_square_mod_2k(
            self.two_residue - 3**c - pow(5, d, 2**self.two_K), self.two_K
        )

    def direct_safe_cells(self) -> list[tuple[int, int]]:
        return [
            (c, d)
            for c in (0, 1)
            for d in range(self.L)
            if self.two_safe(c, d) and all(row.safe(c, d) for row in self.rows)
        ]

    def formula_projection(self) -> set[tuple[int, int]]:
        return {
            (c, x)
            for c in (0, 1)
            for x in range(self.U)
            if self.two_safe(c, x)
            and all(not row.fatal_closed(c, x, self.U) for row in self.rows)
        }

    def audit(self) -> dict:
        full = self.direct_safe_cells()
        direct_projection = {(c, d % self.U) for c, d in full}
        formula_projection = self.formula_projection()
        brute_formula_checks = 0
        for c in (0, 1):
            for x in range(self.U):
                for row in self.rows:
                    brute = all(row.safe(c, d) is False for d in range(x, self.L, self.U))
                    closed = row.fatal_closed(c, x, self.U)
                    if brute != closed:
                        raise AuditError(
                            f"fatal mismatch p={row.p} c={c} x={x}: {closed} != {brute}"
                        )
                    brute_formula_checks += 1
        if direct_projection != formula_projection:
            raise AuditError("reverse CRT projection mismatch")
        return {
            "U": self.U,
            "L": self.L,
            "full_safe_count": len(full),
            "projected_safe_count": len(direct_projection),
            "closed_formula_checks": brute_formula_checks,
            "complete_certificate": not full,
            "first_escape": list(min(full)) if full else None,
            "PASS": True,
        }
