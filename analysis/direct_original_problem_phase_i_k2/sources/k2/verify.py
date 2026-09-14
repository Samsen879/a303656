#!/usr/bin/env python3
"""Read-only verification of K2 stored finite arithmetic and payload hashes.

This verifier does not certify the analytic proofs and is not described as a
fully independent replication project. It does not import the producer script.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math

P=Path(__file__).resolve().parent

def prime(n: int) -> bool:
    if n < 2:return False
    return all(n % d for d in range(2,math.isqrt(n)+1))


def check_row(row: dict, primalities: dict[int,bool]) -> None:
    m=row['m']
    fs={int(p):e for p,e in row['factors'].items()}
    if m == 0:
        assert fs == {} and row['norm'] and row['local_G']
        return
    assert all(e>=1 and primalities[p] for p,e in fs.items())
    assert math.prod(p**e for p,e in fs.items())==m
    bad=sorted(p for p,e in fs.items() if p%4==3 and e%2)
    L2=(m//2**fs.get(2,0))%4==1
    loc=L2 and all(fs.get(p,0)%2==0 for p in (3,7,11))
    assert row['bad_primes']==bad and row['kernel']==math.prod(bad)
    assert row['L2']==L2 and row['local_G']==loc and row['norm']==(not bad)
    assert row['least_bad']==(bad[0] if bad else None)
    if row['norm']:assert row['local_G']


def main() -> None:
    cert=json.loads((P/'FINITE_CERTIFICATES.json').read_text())
    grid=json.loads((P/'ATOM_GRID.json').read_text())
    rows=grid['pairs']+cert['phase_K_adversarial_pair']+cert['synthetic_pair_model']['rows']
    factors={int(p) for row in rows for p in row['factors']}
    primalities={p:prime(p) for p in factors}
    assert all(primalities.values())
    for row in rows:check_row(row,primalities)
    n=grid['n']
    all_pairs=set()
    c=0
    while 3**c<=n:
        d=0
        while 5**d<=n:
            if 3**c+5**d<=n:all_pairs.add((c,d))
            d+=1
        c+=1
    saved={(r['c'],r['d']) for r in grid['pairs']}
    assert saved==all_pairs and len(saved)==len(grid['pairs'])
    for r in grid['pairs']:assert r['m']==n-3**r['c']-5**r['d']
    H=sum(r['local_G'] for r in grid['pairs'])
    R=sum(r['norm'] for r in grid['pairs'])
    N=sum(r['local_G'] and r['least_bad']==100003 for r in grid['pairs'])
    assert (H,R,N)==(82,33,1)
    assert n==100003*100019+2==33798**2+94127**2+3**0+5**5
    for o in cert['orbit_fiber_tests']:
        p=o['p'];h3=o['ord3'];h5=o['ord5']
        assert prime(p)
        assert pow(3,h3,p)==pow(5,h5,p)==1
        assert all(pow(3,h,p)!=1 for h in range(1,h3))
        assert all(pow(5,h,p)!=1 for h in range(1,h5))
        freq=Counter((3**c+5**d)%p for c in range(o['C']+1) for d in range(o['D']+1))
        assert max(freq.values())==o['maximum_exact_fiber']<=o['order_cap']
    a=cert['absolute_remainder_floor_example'];H0=a['H']
    ps=[p for p in range(2*H0+1,a['Q']+1) if p%4==3 and prime(p)]
    v=sum((Fraction(H0,p+1) for p in ps),Fraction())
    assert v==Fraction(**a['exact_lower_bound']) and len(ps)==a['prime_count']
    s=cert['synthetic_pair_model']; used=[]
    for r in s['rows']:
        assert r['m']==r['p']*r['q']<s['ambient_n']
        assert r['p']**4>s['ambient_n'] and r['q']**4>s['ambient_n']
        used.extend([r['p'],r['q']])
    assert len(set(used))==2*s['H']
    checksum=P/'SHA256SUMS.txt'
    hashes=0
    if checksum.exists():
        for line in checksum.read_text().splitlines():
            if not line.strip():continue
            digest,name=line.split(maxsplit=1)
            assert hashlib.sha256((P/name.lstrip('*')).read_bytes()).hexdigest()==digest,name
            hashes+=1
    print(json.dumps({'finite_verification':'PASS','grid_points':len(grid['pairs']),
                      'factor_primes_verified':len(factors),'orbit_models':len(cert['orbit_fiber_tests']),
                      'payload_hashes_checked':hashes,'analytic_proofs_certified_by_this_script':False},indent=2))

if __name__=='__main__':
    main()
