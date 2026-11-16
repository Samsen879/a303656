#!/usr/bin/env python3
"""LP-dual search for a measure certificate  mu = nu0 x Haar  on a class c.

For a finite prime set T (here: the rich core of Cat_B) a covering of the
class c would force  mu(union of fibres) = 1 for EVERY probability measure mu.
With   A = {p in T : supp(p) subset S0},  D = {p : supp(p) cap S0 = empty},
C = T minus (A u D),  S0 = prime divisors of N0,  we have (independence of the
S0-coordinates from the others under mu):
   mu(union) <= 1 - (1 - V_A)(1 - W_D) + V_C,
   V_X = sum_{p in X} max_z mu(F_p(z)),   W_D = Haar union bound of D.
We minimise (1-W_D) V_A + V_C over nu0 by cutting planes (scipy/HiGHS), then
round nu0 to integers; the exact verifier recomputes everything in integers.

usage: search_lp.py weights.json B N0 class out.json [maxprod]
"""
import sys, json, time
from math import gcd
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from core_tools import load_weights, rich_core, fibre_cell_table

def main():
    path, B, N0, cs, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    maxprod = int(sys.argv[6]) if len(sys.argv) > 6 else 3 * 10 ** 6
    c = (int(cs[0]), int(cs[1]))
    rows = [r for r in load_weights(path) if r["H"] < B]
    S = rich_core(rows)
    S0 = {l for l in range(3, N0 + 1, 2) if N0 % l == 0 and all(l % d for d in range(3, int(l ** .5) + 1, 2))}
    A, C, D = [], [], []
    for r in S.values():
        sp = set(r["supp"])
        (A if sp <= S0 else D if not (sp & S0) else C).append(r)
    hw = lambda r: r["cls"][cs]["maxN"] / (r["h3"] * r["h5"])
    WD = sum(hw(r) for r in D)
    print(f"core {len(S)}: A={len(A)} C={len(C)} D={len(D)}  Haar sums: A={sum(map(hw,A)):.4f} C={sum(map(hw,C)):.4f} D={WD:.4f}", flush=True)
    lp = [r for r in A + C if r["h3"] * r["h5"] <= maxprod]
    rest = [r for r in A + C if r["h3"] * r["h5"] > maxprod]
    print(f"LP primes {len(lp)}, deferred big primes {len(rest)} (Haar sum {sum(map(hw,rest)):.5f})", flush=True)
    nv = N0 * N0
    # per-prime tables: K (rows z, cols cells) as CSR counts, and marginalisation matrix
    tabs = []
    xs, ys = np.divmod(np.arange(nv), N0)
    for r in lp:
        g3, g5, z, cell = fibre_cell_table(r["p"], r["h3"], r["h5"], c, N0)
        K = sparse.coo_matrix((np.ones(len(z)), (z, cell)), shape=(r["p"], g3 * g5)).tocsr()
        Mg = sparse.coo_matrix((np.ones(nv), ((xs % g3) * g5 + (ys % g5), np.arange(nv))), shape=(g3 * g5, nv)).tocsr()
        scale = g3 * g5 / (r["h3"] * r["h5"])
        coef = 1.0 if r in C else (1.0 - WD)
        tabs.append((r, K, Mg, scale, coef))
    nu = np.full(nv, 1.0 / nv)
    rowsA, rhs = [], []
    seen = set()
    nl = len(lp)
    def add_cut(k, zrow):
        r, K, Mg, scale, coef = tabs[k]
        if (k, zrow) in seen:
            return False
        seen.add((k, zrow))
        vec = (K[zrow] @ Mg).toarray().ravel() * scale
        row = np.zeros(nv + nl); row[:nv] = vec; row[nv + k] = -1.0
        rowsA.append(row); rhs.append(0.0)
        return True
    t0 = time.time()
    for it in range(200):
        added = 0; val = 0.0
        for k, (r, K, Mg, scale, coef) in enumerate(tabs):
            mass = scale * (K @ (Mg @ nu))
            order = np.argsort(-mass)[:3]
            val += coef * mass[order[0]]
            for zrow in order:
                if add_cut(k, int(zrow)):
                    added += 1
        print(f"it {it}: objective at current nu = {val:.5f}  cuts={len(rowsA)} (+{added}) [{time.time()-t0:.0f}s]", flush=True)
        if it > 0 and (added == 0 or val - lpval < 1.5e-3):
            break
        cvec = np.concatenate([np.zeros(nv), [t[4] for t in tabs]])
        Aeq = np.concatenate([np.ones(nv), np.zeros(nl)])[None, :]
        res = linprog(cvec, A_ub=np.array(rowsA), b_ub=np.array(rhs), A_eq=Aeq, b_eq=[1.0],
                      bounds=[(0, None)] * (nv + nl), method="highs")
        assert res.status == 0, res.message
        nu = np.maximum(res.x[:nv], 0); nu /= nu.sum(); lpval = res.fun
        print(f"      LP value {lpval:.5f}", flush=True)
    # integer rounding
    Dn = 10 ** 7
    nu_int = np.maximum(np.rint(nu * Dn).astype(np.int64), 0)
    json.dump({"B": B, "N0": N0, "class": cs, "nu0": nu_int.reshape(N0, N0).tolist(), "float_objective": val},
              open(out, "w"))
    print("saved", out)

if __name__ == "__main__":
    main()
