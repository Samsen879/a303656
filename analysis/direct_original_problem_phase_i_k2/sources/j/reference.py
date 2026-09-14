#!/usr/bin/env python3
"""Exact, bounded Phase J checks. Requires Python 3.10+ and mpmath.
No network calls, repository mutations, or interval-wide n scan.
Integer results use exhaustive trial division and independent divisor/lattice checks.
Floating transforms use 70-digit arithmetic; the 3920 ratio is also interval evaluated.
"""
from __future__ import annotations
import argparse, json, math
from functools import lru_cache
from pathlib import Path
import mpmath as mp
PANEL = (3920, 358990, 410258, 530230, 9481394)
mp.mp.dps = 70
mp.iv.dps = 60

@lru_cache(None)
def factor(n: int) -> tuple[tuple[int,int],...]:
    if n < 1: raise ValueError('positive integer required')
    original=n; out=[]; p=2
    while p*p<=n:
        e=0
        while n%p==0: n//=p; e+=1
        if e: out.append((p,e))
        p=3 if p==2 else p+2
    if n>1: out.append((n,1))
    assert math.prod(p**e for p,e in out)==original
    return tuple(out)

def primes_to(n:int)->list[int]:
    return [p for p in range(2,n+1) if factor(p)==((p,1),)]

def chi(d:int)->int:
    return 0 if d%2==0 else (1 if d%4==1 else -1)

def divisors(n:int)->list[int]:
    ds=[1]
    for p,e in factor(n): ds=[d*p**j for d in ds for j in range(e+1)]
    return sorted(ds)

def bad(n:int)->list[int]:
    return [p for p,e in factor(n) if p%4==3 and e%2]

def oddpart(n:int)->int:
    return n//2**dict(factor(n)).get(2,0)

def local(n:int)->bool:
    return oddpart(n)%4==1 and dict(factor(n)).get(3,0)%2==0

def r2(n:int)->int:
    return 0 if bad(n) else 4*math.prod(e+1 for p,e in factor(n) if p%4==1)

def lattice_r2(n:int)->int:
    count=0
    for a in range(-math.isqrt(n),math.isqrt(n)+1):
        b2=n-a*a; b=math.isqrt(b2)
        if b*b==b2: count+=1 if b==0 else 2
    return count

def witness(n:int):
    for a in range(math.isqrt(n)+1):
        b=math.isqrt(n-a*a)
        if a*a+b*b==n:return [a,b]
    return None

def powers(base:int,cap:int)->list[int]:
    out=[]; x=1
    while x<=cap:out.append(x); x*=base
    return out

def grid(n:int,bulk=True):
    cap=n//4 if bulk else n-1
    for c,a in enumerate(powers(3,cap)):
        for d,b in enumerate(powers(5,cap)):
            m=n-a-b
            if m>0 and local(m):yield c,d,m

def transform(n:int,s,ctx=mp.mp):
    ans=ctx.mpf(1)
    for p,e in factor(n):
        if p==2:continue
        t=ctx.exp(-s*ctx.log(p)); eps=chi(p)
        ans*=sum((eps*t)**j for j in range(e+1))
    return ans

def nthrootceil(n:int,k:int)->int:
    x=math.isqrt(math.isqrt(n)) if k==4 else int(n**(1/k))
    while x**k<n:x+=1
    while (x-1)**k>=n:x-=1
    return x

