#!/usr/bin/env python3
"""Standalone exact laboratory. All synthetic fixtures are explicitly ABSTRACT."""
from __future__ import annotations
import argparse
import itertools
import json
import math
import random
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

@dataclass
class Atom:
    key: str
    label: int
    kind: str
    shadow: dict[int, int]
    own: int | None = None
    center: int = 0

@dataclass
class Node:
    key: str
    guard: dict[int, int]
    support: frozenset[str]
    parents: tuple['Node', ...] = ()
    eliminated: int | None = None
    atom: str | None = None

class Lab:
    def __init__(self, sizes: dict[int, int], atoms: list[Atom]):
        self.sizes = dict(sorted(sizes.items()))
        self.full = {p: (1 << n)-1 for p,n in sizes.items()}
        self.atoms = {a.key:a for a in atoms}
        assert len(self.atoms)==len(atoms)
        self.dynamic = {a.own:a.key for a in atoms if a.kind=='dynamic'}
        assert len(self.dynamic)==sum(a.kind=='dynamic' for a in atoms)
        self.roots = {a.key for a in atoms if a.kind=='rigid'}
        self.serial=0
        self.counts={'pointwise_projection_checks':0,'minimal_witnesses':0,
                     'private_provider_checks':0,'ancestry_paths':0,
                     'capacity_checks':0,'support_identity_checks':0}
        self.events=[]
        for a in atoms:
            g=dict(a.shadow)
            if a.kind=='dynamic':
                assert a.own is not None
                assert all(p<a.own for p in a.shadow)
                g[a.own]=self.full[a.own]^(1<<a.center)
            else:
                assert all(p<a.label for p in a.shadow)
            assert all(m and m!=self.full[p] for p,m in g.items())
            self.events.append(Node(a.key,g,frozenset([a.key]),atom=a.key))
        self.initial=list(self.events)
        self.history=[]

    def is_dynamic(self, e:Node, p:int) -> bool:
        return e.atom is not None and self.atoms[e.atom].kind=='dynamic' and self.atoms[e.atom].own==p

    @staticmethod
    def holds(e:Node,x:dict[int,int])->bool:
        return all((m>>x[p])&1 for p,m in e.guard.items())

    def intersection(self,parents:list[Node],p:int)->dict[int,int]|None:
        g={}
        for e in parents:
            for r,m in e.guard.items():
                if r==p:continue
                g[r]=g.get(r,self.full[r])&m
                if not g[r]:return None
        return g

    def covers(self,top:list[Node],p:int):
        # Complete enumeration for beta-one proper cylinders + one centered complement.
        n=self.sizes[p]
        assert n==p, 'This engine deliberately tests beta one only.'
        branches=[[] for _ in range(n)]; dyn=[]
        for e in top:
            m=e.guard[p]
            if self.is_dynamic(e,p):dyn.append(e)
            else:
                assert m.bit_count()==1
                branches[m.bit_length()-1].append(e)
        assert len(dyn)<=1
        if all(branches):
            for tup in itertools.product(*branches):yield list(tup)
        if dyn:
            center=self.atoms[dyn[0].atom].center
            for e in branches[center]:yield [dyn[0],e]

    def exact_candidates(self,e:Node,p:int)->list[str]:
        return sorted(q for q in e.support if self.atoms[q].shadow.get(p,self.full[p])==e.guard[p])

    def ancestry(self,e:Node,q:str, prefer:str|None=None)->list[str]:
        assert q in e.support
        if self.atoms[q].kind=='rigid':return [q]
        own=self.atoms[q].own
        # Locate this occurrence's introduction witness, not arbitrary macro co-support.
        def intro(n:Node)->Node:
            if any(c.atom==q for c in n.parents):
                assert n.eliminated==own
                return n
            candidates=[c for c in n.parents if q in c.support]
            assert candidates, (q,n.key)
            return intro(candidates[0])
        witness=intro(e)
        center=self.atoms[q].center
        cp=[c for c in witness.parents if c.atom!=q and ((c.guard[own]>>center)&1)]
        assert len(cp)==1
        candidates=self.exact_candidates(cp[0],own)
        assert candidates
        r=prefer if prefer in candidates else candidates[0]
        assert self.atoms[r].label>self.atoms[q].label
        path=[q]+self.ancestry(cp[0],r,prefer)
        assert set(path)<=e.support
        return path

    def descendants(self,o:str)->set[str]:
        out=set()
        def dfs(q):
            if q in out:return
            out.add(q)
            for p in self.atoms[q].shadow:
                if p in self.dynamic:dfs(self.dynamic[p])
        dfs(o)
        return out

    def capacity(self,o:str,p:int)->int:
        fam={self.atoms[v].shadow[p] for v in self.descendants(o) if p in self.atoms[v].shadow}
        return width_minimal(fam)

    def audit_witness(self,parents:list[Node],p:int,child:Node):
        self.counts['minimal_witnesses']+=1
        full=self.full[p]
        union=0
        for e in parents:union |= e.guard[p]
        assert union==full
        for j in range(len(parents)):
            u=0
            for i,e in enumerate(parents):
                if i!=j:u |= e.guard[p]
            assert u!=full
        charges={}
        for i,e in enumerate(parents):
            if self.is_dynamic(e,p):
                assert e.atom not in set().union(*(x.support for j,x in enumerate(parents) if j!=i))
                continue
            candidates=self.exact_candidates(e,p)
            assert candidates
            q=candidates[0]
            assert all(q not in x.support for j,x in enumerate(parents) if j!=i)
            self.counts['private_provider_checks']+=1
            path=self.ancestry(e,q)
            self.counts['ancestry_paths']+=1
            o=path[-1]
            assert o in self.roots and q in self.descendants(o)
            charges[o]=charges.get(o,0)+1
        for o,n in charges.items():
            assert n<=self.capacity(o,p)
            self.counts['capacity_checks']+=1
        for e in parents:
            assert len(child.support-e.support)>=len(parents)-1

    def project(self,p:int,verify:bool=True):
        before=list(self.events)
        top=[e for e in before if p in e.guard]
        lower=[e for e in before if p not in e.guard]
        new=[]
        for parents in self.covers(top,p):
            g=self.intersection(parents,p)
            if g is None:continue
            self.serial+=1
            e=Node(f'M{self.serial}',g,frozenset().union(*(v.support for v in parents)),tuple(parents),p)
            self.audit_witness(parents,p,e)
            new.append(e)
        # Same-support/same-geometry alternatives have one canonical witness.
        unique={}
        for e in lower+new:
            k=(tuple(sorted(e.guard.items())),tuple(sorted(e.support)))
            unique.setdefault(k,e)
        self.events=list(unique.values())
        remaining=[q for q in self.sizes if q<p]
        for e in self.events:
            if e.atom is not None and self.atoms[e.atom].kind=='dynamic':continue
            expected={}
            for q in e.support:
                for r,m in self.atoms[q].shadow.items():
                    if r<p:expected[r]=expected.get(r,self.full[r])&m
            assert expected==e.guard,(expected,e.guard)
            self.counts['support_identity_checks']+=1
            for q in e.support:
                path=self.ancestry(e,q)
                assert path[-1] in e.support & self.roots
        if verify:
            for t in itertools.product(*(range(self.sizes[q]) for q in remaining)):
                x=dict(zip(remaining,t))
                got=any(self.holds(e,x) for e in self.events)
                want=all(any(self.holds(e,dict(x,**{} )|{p:z}) for e in before) for z in range(self.sizes[p]))
                assert got==want,(p,x,got,want)
                self.counts['pointwise_projection_checks']+=1
        self.history.append({'coordinate':p,'before':len(before),'after':len(self.events),
                             'nonempty_new_witnesses':len(new)})
        return new

    def run(self):
        for p in sorted(self.sizes,reverse=True):self.project(p)
        return bool(self.events)


