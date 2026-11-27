# True norm pairs in a fixed mod-49 class on two growing axes

On a subgrid with both exponent axes growing, the two unit anchor classes have different **true-norm** means. The blocked class \(r_-\) has zero witnesses from this subgrid. In class \(r_0=0\bmod49\), the mean over genuine anchors is \(\gg\sqrt{\log B}\). The sign for the full grid remains open. Exact rational rescaling can transport only a negligible fraction of the pairs on labels that admit true pairs in both classes.

### A true comparison on two growing axes

Keep even \(a,b\), \(A=3^a\), \(B=5^b\), \(39/40<B/A<122/125\), and
\[
S_0=A+25B,\qquad P=A+125B,\qquad S_3=729A+B,\qquad U=729A+625B.
\]
In \(2S_3-P<n\le U\), use the coarse cell \(n=S_0+45u\). The anchor is genuine exactly when \(u\) is a sum of two squares. In the original steps-\((4,2)\) grid, retain
\[
\mathcal H=\{(x,y):x\equiv a+4\pmod{84},\ y\equiv b+2\pmod{42}\}.
\]
Here the original ranges are \(a/10\le x\le a/3\) and \(b/5\le y\le b/3\). Both axes grow, and \(|\mathcal H|\sim K/441\), where \(K\) is the full grid size.

