#!/usr/bin/env python3
"""Exact fixed-row two-anchor projected-logarithm audit."""
import json
from pathlib import Path
from arithmetic import row

def run():
    q=20771
    info=row(q)
    w=info['w']
    logs={}
    v=1
    for a in range(w):
        assert v not in logs
        logs[v]=a
        v=v*5%q
    assert v==1
    stats={str(l):{'same':0,'different':0,'witnesses':{}} for l in (5,31,67)}
    pairs=[]
    for v,a in logs.items():
        b=logs.get((v-2)%q)
        if b is not None:
            pairs.append(((v+1)%q,a,b))
    pairs.sort()
    for r,a,b in pairs:
        for l in (5,31,67):
            typ='same' if a%l==b%l else 'different'
            stats[str(l)][typ]+=1
            if typ not in stats[str(l)]['witnesses']:
                target0=(1+pow(5,a,q*q))%(q*q)
                target1=(3+pow(5,b,q*q))%(q*q)
                for h in range(3):
                    R=r+h*q
                    if R != target0 and R != target1: break
                else: raise AssertionError('three candidates cannot all be two zeros')
                V0=(R-1-pow(5,a,q*q))%(q*q)
                V1=(R-3-pow(5,b,q*q))%(q*q)
                assert V0%q==V1%q==0 and V0 and V1
                stats[str(l)]['witnesses'][typ]=dict(r_mod_q=r,r_mod_q2=R,
                    anchor_logs=[a,b],projected_digits=[a%l,b%l],
                    valuation_quotients=[V0//q,V1//q])
    return dict(q=q,w=w,s=info['s'],K=2,E=[1],
        paired_low_residue_count=len(pairs),coordinates=stats)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n')
