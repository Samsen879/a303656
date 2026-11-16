#!/usr/bin/env python3
"""Exact verifier for Theorem R (K-target theorem), independent of root_budget.py / search code.

For every parity class c it checks, in integer arithmetic (unit = 1e-15, all masses rounded UP):
    base:   C_7 + top_K{ m_p : p > 7, P^+(L_p) <= 7 }                                   < 1
    (M,t):  C_M + top_t{ m_p : p > M, P^+(L_p) = M } + top_{K-t}{ m_p : p > M, P^+(L_p) < M } < 1
            for every prime 7 < M <= K and every t with M <= t <= K,
where C_M = sum of m_q over all inert primes 7 <= q <= M, the pools contain every catalogue
prime (complete for H_p < B) and infinitely many placeholders tau = rho_max / B for the primes
outside the catalogue.  m_p is an upper bound for max_z mu(F_p^c(z)), mu = nu0 x Haar
(nu0 = uniform reproduces the plain Haar budgets).

usage: verify_root_budget.py weights.json K out.json cert_c00.json cert_c01.json cert_c10.json cert_c11.json
       verify_root_budget.py weights.json K out.json haar
"""
import sys, json, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from core_tools import load_weights, fibre_cell_table
import masses_under_nu

UNIT = 10 ** 15

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

def up(fr):
    return -((-fr.numerator * UNIT) // fr.denominator)   # ceil(fr * UNIT)

def cross_check_mass(r, cert, claimed):
    """Recompute max_z mu(F) with plain Python integers (no numpy) for one prime."""
    N0, cs = cert["N0"], cert["class"]
    nu0 = cert["nu0"]
    p, h3, h5 = r["p"], r["h3"], r["h5"]
    from math import gcd
    g3, g5 = gcd(h3, N0), gcd(h5, N0)
    marg = [[sum(nu0[x][y] for x in range(u, N0, g3) for y in range(v, N0, g5)) for v in range(g5)] for u in range(g3)]
    tot = sum(map(sum, nu0))
    A = [pow(3, int(cs[0]) + 2 * i, p) for i in range(h3)]
    Bv = [pow(5, int(cs[1]) + 2 * j, p) for j in range(h5)]
    acc = {}
    for i, x in enumerate(A):
        row = marg[i % g3]
        for j, y in enumerate(Bv):
            z = (x + y) % p
            acc[z] = acc.get(z, 0) + row[j % g5]
    assert F(max(acc.values()) * g3 * g5, tot * h3 * h5) == claimed, p

def main():
    rows = load_weights(sys.argv[1]); K = int(sys.argv[2]); outp = sys.argv[3]
    haar = (sys.argv[4] == "haar")
    Bcut = max(r["H"] for r in rows) + 1
    B = 1 << (Bcut - 1).bit_length()
    assert all(r["p"] % 4 == 3 and r["p"] > 3 for r in rows)
    primesM = [M for M in range(11, K + 1) if is_prime(M)]
    assert K < 2 * B, "core primes must lie inside the catalogue"
    report = {"K": K, "B": B, "mode": "haar" if haar else "nu0 x Haar", "classes": {}}
    for idx, cs in enumerate(["00", "01", "10", "11"]):
        t0 = time.time()
        if haar:
            mass = {r["p"]: F(r["cls"][cs]["maxN"], r["h3"] * r["h5"]) for r in rows}
            rho_max = F(1)
        else:
            cert = json.load(open(sys.argv[4 + idx]))
            assert cert["class"] == cs
            m, rho_max = masses_under_nu.compute(rows, cert, verbose=False)
            mass = {p: v[0] for p, v in m.items()}
            small = [r for r in rows if m[r["p"]][1] == "exact" and r["h3"] * r["h5"] <= 40000]
            for r in small:
                cross_check_mass(r, cert, mass[r["p"]])
        tau = up(rho_max / B)
        mi = {r["p"]: up(mass[r["p"]]) for r in rows}
        Pp = {r["p"]: max(r["supp"]) for r in rows}
        def pool(pred):
            ws = sorted((mi[p] for p in mi if pred(p)), reverse=True)
            ws = [w for w in ws if w > tau]           # entries <= tau are dominated by placeholders
            pre = [0]
            for w in ws: pre.append(pre[-1] + w)
            return pre
        def top(pre, k):
            n = len(pre) - 1
            return pre[k] if k <= n else pre[n] + (k - n) * tau
        worst = (sum(mi[p] for p in mi if p <= 7) + top(pool(lambda p: p > 7 and Pp[p] <= 7), K), "base")
        nb = 1
        for M in primesM:
            core = sum(mi[p] for p in mi if p <= M)
            act = pool(lambda p: p > M and Pp[p] == M)
            ina = pool(lambda p: p > M and Pp[p] < M)
            for t in range(M, K + 1):
                v = core + top(act, t) + top(ina, K - t)
                nb += 1
                if v > worst[0]:
                    worst = (v, [M, t])
        ok = worst[0] < UNIT
        report["classes"][cs] = {"n_budgets": nb, "worst_budget": worst[0] / UNIT, "worst_at": worst[1],
                                 "rho_max": float(rho_max), "tau": tau / UNIT, "status": "PASS" if ok else "FAIL",
                                 "cross_checked_primes": 0 if haar else len(small)}
        print(f"class {cs}: {nb} budgets, worst {worst[0]/UNIT:.6f} at {worst[1]}  tau={tau/UNIT:.3e}  "
              f"{'PASS' if ok else 'FAIL'} [{time.time()-t0:.0f}s]", flush=True)
    report["status"] = "PASS" if all(v["status"] == "PASS" for v in report["classes"].values()) else "FAIL"
    json.dump(report, open(outp, "w"), indent=1)
    print("K =", K, report["status"])
    assert report["status"] == "PASS"

if __name__ == "__main__":
    main()
