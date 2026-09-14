#!/usr/bin/env python3
"""Second rigorous checker; no imports from primary/producer checker."""
import json
from math import isqrt
from pathlib import Path

def insist(b):
    if not b: raise ArithmeticError('certificate/closure hypothesis failed')

def power(a,k,m):
    v=1
    while k:
        if k&1: v=v*a%m
        a=a*a%m;k//=2
    return v

def coprime(a,b):
    while b: a,b=b,a%b
    return abs(a)==1

def prove(n,proofs,active,done):
    if n in done: return
    insist(n>1 and n not in active)
    if n<=10**9:
        insist(n==2 or n%2!=0)
        for d in range(3,isqrt(n)+1,2): insist(n%d!=0)
    else:
        active.add(n);v=proofs[str(n)];F=1
        insist(bool(v['factors']))
        for raw,e in v['factors'].items():
            p=int(raw);insist(type(e) is int and e>=1 and 1<p<n)
            prove(p,proofs,active,done);F*=p**e
        insist((n-1)%F==0)
        for raw in v['factors']:
            p=int(raw);a=v['witnesses'][raw]
            insist(type(a) is int and 1<a<n)
            insist(power(a,n-1,n)==1 and coprime(power(a,(n-1)//p,n)-1,n))
        if v['method']=='pocklington_sqrt': insist(F*F>n)
        else:
            insist(v['method']=='pocklington_cubic_nonsquare' and F**3>n)
            quotient=(n-1)//F;s=quotient//F;r=quotient-s*F;D=r*r-4*s
            insist(D<0 or isqrt(D)*isqrt(D)!=D)
        active.remove(n)
    done.add(n)

def main():
    P=Path(__file__).resolve().parent
    data=json.loads((P/'PRIMALITY_CERTIFICATE.json').read_text())
    # Independent Mobius evaluation via squarefree subsets of primes dividing 279.
    numerator=1;denominator=1
    for mask in range(4):
        divisor=1;parity=0
        for j,p in enumerate((3,31)):
            if mask&(1<<j): divisor*=p;parity+=1
        term=5**(279//divisor)-1
        if parity%2: denominator*=term
        else: numerator*=term
    insist(numerator%denominator==0);C=numerator//denominator
    insist(C==int(data['value']))
    qs=list(map(int,data['prime_factors']));insist(len(qs)==2 and qs[0]!=qs[1] and qs[0]*qs[1]==C)
    done=set()
    for q in qs:
        prove(q,data['prime_proofs'],set(),done)
        insist(q%4==3 and 279%q!=0)
        insist(power(5,279,q)==1 and all(power(5,e,q)!=1 for e in (93,9)))
        rem=C;valuation=0
        while rem%q==0: rem//=q;valuation+=1
        insist(valuation==1 and power(5,279,q*q)!=1)
    print('PASS\nIndependent rigorous primality: BOTH FACTORS\nSq279_cardinality: 0\nFrozen_I7_architecture: CLOSED\nA303656: UNRESOLVED')

if __name__=='__main__': main()
