# Curve completion lifts the growing-determinant count to exponent \(3/8\)

For every \(\epsilon>0\) the same three exact labels and Gaussian gcd norms \(2,10\) as in [the growing-determinant construction](NONUNIT_DETERMINANT_GCD_FAMILY.md) occur for \(\gg_\epsilon X^{3/8-\epsilon}\) distinct integers \(n\le X\), with labels fixed within each height batch. This is still a sparse family.

Retain that construction's \(M,f,A,B,p,q,Z\). Take squarefree \(h\asymp L^\eta,\ h\equiv1\bmod M\), with all prime divisors \(>200\), and fix \(a\in[L,2L)\) in its required class, prime to \(h\). Vary \(b,c\in[L,2L)\) in their prescribed classes modulo \(M\). The two directions must satisfy \(bc\equiv-h\bmod a\) and the Cramer congruence modulo \(h\), with \(t=c/a\bmod h\).

At each \(\ell\mid h\), the second condition is the open double cover
\[
 b^2=\frac{B-At-\alpha^2t(t-1/2)}{t(t-1/2)},\qquad \alpha=a\bmod\ell,\quad t\ne0,1/2 .
\]
Both denominator roots are genuine simple poles on the \(t\)-line: \(B=66430f^2\) and \(B-A/2=820f^2\) are units at these primes. The numerator has degree two, giving at most four branch points on the line; the smooth normalized cover is geometrically connected, of genus at most one. A nonzero frequency pair gives the additive phase \(rb+s\alpha t\). If \(r\ne0\), \(b\) has a simple pole over each denominator root (ramification there doubles the order of the pole of \(b^2\)), while \(t\) is regular. If \(r=0,\ s\ne0\), \(t\) has a simple pole above infinity, which is unramified since the quotient tends to \(-\alpha^2\ne0\). Thus the phase cannot be of Artin–Schreier type. [Bombieri's curve estimate, Theorem 5](https://www.mathnet.ru/php/archive.phtml?jrnid=mat&option_lang=eng&paperid=462&wshow=paper) gives \(O(\sqrt\ell)\), including the bounded correction for removed points. Zero frequency has \(\ell+O(\sqrt\ell)\) points by the genus bound; an absolute Hasse error at most \(2\sqrt\ell\) plus bounded removed or singular-fiber corrections (at most eight) gives a positive constant multiple of \(\ell\) for every \(\ell>200\).

Complete simultaneously modulo \(Q=ah\), using CRT. The complete sum factors into the modulus-\(a\) Kloosterman sum and these local curve sums. For nonzero global frequency pairs their product is bounded by \(Q^{1/2+o(1)}\sqrt{\gcd(r,s,Q)}\): the local double-zero factors are bounded by \(\ell+O(\sqrt\ell)\), and their extra square roots are exactly those in the gcd weight. The global double-zero value is \(\varphi(a)h^{1+o(1)}\). The geometric-series Fourier bounds recorded in the previous construction apply since the progression step \(M\) is prime to \(Q\), including the single-zero frequencies. Hence the main term is \(L^{1-o(1)}/h\), against error \((Lh)^{1/2+o(1)}\), and wins for fixed \(\eta<1/3\).

There are \(\asymp L^\eta\) admissible \(h\), by the elementary squarefree density in a fixed class with finitely many primes excluded, and each admits \(L^{1-o(1)}\) such \(a\). Summation gives \(L^{2-o(1)}\) direction pairs. The previous height and multiplicity arguments then give \(X^{1/(3-\eta)-o(1)}\) distinct \(n\le X\). Taking fixed \(\eta\) sufficiently close to \(1/3\) gives the claim. No cancellation across different complete moduli has been used.

Composite-modulus control (for integrality, not for the asymptotic size window):

~~~python
from math import gcd
a,b,h,c,d = 39361,1,1436641,80534631458054,2046051495
M,f,D = 19680,3**9,20
assert a*d-b*c == h == 883*1627 and gcd(a,h) == 1
assert (a%M,b%M,c%M,d%M,h%M) == (1,1,614,615,1)
A,B = 131220*f*f-(a*a+b*b)//2,66430*f*f-c*c-d*d
x,r = divmod(d*A-b*B,h)
y,s = divmod(a*B-c*A,h)
assert r == s == 0
R = [2*(u*u+v*v) for u,v in [(x,y),(x+a,y+b),(x+2*c,y+2*d)]]
n = 3**30 + 5**D + R[0]
assert n == 63155381446286131299711353354228891459245478211535724
assert all(n-3**e-5**D == r > 0 for e,r in zip((30,26,18),R))
assert gcd(R[0],R[1]) == gcd(R[1],R[2]) == 10
~~~
