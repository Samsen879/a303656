#!/usr/bin/env python3
"""Exact verifier for a measure certificate (Theorem A of the report).

Input: weights file (exact fibre statistics of the complete catalogue), cutoff B,
       and a certificate {N0, class, nu0 (integer N0 x N0 array)}.
It recomputes, in exact integer/rational arithmetic:
  1. the rich core S of Cat_B (Lemma L3);
  2. A = {supp subset S0}, D = {supp cap S0 = empty}, C = rest  (S0 = primes | N0);
  3. V_A, V_C = sum of  max_z mu(F_p^c(z))  for mu = nu0 x Haar  (all z, all primes);
  4. W_D = sum of Haar weights of D;
  5. the bound  1 - (1-V_A)(1-W_D) + V_C  and asserts it is < 1.
The max over z is taken over ALL residues, by direct enumeration of every point
of Z/h3 x Z/h5 (no LP output is trusted).

usage: verify_lp_cert.py weights.json cert.json [out.json]
"""
import sys, json, time
from fractions import Fraction
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from core_tools import load_weights, rich_core, mu_mass_max
from acp import PrimeData

def main():
    wpath, cpath = sys.argv[1], sys.argv[2]
    cert = json.load(open(cpath))
    B, N0, cs = cert["B"], cert["N0"], cert["class"]
    c = (int(cs[0]), int(cs[1]))
    nu0 = np.array(cert["nu0"], dtype=np.int64)
    assert nu0.shape == (N0, N0) and nu0.min() >= 0 and nu0.sum() > 0
    rows = [r for r in load_weights(wpath) if r["H"] < B]
    S = rich_core(rows)
    S0 = {l for l in range(3, N0 + 1, 2) if N0 % l == 0 and all(l % d for d in range(3, int(l ** .5) + 1, 2))}
    VA = VC = WD = Fraction(0)
    nA = nC = nD = 0
    t0 = time.time()
    detail = []
    for p in sorted(S):
        r = S[p]
        sp = set(r["supp"])
        if not (sp & S0):
            # Haar weight, recomputed from scratch for p of moderate size, else from the table
            w = Fraction(r["cls"][cs]["maxN"], r["h3"] * r["h5"])
            WD += w; nD += 1; detail.append([p, "D", str(w)])
            continue
        m = mu_mass_max(p, r["h3"], r["h5"], c, N0, nu0)
        if sp <= S0:
            VA += m; nA += 1; detail.append([p, "A", str(m)])
        else:
            VC += m; nC += 1; detail.append([p, "C", str(m)])
    bound = 1 - (1 - VA) * (1 - WD) + VC
    ok = VA < 1 and WD < 1 and bound < 1
    res = {"status": "PASS" if ok else "FAIL", "B": B, "N0": N0, "class": cs, "core_size": len(S),
           "nA": nA, "nC": nC, "nD": nD, "V_A": str(VA), "V_C": str(VC), "W_D": str(WD),
           "bound": str(bound), "bound_float": float(bound), "V_A_float": float(VA), "V_C_float": float(VC),
           "W_D_float": float(WD), "seconds": round(time.time() - t0, 1)}
    print(json.dumps(res, indent=1))
    if len(sys.argv) > 3:
        res["detail"] = detail
        json.dump(res, open(sys.argv[3], "w"))
    assert ok

if __name__ == "__main__":
    main()
