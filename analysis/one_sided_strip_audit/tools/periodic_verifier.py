#!/usr/bin/env python3
"""Fail-closed verifier for finite-period one-sided-strip certificates."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


class CertificateError(ValueError):
    pass


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    q = 3
    while q * q <= n:
        if n % q == 0:
            return False
        q += 2
    return True


def order(a: int, modulus: int) -> int:
    if math.gcd(a, modulus) != 1:
        raise CertificateError("multiplicative order is undefined")
    value = 1
    for exponent in range(1, modulus + 1):
        value = value * a % modulus
        if value == 1:
            return exponent
    raise CertificateError("multiplicative order search failed")


def valuation_below_precision(delta: int, p: int, K: int) -> int | None:
    modulus = p**K
    delta %= modulus
    if delta == 0:
        return None
    exponent = 0
    while delta % p == 0:
        exponent += 1
        delta //= p
    return exponent


def two_square_residues(modulus: int) -> set[int]:
    squares = {x * x % modulus for x in range(modulus)}
    return {(a + b) % modulus for a in squares for b in squares}


def crt(rows: list[tuple[int, int]]) -> tuple[int, int]:
    value, modulus = 0, 1
    for residue, local_modulus in rows:
        if math.gcd(modulus, local_modulus) != 1:
            raise CertificateError("CRT moduli are not pairwise coprime")
        step = ((residue - value) * pow(modulus, -1, local_modulus)) % local_modulus
        value += modulus * step
        modulus *= local_modulus
    return value % modulus, modulus


def verify_certificate(obj: dict[str, Any]) -> dict[str, Any]:
    if set(obj) - {"C", "two_adic", "primes"}:
        raise CertificateError("unknown top-level field")
    C = obj.get("C")
    if not isinstance(C, int) or isinstance(C, bool) or C < 0:
        raise CertificateError("C must be a nonnegative integer")
    prime_rows = obj.get("primes")
    if not isinstance(prime_rows, list):
        raise CertificateError("primes must be a list")

    local_rows: list[dict[str, Any]] = []
    congruences: list[tuple[int, int]] = []
    periods: list[int] = []
    seen: set[int] = set()

    two_adic = obj.get("two_adic")
    two_square_mod2: set[int] | None = None
    if two_adic is not None:
        if not isinstance(two_adic, dict) or set(two_adic) != {"K", "r"}:
            raise CertificateError("two_adic must contain exactly K and r")
        K2, r2 = two_adic["K"], two_adic["r"]
        if not isinstance(K2, int) or isinstance(K2, bool) or K2 < 2:
            raise CertificateError("two-adic K must be an integer at least 2")
        if not isinstance(r2, int) or isinstance(r2, bool):
            raise CertificateError("two-adic residue must be an integer")
        modulus2 = 2**K2
        r2 %= modulus2
        period2 = order(5, modulus2)
        periods.append(period2)
        congruences.append((r2, modulus2))
        two_square_mod2 = two_square_residues(modulus2)
        two_adic = {"K": K2, "r": r2, "modulus": modulus2, "period": period2}

    for raw in prime_rows:
        if not isinstance(raw, dict) or set(raw) - {"p", "K", "r", "odd_valuations"}:
            raise CertificateError("invalid prime row fields")
        if not {"p", "K", "r"} <= set(raw):
            raise CertificateError("prime row is missing p, K, or r")
        p, K, residue = raw["p"], raw["K"], raw["r"]
        if any(not isinstance(x, int) or isinstance(x, bool) for x in (p, K, residue)):
            raise CertificateError("prime row values must be integers")
        if p in seen:
            raise CertificateError("duplicate prime")
        seen.add(p)
        if not is_prime(p) or p % 4 != 3 or p == 5:
            raise CertificateError("invalid obstruction prime")
        if K < 2:
            raise CertificateError("odd-prime K must be at least 2")
        allowed = raw.get("odd_valuations", list(range(1, K, 2)))
        if not isinstance(allowed, list) or not allowed:
            raise CertificateError("odd_valuations must be a nonempty list")
        if any(not isinstance(e, int) or isinstance(e, bool) or e < 1 or e >= K or e % 2 == 0 for e in allowed):
            raise CertificateError("invalid accepted valuation")
        if len(set(allowed)) != len(allowed):
            raise CertificateError("duplicate accepted valuation")
        modulus = p**K
        residue %= modulus
        period = order(5, modulus)
        local_rows.append({
            "p": p, "K": K, "r": residue, "modulus": modulus,
            "period": period, "odd_valuations": sorted(allowed),
        })
        periods.append(period)
        congruences.append((residue, modulus))

    period = math.lcm(*periods) if periods else 1
    global_residue, global_modulus = crt(congruences) if congruences else (0, 1)
    uncovered: list[list[int]] = []
    covered = 0
    for c in range(C + 1):
        for d in range(period):
            hit = False
            if two_adic is not None and two_square_mod2 is not None:
                remainder = (two_adic["r"] - pow(3, c, two_adic["modulus"]) - pow(5, d, two_adic["modulus"])) % two_adic["modulus"]
                hit = remainder not in two_square_mod2
            if not hit:
                for row in local_rows:
                    delta = (row["r"] - pow(3, c, row["modulus"]) - pow(5, d, row["modulus"])) % row["modulus"]
                    valuation = valuation_below_precision(delta, row["p"], row["K"])
                    if valuation in row["odd_valuations"]:
                        hit = True
                        break
            if hit:
                covered += 1
            else:
                uncovered.append([c, d])
    return {
        "schema": "a303656-one-sided-periodic-certificate-v1",
        "C": C,
        "global_modulus": global_modulus,
        "global_residue": global_residue,
        "tail_period": period,
        "cell_count": (C + 1) * period,
        "covered_count": covered,
        "uncovered_count": len(uncovered),
        "uncovered_prefix": uncovered[:32],
        "PASS": not uncovered,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = verify_certificate(json.loads(args.certificate.read_text(encoding="utf-8")))
    except (CertificateError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(json.dumps({"PASS": False, "error": str(exc)}, sort_keys=True))
        return 2
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
