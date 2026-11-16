#!/usr/bin/env python3
"""Shared tools: richness pruning (Lemma L3) and exact mu-mass evaluation for
measures of the form  mu = nu0 (on (Z/N0)^2)  x  Haar (all other coordinates)."""
import json
from math import gcd
from collections import Counter
from fractions import Fraction
import numpy as np

CL = ["00", "01", "10", "11"]


def load_weights(path):
    return json.load(open(path))["rows"]


def rich_core(rows, k=0):
    """Largest subset S such that every odd prime l dividing h3*h5 of a member
    divides h3*h5 of at least l-k members (Lemma L3 with k outside primes)."""
    S = {r["p"]: r for r in rows}
    while True:
        cnt = Counter(l for r in S.values() for l in r["supp"])
        bad = {l for l, n in cnt.items() if n < l - k}
        if not bad:
            return S
        S = {p: r for p, r in S.items() if not (set(r["supp"]) & bad)}


def cosets(p, h3, h5, c):
    def run(b, cc, h):
        x, sq, out = pow(b, cc, p), b * b % p, []
        for _ in range(h):
            out.append(x); x = x * sq % p
        return np.array(out, dtype=np.int64)
    return run(3, c[0], h3), run(5, c[1], h5)


def fibre_cell_table(p, h3, h5, c, N0):
    """Return (g3, g5, zs, cells): for every point (i,j) of Z/h3 x Z/h5 its
    residue z = s mod p and its cell index (i mod g3)*g5 + (j mod g5)."""
    g3, g5 = gcd(h3, N0), gcd(h5, N0)
    A, B = cosets(p, h3, h5, c)
    z = ((A[:, None] + B[None, :]) % p).astype(np.int64)
    cell = (np.arange(h3)[:, None] % g3) * g5 + (np.arange(h5)[None, :] % g5)
    return g3, g5, z.ravel(), cell.ravel().astype(np.int64)


def marginal(nu0, N0, g3, g5):
    """Integer marginal of nu0 (N0 x N0 integer array) on Z/g3 x Z/g5."""
    return nu0.reshape(g3, N0 // g3, g5, N0 // g5).transpose(1, 3, 0, 2).sum(axis=(0, 1)) \
        if False else _marg(nu0, N0, g3, g5)


def _marg(nu0, N0, g3, g5):
    out = np.zeros((g3, g5), dtype=object)
    for u in range(g3):
        for v in range(g5):
            out[u, v] = int(nu0[u::g3, v::g5].sum())
    return out


def mu_mass_max(p, h3, h5, c, N0, nu0):
    """Exact max_z mu(F_p^c(z)) for mu = nu0 x Haar, nu0 an integer array
    (unnormalised).  Returns Fraction."""
    total = int(nu0.sum())
    g3, g5, z, cell = fibre_cell_table(p, h3, h5, c, N0)
    m = _marg(nu0, N0, g3, g5).ravel()
    wts = np.array([int(x) for x in m], dtype=np.float64)
    assert max(int(x) for x in m) * min(h3, h5) < 2 ** 52  # exact float accumulation
    mass = np.bincount(z, weights=wts[cell], minlength=p)
    best = int(round(float(mass.max())))
    # mu(F) = sum_cells nu_p(cell)/total * cnt(cell)/((h3/g3)(h5/g5))
    return Fraction(best * g3 * g5, total * h3 * h5)
