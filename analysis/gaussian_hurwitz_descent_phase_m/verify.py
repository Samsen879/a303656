#!/usr/bin/env python3
"""Offline finite replay. Infinite statements stand on inspectable proof text.

No original-n scan or enlarged shell panel. All script outputs use /tmp copies.
Required: Python3.10+ standard library. Optional producer: already available NumPy.
"""
import argparse
import collections
import hashlib
import heapq
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def qmul(p, q):
    a, b, c, d = p
    w, x, y, z = q
    return (a*w-b*x-c*y-d*z, a*x+b*w+c*z-d*y,
            a*y-b*z+c*w+d*x, a*z+b*y-c*x+d*w)


def norm(q):
    return sum(x*x for x in q)


def operators(a, b):
    basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    cols = [qmul(qmul(a, e), b) for e in basis]
    return tuple(cols[j][i] for i in range(4) for j in range(4))


def apply(matrix, q):
    return tuple(sum(matrix[4*i+j]*q[j] for j in range(4)) for i in range(4))


def patterned(pattern):
    return {tuple(x*s for x, s in zip(p, signs))
            for p in set(itertools.permutations(pattern))
            for signs in itertools.product((-1, 1), repeat=4)}


def operator_replay(data):
    integral = patterned((4, 2, 0, 0))
    half = patterned((3, 3, 1, 1))
    all_a = integral | half
    require((len(integral), len(half), len(all_a)) == (48, 96, 144), 'norm5 classification count')
    require(all(norm(a) == 20 for a in all_a), 'doubled norm5')
    require(all_a == {tuple(a) for a in data['norm5_elements']}, 'source element list')
    pairs = collections.Counter(operators(a, b) for a in all_a for b in all_a)
    require(len(pairs) == 10368 and set(pairs.values()) == {2}, 'distinct operators / simultaneous sign')
    for m in pairs:
        transposed = tuple(m[4*j+i] for i in range(4) for j in range(4))
        require(transposed in pairs, 'inverse closure')
        for i in range(4):
            for j in range(4):
                require(sum(m[4*k+i]*m[4*k+j] for k in range(4)) == 400*int(i == j), 'norm preservation matrix')
        for k in range(4):
            changed = tuple(v*(-1 if (i == k) != (j == k) else 1)
                            for i in range(4) for j in range(4)
                            for v in [m[4*i+j]])
            require(changed in pairs, 'coordinate-sign normalization')
        for k in range(3):
            perm = list(range(4)); perm[k], perm[k+1] = perm[k+1], perm[k]
            require(tuple(m[4*perm[i]+perm[j]] for i in range(4) for j in range(4)) in pairs, 'coordinate-swap normalization')
    return len(pairs)


def matrix5(x):
    a, b, c, d = [(v*3) % 5 for v in x]
    return ((a+2*b) % 5, (-c-2*d) % 5, (c-2*d) % 5, (a-2*b) % 5)


def mm(a, b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) % 5
                 for i in range(2) for j in range(2))


def rank(q):
    return 2 if (q[0]*q[3]-q[1]*q[2]) % 5 else int(any(q))


