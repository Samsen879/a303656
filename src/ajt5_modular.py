#!/usr/bin/env python3
"""Strict small-modulus negatives and witness-only strengthened child gate.

The full orbit tests the SAME original c at every residue condition. A modular
pass supplies no positive witness. Bounded admissible-c negatives are separate.
"""
from functools import lru_cache

from ajt5_gates import MAX_M, lower_side
from verify_ajt5_reports import integer, powers, require

MAX_MODULUS = 512


@lru_cache(maxsize=32)
def residue_data(modulus):
    integer(modulus, 2, MAX_MODULUS, "small modulus cap")
    squares = {a * a % modulus for a in range(modulus)}
    s2 = frozenset((a + b) % modulus for a in squares for b in squares)
    orbit, seen, x = [], {}, 1 % modulus
    while x not in seen:
        seen[x] = len(orbit)
        orbit.append(x)
        x = 3 * x % modulus
    return s2, tuple(orbit), seen[x]


def forbidden_residues(modulus):
    s2, orbit, _ = residue_data(modulus)
    return tuple(t for t in range(modulus) if all((t - three) % modulus not in s2 for three in orbit))


def strict_negative(t, modulus):
    integer(t, 0, 50_000_004, "residual domain")
    s2, orbit, _ = residue_data(modulus)
    return all((t - three) % modulus not in s2 for three in orbit)


def bounded_admissible_negative(t, modulus):
    """Separate finite-c test; do not label this an entire-orbit exclusion."""
    integer(t, 0, 50_000_004, "residual domain")
    s2, _, _ = residue_data(modulus)
    return all((t - three) % modulus not in s2 for three in powers(3, t))


def child_summary(m, A, B, H):
    L = len(powers(5, m)) - 1
    S = A | {a + 1 for a in A}
    return {"L": L, "s_size": len(S), "b_size": len(B),
            "h_outside_s": len(H - S), "gFH": len(S) + len(B) - (L + 2) + len(H - S)}


def verify_residue_gate(record):
    """Invalid/nonpositive returns UNKNOWN; acceptance uses counts, not bridges."""
    try:
        require(type(record) is dict and set(record) == {"schema", "m", "r", "parent", "child",
                                                        "modulus", "negative_exponents", "summary"}, "fields")
        require(type(record["schema"]) is int and record["schema"] == 1, "schema")
        m = integer(record["m"], 2, MAX_M, "campaign m")
        r = integer(record["r"], 0, 4, "campaign r")
        n, H = 5 * m + r, record["negative_exponents"]
        L = len(powers(5, m)) - 1
        residue_data(record["modulus"])
        require(type(H) is list and len(H) <= L + 2, "negative exponent list")
        for h in H:
            integer(h, 0, L + 1, "child negative exponent")
            require(strict_negative(n - 5**h, record["modulus"]), "uncertified strict negative")
        require(H == sorted(set(H)), "canonical distinct negatives")
        for side in (record["parent"], record["child"]):
            require(type(side) is dict and type(side.get("witnesses")) is list
                    and len(side["witnesses"]) <= L + 2, "witness list cap")
        A, B = lower_side(record["parent"], m), lower_side(record["child"], n)
        require(not B & set(H), "positive/negative contradiction")
        s = child_summary(m, A, B, set(H))
        import json
        require(json.dumps(s, sort_keys=True) == json.dumps(record["summary"], sort_keys=True), "summary")
        return {"status": "SUFFICIENT_BRIDGE" if s["gFH"] > 0 else "UNKNOWN", "summary": s}
    except (ValueError, TypeError, KeyError, IndexError, OverflowError) as error:
        return {"status": "UNKNOWN", "reason": str(error)}
