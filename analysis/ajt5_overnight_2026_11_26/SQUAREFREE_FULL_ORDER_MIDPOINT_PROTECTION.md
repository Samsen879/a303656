# Squarefree full-order filtering and inverse midpoint protection

The inverse-class midpoint has an exact order-based protection test. At \(r=31\), it excludes **every genuine common-Wieferich reader** in the class where both full orders divide \(31\cdot3960\) and at least one reads \(31\). Outside that order class, a single fixed integer gives two inverse readers with the same safe midpoint and an ordinary noninverse reader that vetoes it. A second fixed integer gives a zero-aligned reader that vetoes the entire line.

### Full-order protection test

Write the two powers on a frozen \(r\)-line modulo a reader prime \(q\) as \(AX^x\) and \(BY^x\), with \(x\in\mathbf F_r\) and \(X^r=Y^r=1\). For an active inverse reader, \(Y=X^{-1}\) and \(X\ne1\). If it hits the same observation at distinct digits \(a,b\), subtraction gives \(B/A=X^{a+b}\). Every hit then belongs to the pair \(\{a,b\}\), since \(X^x\) satisfies a quadratic. Thus readers sharing \(a+b\) all leave \((a+b)/2\) safe. This protection concerns inverse readers with two hits. An inverse reader with a singleton can still hit that midpoint.

