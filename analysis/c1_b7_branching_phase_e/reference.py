#!/usr/bin/env python3
"""Standalone exact checks for the B7 branching Phase-E reduction.

Only the Python standard library is required.  No network, prime inventory,
repository imports, or uninstantiated nonregular roots are used by this replay.
The finite DAG tests verify a combinatorial invariant, not B7 emptiness.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

A7 = (43, 127, 379, 7603, 19531, 519499)
DELTA = (1, 2, 3, 6)
I_MULTIPLIERS = (1, 2, 3, 6, 7, 14, 21, 42)
# Each entry is independently certified below, not trusted as a primality label.
ACTUAL_ORDERS = {
    7: 6, 43: 42, 127: 42, 379: 21, 7603: 42,
    19531: 7, 519499: 21,
    9547: 86, 42743: 602, 18471511: 129,
    558801427: 258, 7866608083: 86,
    6717031: 5461,
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def prime_by_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def factor_trial(n: int) -> dict[int, int]:
    require(n >= 1, 'factor input must be positive')
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def repeated_mod_power(base: int, exponent: int, modulus: int) -> int:
    """A deliberately different modular-power organization for small exponents."""
    out = 1
    for _ in range(exponent):
        out = out * base % modulus
    return out


def certify_prime_order(p: int, n: int) -> dict:
    require(prime_by_trial(p), f'not a certified prime: {p}')
    require(p % 4 == 3 and p > 3, 'not admitted >3')
    factors = factor_trial(n)
    require((p - 1) % n == 0, 'order does not divide p-1')
    require(all(e == 1 for e in factors.values()), 'order is not squarefree')
    require(pow(5, n, p) == 1, 'not an order multiple')
    drops = {str(l): pow(5, n // l, p) for l in factors}
    require(all(v != 1 for v in drops.values()), 'not the exact order')
    lift = pow(5, n, p * p)
    require(lift == repeated_mod_power(5, n, p * p), 'modular cores disagree')
    require(lift != 1, 'fixture unexpectedly nonregular')
    require((lift - 1) % p == 0, 'inconsistent lifting residue')
    return {
        'p': p, 'order': n, 'order_factors': {str(k): v for k, v in factors.items()},
        'primality_method': 'complete odd trial division through isqrt(p)',
        'trial_bound': math.isqrt(p), 'exact_order_drop_residues': drops,
        'pow_5_order_mod_p_squared': lift, 'lifting_coefficient': (lift - 1) // p,
        's': 1, 'classification': 'ACTUAL REGULAR PRIME',
    }


def admitted_support(n: int) -> set[int]:
    return {p for p in factor_trial(n) if p > 3}


def closure(v: int, orders: dict[int, int]) -> set[int]:
    require(v in orders, f'missing arithmetic row: {v}')
    result: set[int] = set()
    todo = [v]
    while todo:
        p = todo.pop()
        if p in result:
            continue
        require(p in orders and p % 4 == 3 and p > 3, 'free/missing descendant')
        result.add(p)
        for r in admitted_support(orders[p]):
            require(r < p, 'non-descending edge')
            todo.append(r)
    return result


def maxima(R: set[int], orders: dict[int, int]) -> set[int]:
    # Numerical direction: larger row -> smaller odd order factor.
    used = set().union(*(admitted_support(orders[p]) for p in R))
    require(used <= R, 'R is not dependency-closed')
    return R - used


def terminal_orders(R: set[int], orders: dict[int, int]) -> list[int]:
    A = maxima(R, orders)
    optional = sorted(R - A)
    out = []
    for bits in range(1 << len(optional)):
        S = A | {p for i, p in enumerate(optional) if bits >> i & 1}
        for d in DELTA:
            out.append(d * math.prod(S))
    require(len(out) == len(set(out)), 'duplicate index')
    return sorted(out)


def validate_regular_state(R: set[int], orders: dict[int, int]) -> None:
    """Check a concrete good regular state, including the basal-gateway gate."""
    require(7 in R and orders.get(7) == 6, 'missing true basal 7')
    for p in R:
        require(p in orders, 'missing exact order')
        certify_prime_order(p, orders[p])
        S = admitted_support(orders[p])
        require(S <= R, 'state is not dependency-closed')
        require(p == 7 or bool(S), 'extra basal gateway is forbidden')
        require(7 in closure(p, orders), 'vertex does not reach 7')


def diamond_lucas_certificate() -> dict:
    """A compact second, full-(p-1) Lucas primality proof for the diamond."""
    p, a = 6717031, 3
    factors = (2, 3, 5, 41, 43, 127)
    require(math.prod(factors) == p - 1, 'incomplete p-1 factorization')
    require(all(prime_by_trial(l) for l in factors), 'nonprime p-1 factor')
    require(pow(a, p - 1, p) == 1, 'Lucas Fermat equality failed')
    residues = {str(l): pow(a, (p - 1) // l, p) for l in factors}
    require(all(math.gcd(z - 1, p) == 1 for z in residues.values()),
            'Lucas order drop condition failed')
    return {'p': p, 'base': a, 'complete_p_minus_1_factors': list(factors),
            'full_power_mod_p': 1, 'order_drop_residues': residues,
            'gcd_drop_minus_1_with_p': {l: math.gcd(z - 1, p) for l, z in residues.items()},
            'scope': 'independent arithmetic method, not independent author or software stack'}


def phi_value_squarefree(n: int) -> int:
    factors = factor_trial(n)
    require(all(v == 1 for v in factors.values()), 'squarefree index required')
    primes = list(factors)
    numerator = denominator = 1
    for bits in range(1 << len(primes)):
        d = math.prod(p for j, p in enumerate(primes) if bits >> j & 1)
        term = pow(5, d) - 1
        if (len(primes) - bits.bit_count()) % 2:
            denominator *= term
        else:
            numerator *= term
    q, r = divmod(numerator, denominator)
    require(r == 0, 'nonintegral cyclotomic value')
    return q


def phi_at_base_via_divisor_recursion(n: int, base: int) -> int:
    """A separate organization for compact critical-integer identities."""
    require(n >= 1 and base >= 2, 'invalid cyclotomic inputs')
    divisors = sorted(d for d in range(1, n + 1) if n % d == 0)
    values: dict[int, int] = {}
    for d in divisors:
        denominator = math.prod(v for e, v in values.items() if d % e == 0)
        values[d], remainder = divmod(pow(base, d) - 1, denominator)
        require(remainder == 0, 'nonintegral divisor-recursion cyclotomic value')
    return values[n]


def critical_integer_checks() -> list[dict]:
    records = []
    for R in ({7}, {7, 43}, {7, 43, 127}):
        A = maxima(R, ACTUAL_ORDERS)
        a = math.prod(A)
        b = 6 * math.prod(R - A)
        require(math.gcd(a, b) == 1, 'mandatory and optional products not coprime')
        compact = phi_at_base_via_divisor_recursion(a, pow(5, b))
        expanded = math.prod(phi_value_squarefree(n) for n in terminal_orders(R, ACTUAL_ORDERS))
        require(compact == expanded, 'critical-integer product identity mismatch')
        cleanup = max(R) if len(A) == 1 else 1
        primitive, remainder = divmod(compact, cleanup)
        require(remainder == 0, 'missing predicted imprimitive factor')
        small_primes = [p for p in range(2, max(R) + 1) if prime_by_trial(p)]
        require(all(primitive % p for p in small_primes), 'imprimitive cleanup incomplete')
        encoded = primitive.to_bytes((primitive.bit_length() + 7) // 8, 'big')
        checks = {}
        for p in (42743, 6717031):
            if closure(p, ACTUAL_ORDERS) - {p} == R:
                require(primitive % p == 0 and primitive % (p*p) != 0,
                        'regular fixture has wrong primitive-integer valuation')
                checks[str(p)] = 1
        records.append({'regular_state': sorted(R), 'maximal_generators': sorted(A),
                        'a': a, 'b': b, 'imprimitive_factor_removed': cleanup,
                        'number_of_expanded_indices': len(terminal_orders(R, ACTUAL_ORDERS)),
                        'identity': 'Phi_a(5^b) = product_{n in J(R)} Phi_n(5)',
                        'primitive_integer_bit_length': primitive.bit_length(),
                        'primitive_integer_sha256_big_endian_unsigned': hashlib.sha256(encoded).hexdigest(),
                        'small_prime_cleanup_checks': len(small_primes),
                        'selected_actual_prime_valuations': checks,
                        'complete_factorization_claimed': False})
    return records


def verify_dag_domains(max_vertices: int = 7) -> list[dict]:
    """Compare reachability testing with maximal-antichain containment.

    Vertex 0 represents 7; vertices are sorted by their numerical labels.
    These are ABSTRACT support DAGs, not claimed arithmetic prime DAGs.
    """
    rows = []
    for m in range(2, max_vertices + 1):
        k = m - 1  # number of proper regular vertices
        regular_dags = 0
        comparisons = accepted = by_formula = 0
        width_histogram: dict[int, int] = {}
        choices = [range(1, 1 << i) for i in range(1, k)]
        for picks in itertools.product(*choices):
            supports = [0, *picks]
            regular_dags += 1
            all_bits = (1 << k) - 1
            used = 0
            desc = []
            for i, support in enumerate(supports):
                used |= support
                mask = 1 << i
                for j in range(i):
                    if support >> j & 1:
                        mask |= desc[j]
                desc.append(mask)
            A = all_bits & ~used
            width_histogram[A.bit_count()] = width_histogram.get(A.bit_count(), 0) + 1
            by_formula += 1 << (k - A.bit_count())
            for S in range(1, 1 << k):
                reached = 0
                for i in range(k):
                    if S >> i & 1:
                        reached |= desc[i]
                independent = reached == all_bits
                theorem = S & A == A
                require(independent == theorem, 'maximal-antichain theorem mismatch')
                accepted += independent
                comparisons += 1
        require(accepted == by_formula, 'terminal count formula mismatch')
        rows.append({
            'vertices_including_formal_root': m, 'regular_support_dags': regular_dags,
            'root_support_comparisons': comparisons, 'accepted_full_basin_support_dags': accepted,
            'accepted_by_formula': by_formula,
            'regular_state_maximal_width_histogram': dict(sorted(width_histogram.items())),
            'classification': 'ABSTRACT SORTED SUPPORT DAGS; arithmetic labels not instantiated',
        })
    return rows


def regular_fork_mask() -> dict:
    """Full-period exact mask check for the ACTUAL regular forest {7,43,127}."""
    R = [7, 43, 127]
    P = math.prod(R)
    L = 6 * P
    a = P * ((4 * pow(P, -1, 6)) % 6)
    residues = {p: (3 + pow(5, a, p * p)) % (p * p) for p in R}
    U = math.lcm(*(ACTUAL_ORDERS[p] for p in R))
    holes = []
    comparisons = covered = 0
    for d in range(4, L, 6):
        coverage = False
        for p in R:
            value = (residues[p] - 3 - pow(5, d, p * p)) % (p * p)
            direct = value != 0 and value % p == 0
            formula = (d - a) % ACTUAL_ORDERS[p] == 0 and (d - a) % p != 0
            require(direct == formula, 'direct mask / shell mismatch')
            coverage |= direct
            comparisons += 1
        if coverage:
            covered += 1
        else:
            holes.append(d)
    require(holes == [a], 'regular forest does not have exactly the stated hole')
    return {
        'classification': 'ACTUAL REGULAR PARTIAL SYSTEM, NOT A COMPLETE CERTIFICATE',
        'rows': R, 'anchor': 1, 'K': 2, 'E': [1], 'a': a,
        'residues_mod_prime_squared': {str(p): residues[p] for p in R},
        'coarse_U_without_a_nonregular_root': U,
        'full_period_L': L, 'branch': 'd = 4 mod 6',
        'branch_exponents': P, 'covered_branch_exponents': covered,
        'holes': holes, 'direct_row_comparisons': comparisons,
        'warning': 'U != L for this partial system; a hypothetical root was NOT added',
    }


def negative_regressions() -> list[str]:
    passed = []
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            passed.append(name)
        else:
            raise ValueError('invalid fixture accepted: ' + name)
    reject('42743 does not have compressed order 86', lambda: certify_prime_order(42743, 86))
    reject('6717031 does not have order 43', lambda: certify_prime_order(6717031, 43))
    reject('6717031 does not have order 127', lambda: certify_prime_order(6717031, 127))
    reject('composite label rejected', lambda: certify_prime_order(43 * 127, 42))
    reject('imprimitive 7 cannot have order 42', lambda: certify_prime_order(7, 42))
    reject('nonclosed basin rejected', lambda: maxima({7, 127, 6717031}, ACTUAL_ORDERS))
    require(pow(5, 5461, 6717031 ** 2) != 1, 'regular diamond cannot be labelled B7')
    passed.append('actual regular diamond explicitly fails B7 nonregularity')
    require(5461 // 43 not in I_MULTIPLIERS and 5461 // 127 not in I_MULTIPLIERS,
            'bounded multiplier counterexample failed')
    passed.append('both possible diamond spine multipliers lie outside the proposed eight')
    R = {7, 43, 127}
    require(maxima(R, ACTUAL_ORDERS) == {43, 127}, 'wrong fork maxima')
    require(43 not in terminal_orders(R, ACTUAL_ORDERS), 'omitted mandatory maximum accepted')
    passed.append('omitting a mandatory fork maximum rejected')
    require(len(closure(43, ACTUAL_ORDERS) | closure(127, ACTUAL_ORDERS)) == 3,
            'shared relay counted twice')
    passed.append('shared 7 counted once by closure union')
    require(1 + sum(len(closure(p, ACTUAL_ORDERS)) for p in (43, 127)) == 5,
            'negative additive-cost control broken')
    passed.append('naive additive size is 5 but exact terminal basin cost is 4')
    reject('actual regular 31 rejected as an extra basal gateway',
           lambda: validate_regular_state({7, 31}, {7: 6, 31: 3}))
    reject('squarefree-order violation rejected', lambda: certify_prime_order(43, 49))
    reject('unadmitted prime factor cannot serve as an admitted relay',
           lambda: closure(11, {11: 5}))
    for R0 in ({7}, {7, 43, 127}, {7, 43, 42743}, {7, 43, 127, 6717031}):
        validate_regular_state(R0, ACTUAL_ORDERS)
    return passed


def run(outdir: Path, max_vertices: int) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    records = [certify_prime_order(p, w) for p, w in sorted(ACTUAL_ORDERS.items())]
    # First-relay identities: exact, complete products, imported gate independently replayed.
    first_products = {7: [(19531, 1)], 14: [(29, 1), (449, 1)],
                      21: [(379, 1), (519499, 1)],
                      42: [(7, 1), (43, 1), (127, 1), (7603, 1)]}
    for n, fs in first_products.items():
        require(all(prime_by_trial(p) for p, _ in fs), 'first-relay product composite factor')
        require(phi_value_squarefree(n) == math.prod(p ** e for p, e in fs),
                'first-relay product mismatch')
    C3 = sorted(r * m for r in A7 for m in I_MULTIPLIERS)
    fork_records = []
    for r, s in itertools.combinations(A7, 2):
        indices = sorted(m * r * s for m in I_MULTIPLIERS)
        require(indices == terminal_orders({7, r, s}, ACTUAL_ORDERS), 'fork formula mismatch')
        fork_records.append({'r': r, 's': s, 'indices': indices})
    C4fork = sorted(n for record in fork_records for n in record['indices'])
    require(len(set(C3)) == 48 and len(set(C4fork)) == 120, 'wrong family size')
    require(not set(C3) & set(C4fork), 'different closure costs collided')
    serial_examples = []
    for s in (9547, 42743, 18471511, 558801427, 7866608083):
        R = {7, 43, s}
        require(closure(s, ACTUAL_ORDERS) == R, 'wrong serial closure')
        indices = terminal_orders(R, ACTUAL_ORDERS)
        require(len(indices) == 16, 'wrong serial index count')
        serial_examples.append({'first_relay': 43, 'second_regular_relay': s,
                                'second_relay_order': ACTUAL_ORDERS[s], 'terminal_indices': indices,
                                'classification': 'EXPLICIT REGULAR-STATE INSTANCE; square hits not decided'})
    require(closure(6717031, ACTUAL_ORDERS) == {7, 43, 127, 6717031}, 'wrong diamond closure')
    diamond_phi = phi_value_squarefree(5461)
    require(diamond_phi % 6717031 == 0 and diamond_phi % (6717031 ** 2) != 0,
            'cyclotomic diamond factor check failed')
    triangle_phi = phi_value_squarefree(602)
    require(triangle_phi % 42743 == 0 and triangle_phi % (42743 ** 2) != 0,
            'cyclotomic shortcut fixture failed')
    require(phi_value_squarefree(86) % 42743 != 0, 'invalid same-prime square transfer')
    result = {
        'status': 'PASS',
        'scope': 'finite exact reference only; no global B7 exclusion',
        'first_relay_complete_products_replayed': 4,
        'actual_regular_prime_records': records,
        'diamond_full_p_minus_1_Lucas_certificate': diamond_lucas_certificate(),
        'C3_indices': C3,
        'C4_fork_pair_records': fork_records,
        'C4_fork_indices': C4fork,
        'C4_fork_count': len(C4fork),
        'C4_serial_schema': 'for r in A7; s regular admitted primitive divisor of Phi_(m*r)(5), m in {1,2,3,6,7,14,21,42}; terminal n = delta*7^e*r^f*s, delta|6, e,f in {0,1}',
        'C4_serial_complete_factor_sets_materialized': False,
        'C4_serial_actual_examples': serial_examples,
        'C5_diamond_regular_state_terminal_indices': terminal_orders({7, 43, 127, 6717031}, ACTUAL_ORDERS),
        'critical_integer_identity_checks': critical_integer_checks(),
        'abstract_dag_enumeration': verify_dag_domains(max_vertices),
        'actual_regular_fork_mask': regular_fork_mask(),
        'negative_regressions': negative_regressions(),
        'B7_member_found': False,
        'B7_empty_proved': False,
        'global_finite_critical_family_proved': False,
        'all_GitHub_writes': [],
    }
    (outdir / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (outdir / 'C4_FORK_120.json').write_text(json.dumps(fork_records, indent=2) + '\n')
    (outdir / 'C4_FORK_120.txt').write_text('\n'.join(map(str, C4fork)) + '\n')
    (outdir / 'ACTUAL_REGULAR_CERTIFICATES.json').write_text(json.dumps(records, indent=2) + '\n')
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--max-dag-vertices', type=int, default=7, choices=range(2, 8))
    args = parser.parse_args()
    result = run(args.output_dir, args.max_dag_vertices)
    print(json.dumps({
        'status': result['status'], 'certified_actual_regular_primes': len(result['actual_regular_prime_records']),
        'C4_fork_count': result['C4_fork_count'],
        'critical_integer_identity_checks': len(result['critical_integer_identity_checks']),
        'DAG_support_comparisons': sum(r['root_support_comparisons'] for r in result['abstract_dag_enumeration']),
        'DAG_accepted_counts': [r['accepted_full_basin_support_dags'] for r in result['abstract_dag_enumeration']],
        'mask_comparisons': result['actual_regular_fork_mask']['direct_row_comparisons'],
        'negative_regressions': len(result['negative_regressions']),
        'nonclaims': 'no B7 member; no B7 emptiness; no global finite family',
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
