#!/usr/bin/env python3
"""Direct budgets for the C21/C22-type induction with a COMPLETE catalogue
(all inert primes with H_p < B, any order structure) and exact per-class weights.

For a parity class c, a prime M and K targets the critical budget is
   D_c(M, t, K) = C_M^c + I_M^c(K - t) + A_M^c(t),      M <= t <= K,
   C_M^c = sum_{7 <= q <= M, q = 3 mod 4} m_q^c     (core: unit conditions at regular norm primes)
   A_M^c(t) = sum of the t largest m_p^c among  p > M, P^+(L_p) = M   (plus placeholders tau)
   I_M^c(k) = sum of the k largest m_p^c among  p > M, P^+(L_p) < M   (plus placeholders tau)
and the base budget is  D_c(M0, K) = C_M0^c + top_K{ m_p^c : p > M0, P^+(L_p) <= M0 }.
Here m_p^c is an upper bound for max_z mu(F_p^c(z)); for mu = Haar it is the exact weight.
Unknown primes (H_p >= B) get the placeholder tau >= sup of their mass.

usage: root_budget.py weights.json [Kmax]
"""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from core_tools import load_weights, CL
from arith import sieve

def Pplus(r):
    return max(r["supp"])

def budgets(rows, cs, K, tau, mass, M0=7, core_bonus=None):
    """Return dict of all budgets needed for the K-target theorem in class cs."""
    out = {}
    top = lambda ws, k: sum(sorted(ws + [tau] * k, reverse=True)[:k], F(0))
    core = lambda M: sum((mass(r) for r in rows if r["p"] <= M), F(0)) - (core_bonus(M) if core_bonus else 0)
    out[("base", M0)] = core(M0) + top([mass(r) for r in rows if r["p"] > M0 and Pplus(r) <= M0], K)
    for M in sieve(K):
        if M <= M0:
            continue
        cM = core(M)
        act = [mass(r) for r in rows if r["p"] > M and Pplus(r) == M]
        ina = [mass(r) for r in rows if r["p"] > M and Pplus(r) < M]
        for t in range(M, K + 1):
            out[(M, t)] = cM + top(act, t) + top(ina, K - t)
    return out

def main():
    rows = load_weights(sys.argv[1])
    B = max(r["H"] for r in rows) + 1
    B = 1 << (B - 1).bit_length()
    tau = F(1, B)
    Kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    for cs in CL:
        mass = lambda r: F(r["cls"][cs]["maxN"], r["h3"] * r["h5"])
        best = None
        for K in range(22, Kmax + 1):
            b = budgets(rows, cs, K, tau, mass)
            worst = max(b, key=b.get)
            if b[worst] < 1:
                best = (K, worst, float(b[worst]))
            else:
                print(f"class {cs}: Haar budgets hold up to K={best[0]} (worst {best[1]} = {best[2]:.4f}); "
                      f"fail at K={K}: {worst} = {float(b[worst]):.4f}")
                break
        else:
            print(f"class {cs}: budgets hold up to K={Kmax}", best)

if __name__ == "__main__":
    main()