def analyze(n:int)->dict:
    s=1/mp.log(n); z=nthrootceil(n,4); rows=[]
    for c,d,m in grid(n):
        f=factor(m); b=bad(m); o=oddpart(m); ds=divisors(o)
        R=r2(m); direct=sum(chi(h) for h in ds)
        small=sum(chi(h) for h in ds if h*h<o)
        square=chi(math.isqrt(o)) if math.isqrt(o)**2==o else 0
        assert R==4*direct==4*(2*small+square)==lattice_r2(m)
        assert len(b)%2==0 and 3 not in b
        S=int(all(p>z for p in b))
        large=[p for p,e in f if p%4==3 and p>z]
        B=len(large)*(len(large)-1)//2
        exact=S*(1-B); minor=S-B
        assert exact==int(R>0)
        assert minor<=int(R>0)
        if S and b:
            assert len(b)==2 and all(dict(f)[p]==1 for p in b)
            assert B==1 and not bad(m//(b[0]*b[1]))
        x=transform(m,s); y=transform(m,2*s)
        rho=y/x; psi=max(mp.mpf(0), (2-rho)/2)
        assert (psi>0)==(R>0) and psi<=int(R>0)
        assert rho <= mp.exp(mp.mpf('0.5')) if R else rho >= 4/mp.exp(mp.mpf('0.5'))
        rows.append(dict(c=c,d=d,m=m,factors=[[p,e] for p,e in f],oddpart=o,
            bad_primes=b,bad_kernel=math.prod(b),r2=R,witness=witness(m) if R else None,
            T_s=mp.nstr(x,62),T_2s=mp.nstr(y,62),ratio=mp.nstr(y/x,42),
            ML_gap=mp.nstr(y-2*x,42),hyperbola_small_sum=small,hyperbola_square_term=square,
            small_bad_survivor=S,large_pair_count=B,exact_pair_weight=exact,
            genuine_minorant=minor,ratio_witness_minorant=mp.nstr(psi,42)))
    D1=sum(mp.mpf(r['T_s']) for r in rows); D2=sum(mp.mpf(r['T_2s']) for r in rows)
    full=[dict(c=c,d=d,m=m,r2=r2(m),witness=witness(m)) for c,d,m in grid(n,False) if r2(m)>0]
    return dict(n=n,C=len(powers(3,n//4))-1,D=len(powers(5,n//4))-1,z=z,
        A23_count=len(rows),bulk_norm_pair_count=sum(r['r2']>0 for r in rows),
        bulk_norm_distinct_count=len({r['m'] for r in rows if r['r2']}),
        W=sum(r['r2'] for r in rows),ratio_minorant_sum=mp.nstr(sum(mp.mpf(r['ratio_witness_minorant']) for r in rows),42),D_s=mp.nstr(D1,62),D_2s=mp.nstr(D2,62),
        rho=mp.nstr(D2/D1,62),S_z=sum(r['small_bad_survivor'] for r in rows),
        P_z=sum(r['small_bad_survivor']*r['large_pair_count'] for r in rows),
        unweighted_large_pairs=sum(r['large_pair_count'] for r in rows),
        minorant_sum=sum(r['genuine_minorant'] for r in rows),rows=rows,
        full_positive_norm_pair_count=len(full),full_positive_witnesses=full)

def periodic_example()->dict:
    # Same residue modulo 120 preserves all divisibility data d<=5, L2 and L3 here.
    M=120; p=7; anchor=794
    x=next(x for x in range(anchor%M,M*p*p,M) if x%(p*p)==p)
    assert x%M==anchor%M and x%(p*p)==p and local(x) and not bad(anchor) and bad(x)
    assert [x%d==0 for d in range(1,6)]==[anchor%d==0 for d in range(1,6)]
    # Certify every residue class has a bad sample in each block of M p^2 integers.
    samples=[]
    for a in range(M):
        y=next(y for y in range(a,M*p*p,M) if y%(p*p)==p)
        assert y>0 and y%M==a and dict(factor(y)).get(p)==1
        samples.append(y)
    return dict(H=5,M=M,p=p,period=M*p*p,norm_anchor=anchor,nonnorm=x,
        anchor_factorization=factor(anchor),nonnorm_factorization=factor(x),
        all_120_classes_certified=True,max_sample=max(samples))

def support_stress()->dict:
    # Residual-level functional test only; NOT a representation search over targets n.
    total=0; nr=(mp.mpf(0),0); fr=(mp.inf,0)
    for m in range(1,4097):
        if oddpart(m)%4!=1:continue
        s=1/mp.log(max(m,2)); R=transform(m,2*s)/transform(m,s)
        norm=not bad(m); total+=1
        assert (R<2)==norm
        assert R<=mp.sqrt(mp.e) if norm else R>=4/mp.sqrt(mp.e)
        if norm and R>nr[0]:nr=(R,m)
        if not norm and R<fr[0]:fr=(R,m)
    M=120; a=1994; b=2114
    assert not bad(a) and bad(b) and local(a) and local(b)
    assert a%M==b%M and 1960<=a<=3920 and 1960<=b<=3920
    return dict(test_domain='L2-admissible residual integers 1<=m<=4096',
       cases=total,all_support_assertions_passed=True,
       largest_norm_ratio=dict(m=nr[1],ratio=mp.nstr(nr[0],42)),
       smallest_failed_ratio=dict(m=fr[1],ratio=mp.nstr(fr[0],42)),
       finite_interval_feature_collision=dict(interval=[1960,3920],M=M,
           norm_m=a,norm_factors=factor(a),norm_witness=witness(a),
           nonnorm_m=b,nonnorm_factors=factor(b)))

def main(out:Path)->None:
    results=[analyze(n) for n in PANEL]
    s=1/mp.iv.log(3920); dd1=mp.iv.mpf(0); dd2=mp.iv.mpf(0)
    for r in results[0]['rows']:
        dd1+=transform(r['m'],s,mp.iv);dd2+=transform(r['m'],2*s,mp.iv)
    ratio=dd2/dd1
    assert bool(ratio>mp.iv.mpf('2.74259591150304'))
    assert bool(ratio<mp.iv.mpf('2.74259591150305'))
    extra=dict(m=794,c=0,d=5,factors=factor(794),r2=r2(794),witness=witness(794),
        T_s=mp.nstr(transform(794,1/mp.log(3920)),62),
        T_2s=mp.nstr(transform(794,2/mp.log(3920)),62))
    x=mp.mpf(results[0]['D_s'])+mp.mpf(extra['T_s'])
    y=mp.mpf(results[0]['D_2s'])+mp.mpf(extra['T_2s'])
    extra['rho_after_adding_only_this_witness']=mp.nstr(y/x,62)
    # Countercheck unsafe square-root central sign: odd part 9 has chi(sqrt(9))=-1.
    assert sum(chi(d) for d in divisors(9))==1 and chi(3)==-1
    payload=dict(schema='a303656-phase-j-v1',panel=results,scope='five named targets only',
        proof_checks='exact trial factorization, divisor identity and exhaustive lattice counts',
        ratio_3920_interval=str(ratio),outside_bulk_witness=extra,
        periodic_minorant_counterexample=periodic_example(),support_stress=support_stress(),
        github_writes_performed='NONE')
    out.write_text(json.dumps(payload,indent=2)+'\n')
    for r in results:
        print({k:r[k] for k in ['n','C','D','A23_count','W','bulk_norm_pair_count','rho','z','S_z','P_z','minorant_sum','full_positive_norm_pair_count']})
    print('interval:',ratio);print('outside:',extra);print('periodic:',payload['periodic_minorant_counterexample'])
    print('All exact assertions passed; saved',out)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_name('results.json'))
    main(ap.parse_args().output)
