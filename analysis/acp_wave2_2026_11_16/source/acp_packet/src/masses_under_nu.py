#!/usr/bin/env python3
"""Upper bounds m_p >= max_z mu(F_p^c(z)) for EVERY catalogue prime, mu = nu0 x Haar.
   - supp(p) disjoint from the primes of N0:  m_p = Haar weight (exact)
   - h3*h5 <= LIMIT:                          m_p = exact max_z mu-mass (full enumeration)
   - otherwise:                               m_p = rho(g3,g5) * Haar weight, where rho is the
                                              maximal density ratio of the (g3,g5)-marginal of nu0.
Also returns rho_max (bound for primes outside the catalogue: mass <= rho_max / B).
usage: masses_under_nu.py weights.json cert.json out.json [LIMIT]
"""
import sys, json, time
from math import gcd
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from core_tools import load_weights, mu_mass_max

def rho(nu0, N0, g3, g5):
    tot = int(nu0.sum())
    mx = max(int(nu0[u::g3, v::g5].sum()) for u in range(g3) for v in range(g5))
    return F(mx * g3 * g5, tot)

def compute(rows, cert, limit=4 * 10 ** 6, verbose=True):
    N0, cs = cert["N0"], cert["class"]
    c = (int(cs[0]), int(cs[1]))
    nu0 = np.array(cert["nu0"], dtype=np.int64)
    S0 = {l for l in range(3, N0 + 1, 2) if N0 % l == 0 and all(l % d for d in range(3, int(l ** .5) + 1, 2))}
    cache = {}
    out = {}
    t0 = time.time()
    for r in rows:
        w = F(r["cls"][cs]["maxN"], r["h3"] * r["h5"])
        if not (set(r["supp"]) & S0):
            out[r["p"]] = (w, "haar")
        elif r["h3"] * r["h5"] <= limit:
            out[r["p"]] = (mu_mass_max(r["p"], r["h3"], r["h5"], c, N0, nu0), "exact")
        else:
            g = (gcd(r["h3"], N0), gcd(r["h5"], N0))
            if g not in cache:
                cache[g] = rho(nu0, N0, *g)
            out[r["p"]] = (cache[g] * w, "rho")
    rmax = rho(nu0, N0, N0, N0)
    if verbose:
        print(f"class {cs}: {sum(1 for v in out.values() if v[1]=='exact')} exact, "
              f"{sum(1 for v in out.values() if v[1]=='rho')} rho-bounded, rho_max={float(rmax):.3f} [{time.time()-t0:.0f}s]", flush=True)
    return out, rmax

if __name__ == "__main__":
    rows = load_weights(sys.argv[1]); cert = json.load(open(sys.argv[2]))
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 4 * 10 ** 6
    out, rmax = compute(rows, cert, limit)
    json.dump({"class": cert["class"], "N0": cert["N0"], "rho_max": str(rmax),
               "mass": {str(p): [str(m), how] for p, (m, how) in out.items()}}, open(sys.argv[3], "w"))
