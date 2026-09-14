#!/usr/bin/env python3
"""Reproduce only bounded I4 checks; never runs or enlarges the 10^7 scan.

Default: python reference.py
Optional full input-integrity check:
    python reference.py --source-zip /path/to/A303656_DIRECT_ADDITIVE_RESET_PHASE_I.zip

Needs mpmath. The optional NPZ byte-hash audit additionally needs numpy.
Factorizations used for the supplied panel are independently trial-verified.
Numeric inequalities are also checked with mpmath's interval arithmetic;
these finite checks are not a proof of the unproved uniform lemma.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
import mpmath as mp

EXPECTED = '3befe3e5f1cc92e757da748d80ffbeefaf1ac5b9bf6641eecb783fc7e3b0d293'
mp.mp.dps = 70
mp.iv.dps = 60


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def factor(n: int) -> list[list[int]]:
    if n < 1: raise ValueError('factor expects a positive integer')
    out: list[list[int]] = []
    p = 2
    while p*p <= n:
        v = 0
        while n % p == 0:
            n //= p; v += 1
        if v: out.append([p, v])
        p = 3 if p == 2 else p + 2
    if n > 1: out.append([n, 1])
    return out


def valuation(n: int, p: int) -> int:
    if n == 0: return 10**9  # zero residue is rejected at finite truncations
    v = 0
    while n % p == 0:
        v += 1; n //= p
    return v


def local23(m: int) -> bool:
    if m <= 0: return False
    return (m // 2**valuation(m, 2)) % 4 == 1 and valuation(m, 3) % 2 == 0


def norm(f: list[list[int]]) -> bool:
    return not any(p % 4 == 3 and v % 2 for p, v in f)


def powers(base: int, limit: int) -> list[int]:
    out = []; x = 1
    while x <= limit:
        out.append(x); x *= base
    return out


def order(base: int, q: int) -> int:
    if q == 1: return 1
    if math.gcd(base, q) != 1: raise ValueError('non-unit in order')
    x = 1
    for k in range(1, q + 1):
        x = x * base % q
        if x == 1: return k
    raise AssertionError('order not found')


def divisors(f: list[list[int]]) -> list[int]:
    out = [1]
    for p, v in f:
        if p != 2:
            out = [d*p**j for d in out for j in range(v + 1)]
    return out


def chi(h: int) -> int:
    return 0 if h % 2 == 0 else (1 if h % 4 == 1 else -1)


def dmass(f: list[list[int]], s, interval: bool = False):
    ctx = mp.iv if interval else mp.mp
    z = ctx.mpf(1)
    for p, v in f:
        if p == 2: continue
        x = ctx.exp(-s*ctx.log(p)) * (1 if p % 4 == 1 else -1)
        z *= sum(x**j for j in range(v + 1))
    return z


def centered(f: list[list[int]], s):
    """Independent positive-local-factor evaluation of F_u(s)."""
    z = mp.mpf(1)
    for p, v in f:
        if p == 2: continue
        x = s*mp.log(p)
        if p % 4 == 1:
            t = sum(mp.exp((mp.mpf(v)/2-j)*x) for j in range(v+1))
        elif v % 2 == 0:
            t = mp.cosh((v+1)*x/2)/mp.cosh(x/2)
        else:
            t = mp.sinh((v+1)*x/2)/mp.cosh(x/2)
        z *= t
    return z


def interval_record(x) -> dict[str, str]:
    # Endpoints of an interval, serialized at greater precision than iv.dps.
    return {'lower': mp.nstr(mp.mpf(x._mpi_[0]), 65),
            'upper': mp.nstr(mp.mpf(x._mpi_[1]), 65)}


def orbit_density(n: int, q: int, k: int = 4, ell: int = 3) -> dict:
    m2, m3 = 2**(k+1), 3**ell
    tc = math.lcm(order(3, m2), order(3, q))
    td = math.lcm(order(5, m2), order(5, m3), order(5, q))
    c2 = [pow(3, a, m2) for a in range(tc)]
    cq = [pow(3, a, q) for a in range(tc)]
    d2 = [pow(5, b, m2) for b in range(td)]
    d3 = [pow(5, b, m3) for b in range(td)]
    dq = [pow(5, b, q) for b in range(td)]
    hits = 0
    for a in range(tc):
        for b in range(td):
            r2 = (n-c2[a]-d2[b]) % m2
            v2 = valuation(r2, 2)
            if v2 >= k or (r2//2**v2) % 4 != 1: continue
            # c is a tail exponent >=ell: its residue mod 3^ell is zero.
            r3 = (n-d3[b]) % m3
            v3 = valuation(r3, 3)
            if v3 >= ell or v3 % 2: continue
            if (n-cq[a]-dq[b]) % q == 0: hits += 1
    return {'q': q, 'k': k, 'ell': ell, 'tc': tc, 'td': td,
            'hits': hits, 'rho': str(Fraction(hits, tc*td))}


def audit_source(path: Path) -> dict:
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    with ZipFile(io.BytesIO(raw)) as z:
        verified = []
        for line in z.read('SHA256SUMS.txt').decode().splitlines():
            if not line.strip(): continue
            digest, name = line.split(None, 1)
            name = name.lstrip('*')
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
            verified.append(name)
        src = json.loads(z.read('results.json'))
        rows = 0; primes = set()
        for item in src['extremal_panel']:
            for r in item['all_pair_rows']:
                m = r['residual']; f = r['factors']
                assert m == item['n']-3**r['c']-5**r['d']
                if m > 0:
                    assert math.prod(p**v for p,v in f) == m
                    assert norm(f) == r['success']
                else: assert m == 0 and r['success']
                primes.update(p for p,v in f); rows += 1
        assert all(is_prime(p) for p in primes)
        import numpy as np
        arrays = np.load(io.BytesIO(z.read('per_n_metrics.npz')), allow_pickle=False)
        for name, meta in src['per_n_arrays'].items():
            arr = arrays[name]
            assert list(arr.shape) == meta['shape'] and str(arr.dtype) == meta['dtype']
            assert hashlib.sha256(arr.tobytes(order='C')).hexdigest() == meta['little_endian_data_sha256']
    return {'outer_sha256': EXPECTED, 'manifest_files_verified': verified,
            'all_panel_rows_verified': rows, 'distinct_panel_primes_trial_verified': len(primes),
            'npz_array_byte_hashes_verified': len(src['per_n_arrays']),
            'new_global_scan_performed': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-zip', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    inp = json.loads((root/'reference_input.json').read_text())
    panel = []; checked = 0; quarter_cases = 0
    E1 = (mp.cosh(1)-4*mp.cosh(mp.mpf('0.5'))+3)/3
    for item in inp['targets']:
        n = item['n']; rows = item['rows']
        p3, p5 = powers(3, n//4), powers(5, n//4)
        expected_pairs = {(c,d) for c,x in enumerate(p3) for d,y in enumerate(p5) if local23(n-x-y)}
        assert expected_pairs == {(r['c'], r['d']) for r in rows}
        if not rows: continue
        s = 1/mp.log(n); si = 1/mp.iv.log(n)
        D1 = D2 = Z0 = H1 = H2 = mp.mpf(0)
        I1 = I2 = mp.iv.mpf(0)
        D0 = 0
        for r in rows:
            m, f = r['residual'], r['factors']
            assert m == n-3**r['c']-5**r['d'] and 2*m >= n and m < n
            assert local23(m) and math.prod(p**v for p,v in f) == m
            assert all(v >= 1 and is_prime(p) for p,v in f)
            assert norm(f) == r['success']
            u = m//2**valuation(m, 2)
            tau = math.prod(v+1 for p,v in f if p != 2)
            z0 = sum(chi(h) for h in divisors(f))
            D0 += z0; Z0 += mp.mpf(z0)/tau
            a, b = dmass(f,s), dmass(f,2*s)
            fa, fb = centered(f,s), centered(f,2*s)
            assert abs(fa-u**(s/2)*a) <= mp.mpf('1e-60')*max(1,fa)
            assert abs(fa-sum(chi(h)*mp.exp(s*mp.log(mp.sqrt(u)/h)) for h in divisors(f))) <= mp.mpf('1e-60')*max(1,fa)
            w = (4*fa-fb)/(3*tau)
            err = mp.mpf(z0)/tau-w
            assert -mp.mpf('1e-60') <= err <= E1+mp.mpf('1e-60')
            if not r['success']:
                assert fb >= 4*fa-mp.mpf('1e-60')
                bad = [(p,v) for p,v in f if p%4 == 3 and v%2]
                if all(p**4 > n for p,v in bad):
                    assert len(bad) == 2 and all(v == 1 for p,v in bad)
                    quotient = m//(bad[0][0]*bad[1][0])
                    assert norm(factor(quotient)) and quotient**2 < n
                    quarter_cases += 1
            else:
                assert w > 0
            D1 += a; D2 += b; H1 += fa/tau; H2 += fb/tau
            I1 += dmass(f,si,True); I2 += dmass(f,2*si,True)
            checked += 1
        ratio_iv = I2/I1
        assert ratio_iv < 2
        panel.append({'n': n, 'n_mod24': n%24, 'bulk_active': item['bulk_active'],
                      'bulk_local23': len(rows), 'bulk_successes': sum(r['success'] for r in rows),
                      'D0': D0, 'D1': str(D1), 'D2': str(D2),
                      'divisor_mass_ratio': str(D2/D1), 'divisor_mass_ratio_interval': interval_record(ratio_iv),
                      'gap_2D1_minus_D2': str(2*D1-D2),
                      'normalized_F_doubling_ratio': str(H2/H1),
                      'quartic_minorant_sum': str((4*H1-H2)/3), 'normalized_exact_norm_mass': str(Z0)})
    # Exact local Taylor-moment checks; no floating point in coefficient signs.
    moments = 0
    for v in range(25):
        for degree in range(25):
            good = sum((v-2*j)**degree for j in range(v+1))
            bad = sum((-1)**j*(v-2*j)**degree for j in range(v+1))
            assert good >= 0 and bad >= 0
            if degree % 2: assert good == 0
            if degree % 2 != v % 2: assert bad == 0
            moments += 1
    # Exact corrected-period nonmultiplicativity.
    period_tests = []
    for n in [2,358990,410258,530230,9481394]:
        tab = [orbit_density(n,q) for q in [1,7,19,133,49]]
        rho1 = Fraction(tab[0]['rho']); assert rho1 > 0
        for x in tab: x['Gamma'] = str(Fraction(x['rho'])/rho1)
        period_tests.append({'n_signature': n, 'table': tab})
    t = period_tests[1]['table']
    assert [x['Gamma'] for x in t[:4]] == ['1','11/63','8/189','0']
    # Strictness: one norm is not sufficient for ML-D2 on an arbitrary bulk multiset.
    N = 1002; fs = [factor(576)] + [factor(1001)]*40
    assert all(local23(m) for m in [576,1001])
    si = 1/mp.iv.log(N)
    strict_ratio = sum(dmass(f,2*si,True) for f in fs)/sum(dmass(f,si,True) for f in fs)
    assert strict_ratio > 2
    # One fixed base-(2,2) target from Platt--Trudgian, not a new scan.
    N2 = 535903; ps = powers(2,N2//4)
    fs2 = [factor(N2-x-y) for x in ps for y in ps if local23(N2-x-y)]
    assert fs2 and not any(norm(f) for f in fs2)
    si = 1/mp.iv.log(N2)
    base2_ratio = sum(dmass(f,2*si,True) for f in fs2)/sum(dmass(f,si,True) for f in fs2)
    assert base2_ratio > 4/mp.iv.sqrt(mp.iv.e)
    # Diagonal correction in the hyperbola identity.
    diagonal = sum(chi(h) for h in divisors([[3,2]]))
    assert diagonal == 1 and 2*chi(1)+chi(3) == 1
    audit = audit_source(args.source_zip) if args.source_zip else {'full_source_audit_requested': False}
    out = {'scope': 'bounded theorem checks only; no new global scan', 'precision_decimal_digits': mp.mp.dps,
           'interval_precision_decimal_digits': mp.iv.dps, 'input_targets': len(inp['targets']),
           'nonempty_bulk_targets': len(panel), 'filtered_factorized_rows_checked': checked,
           'local_Taylor_moment_tests_exact': moments, 'quarter_cutoff_failure_rows_checked': quarter_cases,
           'E1': str(E1), 'all_failure_dmass_threshold': str(4/mp.sqrt(mp.e)),
           'panel': panel, 'period_tests': period_tests,
           'strictness_test': {'N':N,'multiset':'one 576 and forty 1001','norm_count':1,'ratio_interval':interval_record(strict_ratio)},
           'base2_test': {'n':N2,'bulk_pairs':len(ps)**2,'bulk_local23':len(fs2),'norm_count':0,'ratio_interval':interval_record(base2_ratio),
                          'does_not_assert_I2_density_for_base2':True},
           'hyperbola_diagonal_u9':'PASS: 2*chi(1)+chi(3)=1, not 3', 'source_audit':audit,
           'uniform_ML_D2_proved':False}
    dest = args.out or root/'benchmark_results.json'
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(dest),'panel_targets':len(panel),'rows':checked,
                      'maximum_panel_ratio_n':max(panel,key=lambda r:mp.mpf(r['divisor_mass_ratio']))['n'],
                      'quarter_cutoff_cases':quarter_cases,'all_checks':'PASS','uniform_lemma':'UNPROVED'},indent=2))

if __name__ == '__main__':
    main()
