#!/usr/bin/env python3
"""Replay the R5 AJT5 palette exclusions using exact integers only."""
import argparse
import gzip
import json
import sys
from collections import Counter
from fractions import Fraction
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))
from ajt5_integer_certificates import MAX_BYTES, parse
from verify_ajt5_palette import catalogue, labels, maximal_masks, pair, require, restrict

FIRST_M = 547067
VARIANTS = ("all15", "no3_24")


def systems(variant, r, mask):
    # R4 labels are rebuilt by exponent and side independently of the producer.
    base = set(labels("all14_d7" if variant == "all15" else "no3_23", r, mask).values())
    if variant == "no3_24" and mask == 0:
        child_c = (1, 2, 5, 2, 4)[r]
        return [base | {5**9 + 5*3}, base | {5**8 + 3**child_c - r}]
    return [base]


def check_tree(tree, active, groups, budget, stats):
    # One residue per remaining prime. Other primes can each remove one root.
    key, payload = pair(tree)
    require(type(key) is int and type(payload) is list and payload, "invalid proof node")
    if type(payload[0]) is int:
        require(key > 0 and len(active) == len(payload), "invalid scale or weight count")
        require(all(type(w) is int and 0 <= w <= key for w in payload), "invalid weight")
        weights = dict(zip(sorted(active), payload))
        penalty = sum(max(0, max(sum(weights[k] for k in group)
                                 for group in residues.values()) - key)
                      for residues in groups.values())
        slack = sum(payload) - penalty - budget*key
        require(slack > 0, "dual bound must be strict")
        margin = Fraction(slack, key)
        stats["min_margin"] = min(margin, stats.get("min_margin", margin))
        stats["leaves"] += 1
        return

    require(key in groups, "branch prime unavailable")
    residues = groups[key]
    required = set(residues) | {None}
    seen = set()
    for item in payload:
        residue, child = pair(item)
        require(residue is None or type(residue) is int, "invalid branch residue type")
        require(residue in required - seen, "unavailable or duplicate residue")
        seen.add(residue)
        remaining = active if residue is None else active - residues[residue]
        # None includes unused primes and singleton classes. The singleton
        # relaxation remains available, so this branch must keep the budget.
        check_tree(child, remaining, restrict(groups, remaining, excluded=key),
                   budget - int(residue is not None), stats)
    require(seen == required, "missing branch")
    stats["branches"] += 1


def check_all(tree, active, catalog, stats):
    groups = restrict(catalog, active)
    require(type(tree) is list and len(tree) == 4, "missing 3-adic alternative")
    check_tree(tree[0], active, groups, 15, stats)
    stats["no3_alternatives"] += 1
    for residue, entry in enumerate(tree[1:]):
        mode, proof = pair(entry)
        if mode == "coarse":
            kept = {k for k in active if k % 3 != residue}
            check_tree(proof, kept, restrict(groups, kept), 14, stats)
            stats["coarse_classes"] += 1
            continue
        require(mode == "exact" and type(proof) is list, "unknown 3-adic case")
        ordered = sorted(active)
        wanted = {hex(mask) for mask in maximal_masks(ordered, residue)}
        seen = set()
        for row in proof:
            tag, node = pair(row)
            require(type(tag) is str and tag in wanted - seen, "invalid 3-adic mask")
            seen.add(tag)
            mask = int(tag, 16)
            kept = {k for i, k in enumerate(ordered) if not mask >> i & 1}
            check_tree(node, kept, restrict(groups, kept), 14, stats)
            stats["refined_masks"] += 1
        require(seen == wanted, "missing 3-adic mask")
        stats["refined_classes"] += 1


def replay(variant, path):
    stats = Counter()
    with gzip.open(path, "rb") as source:
        for r in range(5):
            root_sets = [systems(variant, r, mask) for mask in range(256)]
            universe = set().union(*(system for cases in root_sets for system in cases))
            require(max(universe) == 5*(FIRST_M-1), "strict activation threshold")
            require(all(5*FIRST_M > k for k in universe), "nonpositive tail residual")
            catalog = catalogue(universe)
            for mask, cases in enumerate(root_sets):
                stats["directions"] += 1
                if variant == "no3_24":
                    closed = mask | ((mask >> 1) & (mask << 1) & 255)
                    require(root_sets[closed][0] <= cases[0], "invalid direction reduction")
                    if closed != mask:
                        continue
                record = parse(source.readline(MAX_BYTES+1))
                require(type(record) is list and len(record) == 3, "malformed direction")
                digit, bits, tree = record
                require(type(digit) is int and type(bits) is int and (digit, bits) == (r, mask),
                        "incorrect proof order or missing direction")
                if variant == "all15":
                    check_all(tree, cases[0], catalog, stats)
                else:
                    require(type(tree) is list and len(tree) == len(cases), "missing d=8 case")
                    for node, active in zip(tree, cases):
                        check_tree(node, active, restrict(catalog, active), 24, stats)
                stats["records"] += 1
        require(not source.read(1), "extra proof record")
    stats["min_margin"] = str(stats["min_margin"])
    return dict(stats)


def check_p80_control():
    data = parse((HERE / "global_p80_control.json").read_bytes())
    m, primes = data["m"], data["primes"]
    require(type(m) is int and m >= FIRST_M, "control activation")
    require(len(set(primes)) == len(primes) == 24, "control prime count")
    for p in primes:
        require(type(p) is int and p > 3 and p % 4 == 3 and
                all(p % i for i in range(2, isqrt(p)+1)), "control prime")
    cells = [(d, c) for d in range(8) for c in range(13) if (d, c) != (7, 12)]
    for d, c in cells + [(8, 0)]:
        residual = m - 5**d - 3**c
        require(residual > 0 and any(residual % p == 0 and residual % (p*p) for p in primes),
                "P(8,0) finite covering control failed")
    require(all((m - 5**8 - 3) % p for p in primes), "P(8,1) control must survive")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=VARIANTS)
    parser.add_argument("--proof-dir", type=Path, default=HERE)
    args = parser.parse_args()
    for variant in (args.variant,) if args.variant else VARIANTS:
        if variant == "no3_24":
            check_p80_control()
        print(json.dumps({"variant": variant, **replay(variant, args.proof_dir / f"global_{variant}.jsonl.gz")},
                         sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
