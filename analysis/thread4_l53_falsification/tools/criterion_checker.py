#!/usr/bin/env python3
"""Independent arithmetic-criterion checker for Thread 4 L5,3 candidates."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def factor(n: int) -> list[tuple[int, int]]:
    assert n >= 0
    if n in (0, 1):
        return []
    result = []
    p = 2
    while p * p <= n:
        if n % p:
            p = 3 if p == 2 else p + 2
            continue
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        result.append((p, e))
        p = 3 if p == 2 else p + 2
    if n > 1:
        result.append((n, 1))
    return result


def sum2_criterion(n: int) -> tuple[bool, list[list[int]]]:
    if n < 0:
        return False, []
    if n == 0:
        return True, []
    fs = factor(n)
    blockers = [[p, e] for p, e in fs if p % 4 == 3 and e % 2]
    return not blockers, blockers


def sum2_witness(n: int) -> list[int] | None:
    if n < 0:
        return None
    for a in range(math.isqrt(n) + 1):
        b2 = n - a * a
        b = math.isqrt(b2)
        if b * b == b2:
            return [a, b]
    return None


def powers(base: int, bound: int) -> list[int]:
    result = []
    value = 1
    while value <= bound:
        result.append(value)
        value *= base
    return result


def t3_certificate(x: int) -> dict:
    attempts = []
    for c, p3 in enumerate(powers(3, x)):
        residual = x - p3
        ok, blockers = sum2_criterion(residual)
        if ok:
            witness = sum2_witness(residual)
            assert witness is not None
            return {"in_T3": True, "witness": {"a": witness[0], "b": witness[1], "c": c}, "attempts_before_success": attempts}
        attempts.append({"c": c, "three_power": p3, "residual": residual, "odd_3mod4_valuations": blockers})
    return {"in_T3": False, "exhaustive_attempts": attempts}


def d_table(m: int) -> dict:
    rows = []
    support = []
    for d, p5 in enumerate(powers(5, m)):
        cert = t3_certificate(m - p5)
        rows.append({"d": d, "five_power": p5, "residual": m - p5, **cert})
        if cert["in_T3"]:
            support.append(d)
    return {"m": m, "D": support, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    candidates = [7_963_079, 8_984_426]
    payload = {"engine": "arithmetic criterion with exact trial-division valuations", "candidates": []}
    for m in candidates:
        n = 5 * m + 3
        dm = d_table(m)
        dn = d_table(n)
        shifted = [d + 1 for d in dm["D"]]
        intersection = sorted(set(shifted) & set(dn["D"]))
        payload["candidates"].append({"m": m, "five_m_plus_three": n, "source": dm, "target": dn, "shifted_D_m": shifted, "intersection": intersection})
    payload["reported_representations"] = [
        {"n": 7_963_079, "a": 1446, "b": 2311, "c": 12, "d": 0},
        {"n": 39_815_398, "a": 614, "b": 6280, "c": 0, "d": 0},
    ]
    for row in payload["reported_representations"]:
        row["verified"] = row["n"] == row["a"]**2 + row["b"]**2 + 3**row["c"] + 5**row["d"]
    out = args.output
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "candidates": [{"m": x["m"], "D_m": x["source"]["D"], "D_target": x["target"]["D"], "intersection": x["intersection"]} for x in payload["candidates"]], "representations": payload["reported_representations"]}, indent=2))


if __name__ == "__main__":
    main()
