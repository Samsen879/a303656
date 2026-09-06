#!/usr/bin/env python3
"""Boundary-primed coordinate 3, with independent direct square-set audit."""
import argparse
import json
from pathlib import Path
from arithmetic import row, isprime, closure
from graphs import (subsets, capacity, maximum_matching, terminal_frontiers,
                    dag_min_cut, route_forest)

def choose_boundary(K, r2, r3):
    if K < 2: raise ValueError('K >= 2 required')
    M=1 << K
    r2%=M; r3%=3
    period=1 if K==2 else 1 << (K-2)
    if r2%2:
        c=0 if r2%4==3 else 1
        d=next(d for d in (0,1) if (r3-pow(3,c,3)-pow(5,d,3))%3)
    else:
        target=(r2-(3 if r2%4==0 else 5))%M
        d=next(d for d in range(period) if pow(5,d,M)==target)
        c=next(c for c in (0,1) if (r3-pow(3,c,3)-pow(5,d,3))%3)
    return c,d

def audit():
    by_K={}; total=0
    for K in range(2,10):
        M=1<<K
        squares={x*x%M for x in range(M)}
        two_squares={(x+y)%M for x in squares for y in squares}
        n=0
        for r2 in range(M):
            for r3 in range(3):
                c,d=choose_boundary(K,r2,r3)
                assert (r2-3**c-pow(5,d,M))%M in two_squares
                assert (r3-pow(3,c,3)-pow(5,d,3))%3 != 0
                n+=1
        by_K[str(K)]=n;total+=n
    vertices=(3,7,11,23,31,67)
    supports={p:set(row(p)['odd_order_factors']) for p in vertices if p!=3}
    labels=set(vertices)|set().union(*supports.values())
    caps={p:p-1 for p in labels}
    cases=passed=0
    for P in subsets(vertices):
        effective=set(P)-{3}  # row 3 is pre-inactive, NOT deleted arithmetically
        front=terminal_frontiers(effective,supports)
        for T in subsets(sorted(effective)):
            matching=maximum_matching({q:front[q] for q in T},caps)
            value,_=dag_min_cut(effective,T,supports,caps)
            assert value==len(matching)
            if len(matching)==len(T):
                route_forest(effective,T,supports,caps,matching);passed+=1
            cases+=1
    return dict(boundary_cases=total,cases_by_K=by_K,
        verification='directly enumerated sums of two square residues',
        route_cases=cases,route_passing=passed,mismatches=0,
        route_target_scope='arbitrary mandatory regular-row guard targets, excluding pre-inactive 3')

def primed_frontier(p):
    if p==3: return {3}
    out=set()
    for lam in row(p)['odd_order_factors']:
        out.update({lam} if lam%4==1 else primed_frontier(lam))
    assert out
    assert sum(lam-1 for lam in out)<p-1
    return out

def signatures():
    out={}
    for m in range(1,101):
        ps=[p for p in range(3,m+1) if isprime(p) and (p==3 or p%4==1)]
        found=[]
        def rec(i,total,chosen):
            if total==m-1:
                if chosen: found.append(chosen)
                return
            for j in range(i,len(ps)):
                p=ps[j]
                if total+p-1<=m-1:rec(j+1,total+p-1,chosen+[p])
        rec(0,0,[])
        if found:out[str(m)]=found
    return dict(max_core_size=100,
        interpretation='necessary capacity signatures only; not arithmetic realization',
        signatures=out,
        seed_frontiers={str(p):sorted(primed_frontier(p)) for p in (20771,40487,1645333507)})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
    a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
    for name,fn in [('primed_three',audit),('primed_terminal_signatures',signatures)]:
        r=fn();(a.output_dir/(name+'.json')).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
        print(name, r if name=='primed_three' else {k:v for k,v in r['signatures'].items() if int(k)<=23})
