# A cubic factor split forces a penultimate divisor in P2

**The penultimate block forces a new divisor.** In the pinned P2 phase, both cyclotomic inputs are cubes. This gives two explicit, coprime factors of the penultimate block. In any ordinary-height solution, the side with the smaller highest-block share must take a divisor from the larger penultimate factor. On the pinned cofinal progression, the certified \(727\) alone is too small. Concentrating the rest of that factor on either side therefore rules out one highest-block polarity. [Pinned signed-divisor result](https://github.com/Samsen879/a303656/commit/19d61d7c2a52a8ed0d1dfe31844bd11ef91c650b)

### The size constraint

Write \(A=3^a\), \(B=5^b\), \(W=\sqrt A\), \(T=D_r\), and \(E=24D_0\cdots D_{r-2}\). Since \(a-1,b+2\) are divisible by \(3\), the inputs \(X,Y\) are cubes \(x^3,y^3\). With \(n=11^{j-1}\), the actual factorization is
\[
D_j=C_jF_j,\qquad
C_j=\frac{x^{11n}+y^{11n}}{x^n+y^n},\qquad
F_j=\frac{x^{22n}-x^{11n}y^{11n}+y^{22n}}
          {x^{2n}-x^ny^n+y^{2n}}.
\]
The prime orders of \(x/y\) in the two factors are \(2\cdot11^j\) and \(6\cdot11^j\), respectively. The possible overlap primes \(3,11\) do not divide \(D_j\) in this phase.

For either side of \(uv=d\), write its factor as \(ecfz\), with \(e\mid E,\ c\mid C_{r-1},\ f\mid F_{r-1},\ z\mid T\). Both sides exceed \(4W\) in the ordinary window. The exact integer test
\[
(E C_{r-1}b_0)^2T\le16A
\]
therefore excludes \(f\le b_0\) and \(z\le\sqrt T\) on the same side, including equality in the test.

On the pinned balanced strip,
\[
E<18A^{1/121},\qquad C_{r-1}<4A^{10/363},\qquad \sqrt T<6A^{5/11}.
\]
The middle bound follows directly from the formula for \(C_{r-1}\) and \(y^{3\cdot11^r}=25B\). Thus a side with \(z\le c_0\sqrt T\) must take a true divisor
\[
f>\frac{A^{7/726}}{108c_0}
\qquad\text{from }F_{r-1}.
\]
In particular, the side with the smaller highest-block share must draw from \(F_{r-1}\), even if it has access to every earlier factor and all of \(C_{r-1}\).

### What this rules out on the actual progression

On the pinned \(r=3\) progression, \(727^1\parallel F_2\). Put \(N=F_2/727\). For every balanced member with even \(a\ge1142\), the bound above exceeds \(727\) even at \(c_0=2\). Consequently:

- If **all of \(N\) is assigned to the long side**, the short-side highest share must exceed \(2\sqrt T\).
- If **all of \(N\) is assigned to the short side**, the long-side highest share must exceed \(2\sqrt T\), so the short-side share is below \(\sqrt T/2\).
- If both highest shares are at most \(2\sqrt T\), **\(N\) must split nontrivially between the two sides**. If \(N\) is certified indivisible in an allocation, that entire range of highest-block splits is excluded.

The replay confirms \(727\)'s exact depth by modular powers and also places \(15973^1\) in the *smaller* top factor \(C_3\). It checks the same exact \(v=4\cdot727\cdot15973\) and \(u=d/v\) at all three local sites. That control passes the local square tests and lies below \(4W\). The ordinary window remains open for allocations with a sufficiently large split of \(N\), or with highest shares far enough apart. The two remaining integer square conditions are still required.


In the balanced strip \(0.9\le B/A\le1.1\), use
\((U^{11}+V^{11})/(U+V)\le \max(U,V)^{10}\) for the upper bounds on \(C_{r-1}\) and \(T\). The former uses \(U=(A/3)^{1/363},V=(25B)^{1/363}\), and the latter uses exponents \(1/11\). For \(E\), the product telescopes to \(6((A/3)^{1/121}+(25B)^{1/121})\). The two cubic factors are the corresponding cyclotomic factors of coprime \(x,y\); the exceptional primes dividing their cyclotomic indices, 2, 3 and 11, do not divide \(D_j\) here.

```python
from math import isqrt, gcd
M=11128367376720
s,t=1273865740071,681186
assert s%3==t%3==M%3==0
a,b=1331*s+1,1331*t-2
assert (a%720,b%720)==(22,4)
for p,j,o in ((727,2,726),(15973,3,2662)):
    assert all(p%i for i in range(2,isqrt(p)+1))
    m=p*p
    assert all(pow(x,M//3,m)==1 for x in (3,5))
    x,y=pow(3,s//3,m),pow(5,t//3,m)
    ratio=x*pow(y,-1,p)%p
    assert pow(ratio,o,p)==1
    for l in (2,3,11):
        if o%l==0: assert pow(ratio,o//l,p)!=1
    low=(pow(x,3*11**(j-1),m)+pow(y,3*11**(j-1),m))%m
    high=(pow(x,3*11**j,m)+pow(y,3*11**j,m))%m
    assert low%p and high%p==0 and high!=0
assert 3**(1142*7)>(216*727)**726
v=4*727*15973
for m,expected in ((1331,(121,289)),(727,(272,418)),(15973,(15738,6122))):
    Q=m*v
    assert all(pow(x,1331*M,Q)==1 for x in (3,5))
    A,B=pow(3,a,Q),pow(5,b,Q)
    d=2*(A+75*B)%Q
    assert d%v==0
    u=d//v
    assert (((u+v)**2-4*(20*A+25*B))%m,
            ((u+v)**2-4*(182*A-6*B))%m)==expected
print("OK")
```