def width_minimal(fam:set[int])->int:
    """Inclusion-minimal DISTINCT nonempty cylinders, not maximal union components."""
    assert all(fam)
    return sum(not any(b!=a and b&a==b for b in fam) for a in fam)


def rigid(key:str,shadow:dict[int,int],label:int=100003)->Atom:
    return Atom(key,label,'rigid',shadow)


def dynamic(p:int,shadow:dict[int,int],center:int=0)->Atom:
    return Atom(str(p),p,'dynamic',shadow,p,center)


def subset_projection_check(lab:Lab,after:list[Node],p:int)->int:
    """Independent bitset universal projection for every enabled atom subset."""
    keys=list(lab.atoms); n=len(keys)
    assert n<=16
    pos={q:i for i,q in enumerate(keys)}
    lower=[q for q in lab.sizes if q<p]
    ys=list(itertools.product(*(range(lab.sizes[q]) for q in lower)))
    atom_masks=[]
    for e in lab.initial:
        m=0
        for i,t in enumerate(ys):
            x=dict(zip(lower,t))
            for z in range(lab.sizes[p]):
                if lab.holds(e,x|{p:z}):m|=1<<(i*lab.sizes[p]+z)
        atom_masks.append(m)
    supports=[sum(1<<pos[q] for q in e.support) for e in after]
    masks=[sum(1<<i for i,t in enumerate(ys) if lab.holds(e,dict(zip(lower,t)))) for e in after]
    unions=[0]*(1<<n); checks=0
    block=(1<<lab.sizes[p])-1
    for a in range(1<<n):
        if a:
            b=a&-a; unions[a]=unions[a^b]|atom_masks[b.bit_length()-1]
        expected=sum(1<<i for i in range(len(ys)) if (unions[a]>>(i*lab.sizes[p]))&block==block)
        got=0
        for s,m in zip(supports,masks):
            if s&a==s:got|=m
        assert got==expected
        checks+=1
    return checks


