#!/usr/bin/env python3
"""Independent standard-library checks for the Thread 3 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path


def convolve(a: list[int], b: list[int], n: int) -> list[int]:
    out = [0] * (n + 1)
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b[: n + 1 - i]):
            if bj:
                out[i + j] += ai * bj
    return out


def theta(n: int) -> list[int]:
    out = [0] * (n + 1)
    r = math.isqrt(n)
    for a in range(-r, r + 1):
        out[a * a] += 1
    return out


def lacunary(base: int, scale: int, n: int) -> list[int]:
    out = [0] * (n + 1)
    x = scale
    while x <= n:
        out[x] += 1
        x *= base
    return out


def series_H(u: int, v: int, n: int) -> list[int]:
    t = convolve(theta(n), theta(n), n)
    return convolve(convolve(t, lacunary(3, 5**u, n), n), lacunary(5, 9**v, n), n)


def dilate(a: list[int], k: int, n: int) -> list[int]:
    out = [0] * (n + 1)
    for i, value in enumerate(a):
        if k * i > n:
            break
        out[k * i] = value
    return out


def direct_F(n: int) -> list[int]:
    out = [0] * (n + 1)
    p3, p5 = [], []
    x = 1
    while x <= n:
        p3.append(x)
        x *= 3
    x = 1
    while x <= n:
        p5.append(x)
        x *= 5
    r = math.isqrt(n)
    for a in range(-r, r + 1):
        aa = a * a
        for b in range(-r, r + 1):
            q = aa + b * b
            if q > n:
                continue
            for x3 in p3:
                for x5 in p5:
                    s = q + x3 + x5
                    if s <= n:
                        out[s] += 1
    return out


def auxiliary_sections(n: int) -> tuple[list[int], list[int], list[int]]:
    t = convolve(theta(n), theta(n), n)
    # G_e exponent weights are halved; retain only even total power shifts.
    ge2 = [0] * (n + 1)
    for q, tq in enumerate(t):
        if not tq:
            continue
        x3 = 1
        while q + (x3 + 1) // 2 <= n:
            x5 = 1
            while q + (x3 + x5) // 2 <= n:
                ge2[q + (x3 + x5) // 2] += tq
                x5 *= 5
            x3 *= 3

    th = theta(n)
    U = [0] * (n + 1)
    r = math.isqrt(n) + 2
    for z in range(-r - 1, r + 1):
        e = z * (z + 1)
        if 0 <= e <= n:
            U[e] += 1
    base = convolve(th, U, n)
    g1 = [0] * (n + 1)
    g3 = [0] * (n + 1)
    for q, bq in enumerate(base):
        if not bq:
            continue
        p9 = 1
        while q + (3 * p9 + 1) // 4 <= n:
            p5 = 1
            while q + (3 * p9 + p5) // 4 <= n:
                g1[q + (3 * p9 + p5) // 4] += bq
                p5 *= 5
            p9 *= 9
        p9 = 1
        while q + (p9 - 1) // 4 <= n:
            p5 = 1
            while q + (p9 + p5 - 2) // 4 <= n:
                g3[q + (p9 + p5 - 2) // 4] += bq
                p5 *= 5
            p9 *= 9
    return ge2, g1, g3


def check_grid(limit: int) -> dict:
    results = []
    t = convolve(theta(limit), theta(limit), limit)
    d5 = [x - y for x, y in zip(t, dilate(t, 5, limit))]
    d9 = [x - y for x, y in zip(t, dilate(t, 9, limit))]
    for u in range(3):
        for v in range(3):
            huv = series_H(u, v, limit)
            hu1v = series_H(u + 1, v, limit)
            huv1 = series_H(u, v + 1, limit)
            l3next = lacunary(3, 5 ** (u + 1), limit)
            l5next = lacunary(5, 9 ** (v + 1), limit)
            shifted_t = [0] * (limit + 1)
            shift = 9**v
            for i, value in enumerate(t[: limit + 1 - shift]):
                shifted_t[i + shift] = value
            e5a = convolve(shifted_t, l3next, limit)
            e5b = convolve(convolve(d5, l3next, limit), lacunary(5, 5 * 9**v, limit), limit)
            e5 = [x + y for x, y in zip(e5a, e5b)]
            rhs5 = [x + y for x, y in zip(dilate(huv, 5, limit), e5)]

            short3 = [0] * (limit + 1)
            for exponent in (5**u, 3 * 5**u):
                if exponent <= limit:
                    short3[exponent] += 1
            e9a = convolve(convolve(t, short3, limit), l5next, limit)
            e9b = convolve(convolve(d9, lacunary(3, 9 * 5**u, limit), limit), l5next, limit)
            e9 = [x + y for x, y in zip(e9a, e9b)]
            rhs9 = [x + y for x, y in zip(dilate(huv, 9, limit), e9)]
            ok5 = hu1v == rhs5 and min(e5) >= 0
            ok9 = huv1 == rhs9 and min(e9) >= 0
            results.append({"u": u, "v": v, "B2_exact_and_nonnegative": ok5, "B4_exact_and_nonnegative": ok9})
    return {"cases": results, "all_pass": all(x["B2_exact_and_nonnegative"] and x["B4_exact_and_nonnegative"] for x in results)}


def check_catalogue_identities() -> dict:
    checked = 0
    for a in range(-8, 9):
        for b in range(-8, 9):
            for c in range(5):
                for d in range(5):
                    n = a * a + b * b + 3**c + 5**d
                    assert 5 * n - 4 * 3**c == (a - 2*b)**2 + (2*a + b)**2 + 3**c + 5**(d+1)
                    assert 9 * n - 8 * 5**d == (3*a)**2 + (3*b)**2 + 3**(c+2) + 5**d
                    assert 25 * n - 24 * 3**c == (3*a - 4*b)**2 + (4*a + 3*b)**2 + 3**c + 5**(d+2)
                    checked += 3
            for s in (Fraction(-3, 2), Fraction(-1, 1), Fraction(0), Fraction(2, 3)):
                den = 1 + s*s
                x = ((1-s*s)*a - 2*s*b) / den
                y = (2*s*a + (1-s*s)*b) / den
                assert x*x + y*y == a*a + b*b
                checked += 1
    return {"exact_evaluations": checked, "pass": True}


def check_nonlinear_theta(limit: int) -> dict:
    phi = theta(limit)
    psi = [0] * (limit + 1)
    j = 0
    while j * (j + 1) // 2 <= limit:
        psi[j * (j + 1) // 2] += 1
        j += 1
    b15_rhs = dilate(phi, 4, limit)
    psi8 = dilate(psi, 8, limit)
    for i in range(limit):
        if psi8[i]:
            b15_rhs[i + 1] += 2 * psi8[i]
    b16_lhs = convolve(psi, psi, limit)
    b16_rhs = convolve(phi, dilate(psi, 2, limit), limit)
    return {"checked_through": limit, "B15": phi == b15_rhs, "B16": b16_lhs == b16_rhs, "all_pass": phi == b15_rhs and b16_lhs == b16_rhs}


def check_sections(limit: int) -> dict:
    f = direct_F(4 * limit + 3)
    ge, g1, g3 = auxiliary_sections(limit)
    even = all(f[2 * m] == ge[m] for m in range(limit + 1) if 2 * m < len(f))
    one = all(f[4 * m + 1] == 2 * g1[m] for m in range(limit + 1) if 4 * m + 1 < len(f))
    three = all(f[4 * m + 3] == 2 * g3[m] for m in range(limit + 1) if 4 * m + 3 < len(f))
    return {"m_max": limit, "even": even, "one_mod_4": one, "three_mod_4": three, "all_pass": even and one and three}


def affine_norm_search(coeff_bound: int) -> dict:
    # Exhaust affine integer A,B of coefficient size <=B. Record all identities
    # A(a,b)^2+B(a,b)^2=K(a^2+b^2)+eta by exact coefficient comparison.
    identities = []
    vals = range(-coeff_bound, coeff_bound + 1)
    for au in vals:
        for av in vals:
            for ac in vals:
                for bu in vals:
                    for bv in vals:
                        for bc in vals:
                            cross = 2 * (au * av + bu * bv)
                            lina = 2 * (au * ac + bu * bc)
                            linb = 2 * (av * ac + bv * bc)
                            ka = au * au + bu * bu
                            kb = av * av + bv * bv
                            if cross == lina == linb == 0 and ka == kb and ka > 0:
                                identities.append({"A": [au, av, ac], "B": [bu, bv, bc], "K": ka, "eta": ac * ac + bc * bc})
    nonzero_eta = [x for x in identities if x["eta"] != 0]
    return {"coefficient_bound": coeff_bound, "identity_count": len(identities), "nonzero_eta_count": len(nonzero_eta), "pass": not nonzero_eta}


def explore_toy_system(max_x: int) -> dict:
    # Fixed finite multipliers with an intentional duplicate and two states.
    # Each edge carries q -> Kq; indices are q+3^c+5^d. This isolates the
    # multiplier/path-count mechanism independently of packet code.
    multipliers = [2, 2, 3]
    seeds = {(0, 1), (1, 2)}  # state, positive norm
    seen = set(seeds)
    todo = deque(seeds)
    while todo:
        state, q = todo.popleft()
        for edge, k in enumerate(multipliers):
            nxt = ((state + edge + 1) % 2, k * q)
            if nxt[1] <= max_x and nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    reach = set()
    for state, q in seen:
        p3 = 1
        while q + p3 + 1 <= max_x:
            p5 = 1
            while q + p3 + p5 <= max_x:
                reach.add(q + p3 + p5)
                p5 *= 5
            p3 *= 3
    # A K=1 identity transition would make a graph cycle, but no new witness.
    graph = {0: [1], 1: [0]}
    colors = {node: 0 for node in graph}

    def visit(node: int) -> bool:
        colors[node] = 1
        for nxt in graph[node]:
            if colors[nxt] == 1 or (colors[nxt] == 0 and visit(nxt)):
                return True
        colors[node] = 2
        return False

    cycle_detected = any(colors[node] == 0 and visit(node) for node in graph)
    return {
        "X": max_x,
        "distinct_state_norms": len(seen),
        "reachable_original_indices": len(reach),
        "density": len(reach) / max_x,
        "duplicate_multiplier_deduplicated": True,
        "excluded_K1_cycle_detected": cycle_detected,
    }


def check_affine_tail() -> dict:
    worst = Fraction(0)
    witnesses = []
    # Exhaust words up to length 9 with K in {2,3,5}, R in {-3,...,3}.
    states = [(Fraction(0), 1, [])]  # normalized displacement, product, word
    for _ in range(9):
        nxt = []
        for disp, prod, word in states:
            for k in (2, 3, 5):
                for r in range(-3, 4):
                    nd = disp + Fraction(r, prod * k)
                    np = prod * k
                    nw = word + [(k, r)]
                    if abs(nd) > worst:
                        worst = abs(nd)
                        witnesses = nw
                    nxt.append((nd, np, nw))
        # Keep only extrema for each product to prevent exponential storage.
        bucket = {}
        for item in nxt:
            key = item[1]
            if key not in bucket:
                bucket[key] = [item, item]
            else:
                if item[0] < bucket[key][0][0]: bucket[key][0] = item
                if item[0] > bucket[key][1][0]: bucket[key][1] = item
        states = [x for pair in bucket.values() for x in pair]
    return {"R_max": 3, "max_abs_normalized_displacement": str(worst), "bound": 3, "pass": worst <= 3, "witness_word": witnesses}


def digest_ints(values: list[int]) -> str:
    return hashlib.sha256(",".join(map(str, values)).encode()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1200)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not 100 <= args.limit <= 5000:
        raise SystemExit("limit must be in [100,5000]")
    f = direct_F(args.limit)
    checks = {
        "implementation": "independent standard-library verifier; packet code not imported",
        "parameters": {"limit": args.limit},
        "coefficient_sanity": {
            "f_0": f[0], "f_1": f[1], "f_2": f[2],
            "hash": digest_ints(f),
            "pass": (f[0], f[1], f[2]) == (0, 0, 1),
        },
        "catalogue_identities": check_catalogue_identities(),
        "positive_grid": check_grid(args.limit),
        "binary_sections": check_sections(args.limit // 4),
        "nonlinear_theta": check_nonlinear_theta(args.limit),
        "affine_nonzero_defect_search": affine_norm_search(2),
        "affine_tail_bound": check_affine_tail(),
        "toy_finite_state_reach": explore_toy_system(args.limit),
    }
    pass_fields = [
        checks["coefficient_sanity"]["pass"],
        checks["catalogue_identities"]["pass"],
        checks["positive_grid"]["all_pass"],
        checks["binary_sections"]["all_pass"],
        checks["nonlinear_theta"]["all_pass"],
        checks["affine_nonzero_defect_search"]["pass"],
        checks["affine_tail_bound"]["pass"],
    ]
    checks["status"] = "PASS" if all(pass_fields) else "FAIL"
    args.output.write_text(json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": checks["status"], "output": str(args.output), "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
