# Target-activated repair cut in a minimal tail obstruction

Fix a target and the tail c>=v3(M), with that threshold held fixed as M is reduced. In a divisor-minimal tail obstruction, reducing an inert factor p^e by one power admits an anchor that still fails at p^e. Its residual has exact valuation e−1, odd. Thus e is even. Assume each base a=3,5 has intrinsic lift depth s_a<=e−1. Change each exponent in steps L_a of p-valuation h_a=e−1−s_a, preserving the prime-to-p coordinate at all other rows and its own order modulo p. The repairs at p^e lie exactly on a nondegenerate affine line of p first-digit pairs, by expansion modulo p^e.

Row q>p sees m_qa=max(0,v_p(ord_q(a))−h_a) variable digits on the a-axis, and must meet actual odd-valuation rejection, not merely have a structural read. For each first-digit pair on the repair line, either a shallow reader vetoes the whole higher-digit fiber, or the sum of p^(1−max(m_q3,m_q5)) over active deeper readers is at least one. Indeed, holding the other axis fixed, collision modulo q restricts at most one higher-digit class on the deeper axis. Thus at least p distinct deeper readers are required at an uncovered first pair. Smaller rows and rows reading neither variable coordinate are preserved by construction.

One ancestor can cover the whole line only if it reads exactly one digit on both axes and its two characters along the line agree, with their coefficients summing to zero and n=0 modulo that ancestor. A one-axis reader hits at most one point and deeper rows fail the fiber bound. With two distinct shallow characters, the equation on p-th roots is U T+V T^r=n. It has at most min(r,p+1−r) solutions by two polynomial forms, and at most one if n=0. Actual square-precision veto must still be checked. The replay gives four anchors at one target and fixed 7/43 orders with 7,0,1 and 6 real vetoes. Small c can still require a separate fixed-c cut. No global threshold or density change follows.

```python
from itertools import product

n, L = 46268, 258
P = list(product(range(7), repeat=2))

def order(a,m):
    return next(k for k in range(1,m) if pow(a,k,m)==1)

for a in (3,5):
    assert [order(a,m) for m in (7,49,43,1849)] == [6,42,42,1806]

def grid(c,d):
    return {(x,y): tuple((n-pow(3,c+L*x,m)-pow(5,d+L*y,m))%m
                         for m in (49,1849)) for x,y in P}

def repair(T):
    return {xy for xy,(r,s) in T.items() if r==0}

T,U,V,W = [grid(c,d) for c,d in ((1,514),(3,3),(379,514),(2,5))]
line = {(x,(2*x+1)%7) for x in range(7)}
assert repair(T)==repair(V)==line and {(0,1),(3,0)}<=line
assert all(T[z][1]==43 for z in line)
assert all(r and r%7==0 for z,(r,s) in T.items() if z not in line)
assert len(repair(U))==7 and all(s%43 for r,s in U.values())
assert all(T[z][0]==V[z][0] and (T[z][1]-V[z][1])%43==0 for z in P)
assert {z for z in line if V[z][1]==0} == {(2,5)}
assert {z for z in repair(W) if W[z][1]%43==0} == {(2,5)}
assert W[2,5] == (0,1032)
print("PASS")
```
