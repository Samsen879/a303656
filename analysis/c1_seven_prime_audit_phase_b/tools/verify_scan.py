"""Independent Python checks: baseline, hit certificates, complete block comparison."""
from __future__ import annotations
import json, math, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def factor(n:int)->dict[int,int]:
    ans={};d=2
    while d*d<=n:
        while n%d==0:ans[d]=ans.get(d,0)+1;n//=d
        d=3 if d==2 else d+2
    if n>1:ans[n]=ans.get(n,0)+1
    return ans
def prime(n:int)->bool:
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,math.isqrt(n)+1,2))
def certify(q:int)->dict:
    assert prime(q)
    f=factor(q-1); w=q-1
    for r in f:
        while w%r==0 and pow(5,w//r,q)==1:w//=r
    assert pow(5,w,q)==1
    exclusions={str(r):pow(5,w//r,q) for r in factor(w)}
    assert all(a!=1 for a in exclusions.values())
    s=1
    while pow(5,w,q**(s+1))==1:s+=1
    return dict(q=q,admitted=q%4==3,q_minus_one_factorization=f,order=w,order_factorization=factor(w),order_exclusion_residues=exclusions,s=s,power_mod_q2=pow(5,w,q*q),power_mod_q_s_plus_one=pow(5,w,q**(s+1)),free_odd_factor_coordinates=[r for r in factor(w) if r>2 and r%4!=3],primality='exhaustive trial division')
def baseline()->dict:
    n=10_000_000;t=time.perf_counter()
    a=bytearray(b'\x01')*(n+1);a[:2]=b'\x00\x00'
    for p in range(2,math.isqrt(n)+1):
        if a[p]:a[p*p:n+1:p]=b'\x00'*((n-p*p)//p+1)
    count=total=digest=0;hits=[];mask=(1<<64)-1
    for q in range(3,n+1,4):
        if a[q]:
            count+=1;total+=q;r=pow(5,q-1,q*q)
            digest^=(r+q*0x9e3779b97f4a7c15)&mask
            if r==1:hits.append(q)
    return dict(limit=n,count=count,sum=total,digest=digest,hits=hits,seconds=time.perf_counter()-t)
def finish()->dict:
    sets=[]
    for alg in ['a','b']:
        rows=[json.loads(s) for s in (ROOT/f'results/scan_{alg}.jsonl').read_text().splitlines()]
        assert len(rows)==201 and rows[0]['lo']==0 and rows[-1]['hi']==2_000_000_000
        assert all(x['hi']+1==y['lo'] for x,y in zip(rows,rows[1:]))
        sets.append(rows)
    assert sets[0]==sets[1]
    rows=sets[0];hits=[q for row in rows for q in row['hits']]
    b=json.loads((ROOT/'results/python_baseline.json').read_text())
    # 10^7 is not prime, so the first block has the same mathematical content.
    assert {k:b[k] for k in ['count','sum','digest','hits']}=={k:rows[0][k] for k in ['count','sum','digest','hits']}
    summary=dict(limit=2_000_000_000,blocks=len(rows),candidate_count=sum(r['count'] for r in rows),candidate_sum=sum(r['sum'] for r in rows),hits=hits,new_admitted_hits=[q for q in hits if q>10_000_000],full_block_comparison='PASS',python_baseline_comparison='PASS',certificates=[certify(q) for q in hits])
    (ROOT/'results/scan_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary
if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='baseline':
        r=baseline();(ROOT/'results/python_baseline.json').write_text(json.dumps(r,indent=2)+'\n')
    else:r=finish()
    print(json.dumps(r,indent=2))
