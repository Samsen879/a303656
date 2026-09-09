#!/usr/bin/env python3
"""Independent, standard-library exact checks for the Phase E report.
No repository code is imported; no nonregular terminal is fabricated.
Run: python3 reference.py --output RESULTS.json
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, time
from collections import Counter
from pathlib import Path


def factors(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError('positive integer required')
    out: dict[int, int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def prime(p: int) -> bool:
    return p >= 2 and factors(p) == {p: 1}


def order5(p: int) -> int:
    if not prime(p) or p == 5:
        raise ValueError('prime distinct from 5 required')
    n = p - 1
    for t in factors(n):
        while n % t == 0 and pow(5, n//t, p) == 1:
            n //= t
    assert pow(5, n, p) == 1
    assert all(pow(5, n//t, p) != 1 for t in factors(n))
    return n


def lift5(p: int, w: int) -> int:
    for s in range(1, 12):
        if pow(5, w, p**(s+1)) != 1:
            return s
    raise ValueError('increase exact lifting limit')


def crt(residues: list[tuple[int, int]]) -> tuple[int, int]:
    a, m = 0, 1
    for b, n in residues:
        if math.gcd(m, n) != 1:
            raise ValueError('pairwise coprime CRT only')
        a += m * (((b-a)*pow(m, -1, n)) % n)
        m *= n
        a %= m
    return a, m


def fatal_from_power(p: int, K: int, E: set[int], r: int, c: int, power: int) -> bool:
    value = (r - 3**c - power) % (p**K)
    if value == 0:
        return False  # local-zero fail-closed, including odd K
    v = 0
    while value % p == 0:
        value //= p
        v += 1
    return 0 < v < K and v in E and v % 2 == 1


def fatal(p: int, K: int, E: set[int], r: int, c: int, d: int) -> bool:
    return fatal_from_power(p, K, E, r, c, pow(5, d, p**K))


def arithmetic_checks() -> dict:
    expected = {3:2, 7:6, 31:3, 19:9, 5167:18, 163:54, 271:27,
                487:54, 4159:27, 31051:27, 16018507:54,
                43:42, 127:42, 1303:62, 20771:10385, 40487:40486}
    data = []
    for p, w in expected.items():
        assert p % 4 == 3 and order5(p) == w
        s = lift5(p, w)
        assert s == (2 if p in (20771, 40487) else 1)
        data.append({'p':p, 'w':w, 's':s, 'prime_proof':'complete trial division'})
    return {'pass':True, 'rows':data}


def frontier_checks() -> dict:
    depths = [1,1,2,2,3,3,3]
    positions = [0,1,2,5,8,17,26]
    coverage = []
    cumulative: set[int] = set()
    for e, a in zip(depths, positions):
        leaf = {x for x in range(27) if x % (3**e) == a}
        assert not (cumulative & leaf)
        cumulative |= leaf
        coverage.append(len(cumulative))
    assert coverage == [9,18,21,24,25,26,27]
    G3 = (163,271,487,4159,31051,16018507)
    fixed = (31,7,19,5167)
    table = []
    count = 0
    for triple in itertools.permutations(G3, 3):
        heads = fixed + triple
        ws = [order5(p) for p in heads]
        logs = []
        rows = []
        for p, w, a, e in zip(heads, ws, positions, depths):
            ell = next(x for x in range(w) if x % (3**e) == a and (w % 2 or x % 2 == 0))
            dh, _ = crt([(ell,w),(0,p)])
            r = (3 + pow(5,dh,p*p)) % (p*p)
            logs.append(ell)
            rows.append(r)
            assert (r-3-pow(5,dh,p*p)) % (p*p) == 0
        for d in range(54):
            hits = [i for i,w in enumerate(ws) if d % w == logs[i]]
            if d % 2 == 0:
                assert len(hits) == 1
            # Conditional basin filling on its guard, not a fabricated root.
            a1 = bool(hits) or fatal(3,2,{1},2,1,d)
            a0 = (1-1-pow(5,d,4)) % 4 == 3
            assert a0 and a1
            count += 1
        if triple == (271,4159,31051):
            table = [{'p':p,'ell':ell,'r_mod_p2':r} for p,ell,r in zip(heads,logs,rows)]
    assert count == 6480
    return {'pass':True,'conditional_assignments':120,'conditional_exponent_cases':count,
            'cumulative_even_cells':coverage,'literal_H0_head_states':table,
            'scope':'conditional guard/profile checks, NOT actual terminal roots'}


def skeleton_checks() -> dict:
    output = []
    for R in ((7,43),(7,43,127)):
        a,L = crt([(4,6)] + [(0,p) for p in R])
        rs = {p:(3+pow(5,a,p*p))%(p*p) for p in R}
        holes = []
        total = 0
        for d in range(4,L,6):
            total += 1
            covered = any(fatal(p,2,{1},rs[p],1,d) for p in R)
            if not covered:
                holes.append(d)
        assert holes == [a]
        output.append({'regular_rows':list(R),'a':a,'L':L,'guard_cells':total,
                       'covered_cells':total-1,'holes':holes,'states':rs})
    # An even-order relay can obstruct cross-parity persistence. No root is supplied.
    R = (31,1303)
    a,L = crt([(0,6)] + [(0,p) for p in R])
    assert a == 0 and order5(1303) == 62
    parity_counts = {}
    for b in (0,1):
        ds = range(0 if b == 0 else 3, L, 6)
        total = uncovered = 0
        for d in ds:
            total += 1
            if not any(fatal(p,2,{1},4,1,d) for p in R):
                uncovered += 1
        parity_counts[str(b)] = {'cells':total,'uncovered':uncovered}
    assert parity_counts['0']['uncovered'] == 1
    assert parity_counts['1']['uncovered'] == 1303
    return {'pass':True,'B7_regular_skeletons':output,
            '31_even_relay_skeleton':{'R':list(R),'L':L,'parity_counts':parity_counts},
            'scope':'actual regular-row skeletons; all nonregular terminal positions remain OPEN'}


def actual_31_collision() -> dict:
    M, U = 1312530, 40688430
    assert U == 31*M
    fixed = {3:2,20771:20773,40487:40493}
    cells = []
    fixed_hits = {}
    for f in (0,437511):
        covered_x = []
        for x in range(31):
            d = (f + M*(((x-f)*pow(M,-1,31))%31)) % U
            covered = any(fatal(p,2,{1},r,c,d) for p,r in fixed.items() for c in (0,1))
            if covered:
                covered_x.append(x)
            cells.append((covered,pow(5,d,961)))
        fixed_hits[str(f)] = covered_x
    assert fixed_hits == {'0':[0], '437511':[1]}
    hist: Counter[int] = Counter()
    for r in range(961):
        hit = 0
        for covered,power in cells:
            if covered or any(fatal_from_power(31,2,{1},r,c,power) for c in (0,1)):
                hit += 1
        hist[hit] += 1
    assert dict(hist) == {2:899,60:58,61:4}
    return {'pass':True,'fixed_hits':fixed_hits,'histogram':dict(sorted(hist.items())),
            'states_checked':961,'exponent_cells':62,'max_covered':max(hist),
            'scope':'actual shared-row collision; violates seven-basin vertex disjointness'}


def actual_three_way_MUS() -> dict:
    states = set(range(9))
    family = [{r for r in states if fatal(3,2,{1},r,0,d)} for d in (0,2,4)]
    assert family == [{5,8},{2,5},{2,8}]
    pairs = [sorted(family[i]&family[j]) for i,j in itertools.combinations(range(3),2)]
    assert all(pairs) and not set.intersection(*family)
    parity_family = [{r for r in states if fatal(3,2,{1},r,1,d)} for d in (3,1,5)]
    assert parity_family == family
    return {'pass':True,'prime':3,'K':2,'E':[1],'states_checked':9,'anchor':0,'exponents':[0,2,4],
            'allowed_actual_residues':[sorted(x) for x in family],
            'pair_intersections':pairs,'triple_intersection':[],
            'opposite_parity_version':{'anchor':1,'exponents':[3,1,5],
                'missing_cylinders':['d=0 mod3, odd','d=1 mod3, odd','d=5 mod9, odd'],
                'allowed_actual_residues':[sorted(x) for x in parity_family]},
            'scope':'actual row3 MUS; basin-derived necessity is conditional on parity-defective 31 closure, not an instantiated seven-root ledger'}


def opposite_parity_row3() -> dict:
    checks = []
    for K in range(2,6):
        modulus = 3**K
        ell = 2*3**(K-1)
        period = math.lcm(54,ell)
        accepted = list(range(1,K,2))
        powers = {d:pow(5,d,modulus) for d in range(ell)}
        logs = {v:d for d,v in powers.items()}
        required = [d for d in range(1,period,2) if d%3 == 1 or d%9 == 5]
        possible = 0
        tested = 0
        for r in range(modulus):
            if r%3 not in (0,2):
                continue  # even-d inactive at c=1
            for mask in range(1,1<<len(accepted)):
                E = {h for j,h in enumerate(accepted) if mask & (1<<j)}
                tested += 1
                if all(fatal_from_power(3,K,E,r,1,powers[d%ell]) for d in required):
                    possible += 1
                    alpha = logs[(r-3)%modulus]
                    assert 1 in E and alpha % 3 == 0 and alpha % 2 == 1
                    assert not fatal(3,K,E,r,1,alpha)
        assert possible == 3**(K-2) * (2**(len(accepted)-1))
        checks.append({'K':K,'states_and_E_tested':tested,'passing_states_and_E':possible,
                       'all_passing_centers_mod3':0})
    return {'pass':True,'checks':checks,
            'scope':'bounded check of local row3 lemma; unbounded argument is in REPORT.md'}


def profile_join(A: frozenset[int],B: frozenset[int]) -> frozenset[int]:
    return frozenset(a|b for a in A for b in B)


def typed_profile_checks() -> dict:
    domains = [frozenset(i for i in range(4) if bits&(1<<i)) for bits in range(1,16)]
    count = 0
    for A,B,C in itertools.product(domains,repeat=3):
        assert profile_join(profile_join(A,B),C) == profile_join(A,profile_join(B,C))
        count += 1
    split = frozenset((1,2))
    assert all(bool(m&3) for m in split) and not all(m==3 for m in split)
    # Seven whole-state profiles; canonical guards plus row3 and dyadic A0.
    leaves = [(1,0),(1,1),(2,2),(2,5),(3,8),(3,17),(3,26)]
    for z in range(54):
        accum = frozenset((1,)) # dyadic A0
        if fatal(3,2,{1},2,1,z):
            accum = profile_join(accum,frozenset((2,)))
        for i,(e,a) in enumerate(leaves):
            full = z % (3**e) == a and (z%2==0 or i==0)
            # Guaranteed A1 projection only: extra actual A0 events are ignored,
            # not suppressed. Off-guard profiles conservatively include no coverage.
            prof = frozenset((2,)) if full else frozenset((0,2))
            accum = profile_join(accum,prof)
        assert all(m == 3 for m in accum)
    return {'pass':True,'associativity_cases':count,'typed_BOTH_separator_cells':54,
            'EITHER_not_BOTH_actual_mask_profile':sorted(split),
            'scope':'exact profile algebra; conditional lower-envelope A1-projection sufficiency check, not instantiated full-root masks'}


def resultant_gate_check() -> dict:
    f = {2:67,269:15,1609:3,1877:4,3083:1,4289:1,4691:1,5897:1,7639:1,20771:1,27337:1}
    G = math.prod(p**e for p,e in f.items())
    phi = (5**67-1)//4
    g = math.gcd(phi,G)
    assert g == 432821 == 269*1609
    assert prime(269) and prime(1609) and 269%4 == 1 and 1609%4 == 1
    assert (8-7)%155 != 0
    return {'pass':True,'gcd':g,'remaining_primes':[269,1609],
            'scope':'recomputed gcd from SOURCE resultant factorization, not a new resultant computation'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULTS.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    checks = {
        'arithmetic':arithmetic_checks(),
        'frontier_and_literal_model':frontier_checks(),
        'regular_skeletons':skeleton_checks(),
        'actual_shared_31_collision':actual_31_collision(),
        'actual_three_way_MUS':actual_three_way_MUS(),
        'opposite_parity_row3':opposite_parity_row3(),
        'typed_profiles':typed_profile_checks(),
        'source_resultant_gcd_gate':resultant_gate_check(),
    }
    result = {'all_checks_passed':all(x['pass'] for x in checks.values()),
              'authority_main':'fd59aad038a09f2fc6df7039111408fa231c27dd',
              'actual_seven_root_ledger_found':False,'A303656_solved':False,
              'source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'elapsed_seconds':round(time.perf_counter()-start,4),'checks':checks}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'all_checks_passed':result['all_checks_passed'],
                      'elapsed_seconds':result['elapsed_seconds'],'output':str(args.output)},indent=2))

if __name__ == '__main__':
    main()
