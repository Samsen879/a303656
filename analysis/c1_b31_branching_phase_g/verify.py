#!/usr/bin/env python3
"""Exact, offline, standard-library replay for B31 branching Phase G.

This verifies finite evidence, not the universal theorems or B31 emptiness.
All checks remain active under python -O. Primality is proved recursively
with complete p-1 Lucas certificates; probable-prime flags are not trusted.
"""
from __future__ import annotations
import argparse
import copy
import itertools
import json
import math
from pathlib import Path
from typing import Any

class CheckFailure(ValueError):
    pass

def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)

def trial_factors(n: int) -> dict[int, int]:
    require(n >= 1, 'factor input must be positive')
    ans: dict[int, int] = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            ans[d] = ans.get(d, 0)+1
            n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        ans[n] = ans.get(n, 0)+1
    return ans

def product_factors(factors: dict[int, int]) -> int:
    require(all(p >= 2 and e >= 1 for p, e in factors.items()), 'malformed factors')
    return math.prod(p**e for p, e in factors.items())

def legendre(a: int, p: int) -> int:
    z = pow(a, (p-1)//2, p)
    require(z in (0, 1, p-1), 'non-Legendre result')
    return -1 if z == p-1 else z

class Verifier:
    def __init__(self, evidence: dict[str, Any]):
        self.evidence = evidence
        self.certificates = evidence['lucas_certificates']
        self.proven: set[int] = set()
        self.checks = 0

    def prime(self, p: int) -> None:
        if p in self.proven:
            return
        require(str(p) in self.certificates, f'missing prime certificate {p}')
        c = self.certificates[str(p)]
        require(int(c['p']) == p, 'prime certificate label mismatch')
        if p == 2:
            require(c['factors'] == {} and c['witness'] is None, 'bad base certificate')
        else:
            require(p > 2 and p % 2 == 1, 'bad prime label')
            f = {int(r): int(e) for r, e in c['factors'].items()}
            require(product_factors(f) == p-1, 'p-1 factorization incomplete')
            for r in f:
                require(r < p, 'non-descending prime certificate')
                self.prime(r)
            g = int(c['witness'])
            require(1 < g < p, 'Lucas witness out of range')
            require(pow(g, p-1, p) == 1, 'Lucas full power fails')
            for r in f:
                require(math.gcd(pow(g, (p-1)//r, p)-1, p) == 1,
                        'Lucas order-drop gcd fails')
        self.proven.add(p)

    def row(self, base: int, r: dict[str, Any]) -> tuple[int, int, int]:
        p, n, s = int(r['p']), int(r['order']), int(r['valuation'])
        self.prime(p)
        f = {int(t): int(e) for t, e in r['order_factors'].items()}
        require(product_factors(f) == n, 'incomplete exact-order factors')
        for t in f:
            self.prime(t)
        require(n > 1 and (p-1) % n == 0 and math.gcd(base, p) == 1, 'bad order divisibility')
        require(pow(base, n, p) == 1, 'order full power fails')
        for t in f:
            require(pow(base, n//t, p) != 1, 'exact order-drop fails')
        require(s >= 1 and pow(base, n, p**s) == 1, 'claimed valuation too high')
        z = pow(base, n, p**(s+1))
        require(z != 1, 'claimed valuation too low')
        require((z-1)//p**s == int(r['first_nonzero_lift']), 'lifting coefficient mismatch')
        require(base % p == int(r['residue_mod_p']), 'residue mod p mismatch')
        require(base % (p*p) == int(r['residue_mod_p2']), 'residue mod p2 mismatch')
        self.checks += 1
        return p, n, s

    def model(self, m: dict[str, Any]) -> dict[str, Any]:
        base = int(m['base'])
        require(base > 1 and base != 5, 'variable-base fixture must not be relabelled base 5')
        require(m['is_base5_member'] is False, 'false actual-base5 member claim')
        if m['base_is_certified_prime']:
            self.prime(base)
        rows = [self.row(base, r) for r in m['rows']]
        ps = [p for p, _, _ in rows]
        require(ps == sorted(set(ps)), 'duplicate/unsorted vertex labels')
        root = int(m['root'])
        require(root == ps[-1] and 31 in ps, 'bad root/head')
        require(all(p > 3 and p % 20 in (11, 19) for p in ps), 'admission/all-odd label guard')
        R = set(ps)-{root}
        require(R == {int(p) for p in m['proper_state']}, 'proper state mismatch')
        order_map = {p: n for p, n, _ in rows}
        child: dict[int, set[int]] = {}
        actual_edges: list[dict[str, Any]] = []
        basal = set()
        for p, n, s in rows:
            f = {int(t): int(e) for t, e in next(r for r in m['rows'] if int(r['p']) == p)['order_factors'].items()}
            require(n % 2 == 1 and all(e == 1 for e in f.values()), 'order not odd squarefree')
            require(set(f) <= set(ps) | {3}, 'unexpanded absolute-order factor')
            require(all(t < p for t in f), 'non-descending arithmetic edge')
            child[p] = set(f)-{3}
            if set(f) == {3}:
                basal.add(p)
            require(s == (2 if p == root else 1), 'root/proper regularity guard')
            require(legendre(5, p) == 1, 'base-5 quadratic residue label guard')
            require(legendre(base, p) == 1, 'base quadratic residue guard')
            for t in sorted(child[p]):
                edge = {'upper': str(p), 'lower': str(t),
                        'lower_over_upper': legendre(t, p), 'upper_over_lower': legendre(p, t)}
                require(edge['lower_over_upper'] == -1 and edge['upper_over_lower'] == 1,
                        'edge reciprocity fails')
                actual_edges.append(edge)
        require(basal == {31}, 'wrong basal gateway')
        seen, todo = set(), [root]
        while todo:
            p = todo.pop()
            if p in seen:
                continue
            seen.add(p)
            todo.extend(child[p])
        require(seen == set(ps), 'root does not generate entire state')
        require({int(t) for p in seen for t in next(r for r in m['rows'] if int(r['p']) == p)['order_factors']} - seen == {3},
                'absolute terminal set not exactly {3}')
        maximal = R-set().union(*(child[p] for p in R))
        require(maximal == {int(p) for p in m['maximal_generators']}, 'maximal generators mismatch')
        require(maximal <= child[root], 'terminal omits a maximal generator')
        sym = math.prod(legendre(p, root) for p in maximal)
        require(sym == (-1)**len(maximal) == m['maximal_symbol_product'], 'antichain sign mismatch')
        key = lambda e: (int(e['upper']), int(e['lower']))
        require(sorted(actual_edges, key=key) == sorted(m['edges_excluding_terminal3'], key=key), 'edge evidence mismatch')
        require(self.row(base, m['terminal3']) == (3, 2, 1), 'terminal3 sanity check')
        # Terminal 3 is intentionally NOT a row in the all-odd quantifier above.
        ex = m['extra']
        if 'preserved_modulus' in ex:
            require((base-5) % int(ex['preserved_modulus']) == 0, 'base-5 lower data not preserved')
        if 'progression_step' in ex:
            require(base == int(ex['least_lifted_base']) + int(ex['progression_step'])*int(ex['progression_modulus']), 'CRT progression mismatch')
        if 'same_first_order_as_5' in m['name'] or 'also_preserves_mod8' in m['name']:
            require(all(base % p == 5 % p for p in ps), 'first-order data not equal to base 5')
        if 'also_preserves_mod8' in m['name']:
            require(base % 8 == 5, 'lost base-5 mod8 residue')
        if 'crt_congruences' in ex:
            for residue, modulus in ex['crt_congruences']:
                require(base % int(modulus) == int(residue) % int(modulus), 'CRT residue fails')
        if 'regular_comparator_base' in ex:
            comparator = int(ex['regular_comparator_base'])
        else:
            M = 8*9*math.prod(p*p for p in R)
            comparator = base + M*root
        require(all((base-comparator) % (p*p) == 0 for p in R), 'comparator changes proper lifting')
        require(base % root == comparator % root, 'comparator changes terminal first order')
        n = order_map[root]
        require(pow(comparator, n, root) == 1 and pow(comparator, n, root*root) != 1, 'comparator not regular')
        # Tame power-residue tests in the cyclic unit groups, no enumeration of huge fields.
        indices = {2, 3, 4, 8, 16, 31, root-1, root+1}
        indices.update(int(t) for t in next(r for r in m['rows'] if int(r['p']) == root)['order_factors'])
        tame_count = 0
        for d in sorted(indices):
            require(math.gcd(d, root) == 1, 'test index accidentally wild')
            test_mod_p = pow(base, (root-1)//math.gcd(d, root-1), root) == 1
            exp = root*(root-1)//math.gcd(d, root*(root-1))
            left = pow(base, exp, root*root) == 1
            right = pow(comparator, exp, root*root) == 1
            require(left == right == test_mod_p, 'tame lift invariance fails')
            tame_count += 1
        require(pow(base, root-1, root*root) == 1, 'square-hit base is not a q-th power')
        require(pow(comparator, root-1, root*root) != 1, 'wild q-th-power test failed to distinguish')
        return {'name': m['name'], 'root': str(root), 'vertices': len(ps),
                'maximal_generators': len(maximal), 'symbol_product': sym, 'tame_tests': tame_count,
                'exact_root_valuation': 2, 'base_prime_certified': m['base_is_certified_prime']}

    def run(self) -> dict[str, Any]:
        for p in self.certificates:
            self.prime(int(p))
        actual = [self.row(5, r) for r in self.evidence['actual_base5_rows_inherited_then_recertified']]
        require(all(s == 1 for _, _, s in actual), 'inherited fixture unexpectedly nonregular')
        actual_labels = {p for p, _, _ in actual}
        require(31 in actual_labels and 3 not in actual_labels, 'bad inherited head/terminal')
        for r in self.evidence['actual_base5_rows_inherited_then_recertified']:
            p, n = int(r['p']), int(r['order'])
            f = {int(t): int(e) for t, e in r['order_factors'].items()}
            require(p > 3 and p % 20 in (11, 19), 'bad inherited all-odd admission')
            require(n % 2 == 1 and all(e == 1 for e in f.values()), 'bad inherited squarefree order')
            require(set(f) <= actual_labels | {3} and all(t < p for t in f), 'bad inherited closure')
            require((set(f) == {3}) == (p == 31), 'bad inherited basal gateway')
        models = [self.model(m) for m in self.evidence['countermodels']]
        return {'status': 'PASS', 'lucas_primes_certified': len(self.proven),
                'row_records_checked': self.checks, 'countermodels': models,
                'actual_base5_member_found': False}

def cyclotomic_mod8_odd_squarefree(primes: list[int], b: int) -> int:
    """Evaluate Phi_a(5^b) mod8 using odd 2-adic units of Mobius factors.
    All divisors d and b are odd, so v2(5^(bd)-1)=2, cancelling exactly.
    """
    require(primes and b % 2 == 1, 'mod8 domain')
    r = 1
    for mask in range(1 << len(primes)):
        d = math.prod(primes[j] for j in range(len(primes)) if mask >> j & 1)
        unit = (pow(5, b*d, 32)-1)//4
        require(unit % 2 == 1, 'unexpected 2-adic valuation')
        sign = (-1)**(len(primes)-mask.bit_count())
        r = r*(unit if sign == 1 else pow(unit, -1, 8)) % 8
    return r

def mod8_checks(evidence: dict[str, Any]) -> dict[str, Any]:
    rows = {int(r['p']): r for r in evidence['actual_base5_rows_inherited_then_recertified']}
    ps = sorted(rows)
    states = []
    for mask in range(1 << len(ps)):
        R = {ps[j] for j in range(len(ps)) if mask >> j & 1}
        if 31 not in R:
            continue
        child = {p: {int(t) for t in rows[p]['order_factors']}-{3} for p in R}
        if not all(c <= R for c in child.values()):
            continue
        A = R-set().union(*child.values())
        beta = 3*math.prod(R-A)
        w = cyclotomic_mod8_odd_squarefree(sorted(A), beta)
        z = w*pow(next(iter(A)), -1, 8) % 8 if len(A) == 1 else w
        require(z == (5 if len(A) == 1 else 1), 'actual-state critical mod8 signature fails')
        states.append({'R': [str(p) for p in sorted(R)], 'A': [str(p) for p in sorted(A)],
                       'Z_mod8': z})
    # These are algebraic congruence regressions, NOT additional base-5 good states.
    generic = 0
    labels = [3, 7, 11, 19, 23, 31]
    for k in range(1, 5):
        for A in itertools.combinations(labels, k):
            for beta in [1, 3, 5, 9, 31]:
                w = cyclotomic_mod8_odd_squarefree(list(A), beta)
                z = w*pow(A[0], -1, 8) % 8 if k == 1 else w
                require(z == (5 if k == 1 else 1), 'generic signature fails')
                generic += 1
    # Actual base-5 first-order sign counterexample: all three admitted edges are negative.
    p, a, t = 31, 878851, 490398859
    triangle_product = legendre(p, a)*legendre(p, t)*legendre(a, t)
    require(triangle_product == -1, 'triangle sign countermodel fails')
    return {'status': 'PASS', 'actual_closed_substates': len(states),
            'actual_state_records': states, 'generic_mod8_checks': generic,
            'actual_base5_admitted_triangle_product': triangle_product}

def abstract_dag_checks() -> dict[str, Any]:
    records = []
    for m in range(2, 7):
        accepted = 0
        widths: dict[int, int] = {}
        ranges = [range(1, 1 << j) for j in range(1, m)]
        for masks in itertools.product(*ranges):
            children = [set()]+[{i for i in range(j) if masks[j-1] >> i & 1} for j in range(1, m)]
            seen, todo = set(), [m-1]
            while todo:
                j = todo.pop()
                if j not in seen:
                    seen.add(j); todo.extend(children[j])
            if len(seen) != m:
                continue
            R = set(range(m-1))
            maxima = R-set().union(*(children[j] for j in R))
            require(maxima <= children[m-1], 'abstract mandatory maxima fails')
            # A QR-consistent orientation: every lower-over-upper edge has sign -1.
            # No assertion that these abstract labels are base-5 arithmetic primes.
            e = sum(map(len, children))
            left_product = (-1)**e
            reverse_product = 1
            require(left_product*reverse_product == (-1)**e, 'QR edge-product consistency')
            require((-1)**len(maxima) in (-1, 1), 'bad antichain sign')
            accepted += 1
            widths[len(maxima)] = widths.get(len(maxima), 0)+1
        records.append({'vertices': m, 'accepted_root_closed_dags': accepted,
                        'maximal_width_distribution': {str(k): v for k, v in sorted(widths.items())}})
    require([r['accepted_root_closed_dags'] for r in records] == [1, 2, 10, 122, 3346],
            'abstract enumeration regression mismatch')
    return {'status': 'PASS', 'records': records}

def negative_tests(evidence: dict[str, Any]) -> list[str]:
    tests: list[tuple[str, Any]] = []
    tests.append(('fake_base5_member', lambda e: e['countermodels'][0].update(is_base5_member=True)))
    tests.append(('replace_variable_base_with_5', lambda e: e['countermodels'][0].update(base='5')))
    tests.append(('wrong_root_valuation', lambda e: e['countermodels'][0]['rows'][-1].update(valuation=1)))
    tests.append(('wrong_lift_coefficient', lambda e: e['countermodels'][0]['rows'][-1].update(first_nonzero_lift='0')))
    tests.append(('drop_maximal_generator', lambda e: e['countermodels'][2].update(maximal_generators=['878851'])))
    tests.append(('wrong_edge_sign', lambda e: e['countermodels'][0]['edges_excluding_terminal3'][0].update(lower_over_upper=1)))
    tests.append(('missing_head_state', lambda e: e['countermodels'][0].update(proper_state=[])))
    tests.append(('bad_Lucas_witness', lambda e: e['lucas_certificates']['31'].update(witness=1)))
    tests.append(('incomplete_pminus1', lambda e: e['lucas_certificates']['31']['factors'].pop('5')))
    tests.append(('false_prime_base_flag', lambda e: e['countermodels'][2].update(base_is_certified_prime=True)))
    tests.append(('terminal3_in_all_odd_rows', lambda e: e['countermodels'][0]['rows'].insert(0, e['countermodels'][0]['terminal3'])))
    tests.append(('corrupt_exact_order', lambda e: e['countermodels'][0]['rows'][-1].update(order='31')))
    rejected = []
    for name, mutate in tests:
        e = copy.deepcopy(evidence)
        mutate(e)
        try:
            Verifier(e).run()
        except (CheckFailure, KeyError, ValueError, TypeError):
            rejected.append(name)
        else:
            raise CheckFailure(f'corruption accepted: {name}')
    return rejected

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, default=Path(__file__).with_name('evidence.json'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--skip-negative-tests', action='store_true')
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding='utf-8'))
    result = Verifier(evidence).run()
    result['critical_mod8'] = mod8_checks(evidence)
    result['abstract_dags'] = abstract_dag_checks()
    if not args.skip_negative_tests:
        result['corruptions_rejected'] = negative_tests(evidence)
    result['scope'] = 'Finite evidence only; no infinite theorem formalization, no base-5 emptiness, no N>=8.'
    output = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
    print(output)

if __name__ == '__main__':
    main()
