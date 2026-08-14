#!/usr/bin/env python3
"""Clean-room exact finite interval scanner, independent of the C++ bitset code.

It deliberately reimplements parsing, primality, power generation, activation,
and the valuation-one predicate without importing common.py.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from time import perf_counter


def prime(n:int)->bool:
    if n<2:return False
    if n%2==0:return n==2
    f=3
    while f<=n//f:
        if n%f==0:return False
        f+=2
    return True

def parse(text:str)->list[int]:
    q=Path(text)
    raw=q.read_text() if q.is_file() else text
    vals=[int(x) for x in raw.replace('\n',',').replace(' ', ',').split(',') if x.strip()]
    if not vals or len(vals)!=len(set(vals)):raise ValueError('empty or duplicate pool')
    for p in vals:
        if not prime(p) or p%4!=3:raise ValueError(f'invalid p={p}')
    return vals

def powers(base:int,e:int)->list[int]:
    out=[1]
    for _ in range(e):out.append(out[-1]*base)
    return out

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--high',type=int,required=True)
    ap.add_argument('--C',type=int,required=True);ap.add_argument('--D',type=int,required=True);ap.add_argument('--primes',required=True);ap.add_argument('--json',required=True)
    args=ap.parse_args();
    if args.low>args.high:raise SystemExit('low>high')
    if args.high>=3**(args.C+1)+1:raise SystemExit('C bound fails')
    if args.high>=5**(args.D+1)+1:raise SystemExit('D bound fails')
    P=parse(args.primes);p3=powers(3,args.C);p5=powers(5,args.D)
    shifts=sorted({x+y for x in p3 for y in p5 if x+y<=args.high})
    t0=perf_counter();found=[];tested=0;shift_tests=0;mod_tests=0
    for n in range(args.low,args.high+1):
        tested+=1;ok=True
        for s in shifts:
            if s>n:break
            shift_tests+=1;r=n-s;covered=False
            # r=0 is deliberately rejected: r%(p*p)==0 for every p.
            if r>0:
                for p in P:
                    mod_tests+=1
                    if r%p==0 and r%(p*p)!=0:
                        covered=True;break
            if not covered:
                ok=False;break
        if ok:found.append(n)
    elapsed=perf_counter()-t0
    payload={'method':'clean_room_python_exhaustive','low':str(args.low),'high':str(args.high),'C':args.C,'D':args.D,
             'primes':P,'distinct_shift_count_relevant_to_high':len(shifts),'integers_tested':tested,'shift_tests':shift_tests,'mod_tests':mod_tests,
             'candidate_count':len(found),'candidates':[str(x) for x in found],'elapsed_seconds':elapsed,
             'classification':'EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL'}
    Path(args.json).write_text(json.dumps(payload,indent=2)+'\n')
    print(f'integers_tested={tested}');print(f'shift_tests={shift_tests}');print(f'mod_tests={mod_tests}');print(f'candidate_count={len(found)}');print(f'elapsed_seconds={elapsed:.9f}');print('EXACT_EMPTY' if not found else 'CANDIDATES_FOUND')
    return 1 if not found else 0
if __name__=='__main__':raise SystemExit(main())
