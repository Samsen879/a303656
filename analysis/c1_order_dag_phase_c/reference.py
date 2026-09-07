#!/usr/bin/env python3
"""Exact Phase-C reference verifier. Standard library only; no repository imports.

Arithmetic inputs include discovery output, NOT trusted prime declarations.
Every prime is re-proved with a recursive complete n-1 Lucas certificate.
The conditional construction fixture does NOT instantiate nonregular roots.
"""
from __future__ import annotations
from functools import lru_cache
from fractions import Fraction
from itertools import combinations, product
from math import prod
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parent

def fail(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def factors_small(n: int) -> dict[int, int]:
    fail(n >= 1, 'positive factorization input required')
    ans: dict[int, int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            ans[p] = ans.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        ans[n] = ans.get(n, 0) + 1
    return ans


@lru_cache(None)
def cyclo5(n: int) -> int:
    fail(n >= 1, 'positive cyclotomic index required')
    value = 5**n-1
    for d in range(1, n):
        if n % d == 0:
            a = cyclo5(d)
            fail(value % a == 0, 'cyclotomic division not exact')
            value //= a
    return value


class Arithmetic:
    def __init__(self, data: dict):
        self.data = data
        self.proven: set[int] = set()
        self.visiting: set[int] = set()

    def prime(self, n: int) -> None:
        if n in self.proven:
            return
        fail(n >= 2 and n not in self.visiting, 'invalid/cyclic prime certificate')
        self.visiting.add(n)
        c = self.data['primality_certificates'][str(n)]
        fs = {int(p): int(e) for p, e in c['n_minus_1_factors'].items()}
        if n == 2:
            fail(not fs, 'invalid base certificate')
        else:
            fail(n % 2 == 1, 'even composite')
            fail(all(2 <= p < n and e > 0 for p, e in fs.items()), 'bad n-1 factors')
            fail(prod(p**e for p, e in fs.items()) == n-1, 'incomplete n-1 factorization')
            for p in fs:
                self.prime(p)
            a = int(c['base'])
            fail(pow(a, n-1, n) == 1, 'Fermat/Lucas equation fails')
            fail(all(pow(a, (n-1)//p, n) != 1 for p in fs), 'full-order Lucas test fails')
        self.visiting.remove(n)
        self.proven.add(n)

    def order(self, q: int, w: int, fs: dict[int, int]) -> int:
        self.prime(q)
        fail(prod(p**e for p, e in fs.items()) == w, 'wrong order factorization')
        for p in fs:
            self.prime(p)
        fail((q-1) % w == 0 and pow(5, w, q) == 1, 'invalid claimed order')
        fail(all(pow(5, w//p, q) != 1 for p in fs), 'claimed order not minimal')
        s, modulus = 0, q
        while pow(5, w, modulus) == 1:
            s += 1
            modulus *= q
        return s

    def cyclotomics(self) -> list[dict]:
        records = []
        for ns, item in sorted(self.data['cyclotomics'].items(), key=lambda t: int(t[0])):
            n = int(ns)
            fs = {int(p): int(e) for p, e in item['factors'].items()}
            value = cyclo5(n)
            fail(value == int(item['value']), 'wrong cyclotomic integer')
            fail(value == prod(p**e for p, e in fs.items()), 'factor product mismatch')
            factors = []
            for q, exponent in fs.items():
                self.prime(q)
                w = n
                for p in factors_small(n):
                    while w % p == 0 and pow(5, w//p, q) == 1:
                        w //= p
                s = self.order(q, w, factors_small(w))
                factors.append({'q': str(q), 'multiplicity': exponent,
                                'order': w, 'lifting_s': s, 'admitted': q % 4 == 3,
                                'primitive_at_index': w == n})
            records.append({'n': n, 'value': str(value), 'factors': factors,
                            'squarefree': all(e == 1 for e in fs.values())})
        return records

    def dags(self) -> dict:
        rows = {}
        for qs, row in self.data['order_dag'].items():
            q, w = int(qs), int(row['order'])
            fs = {int(p): int(e) for p, e in row['factors'].items()}
            s = self.order(q, w, fs)
            rows[q] = {'order': w, 'factors': fs, 's': s}

        @lru_cache(None)
        def terminals(q: int) -> tuple[int, ...]:
            if q == 3 or q % 4 == 1:
                return (q,)
            fail(q in rows, 'missing admitted relay')
            out: set[int] = set()
            for p in rows[q]['factors']:
                if p != 2:
                    fail(p < q, 'order DAG must strictly decrease')
                    out.update(terminals(p))
            fail(bool(out), 'empty absolute terminal set')
            return tuple(sorted(out))

        roots = {str(q): {'order': rows[q]['order'], 's': rows[q]['s'],
                          'terminals': list(terminals(q))}
                 for q in (20771, 40487, 1645333507)}
        fail([roots[str(q)]['s'] for q in (20771,40487,1645333507)] == [2,2,2], 'nonregularity check')
        fail(roots['20771']['terminals'] == [3,5], '20771 closure mismatch')
        fail(roots['40487']['terminals'] == [3,653], '40487 closure mismatch')
        fail(roots['1645333507']['terminals'] == [3,761,1429], 'large-root closure mismatch')
        return {'rows': rows, 'roots': roots, 'inventory_range_replayed': False}


def frontier_profiles(p: int, limit: int) -> list[tuple[int, ...]]:
    depth = (limit-1)//(p-1)
    start = (1,) + (0,)*depth
    seen, stack = {start}, [start]
    while stack:
        a = stack.pop()
        if sum(a)+p-1 > limit:
            continue
        for i in range(depth):
            if a[i]:
                b = list(a)
                b[i] -= 1
                b[i+1] += p
                b = tuple(b)
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
    return sorted(a for a in seen if a[0] == 0)


def minimal_deficient(labels: tuple[int, ...]) -> list[tuple[int, ...]]:
    # root labels 1={3}, 2={5}, 3={3,5}; capacities 2 and 4.
    deficient: set[int] = set()
    ans = []
    for size in range(1, len(labels)+1):
        for subset in combinations(range(len(labels)), size):
            mask = sum(1 << i for i in subset)
            nb = 0
            for i in subset:
                nb |= labels[i]
            cap = (2 if nb & 1 else 0) + (4 if nb & 2 else 0)
            if size > cap:
                if not any(s & mask == s for s in deficient):
                    ans.append(subset)
                deficient.add(mask)
    return ans


def combinatorics() -> dict:
    signatures = []
    ts = [3,5,13,17]
    for r in range(1, len(ts)+1):
        for terminal_set in combinations(ts, r):
            m = 1 + sum(p-1 for p in terminal_set)
            if m <= 19:
                signatures.append({'size': m, 'terminals': terminal_set})
    signatures.sort(key=lambda x: (x['size'], x['terminals']))
    cases = 0
    for labels in product((1,2,3), repeat=7):
        for subset in minimal_deficient(labels):
            nb = 0
            for i in subset:
                nb |= labels[i]
            cap = (2 if nb & 1 else 0) + (4 if nb & 2 else 0)
            fail(len(subset) == cap+1, 'minimal circuit equality')
            if nb & 1:
                fail(sum(bool(labels[i]&1) for i in subset) >= 3, 'degree 3')
            if nb & 2:
                fail(sum(bool(labels[i]&2) for i in subset) >= 5, 'degree 5')
        cases += 1
    profiles = {str(p): frontier_profiles(p, 12) for p in (3,5,7,11)}
    seven = [v for v in frontier_profiles(3,7) if any(v[3:])]
    fail(seven == [(0,2,2,3)], 'seven-leaf deep ternary profile')
    witness_max = {}
    for n in range(5,13):
        tuples = (xs for xs in product(range(1,n-3), repeat=4) if sum(xs) < n)
        witness_max[n] = max(prod(xs)*(n-sum(xs)) for xs in tuples)
    fail([witness_max[n] for n in (5,6,7,8)] == [1,2,4,8], 'witness counts')
    # The cross-strip lemma leaves at least three first-level cells uncovered.
    H3, H5 = {0,1}, {0,1}
    union = {(a,b) for a in range(3) for b in range(5) if a in H3 or b in H5}
    holes = sorted(set(product(range(3),range(5))) - union)
    fail(holes == [(2,2),(2,3),(2,4)], 'cross-strip holes')
    roots_by_type = [{'a':a,'b':b,'k':7-a-b} for a in range(8) for b in range(8-a)]
    return {'terminal_signatures_le_19': signatures, 'labeled_seven_graphs_checked': cases,
            'seven_terminal_count_profiles': roots_by_type,
            'frontier_profiles_le_12': profiles, 'deep_seven_ternary_profile': seven,
            'first_digit_five_witness_maxima': witness_max,
            'witness_scope': 'For n>=9 deeper five-frontiers also occur: not a total clause bound.',
            'cross_strip_holes': holes,
            'depth_three_gateway_triples': list(combinations([163,271,487,4159,31051,16018507],3))}


def conditional_fixture(arithmetic: Arithmetic) -> dict:
    # These are ACTUAL REGULAR ROWS. Their upstream rigid seeds are conditional
    # contractions of not-yet-instantiated prime-order chains, NOT actual roots.
    heads = [(31,1,0),(7,1,1),(19,2,2),(5167,2,5),(271,3,8),(4159,3,17),(31051,3,26)]
    records, checked = [], 0
    for h, depth, residue in heads:
        arithmetic.prime(h)
        w = 3**depth * (2 if h in (7,5167) else 1)
        fail(arithmetic.order(h,w,factors_small(w)) == 1, 'gateway must be regular')
        log = residue
        if w % 2 == 0 and log % 2:
            log += 3**depth
        d0 = h * ((log*pow(h,-1,w)) % w)
        rh = (3 + pow(5,d0,h*h)) % (h*h)
        power = 1
        for d in range(w*h):
            value = (rh-3-power) % (h*h)
            actual = value % h == 0 and value != 0
            expected = d % w == log and d % h != 0
            fail(actual == expected, 'actual regular-row normal form mismatch')
            power = power*5 % (h*h)
            checked += 1
        records.append({'head':h,'w':w,'depth':depth,'residue':residue,
                        'log':log,'r_mod_h2':rh,'upstream_seed':'CONDITIONAL x_h=0'})
    r3 = 2
    for d in range(6):
        v = (r3-3-pow(5,d,9)) % 9
        fail((v%3 == 0 and v != 0) == (d%2 == 1 and d%3 != 0), 'row 3 fixture')
    collapsed = []
    for d in range(54):
        active_heads = [row['head'] for row in records if d%row['w'] == row['log']]
        row3_fatal = d%2 == 1 and d%3 != 0
        fail(bool(active_heads) or row3_fatal, 'conditional collapsed cover has hole')
        collapsed.append({'d_mod_54':d,'head_pair_cover_options':active_heads,'row3_fatal':row3_fatal})
    leaves = [(depth,residue) for _,depth,residue in heads]
    for j in range(7):
        good = set()
        for i,(depth,residue) in enumerate(leaves):
            if i != j:
                good.update(a for a in range(27) if a % 3**depth == residue)
        fail(len(good) < 27, 'seven-frontier irredundancy')
    fail(all((1-1-pow(5,d,4))%4 == 3 and (1-3-pow(5,d,4))%4 == 1 for d in range(2)), 'two-adic completion')
    return {'actual_regular_rows':records, 'actual_regular_row_comparisons':checked,
            'r3_mod_9':2,'r2_mod_4':1,'collapsed_classes':collapsed,
            'actual_nonregular_roots_instantiated':False,
            'actual_complete_certificate_constructed':False,
            'scope':'Conditional chain-completion theorem fixture only; seven upstream seeds are not actual prime rows.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.resolve().is_relative_to(ROOT):
        parser.error('Choose an output directory outside the frozen research bundle')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT/'arithmetic_inputs.json').read_text())
    arithmetic = Arithmetic(data)
    for n in data['primality_certificates']:
        arithmetic.prime(int(n))
    cyclotomic_records = arithmetic.cyclotomics()
    dags = arithmetic.dags()
    comb = combinatorics()
    fixture = conditional_fixture(arithmetic)
    output = {'arithmetic': {'prime_certificates_verified':len(arithmetic.proven),
                             'cyclotomics':cyclotomic_records,'dag':dags},
              'combinatorics':comb,'conditional_construction_fixture':fixture,
              'scope':{'source_code_imported':False,'standard_library_verifier':True,
                       'prime_range_scan_performed':False,'github_writes':'NONE',
                       'universal_theorems_proved_by_enumeration':False}}
    path = args.output_dir/'reference_results.json'
    path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','output':str(path),
                      'primality_certificates':len(arithmetic.proven),
                      'cyclotomic_values':len(cyclotomic_records),
                      'seven_labeled_hall_graphs':comb['labeled_seven_graphs_checked'],
                      'actual_regular_row_comparisons':fixture['actual_regular_row_comparisons'],
                      'conditional_nonregular_roots_instantiated':False},indent=2))

if __name__ == '__main__':
    main()