def fork_fixture():
    atoms=[rigid('R',{7:1,31:1})]
    atoms += [rigid(f'A{j:02}',{3:1,7:1,31:1<<j},100010+j) for j in range(1,31)]
    atoms += [rigid(f'B{i}',{3:2,7:1<<i,31:1},100100+i) for i in range(1,7)]
    atoms += [rigid('C',{3:4},100201),dynamic(7,{3:1}),dynamic(31,{3:2})]
    lab=Lab({3:3,7:7,31:31},atoms)
    lab.project(31);lab.project(7)
    parents=list(lab.events)
    assert len(parents)==3
    p0=next(e for e in parents if e.guard=={3:1})
    p1=next(e for e in parents if e.guard=={3:2})
    assert '7' in lab.exact_candidates(p0,3) and '31' in lab.exact_candidates(p1,3)
    assert all('7' not in e.support for e in parents if e!=p0)
    assert all('31' not in e.support for e in parents if e!=p1)
    a=lab.ancestry(p0,'7','R');b=lab.ancestry(p1,'31','R')
    assert a==['7','R'] and b==['31','R']
    assert lab.capacity('R',3)==2
    lab.project(3)
    assert lab.events and lab.events[0].guard=={}
    return {'classification':'ABSTRACT; initial rigid rows not arithmetically instantiated',
            'rigid_roots':38,'regular_helper_roles':2,'grid_cells':651,
            'chosen_ancestry_paths':[a,b],'shared_root_shadow_width':2,
            'unit_capacity_chosen_charge_fails':True,
            'existential_unit_Hall_failure_claimed':False,
            'history':lab.history,'checks':lab.counts}


def cartesian_fixture():
    atoms=[rigid(f'C{k}',{7:1<<k},100010+k) for k in range(2,7)]
    atoms +=[rigid(f'A{i}',{7:1,3:1<<i},100100+i) for i in range(3)]
    atoms +=[rigid(f'B{j}',{7:2,5:1<<j},100200+j) for j in range(5)]
    lab=Lab({3:3,5:5,7:7},atoms)
    lab.project(7)
    macros=list(lab.events)
    assert len(macros)==15
    for i,j in itertools.combinations(range(15),2):
        a,b=macros[i],macros[j]
        assert any(not(a.guard.get(p,lab.full[p])&b.guard.get(p,lab.full[p])) for p in (3,5))
    assert len(set().union(*(e.support for e in macros)))==13
    enabled=subset_projection_check(lab,macros,7)
    # Each of the three LOWER fibers has only five simultaneous p=5 obligations.
    assert all(sum((e.guard[3]>>i)&1 for e in macros)==5 for i in range(3))
    lab.project(5);lab.project(3)
    assert lab.events and lab.events[0].guard=={}
    return {'classification':'ABSTRACT rigid-only canonical grammar',
            'original_roots':13,'post_7_indispensable_disjoint_macros':15,
            'global_frontier_unit_Hall_deficiency':2,
            'same_fiber_p5_obligations':5,'enabled_subledger_checks':enabled,
            'history':lab.history,'checks':lab.counts}


def duplicate_fixture():
    lab=Lab({3:3},[rigid(f'{i}{j}',{3:1<<i},101+i*2+j) for i in range(3) for j in range(2)])
    lab.project(3)
    assert len(lab.events)==8 and all(e.guard=={} for e in lab.events)
    multiplicity={q:sum(q in e.support for e in lab.events) for q in lab.atoms}
    assert set(multiplicity.values())=={4}
    return {'classification':'ABSTRACT OR alternatives','original_roots':6,
            'alternative_TRUE_clauses':8,'occurrences_per_original':4}


