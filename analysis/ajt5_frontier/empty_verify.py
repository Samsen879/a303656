#!/usr/bin/env python3
"""Replay the EMPTY_D exclusion, finite boundary and adversarial controls with integers."""
import argparse
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from ajt5_integer_certificates import parse
from verify_ajt5_palette import pair, require, trial_primes

BOUNDARY = 547066


def catalogue(roots):
    """Enumerate all primes small enough to divide a nonzero difference."""
    classes = {}
    for p in trial_primes(max(roots) - min(roots)):
        if p == 3 or p % 4 != 3:
            continue
        by_residue = defaultdict(list)
        for root in roots:
            by_residue[root % p].append(root)
        multi = {a: set(group) for a, group in by_residue.items() if len(group) > 1}
        if multi:
            classes[p] = multi
    return classes


def valuation3(n):
    require(n != 0, "v3(0) undefined")
    h = 0
    while n % 3 == 0:
        n //= 3
        h += 1
    return h


def masks(roots):
    depth = max(valuation3(b-a) for a, b in combinations(roots, 2))
    samples = set(roots)
    for a in roots:
        for h in range(depth + 3):
            samples.update((a + 3**h, a + 2*3**h))
    raw = {sum(1 << i for i, a in enumerate(roots) if a != x and valuation3(x-a) % 2)
           for x in samples}
    maximal = {m for m in raw if not any(m != n and (m & n) == m for n in raw)}
    return raw, maximal


def check_tree(node, live, available, budget, stats, margins):
    key, payload = pair(node)
    require(type(key) is int and type(payload) is list and payload, "bad proof node")
    if type(payload[0]) is int:
        scale = key
        require(scale > 0 and len(payload) == len(live), "incorrect weight dimensions")
        require(all(type(w) is int and 0 <= w <= scale for w in payload), "bad weight")
        weights = dict(zip(sorted(live), payload))
        penalty = 0
        for classes in available.values():
            best = max(sum(weights[a] for a in group if a in weights) for group in classes.values())
            penalty += max(0, best - scale)
        margin = Fraction(sum(payload) - penalty, scale) - budget
        require(margin > 0, "non-strict EMPTY_D leaf")
        margins.append(margin)
        stats["leaves"] += 1
        return

    p = key
    require(p in available, "invalid branch prime")
    groups = {k: hit for k, block in available[p].items() if len(hit := live & block) >= 2}
    require(groups, "no multiroot branch")
    other = available.copy()
    del other[p]
    required = set(groups) | {None}
    for entry in payload:
        residue, child = pair(entry)
        require(residue is None or type(residue) is int, "bad residue type")
        require(residue in required, "unexpected or repeated branch")
        required.remove(residue)
        if residue is None:
            # A palette may omit p. The full remaining budget is still available.
            check_tree(child, live, other, budget, stats, margins)
        else:
            check_tree(child, live - groups[residue], other, budget-1, stats, margins)
    require(not required, "incomplete residue/default branches")
    stats["branches"] += 1


def replay(proof):
    rows = {(d, c): 5**d + 3**c for d in range(8) for c in range(13) if (d, c) != (7, 12)}
    roots = sorted(set(rows.values()))
    require(len(rows) == 103 and len(roots) == 102 and max(roots) == BOUNDARY, "window")
    require(type(proof) is dict and set(proof) == {"no3", "with3"}, "unknown proof fields")
    classes = catalogue(roots)
    raw, wanted = masks(roots)
    stats = Counter(labels=len(rows), roots=len(roots), multiroot_primes=len(classes),
                    raw_3_masks=len(raw), maximal_3_masks=len(wanted))
    margins = []
    check_tree(proof["no3"], set(roots), classes, 16, stats, margins)
    require(type(proof["with3"]) is list, "bad mask list")
    for entry in proof["with3"]:
        tag, tree = pair(entry)
        require(type(tag) is str, "bad mask tag")
        mask = int(tag, 16)
        require(tag == hex(mask) and mask in wanted, "unexpected or repeated 3-mask")
        wanted.remove(mask)
        live = {a for i, a in enumerate(roots) if not (mask >> i) & 1}
        check_tree(tree, live, classes, 15, stats, margins)
    require(not wanted, "missing maximal 3-mask")
    return dict(stats, minimum_margin=str(min(margins)))


def finite_boundary(limit):
    # Bit k denotes an actual representation. Enumerate square pairs including zero.
    squares = bytearray(limit // 8 + 1)
    for b in range(isqrt(limit) + 1):
        for a in range(min(b, isqrt(limit - b*b)) + 1):
            k = a*a + b*b
            squares[k // 8] |= 1 << (k % 8)
    s2 = int.from_bytes(squares, "little")
    triples = 0
    power = 1
    while power < limit:
        triples |= s2 << power
        power *= 3
    represented = 0
    power = 1
    while power < limit:
        represented |= triples << power
        power *= 5
    expected = (1 << (limit+1)) - 4  # ones at 2,...,limit
    require(represented & expected == expected, "unrepresented x in finite interval")
    return expected.bit_count()


def adversarial_control():
    roots = [0, 11, 77]
    for root in roots:
        residual = 143 - root
        require(residual % 11 == 0 and residual % 121 != 0, "synthetic cover failed")
    # At 7:0 we can remove {0,77}. At None the 11-class still covers all three.
    # A verifier charging None would accept this false tree with budget one.
    forged = [7, [[None, [1, [1, 0, 0]]], [0, [1, [1]]]]]
    try:
        check_tree(forged, set(roots), catalogue(roots), 1, Counter(), [])
    except ValueError as exc:
        require(str(exc) == "non-strict EMPTY_D leaf", "unexpected reason for rejection")
    else:
        raise ValueError("false cover exclusion accepted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proof", nargs="?", type=Path, default=Path(__file__).with_name("empty_proof.json"))
    proof = parse(parser.parse_args().proof.read_bytes())
    result = replay(proof)
    result["finite_represented"] = finite_boundary(BOUNDARY)
    adversarial_control()
    result["none_mutant"] = "rejected"
    print(json.dumps(result, sort_keys=True))
