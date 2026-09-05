#!/usr/bin/env python3
"""Independent exact reference laboratory. Python standard library only.

No repository implementation is imported. Abstract models are NOT asserted
arithmetically realizable. Their optional shared-residue tables use arbitrary
periodic functions g_i, explicitly not the genuine function 5**d.

Run: python reference.py --out results
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product, permutations
from math import gcd, lcm, prod
from pathlib import Path
import json
import hashlib
import random


@dataclass(frozen=True)
class Event:
    row: str
    anchor: int
    rank: int
    # A CRT conjunction (coordinate, modulus dividing that coordinate, residue).
    guard: tuple[tuple[int, int, int], ...]
    mask: int
    kind: str = 'rigid'
    zero_mask: int = 0
    provenance: frozenset[str] = frozenset()

    def active(self, prefix: tuple[int, ...]) -> bool:
        return all(prefix[i] % modulus == residue for i, modulus, residue in self.guard)

    def covers(self, point: tuple[int, ...]) -> bool:
        return self.active(point) and (self.rank < 0 or bool(self.mask & (1 << point[self.rank])))

    def zero(self, point: tuple[int, ...]) -> bool:
        return self.rank >= 0 and self.active(point) and bool(self.zero_mask & (1 << point[self.rank]))

    def support(self) -> frozenset[str]:
        return self.provenance or frozenset([self.row])

    def as_dict(self) -> dict:
        return dict(row=self.row, anchor=self.anchor, rank=self.rank,
                    guard=[list(t) for t in self.guard], mask=self.mask,
                    kind=self.kind, zero_mask=self.zero_mask,
                    provenance=sorted(self.support()))


def points(dims: tuple[int, ...]):
    return product(*(range(n) for n in dims))


def minimal_covers(masks: list[int], full: int) -> list[tuple[int, ...]]:
    """Exhaustive, inclusion-minimal covers; no cardinality optimization shortcut."""
    answer = []
    unions = [0] * (1 << len(masks))
    for s in range(1, 1 << len(masks)):
        bit = s & -s
        i = bit.bit_length() - 1
        unions[s] = unions[s ^ bit] | masks[i]
        if unions[s] != full:
            continue
        if any(unions[s ^ (1 << j)] == full for j in range(len(masks)) if s >> j & 1):
            continue
        answer.append(tuple(j for j in range(len(masks)) if s >> j & 1))
    return answer


def crt_pair(a: int, m: int, b: int, n: int):
    g = gcd(m, n)
    if (b - a) % g:
        return None
    nn = n // g
    k = 0 if nn == 1 else ((b - a) // g * pow(m // g, -1, nn)) % nn
    modulus = m * nn
    return ((a + m * k) % modulus, modulus)


def meet_guards(guards):
    current = {}
    for guard in guards:
        for i, m, a in guard:
            b, n = current.get(i, (0, 1))
            merged = crt_pair(b, n, a, m)
            if merged is None:
                return None
            current[i] = merged
    return tuple((i, m, a) for i, (a, m) in sorted(current.items()) if m > 1)


def macro_from_guard(guard, anchor, provenance, dims, name):
    if not guard:
        return Event(name, anchor, -1, (), 1, 'macro', 0, provenance)
    k = max(i for i, m, a in guard)
    _, modulus, residue = next(t for t in guard if t[0] == k)
    mask = sum(1 << z for z in range(dims[k]) if z % modulus == residue)
    lower = tuple(t for t in guard if t[0] < k)
    return Event(name, anchor, k, lower, mask, 'macro', 0, provenance)


def contraction(dims: tuple[int, ...], events: list[Event], anchor: int):
    """Guard-intersection provenance elimination; audited against direct forall."""
    current = [e for e in events if e.anchor == anchor]
    trace = []
    for k in reversed(range(len(dims))):
        top = [e for e in current if e.rank == k]
        lower = [e for e in current if e.rank < k]
        clauses = []
        added = []
        for idx in minimal_covers([e.mask for e in top], (1 << dims[k]) - 1):
            guard = meet_guards([top[i].guard for i in idx])
            if guard is None:
                continue
            support = frozenset().union(*(top[i].support() for i in idx))
            name = f'macro_{anchor}_{k}_{len(added)}'
            added.append(macro_from_guard(guard, anchor, support, dims, name))
            clauses.append(dict(guard=[list(t) for t in guard],
                                parent_events=[top[i].row for i in idx], rows=sorted(support)))
        child = lower + added
        for y in points(dims[:k]):
            lhs = all(any(e.covers(y + (z,)) for e in current) for z in range(dims[k]))
            rhs = any(e.covers(y) for e in child)
            assert lhs == rhs, ('contraction mismatch', dims, anchor, k, y)
        trace.append(dict(rank=k, clauses=clauses, top_events=len(top)))
        current = child
    root = any(e.covers(()) for e in current)
    return dict(root_covered=root, trace=trace)


def saturation(dims: tuple[int, ...], events: list[Event], anchor: int):
    out = {}
    for k, size in enumerate(dims):
        top = [e for e in events if e.anchor == anchor and e.rank == k]
        full = (1 << size) - 1
        sat = []
        for y in points(dims[:k]):
            union = 0
            for e in top:
                if e.active(y):
                    union |= e.mask
            if union == full:
                sat.append(list(y))
        out[str(k)] = sat
    return out


def validate(dims: tuple[int, ...], events: list[Event], detailed=False):
    assert all(n >= 2 for n in dims)
    grid = tuple(points(dims))
    coverage = [0, 0]
    row_sets = {}
    for e in events:
        assert e.anchor in (0, 1)
        assert e.rank < len(dims)
        assert not (e.mask & e.zero_mask), 'local zero counted fatal'
        for i, m, r in e.guard:
            assert 0 <= i < e.rank and dims[i] % m == 0 and 0 <= r < m
        if e.rank >= 0:
            assert 0 <= e.mask < (1 << dims[e.rank])
        fatal = sum(1 << j for j, x in enumerate(grid) if e.covers(x))
        zeros = sum(1 << j for j, x in enumerate(grid) if e.zero(x))
        coverage[e.anchor] |= fatal
        pair = row_sets.setdefault(e.row, [[0, 0], [0, 0]])
        pair[e.anchor][0] |= fatal
        pair[e.anchor][1] |= zeros
    for row, pair in row_sets.items():
        # Odd-row positive-divisibility exclusion includes local zeros.
        assert not ((pair[0][0] | pair[0][1]) & (pair[1][0] | pair[1][1])), row
    sats = [saturation(dims, events, c) for c in (0, 1)]
    ranks = [set(int(k) for k, ys in s.items() if ys) for s in sats]
    h2 = bool(ranks[0] & ranks[1])
    h1 = any(set(map(tuple, sats[0][str(k)])) & set(map(tuple, sats[1][str(k)]))
             for k in range(len(dims)))
    full = (1 << len(grid)) - 1
    answer = dict(dims=list(dims), covered_cells=[x.bit_count() for x in coverage],
                  domain_cells=len(grid), complete=[x == full for x in coverage],
                  original_rank_saturation=sats, H1=h1, H2=h2,
                  all_rows_active_at_both_anchors=all(p[0][0] and p[1][0] for p in row_sets.values()))
    if detailed:
        answer['events'] = [e.as_dict() for e in events]
        answer['contraction'] = [contraction(dims, events, c) for c in (0, 1)]
        answer['minimal_global_row_covers'] = []
        rows = list(row_sets)
        for c in (0, 1):
            covs = minimal_covers([row_sets[r][c][0] for r in rows], full)
            answer['minimal_global_row_covers'].append([[rows[i] for i in cc] for cc in covs])
        essential = []
        for removed in rows:
            remainder = [0, 0]
            for row in rows:
                if row != removed:
                    for c in (0, 1):
                        remainder[c] |= row_sets[row][c][0]
            essential.append(any(m != full for m in remainder))
        answer['simultaneously_row_irredundant'] = all(essential)
        answer['paired_greedy'] = paired_greedy(dims, events)
        answer['paired_residue_surrogate'] = surrogate_tables(dims, events)
    return answer


def paired_greedy(dims, events):
    stops = []
    def visit(y):
        k = len(y)
        if k == len(dims):
            stops.append(dict(prefix=list(y), kind='COMMON_ESCAPE'))
            return
        masks = [0, 0]
        for e in events:
            if e.rank == k and e.active(y):
                masks[e.anchor] |= e.mask
        full = (1 << dims[k]) - 1
        escape = [full ^ m for m in masks]
        common = escape[0] & escape[1]
        if not common:
            kind = ('JOINT_FULL' if escape == [0, 0] else
                    'SINGLE_FULL' if 0 in escape else 'SPLIT')
            stops.append(dict(prefix=list(y), rank=k, kind=kind,
                              escape_digits=[[z for z in range(dims[k]) if e >> z & 1] for e in escape]))
        else:
            for z in range(dims[k]):
                if common >> z & 1:
                    visit(y + (z,))
    visit(())
    return stops


def surrogate_tables(dims, events):
    """Stronger paired constraint: V_0-V_1=2 with shared r=0.
    g_i is arbitrary periodic data, NOT powers of five. This is only a surrogate.
    """
    qs = [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 103, 107, 127, 131]
    rows = sorted({e.row for e in events})
    if len(rows) > len(qs):
        raise ValueError("Too many rows for the explicit surrogate-prime inventory")
    result = []
    grid = tuple(points(dims))
    for row, q in zip(rows, qs):
        es = [e for e in events if e.row == row]
        values = []
        for x in grid:
            fatal = [any(e.anchor == c and e.covers(x) for e in es) for c in (0, 1)]
            zero = [any(e.anchor == c and e.zero(x) for e in es) for c in (0, 1)]
            assert sum(fatal) + sum(zero) <= 1
            if fatal[0]: g = -1 - q
            elif fatal[1]: g = -3 - q
            elif zero[0]: g = -1
            elif zero[1]: g = -3
            else: g = 1
            g %= q*q
            assert gcd(g,q)==1
            v = [(-1-g) % (q*q), (-3-g) % (q*q)]
            ff = [a != 0 and a % q == 0 for a in v]
            zz = [a == 0 for a in v]
            assert ff == fatal and zz == zero
            assert ((v[0] - v[1]) - 2) % (q*q) == 0
            values.append(g)
        result.append(dict(row=row, q=q, K=2, r=0, E=[1], g_table=values))
    return dict(scope='arbitrary periodic g_i, NOT 5^d; not an admitted arithmetic realization', rows=result)


def rectangular(m, n, f=None, g=None):
    """Complete covers, all rows active at both anchors; saturated ranks disjoint."""
    f = tuple(1 if i == 0 else 0 for i in range(m)) if f is None else f
    g = tuple(1 if j == 0 else 0 for j in range(n)) if g is None else g
    events = []
    for i in range(m):
        events.extend([Event(f'A{i}', 0, 0, (), 1 << i),
                       Event(f'A{i}', 1, 0, (), 1 << f[i])])
    for j in range(n):
        events.extend([Event(f'B{j}', 0, 1, (), 1 << g[j]),
                       Event(f'B{j}', 1, 1, (), 1 << j)])
    return (m, n), events


def partial_derangement(m, a, b):
    src = [i for i in range(m) if i != a]
    dst = [i for i in range(m) if i != b]
    for image in permutations(dst):
        if all(i != j for i, j in zip(src, image)):
            return tuple(zip(src, image))
    return None


def nested(m, n, a, b, shift=1, spectator=False):
    """Saturation only at the top: Sat_0={a}, Sat_1={b}."""
    pairs = partial_derangement(m, a, b)
    if pairs is None:
        return None
    events = []
    for idx, (i, j) in enumerate(pairs):
        events.extend([Event(f'L{idx}', 0, 0, (), 1 << i),
                       Event(f'L{idx}', 1, 0, (), 1 << j)])
    for z in range(n):
        events.extend([Event(f'R{z}', 0, 1, ((0, m, a),), 1 << z),
                       Event(f'R{z}', 1, 1, ((0, m, b),), 1 << ((z + shift) % n))])
    return ((m, n, 2) if spectator else (m, n)), events


def dynamic_switch():
    """Three-row abstract 2x3 cover with explicit unresolved centers.
    The rank-0 paired row is NOT a sound arithmetic two-adic row.
    """
    return (2, 3), [
        Event('L', 0, 0, (), 1 << 1), Event('L', 1, 0, (), 1 << 0),
        Event('D', 0, 1, ((0, 2, 0),), 0b110, 'dynamic', 0b001),
        Event('D', 1, 1, ((0, 2, 1),), 0b110, 'dynamic', 0b001),
        Event('R', 0, 1, ((0, 2, 0),), 0b001),
        Event('R', 1, 1, ((0, 2, 1),), 0b001),
    ]


def template_search():
    records = []
    for m, n, spectator in [(2,3,False), (2,3,True), (3,3,False), (3,5,False)]:
        nested_count = h1false = 0
        differences = set()
        for a in range(m):
            for b in range(m):
                for shift in range(1, n):
                    model = nested(m,n,a,b,shift,spectator)
                    if model is None:
                        continue
                    ans = validate(*model)
                    assert ans['complete'] == [True,True] and ans['H2']
                    assert ans['H1'] == (a == b)
                    nested_count += 1
                    h1false += not ans['H1']
                    differences.add((a-b) % m)
        fs = [f for f in product(range(m), repeat=m)
              if all(f[i] != i for i in range(m)) and len(set(f)) < m]
        gs = [g for g in product(range(n), repeat=n)
              if all(g[j] != j for j in range(n)) and len(set(g)) < n]
        rectangular_count = 0
        for f in fs:
            for g in gs:
                dims, es = rectangular(m,n,f,g)
                if spectator: dims += (2,)
                ans = validate(dims, es)
                assert ans['complete'] == [True,True]
                assert not ans['H1'] and not ans['H2']
                assert ans['all_rows_active_at_both_anchors']
                rectangular_count += 1
        records.append(dict(dims=[m,n]+([2] if spectator else []),
                            nested_complete=nested_count,nested_H1_false=h1false,
                            nested_separations=sorted(differences),
                            rectangular_complete_H2_false=rectangular_count,
                            f_maps=len(fs),g_maps=len(gs)))
    return records


def truth_table_audit():
    count = 0
    for n in (2,3,5):
        full = (1 << n)-1
        for low0,low1 in product((False,True),repeat=2):
            for top0,top1 in product(range(1<<n),repeat=2):
                complete = (low0 or top0==full) and (low1 or top1==full)
                if complete:
                    assert (low0 or low1) or (top0==full and top1==full)
                    if not (top0==full and top1==full):
                        assert low0 or low1
                if not ((full^top0)&(full^top1)):
                    assert (top0|top1)==full
                count += 1
    # Tax audit with depth 1 and 2, active dynamic at at most one anchor.
    tax_count = 0
    for p,beta in [(3,1),(3,2),(5,1)]:
        n = p**beta
        cylinders = []
        for depth in range(1,beta+1):
            mod = p**depth
            for a in range(mod):
                cylinders.append(sum(1<<z for z in range(n) if z%mod==a))
        for r in range(p):
            for choices in product(cylinders,repeat=r):
                mask=0
                for x in choices: mask |= x
                assert mask != (1<<n)-1
                tax_count += 1
    return dict(last_coordinate_cases=count, rigid_tax_cases=tax_count, mismatches=0)


def random_contraction_audit(seed=20260905, cases_per_grid=250):
    rng=random.Random(seed)
    total=complete=clauses=0
    grids=[(2,3),(2,3,2),(3,3),(3,5)]
    for dims in grids:
        for case in range(cases_per_grid):
            es=[]
            for r in range(rng.randint(1,7)):
                k=rng.randrange(len(dims))
                row=f'q{r}'
                atoms=[]
                for c in (0,1):
                    if rng.randrange(5)==0: continue
                    guard=tuple((i,dims[i],rng.randrange(dims[i]))
                                for i in range(k) if rng.randrange(2))
                    mask=1 << rng.randrange(dims[k])
                    atoms.append(Event(row,c,k,guard,mask))
                # Keep a common-row pair only if its positive-divisibility masks are disjoint.
                if len(atoms)==2 and any(atoms[0].covers(x) and atoms[1].covers(x) for x in points(dims)):
                    atoms=atoms[:1]
                es += atoms
            ans=validate(dims,es)
            for c in (0,1):
                trace=contraction(dims,es,c)
                assert trace['root_covered']==ans['complete'][c]
                clauses += sum(len(t['clauses']) for t in trace['trace'])
            total += 1
            complete += ans['complete']==[True,True]
    return dict(seed=seed,cases=total,complete_simultaneous=complete,
                derived_clauses=clauses, mismatches=0)


def multiplicative_order_5(q):
    x=5%q; w=1
    while x!=1:
        x=x*5%q;w+=1
        assert w<=q-1
    return w


def base5_s(q,w):
    s=1
    while pow(5,w,q**(s+1))==1:
        s+=1
    return s


def actual_pair(rp,rq):
    ps=(67,20771)
    rs=(rp,rq)
    ws=[multiplicative_order_5(p) for p in ps]
    ss=[base5_s(p,w) for p,w in zip(ps,ws)]
    fullperiods=[w*p**max(0,2-s) for p,w,s in zip(ps,ws,ss)]
    U=lcm(*ws); L=lcm(*fullperiods)
    assert U==L==228470 and ws==[22,10385] and ss==[1,2]
    assert all(factor(p)=={p:1} for p in ps)
    lower=U//67
    fatal=[];zeros=[]
    for p,r,period in zip(ps,rs,fullperiods):
        ff=[[],[]];zz=[[],[]];a=1
        for d in range(period):
            for c in (0,1):
                v=(r-3**c-a)%(p*p)
                ff[c].append(v!=0 and v%p==0)
                zz[c].append(v==0)
            a=a*5%(p*p)
        fatal.append(ff);zeros.append(zz)
    # These exact counts certify the claimed dynamic/rigid event types here.
    assert [sum(layer) for layer in fatal[0]] == [66,66]
    assert [sum(layer) for layer in fatal[1]] == [1,1]
    covers=[bytearray(L),bytearray(L)]
    zero_counts=[[0,0],[0,0]]
    for d in range(L):
        for idx, period in enumerate(fullperiods):
            assert not ((fatal[idx][0][d%period] or zeros[idx][0][d%period])
                        and (fatal[idx][1][d%period] or zeros[idx][1][d%period]))
            for c in (0,1):
                covers[c][d] |= fatal[idx][c][d%period]
                zero_counts[idx][c] += zeros[idx][c][d%period]
    sats=[[],[]]; joint_min=2*67
    pooled_saturation=[]
    fiberrecords=[]
    for y in range(lower):
        counts=[sum(covers[c][y+lower*k] for k in range(67)) for c in (0,1)]
        joint_min=min(joint_min,2*67-sum(counts))
        if all(covers[0][y+lower*k] or covers[1][y+lower*k] for k in range(67)):
            pooled_saturation.append(y)
        for c in (0,1):
            if counts[c]==67:
                sats[c].append(y)
                dpoints=[y+lower*k for k in range(67)]
                perrow=[sum(fatal[i][c][d%fullperiods[i]] for d in dpoints) for i in range(2)]
                fiberrecords.append(dict(anchor=c,lower=y,row_cells=perrow,covered=counts[c]))
    # A second direct modular-power formulation checks all selected full fibers.
    direct_tests=0
    for rec in fiberrecords:
        c,y=rec['anchor'],rec['lower']
        for k in range(67):
            d=y+lower*k
            flags=[]
            for p,r in zip(ps,rs):
                a=(r-3**c-pow(5,d,p*p))%(p*p)
                flags.append(a!=0 and a%p==0)
            assert any(flags)
            direct_tests+=1
    return dict(primes=list(ps),residues=list(rs),w=ws,s=ss,U=U,L=L,
                lower_modulus=lower,saturation=sats,
                common_saturation=sorted(set(sats[0])&set(sats[1])),
                pooled_saturation=pooled_saturation,
                covered_cells=[sum(c) for c in covers],safe_cells=[L-sum(c) for c in covers],
                local_zero_counts=zero_counts,minimum_joint_holes=joint_min,
                full_fibers=fiberrecords,direct_pow_crosschecks=direct_tests,
                complete_simultaneous=all(all(c) for c in covers),
                new_no_go_class=dict(top_prime=67,distinct_top_rigid_resources=1,
                                      top_rigid_Kraft_per_anchor=['1/67','1/67'],
                                      pooled_lower_events=0,boundary='no two-adic row',passes=True))


def actual_first_split():
    # Same actual admitted rows, shared residues, different anchor coverage.
    ps=(67,20771);rs=(2,20775);M=3410
    row_digits=[[],[]];union=[set(),set()]
    for c in (0,1):
        for p,r in zip(ps,rs):
            hits=set()
            for k in range(67):
                d=M*k
                v=(r-3**c-pow(5,d,p*p))%(p*p)
                if v!=0 and v%p==0: hits.add(d%67)
            row_digits[c].append(sorted(hits));union[c] |= hits
    assert [list(map(len,layer)) for layer in row_digits]==[[66,0],[0,1]]
    assert union[0]==set(range(1,67)) and union[1]=={0}
    assert pow(3,67,20771)!=1
    return dict(primes=list(ps),residues=list(rs),K=[2,2],E=[[1],[1]],
                U=228470,lower_modulus=M,lower_assignment=0,
                top_coordinate=67,row_digit_sets=row_digits,
                anchor_coverage_sizes=[66,1],pooled_coverage_size=67,
                anchor_escape_digits=[[0],list(range(1,67))],
                split_type='proper/proper split; neither anchor full on this fiber',
                pow_3_67_mod_20771=pow(3,67,20771),
                complete_certificate=False,
                scope='actual local split witness; NOT an actual complete counterexample to H1 or H2')


def factor(n):
    out={};q=2
    while q*q<=n:
        while n%q==0:
            out[q]=out.get(q,0)+1;n//=q
        q=3 if q==2 else q+2
    if n>1:out[n]=out.get(n,0)+1
    return out


def arithmetic_nonrealizability():
    # Every odd row in a genuinely frozen U=15 system has order dividing 15,
    # and hence its prime divides 5^15-1. This is exhaustive, not a prime cutoff.
    N=5**15-1; fs=factor(N)
    assert prod(q**e for q,e in fs.items())==N
    admitted=[]
    for q in fs:
        if q%4==3 and q!=5:
            w=multiplicative_order_5(q);s=base5_s(q,w)
            assert 15%w==0
            admitted.append(dict(q=q,w=w,s=s,pow_mod_q_squared=pow(5,w,q*q)))
    assert [x['q'] for x in admitted]==[11,31,71]
    assert all(x['s']==1 and 15%x['q'] for x in admitted)
    return dict(frozen_U=15,N=N,factorization={str(q):e for q,e in fs.items()},
                all_possible_admitted_primes=admitted,rigid_resources=0,
                status='exact CRT 3x5 countermodel NOT realizable in unchanged U=15',
                extension_to_enlarged_U='NOT decided by this calculation')


def two_adic_audit():
    out=[]
    for K in range(2,9):
        modulus=1<<K
        sq={a*a%modulus for a in range(modulus)}
        sums={(a+b)%modulus for a in sq for b in sq}
        period=1 if K==2 else 1<<(K-2)
        no_common=[]
        log5={pow(5,d,modulus):d for d in range(period)}
        assert len(log5)==period and set(log5)==set(range(1,modulus,4))
        constructed=0
        for r in range(modulus):
            common=[d for d in range(period)
                    if all((r-3**c-pow(5,d,modulus))%modulus in sums for c in (0,1))]
            if not common:no_common.append(r)
            if r%2==0:
                target=(r-(3 if r%4==0 else 5))%modulus
                d=log5[target]
                assert d in common
                expected=(2,0) if r%4==0 else (4%modulus,2)
                assert tuple((r-3**c-pow(5,d,modulus))%modulus for c in (0,1))==expected
                constructed+=1
        assert no_common==list(range(1,modulus,2))
        out.append(dict(K=K,residues=modulus,no_common_safe_count=len(no_common),
                        no_common_exactly_odd_r=True,explicit_even_residue_witnesses=constructed))
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'results')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    examples={}
    examples['H2_disjoint_coordinates_3x5']=validate(*rectangular(3,5),detailed=True)
    examples['H2_disjoint_coordinates_3x3']=validate(*rectangular(3,3),detailed=True)
    examples['H1_split_same_coordinate_3x5']=validate(*nested(3,5,0,2),detailed=True)
    examples['H1_split_2x3']=validate(*nested(2,3,0,1),detailed=True)
    examples['H1_split_2x3x2']=validate(*nested(2,3,0,1,spectator=True),detailed=True)
    examples['dynamic_local_zero_switch_2x3']=validate(*dynamic_switch(),detailed=True)
    assert examples['H2_disjoint_coordinates_3x5']['minimal_global_row_covers']==[
        [['A0','A1','A2']],[['B0','B1','B2','B3','B4']]]
    # Corruption test: accepting the dynamic local zero must be rejected.
    dims,es=dynamic_switch();bad=list(es)
    e=bad[2];bad[2]=Event(e.row,e.anchor,e.rank,e.guard,e.mask|e.zero_mask,e.kind,e.zero_mask)
    rejected=False
    try:validate(dims,bad)
    except AssertionError:rejected=True
    assert rejected
    outputs={
        'counterexamples.json':examples,
        'template_search.json':template_search(),
        'truth_table_audit.json':truth_table_audit(),
        'random_contraction_audit.json':random_contraction_audit(),
        'actual_arithmetic_replay.json':[actual_pair(2,13471),actual_pair(0,4494),actual_pair(2,20775)],
        'actual_first_split.json':actual_first_split(),
        'frozen_U15_nonrealizability.json':arithmetic_nonrealizability(),
        'two_adic_audit.json':two_adic_audit(),
    }
    outputs['summary.json']=dict(
        phase_verdict='C. WEAKER USEFUL BRIDGE FOUND; secondary D, abstract structural negative',
        authority_main='0200beede923c56e0284d9555c1dabaf91fa1755',
        authority_tree='23f10c12181c5caa394f7a3fb1acb6e79cc02fe6',
        project='PAUSED',active_promoted_route='NONE',A303656='UNRESOLVED',
        github_writes='NONE', local_zero_corruption_rejected=rejected,
        independent='No repository code imported; one independently written standard-library program',
        actual_H1='OPEN AFTER TARGETED SEARCH',actual_H2='OPEN AFTER TARGETED SEARCH',
        abstract_H1='DISPROVED ABSTRACTLY',abstract_H2='DISPROVED ABSTRACTLY',
        no_go_scope='pooled lower strict deficit + common-safe boundary + top rigid Kraft mass <1 at each anchor (in particular <p original rigid rows)',
        search=outputs['template_search.json'],truth=outputs['truth_table_audit.json'],
        contraction=outputs['random_contraction_audit.json'])
    for name,content in outputs.items():
        (args.out/name).write_text(json.dumps(content,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(outputs['summary.json'],indent=2))

if __name__=='__main__':main()
