#!/usr/bin/env python3
"""Independent checks of the complete catalogue Cat_B (no code shared with build_catalogue.py
except arith.sieve / trial division).

 1. every listed prime is prime (complete trial division) and the stored orders are the exact
    multiplicative orders (b^o = 1 and b^(o/q) != 1 for every prime q | o);  H < B.
 2. the stored integer G equals prod p^e over the listed primes (so G is completely factored).
 3. COMPLETENESS, route A (brute force): every inert prime p < SCAN with max(h3,h5) < B is listed,
    and conversely (orders recomputed from scratch from the factorisation of p-1).
 4. COMPLETENESS, route B (modular, for the sub-cutoff B2): for every odd h < B2 the number
    gcd(3^(2h)-1, prod_{h' odd < B2} (5^(2h')-1) mod (3^(2h)-1)) factors completely over the listed
    primes with H < B2 -- i.e. no prime with H < B2 is missing.
usage: verify_catalogue.py catalogue.json [SCAN=3000000] [B2=1024]
"""
import sys, json, time
from math import gcd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from arith import sieve, is_prime_td

def factor_small(n, primes):
    out = []
    for p in primes:
        if p * p > n: break
        if n % p == 0:
            out.append(p)
            while n % p == 0: n //= p
    if n > 1: out.append(n)
    return out

def order(b, p, qs):
    o = p - 1
    for q in qs:
        while o % q == 0 and pow(b, o // q, p) == 1:
            o //= q
    return o

def odd(n):
    while n % 2 == 0: n //= 2
    return n

def main():
    if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
    cat = json.load(open(sys.argv[1]))
    SCAN = int(sys.argv[2]) if len(sys.argv) > 2 else 3 * 10 ** 6
    B2 = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    B = cat["B"]; rows = cat["rows"]
    primes = sieve(50000)
    t0 = time.time()
    G = int(cat["G"]); prod = 1
    for r in rows:
        p = r["p"]
        assert is_prime_td(p), p
        prod *= p ** r["e_in_G"]
        if p > 5:
            qs = factor_small(p - 1, primes)
            assert all(is_prime_td(q) for q in qs)
            o3, o5 = order(3, p, qs), order(5, p, qs)
            assert (o3, o5) == (r["ord3"], r["ord5"]), p
            if p % 4 == 3:
                assert max(odd(o3), odd(o5)) == r["H"] < B
    assert prod == G
    print(f"[PASS] 1-2: {len(rows)} primes certified, orders exact, G = prod p^e  [{time.time()-t0:.0f}s]", flush=True)
    listed = {r["p"] for r in rows if r["p"] > 3 and r["p"] % 4 == 3}
    found = set()
    for p in sieve(SCAN):
        if p > 3 and p % 4 == 3:
            # quick filter: 3^(2*odd) = 1 needs order with 2-part <= 2: automatic.  Compute orders.
            qs = factor_small(p - 1, primes)
            if max(odd(order(3, p, qs)), odd(order(5, p, qs))) < B:
                found.add(p)
    assert found == {p for p in listed if p < SCAN}, sorted(found ^ {p for p in listed if p < SCAN})[:10]
    print(f"[PASS] 3: brute-force scan of all inert primes p < {SCAN}: exactly {len(found)} have H < {B}, all listed "
          f"[{time.time()-t0:.0f}s]", flush=True)
    sub = [r["p"] for r in rows if r["p"] > 5 and max(odd(r["ord3"]), odd(r["ord5"])) < B2 and
           r["ord3"] % 4 != 0 and r["ord5"] % 4 != 0] + [2]
    hs = list(range(1, B2, 2))
    for h in hs:
        m = 3 ** (2 * h) - 1
        r5 = 1
        x = 25 % m
        cur = x
        for _ in hs:
            r5 = r5 * (cur - 1) % m
            cur = cur * 625 % m       # 5^(2(h'+2)) = 5^(2h') * 5^4
        g = gcd(m, r5)
        for p in sub:
            while g % p == 0: g //= p
        assert g == 1, (h, g)
    print(f"[PASS] 4: modular completeness check for cutoff {B2}: no unlisted prime divides both products "
          f"[{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    main()
