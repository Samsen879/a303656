# An optimal-order Gaussian-sieved true-pair lower bound in a fixed mod-49 class

The bilinear parametrization gives an unconditional **\(\gg B/\log B\) lower bound for each admissible label** in either specified residue class. The constant is uniform in the label. The sieve removes one Gaussian prime above each small split rational prime. Summing over the common divisors of the two half-difference coordinates removes the loss at primes dividing the shift.

### Consequence for the actual grid

Keep even \(a,b\), \(A=3^a\), \(B=5^b\), \(39/40<B/A<122/125\), and set
\[
S_0=A+25B,\quad P=A+125B,\quad S_3=729A+B,\quad U=729A+625B.
\]
Use \(2S_3-P<n\le U\) and \(n=S_0+45u\). On the original steps-\((4,2)\) grid, with \(a/10\le x\le a/3\) and \(b/5\le y\le b/3\), take any label \(S=3^x+5^y\) with \(y\equiv b+2\pmod6\). Then \(k=(S_0-S)/45\) is a positive multiple of \(8\), with \(k\asymp B\).

Fix a target residue \(r\bmod49\) for which \(u\) is a unit at \(7\) and \(u+k\bmod49\) is either a unit or zero. For every sufficiently large balanced pair \((a,b)\), there are \(\gg B/\log B\) **distinct** targets in that class and window for which both \(u\) and \(u+k\) are sums of two squares. The corresponding remainders \(45u,45(u+k)\) have ordinary-height witnesses. Multiplication by \(2+i\), with suitable coordinate signs, puts at least \(4/5\) of the remainder into one square, and \(4n/5>S_3\) in this window.

