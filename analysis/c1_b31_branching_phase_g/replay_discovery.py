#!/usr/bin/env python3
"""Optional finite probe replay. No infinite-domain or squarefree conclusion.
Standard library only. Does not certify any survivor prime.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--k-max', type=int, default=100000)
    p.add_argument('--output', type=Path)
    args=p.parse_args()
    if not 1 <= args.k_max <= 100000:
        raise ValueError('This reference gate authorizes only 1 <= k-max <= 100000')
    a,b=878851,625552508473588471
    count,hits=0,[]
    start=time.perf_counter()
    for c in (1,3,31,93):
        n=c*a*b
        factors=[a,b]+([3] if c%3==0 else [])+([31] if c%31==0 else [])
        for k in range(1,args.k_max+1,2):
            q=1+2*k*n
            if q%20 not in (11,19):
                continue
            count+=1
            if pow(5,n,q)!=1 or any(pow(5,n//r,q)==1 for r in factors):
                continue
            hits.append({'q':str(q),'n':str(n),'k':k,'multiplier':c,
                         'prime_certified':False,'q2_residue':str(pow(5,n,q*q))})
    out={'count':count,'seconds':time.perf_counter()-start,'hits':hits,
         'scope':'Only the displayed finite modular domain; no unbounded exclusion.'}
    text=json.dumps(out,indent=2)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':
    main()
