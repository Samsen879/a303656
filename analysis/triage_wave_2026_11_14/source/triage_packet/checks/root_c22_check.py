"""Independent C22 budget replay using the already audited H<512 catalogue.

This is a scratch audit calculation. It does not edit the frozen C21 package.
The full catalogue is rebuilt by executing our independent integer-GCD script.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import runpy

base = runpy.run_path(str(Path(__file__).with_name('root_c21_check.py')))
rows = base['catalog']
pair_checks = []
for e3, e5 in product(range(2), repeat=2):
    joint, c7, c11 = Counter(), Counter(), Counter()
    for a, b in product(range(15), repeat=2):
        alpha, beta = e3 + 2*a, e5 + 2*b
        x = (pow(3, alpha, 7) + pow(5, beta, 7)) % 7
        y = (pow(3, alpha, 11) + pow(5, beta, 11)) % 11
        joint[x, y] += 1
        c7[x] += 1
        c11[y] += 1
    for x, y in product(range(7), range(11)):
        assert joint[x, y]*225 == c7[x]*c11[y]
    worst = max(F(c7[x] + c11[y] - joint[x, y], 225)
                for x, y in product(range(7), range(11)))
    assert worst <= F(31, 75)
    pair_checks.append({'parities': [e3, e5], 'max_union': worst})

def top(k, subset):
    return sum(sorted([r['weight'] for r in subset] + [F(1, 512)]*k,
                      reverse=True)[:k], F(0))

def core(m):
    old = sum((r['weight'] for r in rows if 7 <= r['p'] <= m), F(0))
    return old - (F(1, 25) if m >= 11 else F(0))

K = 22
budgets = [{'M': 7, 't': 'base', 'bound': core(7) + top(K, [
    r for r in rows if r['p'] > 7 and r['M'] <= 7])}]
for m in (11, 13, 17, 19):
    active = [r for r in rows if r['p'] > m and r['M'] == m]
    inactive = [r for r in rows if r['p'] > m and r['M'] < m]
    for t in range(m, K+1):
        budgets.append({'M': m, 't': t,
                        'bound': core(m)+top(t, active)+top(K-t, inactive)})
assert len(budgets) == 33
for r in budgets:
    r['slack'] = 1-r['bound']
    assert r['slack'] > 0
tight = max(budgets, key=lambda r: r['bound'])
assert (tight['M'], tight['t'], tight['bound']) == (11, 11, F(4238011529, 4390848000))
out = {'target_budget': K, 'H_cutoff': 512, 'max_catalogue_order_prime': 19,
       'pair_checks': pair_checks, 'budgets': budgets, 'tight': tight,
       'scope': '22 arbitrary inert unit targets plus finite external regular norm conditions; independently refereed in the accompanying proof notes'}
path = Path(__file__).with_name('root_c22_results.json')
path.write_text(json.dumps(out, default=str, indent=2)+'\n')
print(json.dumps({'C22': {'pair_checks': pair_checks, 'budget_count': len(budgets),
                          'tight': tight}}, default=str, indent=2))
