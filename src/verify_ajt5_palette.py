#!/usr/bin/env python3
"""Integer-only replay of the R4 restricted palette proofs, with regenerated obligations."""
import argparse
import functools
import gzip
import json
from collections import Counter, defaultdict
from itertools import combinations
from math import isqrt
from pathlib import Path

from ajt5_integer_certificates import MAX_BYTES, parse


PROOFS = Path(__file__).resolve().parents[1] / "analysis/ajt5_integer_certificates/proofs"
VARIANTS = ("no3_22", "no3_23", "all14_d7", "all14_d6")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def parent_count(variant):
    return 8 if variant in ("no3_23", "all14_d7") else 7


def labels(variant, r, mask):
    """Keep row labels up to the final projection to distinct integer roots."""
    levels = parent_count(variant)
    inside = {j for j in range(levels) if mask >> j & 1}
    targets = inside | {j+1 for j in inside}
    rows = {}
    for j in set(range(levels)) - inside:
        for c in range(13):
            if j == 7 and c == 12:
                continue  # inactive near the lower endpoint
            rows["P", j, c] = 5**(j+1) + 5*3**c
    for e in targets:
        cmax = 12
        if variant.startswith("all14"):
            cmax = 14 if variant == "all14_d6" and e <= 2 else 13
        for c in range(cmax+1):
            rows["Q", e, c] = 5**e + 3**c - r
    return rows


def trial_primes(bound):
    sieve = bytearray([1]) * (bound+1)
    for p in range(2, isqrt(bound)+1):
        if sieve[p]:
            for composite in range(p*p, bound+1, p):
                sieve[composite] = 0
    return tuple(p for p in range(2, bound+1) if sieve[p])


@functools.lru_cache(maxsize=32768)
def inert_divisors(diff, primes):
    found = []
    for p in primes:
        if p*p > diff:
            break
        if diff % p:
            continue
        if p % 4 == 3 and p != 3:
            found.append(p)
        while diff % p == 0:
            diff //= p
    if diff > 3 and diff % 4 == 3:
        found.append(diff)
    return tuple(found)


def catalogue(universe):
    roots = sorted(universe)
    primes = trial_primes(isqrt(roots[-1]-roots[0]))
    colors = set()
    for a, b in combinations(roots, 2):
        colors.update(inert_divisors(b-a, primes))
    catalogue = {}
    for p in sorted(colors):
        groups = defaultdict(set)
        for a in roots:
            groups[a % p].add(a)
        catalogue[p] = {k: group for k, group in groups.items() if len(group) >= 2}
    return catalogue


def restrict(catalog, active, excluded=None):
    result = {}
    for p, groups in catalog.items():
        if p == excluded:
            continue
        remaining = {}
        for k, group in groups.items():
            overlap = group & active
            if len(overlap) >= 2:
                remaining[k] = overlap
        if remaining:
            result[p] = remaining
    return result


def v3(nonzero):
    t = abs(nonzero)
    require(t > 0, "zero has no finite valuation")
    h = 0
    while t % 3 == 0:
        h += 1
        t //= 3
    return h


def maximal_masks(roots, residue):
    # Choose a nearest root and represent its last matching ternary digit.
    # Beyond the largest pairwise coincidence depth only its parity matters.
    depth = max((v3(b-a) for a, b in combinations(roots, 2)), default=0)
    samples = {a + t*3**h for a in roots for h in range(depth+3) for t in (1, 2)}
    samples.update(roots)
    masks = {sum(1 << i for i, a in enumerate(roots) if x != a and v3(x-a) % 2)
             for x in samples if x % 3 == residue}
    maximal = []
    for mask in sorted(masks, key=int.bit_count, reverse=True):
        if not any(mask & other == mask for other in maximal):
            maximal.append(mask)
    return set(maximal) - {0}


def pair(node):
    require(type(node) is list and len(node) == 2, "expected pair")
    return node


