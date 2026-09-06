#!/usr/bin/env python3
"""Standalone deterministic integer reference computations (no dependencies)."""
import json
from math import isqrt, lcm
from pathlib import Path

def factor(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError('factor expects a positive integer')
    ans = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            ans[d] = ans.get(d,0)+1
            n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        ans[n] = ans.get(n,0)+1
    return ans

def isprime(n):
    return n >= 2 and factor(n) == {n:1}

def admitted(p):
    return p != 5 and p%4 == 3 and isprime(p)

def row(p):
    if not admitted(p):
        raise ValueError(f'{p} is not an admitted odd prime label')
    f = factor(p-1)
    w = p-1
    for r in f:
        while w%r == 0 and pow(5, w//r, p) == 1:
            w //= r
    wf = factor(w)
    s=1
    while pow(5,w,p**(s+1)) == 1:
        s+=1
    order_checks = {str(r): pow(5,w//r,p) for r in wf}
    assert pow(5,w,p)==1 and all(v != 1 for v in order_checks.values())
    return dict(p=p, prime=True, primality_method='complete trial division',
        p_minus_one_factorization=f, w=w, w_factorization=wf, s=s,
        order_one_check=pow(5,w,p), order_proper_divisor_checks=order_checks,
        valuation_one_check=pow(5,w,p**s),
        valuation_next_check=pow(5,w,p**(s+1)),
        odd_order_factors=[r for r in wf if r != 2],
        admitted_children=[r for r in wf if r != 2 and admitted(r)],
        unadmitted_terminal_factors=[r for r in wf if r != 2 and not admitted(r)])

def closure(seed):
    rows={}
    todo=[seed]
    while todo:
        p=todo.pop()
        if p in rows: continue
        a=rows[p]=row(p)
        todo.extend(a['admitted_children'])
    return dict(seed=seed, rows=[rows[p] for p in sorted(rows)],
        edges=[[p,q] for p in sorted(rows) for q in rows[p]['admitted_children']],
        terminal_factors=sorted({r for a in rows.values() for r in a['unadmitted_terminal_factors']}),
        U=lcm(*(a['w'] for a in rows.values())))

def run():
    return dict(domain='fixed-seed descending admitted-label closures',
        closures=[closure(p) for p in (1645333507,20771,40487)])

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n')
