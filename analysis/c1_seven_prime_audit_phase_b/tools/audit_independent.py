"""Fresh exact checks. Does NOT import source-package or repository reference code.
Finite tests support, but do not replace, SEVEN_PRIME_INDEPENDENT_PROOF.md.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from fractions import Fraction
from functools import lru_cache
from math import gcd, lcm
from pathlib import Path
import json, random, time
ROOT=Path(__file__).resolve().parents[1]

def factors(n:int)->dict[int,int]:
    ans={};d=2
    while d*d<=n:
        while n%d==0:ans[d]=ans.get(d,0)+1;n//=d
        d=3 if d==2 else d+2
    if n>1:ans[n]=ans.get(n,0)+1
    return ans

def ord5(q:int)->int:
    w=q-1
    for p in factors(w):
        while w%p==0 and pow(5,w//p,q)==1:w//=p
    return w

def arithmetic()->dict:
    # Derive cyclotomic values by exact divisor recursion, not a hard-coded product.
    @lru_cache(None)
    def cyclo(n:int)->int:
        v=5**n-1
        for d in range(1,n):
            if n%d==0:
                h=cyclo(d);assert v%h==0;v//=h
        return v
    out=[]
    for m in [3,6,9,18,5,10]:
        v=cyclo(m);fs=factors(v);rows=[]
        for q,e in fs.items():
            w=ord5(q);s=1
            while pow(5,w,q**(s+1))==1:s+=1
            rows.append(dict(q=q,multiplicity=e,order=w,s=s,admitted=q%4==3))
        out.append(dict(m=m,cyclotomic_value=v,primes=rows))
    heads={}
    for d in [1,2]:
        heads[str(d)]=sorted(row['q'] for rec in out if rec['m'] in [3**d,2*3**d]
                     for row in rec['primes'] if row['admitted'] and row['order']==rec['m'])
    assert heads=={'1':[7,31],'2':[19,5167]}
    five=sorted(row['q'] for rec in out if rec['m'] in [5,10]
                for row in rec['primes'] if row['admitted'] and row['order']==rec['m'])
    assert five==[11,71]
    assert all(row['s']==1 for rec in out for row in rec['primes'] if row['admitted'] and row['order']==rec['m'])
    return dict(factorizations=out,rank3_heads=heads,rank5_3free_depth1_heads=five)

def boundary(max_K:int=12)->dict:
    count=parities=0
    for K in range(2,max_K+1):
        mod=1<<K
        squares={a*a%mod for a in range(mod)}
        sums={(a+b)%mod for a in squares for b in squares}
        t=1<<(K-2)
        logs={pow(5,d,mod):d for d in range(t)}
        assert len(logs)==t
        for r in range(mod):
            c=1 if r%4 in [0,1] else 0
            targets=[0,4] if r%2==0 else [1,5]
            if K==2:
                for b in [0,1]:
                    assert (r-3**c-pow(5,b,mod))%mod in sums
                    parities+=1
            else:
                ds=[logs[(r-3**c-T)%mod] for T in targets]
                assert {d%2 for d in ds}=={0,1}
                for d in ds:
                    assert (r-3**c-pow(5,d,mod))%mod in sums
                    parities+=1
            count+=1
    # At q=3 a frozen residue/anchor is divisible on at most one exponent parity.
    for K in [2,3,4]:
        for r in range(3**K):
            for c in [0,1]:
                assert sum((r-3**c-pow(5,b,3))%3==0 for b in [0,1])<=1
    return dict(K_min=2,K_max=max_K,residues=count,parity_witnesses=parities,mismatches=0,method='direct square-sum residue sets and discrete log dictionary')

def cmask(p:int,beta:int,depth:int,pos:int)->int:
    m=p**depth
    return sum(1<<x for x in range(pos%m,p**beta,m))

def dmask(p:int,beta:int,center:int,J:tuple[int,...])->int:
    ans=0
    for x in range(p**beta):
        a=(x-center)%(p**beta)
        if a==0:continue
        v=0
        while a%p==0:v+=1;a//=p
        if v in J:ans|=1<<x
    return ans

def shellsets(beta:int):
    yield ()
    for parity in [0,1]:
        ids=list(range(parity,beta,2))
        for i in range(1,len(ids)+1):yield from combinations(ids,i)

def sparse_geometry()->dict:
    cases=[]
    # Complete subset enumeration in each declared finite grammar, all centers.
    for p,beta in [(3,1),(3,2),(3,3),(5,1),(5,2),(7,1)]:
        cylinders=[(d,a,cmask(p,beta,d,a)) for d in range(1,beta+1) for a in range(p**d)]
        configs=[(z,J,dmask(p,beta,z,J)) for z in range(p**beta) for J in shellsets(beta)]
        full=(1<<(p**beta))-1;tests=0
        for n in range(p):
            for ids in combinations(range(len(cylinders)),n):
                U=0;first=set()
                for i in ids:
                    d,a,mask=cylinders[i];U|=mask
                    if d==1:first.add(a)
                for z,J,D in configs:
                    assert (D|U==full)==(0 in J and z%p in first)
                    tests+=1
        cases.append(dict(p=p,beta=beta,distinct_cylinders=len(cylinders),tests=tests))
    # Regression: parity and the proper-center proviso really matter.
    badJ=(0,1);p=3;beta=2
    assert dmask(p,beta,0,badJ)|cmask(p,beta,2,0)==(1<<9)-1
    assert dmask(3,2,0,(0,))!=(1<<9)-1
    return dict(cases=cases,total=sum(c['tests'] for c in cases),mismatches=0,out_of_class_counterexample=dict(p=3,beta=2,J=[0,1],rigid_depth=2,rigid_position=0))

def shallow_three()->dict:
    histogram=Counter();best=None
    for a,b in product(range(3),repeat=2):
        for c,d in product(range(9),repeat=2):
            union=cmask(3,2,1,a)|cmask(3,2,1,b)|cmask(3,2,2,c)|cmask(3,2,2,d)
            size=union.bit_count();histogram[size]+=1
            if size==8:best=[a,b,c,d]
            assert size<=8
    # Exhaust every complete ternary tree with <=7 leaves, retaining positions.
    level={((0,0),)};seen=set();proper=[]
    while level:
        frontier=level.pop()
        if frontier in seen:continue
        seen.add(frontier)
        leaves=len(frontier)
        if leaves>1:
            deepest=max(d for d,a in frontier)
            assert leaves>=1+2*deepest
            assert sum((Fraction(1,3**d) for d,a in frontier),Fraction())==1
            proper.append((leaves,deepest))
        if leaves+2<=7:
            for idx,(d,a) in enumerate(frontier):
                new=list(frontier);new.pop(idx)
                new.extend((d+1,a+j*3**d) for j in range(3))
                level.add(tuple(sorted(new)))
    assert min(n for n,d in proper if d>=3)==7
    return dict(head_placements=729,union_size_histogram=dict(histogram),max_union='8/9',max_example=best,complete_frontiers_including_root=len(seen),min_leaves_at_depth3=7)

def five_witnesses()->dict:
    masks=[cmask(5,2,d,a) for d in [1,2] for a in range(5**d)]
    full=(1<<25)-1;out=[]
    # Repeated positions correspond to distinct seed identities, NOT a shared seed.
    for n in [5,6]:
        count=complete=max_witnesses=0;hist=Counter()
        for ids in combinations_with_replacement(range(30),n):
            count+=1;union=0
            for i in ids:union|=masks[i]
            if union!=full:continue
            complete+=1;minimal=[]
            for bits in range(1,1<<n):
                u=0
                for i in range(n):
                    if bits>>i&1:u|=masks[ids[i]]
                if u!=full:continue
                redundant=False
                for i in range(n):
                    if not(bits>>i&1):continue
                    v=0
                    for j in range(n):
                        if j!=i and bits>>j&1:v|=masks[ids[j]]
                    if v==full:redundant=True;break
                if not redundant:minimal.append(bits)
            assert all(bits.bit_count()==5 for bits in minimal)
            assert all(all(ids[i]<5 for i in range(n) if bits>>i&1) for bits in minimal)
            assert len(minimal)<=n-4
            max_witnesses=max(max_witnesses,len(minimal));hist[len(minimal)]+=1
        out.append(dict(n=n,multisets=count,full=complete,max_minimal_witnesses=max_witnesses,witness_count_histogram=dict(hist)))
    # Every possible pair of fixed 3-free helper positions covers <=2/5.
    for a,b in product(range(5),repeat=2):assert len({a,b})<5
    return dict(grammar='depth 1 or 2 cylinders in Z/25; distinct source identities may repeat geometry',cases=out,total_multisets=sum(x['multisets'] for x in out),mismatches=0)

def join(g:dict[int,tuple[int,int]],h:dict[int,tuple[int,int]]):
    out=dict(g)
    for p,(e,b) in h.items():
        if p in out:
            f,a=out[p]
            if (a-b)%(p**min(e,f)):return None
            if e>f:out[p]=(e,b)
        else:out[p]=(e,b)
    return out

def guards()->dict:
    opts=[{}]+[{3:(d,a)} for d in range(1,4) for a in range(3**d)]
    tests=0
    def points(g):
        return {x for x in range(27) if all(x%(p**d)==a for p,(d,a) in g.items())}
    for g,h in product(opts,repeat=2):
        out=join(g,h);truth=points(g)&points(h)
        assert (set() if out is None else points(out))==truth
        if out is not None and (g or h):assert out and len(truth)<=9
        tests+=1
    return dict(pair_intersections=tests,mismatches=0)

def abstract_linear()->dict:
    rng=random.Random(260906)
    stats=Counter()
    for trial in range(1200):
        # Fixed lower product Z/3 x Z/5 and top Z/7, not an actual arithmetic system.
        p=7;lower=list(product(range(3),range(5)));n=rng.randrange(7)
        seeds=[]
        for i in range(n):
            guard={j:rng.randrange(m) for j,m in enumerate([3,5]) if rng.randrange(2)}
            seeds.append((i,guard,rng.randrange(7)))
        H={j:rng.randrange(m) for j,m in enumerate([3,5]) if rng.randrange(2)}
        zeta=rng.randrange(7);active=bool(rng.randrange(2))
        def match(g,y):return all(y[j]==v for j,v in g.items())
        children=[(i,g) for i,g,z in seeds if active and z==zeta]
        # Intersection with H is tested semantically; origins remain injective.
        assert len({i for i,g in children})==len(children)<=n
        for y in lower:
            direct=all((active and match(H,y) and z!=zeta) or any(match(g,y) and z==a for i,g,a in seeds) for z in range(7))
            residual=any(match(H,y) and match(g,y) for i,g in children)
            assert direct==residual
            stats['fiber_comparisons']+=1
        stats['states']+=1
    return dict(stats,mismatches=0,scope='abstract sparse guarded-cylinder states, not prime realizations')

def row_normal_forms()->dict:
    full_tests=coarse_tests=0
    configs=[(3,K,None) for K in range(2,6)]+[(7,2,None),(7,3,None),(11,2,None),(20771,2,[0,2,20775,13471])]
    for q,K,residues in configs:
        M=q**K;w=ord5(q);s=1
        while pow(5,w,q**(s+1))==1:s+=1
        a=max(0,K-s);period=w*q**a
        values=[];v=1
        for d in range(period):values.append(v);v=v*5%M
        assert v==1 and len(set(values))==period
        logfull={v:d for d,v in enumerate(values)}
        logmod={pow(5,d,q):d for d in range(w)}
        odd=list(range(1,K,2));accepted=[set(E) for n in range(1,len(odd)+1) for E in combinations(odd,n)]
        def valuation(v,cap):
            if v==0:return cap
            j=0
            while j<cap and v%q==0:j+=1;v//=q
            return j
        for r in range(M) if residues is None else residues:
            for c in [0,1]:
                t=(r-3**c)%M;lower=logmod.get(t%q)
                h=K if lower is None else valuation((t-values[lower])%M,K)
                kind='inert' if lower is None else ('rigid' if h<min(s,K) else ('dynamic' if t in logfull and a>0 else 'inert'))
                center=logfull.get(t,0)
                vals=[valuation((t-v)%M,K) for v in values]
                for E in accepted:
                    fatal=[h0 in E and h0<K for h0 in vals]
                    for d,actual in enumerate(fatal):
                        pred=False
                        if lower is not None and d%w==lower:
                            if kind=='rigid':pred=h in E
                            elif kind=='dynamic':
                                j=valuation((d-center)%(q**a),a)
                                pred=j<a and s+j in E
                        assert pred==actual
                        full_tests+=1
                    for beta in range(a+1):
                        U=w*q**beta
                        for x in range(U):
                            actual=all(fatal[x::U]);pred=False
                            if lower is not None and x%w==lower:
                                if kind=='rigid':pred=h in E
                                elif kind=='dynamic':
                                    j=valuation((x-center)%(q**beta),beta)
                                    pred=j<beta and s+j in E
                            assert pred==actual
                            coarse_tests+=1
    return dict(full_event_comparisons=full_tests,coarse_forall_comparisons=coarse_tests,mismatches=0,configs=[dict(q=q,K=K,residues='all' if R is None else R) for q,K,R in configs])

def run()->dict:
    result={}
    for name,fn in [('arithmetic',arithmetic),('row_normal_forms',row_normal_forms),('boundary',boundary),('sparse_geometry',sparse_geometry),('shallow_three',shallow_three),('five_witnesses',five_witnesses),('guard_intersections',guards),('abstract_linear',abstract_linear)]:
        start=time.perf_counter();r=fn();r['seconds']=time.perf_counter()-start
        (ROOT/f'results/audit_{name}.json').write_text(json.dumps(r,indent=2)+'\n');result[name]=r
        print(name,'PASS',round(r['seconds'],4),flush=True)
    return result
if __name__=='__main__':run()