In particular, put \(r_0=0\) and \(r_-=3^{a+4}+5^{b+2}+7\bmod49\). The subgrid with \(y\equiv b+2\bmod6\) and
\[
S\equiv r_-\pmod7,\qquad S\not\equiv r_-\pmod{49}
\]
occupies **42 of the 441 phase cells** of the original grid. There are seven hitting \(x\bmod84\) phases. In each, \(5^6\equiv43\bmod49\) cycles through seven lifts, six of which give exact \(7\)-valuation one. This whole subgrid contributes zero in \(r_-\) and has true-anchor mean \(\gg K/\sqrt{\log B}\) in \(r_0\), where \(K\) is the full grid size. The signed contribution from the other cells remains undetermined. [Anchor denominator: Balog–Wooley, Lemma 2.1](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf#page=4)

### Proof of the lower bound

Write \(X=\sqrt B\), \(H=k/4\), and use Gaussian coordinates
\[
Z_\pm=(w\pm gm)+i(e\pm gd),\qquad mw+de=H/g,\qquad (m,d)=1.
\]
Here \(g\mid H\) is the common divisor of the two original half-difference coordinates. The norm difference is exactly \(k\). Fix residues of the original coordinates modulo \(49\) that realize the two prescribed norms. Units lift from modulo \(7\), and zero is represented by \((0,0)\). A signed permutation of the anchor vector makes \(gm\) a unit modulo \(7\). All \(g\) used below are coprime to \(49\).

Let \(u_*\) be the midpoint of the allowed \(u\)-interval. Center \(gm\) at \((\sqrt{u_*+k}-\sqrt{u_*})/2\) and \(gd,e\) at zero. Boxes of a sufficiently small fixed width \(\delta X\) keep \(N(Z_-)\) inside the window. This follows uniformly by scaling the coordinates by \(X\): the midpoint has a fixed positive margin, and the center of \(gm/X\) is bounded away from zero. In the normalized coordinates the \(m,d\) box widths are \(\asymp X/g\), and the width for \(e\) is \(\asymp X\).

**Distribution in the sieve moduli.** For squarefree \(\ell\le X^{1/20}\) supported on split primes, complete each compatible residue tuple modulo \(q=49\ell\). For fixed \(m\), put \(h=(m,\ell)\). The required equation for the two box coordinates is
\[
de\equiv H/g-mw_0\pmod{mh}.
\]
The extra factor \(h\) is needed to fix \(w\bmod h\). Since \(q/h\) is coprime to \(m\), the equation modulo \(q/h\) already fixes the other part of \(w\bmod q\). At zero frequency, the admissible \(d\) residues modulo \(mh\) are precisely the units over the fixed unit class modulo \(h\), of size \(\varphi(mh)/\varphi(h)\); each determines the \(e\) progression residue modulo \(m\).

For the progressions \(D,E\) of box values, completion gives main term \(|D||E|\varphi(mh)/(m^2\varphi(h))\). To see the error bound, complete in the quotient coordinates modulo \(m\), where the progression step \(q/h\) is invertible. The restriction \(d\equiv d_0\bmod h\) averages Kloosterman sums with frequencies \(j+tm\) and \(l(H/g-mw_0)\). Their common gcd with \(mh\) is at most \(h(m,H/g)(m,j,l)\). The weighted nonzero interval Fourier sums are \(m^{1+o(1)}\), by grouping frequencies by divisors of \(m\). The zero frequency for the longer interval is \(O(gm)\). Thus the error for fixed \(m\) is \(O(hg\sqrt{m(m,H/g)}\,X^{o(1)})\). Summing over \(m\asymp X/g\) uses \(\sum_{m\le L}\sqrt{(m,H/g)}\le L\tau(H/g)\). [Classical Kloosterman bound, equation (1.4)](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70291)

In the main term, \(\varphi(mh)/\varphi(h)=h\varphi(m)/\varphi(h)\). The prefactor \(h/\varphi(h)\) cancels the prime factors of \(\varphi(m)/m\) at primes shared with \(q\). Expanding the remaining \(\varphi(m)/m\) by divisors and summing \(1/m\) in the specified progression gives density \(q^{-1}\prod_{p\nmid q}(1-p^{-2})\) against \(dm/m\), with error \(O(g\log X/X)\). Consequently the main term is uniform on the primitive local tuples
\[
mw+de=H/g,\qquad (m,d)\ne(0,0)\pmod p.
\]
There are \(p(p^2-1)\) such tuples at \(p\). For any prescribed local bad sets of fractions \(\rho_g(p)\), the count bad at every \(p\mid\ell\) is therefore
\[
\frac{Y_1}{g}\prod_{p\mid\ell}\rho_g(p)
+O\!\left(\ell^4 X^{3/2+o(1)}\right),\qquad Y_1\asymp X^2.
\]
The error includes the at most \(\ell^3\) residue tuples and is uniform for \(g\le X^{1/20}\).

**Sieve and common-divisor sum.** At each split prime \(p<z\), choose \(j^2=-1\bmod p\) and forbid \(w+je\pm g(m+jd)=0\bmod p\) for either sign. Counting on the primitive local tuples gives
\[
\rho_g(p)=
\begin{cases}
(2+\mathbf1_{p\mid H})/(p+1),&p\nmid g,\\
(1+\mathbf1_{p\mid H/g})/(p+1),&p\mid g.
\end{cases}
\]
On the \(p-1\) exceptional rows \(d=jm\), the value \(w+je\) is fixed and \(m+jd=0\). On every other row it ranges freely. This gives both formulas. The bound \(\rho_g(p)\le3/(p+1)\) gives a uniform dimension-\(3\) hypothesis for the fundamental lemma. Use level \(X^{1/20}\) and \(z=X^{1/(20s)}\) for a sufficiently large fixed \(s\). The summed errors, even over all \(g\mid H\) used here, are \(X^{7/4+o(1)}\). [Fundamental lemma, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

Sum \(g^{-1}\prod_{p<z}(1-\rho_g(p))\) over squarefree \(g\) built from split primes \(p<z\) dividing \(H\). At a prime of exact depth one in \(H\), adding the \(p\mid g\) term restores the factor \((p-1)/(p+1)\). At higher depth it restores that factor times \(1-1/[p(p-1)]\). Thus the sum is \(\asymp1/\log z\), uniformly in \(H\). The normalized weights include each prime with probability at most \(2/p\), so their mean \(\log g\) is \(O(\log\log(3H))\). Restricting to \(g\le X^{1/20}\) retains \(1-o(1)\) of the mass. The sieve therefore leaves \(\gg B/\log B\) ordered representation pairs.

Finally, unique factorization in \(\mathbb Z[i]\) bounds their multiplicity per target by a constant. For \(p<z\) all the split-prime exponent must go to the allowed conjugate. Primes \(p\ge z\) have bounded total exponent because both norms are \(O(B)\) and \(z\) is a fixed power of \(B\). Each pair determines \(g\) from its half-difference, so the common-divisor sum introduces no duplicates.

### Exact replay

The first target represents the blocked label \((1064,1086)\) in \(r_0\), using \(g=5\) and the extra lift at \(5\mid m\). The second has a genuine anchor and a true alternative, but the same blocked label has exact \(7\)-depth one.

```python
from itertools import product
from math import isqrt

for p, j in [(5, 2), (13, 5)]:
    for g, h, count in [(1, 1, 2), (1, 0, 3), (0, 1, 1), (0, 0, 2)]:
        V = [(m,d,w,e) for m,d,w,e in product(range(p), repeat=4)
             if (m or d) and (m*w+d*e-h) % p == 0]
        bad = sum(any((w+j*e+s*g*(m+j*d)) % p == 0 for s in [-1, 1])
                  for m,d,w,e in V)
        assert len(V) == p*(p*p-1) and (p+1)*bad == count*len(V)

a,b = 7864,5368
A,B = 3**a,5**b
assert a%2 == b%2 == 0 and 39*A < 40*B and 125*B < 122*A
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
mid = ((lo-S0)//45+(hi-S0)//45)//2
T = 3**1064+5**1086
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert (1064-a-4)%84 == (1086-b-2)%42 == 0

for x,g,offset,t,cls in [(1064,5,35,0,0),(796,1,32,2,r)]:
    S = 3**x+5**1086
    k,rem = divmod(S0-S,45)
    assert rem == k%8 == 0
    H = k//4
    m = (isqrt(mid+k)-isqrt(mid))//(2*g)+offset
    w,e = divmod(H//g,m)
    w,e = w-t,e+m*t
    pairs = [(w-g*m,e-g),(w+g*m,e+g)]
    n = S0+45*sum(z*z for z in pairs[0])
    assert lo < n <= hi and n > T and n%49 == cls
    for label,(v,z) in zip((S0,S),pairs):
        assert all((v+j*z)%p for p,j in [(5,2),(13,5)])
        v,z = sorted((3*abs(v),3*abs(z)),reverse=True)
        X,Y = 2*v+z,v-2*z
        assert n == label+X*X+Y*Y and S3 < label+X*X <= hi
    if g == 5:
        assert H%25 == 0 and H%125 and m%25 == 5 and w%5 == 1
        assert (e-H//g+m*(w%5))%(5*m) == 0
        assert (e-H//g)%(5*m) != 0
    assert (n-T)%49 == (11 if cls == 0 else 7)
```

Independent BigInt replay verified the complete local tuple counts at 5 and 13 and the two ordinary target controls, including the necessity of the extra shared-modulus lift. The count is a lower bound in each admissible progression, not a signed two-norm comparison for the full grid.
