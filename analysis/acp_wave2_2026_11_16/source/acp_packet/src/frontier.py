#!/usr/bin/env python3
"""Phase 2B: the M = t frontier.

Part 1 (brute-force check of Lemma L4, "no full exponential curve"):
  for odd primes M and primes p = 1 (mod M), all cosets A = u*mu_M, B = u'*mu_M of the
  group mu_M of M-th roots of unity in F_p and all z:
      z  = 0 :  #{x in A, y in B : x+y = 0} is 0 or M                        (a full line)
      z != 0 :  #{x in A, y in B : x+y = z} <= (M-1)/2   if A != B,
                                             <= M-2       if A == B   (M >= 5),  <= M-1 always.
Part 2: census of M-active inert primes (M = 23, 29, 31, 37, 41, 43, 47): type V (M | h3 only),
  type H (M | h5 only), type B (both); exact maximal trace of a type-B curve on a fresh M-fibre.
Part 3: an explicit LOCAL exact tiling of one fresh 23-fibre by 23 vertical lines, and the exact
  reason it cannot persist: the set of lower points carrying the tiling lies in the intersection
  of the 23 projections G_p, each of Haar measure <= 1/m_p'.

usage: frontier.py weights.json out.json
"""
import sys, json
from math import gcd
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from arith import sieve, factorint, mult_order, odd_part, is_prime_td, prime_factors
from core_tools import load_weights

