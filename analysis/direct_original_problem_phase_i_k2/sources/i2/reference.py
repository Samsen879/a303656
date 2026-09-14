#!/usr/bin/env python3
"""Exact, offline Phase I2 reference experiment. No repository or network writes.

Python 3.10+, NumPy, SymPy. Default B=10,000,000; no exponent logarithms
are used for enumeration. Run: python reference.py --out reproduction
Use --no-arrays to omit the optional per-n metrics archive.
All n arrays are indexed by n, include indices 0 and 1 (not conjecture cases),
and use 65535 as the missing pair-index sentinel. The pair table stores
(shift,c,d). min_residual(n) = n - pair_table[max_shift_index[n],0].

Factorization is performed only on the deterministic extremal panel and
independent audit samples, not on every residual in the entire interval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy

SHA = 'fd8aa2d5dd2cff758f2eb021c486ff9e2c3d1f38'
TREE = '325265d83abae42acadc59f8107d88d1375085be'
MISSING = 65535

def powers(base: int, limit: int) -> list[int]:
    result: list[int] = []
    x = 1
    while x <= limit:
        result.append(x)
        x *= base
    return result

def pairs_for(limit: int) -> list[tuple[int,int,int]]:
    return [(x+y,c,d) for c,x in enumerate(powers(3,limit))
            for d,y in enumerate(powers(5,limit)) if x+y <= limit]

def ipowlog(base: int, numerator: int, denominator: int = 1) -> int:
    """floor(log_base(numerator/denominator)), for numerator>=denominator>0."""
    assert numerator >= denominator > 0
    p, e = denominator, 0
    while p*base <= numerator:
        p *= base
        e += 1
    return e

def prime_trial(p: int) -> bool:
    if p < 2: return False
    if p % 2 == 0: return p == 2
    return all(p % d for d in range(3, math.isqrt(p)+1, 2))

def exact_factors(m: int) -> dict[int,int]:
    if m == 0: return {}
    f = {int(p):int(e) for p,e in sympy.factorint(m).items()}
    assert math.prod(p**e for p,e in f.items()) == m
    assert all(prime_trial(p) for p in f)
    return dict(sorted(f.items()))

def norm_from_factors(m: int, f: dict[int,int]) -> bool:
    return m == 0 or all(p%4 != 3 or e%2 == 0 for p,e in f.items())

def local23(m: int) -> tuple[bool,bool]:
    if m == 0: return True, True  # exact zero norm, no finite v_p(0)
    odd = m
    while odd % 2 == 0: odd //= 2
    v, t = 0, m
    while t % 3 == 0: v += 1; t //= 3
    return odd%4 == 1, v%2 == 0

def lambda23(n: int) -> Fraction:
    if n%3 == 0: return Fraction(1,2)
    if n%2: return Fraction(5,16)
    return Fraction(7,32) if n%24 in (2,4,8,22) else Fraction(13,32)

def square_pairs(m: int) -> list[list[int]]:
    out = []
    for a in range(math.isqrt(m//2)+1):
        b = math.isqrt(m-a*a)
        if a*a+b*b == m: out.append([a,b])
    return out

def hash_array(a: np.ndarray) -> str:
    return hashlib.sha256(a.astype(a.dtype.newbyteorder('<'),copy=False).tobytes()).hexdigest()

def longest_run(r: np.ndarray, lo: int, hi: int, k: int) -> dict:
    f = r[lo:hi+1] <= k
    d = np.diff(np.concatenate(([False], f, [False])).astype(np.int8))
    starts, ends = np.flatnonzero(d==1), np.flatnonzero(d==-1)
    if len(starts)==0: return dict(lo=lo,hi=hi,threshold=k,length=0,first_interval=None)
    lengths = ends-starts
    j = int(lengths.argmax())
    return dict(lo=lo,hi=hi,threshold=k,length=int(lengths[j]),
                first_interval=[int(lo+starts[j]),int(lo+ends[j]-1)],
                tied_run_count=int(np.count_nonzero(lengths==lengths[j])))

def torus_checks() -> list[dict]:
    out = []
    for k2,k3 in [(5,2),(7,4),(8,5)]:
        q2,q3 = 2**k2,3**k3
        tc,td = 2**(k2-2),2**(k2-2)*3**(k3-1)
        c2 = np.array([pow(3,j,q2) for j in range(tc)])[:,None]
        d2 = np.array([pow(5,j,q2) for j in range(td)])[None,:]
        d3 = np.array([pow(5,j,q3) for j in range(td)])[None,:]
        def l2(x: int) -> int:
            if x % 2**(k2-1) == 0: return -1
            while x%2 == 0: x //= 2
            return int(x%4==1)
        def l3(x: int) -> int:
            if x == 0: return -1
            v = 0
            while x%3 == 0: v += 1; x //= 3
            return int(v%2==0)
        t2,t3 = np.array([l2(x) for x in range(q2)]),np.array([l3(x) for x in range(q3)])
        rows = []
        # Representatives, plus nontrivial lifts of each mod-24 class.
        for n in list(range(24))+[r+24*137 for r in range(24)]:
            a,b = t2[(n-c2-d2)%q2], t3[(n-d3)%q3]
            lower = int(np.count_nonzero((a==1)&(b==1)))
            upper = int(np.count_nonzero((a!=0)&(b!=0)))
            lam = lambda23(n)
            assert Fraction(lower,tc*td) <= lam <= Fraction(upper,tc*td)
            rows.append(dict(n=n,lower_count=lower,upper_count=upper,
                             cells=tc*td,lambda_num=lam.numerator,lambda_den=lam.denominator))
        out.append(dict(k2=k2,k3=k3,c_period=tc,d_period=td,checks=rows))
    return out

def gap_and_nearshift_checks() -> dict:
    gaps = []
    for k in range(2,19):
        X = 10**k
        vals = sorted({s for s,c,d in pairs_for(2*X) if X <= s <= 2*X}|{X,2*X})
        widths = [(b-a,a,b) for a,b in zip(vals,vals[1:])]
        w,a,b = max(widths)
        assert 20*w >= X
        gaps.append(dict(X=X,left=a,right=b,empty_open_length=w,
                         endpoints_may_be_shifts=True))
    near = []
    for X in (100,1000,10000,1000000):
        ss = sorted({s for s,c,d in pairs_for(2*X)})
        for H in sorted({1,max(1,math.isqrt(X)),max(1,X//100),X//2}):
            ints = [(max(X,s),min(2*X,s+H)) for s in ss if s<=2*X and s+H>=X]
            total, last = 0, X-1
            for a,b in ints:
                a = max(a,last+1)
                if a<=b: total += b-a+1; last=b
            bound = 4*(2*H+1)+2*(H+1)*(ipowlog(3,2*X,H)+ipowlog(5,2*X,H)+2)
            assert total <= bound
            near.append(dict(X=X,H=H,exact_union_count=total,proved_upper_bound=bound))
    return dict(macroscopic_gap_checks=gaps,nearshift_bound_checks=near)

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound',type=int,default=10_000_000)
    ap.add_argument('--out',type=Path,default=Path('.'))
    ap.add_argument('--no-arrays',action='store_true')
    args = ap.parse_args()
    B = args.bound
    if not 100 <= B <= 10_000_000:
        ap.error('This audited implementation permits 100 <= bound <= 10,000,000; no unreviewed scale extension.')
    args.out.mkdir(parents=True,exist_ok=True)
    pairs = pairs_for(B)
    assert len(pairs) < MISSING
    # Exact first method: unordered lattice enumeration, independent of factoring.
    u = np.zeros(B+1,dtype=np.uint16)
    sq = np.arange(math.isqrt(B)+1,dtype=np.int64)**2
    for a in range(math.isqrt(B//2)+1):
        u[a*a+sq[a:math.isqrt(B-a*a)+1]] += 1
    b = u>0
    R,A,Rc0,Rd0,Rgreedy = [np.zeros(B+1,dtype=np.uint32) for _ in range(5)]
    lex = np.full(B+1,MISSING,dtype=np.uint16)
    smallest = lex.copy();largest = lex.copy()
    # Greedy residual square decomposition: larger coordinate floor(sqrt(m)).
    greedy = np.zeros(B+1,dtype=bool)
    for a in range(math.isqrt(B)+1):
        upper = min(B,(a+1)**2-1)-a*a
        js = sq[:math.isqrt(upper)+1]
        greedy[a*a+js] = True
    assert np.all(~greedy | b)
    for i,(s,c,d) in enumerate(pairs):
        mask = b[:B+1-s]
        R[s:] += mask; A[s:] += u[:B+1-s]
        Rgreedy[s:] += greedy[:B+1-s]
        if c==0: Rc0[s:] += mask
        if d==0: Rd0[s:] += mask
        target = lex[s:]
        np.copyto(target,i,where=mask & (target==MISSING))
    for i in sorted(range(len(pairs)),key=lambda i:(pairs[i][0],pairs[i][1:])):
        s,c,d = pairs[i];mask=b[:B+1-s]
        t=smallest[s:]
        np.copyto(t,i,where=mask & (t==MISSING))
        np.copyto(largest[s:],i,where=mask)
    D=np.zeros(B+1,dtype=np.uint32)
    for s in sorted({s for s,c,d in pairs}): D[s:]+=b[:B+1-s]
    assert int(max(R.max(),A.max(),D.max(),Rc0.max(),Rd0.max(),Rgreedy.max()))<65535
    R,A,D,Rc0,Rd0,Rgreedy=[x.astype(np.uint16) for x in (R,A,D,Rc0,Rd0,Rgreedy)]
    assert np.array_equal(R>0, A>0) and np.array_equal(R>0,D>0)
    assert np.all((lex==MISSING)==(R==0))
    assert np.all((smallest==MISSING)==(R==0)) and np.all((largest==MISSING)==(R==0))
    # Audit against independent trial-validated factorizations and OEIS initial terms.
    independent=[]
    sample=set(range(min(B,5000)+1));state=303656
    for _ in range(1000):
        state=(1664525*state+1013904223)&0xffffffff
        sample.add(state%(B+1))
    for m in sorted(sample):
        assert bool(b[m])==norm_from_factors(m,exact_factors(m))
    oeis90=[0,1,1,2,1,3,2,3,2,4,3,4,2,4,4,3,2,4,4,3,2,4,3,4,1,4,5,6,4,6,5,5,6,6,5,8,4,6,6,5,4,7,5,7,5,6,4,5,3,4,7,6,7,8,5,4,7,5,5,9,3,6,5,6,4,6,5,7,7,4,5,5,5,4,6,5,6,10,5,4,5,7,4,9,2,9,8,5,6,6]
    assert A[1:91].tolist()==oeis90
    ranges=[(2,99),(100,999),(1000,9999),(10000,99999),(100000,999999),
            (1000000,9999999),(5000000,10000000)]
    summaries=[];panel={2,3,5,25,560}
    for lo,hi in ranges:
        hi=min(hi,B)
        if lo>hi: continue
        r=R[lo:hi+1]; aa=A[lo:hi+1]
        mn=int(r.min());ids=np.flatnonzero(r==mn)+lo
        panel.update(int(n) for n in ids[:5])
        summaries.append(dict(lo=lo,hi=hi,rows=hi-lo+1,min_successful_pairs=mn,
            argmin_count=len(ids),argmin_first=ids[:30].tolist(),
            min_unordered_representations=int(aa.min()),
            sum_successful_pairs=int(r.sum(dtype=np.uint64)),
            mean_successful_pairs=float(r.mean()),mean_unordered_representations=float(aa.mean())))
    if B>=100000:
        panel.update(int(n) for n in np.flatnonzero(R[100000:]<=3)+100000)
    panel=sorted(n for n in panel if n<=B)
    fullpanel=[]
    for n in panel:
        rows=[];winners=[];hist=Counter();L23=0;bulkL23=0;bulkR=0;bulkN=0
        for s,c,d in pairs:
            if s>n: continue
            m=n-s;f=exact_factors(m)
            bad=[[p,e] for p,e in f.items() if p%4==3 and e%2]
            ok=not bad if m>0 else True
            l2,l3=local23(m);L23+=int(l2 and l3)
            if 3**c<=n//4 and 5**d<=n//4:
                bulkN+=1;bulkL23+=int(l2 and l3);bulkR+=int(ok)
            rec=dict(c=c,d=d,shift=s,residual=m,factors=[[p,e] for p,e in f.items()],
                     odd_bad_prime_valuations=bad,local2=l2,local3=l3,success=ok)
            if ok:
                rec['unordered_square_pairs']=square_pairs(m)
                assert len(rec['unordered_square_pairs'])==int(u[m])
                winners.append(rec.copy())
            else: hist[bad[0][0]]+=1
            rows.append(rec)
        assert len(winners)==int(R[n])
        assert sum(len(w['unordered_square_pairs']) for w in winners)==int(A[n])
        assert len({w['shift'] for w in winners})==int(D[n])
        def record_of(index: np.ndarray):
            i=int(index[n])
            if i==MISSING: return None
            s,c,d=pairs[i]
            assert norm_from_factors(n-s,exact_factors(n-s))
            return dict(c=c,d=d,shift=s,residual=n-s)
        if winners:
            assert pairs[int(lex[n])][1:]==min((w['c'],w['d']) for w in winners)
            assert pairs[int(smallest[n])][0]==min(w['shift'] for w in winners)
            assert pairs[int(largest[n])][0]==max(w['shift'] for w in winners)
        fullpanel.append(dict(n=n,n_mod24=n%24,n_mod72=n%72,active_pairs=len(rows),
             successful_pairs=int(R[n]),distinct_winning_shifts=int(D[n]),unordered_representations=int(A[n]),
             lexicographically_first=record_of(lex),smallest_winning_shift=record_of(smallest),
             minimum_successful_residual=record_of(largest),local23_survivors=L23,
             bulk_rectangle=dict(active=bulkN,local23_survivors=bulkL23,successful_pairs=bulkR),
             smallest_bad_prime_histogram=dict(sorted(hist.items())),winners=winners,all_pair_rows=rows))
    cls=[]
    lo=1_000_000 if B>=1_000_000 else 2
    for residue in range(24):
        first=lo+(residue-lo)%24
        rr=R[first:B+1:24]
        if rr.size:
            lam=lambda23(residue)
            cls.append(dict(residue=residue,lo=lo,hi=B,rows=len(rr),mean=float(rr.mean()),
                            minimum=int(rr.min()),lambda_num=lam.numerator,lambda_den=lam.denominator))
    runs=[]
    for lo in (2,1_000_000):
        if lo<=B:
            for k in (3,5,10):runs.append(longest_run(R,lo,B,k))
    blocks=[]
    if B>=1_000_000:
        start=1_000_000;usable=(B-start+1)//1000*1000
        mins=R[start:start+usable].reshape(-1,1000).min(axis=1)
        unique,counts=np.unique(mins,return_counts=True)
        blocks=dict(start=start,width=1000,blocks=len(mins),minima_histogram=dict(zip(map(int,unique),map(int,counts))))
    restriction={}
    for label,arr in [('c_zero',Rc0),('d_zero',Rd0),('greedy_largest_square',Rgreedy)]:
        failures=np.flatnonzero(arr[2:]==0)+2
        restriction[label]=dict(uncovered_count=len(failures),first_failures=failures[:20].tolist(),
                                represented_count=B-1-len(failures))
    arrays=dict(pair_count=R,unordered_representations=A,distinct_shift_count=D,
                lex_first_index=lex,min_shift_index=smallest,max_shift_index=largest,
                c_zero_count=Rc0,d_zero_count=Rd0,greedy_count=Rgreedy,
                pair_table=np.array(pairs,dtype=np.int64))
    metadata={name:dict(shape=list(a.shape),dtype=str(a.dtype),little_endian_data_sha256=hash_array(a)) for name,a in arrays.items()}
    if not args.no_arrays:
        np.savez_compressed(args.out/'per_n_metrics.npz',**arrays)
    results=dict(task='A303656 direct additive reset Phase I2',bound=B,inclusive_domain=[2,B],
        authority=dict(repository='Samsen879/a303656',main_sha=SHA,tree_sha=TREE,
                       github_writes='NONE',frozen_zip_bytes_read=False),
        classifications=dict(level='D',direct_progress='YES: scoped route exclusions and local count, not global support',
            all_sufficiently_large='NOT PROVED',effective_finite_threshold=None,
            new_exceptional_set_structure=False,codex_large_computation_justified=False,A303656='UNRESOLVED'),
        definitions=dict(pair_count='successful (c,d), including m=0; equals A303429 convention',
            unordered_representations='all (a,b,c,d), 0<=a<=b; A303656 convention',
            min_residual='n - pair_table[max_shift_index[n],0]',
            sentinel=MISSING,full_factorization_scope='deterministic extremal panel and independent residual audit samples only'),
        environment=dict(python=platform.python_version(),numpy=np.__version__,sympy=sympy.__version__),
        active_pairs_at_bound=len(pairs),distinct_shifts_at_bound=len({s for s,c,d in pairs}),
        collisions=[dict(shift=s,pairs=[[c,d] for t,c,d in pairs if t==s])
                    for s,k in sorted(Counter(s for s,c,d in pairs).items()) if k>1],
        counterexample_count=int(np.count_nonzero(R[2:]==0)),last_pair_count_one=np.flatnonzero(R==1)[-30:].tolist(),
        interval_summaries=summaries,low_count_n_ge_100000=[int(n) for n in np.flatnonzero(R[100000:]<=3)+100000] if B>=100000 else [],
        extremal_panel=fullpanel,mod24_statistics=cls,longest_low_count_runs=runs,
        block_minima=blocks,restricted_subclasses=restriction,
        theorem_checks=dict(local_torus=torus_checks(),**gap_and_nearshift_checks()),
        audit=dict(independent_factor_criterion_samples=len(sample),oeis_first_90='PASS',
                   panel_full_pair_factorizations='PASS',pair_support_equals_weighted_support='PASS',
                   finite_torus_brackets='PASS',macroscopic_gap_tests='PASS',nearshift_union_tests='PASS'),
        per_n_arrays=metadata)
    (args.out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(bound=B,counterexamples=results['counterexample_count'],panel_size=len(panel),audit=results['audit']),indent=2))

if __name__=='__main__': main()
