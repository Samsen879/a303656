# A full mod-5 failure subclass for the fixed-head power selector

This is a limitation of [the all-head Gaussian gcd selector](https://github.com/Samsen879/a303656/commit/670613071ddbe90fce39e37e2b5527fa169a1828) **as a certificate algorithm**, not of the original representation. Both actual exponent axes are still in their logarithmic height window. The failure applies to the stated head, direct test and optional 17 peel, and to a polylogarithmic-size **fixed-for-the-scale** set of bases. Applying the uniform pseudoprime bound separately to a base picked afresh at each candidate would not justify the same assertion for arbitrary adaptive bases.

For the witnessed misses, the coordinate sum-length proof uses only the prescribed congruences. In the equal-norm count, the nonzero difference is an integer multiple of a primitive direction and the sum an integer multiple of its unique perpendicular primitive direction. The diagonal contributes \(O(X)\); summing the nonzero counts over primitive max-coordinate \(m\) gives \(O(X\log X)\). This proves the stated \(\gg X/\log X\) actual witnessed misses, separately from the asymptotic one-fifth failure subclass of the selector. Both 1,200-bit fixtures, all 32 labels, every matched panel pass, and both Gaussian witnesses were independently replayed.

**The current selector fails on asymptotically one entire mod-\(5\) subclass in every selected head.** Its lower failure density is therefore at least **20% in each head**, even if it tries both the direct test and the \(17\)-peel and accepts every composite that passes. Each failure subclass also contains \(\gg X/\log X\) targets per dyadic window with a genuine two-square witness inside the actual exponent box.

### The obstruction

Fix a head \(h\bmod M\), where \(M=1728\cdot17\). Write its chart as \(c\equiv c_0\bmod16,\ d\equiv d_0\bmod144\), with normalization \(w=2^a9^b\) and peel \(A\in\{1,17\}\). On the CRT subclass
\[
n\equiv h\pmod M,\qquad n\equiv3^{c_0}\pmod5,
\]
every menu remainder \(R=n-3^c-5^d\) is divisible by \(5\). Indeed \(3^c\equiv3^{c_0}\bmod5\) and \(d>0\). Both \(R/w\) and \(R/(wA)\) retain that factor.

For \(X=2^H\), \(X/2\le n<X\), and the actual box \(H/32\le c,d\le H/4\), the shifts are \(o(X)\). Thus every tested normalized remainder \(V\) on this subclass is positive, \(\asymp X\), and composite. A successful root check requires \(2^{(V-1)/2}\equiv-1\bmod V\), hence \(2^{V-1}\equiv1\bmod V\). For a fixed label and normalization, each such \(V\) gives at most one \(n\). The \(O(H^2)\) labels therefore give at most
\[
O\!\left(H^2X/L(X)^{1/2}\right)=o(X),
\qquad
L(X)=\exp\!\left(\frac{\log X\,\log\log\log X}{\log\log X}\right)
\]
successful targets, by the Li–Pomerance uniform pseudoprime bound. The CRT subclass is one fifth of its head. The same count shows that across the full menu, successes obtained from composite tested values \(V\) occur on only \(o(X)\) targets. [Li–Pomerance, *Fermat pseudoprimes*, Theorem 1](https://math.dartmouth.edu/~carlp/evenpspsfinal.pdf)

This obstruction survives adding any polylogarithmic-sized set of bases drawn from \([2,X]\), using Li–Pomerance’s uniform bound and a union over that set. Peeling one factor \(5\) while keeping the same base-\(2\) quarter-power rule also leaves the obstruction: the new tested value is \(1\bmod8\), so primes fail by the supplementary law for \(2\), and passing composites remain sparse. [Li–Pomerance, *Fermat pseudoprimes*, Theorem 1](https://math.dartmouth.edu/~carlp/evenpspsfinal.pdf)

### Genuine witnesses among the misses

Fix one in-box label per head and scale, with shift \(S=3^c+5^d\). Put \(n=S+5wA(x^2+y^2)\). The head prescribes one residue for \(x^2+y^2\bmod M/(wA)\). It is \(1\bmod8\), a unit at \(3\), and representable mod \(17\) when that modulus is present. The first condition allows a square root at the required \(2\)-power. At \(3\), a unit norm mod \(3\) lifts using a unit coordinate. At \(17\), the norm splits into two linear factors.

At each other inert panel prime \(p\le H/16\), exclude just \((x,y)\equiv(0,0)\bmod p\). These tests retain a constant fraction of the coordinate residue pairs because \(\prod_p(1-p^{-2})>0\). The CRT modulus is \(O(X^{1/8})\) by the elementary primorial bound. Taking both coordinates in \([\,\sqrt{X/(5wA)}/2,\ 5\sqrt{X/(5wA)}/8\,]\) gives \(\gg X\) pairs with \(n\in[X/2,X)\), a genuine norm at the chosen label, and a pass on the growing inert panel.

There are \(\gg X/\log X\) distinct targets. For the multiplicity bound, two equal norms give orthogonal difference and sum vectors. If the primitive direction of the nonzero difference has maximum coordinate \(m\), there are \(O(m)\) directions and \(O(X/m^2)\) choices of the two multipliers. Summing gives \(O(X\log X)\) equal-norm pairs, including the diagonal. Cauchy–Schwarz gives the distinct-target bound. The pseudoprime exceptions are \(o(X/\log X)\), so the full selector still misses \(\gg X/\log X\) of these witnessed targets in each head.

### Matched exact replay

Both 1,200-bit inputs below use the \(17\)-peel. They have identical readings mod \(1728\cdot17\) and every inert panel \(p^3\). Their actual grids each contain 32 positive labels, with the same 23 passing the panel. The first certifies \((51,145)\). The second has a true norm at that same label, but neither base-\(2\) branch succeeds anywhere in its grid.

```python
from itertools import product
from math import isqrt, prod

def prime(p):
    return p > 1 and all(p % j for j in range(2, isqrt(p)+1))

def head(n):
    a = 0 if n % 2 else 3
    Q = 1 << (a+3)
    L = Q//4
    c, e = next((c,e) for e in (0,1) for c in range(3,3+L)
                if (n-pow(3,c,Q)-pow(5,e,Q)) % Q == 5*2**a)
    b = int(n % 3 == pow(5,e,3))
    d = next(d for d in range(1,145)
             if (d-e) % L == 0 and (not b or (n-pow(5,d,27)) % 27 == 9))
    return c, d, 2**a*9**b

def root(base, V):
    r = pow(base, (V-1)//4, V)
    return r if r*r % V == V-1 else None

def norm(V, r):
    assert r is not None
    a,b,c,d = V,0,r,1
    while c or d:
        D = c*c+d*d
        x = (2*(a*c+b*d)+D)//(2*D)
        y = (2*(b*c-a*d)+D)//(2*D)
        a,b,c,d = c,d,a-x*c+y*d,b-x*d-y*c
    assert a*a+b*b == V
    return a,b

def mul(z, w):
    a,b = z
    c,d = w
    return a*c-b*d, a*d+b*c

H = 1200
P = [p for p in range(7,H//16+1,4) if prime(p)]
W = 1728*17*prod(p**3 for p in P)
p = 2**(H-5)+1109
q0 = 2**(H-7)
q = q0+(p*pow(5,-1,W)-q0)%W+413*W
S = 3**51+5**145
good, bad = S+17*p, S+85*q

assert (good-bad)%W == 0 and (good-S)%5 and (bad-S)%5 == 0
assert good.bit_length() == bad.bit_length() == H
C,D,w = head(good)
assert (C,D,w) == head(bad) == (3,1,1)
box = range((H+31)//32,H//4+1)
grid = list(product([c for c in box if (c-C)%16==0],
                    [d for d in box if (d-D)%144==0]))

for n in (good,bad):
    hits, legal = [], 0
    for c,d in grid:
        R = n-3**c-5**d
        assert R>0 and R%17==0 and (R//17)%8==5 and R%3
        if n==bad:
            assert (R//17)%5==0 and root(2,R) is None
        legal += int(all(R%l for l in P))
        if root(2,R//17) is not None:
            hits.append((c,d))
    assert len(grid)==32 and legal==23
    assert hits == ([(51,145)] if n==good else [])
    print(legal,hits)

gp = mul((4,1),norm(p,root(2,p)))
bq = mul(mul((4,1),(2,1)),norm(q,root(3,q)))
assert sum(t*t for t in gp)==good-S and sum(t*t for t in bq)==bad-S
assert all((good-S)%l for l in P)
```

The failure is a property of this chart and certificate rule. It gives no failures of the original conjecture.
