#!/usr/bin/env python3
"""Explicit exact p^2 coverage bitsets for small global exponent tori.

This is Method A only.  It materializes U = Z/L3 x Z/L5 and therefore
refuses instances above --max-universe.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


def multiplicative_order(a: int, modulus: int) -> int:
    if math.gcd(a, modulus) != 1:
        raise ValueError(f"{a} is not a unit modulo {modulus}")
    x = 1
    for k in range(1, modulus + 1):
        x = (x * a) % modulus
        if x == 1:
            return k
    raise AssertionError("order not found")


@dataclass(frozen=True)
class PrimeData:
    p: int
    r2: int
    s2: int


def parse_primes(text: str) -> list[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values or len(set(values)) != len(values):
        raise ValueError("--primes must be a nonempty duplicate-free comma list")
    for p in values:
        if p < 2 or p % 4 != 3 or p in (3, 5):
            raise ValueError(f"ineligible p={p}")
    return values


def make_masks(p: int, L3: int, L5: int) -> tuple[list[tuple[int, int]], dict[str, int | float]]:
    pp = p * p
    x = np.fromiter((pow(3, u, pp) for u in range(L3)), dtype=np.int64, count=L3)
    y = np.fromiter((pow(5, v, pp) for v in range(L5)), dtype=np.int64, count=L5)
    sums = (x[:, None] + y[None, :]) % pp

    by_mask: dict[int, int] = {}
    best = 0
    started = time.perf_counter()
    for t in range(pp):
        covered = ((t - sums) % p == 0) & (sums != t)
        packed = np.packbits(covered.ravel(), bitorder="little")
        mask = int.from_bytes(packed.tobytes(), "little")
        best = max(best, mask.bit_count())
        # Identical coverage sets are interchangeable; retain the least t.
        by_mask.setdefault(mask, t)
    masks = sorted(((t, m) for m, t in by_mask.items()), key=lambda z: z[1].bit_count(), reverse=True)
    stats = {
        "p": p,
        "raw_t_count": pp,
        "distinct_mask_count": len(masks),
        "nonempty_distinct_mask_count": sum(m != 0 for _, m in masks),
        "best_single_coverage": best,
        "build_seconds": time.perf_counter() - started,
    }
    return masks, stats


def exhaustive_max_union(mask_families: list[list[tuple[int, int]]], universe_bits: int) -> dict:
    """Exact DFS; suitable only for tiny Method-A instances."""
    full = (1 << universe_bits) - 1
    # Put the smallest choice family first to reduce branching.
    order = sorted(range(len(mask_families)), key=lambda i: len(mask_families[i]))
    fams = [mask_families[i] for i in order]

    suffix_possible = [0] * (len(fams) + 1)
    for i in range(len(fams) - 1, -1, -1):
        possible = 0
        for _, mask in fams[i]:
            possible |= mask
        suffix_possible[i] = suffix_possible[i + 1] | possible

    best_count = -1
    best_choice_ordered: list[int] | None = None
    nodes = 0
    complete_cover: list[int] | None = None

    def dfs(i: int, union: int, choices: list[int]) -> None:
        nonlocal best_count, best_choice_ordered, nodes, complete_cover
        nodes += 1
        current = union.bit_count()
        if current > best_count:
            best_count = current
            best_choice_ordered = choices.copy()
        if union == full:
            complete_cover = choices.copy()
            return
        if i == len(fams) or complete_cover is not None:
            return
        if (union | suffix_possible[i]) != full and i == 0:
            # This root-level condition is recorded, but we still maximize union.
            pass
        # Upper bound for maximizing: all masks from all remaining families.
        if (union | suffix_possible[i]).bit_count() <= best_count:
            return
        for t, mask in fams[i]:
            dfs(i + 1, union | mask, choices + [t])
            if complete_cover is not None:
                return

    dfs(0, 0, [])

    def unpermute(choice: list[int] | None) -> list[int] | None:
        if choice is None:
            return None
        out = [0] * len(order)
        for j, original_index in enumerate(order):
            out[original_index] = choice[j]
        return out

    return {
        "cover_found": complete_cover is not None,
        "cover_t": unpermute(complete_cover),
        "best_t": unpermute(best_choice_ordered),
        "best_covered": best_count,
        "uncovered_at_best": universe_bits - best_count,
        "nodes": nodes,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", required=True)
    ap.add_argument("--max-universe", type=int, default=2_000_000)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    primes = parse_primes(args.primes)
    data = [PrimeData(p, multiplicative_order(3, p * p), multiplicative_order(5, p * p)) for p in primes]
    L3 = math.lcm(*(z.r2 for z in data))
    L5 = math.lcm(*(z.s2 for z in data))
    universe = L3 * L5
    result: dict = {
        "method": "A-explicit-bitset",
        "primes": primes,
        "orders_p2": {str(z.p): [z.r2, z.s2] for z in data},
        "L3": L3,
        "L5": L5,
        "universe": universe,
        "max_universe": args.max_universe,
    }
    if universe > args.max_universe:
        result.update({"status": "REFUSED_UNIVERSE_TOO_LARGE"})
        print(json.dumps(result, indent=2))
        if args.json:
            args.json.write_text(json.dumps(result, indent=2) + "\n")
        return 3

    started = time.perf_counter()
    families: list[list[tuple[int, int]]] = []
    build_stats = []
    for p in primes:
        masks, stats = make_masks(p, L3, L5)
        families.append(masks)
        build_stats.append(stats)
    search_started = time.perf_counter()
    search = exhaustive_max_union(families, universe)
    search_seconds = time.perf_counter() - search_started
    result.update({
        "status": "EXACT_COMPLETE",
        "build_stats": build_stats,
        "search": search,
        "search_seconds": search_seconds,
        "total_seconds": time.perf_counter() - started,
    })
    print(json.dumps(result, indent=2))
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
