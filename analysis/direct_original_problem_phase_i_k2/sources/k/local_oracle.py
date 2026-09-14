#!/usr/bin/env python3
"""Optional independent raw prime-power oracle (requires NumPy).
This enumerates exponent residue states, NEVER an interval of original n.
It brackets the closed-form density using unresolved-valuation cells.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import json
import numpy as np
from reference import rho4

def order(a:int,q:int)->int:
    x=a%q;t=1
    while x!=1:x=x*a%q;t+=1
    return t

def tables(p:int,k:int):
    q=p**k;lo=np.zeros(q,dtype=bool);hi=np.zeros(q,dtype=bool)
    for r in range(q):
        if r==0:hi[r]=True;continue
        e=0;u=r
        while u%p==0:u//=p;e+=1
        if p==2:
            if e>=k-1:hi[r]=True
            else:lo[r]=hi[r]=(u%4==1)
        else:lo[r]=hi[r]=(e%2==0)
    return lo,hi

def run():
    records=[]
    for depths,targets in [((4,2,1,1),(0,2,4,56,70,560,8120,23240,28280)),
        ((5,3,2,2),(0,2,4,56,70,560,8120,23240,28280)),
        ((7,4,2,2),(4,560))]:
        primes=(2,3,7,11);qs=[p**k for p,k in zip(primes,depths)]
        T=lcm(*(order(5,q) for q in qs)); assert T%30==0
        pows=[];masks=[]
        for p,k,q in zip(primes,depths,qs):
            a=np.empty(T,dtype=np.int64);x=1
            for j in range(T):a[j]=x;x=x*5%q
            pows.append(a);masks.append(tables(p,k))
        for n in targets:
            countlo=counthi=0
            for c0 in range(30):
                c=c0 if c0>=depths[1] else c0+30
                low=np.ones(T,dtype=bool);high=np.ones(T,dtype=bool)
                for q,ds,(lo,hi) in zip(qs,pows,masks):
                    r=(n-pow(3,c,q)-ds)%q
                    low &=lo[r];high &=hi[r]
                countlo+=int(np.count_nonzero(low));counthi+=int(np.count_nonzero(high))
            lower=F(countlo,30*T);upper=F(counthi,30*T);exact=rho4(n)
            assert lower<=exact<=upper,(n,depths,lower,exact,upper)
            records.append({'n_signature':n,'depths':list(depths),'prime_powers':qs,
                'd_period':T,'states_enumerated':30*T,'lower':str(lower),'exact':str(exact),
                'upper':str(upper),'bracket_passed':True})
    path=Path(__file__).with_name('LOCAL_ORACLE.json')
    path.write_text(json.dumps({'method':'raw modular power cycles with lower/upper unresolved-valuation masks',
        'raw_c_representatives':'one per c mod30, chosen >= the 3-adic truncation exponent',
        'why_30_representatives_suffice':'complete d-cycle translations remove higher c-coordinates; proved in LOCAL_MODEL.md',
        'records':records},indent=2)+'\n')
    print(f'{len(records)} exact rational brackets passed; written {path.name}')

if __name__=='__main__':run()
