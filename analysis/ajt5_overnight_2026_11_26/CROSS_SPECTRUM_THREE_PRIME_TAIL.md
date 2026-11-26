# Shared phase at 17, 97, and 193, and a nonzero-shift tail control

This extends the local phase calculation in [CROSS_SPECTRUM_JOINT_PHASE_17_97.md](CROSS_SPECTRUM_JOINT_PHASE_17_97.md) to a third prime. The conclusions below concern a local model, not a mixed moment of genuine prime counts.

## A single joint phase average

Take (s=3^{26+120i}+5^{50+120j}) and (t=3^{50+120k}+5^{50+120l}). At the primes (17,97,193), the orders of (3^{120}) are (2,2,2) and those of (5^{120}) are (2,4,8). Thus (i,k) range over two residues and (j,l) over eight in the common period. Write (h=t-s), and check (pmid h) for each of the three primes on that same tuple.

| Collision bits in order 17, 97, 193 | Count |
| --- | ---: |
| 000 | 160 |
| 100 | 64 |
| 110 | 16 |
| 111 | 16 |

With these primes excluded from the coefficients, the normalized two-class residue avoidance factor is (p/(p-1)) on a collision and (1-(p-1)^{-2}) otherwise. Indeed, one forbidden residue on a collision and two otherwise are normalized by ((1-1/p)^2). The average of the joint product is **711514126363/695784701952**. Multiplying the three marginal averages would instead give **10118605453483/9895604649984**, smaller by **6359093117/89060441849856**. In particular, a collision at 193 is strictly nested inside the collision at 17 in this period, and coincides with the collision at 97 in this period.

## A concrete nonzero separation with a controlled tail

For the toy local product set (y=17). For primes not dividing (672cdot65cdot11), let (	heta=1/(p+1)) at (p>y) allowed split primes (pequiv1mod4), excluding 97 and 193, and let (	heta=0) otherwise. The kernel weights are
```text
K_p(1) = (1-theta)^2 p/(p-1)
K_p(0) = (1-theta)^2 (1-1/(p-1)^2) + 2 theta(1-theta) p/(p-1).
```
These are definitions of the model; no stochastic independence between the three collision bits is assumed. At an allowed split prime the two expressions simplify to (p^3/((p+1)^2(p-1))) and (1-1/(p^2-1)^2), respectively.

Use the actual exponents ((26,50),(50,50)). Then
```text
h = 3^50 - 3^26 = 3^26 * 2^5 * 5 * 7 * 13 * 41 * 73 * 6481.
```
The only collision beyond 193 is at the allowed split prime 6481, with factor (U=272223782641/272265779520<1). At every noncolliding prime (p>193), the factor is between (1-1/(p-1)^2) and 1. In this particular example the infinite product therefore exists, and its ratio to the product through 193 lies in
```text
7223782641/273683830455 <= ratio <= 272223782641/272265779520 < 1.
```
The lower endpoint is (Ucdot192/193), from the telescoping lower product over *all* integers (mge193) of (1-1/m^2); adding those extra factors only weakens the bound. Both endpoints refer to a single nonzero shift; no averaging over (h=0), uniform short-box estimate, or prime-pair distribution is asserted here.

## Standard-library replay

```python
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import isqrt, prod

P = (17, 97, 193)
def order(a, p):
    return next(t for t in range(1, p) if pow(a, t, p) == 1)

assert [order(pow(3, 120, p), p) for p in P] == [2, 2, 2]
assert [order(pow(5, 120, p), p) for p in P] == [2, 4, 8]
counts = Counter()
for i, j, k, l in product(range(2), range(8), range(2), range(8)):
    h = (3**(50+120*k) + 5**(50+120*l)
         - 3**(26+120*i) - 5**(50+120*j))
    counts[''.join(str(int(h % p == 0)) for p in P)] += 1
assert counts == {'000': 160, '100': 64, '110': 16, '111': 16}

def factor(p, b):
    return Q(p, p-1) if b == '1' else 1-Q(1, (p-1)**2)

joint = sum(Q(n, 256)*prod(factor(p, b) for p, b in zip(P, bits))
            for bits, n in counts.items())
separate = prod(sum(Q(n, 256)*factor(p, bits[i])
                    for bits, n in counts.items()) for i, p in enumerate(P))
assert joint == Q(711514126363, 695784701952)
assert separate == Q(10118605453483, 9895604649984)
assert joint-separate == Q(6359093117, 89060441849856)
F = {3: 26, 2: 5, 5: 1, 7: 1, 13: 1, 41: 1, 73: 1, 6481: 1}
assert all(all(p % d for d in range(2, isqrt(p)+1)) for p in F)
assert 3**50-3**26 == prod(p**e for p, e in F.items())
p = 6481
U = Q(p**3, (p+1)**2*(p-1))
assert U == Q(272223782641, 272265779520)
assert U*Q(192, 193) == Q(7223782641, 273683830455)
```