For \(S_i=3^x+5^y\) in this subgrid, \(k_i=(S_0-S_i)/45\) is a positive multiple of \(8\) and \(k_i\asymp B\). At \(r_-=3^{a+4}+5^{b+2}+7\bmod49\), every \(n-S_i\) has exact \(7\)-valuation one. At \(r_0\), both \(u\) and \(u+k_i\) are units at \(7\). Writing \(\beta\) for the true norm indicator, I obtain
\[
\sum_{i\in\mathcal H}\ \sum_{\substack{u:\ n=S_0+45u\ \text{in the window}\\ n\equiv0\ (49)}}
\beta(u)\beta(u+k_i)
\ \gg\ \frac{B|\mathcal H|}{(\log B)^2}.
\tag{1}
\]
There are \(\asymp B/\sqrt{\log B}\) genuine anchors in each class. Dividing (1) by the anchor count gives the asserted growing mean. Each counted norm gives an ordinary-height witness. Multiplication by \(2+i\), with the coordinates oriented suitably, puts at least \(4/5\) of the remainder into one square, and \(4n/5>S_3\) throughout the window. [Balog–Wooley, Lemma 2.1](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf#page=4)

**Proof of (1).** Fix \(k=k_i\), put \(H=k/4\), and write the two norm vectors as
\[
(w-m,e-d),\qquad (w+m,e+d),\qquad mw+de=H.
\]
Choose their residues modulo \(49\) to represent the prescribed unit residues of \(u,u+k\). Every unit has a representation modulo \(7\) that lifts modulo \(49\). A signed permutation of the second vector makes \(m\) a unit at \(7\).

Let \(X=\sqrt B\) and \(u_*\) be the midpoint of the allowed interval for \(u\). At \(d=e=0\) the real center is \(m_*=(\sqrt{u_*+k}-\sqrt{u_*})/2\asymp X\). Take \(m\) in a fixed sufficiently small interval of radius \(\delta X\) about \(m_*\), and \(d,e\) in \([0,\delta X]\), all in their prescribed classes. Uniformly over the balanced window, these boxes keep \((w-m)^2+(e-d)^2\) inside the allowed interval whenever \(w=(H-de)/m\) is integral. This follows by rescaling by \(X\), since the midpoint has a fixed positive margin and \(m_*/X\) is bounded away from zero.

For each \(m\), count \(de\equiv H\bmod m\) with \(d\) a unit. If \(D,E\) are the two progressions in the boxes, completion gives
\[
\frac{|D||E|\varphi(m)}{m^2}
+O\!\left(m^{1/2}(H,m)^{1/2}\tau(m)^2\log^2(2m)\right).
\]
Indeed the nonconstant Fourier terms are Kloosterman sums \(S(j,\ell H;m)\). For a nonzero frequency the interval Fourier sum weighted by \((j,m)^{1/2}\) is \(O(m\tau(m)\log(2m))\), by grouping frequencies by divisors of \(m\). The progression step \(49\) is invertible modulo \(m\). Discarding \((H,m)>X^{1/4}\) removes at most \(X^{3/4+o(1)}\) moduli by summing over divisors of \(H\). On the remaining moduli the errors sum to \(o(X^2)\). The main terms sum to \(\gg X^2\), using the positive mean of \(\varphi(m)/m\) in a reduced class modulo \(49\), obtained by expanding \(\sum_{d\mid m}\mu(d)/d\). This gives \(\gg B\) distinct ordered representation pairs for each label. [Kloosterman bound, equation (1.4)](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70291)

To count **integers** rather than representations, write \(R(u)=r_2(u)\). The uniform multiplicative-function upper bound for the primitive forms \(u,u+k\) gives, for an absolute \(C\),
\[
\sum_{u\ \text{in the window}} R(u)^2R(u+k)^2
\ll B(\log B)^2 F(k),\qquad
F(k)=\prod_{p\mid k}(1+C/p).
\]
For the application use \(f=(R/4)^2\) in both forms. The interval endpoints, length and coefficient height are all \(O(B)\), with endpoints and length \(\asymp B\). At \(p\nmid 2k\) the two roots are disjoint, so the combined local factor is \(1+(2f(p)-2)/p+O(p^{-2})\). Here \(f(p)=4\) at split primes and \(0\) at inert primes, giving exponent \(2\). At \(p\mid k\), the joint divisibility probability for powers \(p^s,p^t\) is at most \(p^{-\max(s,t)}\), giving a uniform \(1+O(1/p)\) correction. Cauchy–Schwarz now gives \(\gg B/((\log B)^2F(k))\) distinct integers for each label. [De la Bretèche–Tenenbaum, Theorem 3.1](https://arxiv.org/pdf/2403.19320#page=4)

The factor \(F\) costs only a constant in the lower bound after averaging. For fixed \(y\) and \(p\nmid15\), the fraction of \(x\) with \(p\mid k_i\) is \(O(1/\log p+1/a)\). A hit occupies one class modulo \(\operatorname{ord}_p(3^{84})\), and this order is at least \(\log p/(84\log3)\). Summing the resulting bound for the mean of \(\log F(k_i)\) uses \(\sum_p1/(p\log p)<\infty\). Jensen gives a positive lower bound for the mean of \(1/F(k_i)\), proving (1).

### The remaining full-grid comparison

Let \(J_r\) be the allowed \(u\) in class \(r\), and let \(Y\asymp B\) be the interval length before restricting modulo \(49\). In the coarse cell, only \(y\equiv b+2\bmod6\) can contribute. Sum over **all** those labels and write
\[
T_r=\sum_i\sum_{u\in J_r}\beta(u)\beta(u+k_i).
\]
Both anchor denominators equal \(8\kappa Y/(343\sqrt{\log B})\) with relative error \(O(1/\log B)\), where \(\kappa\) is the Landau–Ramanujan constant. Thus a positive leading gap of order \(K/\sqrt{\log B}\) is equivalent to
\[
\liminf \frac{\log B}{YK}(T_0-T_-)>0.
\]
The subgrid proof supplies a positive term in this signed sum. It leaves the contribution of the other labels uncontrolled.

For an exact rescaling between labels \(i,j\), the multiplier has to be \(k_j/k_i\). Since all \(k_i\asymp B\) and \(|k_i-k_j|=O(B^{1/3})\), any multiplier other than \(1\) has reduced denominator \(\gg B^{2/3}\). That denominator must divide the source \(u\), leaving only \(O(KB^{1/3})\) possible source targets per label even with every destination label available. Multiplier \(1\) leaves the target class fixed. On labels for which both remainders are units at \(7\) in both classes, the pair construction above gives \(B/(\log B)^{O(1)}\) genuine source targets in either class. This rules out an injection covering those pairs by exact rational rescaling.

### Exact positive and negative controls

The same label \((812,1086)\) is a true norm at the first target and has exact \(7\)-valuation one at the second. Both targets have genuine anchors. The second also has a true alternative outside the blocked subgrid.

```python
from math import isqrt

a, b = 7864, 5368
A, B = 3**a, 5**b
assert a % 2 == b % 2 == 0 and 39*A < 40*B and 125*B < 122*A
S0, P, S3, U = A+25*B, A+125*B, 729*A+B, 729*A+625*B
lo = 2*S3-P
T = 3**812 + 5**1086
r = (pow(3, a+4, 49) + pow(5, b+2, 49) + 7) % 49
assert (812-a-4) % 84 == (1086-b-2) % 42 == 0

for x, offset, cls in [(812, 2450, 0), (796, 1800, r)]:
    S = 3**x + 5**1086
    k, rem = divmod(S0-S, 45)
    assert rem == k % 8 == 0
    m = (isqrt(B//45) | 1) + offset
    z = (k-m*m-1)//2
    v = isqrt((lo-S0)//45-(z//m)**2)
    v += (z-v) % m
    u = (z-v)//m
    n = S0 + 45*(u*u+v*v)
    assert lo < n <= U and n > T and n % 49 == cls
    for label, p, q in [(S0, u, v), (S, u+m, v+1)]:
        p, q = sorted((3*abs(p), 3*abs(q)), reverse=True)
        X, Y = 2*p+q, p-2*q
        assert n == label+X*X+Y*Y and S3 < label+X*X <= U
    assert (n-T) % 49 == (11 if cls == 0 else 7)
    print(n.bit_length(), n % 49, (n-T) % 49)

# 12475 0 11
# 12475 45 7
```

Independent BigInt replay verified both ordinary-height anchors in the two prescribed classes, the genuine witness on the selected subgrid, the exact 7-adic failure in the other class, and the alternative outside the subgrid. The lower bound applies to actual norm pairs, but it is only at the weaker (log B)^−2 scale before anchor normalization and gives no full-grid signed estimate.
