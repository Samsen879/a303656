#!/usr/bin/env python3
"""Reference objects for the Abstract Covering Problem (ACP), A303656.

Model (see REPORT.md, section 1).  Fix a parity class c = (c1, c2) in {0,1}^2,
i.e. alpha = c1 + 2a, beta = c2 + 2b.  For an inert prime p > 3 (p = 3 mod 4)
put h3 = oddpart(ord_p 3), h5 = oddpart(ord_p 5).  On the class c the residue
        s = b1^alpha + b2^beta  (mod p)        (b1, b2) = (3, 5) by default
depends only on (a mod h3, b mod h5), and the *fibre*
        F_p^c(z) = {(a,b) in Z/h3 x Z/h5 : b1^c1 (b1^2)^a + b2^c2 (b2^2)^b = z (mod p)}
is the maximal bad event at p (Lemma L1 of the report).  A *covering* of the
class c is a finite set of pairs (p, z_p), with distinct primes, whose fibres
cover (Z/N)^2 for N = lcm of all h3, h5.

Everything in this file is exact integer arithmetic; numpy is used only for
integer vector operations.
"""
from math import gcd
from fractions import Fraction
import numpy as np
from arith import mult_order, odd_part, factorint

CLASSES = [(0, 0), (0, 1), (1, 0), (1, 1)]


def lcm(a, b):
    return a // gcd(a, b) * b


