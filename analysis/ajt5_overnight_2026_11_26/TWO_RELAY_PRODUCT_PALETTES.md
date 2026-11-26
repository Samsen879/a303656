# Two-relay product palettes and zero-reader fibres

**The nonzero-reader Sidon bound survives on any sparse subset of a genuine two-relay product.** Conditioning gives a bound on each fibre, but the two fibre caps cannot be multiplied. On the actual \(7,79\to3319\) graph, both diagonal pairs of a \(2\times2\) palette have exact valuation one, while both off-diagonal pairs are safe. One more synchronized pair gives a safe choice. [Pinned one-relay palettes](https://github.com/Samsen879/a303656/blob/56fa061cd543e3869346a14716e86e5ebbf1197b/analysis/ajt5_overnight_2026_11_26/PHASE_DEPENDENT_REPAIR_PALETTES.md) · [Actual \(3319\) graph](https://github.com/Samsen879/a303656/blob/f0c2bac68b965850151c8a12a314f980930c72e4/analysis/ajt5_overnight_2026_11_26/DOUBLE_RELAY_CANCELLATION_CRITERION.md)

### Product and sparse palettes

Fix the shared spare label. Suppose the two shallow relay repairs have independent affine digit lines, with the high corrections invisible to the reader. Write its equation as
\[
A\chi(x,y)+B\psi(x,y)=N.
\]
Here the two characters are jointly injective because the reader sees a nontrivial primary component of each distinct relay prime. Let \(E\) be the available set of digit pairs and let \(\theta=\chi/\psi\).

For \(N\ne0\), two hits at a prescribed difference \(d\notin\ker\theta\) determine both character values by a two-by-two linear system. Thus there is at most one such ordered pair. A nonzero difference in \(\ker\theta\) is impossible between hits because the common multiplier would have to fix \(N\), forcing both characters to be trivial on \(d\). Consequently the hit set \(T\) satisfies
\[
|T|(|T|-1)\le |(E-E)\setminus\ker\theta|.
\]
The same argument holds inside each conditioned fibre. Its cap can be summed over fibres and compared with the joint bound.

For \(m\) nonzero readers, a product of two first-digit progressions of length \(2m\) leaves a safe pair. Each reader hits at most \(4m-1\) of the \(4m^2\) cells by the difference bound. A sparser option is **\(2m^2+1\) synchronized pairs** along one progression with both coordinates moving. There are at most \(4m^2\) nonzero differences, so each reader hits at most \(2m\) pairs. These statements require the indicated digits to be available. On a nonhomogeneous repair line, every nonzero first digit comes from an admissible finite ray. Common scaling preserves the progression when those same rays are used at another spare label. If one relay instead changes the other’s repair slope, the conditioned bound still applies inside each fibre where that slope is fixed.

### Exactly when a zero fibre fills

Put \(D_p=\chi(1,0)/\psi(1,0)\) and \(D_t=\chi(0,1)/\psi(0,1)\). For \(N=0\), the equation is
\[
D_p^xD_t^y=-B/A.
\]
A fibre with at least two distinct \(x\)-choices fills **exactly when** \(D_p=1\) and the fixed \(y\) satisfies the remaining equation. The primary orders are coprime. Thus, when the right-hand side lies in the image, each transverse coordinate is fixed uniquely and each aligned coordinate is free.

Filling modulo \(r\) is the first test. If the common multiplier on an aligned fibre lifts to \(g\) modulo \(r^2\), and the frozen sum there is \(S\), exact valuation one at \(x\) is equivalent to
\[
n/r\ne (S/r)g^x\pmod r.
\]
In the actual \(7,19\to9603931\) control below, \(S=0\bmod r^2\) and \(n=r\bmod r^2\), so the entire rooted product has exact valuation one in the frozen reader phase. A second control uses a transverse digit line on a **unit** branch at \(19\). It fills exactly the \(y=0\) fibre, while the rooted relay at \(7\) still has exact valuation two. [Known \(9603931\) alignment](https://github.com/Samsen879/a303656/blob/e6cf8efaa12572fce12599e3bc54fdbe148c6c5c/analysis/ajt5_overnight_2026_11_26/ALIGNED_SMOOTH_COMPLEMENT_TAIL.md)

### Runnable replay

At the known spare label \(1\) of the \(3319\) graph, the first-digit pairs \((1,8),(2,34),(3,60)\) correspond to actual ray pairs \((3,70),(2,65),(4,38)\). The first two hit at the same target. The third pair and the two off-diagonals pass.

```python
from itertools import product
from math import isqrt, lcm, prod

def setup(p,t,r):
    assert all(z%4 == 3 and all(z%d for d in range(2,isqrt(z)+1))
               for z in (p,t,r))
    H = lcm(p*p*(p-1), t*t*(t-1), r*(r-1))
    def step(m):
        b = H//m
        return b*pow(b,-1,m)
    U,V = step(p*p),step(t*t)
    assert U%(t*t*(t-1)) == V%(p*p*(p-1)) == 0
    assert p*U%(r*(r-1)) == t*V%(r*(r-1)) == 0
    for q,W in ((p,U),(t,V)):
        assert all(pow(a,W,q)==1 and pow(a,W,q*q)!=1 for a in (3,5))
        assert all(pow(a,W,r)!=1 and pow(a,W*q,r)==1 for a in (3,5))
    return H,U,V,step

def rem(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def even(n,c,d,roots):
    for p,U in roots:
        assert rem(n,c,d,p*p)==0
        if rem(n,c,d,p**3)==0:
            c+=p*U
    assert all(rem(n,c,d,p**3) in range(p*p,p**3,p*p) for p,_ in roots)
    assert rem(n,c,d,3)==rem(n,c,d,4)==1
    return c,d

p,t,r = 7,79,3319
H,U,V,step = setup(p,t,r)
J = step(3)
C,D = 214742619+J,79168445538+2*J
n = 21784939874149193

def line(q,W):
    a,b = ((pow(z,W,q*q)-1)//q*pow(z,e,q)%q
           for z,e in ((3,C),(5,D)))
    assert rem(n,C,D,q*q)==q
    return pow(b,-1,q),-a*pow(b,-1,q)%q

assert (line(p,U),line(t,V)) == ((2,1),(28,27))
assert n%(r*r)==1517
for x,y,s in ((1,8,1517),(1,34,3240),(2,8,1136),(2,34,1517),(3,60,575)):
    c,d = even(n,C+U*x+V*y,D+U*((2+x)%p)+V*((28+27*y)%t),((p,U),(t,V)))
    assert (pow(3,c,r)+pow(5,d,r))%r == s
    if s==1517:
        assert rem(n,c,d,r*r) in range(r,r*r,r)

p,t,r = 7,19,9603931
D,U,V,_ = setup(p,t,r)
C = prod(z*((z-1)//2) for z in (p,t,r))
assert all(pow(3,C,z*z)==z*z-1 and pow(5,D,z*z)==1 for z in (p,t,r))
assert pow(3,U,p*p)==pow(5,U,p*p)
assert pow(3,V,t*t)==pow(5,11*V,t*t)
assert pow(3,U,r*r)==pow(5,U,r*r)
assert pow(3,V,r*r)==pow(5,11*V,r*r)
assert pow(3,V,r)!=pow(5,V,r)

for mixed in (False,True):
    pairs = ((5,12),(0,p*p),(int(mixed),t*t),(r,r*r))
    M = prod(m for _,m in pairs)
    n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M
    roots = ((p,U),) if mixed else ((p,U),(t,V))
    for x,y in product((1,2),(0,1)):
        c,d = even(n,C+U*x+V*y,D+U*x+V*(1 if mixed else 11)*y,roots)
        if mixed:
            assert rem(n,c,d,t)==1
        if mixed and y:
            assert rem(n,c,d,r)!=0
        else:
            assert rem(n,c,d,r*r)==r
print('OK')
```

A single sufficiently large lift of each target by a multiple of \(12p^3t^3r^2\) makes all selected remainders positive while preserving the tests. The resulting certificates control the specified finite panel and reader phase.

The modulo-reader squared rule assumes that the two term multipliers in the varying aligned coordinate agree modulo the squared reader prime, and that the reader observation is a multiple of its prime. With those hypotheses both terms share a common multiplier after lifting, so division by the reader prime is legitimate. Without this stronger alignment, a full zero fibre modulo the reader prime need not have the same valuation parity at its lifts. The nonzero difference bound only uses the prime-level characters and remains valid on arbitrary subsets of the stated independent digit product.
