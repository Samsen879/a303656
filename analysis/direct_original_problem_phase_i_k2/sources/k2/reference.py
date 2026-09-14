#!/usr/bin/env python3
"""K2 bounded falsification/reference tests. No interval scan, no network.

All primality and factorizations in the stored finite certificates are exact
trial division. The assertions test implementations, not asymptotic theorems.
Run: python reference.py --output-dir replay
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from time import perf_counter


def prime_sieve(limit: int) -> list[int]:
    if limit < 2:
        return []
    flags = bytearray(b'\x01') * (limit + 1)
    flags[0:2] = b'\x00\x00'
    for d in range(2, math.isqrt(limit) + 1):
        if flags[d]:
            flags[d*d:limit+1:d] = b'\x00' * ((limit-d*d)//d+1)
    return [i for i, ok in enumerate(flags) if ok]


def factor(n: int, primes: list[int]) -> dict[int, int]:
    if n < 1:
        raise ValueError('factor expects a positive integer')
    if n > 1 and (not primes or primes[-1] < math.isqrt(n)):
        raise ValueError('prime table must cover sqrt(original input)')
    out: dict[int, int] = {}
    left = n
    for p in primes:
        if p*p > left:
            break
        while left % p == 0:
            out[p] = out.get(p, 0) + 1
            left //= p
    if left > 1:
        out[left] = out.get(left, 0) + 1
    assert math.prod(p**e for p, e in out.items()) == n
    return out


def prime_by_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def powers(base: int, limit: int) -> list[int]:
    if base < 2 or limit < 1:
        raise ValueError('base >= 2 and limit >= 1 required')
    out, value = [], 1
    while value <= limit:
        out.append(value)
        value *= base
    return out


def classify(m: int, primes: list[int]) -> dict:
    if m == 0:
        return {'m': 0, 'factors': {}, 'bad_primes': [], 'kernel': 1,
                'L2': True, 'local_G': True, 'norm': True, 'least_bad': None}
    fs = factor(m, primes)
    odd = m // (2**fs.get(2, 0))
    bad = sorted(p for p, e in fs.items() if p % 4 == 3 and e % 2)
    local = odd % 4 == 1 and all(fs.get(p, 0) % 2 == 0 for p in (3,7,11))
    return {'m': m, 'factors': {str(p):e for p,e in fs.items()},
            'bad_primes': bad, 'kernel': math.prod(bad), 'L2': odd % 4 == 1,
            'local_G': local, 'norm': not bad, 'least_bad': bad[0] if bad else None}


def order(a: int, p: int) -> int:
    if math.gcd(a,p) != 1:
        raise ValueError('base must be a unit')
    x = 1
    for h in range(1, p):
        x = x*a % p
        if x == 1:
            return h
    raise AssertionError('order not found')


def frac(x: Fraction) -> dict:
    return {'numerator': x.numerator, 'denominator': x.denominator}


def run(output: Path) -> dict:
    start = perf_counter()
    output.mkdir(parents=True, exist_ok=True)
    p, q = 100003, 100019
    assert p < q < 2*p and p % 4 == q % 4 == 3
    assert prime_by_trial(p) and prime_by_trial(q)
    n = p*q + 2
    primes = prime_sieve(math.isqrt(n) + 100)
    p3, p5 = powers(3,n), powers(5,n)
    entries, counts = [], Counter()
    for c,a in enumerate(p3):
        for d,b in enumerate(p5):
            if a+b > n:
                continue
            row = {'c': c, 'd': d, **classify(n-a-b, primes)}
            entries.append(row)
            counts['D'] += 1
            counts['R'] += int(row['norm'])
            if row['local_G']:
                counts['G'] += 1
                if row['least_bad'] is not None:
                    counts['failures'] += 1
                    if row['least_bad'] == p:
                        counts['N_p'] += 1
    assert counts['R'] == counts['G']-counts['failures']
    initial = next(e for e in entries if e['c']==0 and e['d']==0)
    assert initial['local_G'] and initial['least_bad'] == p and not initial['norm']
    assert initial['factors'] == {str(p):1, str(q):1}
    J = len(p3)*len(p5)
    assert counts['N_p'] >= 1 and J < p
    (output/'ATOM_GRID.json').write_text(json.dumps({'n':n,'pairs':entries},indent=2)+'\n')

    local_pair=[]
    for target in (28280,915320):
        row={'n':target,'c':3,'d':2,**classify(target-27-25,primes)}
        assert target % 27720 == 560 and target % 16 == 8
        assert row['local_G']
        local_pair.append(row)
    assert local_pair[0]['norm'] and not local_pair[1]['norm']
    assert local_pair[0]['m'] == 2**2+168**2
    local_pair[0]['norm_witness'] = {'a':2,'b':168}

    # Abstract factor-incidence countermodel, expressly NOT a common-n grid.
    pool=[r for r in prime_sieve(2000) if r>=1000 and r%4==3][:32]
    assert len(pool)==32
    ambient=4000000
    synthetic=[]
    for i in range(16):
        a,b=pool[2*i:2*i+2]
        m=a*b
        assert m < ambient and a**4 > ambient and b**4 > ambient
        row=classify(m,primes)
        assert row['local_G'] and not row['norm'] and row['bad_primes']==[a,b]
        synthetic.append({'p':a,'q':b,'u':1,**row})
    all_primes=[r for row in synthetic for r in (row['p'],row['q'])]
    assert max(Counter(all_primes).values())==1

    # Exhaustive finite residue models (not scans of original n).
    orbit_tests=[]
    for r in (19,23,31,43,47,59,101,251,1019):
        h3,h5=order(3,r),order(5,r)
        assert 3**h3>=r+1 and 5**h5>=r+1
        for C,D in ((8,5),(20,14),(40,29)):
            freq=Counter((pow(3,c,r)+pow(5,d,r))%r
                         for c in range(C+1) for d in range(D+1))
            cap=min((C+1)*(D//h5+1),(D+1)*(C//h3+1))
            assert max(freq.values()) <= cap
            orbit_tests.append({'p':r,'C':C,'D':D,'ord3':h3,'ord5':h5,
                                'maximum_exact_fiber':max(freq.values()),'order_cap':cap})

    # Integer-distance inequality for several admissible models.
    round_tests=0
    for H in range(1,33):
        for r in (67,101,251,1019):
            if r<=2*H: continue
            mu=Fraction(H,r+1)
            for count in (0,1,H):
                assert abs(Fraction(count)-mu)>=mu
                round_tests+=1
    H=32
    chosen=[r for r in prime_sieve(5000) if r>2*H and r%4==3]
    exact_floor=sum((Fraction(H,r+1) for r in chosen),Fraction())

    # The quarter-cutoff identity is inherited from Phase J. Recheck it only
    # on the constructed literal grid and the two supplied adversarial rows.
    quarter_tests=0
    for ambient_n, rows in ((n,entries),(28280,[local_pair[0]]),(915320,[local_pair[1]])):
        for row in rows:
            if not row['local_G'] or row['m']==0: continue
            surviving_cutoff=all(r**4>ambient_n for r in row['bad_primes'])
            if surviving_cutoff:
                if row['norm']:
                    assert not row['bad_primes']
                else:
                    assert len(row['bad_primes'])==2
                    a,b=row['bad_primes']
                    assert row['factors'][str(a)]==row['factors'][str(b)]==1
                    u=row['m']//(a*b)
                    assert classify(u,primes)['norm']
                    assert u*u<ambient_n
            quarter_tests+=1

    distinct=sorted({int(r) for row in entries+local_pair+synthetic for r in row['factors']})
    assert all(prime_by_trial(r) for r in distinct)
    data={
        'scope':'Bounded lemma falsification and model verification; no original-n interval scan.',
        'literal_atom':{'p':p,'q':q,'n':n,'J':J,**dict(counts),
                        'G_over_p':frac(Fraction(counts['G'],p)),
                        'J_over_p':frac(Fraction(J,p)),
                        'pair_00':initial,'full_representation':{'a':33798,'b':94127,'c':0,'d':5}},
        'phase_K_adversarial_pair':local_pair,
        'synthetic_pair_model':{'NOT_A_LITERAL_EXPONENTIAL_GRID':True,'ambient_n':ambient,
                                'H':16,'maximum_prime_incidence':1,'rows':synthetic},
        'orbit_fiber_tests':orbit_tests,
        'integer_distance_assertions':round_tests,
        'absolute_remainder_floor_example':{'H':H,'Q':5000,'prime_count':len(chosen),
                                             'exact_lower_bound':frac(exact_floor)},
        'inherited_quarter_identity_tests':quarter_tests,
        'factorization_certification':{'method':'exact trial division; second trial-primality pass for all output factors',
                                        'distinct_primes':len(distinct),'largest_prime':max(distinct)},
        'new_original_n_windows':0,
        'literal_n_full_grid_tests':1,
        'github_writes':0,
        'all_assertions_passed':True
    }
    (output/'FINITE_CERTIFICATES.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'n':n,'J':J,**dict(counts),'orbit_models':len(orbit_tests),
                      'distinct_primes':len(distinct),'all_assertions_passed':True,
                      'elapsed_seconds':round(perf_counter()-start,3)},indent=2))
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    run(args.output_dir)
