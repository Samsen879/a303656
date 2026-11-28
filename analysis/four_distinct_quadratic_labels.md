# Four distinct exponent labels from an integer quadratic parameter

For every fixed integer \(m\ge1\), the construction below gives
\(\Theta_m(X^{m/(10+4m)})\) distinct generated targets up to \(X\).
At each target the four \(3\)-exponents are pairwise distinct, the four
\(5\)-exponents are pairwise distinct, and all four residuals are positive
sums of two squares. Both exponent axes grow on the order of \(\log n\).

Draft #84 gives the affine three-label family used here. Draft #88
gives four labels at ordinary height, with \(\Theta((\log X)^2)\)
targets and different offsets. The quadratic family was obtained in the
preceding research round. This note independently replays it and gives
a new ordinary-height obstruction for a sublattice of fourth witnesses,
together with an ordinary-height witness outside that sublattice.
[Draft #84](https://github.com/Samsen879/a303656/pull/84) ·
[Draft #88](https://github.com/Samsen879/a303656/pull/88)

## Integer construction

Set \(T=5^U,W=3^V\), where \(1\le V\le U\). The shifts \(s_1,s_2,s_3,s\)
have offset pairs \((c_0,d_0)=(3,2),(7,6),(1,0),(5,1)\), with actual
exponents \((2V+c_0,2U+d_0)\). Define
\[
p=(51T-19W)/6,\quad q=(51T+19W)/6,\quad
w=(p,q),\quad v=(q,-p),\quad G=p^2+q^2,\quad R=(T^2+W^2)/2.
\]
Since \(\gcd(51T,19W)=3\), the integers \(p,q\) are coprime and have
opposite parity. Choose \(z_0=(x_0,y_0)\) with \(z_0\cdot w=R\) by
taking \(x_0=Rp^{-1}\bmod q\) in \([0,q)\) and \(y_0=(R-px_0)/q\).
Write \(L=z_0\cdot v\), \(z=z_0+\tau v\), and \(N(x,y)=x^2+y^2\).

For \(j=-12,-6,12\), respectively, the first three rows have coordinates
\(z+jw\), and \(s_i+2jR+j^2G=C\) by direct expansion, where
\[
C=20821T^2+2903W^2.
\]
Their common target is \(n=C+N(z)\). The fourth row uses \(z-2v+Kw\),
with \(s=5T^2+243W^2\). Its norm agrees with \(n-s\) exactly when
\[
\tau=1+K^2/4+(s-C-4L+2RK)/(4G). \tag{1}
\]
Indeed the norm difference is \(4L+4G\tau-2RK-G(4+K^2)\).

The identity \(18G-361(2R)=2240T^2\) gives \(\gcd(2R,G)=1\).
Any common prime must divide \(2240\) since \(\gcd(T,2R)=1\). The
prime 2 cannot divide odd \(G\), the prime 5 cannot divide \(2R\), and
the prime 7 cannot divide \(2R\) because \(-1\) is a nonsquare modulo 7.
Take the unique even \(k\in[0,2G)\) with \(2Rk\equiv C-s+4L\pmod G\),
and set \(K=k+2Gt\), \(t\in\mathbb Z\). The last numerator of (1) is
divisible by 4 since \(s-C\equiv0\pmod4\) and \(K\) is even. All the
coordinates are integers. In the fourth row the \(t^2\) coefficient is
\(G^2v\), and the \(t\) coefficient has perpendicular component \(2Gw\).
Its image is a parabola.

For the count take \(U=V\), \(T^m\le t\le2T^m\). Uniformly on these
layers \(G\asymp T^2\), \(z_0=O(T)\), \(K\asymp T^2t\), and
\(\tau\asymp K^2\) by (1). Hence \(n\asymp T^{10+4m}\), and the
residuals are positive for all sufficiently large \(U\). Both \(\tau\)
and \(N(z_0+\tau v)=G\tau^2+2L\tau+N(z_0)\) increase on this range
for large \(U\). Each layer gives \(T^m+1\) distinct targets. The
largest complete layer below \(X\) gives the lower bound. Summing layer
sizes up through \(T=O_m(X^{1/(10+4m)})\) gives the upper bound.

## Exact obstruction in the ordinary-height window

For the same first-three strand, enlarge the fourth row to \(z-hv+Kw\)
for arbitrary integers \(h,K\). Fix \(V\ge2\), and define
\(J=2240K+595916\) and \(A=2240h\). Any witness in this step lattice must
satisfy
\[
pJ\equiv qA\pmod G. \tag{2}
\]
This is equivalent to the necessary norm congruence
\(s-C-2hL+2RK\equiv0\pmod G\). To check it, use \(pL\equiv qR\pmod G\)
and expand
\[
P=(51T-19W)((K-20816)T^2+(K-2660)W^2)
    -h(51T+19W)(T^2+W^2).
\]
The raw congruence is \(G\mid P\). Eliminating the \(T^3,T^2W\) terms
using \(18G=2601T^2+361W^2\) gives
\[
2601P\equiv 6W^2(pJ-qA)\pmod G.
\]
The cancelled factors are units. The norm \(G\) is odd, \(17\nmid G\)
by the displayed formula for \(18G\), and \(3\nmid G\) for \(V\ge2\)
by the exact valuation of \(18G\).

Equivalently, (2) is the integrality of the two simultaneous projections
\[
a=(qJ+pA)/G,\quad b=(qA-pJ)/G,\qquad
pa+qb=A,\quad qa-pb=J .
\]
The first congruence implies the second because \(p\) is a unit
modulo \(G\) and \(p^2+q^2=G\). Hence \(J^2+A^2=G(a^2+b^2)\).
As \(J\equiv76\pmod{2240}\), this is a nonzero multiple of \(G\).

Put \(Q=15625T^2\), the largest of the four individual powers for
\(V\le U\). A true fourth row at \(n<5Q\) has
\(\sqrt{G(h^2+K^2)}\le2\sqrt n\), since both \(z\) and the fourth
vector have length at most \(\sqrt n\). Since \(G\ge144T^2\), this gives
\(\sqrt{h^2+K^2}<47\). Thus
\(\sqrt{J^2+A^2}<2240\cdot47+595916=701196\).
For \(U\ge7\), however, \(\sqrt G\ge12\cdot5^7=937500\).
Consequently **for all \(U\ge7,\ 2\le V\le U\), no fourth witness
in the step lattice can have \(Q<n<5Q\)**.

The same test applies to any fixed-offset shift
\(s=\alpha T^2+\beta W^2\). Replace 595916 in \(J\) by
\(2601(\beta-2903)-361(\alpha-20821)\). For fixed offsets and a fixed
ordinary height constant, \(J,A\) would be bounded, so for sufficiently
large \(U\) both must vanish. This forces \(h=0\). The exact norm equation
then reads \(s-C+2RK=-GK^2\). Since \(J=0\) makes its two quadratic
coefficients proportional to those of \(G\), the equation gives
\[
\alpha=20821-K-2601K^2/18,\qquad
\beta=2903-K-361K^2/18.
\]
Integrality forces \(6\mid K\). For \(K=6j\), positivity of \(\alpha\)
leaves \(|j|\le2\). The values \(j=0,1\) give 20821 and 15613, which
are not powers of 5. The values \(j=-2,-1,2\) are the existing three
labels.

### Quantitative height for the quadratic chart

For \(h=2\), the equation \(pa+qb=4480\) becomes
\(51T(a+b)+19W(b-a)=26880\). The sum \(a+b\) cannot vanish because
19 does not divide 26880. For \(U\ge6\) this gives
\(|b-a|\ge T/W\) and \(J^2+4480^2\ge72T^4/W^2\).
Since \(4480^2\le8T^4/W^2\), it follows that \(|J|\ge8T^2/W\).
Also \(4T^2/W\ge4(25/3)^6>595916\). Therefore
\[
|K|\ge T^2/(560W),\qquad n\ge T^{10}/(560^4W^4).
\]
For the second inequality, (1) gives
\(\tau+L/G\ge K^2/4-|K|/288-40\ge K^2/8\) in this range.
Use \(N(z)\ge G(\tau+L/G)^2\) and \(G\ge144T^2\).
This holds for every feasible \(K\) in the fixed \(h=2\) chart,
including the least absolute representative.

## Controls and replay

- At \(U=V=1,t=0\), the target is \(512258746876272177\), with labels
  \((5,4),(9,8),(3,2),(7,3)\). At that same target the crossed label
  \((3,3)\) has a positive residual congruent to 7 modulo 49.
- At \(U=3,V=2,\tau=-5\), the same moving offsets give ordinary-height
  \(n=371992113\). The first three coordinates are
  \((-17350,-8401),(-11146,-1855),(7466,17783)\), and the fourth is
  \((19164,2153)\). The fourth witness lies outside the step lattice.
  The checker also exhausts that lattice at this target using the
  proved \(|h|,|K|<47\) bound and finds no fourth witness.

Run `python scripts/replay_four_distinct_quadratic.py` from the repository
root. The replay uses integer arithmetic and the Python standard
library. It checks the explicit coordinates, uses an exhaustive
first-layer oracle for the quadratic congruence, compares the raw and
reduced congruences, and verifies the ordinary-height controls. The
arithmetic proofs supply the unbounded quantifiers.

Coverage of arbitrary \(n\), an ordinary-height four-label power-law
count, and the Sun conjecture remain open here.