For an odd prime \(r\nmid W\), define
\[
 L_b=b^W-1,\qquad P_b=\frac{b^{rW}-1}{b^W-1}\qquad(b=3,5).
\]
Suppose \(q>5\) is common Wieferich, both full orders modulo \(q\) divide \(rW\), and at least one contains \(r\). The orders modulo \(q^2\) equal the orders modulo \(q\). Indeed, if \(d=\operatorname{ord}_q(b)\), the binomial expansion of \((b^d)^{(q-1)/d}\) forces \(b^d\equiv1\bmod q^2\). A reading axis therefore has \(q^2\mid P_b\), since its denominator is a \(q\)-unit. An axis whose order omits \(r\) has \(q^2\mid L_b\). Consequently one of
\[
 \gcd(P_3,P_5),\qquad \gcd(P_3,L_5),\qquad \gcd(L_3,P_5)
\]
must contain \(q^2\). All three are squarefree at \((r,W)=(31,3960)\), as the exact replay below verifies. The mod-\(3960\) phase lock alone leaves the readers’ full prime-to-\(31\) orders unrestricted. [Mod-\(3960\) head policy](https://github.com/Samsen879/a303656/commit/4a33a5d51aa0e617fb108629f84b782beebd7977)

The same test gives a finer filter when those gcds have square factors. For increments \(U,V\) and slope \(s\), remove from the appropriate gcd all prime supports dividing \(3^U5^{sV}-1\). At a genuine common reader, this removes exactly the inverse characters: reduction modulo \(q\) is injective on the \((q-1)\)-torsion modulo \(q^2\). Any remaining reader hitting a fixed midpoint must have its square divide the resulting gcd and \((n-S_{\rm mid})^2\), where \(S_{\rm mid}\) is the actual sum of the two powers. This is a necessary test against the same integer \(n\).

### Fixed-target controls

Take \(H=499466286827715209306040\), \(c_0=31H\), \(d_0=26H\), and
\[
 n=3^{c_0}+5^{d_0}+31^2\cdot242731\cdot476719.
\]
Use \(c=c_0+Hx,\ d=d_0+H(5x\bmod31)\), and then choose the unique top digit \(k\) by increasing \(c\) by \(31Hk\) so the source remainder is \(31^2\bmod31^3\). This repair leaves the listed readings unchanged even modulo their squares. The small-head remainders remain \(1\bmod4\) and units at \(3,7,11,19,23\).

| Reader \(q\) | \(\operatorname{ord}_q(3)\) | \(\operatorname{ord}_q(5)\) | \(Y=X^j\) | Digits with exact valuation one |
|---:|---:|---:|---:|---|
| 242731 | 242730 | 40455 | \(j=-1\) | \(0,1\) |
| 476719 | 476718 | 79453 | \(j=-1\) | \(0,1\) |
| 3163 | 3162 | 3162 | \(j=12\) | \(16\) |

The common midpoint is \(16\). All three observations are nonzero, and all six base lifts are ordinary. In fact, for each displayed exact order pair \((u,v)\), \(\gcd(\Phi_u(3),\Phi_v(5))=q\). Those order pairs cannot support a genuine common-Wieferich reader. Other digits survive the three rows.

For a **zero observation**, an unaligned reader has at most one hit, since \((X/Y)^x=-B/A\). An active aligned reader \(X=Y\ne1\) hits every digit exactly when \(A+B=0\bmod q\). The even-even head above rules that out at every inert prime because both powers are squares. To see the other case with actual bases, keep \(H\), use \((c_0,d_0)=(7741,4)\), slope \(3\), and set \(n=3^{7741}+5^4+43\cdot31^2\cdot3163\). The same top repair works, and \(3163\) is zero-aligned with exact valuation one at all 31 digits. Both controls can be made positive throughout by adding a sufficiently large multiple of the checked moduli to their respective targets. They certify finite modular charts, without an ordinary-height bound or a first-blocker density claim.

```python
from math import gcd, isqrt, lcm, prod

r, W = 31, 3960
def prime(q):
    return q > 1 and all(q % d for d in range(2, isqrt(q) + 1))

A, B = 3**W, 5**W
P, T = (A**r-1)//(A-1), (B**r-1)//(B-1)
both = (31,311,373,683,1117,1489,1861,2729,2791,4093,5581,
        8929,11161,12277,16369,61381,122761)
for g, fs in [(gcd(P,T),both), (gcd(P,B-1),(31,245521)),
              (gcd(A-1,T),(31,))]:
    assert len(set(fs)) == len(fs) and all(map(prime,fs))
    assert g == prod(fs)

def factors(n):
    return [p for p in range(2,n+1) if n % p == 0 and prime(p)]

def cyclo(b,k):
    terms = [(k,1)]
    for p in factors(k):
        terms += [(d//p,-s) for d,s in terms]
    return (prod(b**d-1 for d,s in terms if s == 1)
            // prod(b**d-1 for d,s in terms if s == -1))

p,t,q = 242731,476719,3163
rows = ((p,242730,40455,30),(t,476718,79453,30),(q,3162,3162,12))
H = lcm(W, *(z*k//r for z,u,v,_ in rows for k in (u,v)))
assert H == 499466286827715209306040 and H % r
for z,u,v,j in rows:
    assert prime(z) and z % 4 == 3
    for b,k in ((3,u),(5,v)):
        assert (z-1) % k == 0 and pow(b,k,z) == 1
        assert all(pow(b,k//f,z) != 1 for f in factors(k))
        assert pow(b,z-1,z*z) != 1 and pow(b,r*H,z*z) == 1
    assert gcd(cyclo(3,u),cyclo(5,v)) == z
    X = pow(3,H,z)
    assert X != 1 and pow(X,j,z) == pow(5,5*H,z)

def S(c,d,m):
    return (pow(3,c,m) + pow(5,d,m)) % m

def chart(c,d,s,delta,readers):
    assert delta % 4 == 1 and all(delta % z for z in (3,7,11,19,23))
    def N(m):
        return (S(c,d,m) + delta) % m
    hits = {z:{} for z in readers}
    for x in range(r):
        C,D = c+H*x, d+H*(s*x % r)
        assert (N(r*r)-S(C,D,r*r)) % (r*r) == 0
        k, = [k for k in range(r)
              if (N(r**3)-S(C+r*H*k,D,r**3)) % r**3 == r*r]
        for z in readers:
            R = (N(z*z)-S(C+r*H*k,D,z*z)) % (z*z)
            if R % z == 0:
                assert R
                hits[z][x] = R//z
    return [N(z) for z in readers], hits

obs,hits = chart(31*H,26*H,5,r*r*p*t,(p,t,q))
assert obs == [169140,419276,1994]
assert hits == {p:{0:93562,1:93562}, t:{0:148900,1:148900}, q:{16:2585}}

assert pow(3,H,q) == pow(5,3*H,q) == 708
obs,hits = chart(7741,4,3,43*r*r*q,(q,))
assert obs == [0] and set(hits[q]) == set(range(r))
```

The remaining case is a genuine common reader with prime-to-\(31\) order factors outside \(3960\) that survives the full-order filter and hits the midpoint on the same retained chart. The ordinary controls show why a bound using relative characters alone cannot exclude that case.

Independent BigInt checked the three squarefree core gcds, all three exact pair cyclotomic gcds and both full fixed-target charts. In the midpoint filter, XY=1 removes inverse active readers and any jointly blind ones, whose constant readings need separate checks. The cap on full orders is not inferred from the head phase lock.