def integrality_replay(data):
    reps = [tuple(x) for x in data['associate_representatives_doubled']]
    require(set(reps) == {(2, 4*s, 0, 0) for s in (-1, 1)} |
            {(2, 0, 4*s, 0) for s in (-1, 1)} |
            {(2, 0, 0, 4*s) for s in (-1, 1)}, 'six associate representatives')
    maps = [(matrix5(a), matrix5(b), operators(a, b)) for a in reps for b in reps]
    require(all(rank(matrix5(a)) == 1 for a in reps), 'rank-one associates')
    residues = set(); counts = collections.Counter()
    expected = {0: 36, 1: 11, 2: 6}
    for a, b, c, d in itertools.product(range(5), repeat=4):
        # Coordinates in the actual Hurwitz basis 1,i,j,(1+i+j+k)/2.
        x = (2*a+d, 2*b+d, 2*c+d, d)
        q = matrix5(x); residues.add(q); r = rank(q); counts[r] += 1
        good = 0
        for aa, bb, m in maps:
            criterion = not any(mm(mm(aa, q), bb))
            numerator = apply(m, x)
            legal = all(v % 20 == 0 for v in numerator)
            if legal:
                output = tuple(v//20 for v in numerator)
                legal = len({v % 2 for v in output}) == 1
            require(legal == criterion, 'AQB vs exact doubled-coordinate integrality')
            good += legal
        require(good == expected[r], 'legal rank-dependent class pairs')
    require(len(residues) == 625 and dict(counts) == {0: 1, 1: 144, 2: 480}, 'residue rank table')
    require({int(k): v for k, v in data['residue_ranks'].items()} == dict(counts), 'source rank counts')
    require({int(k): v for k, v in data['legal_class_pairs_by_rank'].items()} == expected, 'source class pair counts')
    return dict(counts)


def bad5(n):
    require(n > 0, 'positive pair/content required')
    while n % 5 == 0:
        n //= 5
    return n


def content(x):
    require(len({v % 2 for v in x}) == 1, 'Hurwitz input parity')
    return math.gcd((x[0]-x[3])//2, (x[1]-x[3])//2, (x[2]-x[3])//2, x[3])


def omega(n):
    total = 0; p = 2
    while p*p <= n:
        while n % p == 0:
            n //= p; total += 1
        p += 1
    return total + int(n > 1)


def heights(panel):
    bad = []; om = []
    for orbit in panel['unit_symmetry_orbits']:
        vals = []
        for i in orbit:
            x = panel['B4_shapes'][i]
            if x[0] % 2:
                continue
            vals.extend(bad5((x[j]*x[j]+x[k]*x[k])//4)
                        for j, k in itertools.combinations(range(4), 2) if x[j] or x[k])
        require(bool(vals), 'integral orbit member / positive pair')
        bad.append(min(vals)); om.append(min(map(omega, vals)))
    require(bad == panel['heights']['bad'] and om == panel['heights']['omega'], 'both symmetry-normalized heights')
    require([i for i, h in enumerate(bad) if h == 1] == panel['target_symmetry_orbits'], 'actual integral target set')
    return bad, om


def component(adj, start, allowed):
    seen = {start}; stack = [start]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen and allowed(v):
                seen.add(v); stack.append(v)
    return seen


def minimax(adj, h, targets):
    costs = [None]*len(h); heap = []
    for t in targets:
        costs[t] = h[t]; heapq.heappush(heap, (h[t], t))
    while heap:
        cost, u = heapq.heappop(heap)
        if costs[u] != cost:
            continue
        for v in adj[u]:
            candidate = max(cost, h[v])
            if costs[v] is None or candidate < costs[v]:
                costs[v] = candidate; heapq.heappush(heap, (candidate, v))
    return costs


def finite_certificates(data):
    panels = {p['M']: p for p in data['panels']}
    require(sorted(panels) == [4, 9, 16, 47, 64, 81, 1175], 'no finite panel extension')
    for p in panels.values():
        heights(p)
    p = panels[1175]; h = p['heights']['bad']; adj = p['symmetry_quotient_adjacency']
    q0 = (1, 3, 3, 34)
    require(norm(q0) == 1175 and content(tuple(2*v for v in q0)) == 1, 'primitive1175')
    require([2, 6, 6, 68] in [p['B4_shapes'][i] for i in p['unit_symmetry_orbits'][8]], '1175 source normalization')
    require(h[8] == h[9] == 2 and component(adj, 8, lambda i: h[i] < 13) == {8, 9}, 'COMPLETE strict sublevel13 cut')
    require(not set(p['target_symmetry_orbits']) & {8, 9}, 'sublevel component target-free')
    require(minimax(adj, h, p['target_symmetry_orbits'])[8] == 13, 'graph-derived minimax lower/upper')
    q1 = (-11, 15, 10, 27)
    triples = [(q0, (-2, 0, 0, -1), (-2, 0, 1, 0), q1),
               ((10, 11, 15, 27), (-2, 0, 1, 0), (-2, 0, 0, -1), (1, 2, 9, 33))]
    for q, a, b, expected in triples:
        numerator = qmul(qmul(a, q), b)
        require(norm(a) == norm(b) == 5 and all(v % 5 == 0 for v in numerator), '1175 legal exact product')
        output = tuple(v//5 for v in numerator)
        require(output == expected and norm(output) == norm(q) == 1175, '1175 multiplication/norm preservation')
    require((q1[2], -q1[0], q1[1], q1[3]) == (10, 11, 15, 27), 'specified signed permutation')
    require(34 in adj[8] and 6 in adj[34] and [h[i] for i in [8, 34, 6]] == [2, 13, 1], 'attained upper path')
    terminal = (9, 33, 1, 2)
    require(norm(terminal) == 1175 and norm(terminal[2:]) == 5, 'literal endpoint after pair swap')
    p = panels[81]; _, om = heights(p); adj = p['symmetry_quotient_adjacency']
    require(norm((2, 2, 3, 8)) == 81 and content((4, 4, 6, 16)) == 1, 'primitive Omega fixture')
    require([4, 4, 6, 16] in [p['B4_shapes'][i] for i in p['unit_symmetry_orbits'][5]], 'Omega source orbit')
    require(adj[5] == [3, 4, 5] and all(om[i] == 1 for i in adj[5]), 'no strict Omega step')
    require(4 in adj[5] and 1 in adj[4] and [om[i] for i in [5, 4, 1]] == [1, 1, 0], 'Omega accessible target path')
    # Frozen algebraic checks are not substitutes for written infinite proofs.
    for k in [0, 1]:
        s = 5**k; q0 = (3*s, 0, 0, 0); target = (2*s, 2*s, s, 0)
        require(norm(q0) == norm(target) == 9*25**k, 'infinite-family sample norm identity')
        require(bad5(content(tuple(2*v for v in q0))) == 3, 'family content sample')
        require(bad5(content(tuple(2*v for v in target))) == 1 and norm(target[2:]) == 5**(2*k), 'family target sample')
    q = (6, 3, 1, 1); output = (6, 2, 1, 2)
    require(q[1]-q[3]-1 == 1 and norm(q)+1 == norm(output)+3 == 48 and norm(output[2:]) == 5, 'conditional exact c-lift')
    for x in panels[16]['B4_shapes']:
        require(x[0] % 2 == 0, 'integral norm16 shell')
        q = [v//2 for v in x]
        require(all(sa*q[i]-sb*q[j] != 2 for i, j in itertools.permutations(range(4), 2) for sa, sb in itertools.product((-1, 1), repeat=2)), 'norm16 lift unavailable even under signed permutations')
    # One bounded-template witness using the source displacement and frozen64 shell.
    units = patterned((2, 0, 0, 0)) | set(itertools.product((-1, 1), repeat=4))
    v = (0, -1, 0, 1); r = 3; C = 1
    require(2**r > norm(v)+3**C-1, 'bounded template hypothesis')
    states = {tuple(4*t for t in u) for u in units}
    require(len(states) == panels[64]['H_points'] == 24 and all(norm(q) == 64 for q in states), 'frozen64 classified shell')
    require(all(norm(tuple(a+b for a, b in zip(q, v)))+3 != 65 for q in states), 'bounded-lift finite avoiding witness')


def run(cmd, cwd):
    env = os.environ.copy(); env['PYTHONDONTWRITEBYTECODE'] = '1'; env.pop('PYTHONOPTIMIZE', None)
    result = subprocess.run([str(x) for x in cmd], cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    require(result.returncode == 0, result.stdout+result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-producer', action='store_true')
    args = parser.parse_args()
    for row in read(ROOT/'SELECTED_PAYLOAD.json'):
        f = ROOT/row['repository_relative_path']
        require(hashlib.sha256(f.read_bytes()).hexdigest() == row['sha256'], 'selected custody '+str(f))
    receipt = read(ROOT/'SOURCE_RECEIPTS.json')
    require(receipt['internal_manifest_result'] == 'PASS' and all(r['status'] == 'PASS' for r in receipt['producer_replays']), 'failed source replay included')
    data = read(ROOT/'results.json')
    count = operator_replay(data); ranks = integrality_replay(data)
    with tempfile.TemporaryDirectory(prefix='gaussian_hurwitz_phase_m_replay_') as name:
        temp = Path(name)
        shutil.copyfile(ROOT/'results.json', temp/'results.json')
        for script in ['independent_audit.py', 'bottlenecks.py']:
            shutil.copyfile(ROOT/'reference'/script, temp/script)
            run([sys.executable, '-B', temp/script, temp], temp)
        independent = read(temp/'INDEPENDENT_REPLAY.json')
        require(independent['status'] == 'PASS' and len(independent['panels']) == 7, 'independent seven-panel replay')
        require(next(r for r in read(temp/'minimax_paths.json') if r['M'] == 1175)['minimax_bad_heights'][8] == 13, 'original bottleneck recurrence')
        if args.with_producer:
            # Exact original producer; its hard-coded43 panel is not enlarged.
            shutil.copyfile(ROOT/'reference/reference.py', temp/'reference.py')
            out = temp/'original43'
            run([sys.executable, '-B', temp/'reference.py', '--out', out], temp)
            fresh = read(out/'results.json')
            source_hash = next(r['source_sha256'] for r in read(ROOT/'SELECTED_PAYLOAD.json') if r['repository_relative_path'] == 'results.json')
            require(hashlib.sha256((out/'results.json').read_bytes()).hexdigest() == source_hash, 'full frozen43 producer result byte hash')
            require(len(fresh['panels']) == 43 and [p for p in fresh['panels'] if p['M'] in data['integration_selection']['committed_norms']] == data['panels'], 'original43 / compact selection equality')
    finite_certificates(data)
    print(json.dumps({'status': 'PASS', 'norm5_elements': 144, 'parameter_pairs': 20736,
                      'distinct_operators': count, 'all625_integrality_residues': ranks,
                      'independent_frozen_panels': 7, '1175_exact_minimax': 13,
                      '81_Omega_strict_descent_failure': 'PASS', 'conditional_lift_and_bounded_fixture': 'PASS',
                      'infinite_proofs_certified_by_samples': False, 'with_original43_producer': args.with_producer,
                      'new_shells': 0, 'original_n_search': False, 'A303656': 'UNRESOLVED'}))


if __name__ == '__main__':
    main()
