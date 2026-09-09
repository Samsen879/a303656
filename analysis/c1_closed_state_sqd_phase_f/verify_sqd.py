#!/usr/bin/env python3
"""Exact reference laboratory for A303656 SQD (Python standard library only).

Scope: Phase-D basal B7; Phase-E source bundle was unavailable.
All mathematical claims are in REPORT.md. This is a bounded arithmetic replay,
not a proof of squarefreeness of unresolved large cofactors.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import pathlib
import time
from functools import lru_cache


def build_spf(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for p in range(2, math.isqrt(limit) + 1):
        if spf[p] == p:
            for x in range(p * p, limit + 1, p):
                if spf[x] == x:
                    spf[x] = p
    return spf


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound', type=int, default=1_000_000,
                    help='inclusive vertex and primitive-prime search bound')
    ap.add_argument('--numeric-exponent-cap', type=int, default=1_000_000)
    ap.add_argument('--out', type=pathlib.Path, default=pathlib.Path('results'))
    args = ap.parse_args()
    if args.bound < 519499:
        raise SystemExit('Use bound >= 519499 to include the six certified first relays.')
    if args.numeric_exponent_cap < 42:
        raise SystemExit('Numeric exponent cap must be at least 42.')
    args.out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    spf = build_spf(args.bound)
    primes = [p for p in range(2, args.bound + 1) if spf[p] == p]

    def fac(n: int) -> dict[int, int]:
        if not 1 <= n <= args.bound:
            raise ValueError(f'factorization argument out of certified sieve range: {n}')
        result: dict[int, int] = {}
        while n > 1:
            p = spf[n]
            result[p] = result.get(p, 0) + 1
            n //= p
        return result

    @lru_cache(None)
    def order(a: int, p: int) -> int:
        if p < 2 or p > args.bound or spf[p] != p or math.gcd(a, p) != 1:
            raise ValueError('Order requires a certified prime coprime to the base.')
        n = p - 1
        for r in fac(n):
            while n % r == 0 and pow(a, n // r, p) == 1:
                n //= r
        assert pow(a, n, p) == 1
        assert all(pow(a, n // r, p) != 1 for r in fac(n))
        return n

    @lru_cache(None)
    def regular_closure(a: int, p: int) -> frozenset[int] | None:
        if p <= 3 or p % 4 != 3 or a % p == 0:
            return None
        n = order(a, p)
        f = fac(n)
        if any(e != 1 for e in f.values()) or pow(a, n, p * p) == 1:
            return None
        odd = set(f) - {2}
        if odd == {3}:
            return frozenset({7}) if p == 7 else None
        if not odd or any(r % 4 == 1 for r in odd):
            return None
        result = {p}
        for r in odd - {3}:
            child = regular_closure(a, r)
            if child is None:
                return None
            result.update(child)
        return frozenset(result)

    def subsets(items):
        items = tuple(sorted(items))
        for k in range(len(items) + 1):
            yield from itertools.combinations(items, k)

    def closure_set(seed) -> frozenset[int]:
        result: set[int] = set()
        for p in seed:
            c = regular_closure(5, p)
            if c is None:
                raise ValueError('Seed contains a non-good regular vertex.')
            result.update(c)
        return frozenset(result)

    good_vertices = [p for p in primes if p > 3 and p % 4 == 3
                     and regular_closure(5, p) is not None]
    useful = [p for p in good_vertices if len(regular_closure(5, p)) <= 4]
    states: list[frozenset[int]] = []
    for k in range(1, 5):
        for seed in itertools.combinations(useful, k):
            if closure_set(seed) == frozenset(seed):
                states.append(frozenset(seed))
    states.sort(key=lambda r: (len(r), tuple(sorted(r))))
    state_set = set(states)
    indices: dict[frozenset[int], set[int]] = {}
    generators: dict[frozenset[int], set[int]] = {}
    owner: dict[int, frozenset[int]] = {}
    rows = {}
    for R in states:
        A = {p for p in R if not any(p in regular_closure(5, v) - {v} for v in R)}
        assert closure_set(A) == R
        J: set[int] = set()
        for extra in subsets(R - A):
            S = set(extra) | A
            assert closure_set(S) == R
            for delta in (1, 2, 3, 6):
                n = delta * math.prod(S)
                assert n not in owner
                owner[n] = R
                J.add(n)
        assert len(J) == 4 * 2 ** (len(R) - len(A))
        # Converse generating-set characterization, not only the forward direction.
        for S in subsets(R):
            assert (closure_set(S) == R) == A.issubset(S)
        proper = [T for T in states if T < R]
        for v in R:
            closed_after_deletion = bool(R - {v}) and closure_set(R - {v}) == R - {v}
            assert closed_after_deletion == (v in A and len(R) > 1)
        indices[R] = J
        generators[R] = A
        rows[R] = {
            'R': sorted(R), 'A': sorted(A), 'J': sorted(J),
            'complexity': len(R),
            'W_symbolic': {'cyclotomic_index': math.prod(A),
                           'base': 5, 'substitution_exponent': 6 * math.prod(R - A)},
            'normalizer': next(iter(A)) if len(A) == 1 else 1,
            'all_proper_good_substates': [sorted(T) for T in proper],
            'primitive_factorization_through_bound': [],
            'primitive_square_hits_through_bound': [],
            'full_factorization_status': 'NOT_COMPLETED; no squarefree conclusion',
        }

    nonregular_admitted = []
    for q in primes:
        if q <= 3 or q == 5:
            continue
        n = order(5, q)
        sq = pow(5, n, q * q) == 1
        if q % 4 == 3 and sq:
            reasons = []
            f = fac(n)
            if any(e != 1 for e in f.values()):
                reasons.append('nonsquarefree order')
            for p in sorted(set(f) - {2, 3}):
                if regular_closure(5, p) is None:
                    reasons.append(f'bad proper descendant {p}')
            nonregular_admitted.append({'q': q, 'order': n, 'order_factorization': f,
                                        'B7_rejection_reasons': reasons})
        if n not in owner:
            continue
        R = owner[n]
        assert q > max(R) and q not in R
        v = 1
        modulus = q * q
        while pow(5, n, modulus) == 1:
            v += 1
            modulus *= q
        rows[R]['primitive_factorization_through_bound'].append(
            {'prime': q, 'exponent': v, 'unique_index': n, 'admitted': q % 4 == 3})
        if v >= 2 and q % 4 == 3:
            rows[R]['primitive_square_hits_through_bound'].append(q)

    def numeric_W(R: frozenset[int]) -> int:
        A = generators[R]
        b = 6 * math.prod(R - A)
        numerator = denominator = 1
        for S in subsets(A):
            value = pow(5, b * math.prod(S)) - 1
            if (len(A) - len(S)) % 2 == 0:
                numerator *= value
            else:
                denominator *= value
        value, remainder = divmod(numerator, denominator)
        assert remainder == 0
        return value

    numeric_R = [R for R in states if 6 * math.prod(R) <= args.numeric_exponent_cap]
    W = {R: numeric_W(R) for R in numeric_R}
    Z = {}
    for R in numeric_R:
        Z[R], rem = divmod(W[R], rows[R]['normalizer'])
        assert rem == 0
        N = Z[R]
        for f in rows[R]['primitive_factorization_through_bound']:
            p, e = f['prime'], f['exponent']
            N, rem = divmod(N, p ** e)
            assert rem == 0 and N % p != 0
        def fingerprint(v: int) -> dict:
            return {'bit_length': v.bit_length(),
                    'sha256_big_endian_unsigned': hashlib.sha256(
                        v.to_bytes((v.bit_length() + 7) // 8, 'big')).hexdigest()}
        rows[R]['Z_numeric'] = fingerprint(Z[R])
        rows[R]['unresolved_cofactor'] = fingerprint(N)
        if N == 1:
            rows[R]['full_factorization_status'] = 'COMPLETE; all primes certified by sieve'
        else:
            rows[R]['full_factorization_status'] = 'PARTIAL; unresolved cofactor not tested squarefree'
    pairs = 0
    for R, T in itertools.combinations(numeric_R, 2):
        assert math.gcd(Z[R], Z[T]) == 1
        pairs += 1
    raw_deletions = 0
    for R in numeric_R:
        for T in numeric_R:
            if not T < R:
                continue
            expect = 1
            if len(generators[R]) == 1:
                p = next(iter(generators[R]))
                if T == R - {p}:
                    expect = p
            assert math.gcd(W[R], W[T]) == expect
            assert math.gcd(Z[R], Z[T]) == 1
            raw_deletions += 1
        sub = [T for T in states if T <= R]
        lhs, rem = divmod(pow(5, 6 * math.prod(R)) - 1,
                          (pow(5, 6) - 1) * math.prod(R))
        assert rem == 0
        rhs = math.prod(Z[T] for T in sub)
        assert lhs == rhs

    # Genuine arithmetic, but base 3589 rather than base 5.
    toy_base, toy_q = 3589, 863
    toy_n = order(toy_base, toy_q)
    assert toy_n == 862 and pow(toy_base, toy_n, toy_q ** 2) == 1
    toy_R = set()
    for p in set(fac(toy_n)) - {2, 3}:
        c = regular_closure(toy_base, p)
        assert c is not None
        toy_R.update(c)
    assert toy_R == {7, 43, 431}
    toy = {'label': 'ACTUAL ARITHMETIC AT DIFFERENT BASE; NOT A BASE-5 COUNTEREXAMPLE',
           'base': toy_base, 'q': toy_q, 'order': toy_n,
           'q_square_modular_residue': pow(toy_base, toy_n, toy_q ** 2),
           'R': sorted(toy_R),
           'order_drop_checks': {str(r): pow(toy_base, toy_n // r, toy_q)
                                 for r in fac(toy_n)},
           'regular_vertices': [{'p': p, 'order': order(toy_base, p),
                                 'mod_p_squared': pow(toy_base, order(toy_base, p), p * p)}
                                for p in sorted(toy_R)],
           'proper_closed_substates': [[7], [7, 43]],
           'SQD_strong_same_root': 'IMPOSSIBLE by exact order, even above the two-vertex stop',
           'SQD_root_different_root': 'NOT DECIDED; proper-state squarefreeness not certified'}
    assert order(19, 7) == 6
    assert 19 * 19 - 19 + 1 == 7 ** 3
    # At the least squarefree composite index n=6, base 19 is the least
    # base >=2 with any admitted primitive q^2. Test all smaller bases exactly.
    for a in range(2, 19):
        v = a * a - a + 1
        for q in primes:
            if q * q > v:
                break
            assert not (q > 3 and q % 4 == 3 and v % (q * q) == 0)
    cyclotomic_toy = {'label': 'GENERAL CYCLOTOMIC COUNTEREXAMPLE, NOT B7',
                      'base': 19, 'n': 6, 'q': 7,
                      'values': {'1': 18, '2': 20, '3': 381, '6': 343},
                      'factorizations': {'1': {2: 1, 3: 2}, '2': {2: 2, 5: 1},
                                         '3': {3: 1, 127: 1}, '6': {7: 3}},
                      'minimality_scope': 'least base for n=6 and q>3, q=3 mod4; n=6 is the least squarefree composite index'}
    for n, f in cyclotomic_toy['factorizations'].items():
        assert all(spf[p] == p for p in f)
        assert math.prod(p ** e for p, e in f.items()) == cyclotomic_toy['values'][n]
    # Abstract marks on a real base-5 regular skeleton, NOT actual square divisors.
    abstract = {'label': 'ABSTRACT MARKED-INDEX MODEL; NO ACTUAL BASE-5 ROOT CLAIMED',
                'R': [7, 43, 127], 'A': [43, 127],
                'marked_index': 5461, 'all_other_indices_unmarked': True,
                'no_actual_q_assigned': True,
                'purpose': 'closure geometry and index localization alone cannot imply a different-root transfer'}
    assert abstract['marked_index'] in indices[frozenset(abstract['R'])]
    summary = {
        'definition_basis': 'Independent exact-closure reconstruction from pinned Phase-D basal B7; Phase E bundle unavailable',
        'vertex_bound_inclusive': args.bound, 'prime_search_bound_inclusive': args.bound,
        'good_regular_vertices': len(good_vertices),
        'good_regular_vertices_with_closure_size_at_most_four': len(useful),
        'state_counts_by_size': {str(k): sum(len(R) == k for R in states) for k in range(1, 5)},
        'states_total': len(states), 'distinct_indices': len(owner),
        'index_ownership_collisions': 0,
        'numeric_state_count': len(numeric_R), 'numeric_pairwise_coprimality_checks': pairs,
        'numeric_raw_deletion_gcd_checks': raw_deletions,
        'numeric_cumulative_partition_checks': len(numeric_R),
        'fully_factored_states': [sorted(R) for R in numeric_R
                                  if rows[R]['full_factorization_status'].startswith('COMPLETE')],
        'admitted_nonregular_primes_through_bound': nonregular_admitted,
        'base5_admitted_square_hits_on_enumerated_states_through_bound': sum(
            len(rows[R]['primitive_square_hits_through_bound']) for R in states),
        'important_boundary': 'Zero bounded hits is NOT a global no-hit or squarefree certificate.',
        'runtime_seconds': round(time.monotonic() - started, 4),
    }
    payloads = {'summary.json': summary, 'states.json': [rows[R] for R in states],
                'vertices.json': [{'p': p, 'order': order(5, p),
                                   'closure': sorted(regular_closure(5, p)),
                                   'mod_p_squared': pow(5, order(5, p), p * p)}
                                  for p in good_vertices],
                'toy_same_root.json': toy, 'toy_cyclotomic_critical.json': cyclotomic_toy,
                'abstract_marked_model.json': abstract}
    for name, payload in payloads.items():
        (args.out / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
