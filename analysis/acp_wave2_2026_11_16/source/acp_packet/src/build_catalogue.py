#!/usr/bin/env python3
"""Build the COMPLETE catalogue Cat_B of primes p with
        h3(p) := oddpart(ord_p 3) < B   and   h5(p) := oddpart(ord_p 5) < B.

Completeness argument (exact):  p | 3^(2h)-1 for some odd h < B  <=>  ord_p(3) | 2h
for some odd h < B  <=>  v_2(ord_p 3) <= 1 and h3(p) < B.  For p = 3 (mod 4),
v_2(p-1) = 1, so the 2-adic condition is automatic.  Hence every inert prime
with H_p = max(h3,h5) < B divides
        G = gcd( prod_{h odd < B} (3^(2h)-1),  prod_{h odd < B} (5^(2h)-1) ),
and we factor G completely.  (Primes with p = 1 mod 4 in G are listed too but
are not complete for that class and are not used.)

usage: build_catalogue.py B out.json
"""
import sys, json, time
from math import gcd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from arith import (HAVE_GMP, gmpy2, sieve, factorint, probable_prime, pollard_rho,
                   certify_prime, mult_order, odd_part, TD_LIMIT, is_prime_td)


def prod_tree(xs):
    xs = list(xs)
    while len(xs) > 1:
        xs = [xs[i] * xs[i + 1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]


def main():
    B = int(sys.argv[1]); out = sys.argv[2]
    t0 = time.time()
    mpz = gmpy2.mpz if HAVE_GMP else int
    hs = list(range(1, B, 2))
    P3 = prod_tree(mpz(3) ** (2 * h) - 1 for h in hs)
    P5 = prod_tree(mpz(5) ** (2 * h) - 1 for h in hs)
    G = gmpy2.gcd(P3, P5) if HAVE_GMP else gcd(P3, P5)
    G = int(G)
    print(f"B={B}: P3 bits={int(P3).bit_length()} P5 bits={int(P5).bit_length()} "
          f"G bits={G.bit_length()}  [{time.time()-t0:.1f}s]", flush=True)
    del P3, P5
    # --- complete factorisation of G ---
    fac = {}
    C = mpz(G)
    for p in sieve(2 * 10 ** 7):
        if C % p == 0:
            e = 0
            while C % p == 0:
                C //= p; e += 1
            fac[p] = e
    C = int(C)
    print(f"after trial division to 2e7: cofactor bits={C.bit_length()} [{time.time()-t0:.1f}s]", flush=True)
    # split the cofactor: every prime q | C has h3(q) < B, so q | 3^(2h)-1 for h = h3(q)
    pieces = []
    if C > 1:
        for h in hs:
            g = gcd(C, pow(3, 2 * h, C) - 1)
            while g > 1:
                pieces.append(g)
                C //= g
                g = gcd(C, g)
            if C == 1:
                break
        assert C == 1, "cofactor not exhausted (impossible by construction)"
    stack = pieces[:]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if probable_prime(m):
            fac[m] = fac.get(m, 0) + 1
            continue
        # perfect powers / composites
        r = None
        for k in (2, 3, 5, 7):
            rt = int(gmpy2.iroot(mpz(m), k)[0]) if HAVE_GMP else round(m ** (1.0 / k))
            if rt ** k == m:
                r = rt; stack.extend([rt] * k); break
        if r is None:
            d = pollard_rho(m, seed=7)
            stack.append(d); stack.append(m // d)
    # exact multiplicities and product check
    chk = 1
    for p in list(fac):
        e = 0; g = G
        while g % p == 0:
            g //= p; e += 1
        fac[p] = e; chk *= p ** e
    assert chk == G, "factorisation of G incomplete"
    print(f"G fully factored: {len(fac)} primes, largest {max(fac)} [{time.time()-t0:.1f}s]", flush=True)
    rows = []
    for p in sorted(fac):
        cert = certify_prime(p)
        row = {"p": p, "e_in_G": fac[p], "mod4": p % 4}
        if p > 5:
            f = factorint(p - 1)
            o3, o5 = mult_order(3, p, f), mult_order(5, p, f)
            row.update(ord3=o3, ord5=o5, h3=odd_part(o3), h5=odd_part(o5))
            row["H"] = max(row["h3"], row["h5"])
            assert row["H"] < B
        if p >= TD_LIMIT:
            row["pratt"] = cert
        rows.append(row)
    inert = [r for r in rows if r["p"] > 3 and r["mod4"] == 3]
    obj = {"format": "A303656-ACP-catalogue-v1", "B": B, "G": str(G),
           "n_primes_in_G": len(rows), "n_inert": len(inert), "rows": rows}
    with open(out, "w") as fh:
        json.dump(obj, fh)
    print(f"written {out}: {len(inert)} inert primes with H<{B}; max inert p = {max(r['p'] for r in inert)} "
          f"[{time.time()-t0:.1f}s]", flush=True)


if __name__ == "__main__":
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    main()
