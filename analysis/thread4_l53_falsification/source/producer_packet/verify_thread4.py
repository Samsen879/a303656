#!/usr/bin/env python3
"""Thread 4: exact, bounded laboratory and constructive obstruction receipts.

Python 3.10+, standard library only. No network, no repository writes.
This checks finite examples and congruence certificates. It is not a formal
proof assistant or an independent human review of the accompanying proofs.

Run: python3 verify_thread4.py --output laboratory.json
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from math import isqrt, prod
from pathlib import Path

SHA = "8f17e88e517720f61f3c21d58d91c04cd6fa11b5"
H = (1, 2, 3, 4, 5, 8, 9, 24)
LIMIT = 5000


def powers(base: int, limit: int) -> list[int]:
    out, value = [], 1
    while value <= limit:
        out.append(value)
        value *= base
    return out


def vp(n: int, p: int) -> int:
    if n == 0:
        raise ValueError("valuation of zero is not finite")
    n, k = abs(n), 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def prime(p: int) -> bool:
    return p >= 2 and all(p % k for k in range(2, isqrt(p) + 1))


def is_power3(n: int) -> bool:
    if n < 1:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


def crt(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    x, mod = 0, 1
    for a, q in zip(residues, moduli, strict=True):
        step = ((a - x) * pow(mod, -1, q)) % q
        x += mod * step
        mod *= q
        x %= mod
    return x, mod


def unit_norm_mod_p2(value: int, p: int) -> tuple[int, int]:
    """Find x^2+y^2=value mod p^2 for a nonzero residue mod odd p."""
    if p % 2 == 0 or not prime(p) or value % p == 0:
        raise ValueError("requires an odd prime and a unit")
    value %= p * p
    root = {b * b % p: b for b in range(p)}
    for a in range(p):
        needed = (value - a * a) % p
        if needed not in root:
            continue
        b = root[needed]
        difference = (value - a*a - b*b) // p
        if a:
            a += p * (difference * pow(2*a, -1, p) % p)
        else:
            b += p * (difference * pow(2*b, -1, p) % p)
        assert (a*a + b*b - value) % (p*p) == 0
        return a, b
    raise AssertionError("finite-field norm surjectivity failed")


def obstruction_certificate(lam: int, K: int) -> dict:
    """Construct S=x^2+y^2 with lam*S+K outside S_2+{3^C}.

    Domain used here: lam in {1,5}, K>0 not a power of 3.
    An odd 3-adic valuation blocks every C>t. Distinct p_C=3 mod 4
    block C=0,...,t. All checks are exact, with unbounded Python integers.
    """
    if lam not in (1, 5) or K <= 0 or is_power3(K):
        raise ValueError("outside the constructive obstruction domain")
    k = vp(K, 3)
    if k % 2:
        t = k
        mod3 = 3 ** ((k+1)//2)
        x3 = y3 = 0
    else:
        t = k + 1
        e = k // 2
        unit = ((3 - K // (3**k)) * pow(lam, -1, 9)) % 9
        u, v = unit_norm_mod_p2(unit, 3)
        mod3 = 3 ** (e+2)
        x3, y3 = (3**e)*u, (3**e)*v
    mods, xs, ys = [mod3], [x3], [y3]
    rows = []
    p = 7
    for C in range(t+1):
        while not (prime(p) and p % 4 == 3 and (lam*(K-3**C)) % p):
            p += 4
        q = p*p
        required = ((p - K + 3**C) * pow(lam, -1, q)) % q
        x, y = unit_norm_mod_p2(required, p)
        mods.append(q); xs.append(x); ys.append(y)
        rows.append({"C": C, "p": p, "required_S_mod_p2": required})
        p += 4
    x, period = crt(xs, mods)
    y, period2 = crt(ys, mods)
    assert period == period2
    S, T = x*x+y*y, lam*(x*x+y*y)+K
    assert vp(T, 3) == t and t % 2
    for row in rows:
        C, p = row["C"], row["p"]
        assert prime(p) and p % 4 == 3
        assert (T-3**C) % (p*p) == p
        assert vp(T-3**C, p) == 1
    # Preserve the full source-coordinate progression, not just one example.
    for j in (1, 2, 7):
        Tj = lam*((x+period*j)**2+y*y)+K
        assert vp(Tj, 3) == t
        for row in rows:
            assert (Tj-3**row["C"]) % row["p"]**2 == row["p"]
    return {"lambda": lam, "K": K, "source_x": x, "source_y": y,
            "coordinate_period": period, "S": S, "T": T,
            "odd_3_valuation": t, "finite_C_blockers": rows,
            "infinite_tail_reason": "For C>t, v_3(T-3^C)=t whenever the residual is positive.",
            "infinite_family": "x_j=source_x+coordinate_period*j, y_j=source_y; j>=0"}


def inert_factor(n: int) -> tuple[int, int]:
    if n <= 0:
        raise ValueError("positive residual required")
    for p in range(3, isqrt(n)+2, 4):
        if prime(p) and n % p == 0 and vp(n, p) % 2:
            return p, vp(n, p)
    # A large remaining inert prime can exceed sqrt(n).
    v = n
    for p in range(2, isqrt(n)+1):
        while v % p == 0:
            v //= p
    if v > 1 and v % 4 == 3:
        return v, 1
    raise AssertionError(f"no inert odd-valuation factor found for {n}")


def laboratory() -> dict:
    target_limit = 5*LIMIT+4
    sq = [[] for _ in range(target_limit+1)]
    for x in range(isqrt(target_limit)+1):
        for y in range(x, isqrt(target_limit-x*x)+1):
            sq[x*x+y*y].append((x,y))
    norm = [bool(row) for row in sq]
    P3, P5 = powers(3, target_limit), powers(5, target_limit)

    def representations(n: int) -> list[tuple[int,int,int,int]]:
        if n < 2:
            return []
        return [(x,y,c,d) for c,a in enumerate(P3) if a<n
                for d,b in enumerate(P5) if a+b<=n for x,y in sq[n-a-b]]

    R = [representations(n) for n in range(LIMIT+1)]
    # Separate loop ordering checks counts for the entire source interval.
    independent_counts = [0]*(LIMIT+1)
    for S in range(LIMIT-1):
        for x,y in sq[S]:
            for a in powers(3, LIMIT-S-1):
                for b in powers(5, LIMIT-S-a):
                    independent_counts[S+a+b] += 1
    assert independent_counts == list(map(len, R))

    source_failure_counts = {}
    source_failure_lists = {}
    first_source_failures = {}
    r3_overlap = Counter()
    for r in range(5):
        fails = []
        first = None
        for m in range(2,LIMIT+1):
            target_d = {d for _,_,_,d in representations(5*m+r)}
            source_d = {d for _,_,_,d in R[m]}
            successes = {d for d in source_d if d+1 in target_d}
            if not successes:
                fails.append(m)
            if first is None:
                bad = [rr for rr in R[m] if rr[3]+1 not in target_d]
                if bad:
                    first = {"m":m, "N":5*m+r, "source":bad[0]}
            if r == 3:
                r3_overlap[len(successes)] += 1
        source_failure_counts[r] = len(fails)
        source_failure_lists[r] = fails
        first_source_failures[r] = first

    first_adversarial = None
    adversarial_count = 0
    for n in range(max(H)+2,LIMIT+1):
        bads=[]
        for h in H:
            bad=[rr for rr in R[n-h] if not norm[n-3**rr[2]-5**rr[3]]]
            if not bad:
                break
            bads.append(min(bad, key=lambda rr:(rr[2]+rr[3],rr)))
        else:
            adversarial_count += 1
            if first_adversarial is None:
                first_adversarial = {"N":n, "H":H, "bad_sources":bads}

    coherent = []
    rows = [(3,0,2),(0,2,2),(5,1,1),(2,1,2),
            (5,0,1),(0,1,2),(5,0,0),(2,1,1)]
    for h,(y,c,d) in zip(H, rows, strict=True):
        assert y*y+3**c+5**d == 36-h
        residual=85-3**c-5**d
        p,k=inert_factor(residual)
        coherent.append({"h":h,"source_at_N85":[7,y,c,d],
                         "target_residual":residual,"blocker_prime":p,
                         "blocker_valuation":k})
    period=9*49*59**2*79**2*83**2
    for j in (0,1,2):
        t=7+period*j
        for h,(y,c,d) in zip(H,rows,strict=True):
            n=t*t+36
            assert n-h == t*t+y*y+3**c+5**d
            residual=n-3**c-5**d
            # These selected primes work throughout this common t progression.
            p={1:59,2:3,3:7,4:3,5:79,8:3,9:83,24:7}[h]
            assert vp(residual,p)==1
        assert t*t+36 == t*t+2**2+3**3+5**1

    three_compensation=[]
    for r,S,x,y,d in [(0,98,7,7,1),(1,0,0,0,0),(2,1,0,1,0)]:
        T=3*S+3*5**d+r
        terms=[]
        for e,q in enumerate(powers(5,T)):
            residual=T-q
            assert residual>0 and not norm[residual]
            p,k=inert_factor(residual)
            terms.append({"e":e,"residual":residual,"p":p,"valuation":k})
        three_compensation.append({"r":r,"x":x,"y":y,"d":d,
                                    "T":T,"all_target_5_exponents":terms,
                                    "family":"m=x^2+y^2+3^c+5^d for arbitrary c>=0"})

    certificates=[]
    for r in range(5):
        for c in range(9):
            K=5*3**c+r
            if (r,c)==(4,0):
                assert K==9
            else:
                certificate=obstruction_certificate(5,K)
                certificate.update({"r":r,"source_c":c})
                certificates.append(certificate)
    # General theorem also covers unit-scale neighboring lifts.
    for K in range(1,51):
        if not is_power3(K):
            certificates.append(obstruction_certificate(1,K))

    return {"authority":{"repository":"Samsen879/a303656","main_sha":SHA,
                          "main_tree":"811a274b1f671412305c8565fcd79e9d41c0189b",
                          "access":"read-only","remote_changes":False},
            "scope":{"source_interval":[2,LIMIT],"target_maximum":target_limit,
                     "normalization":"0<=x<=y; c,d>=0; every tuple enumerated",
                     "meaning":"structural lifting tests, not a proof from absence of small counterexamples"},
            "canonical_source_representation_count":sum(map(len,R)),
            "independent_loop_order_count_check":"PASS",
            "five_lift_some_source_first_failure":first_source_failures,
            "five_lift_all_source_failure_counts":source_failure_counts,
            "five_lift_all_source_failure_source_m_lists":source_failure_lists,
            "r3_overlap_size_histogram":dict(sorted(r3_overlap.items())),
            "all_H_adversarial_witness_selection_count":adversarial_count,
            "first_all_H_adversarial_selection":first_adversarial,
            "coherent_eight_neighbor_model":{"N_at_t7":85,"rows":coherent,
                "infinite_t_progression":{"base":7,"period":period},
                "target_representation":"N=t^2+2^2+3^3+5^1",
                "scope":"blocks retaining any supplied exponent pair; does NOT block other representations or exponent exchange"},
            "three_compensation_counterfamilies":three_compensation,
            "constructive_congruence_certificate_count":len(certificates),
            "constructive_congruence_certificates":certificates,
            "verification_status":"PASS (finite checks and local certificates only)"}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("laboratory.json"))
    args=parser.parse_args()
    results=laboratory()
    args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:results[k] for k in (
        "canonical_source_representation_count","five_lift_all_source_failure_counts",
        "constructive_congruence_certificate_count","verification_status")},indent=2))
    print(f"Receipt written to {args.output}")

if __name__=="__main__":
    main()