def width_suite():
    records=[]
    for p,beta in [(3,2),(5,1)]:
        n=p**beta
        cyl=[]
        for d in range(1,beta+1):
            for a in range(p**d):cyl.append(sum(1<<z for z in range(n) if z%(p**d)==a))
        conflict=[sum(1<<j for j,b in enumerate(cyl) if a&b) for a in cyl]
        @lru_cache(None)
        def packing(mask):
            if not mask:return 0
            bit=mask&-mask;i=bit.bit_length()-1
            return max(packing(mask^bit),1+packing(mask&~conflict[i]))
        for mask in range(1<<len(cyl)):
            fam={cyl[i] for i in range(len(cyl)) if mask>>i&1}
            assert width_minimal(fam)==packing(mask)
        records.append({'prime':p,'depth':beta,'proper_cylinders':len(cyl),'families':1<<len(cyl)})
    frozen=[width_minimal({1<<i}) for i in range(3)]
    assert frozen==[1,1,1] and width_minimal({1,2,4})==3
    return {'exhaustive_families':records,'state_reselection_negative_control':{
        'each_fixed_state_capacity':frozen,'invalid_union_of_states_capacity':3}}


def seeded_suite():
    rng=random.Random(20260907);total={};complete=0
    for case in range(500):
        atoms=[]
        for i in range(rng.randint(1,9)):
            g={p:1<<rng.randrange(p) for p in (3,5,7) if rng.randrange(3)!=0}
            if not g:g={3:1<<rng.randrange(3)}
            atoms.append(rigid(f'R{i}',g,1000+i))
        for p in (5,7):
            if rng.randrange(4):
                g={q:1<<rng.randrange(q) for q in (3,5) if q<p and rng.randrange(2)}
                atoms.append(dynamic(p,g,rng.randrange(p)))
        lab=Lab({3:3,5:5,7:7},atoms)
        truth=lab.run()
        complete+=truth
        confined=set().union(*(lab.descendants(o) for o in lab.roots))
        muted=Lab({3:3,5:5,7:7},atoms)
        muted.events=[e for e in muted.events if e.atom in confined]
        assert muted.run()==truth
        for k,v in lab.counts.items():total[k]=total.get(k,0)+v
    return {'classification':'ABSTRACT, including non-admitted dynamic5',
            'seed':20260907,'cases':500,'complete_cases':complete,
            'basin_muting_checks':500,'checks':total}


def is_prime(n:int)->bool:
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))


def prime_record(p:int)->dict:
    assert p%4==3 and is_prime(p)
    w=1;x=5%p
    while x!=1:x=x*5%p;w+=1
    s=1
    while pow(5,w,p**(s+1))==1:s+=1
    return {'prime':p,'order':w,'lifting_exponent':s}


def actual_fixture():
    primes=[11,31,67,20771]
    records=[prime_record(p) for p in primes]
    orders={r['prime']:r['order'] for r in records}
    assert orders=={11:5,31:3,67:22,20771:10385}
    assert [r['lifting_exponent'] for r in records]==[1,1,1,2]
    U=math.lcm(*orders.values());assert U==685410
    L=math.lcm(*(orders[p]*(1 if p==20771 else p) for p in primes));assert L==U
    residues={p:(20775 if p==20771 else 4) for p in primes}
    checks=0;covered=0;powers={p:1 for p in primes}
    for d in range(U):
        anyfatal=False
        for p in primes:
            v=(residues[p]-3-powers[p])%(p*p)
            got=(v%p==0 and v!=0)
            expected=(d%orders[p]==0 and (p==20771 or d%p!=0))
            assert got==expected
            anyfatal |= got;checks+=1
            powers[p]=powers[p]*5%(p*p)
        covered+=anyfatal
    atoms=[rigid('20771',{5:1,31:1,67:1},20771),
           dynamic(67,{11:1}),dynamic(31,{3:1}),dynamic(11,{5:1})]
    lab=Lab({3:3,5:5,11:11,31:31,67:67},atoms)
    lab.project(67);lab.project(31)
    parent=next(e for e in lab.events if 11 in e.guard and e.atom is None)
    assert lab.exact_candidates(parent,11)==['67']
    path=lab.ancestry(parent,'67');assert path==['67','20771']
    lab.project(11)
    assert len(lab.events)==1 and lab.events[0].guard=={3:1,5:1}
    lab.project(5);lab.project(3);assert not lab.events
    return {'classification':'ACTUAL arithmetic, NOT a complete certificate',
            'anchor':1,'K':2,'accepted':[1],'rows':records,'residues':residues,
            'U':U,'L':L,'normal_form_checks':checks,'covered_exponents':covered,
            'regular_private_provider_at_coordinate11':'67','ancestry':path,
            'collapsed_even_residual':'d=0 mod15; full exponent condition d=0 mod30',
            'history':lab.history,'checks':lab.counts}


