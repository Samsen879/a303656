#!/usr/bin/env python3
"""Bounded, non-circular sufficient AJT5 certificates. Nonpositive is UNKNOWN.

Complete masks use R1's exact witness/valuation wire format. Lower subsets
carry one actual nonnegative square witness per asserted bit. Neither form
can assert unproved positive bits. Gate acceptance never tests D intersect P.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from verify_ajt5_reports import (check_certificate, exponents, integer,
                                 powers, require)

MAX_M = 10_000_000


def forbidden36(m, L):
    return {d for d, five in enumerate(powers(5, m))
            if d <= L and (m - five) % 36 == 24}


def summary(m, D, E):
    """Count each side separately; E alone determines predecessor side P."""
    L = len(powers(5, m)) - 1
    U = set(range(L + 1))
    require(D <= U and E <= set(range(L + 2)), "exponent universe")
    P = (E | {e - 1 for e in E}) & U
    F = forbidden36(m, L)
    return {"L": L, "d_size": len(D), "d_runs": sum(d - 1 not in D for d in D),
            "e_size": len(E), "p_size": len(P),
            "d_parity": [sum(d % 2 == b for d in D) for b in (0, 1)],
            "p_parity": [sum(p % 2 == b for p in P) for b in (0, 1)],
            "u_parity": [sum(u % 2 == b for u in U) for b in (0, 1)],
            "f_outside_p_parity": [sum(f % 2 == b for f in F - P) for b in (0, 1)]}


def margins(s):
    k = [s["d_parity"][b] + s["p_parity"][b] - s["u_parity"][b] for b in (0, 1)]
    augmented = [k[b] + s["f_outside_p_parity"][b] for b in (0, 1)]
    gf = s["d_size"] + s["d_runs"] + s["e_size"] - (s["L"] + 2)
    gb = s["d_size"] + s["p_size"] - (s["L"] + 1)
    return {"gF": gf, "gB": gb, "kappa": k, "PB2": max(k),
            "delta36": gb + sum(s["f_outside_p_parity"]),
            "parity36": augmented, "PB36": max(augmented),
            "K": max(gf, max(k))}


def lower_side(record, n):
    require(type(record) is dict and set(record) == {"n", "witnesses"}, "lower side fields")
    require(type(record["n"]) is int and record["n"] == n, "lower side n")
    require(type(record["witnesses"]) is list, "witness list")
    p5, D = powers(5, n), set()
    for entry in record["witnesses"]:
        require(type(entry) is list and len(entry) == 4, "lower witness shape")
        d, a, b, c = entry
        integer(d, 0, len(p5) - 1, "lower d")
        integer(a, 0, math.isqrt(n), "lower a")
        integer(b, 0, math.isqrt(n), "lower b")
        p3 = powers(3, n - p5[d])
        integer(c, 0, len(p3) - 1, "lower c")
        require(a * a + b * b + p3[c] + p5[d] == n, "lower witness equation")
        require(d not in D, "duplicate lower d")
        D.add(d)
    return D


def verified_sides(record):
    require(type(record) is dict and set(record) == {"schema", "m", "r", "mode", "parent", "child", "summary"},
            "gate certificate fields")
    require(type(record["schema"]) is int and record["schema"] == 1, "gate schema")
    m = integer(record["m"], 2, MAX_M, "campaign m")
    r = integer(record["r"], 0, 4, "campaign r")
    require(record["mode"] in ("complete", "lower"), "certificate mode")
    if record["mode"] == "complete":
        n1, d = check_certificate(record["parent"])
        n2, e = check_certificate(record["child"])
        require((n1, n2) == (m, 5 * m + r), "side integer binding")
        D, E = exponents(d), exponents(e)
    else:
        D, E = lower_side(record["parent"], m), lower_side(record["child"], 5 * m + r)
    s = summary(m, D, E)
    # Strict JSON equality rejects bool/int and float/int substitutions too.
    require(json.dumps(record["summary"], sort_keys=True) == json.dumps(s, sort_keys=True),
            "side-specific summary differs")
    return m, r, D, E, s


def verify_gate(record):
    try:
        _, _, _, _, s = verified_sides(record)
        values = margins(s)
        accepted = [name for name in ("gF", "gB", "PB2", "delta36", "PB36") if values[name] > 0]
        return {"status": "SUFFICIENT_BRIDGE" if accepted else "UNKNOWN",
                "accepted_by": accepted, "margins": values,
                "scope": "verified complete masks" if record["mode"] == "complete" else "verified lower subsets"}
    except (ValueError, TypeError, KeyError, IndexError, OverflowError) as error:
        return {"status": "UNKNOWN", "reason": str(error)}


def classify_exact(record):
    """Separate exhaustive route; never used to accept a positive gate."""
    try:
        _, _, D, E, _ = verified_sides(record)
        require(record["mode"] == "complete", "full certified exponent coverage required")
        if not E:
            return "A303656_COUNTEREXAMPLE"
        if D and not any(d in E or d + 1 in E for d in D):
            return "AJT5_COUNTEREXAMPLE_ONLY"
        return "UNKNOWN"
    except (ValueError, TypeError, KeyError, IndexError, OverflowError):
        return "UNKNOWN"


def certificate(m, r, parent, child, mode="complete"):
    if mode == "complete":
        D, E = exponents(parent["mask"]), exponents(child["mask"])
    else:
        D, E = lower_side(parent, m), lower_side(child, 5 * m + r)
    return {"schema": 1, "m": m, "r": r, "mode": mode, "parent": parent,
            "child": child, "summary": summary(m, D, E)}


def lambda_dp(L, size, runs, E):
    """Minimum directed-edge count over all X with the stated size/runs."""
    states = {(0, 0, 0): 0}  # used vertices, started runs, previous bit
    for i in range(L + 1):
        updated = {}
        weight = int(i in E) + int(i + 1 in E)
        for (used, started, previous), cost in states.items():
            for bit in (0, 1):
                key = used + bit, started + int(bit and not previous), bit
                if key[0] <= size and key[1] <= runs:
                    updated[key] = min(updated.get(key, 10**9), cost + bit * weight)
        states = updated
    candidates = [value for (used, started, _), value in states.items() if (used, started) == (size, runs)]
    require(bool(candidates), "infeasible summary")
    return min(candidates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_gate(json.loads(args.certificate.read_text())), indent=2, sort_keys=True))
