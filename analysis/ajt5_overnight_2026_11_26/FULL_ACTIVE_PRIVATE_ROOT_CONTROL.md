# Five actual parent blocks with private roots of one color

At m=8676127667, r=1, the genuine parent indices 2,3,8,12,13 have a cover of their combined full active child menu by inert primes greater than 3. There are 184 active numerical roots. The prime 7 occurs privately, relative to any inclusion-minimal cover of those five blocks, at the child labels (2,1), (4,17), (9,12), (12,9), (14,7), one from each indicated parent. For the last four labels the allowed support is exactly {7}, so 7 is mandatory. For the first label the only alternative is 41873203, which appears nowhere else and is redundant once 7 is selected. This does not mean that all true parents are covered: parent 0 gives a real bridge on the same integer.

A more general unlimited-budget extension test: for each active root z let V(z) be its allowed odd-valuation support. To make designated roots a private to assigned primes q_a, require q_a∈V(a), and forbid the union B of V(a) minus {q_a} over all designated roots. Extension to a full cover of these blocks is possible iff each V(z) minus B is nonempty. Necessity follows from the privacy condition, and taking all remaining supports proves sufficiency. In particular a truly unblocked row or a zero residual cannot be ignored.

Independent standard-library replay:

```python
from math import isqrt
m = 8676127667
x = 5*m+1
D = [2,3,8,12,13]
E = {d+i for d in D for i in (0,1)}
def shifts(N, e):
    z = 1
    while z+5**e <= N:
        yield z+5**e
        z *= 3
def odd(n, low):
    assert n >= 0
    if n == 0: return set()
    out = set()
    p = 2
    while p*p <= n:
        v = 0
        while n % p == 0:
            n //= p
            v ^= 1
        if v and p >= low and p % 4 == 3:
            out.add(p)
        p += 1
    if n >= low and n % 4 == 3:
        out.add(n)
    return out
assert all(any(not odd(m-z,3) for z in shifts(m,d)) for d in D)
V = {z: odd(x-z,7) for e in E for z in shifts(x,e)}
assert len(V) == 184 and all(V.values())
keys = [5**e+3**f for e,f in [(2,1),(4,17),(9,12),(12,9),(14,7)]]
assert [V[z] for z in keys] == [{7,41873203}]+[{7}]*4
assert sum(41873203 in s for s in V.values()) == 1
assert x == 1+3**11+52008**2+201682**2
```

This is a full-menu control for the five chosen genuine columns, not an unbounded reuse construction or a global no-bridge example.
