#!/usr/bin/env python3
"""Exact, standalone Phase-B laboratory. Python standard library only.

These routines test finite identities, not the universal mathematical theorem.
Original-resource IDs and descended geometric cylinders are deliberately separate.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import comb, gcd, isqrt, lcm
from pathlib import Path
import argparse, json, time


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, isqrt(n)+1, 2))


def factors(n: int) -> dict[int, int]:
    out = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0)+1; n //= d
        d = 3 if d == 2 else d+2
    if n > 1: out[n] = out.get(n, 0)+1
    return out


def order5(q: int) -> int:
    if not is_prime(q) or q == 5: raise ValueError("Expected a prime different from 5")
    w = q-1
    for p in factors(w):
        while w % p == 0 and pow(5, w//p, q) == 1: w //= p
    return w


def lift_s(q: int, w: int) -> int:
    s = 0; mod = q
    while pow(5, w, mod) == 1:
        s += 1; mod *= q
    return s


@dataclass(frozen=True, order=True)
class Cylinder:
    depth: int
    residue: int

    def norm(self, p: int) -> 'Cylinder':
        if self.depth < 0: raise ValueError("Negative depth")
        return Cylinder(self.depth, self.residue % (p**self.depth))

    def contains(self, p: int, other: 'Cylinder') -> bool:
        return self.depth <= other.depth and (other.residue-self.residue) % (p**self.depth) == 0


def cylinder_mask(p: int, beta: int, c: Cylinder) -> int:
    if not 0 <= c.depth <= beta: raise ValueError("Cylinder depth outside ambient domain")
    return sum(1 << x for x in range(c.residue % (p**c.depth), p**beta, p**c.depth))


def shell_mask(p: int, beta: int, center: int, J: tuple[int, ...]) -> int:
    ans = 0
    for x in range(p**beta):
        diff = (x-center) % (p**beta)
        if diff == 0: continue
        v = 0
        while diff % p == 0: v += 1; diff //= p
        if v in J: ans |= 1 << x
    return ans


def shell_cylinders(p: int, beta: int, center: int, J: tuple[int, ...]) -> list[Cylinder]:
    out=[]
    for j in J:
        if not 0 <= j < beta: raise ValueError("Shell index outside ambient domain")
        old = center % (p**j); digit = (center//(p**j)) % p
        out += [Cylinder(j+1, old+t*p**j) for t in range(p) if t != digit]
    return out


def antichain(p: int, cs: list[Cylinder]) -> list[Cylinder]:
    result=[]
    for c in sorted(set(c.norm(p) for c in cs)):
        if not any(a.contains(p, c) for a in result): result.append(c)
    return result


def union_measure(p: int, cs: list[Cylinder]) -> Fraction:
    return sum((Fraction(1, p**c.depth) for c in antichain(p, cs)), Fraction())


def intersection_measure(p: int, B: Cylinder, cs: list[Cylinder]) -> Fraction:
    inside=[]
    for c in cs:
        if c.contains(p, B): return Fraction(1, p**B.depth)
        if B.contains(p, c): inside.append(c)
    return union_measure(p, inside)


def centered_full(p: int, beta: int, center: int, J: tuple[int, ...],
                  F: tuple[int, ...], rigid: list[Cylinder]) -> bool:
    """Position-exact theorem, with blockers geometric only, not prime resources."""
    cs = antichain(p, rigid+[Cylinder(1, f) for f in F])
    centered = [c.depth for c in cs if (center-c.residue) % (p**c.depth) == 0]
    if not centered: return False
    e = min(centered)
    for j in range(e):
        if j in J: continue
        old = center % (p**j); digit = (center//(p**j)) % p
        for t in range(p):
            if t == digit: continue
            B = Cylinder(j+1, old+t*p**j)
            if intersection_measure(p, B, cs) != Fraction(1, p**B.depth): return False
    return True


def allowed_shell_sets(beta: int):
    out = {()}
    for parity in (0,1):
        indices = list(range(parity, beta, 2))
        for k in range(1, len(indices)+1): out.update(combinations(indices,k))
    return sorted(out)


def local_audit(p: int, beta: int, max_r: int, all_blockers: bool = False):
    cs=[Cylinder(d,a) for d in range(1,beta+1) for a in range(p**d)]
    masks=[cylinder_mask(p,beta,c) for c in cs]
    full=(1 << (p**beta))-1
    sparse_cases=full_cases=criterion_cases=hybrid_cases=0
    Js=allowed_shell_sets(beta)
    Fsets=[tuple(f for f in range(p) if n >> f & 1) for n in range(1<<p)] if all_blockers else [()]
    Fmasks={F: sum(cylinder_mask(p,beta,Cylinder(1,f)) for f in F) for F in Fsets}
    for n in range(max_r+1):
        for ix in combinations(range(len(cs)),n):
            R=[cs[i] for i in ix]; rm=0
            for i in ix: rm |= masks[i]
            for J in Js:
                dm=shell_mask(p,beta,0,J)
                covered=(dm|rm)==full
                if n < p:
                    sparse_cases += 1
                    simple=(0 in J and Cylinder(1,0) in R)
                    if covered != simple:
                        raise AssertionError(("Sparse lemma",p,beta,J,R,covered,simple))
                    full_cases += covered
                for F in Fsets:
                    truth=(dm|rm|Fmasks[F])==full
                    assert centered_full(p,beta,0,J,F,R)==truth
                    criterion_cases += 1
                    # One active dynamic bundle, nonnegative rigid union upper bound.
                    mass=Fraction(len(F),p)+Fraction(dm.bit_count(),p**beta)+sum((Fraction(1,p**c.depth) for c in R),Fraction())
                    if mass < 1:
                        assert not truth
                        hybrid_cases += 1
    return dict(p=p,beta=beta,max_r=max_r,sparse_cases=sparse_cases,
                sparse_full_cases=full_cases,centered_criterion_cases=criterion_cases,
                strict_hybrid_cases=hybrid_cases,mismatches=0,centers="0; translation-equivariant")


def safe_anchor_and_targets(r: int):
    c = 1 if r % 4 in (0,1) else 0
    targets = (0,4) if r % 2 == 0 else (1,5)
    return c,targets


def boundary_audit(Kmax=9):
    cases=checks=0
    for K in range(2,Kmax+1):
        M=2**K; T=1 if K==2 else 2**(K-2)
        sq={x*x % M for x in range(M)}
        sums={(a+b)%M for a in sq for b in sq}
        ps=[pow(5,d,M) for d in range(lcm(2,T))]
        for r in range(M):
            c,targets=safe_anchor_and_targets(r)
            for parity in (0,1):
                witnesses=[d for d,z in enumerate(ps) if d % 2==parity and (r-3**c-z)%M in sums]
                assert witnesses
                # The proof uses precisely these four square sums, not a guessed local criterion.
                explicit=[d for d,z in enumerate(ps) if d % 2==parity and (r-3**c-z)%M in {t%M for t in targets}]
                assert explicit
                checks += 1
            common=any((r-1-z)%M in sums and (r-3-z)%M in sums for z in ps)
            assert common == (r % 2==0)
            cases += 1
    return dict(K_min=2,K_max=Kmax,residues=cases,parity_witness_checks=checks,mismatches=0,
                odd_r_boundary_counterexample=dict(K=2,r=1,anchor_0="always unsafe",anchor_1="always safe",simultaneous_complete=False))


# Guards map rational-prime coordinate to (depth, residue).
Guard = tuple[tuple[int,int,int], ...]

def guard_ok(g: Guard, y: dict[int,int]) -> bool:
    return all(p in y and (y[p]-a) % p**d == 0 for p,d,a in g)


def meet(a: Guard,b: Guard) -> Guard | None:
    out={p:(d,r % p**d) for p,d,r in a}
    for p,d,r in b:
        if p in out:
            e,s=out[p]
            if (r-s) % p**min(d,e): return None
            if d>e: out[p]=(d,r % p**d)
        else: out[p]=(d,r % p**d)
    return tuple((p,d,r) for p,(d,r) in sorted(out.items()))


@dataclass(frozen=True)
class Seed:
    origin: str
    guard: Guard
    lineage: tuple[int, ...] = ()

    @property
    def rank(self): return max((p for p,_,_ in self.guard if p != 2), default=0)


@dataclass(frozen=True)
class Dynamic:
    p: int
    guard: Guard
    center: int
    beta: int
    J: tuple[int, ...]


def dynamic_fatal(d: Dynamic,y: dict[int,int]) -> bool:
    if not guard_ok(d.guard,y): return False
    x=(y[d.p]-d.center) % d.p**d.beta
    if not x: return False
    v=0
    while x % d.p==0: x//=d.p; v+=1
    return v in d.J


def assignments(dom: dict[int,int]):
    keys=sorted(dom)
    for vals in product(*(range(p**dom[p]) for p in keys)):
        yield dict(zip(keys,vals))


def covered(seeds: list[Seed], dynamics: list[Dynamic],y):
    return any(guard_ok(s.guard,y) for s in seeds) or any(dynamic_fatal(d,y) for d in dynamics)


def first_escape(dom,seeds,dynamics):
    return next((y for y in assignments(dom) if not covered(seeds,dynamics,y)),None)


def linear_step(p: int,seeds: list[Seed],dynamics: list[Dynamic]):
    ds=[d for d in dynamics if d.p==p]
    assert len(ds)<=1
    d=ds[0] if ds else None
    out=[s for s in seeds if s.rank != p]
    for s in seeds:
        if s.rank != p: continue
        depth,res=next((e,a) for q,e,a in s.guard if q==p)
        if d is None or 0 not in d.J or depth != 1 or (res-d.center) % p: continue
        g=meet(tuple(t for t in s.guard if t[0] != p),d.guard)
        if g is not None: out.append(Seed(s.origin,g,s.lineage+(p,)))
    assert len({s.origin for s in out})==len(out)
    return out,[d for d in dynamics if d.p != p]



def canonical_prune(dom, seeds, dynamics):
    """Deterministic inclusion-minimal subcover at FROZEN ambient depth.
    This mutes redundant events; it does not remove arithmetic support rows or change U.
    """
    seeds=sorted(seeds,key=lambda s:s.origin)
    dynamics=sorted(dynamics,key=lambda d:d.p)
    for s in list(seeds):
        trial=[t for t in seeds if t.origin != s.origin]
        if first_escape(dom,trial,dynamics) is None: seeds=trial
    for d in list(dynamics):
        trial=[t for t in dynamics if t.p != d.p]
        if first_escape(dom,seeds,trial) is None: dynamics=trial
    return seeds,dynamics

def core_extract(dom,seeds,dynamics):
    """Canonical completeness-preserving linear descent, finite small-domain reference."""
    dom=dict(dom); seeds=list(seeds); dynamics=list(dynamics)
    if first_escape(dom,seeds,dynamics) is not None: return dict(kind="NOT_COMPLETE")
    seeds,dynamics=canonical_prune(dom,seeds,dynamics)
    history=[]
    while any(p!=2 for p in dom):
        p=max(q for q in dom if q!=2)
        new_s,new_d=linear_step(p,seeds,dynamics)
        lowdom={q:b for q,b in dom.items() if q!=p}
        y=first_escape(lowdom,new_s,new_d)
        if y is None:
            history.append(dict(eliminated=p,before=len(seeds),after=len(new_s)))
            dom=lowdom
            seeds,dynamics=canonical_prune(dom,new_s,new_d)
            continue
        full=(1 << p**dom[p])-1
        top=[]
        for s in seeds:
            if s.rank != p: continue
            g=tuple(t for t in s.guard if t[0]!=p)
            if guard_ok(g,y):
                e,a=next((e,a) for q,e,a in s.guard if q==p)
                top.append((s.origin,cylinder_mask(p,dom[p],Cylinder(e,a)),s))
        for d in dynamics:
            if d.p==p and guard_ok(d.guard,y):
                top.append(("dynamic:"+str(p),shell_mask(p,dom[p],d.center,d.J),d))
        union=0
        for _,m,_ in top: union |= m
        assert union==full
        # A deterministic irredundant subcover, not a claim of minimum cardinality.
        for i in range(len(top)-1,-1,-1):
            u=0
            for j,(_,m,_) in enumerate(top):
                if i != j: u |= m
            if u==full: top.pop(i)
        R=[o for _,_,o in top if isinstance(o,Seed)]
        assert len(R)>=p
        return dict(kind="NONLINEAR_DESCENDED_CORE",rank=p,lower=y,
                    rigid_origins=[s.origin for s in R],rigid_count=len(R),
                    lineages={s.origin:list(s.lineage) for s in R},
                    guards={s.origin:s.guard for s in R},
                    witness=[name for name,_,_ in top],history=history,
                    source_class="ABSTRACT_OR_ARITHMETIC_INPUT_MUST_BE_LABELLED_BY_CALLER")
    raise AssertionError("Complete terminal state contradicts the arithmetic order-closure hypothesis; check input class")


def triangular_audit():
    # Actual regular-row order signatures w_3=2, w_7=6.
    # Rigid seeds here are abstract cylinders, NOT authenticated nonregular primes.
    pts=list(assignments({2:1,3:1,7:1})); full=(1<<len(pts))-1
    seeds=[]; seed_masks=[]
    for oddmod in (3,7,21):
        for m in (oddmod,2*oddmod):
            fs=factors(m)
            for a in range(m):
                g=tuple((p,e,a % p**e) for p,e in sorted(fs.items()))
                s=Seed(f"abstract_m{m}_a{a}",g)
                seeds.append(s)
                seed_masks.append(sum(1<<i for i,y in enumerate(pts) if guard_ok(g,y)))
    d3=[None]+[Dynamic(3,((2,1,a),),z,1,(0,)) for a in range(2) for z in range(3)]
    d7=[None]+[Dynamic(7,((2,1,a),(3,1,b)),z,1,(0,)) for a in range(2) for b in range(3) for z in range(7)]
    counts=[0,0,0]; complete=[0,0,0]
    pair_unions=[a|b for i,a in enumerate(seed_masks) for b in seed_masks[i:]]
    for a,b in product(d3,d7):
        ds=[d for d in (a,b) if d is not None]
        dm=sum(1<<i for i,y in enumerate(pts) if any(dynamic_fatal(d,y) for d in ds))
        counts[0]+=1; complete[0]+=(dm==full)
        for m in seed_masks: counts[1]+=1; complete[1]+=((dm|m)==full)
        for m in pair_unions: counts[2]+=1; complete[2]+=((dm|m)==full)
    assert complete==[0,0,0]
    sharp=[Seed(f"abstract_R{a}",((3,1,a),)) for a in range(3)]
    core=core_extract({2:1,3:1},sharp,[])
    return dict(domain="Z/2 x Z/3 x Z/7",dynamic_orders={"3":2,"7":6},
                rigid_seed_catalog=len(seeds),cases_by_rigid_count=counts,
                complete_by_rigid_count=complete,abstract_sharp_core=core,
                arithmetic_scope="Only dynamic order signatures are arithmetic; rigid seeds are abstract")


@dataclass(frozen=True)
class Event:
    origin: int
    anchor: int
    rank: int
    guard: Guard
    p: int
    beta: int
    mask: int
    kind: str
    log_class: int | None = None
    order: int | None = None


def normal_events_K2(primes: list[int], residues: dict[int,int]):
    orders={q:order5(q) for q in primes}
    U=lcm(*orders.values()); dom=factors(U); events=[]; info={}
    for q in primes:
        w=orders[q]; s=lift_s(q,w); info[q]=dict(order=w,s=s)
        logs={}; a=1
        for b in range(w): logs[a]=b; a=a*5 % q
        if s==1:
            logs2={}; a=1
            for b in range(w*q): logs2[a]=b; a=a*5 % (q*q)
        for c in (0,1):
            target=(residues[q]-3**c) % (q*q)
            b=logs.get(target % q)
            if b is None: continue
            if s>=2:
                if target==pow(5,b,q*q): continue  # unresolved local zero
                p=max(factors(w)); e=factors(w)[p]
                guard=tuple((r,k,b % r**k) for r,k in sorted(factors(w).items()) if r!=p)
                beta=dom[p]
                events.append(Event(q,c,p,guard,p,beta,cylinder_mask(p,beta,Cylinder(e,b)),"rigid",b,w))
            elif q in dom:
                d=logs2[target]
                guard=tuple((r,k,b % r**k) for r,k in sorted(factors(w).items()))
                events.append(Event(q,c,q,guard,q,dom[q],shell_mask(q,dom[q],d % q,(0,)),"dynamic",b,w))
    return U,dom,events,info


def event_fatal(e: Event,y):
    return guard_ok(e.guard,y) and bool(e.mask >> y[e.p] & 1)


def exponent_to_coords(d,dom): return {p:d % p**b for p,b in dom.items()}


def ascending_game(dom,events,initial=(0,1),forced_prefix=None,common_only=False):
    """Exact finite backtracking. Dropping a covered anchor is sound, not a row deletion."""
    forced_prefix=forced_prefix or {}; keys=sorted(dom); visited=0
    def walk(i,y,S):
        nonlocal visited
        visited+=1
        if not S: return None
        if i==len(keys): return dict(coords=dict(y),surviving_anchors=list(S))
        p=keys[i]
        vals=[forced_prefix[p]] if p in forced_prefix else range(p**dom[p])
        for z in vals:
            y[p]=z
            kill={e.anchor for e in events if e.rank==p and e.anchor in S and event_fatal(e,y)}
            new=tuple(c for c in S if c not in kill)
            if common_only and new!=S: continue
            ans=walk(i+1,y,new)
            if ans is not None: return ans
        y.pop(p,None)
        return None
    out=walk(0,{},tuple(initial))
    return dict(witness=out,visited_states=visited,common_only=common_only)


def blocker_greedy(dom,events,assignment):
    """A sound, deliberately incomplete ascending policy certificate.
    A q assigned at the current rank is removed only inside the jointly checked
    union with its blocker digits. Future assignment alone never removes it.
    """
    F={}; rows={q:[e for e in events if e.kind=="rigid" and e.origin==q] for q in assignment}
    for q,p in assignment.items():
        if p is None: continue
        if not rows[q] or p not in dom or p == 2 or not is_prime(p):
            raise ValueError("Expected an actual odd blocker coordinate and a rigid event")
        if any(e.order % p for e in rows[q]): raise ValueError("Not an order divisor")
        F.setdefault(p,set()).update(e.log_class % p for e in rows[q])
    y={}; pre=set(); steps=[]
    for p in sorted(dom):
        current={q for q,b in assignment.items() if b==p}
        banned=F.get(p,set())
        good=[]
        for z in range(p**dom[p]):
            if z % p in banned: continue
            y[p]=z
            if any(e.rank==p and not (e.kind=="rigid" and e.origin in pre|current)
                   and event_fatal(e,y) for e in events): continue
            good.append(z)
        if not good:
            return dict(success=False,failed_coordinate=p,steps=steps,assignment=assignment)
        y[p]=good[0]
        # Only now does a current blocker become a certified permanent exclusion.
        pre |= current
        steps.append(dict(coordinate=p,chosen=y[p],F=sorted(banned),preblocked=sorted(pre)))
    assert not any(event_fatal(e,y) for e in events)
    return dict(success=True,coords=y,steps=steps,assignment=assignment)


def actual_audit():
    p,q=67,20771; residues={p:2,q:20775}
    U,dom,events,info=normal_events_K2([p,q],residues)
    assert U==228470
    cnt=[0,0]; safe=[0,0]; pooled_safe=0; nf_mismatch=0
    powers={r:1 for r in (p,q)}
    for d in range(U):
        truth=[]; y=exponent_to_coords(d,dom)
        for c in (0,1):
            bad=any((residues[r]-3**c-powers[r]) % r==0 and
                    (residues[r]-3**c-powers[r]) % (r*r)!=0 for r in (p,q))
            check=any(e.anchor==c and event_fatal(e,y) for e in events)
            if bad != check: nf_mismatch+=1
            truth.append(bad); cnt[c]+=bad; safe[c]+=not bad
        pooled_safe += not any(truth)
        for r in (p,q): powers[r]=powers[r]*5 % (r*r)
    assert nf_mismatch==0
    assert safe==[218219,218218]
    prefix={r:0 for r in dom if r!=67}
    fiber=[]
    for c in (0,1):
        fiber.append([z for z in range(67) if any(e.anchor==c and event_fatal(e,{**prefix,67:z}) for e in events)])
    assert fiber==[list(range(1,67)),[0]]
    game=ascending_game(dom,events,forced_prefix=prefix)
    common=ascending_game(dom,events,forced_prefix=prefix,common_only=True)
    assert game['witness'] is not None and common['witness'] is None
    policies=[blocker_greedy(dom,events,{20771:b}) for b in (None,5,31,67)]
    assert any(x['success'] for x in policies)
    # Actual zero-marginal-cost counterexample to the naive potential.
    q=20771; r31=2; rq=1+5*(1+q)
    D=[]
    for z in range(31):
        d=next(d for d in range(3*5*31) if d%3==0 and d%5==1 and d%31==z)
        v=(r31-1-pow(5,d,31**2)) % (31**2)
        if v%31==0 and v!=0: D.append(z)
    assert D==list(range(1,31))
    assert (rq-1-pow(5,1,q*q)) % (q*q)==5*q
    delta=Fraction(1,67)
    return dict(rows=info,period=U,normal_form_cases=2*U,normal_form_mismatches=nf_mismatch,
                individual_safe_counts=safe,common_safe_count=pooled_safe,
                split_fatal_digits=fiber,anchored_game=game,common_only_game=common,
                blocker_policies=policies,
                naive_potential_counterexample=dict(primes=[31,20771],residues={"31":r31,"20771":rq},
                  lower={"3":0,"5":1},dynamic_forbidden=D,blocker_F=[1],
                  safe_budget_before="1/31",safe_budget_after="1/31",future_capacity_removed="1/67",
                  potential_increase=str(delta),scope="actual, fixed anchor 0; naive potential only"))


def bareiss_det(A):
    A=[list(r) for r in A]; n=len(A); sign=1; prev=1
    if n==0: return 1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None: return 0
        if pivot != k: A[k],A[pivot]=A[pivot],A[k]; sign=-sign
        v=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=A[i][j]*v-A[i][k]*A[k][j]
                assert num % prev == 0
                A[i][j]=num//prev
            A[i][k]=0
        prev=v
    return sign*A[-1][-1]


def resultant(h: int,Y: int):
    A=5**(Y*h)
    f=[1]+[0]*(h-1)+[-A]  # descending coefficients
    g=[comb(h,k)*(-2)**(h-k) for k in range(h,-1,-1)]
    g[-1]-=A
    matrix=[]
    for poly in (f,g):
        for i in range(h): matrix.append([0]*i+poly+[0]*(h-1-i))
    return bareiss_det(matrix)


def poly_trim(a):
    while a and a[-1]==0: a.pop()
    return a


def poly_gcd_degree(a,b,q):
    a=poly_trim([x%q for x in a]); b=poly_trim([x%q for x in b])
    while b:
        r=list(a); inv=pow(b[-1],-1,q)
        while len(r)>=len(b):
            c=r[-1]*inv % q; k=len(r)-len(b)
            for j,x in enumerate(b): r[j+k]=(r[j+k]-c*x)%q
            poly_trim(r)
        a,b=b,r
    return len(a)-1


def resultant_audit():
    values=[]
    for h,Y in product((3,5,7),(0,1,2)):
        v=resultant(h,Y); A=5**(Y*h)
        if h==3: closed=-216*A**2-512
        elif h==5: closed=-100000*A**4-20480000*A**2-33554432
        else: closed=-105413504*A**6-12583119618048*A**4-412488659107840*A**2-562949953421312
        assert v==closed and v!=0
        values.append(dict(h=h,Y=Y,resultant=str(v),bit_length=abs(v).bit_length()))
    q=20771; h=67; u=155; histogram={}; examples=[]; total=0; gcd_checks=0
    for Y in range(u):
        coset={pow(5,Y+u*t,q):(Y+u*t)%h for t in range(h)}
        edges=[(x,coset[(a-2)%q]) for a,x in coset.items() if (a-2)%q in coset]
        k=len(edges); histogram[k]=histogram.get(k,0)+1; total+=k
        A=pow(5,Y*h,q)
        f=[-A]+[0]*(h-1)+[1]
        g=[comb(h,j)*(-2)**(h-j) % q for j in range(h+1)]; g[0]=(g[0]-A)%q
        assert poly_gcd_degree(f,g,q)==k; gcd_checks+=1
        if edges and len(examples)<3: examples.append(dict(Y=Y,edges=edges))
        if Y==0: assert not edges
    assert total==33 and histogram=={0:127,1:24,2:3,3:1}
    return dict(exact_resultants=values,paired_pool=dict(q=q,h=h,u=u,edges=total,
       histogram=histogram,gcd_checks=gcd_checks,nonzero_Y_examples=examples),
       scope="Nonzero Y resultants computed exactly, not fully factored; no arbitrary-Y resource exclusion claimed")


def arithmetic_resource_audit():
    products={3:[31],6:[3,7],9:[19,829],18:[3,5167],27:[109,271,4159,31051],54:[3,163,487,16018507]}
    signatures=[]
    for m,fs in products.items():
        d=m if m%2 else m//2
        B=5**(d//3)
        value=B*B+B+1 if m%2 else B*B-B+1
        prod=1
        for q in fs:
            assert is_prime(q); prod*=q
        assert prod==value and len(set(fs))==len(fs)
        for q in fs:
            if q%4==3 and q>3:
                w=order5(q); s=lift_s(q,w)
                signatures.append(dict(q=q,order=w,s=s))
                assert s==1
    q=(5**11-1)//4
    assert q==12207031 and is_prime(q) and order5(q)==11
    boundary=1645333507
    assert is_prime(boundary)
    w=order5(boundary)
    assert w==2*3**3*30469139 and lift_s(boundary,w)>=2
    return dict(squarefree_cyclotomic_orders=list(products),signatures=signatures,
                rigid_3_minimum=81,dynamic_allowed_3_minimum=21,
                no_3_chain_prefix=[5,11,q],chain_orders={"11":order5(11),str(q):order5(q)},
                chain_scope="arbitrarily long existence is proved symbolically; only this prefix computed",
                no_free_direct_blocker_resource=dict(q=boundary,order=w,s=lift_s(boundary,w),
                  odd_order_factors=[3,30469139],factor_admissibility=[is_prime(x) and x%4==3 for x in (3,30469139)]))



def frontier_profiles(p: int, max_leaves: int, max_depth: int):
    """All depth profiles generated by expanding a full p-ary prefix tree.
    This enumerates profiles, not positions or actual arithmetic realizations.
    """
    root=(1,)+(0,)*max_depth
    seen={root}; todo=[root]
    while todo:
        v=todo.pop()
        if sum(v)+p-1>max_leaves: continue
        for d in range(max_depth):
            if not v[d]: continue
            w=list(v); w[d]-=1; w[d+1]+=p; w=tuple(w)
            if w not in seen: seen.add(w); todo.append(w)
    return sorted(v for v in seen if v[0]==0)


def descended_resource_audit():
    # Complete finite cyclotomic identities for the newly needed helper heads.
    records=[]
    for m,fs,value in ((5,[11,71],(5**5-1)//4),(10,[521],5**4-5**3+5**2-5+1)):
        prod=1
        for q in fs:
            assert is_prime(q); prod*=q
            records.append(dict(cyclotomic_order=m,q=q,order=order5(q),s=lift_s(q,order5(q)),admitted=(q%4==3)))
        assert prod==value
    heads3={1:[7,31],2:[19,5167]}
    for d,qs in heads3.items():
        for q in qs:
            w=order5(q)
            assert w in (3**d,2*3**d) and lift_s(q,w)==1 and q%4==3
    shallow_cap=Fraction(2,3)+Fraction(2,9)
    assert shallow_cap==Fraction(8,9)<1
    profiles3=frontier_profiles(3,6,6)
    profiles5=frontier_profiles(5,6,6)
    assert profiles3 and all(not any(v[3:]) for v in profiles3)
    assert profiles5==[(0,5,0,0,0,0,0)]
    witness_cases=complete_witness_patterns=0
    for n in (5,6):
        # labels 0..4 are exact depth-one positions; 5 is any unusable deep cylinder.
        for labels in combinations_with_replacement(range(6),n):
            counts=[labels.count(j) for j in range(5)]
            number=1
            for k in counts: number*=k
            if number:
                assert number<=n-4
                complete_witness_patterns+=1
            witness_cases+=1
    seven=[Cylinder(1,0),Cylinder(1,1),Cylinder(2,2),Cylinder(2,5),
           Cylinder(3,8),Cylinder(3,17),Cylinder(3,26)]
    assert union_measure(3,seven)==1
    assert all(union_measure(3,seven[:i]+seven[i+1:])<1 for i in range(7))
    return dict(shallow_three_heads=heads3,shallow_three_union_upper_bound=str(shallow_cap),
                additional_factor_identities=records,
                proper_frontier_profiles_le_six={"3":[list(v) for v in profiles3],"5":[list(v) for v in profiles5]},
                five_witness_multiset_cases=witness_cases,five_covered_patterns=complete_witness_patterns,
                seven_leaf_abstract_frontier=[dict(depth=c.depth,residue=c.residue) for c in seven],
                scope="Finite supporting identities for the analytic >=7 theorem; not enumeration of all admitted systems. The seven-leaf frontier is geometry only, not actual-prime realization.")


def dual_and_temporal_audit():
    Q1=[frozenset(('a','u')),frozenset(('b','v'))]
    Q2=[frozenset(('a','v')),frozenset(('b','u'))]
    demand=frozenset(('a','b','u','v'))
    assert all(a|b!=demand for a,b in product(Q1,Q2))
    for u in demand:
        assert sum(Fraction(u in C,2) for C in Q1+Q2)==1
    # Synthetic mixed-anchor row, solely an implementation regression:
    # a rigid event is blocked at 3, but the SAME original identity also has
    # an anchor-1 dynamic event at 7. Blocking the rigid event must not delete it.
    dom={3:1,7:1}
    rigid=Event(101,0,3,(),3,1,cylinder_mask(3,1,Cylinder(1,0)),"rigid",0,3)
    dynamic=Event(101,1,7,((3,1,1),),7,1,shell_mask(7,1,1,(0,)),"dynamic",1,3)
    out=blocker_greedy(dom,[rigid,dynamic],{101:3})
    assert out['success'] and out['coords'][3]==1 and out['coords'][7]==1
    # Pure temporal bug at the current top rank, from an authenticated actual row pair.
    U,dom,ev,_=normal_events_K2([67,20771],{67:2,20771:20775})
    point={p:0 for p in dom}
    assert any(e.origin==20771 and e.anchor==1 and event_fatal(e,point) for e in ev)
    assert not any(e.origin!=20771 and event_fatal(e,point) for e in ev)
    # A hand-auditable overlap counterexample: cost >=1, exact center branch survives.
    p=3; beta=2; J=(0,); F=(1,2)
    cost=Fraction(2,3)+Fraction(2,3)
    assert cost==Fraction(4,3) and not centered_full(p,beta,0,J,F,[])
    return dict(configuration_gap=dict(integral_choices=4,integral_covers=0,fractional_half_assignment_covers=True,
                                       scope="abstract configurations; proves scalar/configuration LP necessity is not integral sufficiency"),
                mixed_anchor_blocker_regression=dict(result=out,scope="synthetic geometry, not an arithmetic prime101 row"),
                actual_current_blocker_regression=dict(primes=[67,20771],prefix="all lower coordinates zero",unsafe_if_rigid_removed_without_F=True),
                overlap_counterexample=dict(p=p,beta=beta,J=list(J),F=list(F),naive_cost=str(cost),safe_center_branch=True))


def run(out: Path,quick=False):
    start=time.perf_counter()
    bench_start=time.perf_counter(); bench=local_audit(3,2,2,True); bench_sec=time.perf_counter()-bench_start
    dump(out/'benchmark.json',dict(scope="3-adic depth-2 exact finite benchmark",seconds=bench_sec,result=bench))
    local=[bench]
    if not quick:
        local += [local_audit(3,3,2,True),local_audit(5,2,4,False),local_audit(7,1,6,False)]
    dump(out/'local_geometry.json',dict(audits=local,mismatches=0))
    dump(out/'boundary.json',boundary_audit(7 if quick else 9))
    dump(out/'triangular_models.json',triangular_audit())
    dump(out/'actual_arithmetic.json',actual_audit())
    dump(out/'resultants.json',resultant_audit())
    dump(out/'arithmetic_resources.json',arithmetic_resource_audit())
    dump(out/'descended_resources.json',descended_resource_audit())
    dump(out/'dual_temporal.json',dual_and_temporal_audit())
    dump(out/'run_receipt.json',dict(seconds=time.perf_counter()-start,quick=quick,standard_library_only=True,
                                    source_code_imported_from_repository=False))
    print(json.dumps(dict(output=str(out),seconds=time.perf_counter()-start,quick=quick),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--quick',action='store_true')
    args=parser.parse_args()
    if args.output_dir.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
        parser.error("Choose an output directory outside this research bundle")
    run(args.output_dir,args.quick)
