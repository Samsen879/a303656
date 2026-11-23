#!/usr/bin/env python3
"""Optional proof search. SciPy proposes weights. Only the integer replay is authoritative."""
import argparse
import functools
import gzip
import json
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


CASES = {
    # highest parent d, highest child c, budget for non-3 colors, include 3
    "no3_22": (6, 12, 22, False),
    "no3_23": (7, 12, 23, False),
    "all14_d7": (7, 13, 13, True),
    "all14_d6": (6, 14, 13, True),
}


def obligations(r, mask, dmax, child_c):
    roots = set()
    for d in range(dmax + 1):
        if mask & (1 << d):
            for e in (d, d + 1):
                for c in range(child_c + 1):
                    if c == 14 and e > 2:
                        continue
                    roots.add(5**e + 3**c - r)
        else:
            for c in range(12 if d == 7 else 13):
                roots.add(5 * (5**d + 3**c))
    return sorted(roots)


@functools.lru_cache(None)
def colors(delta):
    primes = []
    q = 3
    while q*q <= delta:
        if delta % q == 0:
            if q % 4 == 3 and q != 3:
                primes.append(q)
            while delta % q == 0:
                delta //= q
        q += 2
    if delta % 4 == 3 and delta != 3:
        primes.append(delta)
    return primes


def catalogue(roots):
    groups = defaultdict(set)
    for i, a in enumerate(roots):
        for j in range(i):
            diff = a - roots[j]
            while diff % 2 == 0:
                diff //= 2
            for p in colors(diff):
                groups[p, a % p].update((i, j))
    return [(p, k, sorted(v)) for (p, k), v in sorted(groups.items())]


def maximal3(roots):
    # An x follows one common-residue path. At a singleton one can
    # realize odd valuation at an arbitrarily large separating depth.
    def visit(indices, power, depth, killed):
        if len(indices) < 2:
            yield frozenset(killed.union(indices))
            return
        buckets = [set() for _ in range(3)]
        for i in indices:
            buckets[roots[i] // power % 3].add(i)
        for group in buckets:
            outside = indices - group if depth % 2 else set()
            yield from visit(group, power*3, depth+1, killed | outside)

    masks = sorted(set(visit(set(range(len(roots))), 1, 0, set())), key=len, reverse=True)
    result = []
    for mask in masks:
        if not any(mask <= other for other in result):
            result.append(mask)
    return sorted(result, key=lambda s: sum(1 << i for i in s))


def dual(active, classes, budget):
    # Give every class its own inequality. z[p] pays once for a color.
    indices = sorted(active)
    col = {i: j for j, i in enumerate(indices)}
    primes = sorted({p for p, _, _ in classes})
    zcol = {p: len(indices) + j for j, p in enumerate(primes)}
    rows, cols, data = [], [], []
    for row, (p, _, members) in enumerate(classes):
        for i in members:
            rows.append(row)
            cols.append(col[i])
            data.append(1)
        rows.append(row)
        cols.append(zcol[p])
        data.append(-1)
    objective = [-1] * len(indices) + [1] * len(primes)
    matrix = coo_matrix((data, (rows, cols)), shape=(len(classes), len(objective))).tocsr()
    fit = linprog(objective, A_ub=matrix, b_ub=np.ones(len(classes)),
                  bounds=[(0, 1)] * len(indices) + [(0, None)] * len(primes), method="highs")
    if not fit.success:
        raise RuntimeError(fit.message)
    if -fit.fun <= budget + 1e-8:
        return None
    for scale in (1, 2, 3, 4, 6, 12, 60, 420, 1000000):
        w = {i: min(scale, max(0, round(float(fit.x[col[i]]) * scale))) for i in indices}
        penalties = defaultdict(int)
        for p, _, members in classes:
            penalties[p] = max(penalties[p], sum(w[i] for i in members) - scale)
        if sum(w.values()) - sum(penalties.values()) > scale * budget:
            return [scale, [w[i] for i in indices]]
    return None


def solve(active, groups, budget, depth=0):
    if len(active) <= budget or depth > 12:
        raise RuntimeError(f"unclosed at depth {depth} with {len(active)} roots and budget {budget}")
    classes = []
    for p, k, members in groups:
        kept = [i for i in members if i in active]
        if len(kept) >= 2:
            classes.append((p, k, kept))
    leaf = dual(active, classes, budget)
    if leaf is not None:
        return leaf
    p = max(classes, key=lambda row: len(row[2]))[0]
    other = [row for row in classes if row[0] != p]
    children = [[None, solve(active, other, budget, depth+1)]]
    for color, k, members in classes:
        if color == p:
            children.append([k, solve(active.difference(members), other, budget-1, depth+1)])
    return [p, children]


def direction(r, mask, case):
    dmax, cmax, budget, with3 = CASES[case]
    roots = obligations(r, mask, dmax, cmax)
    groups = catalogue(roots)
    active = set(range(len(roots)))
    if not with3:
        return solve(active, groups, budget)
    # Try all root classes modulo 3 first, then refine only when needed.
    # Include 3 in a palette of size 14, with 13 other colors left.
    # For a palette omitting 3 we need a separate budget-14 proof.
    result = [solve(active, groups, 14)]
    masks = None
    for k in range(3):
        coarse = {i for i in active if roots[i] % 3 == k}
        try:
            result.append(["coarse", solve(active - coarse, groups, budget)])
        except RuntimeError:
            if masks is None:
                masks = maximal3(roots)
            cases = [m for m in masks if m <= coarse and m]
            result.append(["exact", [[hex(sum(1 << i for i in m)), solve(active-m, groups, budget)]
                                     for m in cases]])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    orientations = 1 << (CASES[options.case][0] + 1)
    with tempfile.TemporaryDirectory(dir=options.output.parent) as stage:
        path = Path(stage) / "proof.gz"
        with path.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
            for r in range(5):
                for mask in range(orientations):
                    try:
                        proof = direction(r, mask, options.case)
                    except Exception as exc:
                        raise RuntimeError((options.case, r, mask)) from exc
                    out.write((json.dumps([r, mask, proof], separators=(",", ":")) + "\n").encode())
                print(options.case, "completed r", r, flush=True)
        path.replace(options.output)


if __name__ == "__main__":
    main()
