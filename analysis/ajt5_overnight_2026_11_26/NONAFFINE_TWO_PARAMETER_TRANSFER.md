# Nonaffine two-parameter transfer at three actual labels

This construction preserves three distinct \(3\)-exponents at one \(5\)-exponent, with two different Gaussian gcd signatures. It gives \(\gg_\varepsilon X^{1/4-\varepsilon}\) distinct \(n\le X\) with both exponent sizes growing logarithmically. The earlier one-free-coordinate family gives a larger count. There is no pointwise coverage claim.

Put \(f=3^j\), \(j\ge 5,\ j\equiv1\bmod4\), and take \(D\ge0\) even. Let \(s\equiv1066\bmod1230\), \(t\equiv0\bmod1230f\), and define
\[
 A=s^2-90t^2-180st,\quad B=s^2+90t^2,\quad C=s^2-90t^2+2st,\quad
 w=-st(s+t)(s-90t)/f.
\]
Take \(z_0,z_1,z_2\) to be \(1+i\) times the Gaussian numbers with coordinates \((-A,639f+w),(B,819f+w),(-C,821f+w)\). Direct expansion gives \(A^2+90C^2=91B^2\) and \(A^2-B^2=360fw\), so the two consecutive norm differences are \((3^{12}-3^8)f^2\) and \((3^8-1)f^2\), in increasing norm order. Thus
\[
 n=3^{2j+12}+5^D+N(z_0)
 =3^{2j+8}+5^D+N(z_1)
 =3^{2j}+5^D+N(z_2).
\]

All norms are \(2\bmod8\) by parity, and nonzero modulo \(3\) since \(s\equiv1\bmod3\) while \(t,w,f\equiv0\bmod3\). The difference constants factor as \(2^4 3^8 5\) and \(2^5 5\cdot41\). Modulo \(41\), \(w\equiv0\) and \(819f\not\equiv0\); a sum of two squares modulo \(41\) can vanish without both coordinates vanishing, so for the Gaussian gcd at \(41\) one must also check the common norm condition. In fact \(t\equiv0\bmod41\) gives \(B\equiv C\equiv s^2\equiv0\bmod41\) because \(1066=26\cdot41\). Hence \(N(z_1)\equiv2(819f)^2\ne0\bmod41\). At \(5\), \(f\equiv3\), \(s\equiv1\), \(t,w\equiv0\); evaluation at the two roots \(i=\pm2\) gives opposite orientations for \(z_0,z_1\), and equal orientations for \(z_1,z_2\). Therefore the adjacent integer norm gcds are both \(10\), and the adjacent Gaussian gcd norms are \(2,10\).

The source submap \((s,t)\mapsto(A,w)\) has Jacobian determinant \(-2s^4/f\) at \(t=0\), \(s\ne0\). Both parameters affect the Gaussian coordinates. For the count, take \(s,t\in[L,2L]\), \(f\asymp L^\eta\) with fixed \(0<\eta<1\), and \(5^D\asymp L^8\). The exponential progressions admit these comparisons with fixed constant factors. There are \(\gg L^2/f\) parameter pairs, each \(n\asymp L^8\) with all displayed exponents \(\Theta(\log n)\). For fixed \(n\), the ordered pair \((z_0,z_1)\) has at most \(n^{o(1)}\) possibilities by the two-square representation bound. Each pair fixes \(A,B\); the ratio \(A/B=(r^2-180r-90)/(r^2+90)\) with \(r=s/t\) gives a nonzero quadratic or linear equation, and \(B\) fixes the positive scale. Thus the multiplicity is \(n^{o(1)}\). Taking \(L\) a sufficiently small constant times \(X^{1/8}\) and \(\eta\) sufficiently small proves the stated bound.

**Affine obstruction.** If real affine coordinate maps \(M_i u+b_i\) have pairwise constant squared norm differences as polynomials, their quadratic and linear terms give \(M_i^\top M_i=M_0^\top M_0\) and \(M_i^\top b_i=M_0^\top b_0\). Align the \(M_i\) by orthogonal maps. The constant shifts then differ only in the common image's orthogonal complement; when that image has dimension two, the complement vanishes and the constants must agree. This explains why an affine full-rank two-parameter lift cannot account for a nonzero shift, even though the nonlinear lift above exists.

Exact replay, using signed coordinates (take absolute values for the nonnegative variables):
~~~python
from math import gcd
f, D, s, t = 3**5, 14, 1066, 298890
A = s*s - 90*t*t - 180*s*t
B = s*s + 90*t*t
C = s*s - 90*t*t + 2*s*t
w = -s*(t//f)*(s+t)*(s-90*t)
Z = [(x-y,x+y) for x,y in [(-A,639*f+w),(B,819*f+w),(-C,821*f+w)]]
R = [x*x+y*y for x,y in Z]
n = 3**22 + 5**D + R[0]
assert n == 223842786101342083575997768685616039924
assert all(r == n-3**e-5**D > 0 and r%8 == 2 for e,r in zip((22,18,10),R))
assert gcd(R[0],R[1]) == gcd(R[1],R[2]) == 10
assert [((x+2*y)%5==0,(x-2*y)%5==0) for x,y in Z] == [
    (False,True),(True,False),(True,False)]
~~~
