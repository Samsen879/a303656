#!/usr/bin/env python3
"""Exact row-local information ablation, with a sweep DP and set oracle.

Inputs are complete arithmetic masks; retained subsets omit information only.
The bridge diagnostic is separate from sufficient-gate evaluation.
"""
from __future__ import annotations

from itertools import combinations

from ajt5_gates import MAX_M, forbidden36
from verify_ajt5_reports import exponents, integer, powers, require


def domain(m, d, e):
    integer(m, 2, MAX_M, "campaign m")
    L = len(powers(5, m)) - 1
    integer(d, 1, (1 << (L + 1)) - 1, "nonempty parent mask")
    integer(e, 0, (1 << (L + 2)) - 1, "child mask")
    F = sum(1 << i for i in forbidden36(m, L))
    require(not d & F, "parent contradicts mod36 negatives")
    return L, F


def optimum_dp(m, d, e):
    """Return minimal deletion cost and EVERY tied pair of retained masks.

    At sweep i, finalize S_i and Q_(i-1). Equal states have identical possible
    suffixes; discard only a strictly more costly prefix at that same state.
    Every equal-cost prefix is retained, so this also reconstructs all ties.
    No cost cutoff, expected value, or heuristic early exit is used.
    """
    L, F = domain(m, d, e)
    # previous A/B bits, nonempty A flag, |S|+|B|, reduced parity counts.
    states = {(0, 0, False, 0, 0, 0): (0, {(0, 0)})}
    for i in range(L + 2):
        updated = {}
        for (ap, bp, used, total, h0, h1), (cost, paths) in states.items():
            for a in range(1 + int(bool(d & (1 << i)))):
                for b in range(1 + int(bool(e & (1 << i)))):
                    hs = [h0, h1]
                    if i:
                        # |A_b|+|Q_b|-|U_b|+|(F\Q)_b| equals
                        # |A_b|+|(Q\F)_b|-|(U\F)_b|.
                        blocked = bool(F & (1 << (i - 1)))
                        hs[(i - 1) % 2] += ap + (int(bool(bp or b)) - 1) * (not blocked)
                    key = (a, b, used or bool(a), total + int(bool(ap or a)) + b, *hs)
                    newcost = cost + int(bool(d & (1 << i))) - a + int(bool(e & (1 << i))) - b
                    oldcost, oldpaths = updated.get(key, (10**9, set()))
                    if newcost <= oldcost:
                        newpaths = {(x | (a << i), y | (b << i)) for x, y in paths}
                        updated[key] = (newcost, newpaths | oldpaths if newcost == oldcost else newpaths)
        states = updated
    feasible = [(cost, paths) for (_, _, used, total, h0, h1), (cost, paths) in states.items()
                if used and total <= L + 2 and h0 <= 0 and h1 <= 0]
    require(bool(feasible), "no row-local feasible ablation")
    best = min(cost for cost, _ in feasible)
    return best, sorted(set().union(*(paths for cost, paths in feasible if cost == best)))


def subsets(values):
    values = sorted(values)
    for count in range(len(values) + 1):
        for choice in combinations(values, count):
            yield set(choice)


def literal_margins(m, A, B):
    L = len(powers(5, m)) - 1
    U, V = set(range(L + 1)), set(range(L + 2))
    Q, S = (B | {b - 1 for b in B}) & U, A | {a + 1 for a in A}
    F = forbidden36(m, L)
    h = []
    for parity in (0, 1):
        Ub = {i for i in U if i % 2 == parity}
        h.append(len(A & Ub) + len(Q & Ub) - len(Ub) + len((F - Q) & Ub))
    return len(S) + len(B) - len(V), h


def optimum_enumeration(m, d, e):
    """Independent oracle: visit the full Cartesian product using literal sets.

    No DP state, pruning, prefix costs or bit margin arithmetic is shared.
    """
    domain(m, d, e)
    D, E, best, tied = exponents(d), exponents(e), None, []
    for A in subsets(D):
        if not A:
            continue
        for B in subsets(E):
            gf, hs = literal_margins(m, A, B)
            if gf <= 0 and all(h <= 0 for h in hs):
                cost = len(D - A) + len(E - B)
                pair = (sum(2**a for a in A), sum(2**b for b in B))
                if best is None or cost < best:
                    best, tied = cost, [pair]
                elif cost == best:
                    tied.append(pair)
    require(best is not None, "no oracle feasible ablation")
    return best, sorted(tied)


def diagnostics(m, d, e, a, b):
    """Actual bridge and recovery diagnostics require exact D/E complements."""
    L, Fmask = domain(m, d, e)
    A, B, D, E, F = map(exponents, (a, b, d, e, Fmask))
    require(bool(A) and A <= D and B <= E, "retained subset binding")
    U, V = set(range(L + 1)), set(range(L + 2))
    N, H = U - D, V - E  # never complements of the retained subsets
    Q, S = (B | {j - 1 for j in B}) & U, A | {j + 1 for j in A}
    gf, h = literal_margins(m, A, B)
    hn = [len(A & {i for i in U if i % 2 == p}) + len(Q & {i for i in U if i % 2 == p})
          - len({i for i in U if i % 2 == p}) + len((N - Q) & {i for i in U if i % 2 == p})
          for p in (0, 1)]
    gfh = gf + len(H - S)
    gaps = []
    for w in ({i: i + 1 if i % 2 else 0 for i in U},
              {i: L + 1 - i if i % 2 else 0 for i in U}):
        gaps.append(sum(w[i] for i in A) + sum(w[i] for i in Q - F) - sum(w[i] for i in U - F))
    edges = [(i, j) for i in sorted(A) for j in sorted(B) if j in (i, i + 1)]
    return {"gF": gf, "h": h, "bridge": bool(edges), "edges": edges,
            "parent_negative_margins": hn, "gFH": gfh, "weight_gaps": gaps}
