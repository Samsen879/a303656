# Two independent integer parameters give three genuine labels

Fix a positive \(C\equiv0\bmod4\) and positive even \(D\). For any primitive integer vector \(p=(a,b)\) with \(p\equiv(1,3)\bmod30\), choose \(q\) with \(\det(p,q)=1\) by Bézout. Add a suitable multiple of \(p\) to arrange \(q\equiv(0,1)\bmod30\): modulo 30 its second coordinate minus three times the first must already be 1. The multiple can be chosen in a bounded range, starting with a Bézout solution of size \(O(|p|)\).

The unimodular system
\[
 Z\cdot p=81\cdot3^C-|p|^2,\qquad
 Z\cdot q=91\cdot3^C-|q|^2
\]
has a unique integer solution \(Z\). Multiply the Gaussian integers corresponding to \(Z,Z+2p,Z+2q\) by \(1+i\), obtaining \(z_0,z_1,z_2\). If \(n=3^{C+6}+5^D+N(z_0)\), their norms certify the actual labels \((C+6,D),(C+4,D),(C,D)\). Indeed the two increments from the first norm are \(648\cdot3^C,728\cdot3^C\), exactly the differences of the corresponding 3-powers.

The congruences on \(p,q,C,D\) ensure all three residuals are \(2\bmod8\) and \(1\bmod3\), by substituting into the unimodular system. Thus they are positive. Modulo 5 the three pre-multiplication vectors are \((1,0),(3,1),(1,2)\). For the latter two, evaluation at \(i=2\) gives zero while at \(i=-2\) it is nonzero; multiplication by \(1+i\) preserves this. The first transfer therefore shares a Gaussian divisor of norm 2 extracted by gcd with 2. The next shares a divisor of norm 10 extracted by gcd of \(z_1\) with 10: its norm-2 part follows from the odd valuation 1 at 2, and its norm-5 part from the specified evaluation. This shared factor divides the known difference \(z_2-z_1\). No square-cofactor assumption is required; the example below has a nonsquare cofactor at the second transfer.

To count distinct targets, let \(1\le a,b\le L\). There are \(\gg L^2\) primitive vectors in the specified residue class by Möbius inversion, since no prime dividing 30 divides both coordinates. Choose \(3^C\asymp L^2\) and \(5^D\asymp L^6\) on their required progressions. Then \(|Z|=O(L^3)\) by the explicit unimodular inverse, so \(n\asymp L^6\). At a fixed \(n\) the two norms of \(Z,Z+2p\) are fixed, and the two vectors determine \(p\). The bound \(r_2(m)\le4\tau(m)\ll_\varepsilon m^\varepsilon\) bounds the multiplicity by \(L^{o(1)}\). Taking \(L\) a sufficiently small fixed multiple of \(X^{1/6}\) gives \(\gg_\varepsilon X^{1/3-\varepsilon}\) distinct \(n\le X\) at these three ordinary-height labels. Finally \(n\equiv4\bmod8,2\bmod3\) excludes \(n=3^j+5^\ell\): mod 8 would force \(j\) odd and \(\ell\) even, giving 1 mod 3. This count concerns three true representations of constructed targets, not arbitrary \(n\).

```python
from math import gcd, isqrt

A, B = 81*3**4-10, 91*3**4-1
x, y = A-3*B, B
qs = [(x,y), (x+2,y+6), (x,y+2)]
zs = [(a-b,a+b) for a,b in qs]
R = [a*a+b*b for a,b in zs]
n = 3**10+5**4+R[0]

assert n == 592858436
assert all(r == n-3**c-5**4 > 0 and r%8 == 2 and r%3 == 1
           for c,r in zip((10,8,4),R))
assert gcd(R[0],R[1]) == 2 and gcd(R[1],R[2]) == 10
assert all((a+2*b)%5 == 0 and (a-2*b)%5 != 0 for a,b in zs[1:])
assert isqrt(R[1]//10)**2 != R[1]//10
```
