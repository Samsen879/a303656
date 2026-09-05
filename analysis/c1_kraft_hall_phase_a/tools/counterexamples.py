#!/usr/bin/env python3
"""Actual-prime regressions for position and shared-residue scope boundaries."""
from __future__ import annotations
import argparse,json
from pathlib import Path
if not __debug__:
    raise RuntimeError('Run without -O.')

def run() -> dict:
    # Source-known mechanism, independently constructed misalignment witness.
    p,q=67,20771
    b=155*pow(155,-1,67)
    rp=2;rq=(1+pow(5,b,q*q)*(1+q))%(q*q)
    dc=[];rc=[]
    for k in range(67):
        e=3410*k;x=e%67
        a=(rp-1-pow(5,e,p*p))%(p*p)
        z=(rq-1-pow(5,e,q*q))%(q*q)
        if a and a%p==0:dc.append(x)
        if z and z%q==0:rc.append(x)
    assert len(dc)==66 and rc==[1]
    assert len(set(dc)|set(rc))==66 and set(range(67))-(set(dc)|set(rc))=={0}
    # Actual counterexample to 'all zero-lower resources are one-sided'.
    q=40487;u=62;h=653;r=25919
    events=[[],[]];coeff=[]
    for c in (0,1):
        for k in range(h):
            e=u*k;z=(r-(1+2*c)-pow(5,e,q*q))%(q*q)
            if z and z%q==0:events[c].append((e%h,e))
    assert events==[[(50,3968)],[(547,14260)]]
    for c,bs in enumerate(events):
        x,e=bs[0];a=(r-(1+2*c)-pow(5,e,q*q))%(q*q)
        assert a%q==0 and a!=0;coeff.append(a//q)
    assert all(x!=0 for x,e in events[0])
    return {'misalignment':{'classification':'EXACT FINITE RESULT; previously known mechanism, independently constructed','p':p,'q':20771,'K':2,'E':[1],'c':0,'lower_modulus':3410,'lower_value':0,'r67':rp,'r20771':rq,'rigid_full_class':b,'dynamic_count':len(dc),'rigid_count':len(rc),'union_count':len(set(dc)|set(rc)),'holes':[0],'mass_sum':'1'},'zero_lower_double_activity':{'classification':'EXACT FINITE RESULT; refutes blanket zero-lower one-sidedness, not the h=5,7 theorems','q':q,'K':2,'E':[1],'r':r,'u':u,'lower_value':0,'ell':h,'beta':1,'events':events,'positive_valuation_one_coefficients':coeff}}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result=run();args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