def mu(p, M):
    g = next(pow(a, (p - 1) // M, p) for a in range(2, p) if pow(a, (p - 1) // M, p) != 1)
    out, x = [], 1
    for _ in range(M):
        out.append(x); x = x * g % p
    return out

def coset_reps(p, M):
    """One representative of each coset of mu_M in F_p^*."""
    seen, reps = set(), []
    U = mu(p, M)
    for a in range(1, p):
        if a not in seen:
            reps.append(a)
            seen.update(a * u % p for u in U)
    return reps, U

import numpy as np

def curve_maxima(M, p):
    """max_z!=0 #{x in mu_M, y in r*mu_M : x+y=z} over cosets r*mu_M, split into
    (same coset as mu_M, different coset); also asserts the z = 0 count is 0 or M."""
    reps, U = coset_reps(p, M)
    Uset = set(U)
    Ua = np.array(U, dtype=np.int64)
    same = diff = 0
    for r in reps:
        s = ((Ua[:, None] + (r * Ua % p)[None, :]) % p).ravel()
        cnt = np.bincount(s, minlength=p)
        assert cnt[0] in (0, M)
        m = int(cnt[1:].max())
        if r in Uset: same = max(same, m)
        else: diff = max(diff, m)
    return same, diff

def lemma_check(M, p):
    same, diff = curve_maxima(M, p)
    assert diff <= (M - 1) // 2, (M, p, same, diff)
    assert same <= (M - 2 if M >= 5 else M - 1), (M, p, same, diff)
    return {"same": same, "diff": diff}

def main():
    rows = load_weights(sys.argv[1])
    out = {"lemma_L4": [], "census": {}, "local_tiling": {}}
    # ---------------- Part 1
    for M in (3, 5, 7, 11, 13, 17, 19, 23):
        cnt = 0
        for p in sieve(20000):
            if p % M == 1:
                r = lemma_check(M, p)
                out["lemma_L4"].append([M, p, r["same"], r["diff"]])
                cnt += 1
        worst_same = max(x[2] for x in out["lemma_L4"] if x[0] == M)
        worst_diff = max(x[3] for x in out["lemma_L4"] if x[0] == M)
        print(f"L4 check M={M}: {cnt} primes p=1 mod M; max curve size: same coset {worst_same} (bound {M-2 if M>=5 else M-1}), "
              f"different cosets {worst_diff} (bound {(M-1)//2})", flush=True)
    # ---------------- Part 2
    for M in (23, 29, 31, 37, 41, 43, 47):
        act = [r for r in rows if M in r["supp"]]
        V = [r for r in act if r["h3"] % M == 0 and r["h5"] % M != 0]
        Hh = [r for r in act if r["h3"] % M != 0 and r["h5"] % M == 0]
        Bo = [r for r in act if r["h3"] % M == 0 and r["h5"] % M == 0]
        curve = []
        for r in Bo:
            p = r["p"]
            if p > 70000:
                continue
            best_same, best_diff = curve_maxima(M, p)
            curve.append([p, r["h3"], r["h5"], best_same, best_diff])
        H1 = sorted(r["H"] for r in act)
        out["census"][M] = {"n_active": len(act), "V": [[r["p"], r["h3"], r["h5"]] for r in V],
                            "H": [[r["p"], r["h3"], r["h5"]] for r in Hh], "n_both": len(Bo),
                            "both_curve_max": curve, "smallest_H": H1[:8],
                            "sum_1_over_H_top_M": float(sum(F(1, h) for h in H1[:M]))}
        print(f"M={M}: {len(act)} active inert primes with H<B; type V: {len(V)}, type H: {len(Hh)}, both: {len(Bo)}; "
              f"sum of the M largest 1/H_p = {out['census'][M]['sum_1_over_H_top_M']:.4f}; "
              f"largest type-B curve (z!=0) on a fresh fibre: "
              f"{max((max(c[3], c[4]) for c in curve), default=0)} of {M} points", flush=True)
    # ---------------- Part 3: local tiling at M = 23 by vertical lines
    M = 23
    Vp = []
    p = 47
    while len(Vp) < M:
        if p % 4 == 3 and is_prime_td(p) and pow(3, (p - 1) // M, p) != 1 and pow(5, (p - 1) // M, p) == 1:
            f = factorint(p - 1)
            h3, h5 = odd_part(mult_order(3, p, f)), odd_part(mult_order(5, p, f))
            if h3 % (M * M) != 0:
                Vp.append((p, h3, h5))
        p += 2 * M
    c = (1, 0)
    lowmod = 1
    for p, h3, h5 in Vp:
        lowmod = lowmod * (h3 // M) // gcd(lowmod, h3 // M)
    assert gcd(lowmod, M) == 1
    astar, bstar = 0, 0
    targets = []
    for i, (p, h3, h5) in enumerate(Vp):
        # a_i = astar (mod lowmod), = i (mod 23)
        a_i = next(a for a in range(astar, astar + lowmod * M, lowmod) if a % M == i)
        z = (pow(3, c[0] + 2 * a_i, p) + pow(5, c[1] + 2 * bstar, p)) % p
        targets.append((p, z))
    # verify the exact partition of the fresh fibre over the lower point (astar mod lowmod ; bstar)
    ok = True
    for X in range(M):
        a = next(a for a in range(astar, astar + lowmod * M, lowmod) if a % M == X)
        for Y in range(M):
            # b = bstar in all coordinates except the 23-primary one, where it equals Y
            covers = []
            for (p, z), (_, h3, h5) in zip(targets, Vp):
                b = bstar  # type V: 5^beta mod p does not see the 23-primary coordinate (23 does not divide h5)
                assert h5 % M != 0
                if (pow(3, c[0] + 2 * a, p) + pow(5, c[1] + 2 * b, p)) % p == z:
                    covers.append(p)
            ok &= (covers == [Vp[X][0]])
    mprimes = [h3 // M for _, h3, _ in Vp]
    out["local_tiling"] = {"M": M, "class": "10", "primes": Vp, "targets": targets, "exact_partition": ok,
                           "m_p": mprimes, "min_1_over_m": str(F(1, max(mprimes))), "max_1_over_m": str(F(1, min(mprimes)))}
    print(f"local tiling at M=23: 23 type-V primes {Vp[0][0]}..{Vp[-1][0]}; exact partition of one fresh fibre: {ok}; "
          f"cofactors m_p = h3/23 range {min(mprimes)}..{max(mprimes)}  =>  the tiling survives on a set of lower points "
          f"of Haar measure <= 1/{max(mprimes)}", flush=True)
    assert ok
    json.dump(out, open(sys.argv[2], "w"))

if __name__ == "__main__":
    main()
