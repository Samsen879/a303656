# Sharp obstruction and compatibility test for short reader directions

**A shared low ratio gives a uniform root bound. A single incompatible relay can force the first relation’s height to grow linearly with the label length.** In the actual \(7\to43\to3011\) graph, changing the repair ray from 26 to 7 makes both local ratios equal to 2. The minimum relation height drops from 11 to 2. The degree-2 test finds one genuine hit at the control target, with relay valuation two and reader valuation one. [Pinned character-lattice setup](https://github.com/Samsen879/a303656/blob/73972acbd44aafbdc8daa9b2c16932309bb9c18e/analysis/ajt5_overnight_2026_11_26/TWO_MOVING_CHARACTER_LATTICE.md)

### A sharp bound from one primitive direction

Write \(D(s,t)=\max(|s|,|t|,|s+t|)\). For a primitive vector \(v\), let \(Q\) be the product of the local prime orders whose character congruences \(v\) satisfies, and \(R\) the product of the remaining orders. If \(D_*\) is the minimum nonzero height in the full reader lattice, then
\[
\boxed{\min\!\left(RD(v),\left\lceil Q/D(v)\right\rceil\right)
       \le D_*\le RD(v).}
\]

A lattice vector parallel to \(v\) is an integer multiple of \(v\), and its multiplier must be divisible by \(R\). For a nonparallel lattice vector \(u\), each agreeing prime divides \(\det(v,u)\). Thus \(|\det(v,u)|\ge Q\). The determinant inequality \(|\det(v,u)|\le D(v)D(u)\) follows by maximizing the linear functional on the six vertices of the unit hexagon of \(D\). This proves the bound and gives **exactly** \(D_*=RD(v)\) whenever \(RD(v)^2\le Q\).

In the rooted common-scaling setup, each active relay prime \(p\) exceeds \(h\), since its scale has order \(h\) modulo \(p\). Suppose the direct order-\(h\) ratio has a primitive direction of height at most a fixed \(K\). If every relay agrees, the first polynomial has degree at most \(K\), so there are at most \(K\) relaxed gcd roots. If a relay disagrees, the lower bound gives \(D_*\ge\lceil h/K\rceil\). At a nonzero observation, a relation of height below the reader characteristic loses at most one degree upon substitution. A degree drop can occur only when the two leading degrees coincide, in which case the next coefficient is nonzero.

**A checkable criterion for several readers.** Give each reader a height budget \(K_r\) with \(K_r^2<h\). Its direct congruence has at most one primitive direction up to sign within the budget, since two such directions have determinant divisible by \(h\) and absolute value at most \(K_r^2\). For direction \((s_r,t_r)\), write \(\ell_{p,r}\) for the actual slope satisfying \(3^{U_p}=5^{\ell_{p,r}U_p}\bmod r\). The ray at \(p\) must satisfy
\[
\lambda_p\equiv-\ell_{p,r}s_r/t_r\pmod p.
\]
In the two-axis ordinary setup, short relations for all readers on one family of rays exist exactly when each direct direction exists, the prescriptions agree at every shared relay, and the prescribed ray differs from that relay’s homogeneous repair slope. An incompatible order costs at least \(h\), so there is no other primitive direction within the budget. When the test passes, at most \(\sum_r K_r\) labels hit a nonzero reader. This gives a sublinear loss on a retained set \(S\) whenever \(\sum_r K_r=o(|S|)\). Existence of growing actual \(3,5\) panels satisfying the compatibility conditions remains open here.

### The shared orbit can still require linear height

There is a growing counterfamily for the character model itself. Take prime \(h>3\), a prime \(p>9h\) with \(p\equiv1\bmod h\), and a prime reader \(r\equiv1\bmod hp\). For example, the primes can be obtained as divisors of \(\Phi_h((9h)!)\) and \(\Phi_{hp}(hp)\), respectively. The first divisor exceeds \(9h\), and neither divisor divides its cyclotomic index, so the required orders are exact.

Choose \(\zeta,g\) of orders \(h,p\) modulo \(r\), and \(w\) of order \(h\) modulo \(p\). On the single shared orbit
\[
X(j)=\zeta^j g^{w^j},\qquad Y(j)=\zeta^{2j}g^{3w^j},
\]
a monomial identity valid at every label must satisfy \(s+3t\equiv0\bmod p\) from \(j=0\) and \(s+2t\equiv0\bmod h\) from \(j=1\). The direction \((3,-1)\) has \(Q=p,\ R=h,\ D=3\), so the minimum is **exactly \(3h\)**, even on the true orbit. This is an obstruction to short monomial relations. It gives no lower bound on gcd root counts and uses abstract characters, while the following control uses the actual bases \(3,5\).

### Actual \(3,5\) replay

At \(3011\) the direct ratio is 2 and \(\ell_{43,3011}=25\), so the required ray is \(2\cdot25\equiv7\bmod43\). The homogeneous ray is 41. At the same target \(n=14271990583035\), ray 26 has no relaxed gcd roots despite its larger first degree.

```python
from math import lcm
from sympy import Poly, symbols

h,p,r = 7,43,3011
n0,n = 92767221879,14271990583035
H = lcm(p*p*(p-1), r*(r-1))
def step(m):
    v = H//m
    return v*pow(v,-1,m)

J,U = step(h),step(p*p)
C,D = H,2718933
assert (n-n0)%(12*h*p**3) == 0 and n%(p*p) == p
assert (pow(3,C,p*p)+pow(5,D,p*p))%(p*p) == 0
assert pow(3,J,p*p) == pow(5,2*J,p*p)
assert pow(3,U,p) == pow(5,U,p) == 1 and p*U%(r*(r-1)) == 0
a,b = ((pow(base,U,p*p)-1)//p*pow(base,e,p)%p
       for base,e in ((3,C),(5,D)))
assert (a,b,(-a*pow(b,-1,p))%p) == (41,42,41)

alpha,beta,g = pow(3,J,r),pow(5,2*J,r),pow(3,U,r)
assert (pow(3,C,r),pow(5,D,r)) == (1,1898)
assert alpha != 1 and pow(alpha,h,r) == 1 and beta == pow(alpha,2,r)
assert g != 1 and pow(g,p,r) == 1 and g == pow(5,25*U,r)
assert pow(5,7*U,r) == pow(g,2,r)
assert pow(5,26*U,r) == pow(g,32,r)

x = symbols("x")
poly = lambda f: Poly(f,x,modulus=r)
Y = (n%r-x)*pow(1898,-1,r)
assert n%r == 899 and poly(x*x-Y).monic() == poly((x-2488)*(x-2717))
assert pow(2488,h*p,r) == 1 and pow(2717,h*p,r) != 1
assert pow(2488,p,r) == alpha  # recovers j=1, since p == 1 mod h

# Ray 26 has CRT ratio 247 and minimum height 11.
assert 247%h == 2 and 247%p == 32
assert min(min(54*j%301, -54*j%301) for j in range(1,11)) > 10
assert poly(x**8-Y**11).gcd(poly(1-x**15*Y**17)).degree() == 0

f0,w = pow((a+7*b)%p,-1,p),pow(3,-J,p)
assert (f0,w) == (19,41) and pow(w,h,p) == 1
f = f0*w%p
c,d = C+J+U*f,D+2*J+7*U*f
def rem(m):
    return (n-pow(3,c,m)-pow(5,d,m))%m
assert pow(3,c,r) == 2488 and rem(p*p) == 0
if rem(p**3) == 0:
    c += p*U
assert rem(p**3) in range(p*p,p**3,p*p) and rem(r*r) == r
def Ht(s,t): return max(abs(s),abs(t),abs(s+t))
V=((1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1))
assert max(abs(s*v-t*u) for s,t in V for u,v in V)==1
assert min(Ht(s,t) for s in range(-15,16) for t in range(-15,16)
           if (s or t) and (s+247*t)%301==0)==11
assert min(Ht(s,t) for s in range(-15,16) for t in range(-15,16)
           if (s or t) and (s+2*t)%301==0)==2
print("OK")

```

The relay coefficients scale together for every label. The ray differs from the homogeneous ray, so its forced digit exists throughout, and the \(pU\) correction makes the relay valuation exactly two while preserving the reader test. A sufficiently large lift by a multiple of \(12hp^3r^2\) makes the tested remainders positive. These are finite-panel conclusions.

The multi-reader formula is in the two-moving situation where both direct exponents are nonzero modulo the prime spare order, and the two relay read directions are present. The budget is strictly smaller than each relay prime, so the denominator t in the displayed prescription is a unit for a nonzero short direction. The growing impossibility example is a character model, not a claimed family of actual 3,5 relays. The root bound uses the nonzero-observation polynomial and the injective projection of a true hit to the direct spare coordinate.
