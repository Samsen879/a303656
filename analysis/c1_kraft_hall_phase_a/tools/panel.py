#!/usr/bin/env python3
"""Independent exact panel; no imported repository code. No bound extension."""
import argparse, json, math, time, hashlib
from pathlib import Path
from array import array

if not __debug__:
    raise RuntimeError("Assertions are required; run Python without -O.")


def panel(B:int)->dict:
    t=time.perf_counter()
    # Independent smallest-factor sieve. Composite assignments proceed downward
    # so each final entry is the least prime factor.
    spf=array('I',[0])*(B+1)
    flags=bytearray(b'\x01')*(B+1); flags[:2]=b'\0\0'
    for p in range(2,math.isqrt(B)+1):
        if flags[p]: flags[p*p::p]=b'\0'*((B-p*p)//p+1)
    plist=[p for p in range(2,B+1) if flags[p]]
    for p in reversed([p for p in plist if p<=math.isqrt(B)]):
        for n in range(p*p,B+1,p): spf[n]=p
    def factors(n):
        ans=[]
        while n>1:
            p=spf[n] or n;ans.append(p)
            while n%p==0:n//=p
        return ans
    counts={str(l):{str(d):{'support':0,'order_signature':0,'active':0} for d in (1,2,3)} for l in (3,67)}
    lists={f'{l}:{d}':[] for l in (3,67) for d in (1,2,3)}
    hits=[]; cand=0; h=hashlib.sha256()
    for q in plist:
        if q%4!=3:continue
        cand+=1;h.update(f'{q}\n'.encode())
        fac=factors(q-1);w=q-1
        for p in fac:
            while w%p==0 and pow(5,w//p,q)==1:w//=p
        wf=[p for p in fac if w%p==0]; largest=max(wf)
        nr=(pow(5,w,q*q)==1)
        if nr:
            s=2
            while pow(5,w,q**(s+1))==1:s+=1
            hits.append({'q':q,'w':w,'s':s,'largest':largest})
        for l in (3,67):
            x=w;d=0
            while x%l==0:x//=l;d+=1
            if d in (1,2,3):
                z=counts[str(l)][str(d)];z['support']+=1
                if largest==l:
                    z['order_signature']+=1;lists[f'{l}:{d}'].append(q)
                    if nr:z['active']+=1
    return {'q_max':B,'admitted_count':cand,'searched_sha256':h.hexdigest(),'nonregular':hits,'counts':counts,'order_lists':lists,'seconds':time.perf_counter()-t}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--bound',type=int,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    if args.bound not in (100000,10000000):raise SystemExit('Unfrozen bound refused')
    r=panel(args.bound);args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='order_lists'},indent=2))