class PrimeData:
    """Exact tame data of one prime for bases (b1, b2)."""

    def __init__(self, p, b1=3, b2=5, require_inert=True, step=2):
        """step=2: exponents run over a parity class (the real model);
        step=1: exponents run over all residues (toy models without parity)."""
        assert p > 2 and p % b1 != 0 and p % b2 != 0 and step in (1, 2)
        if require_inert:
            assert p % 4 == 3
        self.p, self.b1, self.b2, self.step = p, b1, b2, step
        f = factorint(p - 1)
        self.o1, self.o2 = mult_order(b1, p, f), mult_order(b2, p, f)
        self.h1 = self.o1 // gcd(self.o1, step)
        self.h2 = self.o2 // gcd(self.o2, step)
        if p % 4 == 3 and step == 2:
            assert self.h1 == odd_part(self.o1) and self.h2 == odd_part(self.o2)
        self.H = max(self.h1, self.h2)

    def coset(self, which, c):
        """List x_i = b^c (b^step)^i, i = 0..h-1 (index i = exponent coordinate)."""
        b, h = (self.b1, self.h1) if which == 1 else (self.b2, self.h2)
        p = self.p
        x, sq = pow(b, c, p), pow(b, self.step, p)
        out = []
        for _ in range(h):
            out.append(x)
            x = x * sq % p
        return out

    def counts(self, c):
        """N_z = #F_p^c(z) for all z in F_p, exactly (numpy int array of length p)."""
        A = np.array(self.coset(1, c[0]), dtype=np.int64)
        Bv = np.array(self.coset(2, c[1]), dtype=np.int64)
        p = self.p
        if len(A) * len(Bv) <= 2 * 10 ** 7 and p <= 6 * 10 ** 6:
            s = (A[:, None] + Bv[None, :]) % p
            return np.bincount(s.ravel(), minlength=p)
        if p <= 6 * 10 ** 6:
            return _exact_cyclic_convolution(A, Bv, p)
        raise NotImplementedError("use max_count() for very large p")

    def max_count(self, c):
        """(max_z N_z, one maximiser z, N_0, number of nonempty fibres)."""
        p = self.p
        A = np.array(self.coset(1, c[0]), dtype=np.int64)
        Bv = np.array(self.coset(2, c[1]), dtype=np.int64)
        if p <= 6 * 10 ** 6:
            N = self.counts(c)
            z = int(N.argmax())
            return int(N[z]), z, int(N[0]), int(np.count_nonzero(N))
        # large p: several passes over residue classes of s mod R, each pass sorted in memory
        assert p < 2 ** 31
        n = len(A) * len(Bv)
        R = max(1, -(-n // (2 * 10 ** 8)))
        best, bestz, n0, nonempty = 0, -1, 0, 0
        step = max(1, 10 ** 7 // len(Bv))
        for rr in range(R):
            parts = []
            for i in range(0, len(A), step):
                blk = ((A[i:i + step, None] + Bv[None, :]) % p).ravel()
                if R > 1:
                    blk = blk[blk % R == rr]
                parts.append(blk.astype(np.int32))
            s = np.concatenate(parts)
            del parts
            s.sort()
            CH = 10 ** 7
            carry_val, carry_cnt = None, 0
            for i in range(0, len(s), CH):
                u, cnt = np.unique(s[i:i + CH], return_counts=True)
                cnt = cnt.astype(np.int64)
                if carry_val is not None:
                    if u[0] == carry_val:
                        cnt[0] += carry_cnt
                    else:
                        nonempty += 1
                        if carry_cnt > best:
                            best, bestz = carry_cnt, carry_val
                        if carry_val == 0:
                            n0 = carry_cnt
                if len(u) > 1:
                    k = int(cnt[:-1].argmax())
                    if int(cnt[k]) > best:
                        best, bestz = int(cnt[k]), int(u[k])
                    nonempty += len(u) - 1
                    if u[0] == 0:
                        n0 = int(cnt[0])
                carry_val, carry_cnt = int(u[-1]), int(cnt[-1])
            if carry_val is not None:
                nonempty += 1
                if carry_cnt > best:
                    best, bestz = carry_cnt, carry_val
                if carry_val == 0:
                    n0 = carry_cnt
            del s
        return best, bestz, n0, nonempty

    def fibre(self, c, z):
        """List of (a, b) in Z/h1 x Z/h2 lying in F_p^c(z)."""
        A = self.coset(1, c[0])
        Bv = self.coset(2, c[1])
        pos = {y: j for j, y in enumerate(Bv)}
        p = self.p
        out = []
        for i, x in enumerate(A):
            j = pos.get((z - x) % p)
            if j is not None:
                out.append((i, j))
        return out


def _exact_cyclic_convolution(A, Bv, p):
    """Exact N_z via one big-integer multiplication (16-bit slots)."""
    import gmpy2
    assert min(len(A), len(Bv)) < 65536
    def pack(xs):
        buf = np.zeros(p, dtype=np.uint16)
        buf[xs] = 1
        return gmpy2.mpz(int.from_bytes(buf.tobytes(), "little"))
    prod = int(pack(A) * pack(Bv))
    raw = prod.to_bytes(4 * p + 2, "little")
    arr = np.frombuffer(raw, dtype=np.uint16)[:2 * p].astype(np.int64)
    return arr[:p] + arr[p:2 * p]


# ----------------------------------------------------------------------------
# Reference decision procedure: exact coverage by counting over the quotient
# ----------------------------------------------------------------------------

def coverage(c, targets, b1=3, b2=5, require_inert=True, max_cells=4 * 10 ** 8, return_mask=False, step=2):
    """Exact decision.  targets = list of (p, z) with distinct p.
    Returns dict(N1, N2, cells, uncovered) where `uncovered` is the exact
    number of points of Z/N1 x Z/N2 lying in no fibre (0 <=> covering)."""
    ps = [p for p, _ in targets]
    assert len(set(ps)) == len(ps), "one residue per prime"
    data = [PrimeData(p, b1, b2, require_inert, step) for p in ps]
    N1 = N2 = 1
    for d in data:
        N1, N2 = lcm(N1, d.h1), lcm(N2, d.h2)
    cells = N1 * N2
    if cells > max_cells:
        raise MemoryError(f"quotient too large for enumeration: {N1} x {N2}")
    cov = np.zeros((N1, N2), dtype=bool)
    for d, (p, z) in zip(data, targets):
        pts = d.fibre(c, z % p)
        if not pts:
            continue
        local = np.zeros((d.h1, d.h2), dtype=bool)
        ii, jj = zip(*pts)
        local[list(ii), list(jj)] = True
        cov |= np.tile(local, (N1 // d.h1, N2 // d.h2))
    res = {"N1": N1, "N2": N2, "cells": cells, "uncovered": int(cells - np.count_nonzero(cov))}
    if return_mask:
        res["mask"] = cov
    return res


def weight(d, c):
    """Exact w_p^c = max_z #F/(h1 h2) as a Fraction."""
    m, z, n0, ne = d.max_count(c)
    return Fraction(m, d.h1 * d.h2)
