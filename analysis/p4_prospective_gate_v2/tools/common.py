#!/usr/bin/env python3
"""Shared exact-integer utilities for the prospective P4 gate-v2 audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

LOW = 183_968_950_234
HIGH = 246_731_069_451
N0 = 240_000_005_594
L4 = 1_129_118_760
PRIMES = (3, 7, 11, 23)
MODS = tuple(p * p for p in PRIMES)
LEVELS = (
    "E0_DESIGN_ONLY",
    "E1_BINARY_REPRESENTABILITY_CHECK",
    "E2_EXACT_T_COUNT",
    "E3_COMPLETE_WINNER_MASK",
    "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED",
)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_bytes(json.dumps(value, indent=2, sort_keys=True).encode() + b"\n")


def pair_domain() -> list[tuple[int, int, int]]:
    p3, x = [], 1
    while x <= LOW:
        p3.append(x)
        x *= 3
    p5, x = [], 1
    while x <= LOW:
        p5.append(x)
        x *= 5
    pairs = [(c, d, a + b) for c, a in enumerate(p3) for d, b in enumerate(p5) if a + b <= LOW]
    if len(pairs) != 407 or [(c, d) for c, d, s in pairs if s == 28] != [(1, 2), (3, 0)]:
        raise ValueError("PAIR_DOMAIN_AUTHORITY_MISMATCH")
    return pairs


def prime_masks(pairs: list[tuple[int, int, int]], p: int) -> list[int]:
    masks = []
    for residue in range(p * p):
        mask = 0
        for i, (_, _, shift) in enumerate(pairs):
            q = (residue - shift) % (p * p)
            if q % p == 0 and q != 0:
                mask |= 1 << i
        masks.append(mask)
    return masks


def live_authority() -> tuple[list[int], int]:
    pairs = pair_domain()
    live_indices = [i for i, (c, d, _) in enumerate(pairs) if not (c % 2 == 1 and d % 2 == 0)]
    if len(live_indices) != 300:
        raise ValueError("LIVE_DOMAIN_COUNT_MISMATCH")
    return live_indices, sum(1 << i for i in live_indices)


def project_live(full_mask: int, live_indices: list[int]) -> int:
    projected = 0
    for j, i in enumerate(live_indices):
        projected |= ((full_mask >> i) & 1) << j
    return projected


def crt(residues: tuple[int, ...], moduli: tuple[int, ...]) -> int:
    modulus = 1
    residue = 0
    for a, m in zip(residues, moduli):
        inv = pow(modulus, -1, m)
        residue += modulus * (((a - residue) * inv) % m)
        modulus *= m
        residue %= modulus
    return residue


def fixed_p4_class(tup: tuple[int, int, int, int]) -> int:
    r = crt(tup + (N0 % 40,), MODS + (40,))
    if not all(r % m == a for a, m in zip(tup + (N0 % 40,), MODS + (40,))):
        raise ValueError("CRT_RECONSTRUCTION_FAILURE")
    return r


def class_members(residue: int, low: int = LOW, high: int = HIGH) -> list[int]:
    first = residue + ((low - residue + L4 - 1) // L4) * L4
    return list(range(first, high + 1, L4)) if first <= high else []


def normalize_intervals(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for low, high in sorted(intervals):
        if low > high:
            raise ValueError("INTERVAL_ENDPOINT_ORDER")
        if merged and low <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], high)
        else:
            merged.append([low, high])
    return merged


def in_intervals(n: int, intervals: list[list[int]]) -> bool:
    # Deliberately simple and independently testable; there are only tens of ranges.
    return any(low <= n <= high for low, high in intervals)
