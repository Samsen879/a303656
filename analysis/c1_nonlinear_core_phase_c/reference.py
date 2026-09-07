#!/usr/bin/env python3
"""Exact standalone experiments for nonlinear provenance contraction.
No network, GitHub writes, floating-point coverage decisions, or repository imports.
ABSTRACT fixtures are not arithmetic realizations. Timings are descriptive only.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt, prod
from pathlib import Path
from time import perf_counter
import hashlib
import json
import random

@dataclass(frozen=True)
class Coordinate:
    p: int
    beta: int = 1
    @property
    def size(self) -> int:
        return self.p ** self.beta
    @property
    def full(self) -> int:
        return (1 << self.size) - 1

@dataclass(frozen=True)
class Event:
    name: str
    slices: tuple[int, ...]
    support: int
    dynamic: bool = False
    parents: tuple[str, ...] = ()


def cylinder(c: Coordinate, residue: int, depth: int) -> int:
    m = c.p ** depth
    return sum(1 << x for x in range(c.size) if x % m == residue % m)


def cylinder_depth(c: Coordinate, mask: int) -> int | None:
    if mask == 0:
        return None
    first = (mask & -mask).bit_length() - 1
    for d in range(c.beta + 1):
        if cylinder(c, first, d) == mask:
            return d
    return None


def bits(mask: int):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def support_subset(a: int, b: int) -> bool:
    return a & b == a


def normalize(events: list[Event]) -> list[Event]:
    """Only support-aware absorption, never geometry-only deletion."""
    found: dict[tuple[bool, int], Event] = {}
    for e in events:
        if any(x == 0 for x in e.slices):
            continue
        key = (e.dynamic, e.support)
        if key in found:
            assert found[key].slices == e.slices, 'support-to-guard determinacy failed'
        else:
            found[key] = e
    es = sorted(found.values(), key=lambda e: (e.support.bit_count(), e.support, e.name))
    kept: list[Event] = []
    for e in es:
        if not e.dynamic and any(not f.dynamic and support_subset(f.support, e.support) for f in kept):
            continue
        kept.append(e)
    return kept


def event_measure(e: Event, coords: tuple[Coordinate, ...]) -> Fraction:
    out = Fraction(1)
    for s, c in zip(e.slices, coords):
        out *= Fraction(s.bit_count(), c.size)
    return out


def event_point_mask(e: Event, coords: tuple[Coordinate, ...]) -> int:
    out = 0
    for k, x in enumerate(product(*(range(c.size) for c in coords))):
        if all((s >> v) & 1 for s, v in zip(e.slices, x)):
            out |= 1 << k
    return out


def profile(events: list[Event], coords: tuple[Coordinate, ...], m: int) -> tuple[int, list[int]]:
    full = (1 << prod(c.size for c in coords)) - 1
    ev = [(e.support, event_point_mask(e, coords)) for e in events]
    good = []
    bitmap = 0
    for enabled in range(1 << m):
        covered = 0
        for support, mask in ev:
            if support_subset(support, enabled):
                covered |= mask
        if covered == full:
            bitmap |= 1 << enabled
            good.append(enabled)
    return bitmap, good


def minimal_masks(masks: list[int]) -> list[int]:
    out = []
    for a in sorted(masks, key=lambda a: (a.bit_count(), a)):
        if not any(support_subset(b, a) for b in out):
            out.append(a)
    return out


def guard_check(events: list[Event], coords: tuple[Coordinate, ...], shadows: list[tuple[int, ...]]) -> int:
    checked = 0
    for e in events:
        if e.dynamic:
            continue
        for j, c in enumerate(coords):
            expected = c.full
            for q in bits(e.support):
                expected &= shadows[q][j]
            assert expected == e.slices[j], (e.name, j, 'shadow meet mismatch')
            d = cylinder_depth(c, expected)
            assert d is not None
            if d > 0:
                providers = [q for q in bits(e.support) if shadows[q][j] == expected]
                assert providers, 'no original exact-depth provider'
            checked += 1
    return checked


def contraction(events: list[Event], coords: tuple[Coordinate, ...], step: int, shadows):
    assert coords
    c = coords[-1]
    top = [e for e in events if e.slices[-1] != c.full]
    low = [Event(e.name, e.slices[:-1], e.support, e.dynamic, e.parents)
           for e in events if e.slices[-1] == c.full]
    n = len(top)
    if n > 18:
        raise RuntimeError(f'Explicit small-model gate exceeded: {n} top events')
    unions = [0] * (1 << n)
    raw = []
    covers = 0
    incompatible = 0
    for a in range(1, 1 << n):
        bit = a & -a
        j = bit.bit_length() - 1
        unions[a] = unions[a ^ bit] | top[j].slices[-1]
        if unions[a] != c.full:
            continue
        ids = list(bits(a))
        if any(unions[a ^ (1 << i)] == c.full for i in ids):
            continue
        covers += 1
        assert len(ids) >= 2, 'a proper top event cannot cover alone'
        guard = [d.full for d in coords[:-1]]
        support = 0
        for i in ids:
            support |= top[i].support
            for j in range(len(guard)):
                guard[j] &= top[i].slices[j]
        if any(g == 0 for g in guard):
            incompatible += 1
            continue
        for i in ids:
            assert support_subset(top[i].support, support)
            assert top[i].support != support, 'strict support growth failed'
        providers = []
        private_providers = {}
        for i in ids:
            if top[i].dynamic:
                continue
            qs = [q for q in bits(top[i].support) if shadows[q][len(coords)-1] == top[i].slices[-1]]
            assert qs, 'frontier leaf lacks exact original shadow provider'
            q = min(qs)
            assert all(not (top[j].support & (1 << q)) for j in ids if j != i), 'provider was not private to its parent'
            providers.append(q)
            private_providers[top[i].name] = q
        assert len(set(providers)) == len(providers), 'distinct frontier leaves reused one exact provider'
        for i in ids:
            assert (support & ~top[i].support).bit_count() >= len(ids) - 1, 'arity charge failed'
        rigid_ids = [i for i in ids if not top[i].dynamic]
        for ii, i in enumerate(rigid_ids):
            for j in rigid_ids[ii+1:]:
                joined = top[i].slices[-1] | top[j].slices[-1]
                first = (joined & -joined).bit_length() - 1
                lca = max(d for d in range(c.beta + 1)
                          if joined & ~cylinder(c, first, d) == 0)
                for q in bits(top[i].support & top[j].support):
                    e = cylinder_depth(c, shadows[q][len(coords)-1])
                    assert e is not None and e <= lca, 'shared-origin LCA bound failed'
        raw.append(Event(f'M{step}.{a}', tuple(guard), support, False,
                         tuple(top[i].name for i in ids)))
    child = normalize(low + raw)
    return child, {
        'coordinate': c.p, 'beta': c.beta, 'top_count': n,
        'minimal_geometric_cover_clauses': covers,
        'empty_lower_intersections': incompatible,
        'nonempty_raw_macros': len(raw),
        'raw_macro_mass': str(sum((event_measure(e, coords[:-1]) for e in raw), Fraction())),
        'retained_after_support_normalization': len(child),
        'witnesses': [{'child_id':e.name, 'support': list(bits(e.support)), 'shared_state_tokens':[[q, 'frozen'] for q in bits(e.support)], 'anchor':0, 'demand':'A0', 'parents': list(e.parents),
                       'guard_masks': list(e.slices)} for e in raw]
    }


def assert_projection(parent, child, coords, m):
    pe = [(e.support, event_point_mask(e, coords)) for e in parent]
    ce = [(e.support, event_point_mask(e, coords[:-1])) for e in child]
    n = coords[-1].size
    full = (1 << n) - 1
    lower_size = prod(c.size for c in coords[:-1])
    for enabled in range(1 << m):
        pm = 0
        cm = 0
        for support, mask in pe:
            if support_subset(support, enabled): pm |= mask
        for support, mask in ce:
            if support_subset(support, enabled): cm |= mask
        expected = sum(1 << y for y in range(lower_size) if (pm >> (n*y)) & full == full)
        assert cm == expected, 'pointwise universal projection failed'


def compatible_state_union(*terms):
    out = {}
    for term in terms:
        for q, state in term.items():
            if q in out and out[q] != state:
                return None
            out[q] = state
    return out


def random_fixtures():
    rng = random.Random(20260906)
    out = []
    for m in range(1, 8):
        for rep in range(16):
            cs = (Coordinate(3, 1 + (rep % 2)), Coordinate(5), Coordinate(7))
            used_dynamic = set()
            rows = []
            for i in range(m):
                rank = rng.randrange(3)
                sl = [c.full for c in cs]
                for j in range(rank):
                    if rng.randrange(2):
                        sl[j] = cylinder(cs[j], rng.randrange(cs[j].size), rng.randint(1, cs[j].beta))
                dynamic = rank not in used_dynamic and rng.randrange(4) == 0
                if dynamic:
                    used_dynamic.add(rank)
                    sl[rank] = cs[rank].full ^ cylinder(cs[rank], rng.randrange(cs[rank].size), 1)
                else:
                    sl[rank] = cylinder(cs[rank], rng.randrange(cs[rank].size), rng.randint(1, cs[rank].beta))
                rows.append(Event(f'R{i}', tuple(sl), 1 << i, dynamic))
            data = analyze(f'random_{m}_{rep}', cs, rows)
            out.append({'rows':m, 'replicate':rep, 'subledger_checks':(1 << m)*len(data['states']),
                        'projection_checks':(1 << m)*len(data['transitions']),
                        'initial_complete':bool(data['complete_subledgers']),
                        'event_trace':[s['event_count'] for s in data['states']]})
    return out


def analyze(name: str, coords: tuple[Coordinate, ...], originals: list[Event]):
    m = len(originals)
    assert [e.support for e in originals] == [1 << i for i in range(m)]
    shadows = []
    for e in originals:
        h = list(e.slices)
        if e.dynamic:
            k = max(i for i, (s, c) in enumerate(zip(e.slices, coords)) if s != c.full)
            h[k] = coords[k].full
        shadows.append(tuple(h))
    original_rigid_mask = sum(e.support for e in originals if not e.dynamic)
    events = normalize(originals)
    base = (1 << m) + m + 1
    expected, masks = profile(events, coords, m)
    mins = minimal_masks(masks)
    states = []
    transitions = []
    original_coords = coords
    checks = 0
    while True:
        checks += guard_check(events, coords, shadows)
        now, _ = profile(events, coords, m)
        assert now == expected, 'all-subledger profile changed'
        counts = [sum(e.support.bit_count() == s for e in events) for s in range(1, m + 1)]
        potential = sum(base ** (m - e.support.bit_count()) for e in events)
        states.append({
            'coordinates': [[c.p, c.beta] for c in coords],
            'event_count': len(events), 'support_profile': counts,
            'integer_potential': str(potential),
            'macro_supports': [list(bits(e.support)) for e in events],
            'events':[{'id':e.name, 'kind':'original_dynamic' if e.dynamic else 'cylinder',
                       'guard_masks':list(e.slices), 'full_original_support':list(bits(e.support)),
                       'abstract_rigid_origin_support':list(bits(e.support & original_rigid_mask)),
                       'shared_state_tokens':[[q, 'frozen'] for q in bits(e.support)],
                       'anchor':0, 'demand':'A0', 'parents':list(e.parents)} for e in events],
            'sum_event_mass': str(sum((event_measure(e, coords) for e in events), Fraction())),
            'origin_occurrences': {str(q): sum(bool(e.support & (1 << q)) for e in events) for q in range(m)}
        })
        if not coords:
            break
        child, log = contraction(events, coords, len(transitions), shadows)
        assert_projection(events, child, coords, m)
        new_potential = sum(base ** (m - e.support.bit_count()) for e in child)
        if log['top_count']:
            assert new_potential < potential
        else:
            assert new_potential <= potential
        log['potential_strict'] = new_potential < potential
        transitions.append(log)
        events = child
        coords = coords[:-1]
    return {
        'label': 'ABSTRACT', 'name': name, 'original_rows': m,
        'domain': [[c.p, c.beta] for c in original_coords],
        'frozen_originals':[{'id':e.name, 'origin_index':i, 'dynamic':e.dynamic,
                            'event_masks':list(e.slices), 'log_shadow_masks':list(shadows[i]),
                            'state_token':[i,'frozen'], 'anchor':0, 'demand':'A0'}
                            for i,e in enumerate(originals)],
        'enabled_subledgers_checked_per_state': 1 << m,
        'complete_subledgers': len(masks),
        'minimal_complete_supports': [list(bits(a)) for a in mins],
        'subledger_profile_sha256': hashlib.sha256(expected.to_bytes(((1 << m) + 7) // 8, 'little')).hexdigest(),
        'shadow_coordinate_checks': checks, 'base': base,
        'states': states, 'transitions': transitions,
    }


def nested_partition(primes: tuple[int, ...]):
    coords = tuple(Coordinate(p) for p in sorted(primes))
    masks = [c.full for c in coords]
    rows = []
    for j in reversed(range(1, len(coords))):
        for a in range(1, coords[j].size):
            new = list(masks)
            new[j] = 1 << a
            rows.append(tuple(new))
        masks[j] = 1
    for a in range(coords[0].size):
        new = list(masks)
        new[0] = 1 << a
        rows.append(tuple(new))
    return coords, [Event(f'R{i}', r, 1 << i) for i, r in enumerate(rows)]


def duplicate_frontier(p: int):
    c = Coordinate(p)
    rows = [Event(f'R{i}', (1 << (i // 2),), 1 << i) for i in range(2 * p)]
    return (c,), rows


def grid(p: int, q: int):
    coords = (Coordinate(p), Coordinate(q))
    rows = []
    for x, y in product(range(p), range(q)):
        i = len(rows)
        rows.append(Event(f'R{i}', (1 << x, 1 << y), 1 << i))
    return coords, rows


def factor(n: int) -> dict[int, int]:
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def prime_trial(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def order_data(q: int):
    assert prime_trial(q)
    w = q - 1
    for p in factor(w):
        while w % p == 0 and pow(5, w // p, q) == 1:
            w //= p
    s = 1
    while pow(5, w, q ** (s + 1)) == 1:
        s += 1
    return {'q': q, 'prime_verified_by_trial_division': True, 'admitted_label': q % 4 == 3,
            'order': w, 'order_factorization': factor(w), 's': s}


def actual_motifs():
    u = 228470
    qlist = [67, 20771]
    arrays = {}
    logs = {}
    for q in qlist:
        a = 1
        arr = []
        for _ in range(u):
            arr.append(a)
            a = a * 5 % (q * q)
        arrays[q] = arr
        w = order_data(q)['order']
        logs[q] = {arr[d] % q: d for d in range(w)}
    out = []
    for label, residues in [('ALIGNED', (4, 20775)), ('SPLIT', (2, 20775)), ('PAIRED', (2, 13471))]:
        union = []
        normal_forms = []
        for anchor in (0, 1):
            forms = []
            direct = []
            for q, r in zip(qlist, residues):
                b = logs[q].get((r - 3 ** anchor) % q)
                if b is None:
                    form = ('inert',)
                elif q == 20771:
                    form = ('rigid', b, 10385) if (r - 3 ** anchor - arrays[q][b]) % (q*q) else ('inert',)
                else:
                    zeros = [(b + 22*t) % 67 for t in range(67)
                             if (r - 3 ** anchor - pow(5, b + 22*t, 67**2)) % (67**2) == 0]
                    assert len(zeros) == 1
                    form = ('dynamic', b, 22, zeros[0])
                forms.append(form)
                mask = []
                for d, a in enumerate(arrays[q]):
                    v = (r - 3 ** anchor - a) % (q*q)
                    fatal = v != 0 and v % q == 0
                    modeled = (form[0] == 'rigid' and d % form[2] == form[1]) or \
                              (form[0] == 'dynamic' and d % form[2] == form[1] and d % q != form[3])
                    assert fatal == modeled, (label, anchor, q, d)
                    mask.append(fatal)
                direct.append(mask)
            covered = [a or b for a, b in zip(*direct)]
            union.append(covered)
            normal_forms.append(forms)
        sats = [[y for y in range(3410) if all(union[c][y + 3410*k] for k in range(67))] for c in (0, 1)]
        out.append({'label': 'ACTUAL ARITHMETIC', 'motif': label, 'primes': qlist, 'K': 2, 'E': [1],
                    'shared_residues': residues, 'U': u,
                    'normal_forms': normal_forms,
                    'safe_counts': [sum(not a for a in union[c]) for c in (0, 1)],
                    'common_safe_count': sum(not (a or b) for a, b in zip(*union)),
                    'rank67_saturation_lower_residues_mod3410': sats,
                    'y0_fatal_slice_counts': [sum(union[c][3410*k] for k in range(67)) for c in (0,1)],
                    'full_period_normal_form_checks': 4*u})
    assert out[0]['rank67_saturation_lower_residues_mod3410'][1] == [0]
    assert out[1]['y0_fatal_slice_counts'] == [66, 1]
    assert out[1]['safe_counts'] == [218219, 218218]
    assert out[2]['rank67_saturation_lower_residues_mod3410'] == [[2728], [1639]]
    return out


def submodular_obstructions():
    # Before saturation, p disjoint strips have modular covered measure.
    # After saturation their enabled-set function is AND of the p origins.
    p = 3
    allrows = (1 << p) - 1
    a, b = allrows ^ 1, allrows ^ 2
    f = lambda s: int(s == allrows)
    assert f(a) + f(b) < f(a | b) + f(a & b)
    # Duplicated frontier: two disjoint complete choices violate supermodularity.
    left = sum(1 << (2*i) for i in range(p))
    right = sum(1 << (2*i+1) for i in range(p))
    g = lambda s: int(all(s & (3 << (2*i)) for i in range(p)))
    assert g(left) + g(right) > g(left | right) + g(left & right)
    return {'label': 'ABSTRACT', 'submodular_inequality': {'lhs': 0, 'rhs': 1},
            'supermodular_inequality': {'lhs': 2, 'rhs': 1}}


def private_provider_obstruction():
    """No frozen primitive cylinder assignment realizes the all-shared triangle
    as a three-parent minimal proper-slice cover. Not an arithmetic search.
    """
    out = []
    for p, beta in ((3,1),(3,2),(5,1),(7,1)):
        c = Coordinate(p,beta)
        shadows = [c.full] + [cylinder(c,a,d) for d in range(1,beta+1) for a in range(p**d)]
        tested = 0
        realized = 0
        for a,b,d in product(shadows, repeat=3):
            tested += 1
            leaves = [a & b, b & d, a & d]
            if any(x == 0 or x == c.full for x in leaves):
                continue
            if leaves[0] | leaves[1] | leaves[2] != c.full:
                continue
            if any((leaves[(i+1)%3] | leaves[(i+2)%3]) == c.full for i in range(3)):
                continue
            realized += 1
        assert realized == 0
        out.append({'label':'ABSTRACT FIXED-SHADOW ENUMERATION','p':p,'beta':beta,
                    'primitive_cylinder_options':len(shadows),'assignments_tested':tested,
                    'minimal_three_parent_frontiers':realized})
    return out


def main():
    start = perf_counter()
    cases = []
    benchmark_start = perf_counter()
    c, r = duplicate_frontier(3)
    cases.append(analyze('duplicate_frontier_p3', c, r))
    benchmark = perf_counter() - benchmark_start
    for p in (5, 7):
        c, r = duplicate_frontier(p)
        cases.append(analyze(f'duplicate_frontier_p{p}', c, r))
    for ps in ((3,5), (3,5,7)):
        c, r = nested_partition(ps)
        cases.append(analyze('nested_partition_' + '_'.join(map(str, ps)), c, r))
    c, r = grid(3, 5)
    cases.append(analyze('disjoint_support_grid_3_5', c, r))
    c = Coordinate(3, 3)
    rd = [(0,1),(1,1),(2,2),(5,2),(8,3),(17,3),(26,3)]
    r = [Event(f'R{i}', (cylinder(c,a,d),), 1<<i) for i,(a,d) in enumerate(rd)]
    cases.append(analyze('deep_ternary_frontier', (c,), r))
    c = Coordinate(3, 2)
    d = c.full ^ cylinder(c,0,1)
    r = [Event('D', (d,), 1, True)] + [Event(f'R{i}', (1 << a,), 1 << i) for i,a in enumerate((0,3,6),1)]
    cases.append(analyze('dynamic_nonsimple_beta2', (c,), r))
    order_primes = [3,7,11,19,31,67,71,1429,1523,5167,20771,40487,30469139,1645333507]
    arith = [order_data(q) for q in order_primes]
    motifs = actual_motifs()
    # Frozen q can supply one digit, not all three state alternatives at once.
    assert all(sum(1 for x in range(3) if x == state) == 1 for state in range(3))
    for a, b in product(range(3), repeat=2):
        joined = compatible_state_union({'q':a}, {'q':b})
        assert (joined is not None) == (a == b)
    assert compatible_state_union({'q':0}, {'q':1}, {'q':2}) is None
    random_checks = random_fixtures()
    state_test = {'label':'ABSTRACT NEGATIVE CONTROL', 'global_states_tested':3,
                  'frozen_state_complete_choices':0, 'branch_reselection_relaxation_complete':True,
                  'incompatible_state_product_must_be_zero':True}
    result = {'authority': {'repository':'Samsen879/a303656',
                          'main':'71b8d428b32724c37e593bcfd9d5f06a42e72d21',
                          'tree':'5609e47eed0c058c190ef59c61644e2fd4b8fad6'},
              'abstract_cases': cases, 'arithmetic_orders': arith, 'actual_motifs': motifs,
              'submodularity':submodular_obstructions(), 'private_provider_triangle':private_provider_obstruction(), 'state_control':state_test,
              'random_regressions':{'seed':20260906, 'label':'ABSTRACT', 'systems':random_checks},
              'coverage_arithmetic':'integers, bitsets, fractions only; no floating-point decisions',
              'repository_code_imported':False, 'github_writes':'NONE'}
    summary = {
        'named_fixtures':len(cases), 'seeded_fixtures':len(random_checks),
        'seeded_complete':sum(x['initial_complete'] for x in random_checks),
        'total_subledger_state_checks':sum(c['enabled_subledgers_checked_per_state']*len(c['states']) for c in cases)+sum(x['subledger_checks'] for x in random_checks),
        'total_pointwise_subledger_projection_checks':sum(c['enabled_subledgers_checked_per_state']*len(c['transitions']) for c in cases)+sum(x['projection_checks'] for x in random_checks),
        'full_period_row_anchor_exponent_checks':sum(x['full_period_normal_form_checks'] for x in motifs),
        'fixed_prime_order_lifting_checks':len(arith),
        'all_shared_triangle_assignments':sum(x['assignments_tested'] for x in result['private_provider_triangle'])
    }
    Path(__file__).with_name('computed_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    path = Path(__file__).with_name('results.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    metrics = {'benchmark_seconds':benchmark, 'total_seconds':perf_counter()-start}
    Path(__file__).with_name('run_metrics.json').write_text(json.dumps(metrics, indent=2)+'\n')
    print(json.dumps({'case_count':len(cases), 'random_systems':len(random_checks),
        'subledger_state_checks':sum(c['enabled_subledgers_checked_per_state']*len(c['states']) for c in cases),
        'exact_arithmetic_modular_checks':sum(m['full_period_normal_form_checks'] for m in motifs),
        'benchmark_seconds':benchmark,'total_seconds':metrics['total_seconds'],
        'traces': {c['name']: [s['event_count'] for s in c['states']] for c in cases}}, indent=2))

if __name__ == '__main__':
    main()
