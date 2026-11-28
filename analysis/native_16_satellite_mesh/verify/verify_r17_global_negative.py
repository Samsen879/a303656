"""Frozen 36-factor packet: no critical carrier/subset seed at any legal y.

Standard library only.  Exhaust all 2^36 CRT classes by two sorted 18-bit
subset-sum lists and four nearest-sum staircases; certify every factor prime.
Usage: python3 -I -B verify_r17_global_negative.py [directory]
"""
import hashlib
import json
import sys
import time
from fractions import Fraction as F
from math import gcd, prod
from pathlib import Path

start = time.perf_counter()
here = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
source = here / 'released_phase_r17_boundary.json'
blob = source.read_bytes()
assert hashlib.sha256(blob).hexdigest() == '77d913c4ea3dd0dd69ee136d801f846efd492d2b67bbe43172ad50c209380638'
c = json.loads(blob)
oldblob = (here / c['source']).read_bytes()
assert hashlib.sha256(oldblob).hexdigest() == c['source_sha256']
old = json.loads(oldblob)
assert all(pack[:-1] == prefix for pack, prefix in zip(c['packs'], old['packs']))
assert (c['L'], c['K'], c['r']) == (128, 11520, 17)
A, B = 9**128, 25**128
D, E = 12*B-3*A, A+10*B
h, C = D-5, 26*B-10*A-10
assert h % 2 == 0 and C % 10 == 0 and gcd(h, 5) == 1
# Thus t=(5y^2-hy+C)/10 is integral exactly when 10 divides y.

certs = json.loads((here / 'r17_lucas_primes.json').read_text())
proved = {2}
def prove(n):
    if n in proved:
        return
    assert n > 2
    rec = certs[str(n)]
    a, fs = rec['a'], rec['factors']
    assert len({q for q, e in fs}) == len(fs)
    assert all(2 <= q < n and e >= 1 for q, e in fs)
    assert prod(q**e for q, e in fs) == n-1
    for q, e in fs:
        prove(q)
    assert 1 < a < n and pow(a, n-1, n) == 1
    assert all(gcd(pow(a, (n-1)//q, n)-1, n) == 1 for q, e in fs)
    proved.add(n)

rows = []
for edge, pack in enumerate(c['packs']):
    assert len(pack) == 18
    for m, b, z, p in pack:
        prove(p)
        assert m > 0 and b > 0 and gcd(m, b) == 1
        assert p == m*m+b*b and gcd(p, 10*D*E) == 1
        I = m*pow(b, -1, p) % p
        lin = -h+(10*I if edge else 0)
        con = -5-E-h*I if edge else 5-E-(h+10)*I
        zz = (-lin*pow(5, -1, p)-z) % p
        assert zz != z and (lin*lin-20*con) % p != 0
        for y in (z, zz):
            assert (5*y*y+lin*y+con) % p == 0
            t = (5*y*y-h*y+C)*pow(10, -1, p) % p
            x, w = h-3*t, t
            x, w = (x+3-y, w-1-3*y) if edge else (x+1, w+3)
            assert (m*x-b*w) % p == (b*x+m*w) % p == 0
        rows.append((p, z, zz))
assert len({p for p, z, zz in rows}) == 36
# Each quadratic over its proved prime field has exactly these two roots.
M = 10*prod(p for p, z, zz in rows)
assert 39*M == c['M']
base, steps = 0, []
for p, z, zz in rows:
    assert gcd(p, M//p) == 1
    basis = (M//p)*pow(M//p, -1, p)
    base = (base+z*basis) % M
    steps.append((zz-z)*basis % M)
def sums(ds):
    out = [0]
    for d in ds:
        out += [(a+d) % M for a in out]
    return sorted(out)
left, right = sums(steps[:18]), sums(steps[18:])
assert len(left) == len(right) == 2**18
def nearest(target):
    j, above, below = len(right)-1, None, None
    for a in left:
        while j >= 0 and a+right[j] >= target:
            value = a+right[j]
            if above is None or value < above:
                above = value
            j -= 1
        if j >= 0:
            value = a+right[j]
            if below is None or value > below:
                below = value
    return above, below
positive, negative = [], []
for k in range(4):
    target = k*M-base
    above, below = nearest(target)
    if above is not None and 0 <= above-target < M:
        positive.append(above-target)
    if below is not None and 0 < target-below <= M:
        negative.append(target-below)
minpos, minneg = min(positive), min(negative)
assert hashlib.sha256(str(minpos).encode()).hexdigest() == '5c55b483da5a366032e5f092bc2869f892dc2f8d94bfea2fcd28921da48de9f5'
assert hashlib.sha256(str(minneg).encode()).hexdigest() == '7c3a53370cfe4c81b19fd70d8c371658a0a94051fa4dfb166f2067c653a6e477'

# All full-packet loading y have |y| >= Y0.  Then t>=9y^2/20,
# S>=t^2>2^11901 and K_y=floor(log2 S)>=11901.
Y0, K0, eps = 2**2976, 11901, F(1, 2**2970)
assert min(minpos, minneg) >= Y0 and 0 < 2*h < Y0 and C > 0
assert F(81, 400)*Y0**4 > 2**K0
# q/S differs from 2sin^2(theta_G) by at most gap/S+|Q-P|/sqrt(S).
# Both raw chords satisfy |Q-P|<=4|y|, so this is < eps.
assert F(max(D, E), 2**K0)+F(80, 9*Y0) < eps
carrier_ideals = []
for pack in c['packs']:
    assert sum(F(b, m) for m, b, z, p in pack) < F(1, 100)
    m, b, z, p = pack[0]
    carrier_ideals.append(F(2*b*b, p))
# All satellites have positive angles.  Every allowed G contains its carrier,
# hence its ideal ratio is at least its carrier's ratio on this small arc.
assert min(carrier_ideals)-eps > F(1, 64*K0*K0)
print('PASS 36 prime norms, all 2^36 legal root classes exhausted')
print('minimum positive/negative-distance bits:', minpos.bit_length(), minneg.bit_length())
print('PASS no full-packet loading y with S < 2^11521')
print('PASS every allowed carrier/subset q has 64*K_y^2*q > S at every loading y')
print('scope: this frozen oriented full packet and its prescribed rotations only')
print('seconds:', round(time.perf_counter()-start, 3))
