# Two original coordinate gates in the moving square-modulus slice

Retain the middle band of [the square-modulus sieve](SQUARE_MODULUS_DIRECTION_SIEVE.md), and assume \(\gcd(h,k)=1\). In particular \(h\in[H/16,H/15]\), \(k\in[B/8,B/7]\), \(m=p^2\in[H/10,H]\), \(p\nmid2qhk\), and \(q=1\) or \(5\). Write \(j=2qh+mu,\ \ell=2qk+mv\), \(\alpha=j/(qh)\), \(\beta=\ell/(qk)\), and \(P=h^2+k^2,\ J=j^2+\ell^2\). Use the original shift differences \(\delta=S_0-S_1,\ \gamma=S_0-S_2\) and put \(x=\delta-P,\ y=q^2\gamma-J\).

Provided \(2\mid x,\ 2q\mid y,\ m\mid 2P-\gamma+2\delta\), the original norm difference equations are equivalent to
\[
 -ha+kb=x/2,\qquad -ua+vb=(y-2q^2x)/(2qm),
\]
with both right sides integral. The second assertion follows from \(J\equiv4q^2P\bmod m\) and \(\gcd(m,2q)=1\). Parameterize the first line from any integer solution by \((a,b)=(a_1,b_1)+(k,h)\theta\). The reduced denominator of \(\theta\) divides \(E=ku-hv\). If \(b\) is integral, it also divides \(h\), hence divides \(\gcd(h,u)\). Thus \(b\) integral suffices when \(q=1\), since \(0<|u|=q(2-\alpha)h/m\le5q/4\). When \(q=5\), the remaining denominator is \(1,3\), or \(5\): \(h,k\) are odd by \(2\mid x\), even shift differences, and primitivity.

At \(X=2^{58}, C=69/40,\ q=5,\ p=11\), the following directions in the middle band show denominator three. The conclusion is about the original first two coordinates, before any additional rotation-lattice restriction.

~~~python
from fractions import Fraction as Q
from math import gcd
q,h,k,j,l,m = 5,39,75871,27,58241,121
S = [3**10+5**2,3**12+5**2,3**12+5**3]
delta,gamma = S[0]-S[1], S[0]-S[2]
P,J = h*h+k*k, j*j+l*l
x,y,D = delta-P, q*q*gamma-J, k*j-h*l
assert gcd(h,k)==1 and (2*q*h*k)%11 and D
assert (j-2*q*h)%m == (l-2*q*k)%m == 0
assert x%2 == y%(2*q) == (2*P-gamma+2*delta)%m == 0
a,b = Q(q*l*x-k*y,2*q*D), Q(q*j*x-h*y,2*q*D)
assert (a,b) == (Q(1908877144,3),289135)
~~~

## Necessary common rounding at growing shifts

Suppose the three true \(3\)-powers lie in \([X^{1/4},X^{1/3}]\), the \(5\)-powers are at most \(X^{1/8}\), and not all \(3\)-indices are equal. Write \(T=\max_i 3^{c_i}, U=T+X^{1/8}\). Assume \(H>2048U,\ B>1024U,\ T\ge432X^{1/8}\). Let \((a_*,b_*)\) be the rational solution with both shift differences zero. The exact corrections are
\[
 a-a_*=\frac{\gamma-\beta\delta}{2h(\beta-\alpha)},\qquad
 b-b_*=\frac{\gamma-\alpha\delta}{2k(\beta-\alpha)}.
\]
Each has size \(<1/2\) from the band and height assumptions, so a true point uses the unique nearest integers. Outside \((c_0,c_1,c_2)=(c,c+2,c+1)\), the two corrections have the same nonzero sign, and their scaled absolute sizes \(h|a-a_*|,\ k|b-b_*|\) lie between \(T/24\) and \(64U\). To see this, a ratio of the two pure \(3\)-power differences in \((0,1)\), with \(c_0\) minimal, is \((3^g-1)/(3^{g+d}-1)\). It is \(<1/9\) for \(d\ge2\), at least \(4/13\) for \(d=1,g\ge2\), and \(1/4\) in the exception. With \(c_0\) maximal the ratio is at least \(2/3\); other cases have zero or opposite-sign differences or a ratio at least one. The middle band \([1/8,7/25]\) is separated in every nonexceptional case. The pure difference \(\gamma_3-\tau\delta_3\) has size at least \(T/108\) uniformly there; the \(5\)-power contribution is less than \(2X^{1/8}\). The correction formulas give the two bounds. This is a necessary sign and integrality test, not a construction of unbounded hits.