def check_tree(node, active, groups, budget, stats):
    key, payload = pair(node)
    require(type(key) is int and type(payload) is list and payload, "malformed node")
    if type(payload[0]) is int:
        scale = key
        require(scale > 0 and len(payload) == len(active), "weight dimension or scale")
        require(all(type(w) is int and 0 <= w <= scale for w in payload), "invalid weight")
        weights = dict(zip(sorted(active), payload))
        # Compute the least sufficient penalty for each still-available color.
        penalty = 0
        for classes in groups.values():
            best = max(sum(weights[i] for i in members) for members in classes.values())
            penalty += max(0, best - scale)
        require(sum(payload) - penalty > budget*scale, "non-strict dual bound")
        stats["leaves"] += 1
        return
    p = key
    require(p in groups, "branch on unavailable color")
    expected = set(groups[p]) | {None}
    seen = set()
    for edge in payload:
        k, child = pair(edge)
        require((k is None or type(k) is int) and k in expected and k not in seen,
                "invalid or duplicate residue branch")
        seen.add(k)
        kept = active if k is None else active - groups[p][k]
        remaining = restrict(groups, kept, excluded=p)
        check_tree(child, kept, remaining, budget - int(k is not None), stats)
    require(seen == expected, "missing residue or default branch")
    stats["branches"] += 1


def verify_direction(variant, r, mask, proof, catalog, stats):
    rows = labels(variant, r, mask)
    roots = sorted(set(rows.values()))
    threshold = 956599 if variant == "all14_d6" else 547067
    require(all(5*threshold > a for a in roots), "inactive or zero tail obligation")
    active = set(roots)
    groups = restrict(catalog, active)
    if variant.startswith("no3"):
        check_tree(proof, active, groups, 22 if variant == "no3_22" else 23, stats)
        return
    require(type(proof) is list and len(proof) == 4, "missing 3-adic branch")
    check_tree(proof[0], active, groups, 14, stats)
    for k, entry in enumerate(proof[1:]):
        kind, branch = pair(entry)
        if kind == "coarse":
            kept = {a for a in active if a % 3 != k}
            check_tree(branch, kept, restrict(groups, kept), 13, stats)
        else:
            require(kind == "exact" and type(branch) is list, "unknown ternary branch")
            wanted = {hex(z) for z in maximal_masks(roots, k)}
            seen = set()
            for item in branch:
                tag, tree = pair(item)
                require(type(tag) is str and tag in wanted and tag not in seen, "wrong ternary mask")
                seen.add(tag)
                subset = int(tag, 16)
                kept = {a for i, a in enumerate(roots) if not subset >> i & 1}
                check_tree(tree, kept, restrict(groups, kept), 13, stats)
            require(seen == wanted, "missing ternary mask")
            # If 3 kills nothing, the budget-14 root proof already suffices.
            stats["exact_ternary_classes"] += 1


def replay(variant, path):
    orientations = 1 << parent_count(variant)
    stats = Counter()
    with gzip.open(path, "rb") as proof:
        for r in range(5):
            universe = set(labels(variant, r, 0).values()) | set(labels(variant, r, orientations-1).values())
            catalog = catalogue(universe)
            for mask in range(orientations):
                record = parse(proof.readline(MAX_BYTES+1))
                require(type(record) is list and len(record) == 3, "invalid direction")
                digit, bits, tree = record
                require(type(digit) is int and type(bits) is int and (digit, bits) == (r, mask),
                        "missing, duplicated or misplaced direction")
                verify_direction(variant, r, mask, tree, catalog, stats)
                stats["directions"] += 1
        require(not proof.read(1), "unexpected trailing direction")
    return dict(stats)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=VARIANTS)
    parser.add_argument("--proof-dir", type=Path, default=PROOFS)
    args = parser.parse_args()
    for key in ((args.variant,) if args.variant else VARIANTS):
        stats = replay(key, args.proof_dir / (key + ".jsonl.gz"))
        print(json.dumps({"variant": key, **stats}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
