#!/usr/bin/env python3
"""Regenerate finite arithmetic certificates using exact polynomial Euclidean
resultants and elementary integer factorization. The independent checker uses
Sylvester matrices and a Bareiss determinant instead. No third-party packages.
"""
from __future__ import annotations
import argparse
import json
import math
import time
from fractions import Fraction
from pathlib import Path

if not __debug__:
    raise RuntimeError('Verification requires assertions; do not run Python with -O.')

def factor(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError('Positive integer required.')
    out: dict[int,int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        out[n] = out.get(n,0)+1
    return out

def order(q: int) -> int:
    w = q-1
    for p in factor(w):
        while w%p == 0 and pow(5,w//p,q) == 1:
            w //= p
    return w

def strip(f: list[Fraction]) -> list[Fraction]:
    while f and f[-1] == 0:
        f.pop()
    return f

def remainder(f: list[Fraction], g: list[Fraction]) -> list[Fraction]:
    f=f[:]
    while f and len(f) >= len(g):
        j=len(f)-len(g); a=f[-1]/g[-1]
        for k,b in enumerate(g): f[j+k]-=a*b
        strip(f)
    return f

def poly_resultant(f: list[Fraction], g: list[Fraction]) -> Fraction:
    f=strip(f[:]);g=strip(g[:])
    if not f or not g:
        return Fraction(0)
    m,n=len(f)-1,len(g)-1
    if n == 0:
        return g[0]**m
    r=remainder(f,g)
    if not r:
        return Fraction(0)
    k=len(r)-1
    return (-1)**(m*n)*g[-1]**(m-k)*poly_resultant(g,r)

def resultant(h: int) -> int:
    f=[Fraction(-1)]+[Fraction(0)]*(h-1)+[Fraction(1)]
    g=[Fraction(math.comb(h,k)*(-2)**(h-k)) for k in range(h+1)]
    g[0]-=1
    r=poly_resultant(f,g)
    assert r.denominator == 1
    return int(r)

def generate(out: Path) -> None:
    out.mkdir(parents=True,exist_ok=True)
    cc=[]
    for d in (1,2,3):
        t=time.perf_counter();a=5**(3**(d-1));row=[]
        for m,value in ((3**d,a*a+a+1),(2*3**d,a*a-a+1)):
            fac=factor(value);accepted=[]
            for q in sorted(fac):
                if q%4 != 3: continue
                w=order(q);s=1
                while pow(5,w,q**(s+1))==1:s+=1
                accepted.append({'q':q,'w':w,'s':s})
            row.append({'m':m,'value':str(value),'factorization':fac,'admitted':accepted})
        cc.append({'d':d,'factors':row,'seconds':time.perf_counter()-t})
    rr=[]
    for h in (3,5,7,9):
        t=time.perf_counter();R=resultant(h);fs=factor(abs(R));tests=[]
        for q in sorted(fs):
            if q>h and q%4==3 and q!=5:
                w=order(q)
                tests.append({'q':q,'w':w,'order_factors':factor(w),'nonregular':pow(5,w,q*q)==1})
        rr.append({'h':h,'Y':0,'resultant':str(R),'factors':fs,'eligible_tests':tests,'seconds':time.perf_counter()-t})
    (out/'cyclotomic_complete.json').write_text(json.dumps(cc,indent=2)+'\n')
    (out/'resultant_zero_classes.json').write_text(json.dumps(rr,indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args();generate(args.output_dir)
    print('Generated six cyclotomic and four resultant certificates.')
