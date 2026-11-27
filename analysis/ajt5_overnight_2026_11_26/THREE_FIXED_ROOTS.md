# First admissible root and two later roots in one unbounded family

This is an explicit fixed-root example. It does not establish a growing number of admissible roots or resolve A303656.

For an integer $x$, call a distinct value $r=3^c+5^d$, $c,d\ge0$, admissible if $x-r$ is a sum of two integer squares. Put $M=(191\cdot19\cdot7\cdot47\cdot11)^2$. For every integer $n\ge0$ set

$$
k=5Mn,\qquad u=18-6k,\qquad y=6k^2-36k-6,\qquad x=u^2+y^2+24.
$$

Then $x=5m+4$ for an integer $m$ and $m-4=(u^2+y^2)/5$ is also a sum of two integer squares. Indeed $u\equiv3$ and $y\equiv4\pmod5$, so $(2u+y)/5$ and $(u-2y)/5$ are integer coordinates giving the representation.

For each of $(r,a)=(14,-19),(86,-17),(206,-13)$, we have $x-r=a^2+(y+3)^2$. These are actual roots: $14=3^2+5$, $86=3^4+5$, and $206=3^4+5^3$. The identities follow by expanding $x-(y+3)^2=375$.

The only roots below $14$ are $2,4,6,8,10$. At $x=384$ the differences from these have valuation exactly one at $191,19,7,47,11$, respectively. All five primes are $3\bmod4$; since $x\equiv384\pmod M$, the odd valuations persist. Therefore $14$ remains the first admissible root for every member of the family, and the two later roots coexist with it. The polynomial $x=36k^4-432k^3+1260k^2+216k+384$ is unbounded.

Replay (Python standard library):

```python
from math import isqrt, prod

early = {2: 191, 4: 19, 6: 7, 8: 47, 10: 11}
assert {3**c + 5**d for c in range(3) for d in range(3)
        if 3**c + 5**d < 14} == early.keys()
for r, p in early.items():
    assert p % 4 == 3 and all(p % j for j in range(2, isqrt(p) + 1))
    assert (384-r) % p == 0 and (384-r) % (p*p) != 0
M = prod(early.values())**2
target = [(14, -19, 2, 1), (86, -17, 4, 1), (206, -13, 4, 3)]
for n in (0, 1, 2, 17):
    k = 5*M*n
    u, y = 18-6*k, 6*k*k-36*k-6
    x = u*u + y*y + 24
    assert x % M == 384 % M and x % 5 == 4
    p, r = 2*u+y, u-2*y
    assert p % 5 == r % 5 == 0
    assert (p//5)**2 + (r//5)**2 == (x-4)//5-4
    for root, a, c, d in target:
        assert root == 3**c + 5**d
        assert x-root == a*a + (y+3)**2
```