def actual_shared_states():
    q=20771;u=155;rows=[]
    for r,b0,b1 in [(16,2177,9772),(17555,1558,10238)]:
        vals=[]
        for c,b in enumerate((b0,b1)):
            v=(r-3**c-pow(5,b,q*q))%(q*q)
            assert v and v%q==0
            vals.append(1)
        assert b0%u==b1%u
        rows.append({'residue':r,'logs':[b0,b1],'lower_class':b0%u,'valuations':vals})
    assert [r['lower_class'] for r in rows]==[7,8]
    assert 162%u==7
    return {'classification':'ACTUAL imported-state recalibration',
            'prime':q,'states':rows,'valuation_checks':4,
            'compatible_ordinary_lower_representatives':[7,162],
            'incompatible_ordinary_lower_representatives':[7,8]}


def seven_fixture():
    heads=[(31,0),(7,4),(19,2),(5167,14),(271,8),(4159,17),(31051,26)]
    records=[];checks=0;guards=[]
    for h,ell in heads:
        rec=prime_record(h);w=rec['order'];assert rec['lifting_exponent']==1
        dh=h*((ell*pow(h,-1,w))%w)
        r=(3+pow(5,dh,h*h))%(h*h)
        x=1
        for d in range(w*h):
            v=(r-3-x)%(h*h)
            assert (v%h==0 and v!=0)==(d%w==ell and d%h!=0)
            x=x*5%(h*h);checks+=1
        rec.update({'log':ell,'center':0,'CRT_log_representative':dh,'residue':r})
        records.append(rec);guards.append((w,ell))
    row3=prime_record(3);x=1
    for d in range(6):
        v=(2-3-x)%9
        assert (v%3==0 and v!=0)==(d%2==1 and d%3!=0)
        x=x*5%9;checks+=1
    collapsed=[]
    for d in range(54):
        ok=any(d%w==ell for w,ell in guards) or (d%2==1 and d%3!=0)
        assert ok;collapsed.append(int(ok))
    leaves=[(1,0),(1,1),(2,2),(2,5),(3,8),(3,17),(3,26)]
    masks=[sum(1<<z for z in range(27) if z%(3**dep)==a) for dep,a in leaves]
    assert sum(m.bit_count() for m in masks)==27
    assert all(a&b==0 for a,b in itertools.combinations(masks,2))
    assert sum(masks)==(1<<27)-1
    return {'classification':'CONDITIONAL upstream nonregular chains; actual regular heads only',
            'head_records':records,'row3':{'prime':3,'residue':2,'K':2,'accepted':[1]},
            'actual_regular_row_period_checks':checks,'collapsed_classes':54,
            'covered_collapsed_classes':sum(collapsed),'frontier_leaves':leaves,
            'origin_capacities':[1]*7,'Hall_demand':7,'Hall_capacity':7,
            'next_odd_coordinate_after_3':None,'actual_nonregular_roots_instantiated':0}


def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('results.json'))
    args=ap.parse_args()
    if not __debug__:raise RuntimeError('Run without -O: assertions are part of the checker.')
    result={'authority':{'main':'3fb4b4b4f71018017c7ea014ae7a1380f27b6b94',
                         'tree':'5ee6ab9e51f3e6d471991b7407de193d12777882'},
            'same_origin_fork':fork_fixture(),'cartesian_frontier':cartesian_fixture(),
            'OR_reuse':duplicate_fixture(),'shadow_width':width_suite(),
            'seeded_models':seeded_suite(),'actual_provider':actual_fixture(),
            'exactly_seven':seven_fixture(),'actual_shared_states':actual_shared_states(),
            'assertion_failures':0,
            'github_writes':'NONE','proof_assistant_checked':False,'independent_author_checked':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(args.output),'assertion_failures':0,
          'seeded_cases':result['seeded_models']['cases'],
          'actual_row_checks':result['actual_provider']['normal_form_checks'],
          'seven_regular_checks':result['exactly_seven']['actual_regular_row_period_checks']},indent=2))

if __name__=='__main__':main()
