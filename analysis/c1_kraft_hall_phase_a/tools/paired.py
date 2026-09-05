#!/usr/bin/env python3
"""Exact shared-lower paired positions, two independent enumerations."""
import json,time,hashlib
from pathlib import Path
from collections import Counter

if not __debug__:
    raise RuntimeError("Assertions are required; run Python without -O.")


def run(q,w,l):
    t=time.perf_counter();h=1;u=w
    while u%l==0:u//=l;h*=l
    v=1;log={};values=[]
    for b in range(w):
        assert v not in log
        log[v]=b;values.append(v);v=v*5%q
    assert v==1
    full=[(b,log[(a-2)%q]) for b,a in enumerate(values) if (a-2)%q in log]
    groups={y:[] for y in range(u)}
    for b0,b1 in full:
        if (b0-b1)%u==0:groups[b0%u].append((b0%h,b1%h,b0,b1))
    # Enumeration B uses each lower coset separately and scans residues r mod q.
    for y,pairs in groups.items():
        cs={pow(5,y+k*u,q):(y+k*u)%w for k in range(h)}
        other=sorted((cs[(r-1)%q]%h,cs[(r-3)%q]%h,cs[(r-1)%q],cs[(r-3)%q]) for r in range(q) if (r-1)%q in cs and (r-3)%q in cs)
        assert sorted(pairs)==other
        assert len({p[0] for p in pairs})==len(pairs)==len({p[1] for p in pairs})
        assert all(x!=z for x,z,_,_ in pairs)
        succ={x:z for x,z,_,_ in pairs}
        for x in succ:
            seen=set();v=x
            while v in succ:
                assert v not in seen
                seen.add(v);v=succ[v]
        for x,z,b0,b1 in pairs:
            assert (pow(5,b0,q)-pow(5,b1,q))%q==2
            # A common q^2 residue avoiding the (at most two) local-zero lifts.
            r0=(1+pow(5,b0,q))%q
            rr=next(r0+k*q for k in range(3) if (r0+k*q-1-pow(5,b0,q*q))%(q*q) and (r0+k*q-3-pow(5,b1,q*q))%(q*q))
            assert (rr-1-pow(5,b0,q*q))%q==0 and (rr-3-pow(5,b1,q*q))%q==0
    assert all(x!=0 for x,z,b0,b1 in groups[0])  # universal zero-lower outgoing-zero obstruction
    hist=Counter(len(v) for v in groups.values())
    return {'q':q,'w':w,'ell':l,'h':h,'u':u,'all_pair_count':len(full),'same_lower_pair_count':sum(map(len,groups.values())),'nonempty_lower_count':sum(bool(v) for v in groups.values()),'histogram':dict(sorted(hist.items())),'lower_zero_pairs':groups[0],'pairs_by_lower':groups,'seconds':time.perf_counter()-t}
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'results/paired_positions.json');args=ap.parse_args()
    out=[run(20771,10385,67),run(40487,40486,653)]
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in z.items() if k!='pairs_by_lower'} for z in out],indent=2))
