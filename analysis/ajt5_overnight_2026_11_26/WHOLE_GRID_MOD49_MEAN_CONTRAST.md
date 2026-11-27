# Whole-grid mod-49 mean contrast and the true-anchor compensation threshold

The full steps-\((4,2)\) grid has a strict mean deficit in the blocked mod-\(49\) class **before conditioning on a true anchor**. The deficit also survives in the normalized finite-prime model on genuine anchors, uniformly in the choice of finite panel. For the actual true-anchor count, compensation requires a specific signed two-norm correlation. I did not establish its sign.

### A whole-grid comparison

Take even \(a,b\), \(A=3^a\), \(B=5^b\), and \(39/40<B/A<122/125\). Write
\[
S_0=A+25B,\qquad P=A+125B,\qquad S_3=729A+B,\qquad U=729A+625B.
\]
Use \(2S_3-P<n\le U\) and \(n=S_0+5t\). The grid consists of the \(K\) labels \(S_i=3^x+5^y\) with
\[
a/10\le x\le a/3,\quad x\equiv a\pmod4,\qquad
b/5\le y\le b/3,\quad y\equiv b+2\pmod2.
\]
Let \(\beta\) be the genuine sum-of-two-squares indicator and \(W(n)=\sum_i\beta(n-S_i)\). Compare the two target classes modulo \(49\)
\[
r_0=0,\qquad r_-=3^{a+4}+5^{b+2}+7.
\]
In either class \(t\) is a unit at \(7\). Indeed \(S_0\equiv A+4B\not\equiv0\pmod7\) and \(r_--S_0\equiv3A\pmod7\).

Since **both exponents are even**, the two axes each cycle through \(1,2,4\bmod7\). Their sum has multiplicities \((0,1,1,2,1,2,2)\). Thus every label is a unit at \(7\) in class \(r_0\). In class \(r_-\), let \(\eta=1/9\) if \(r_-\bmod7\) is a square and \(2/9\) otherwise. Then \(\eta+o(1)\) of **all** labels hit \(n-S_i\equiv0\pmod7\). Within each hitting \(y\bmod6\) phase, \(5^6\equiv43\bmod49\) cycles through all seven lifts. Six have exact valuation one. In the seventh, the conditional \(7\)-adic pass probability is \(7/8\). The whole-grid local deficit is therefore \(7\eta/8+o(1)\).

The same calculation works in the coarse cell \(9\mid t\), with **\(\eta=1/9\)** regardless of \(r_-\bmod7\). Here \(y\not\equiv b+2\bmod6\) forces exact valuation one at \(3\) and contributes zero to the actual count. Among the remaining labels, one of the three \(x\) phases hits \(r_-\bmod7\). The denominator is still the original \(K\).

Let \(\bar W_r\) be the uniform target mean in class \(r\), with either choice of coarse conditioning and without the anchor requirement. Write \(t=gu\), where \(g=1\) or \(9\). For each contributing label the test becomes \(\beta(u+(S_0-S_i)/(5g))\). All translated intervals have length and endpoints comparable to \(B\). The fixed-progression sum-of-two-squares asymptotic gives mean \(8\kappa/(7\sqrt{\log B})\) in a unit class modulo \(49\), where \(\kappa\) is the Landau–Ramanujan constant. The mean is zero at exact valuation one. In the zero class modulo \(49\), division by \(49\) gives mean \(\kappa/\sqrt{\log B}\). These estimates are uniform over the labels, so
\[
\boxed{\displaystyle
\bar W_{r_0}-\bar W_{r_-}
=(\kappa\eta+o(1))\,\frac{K}{\sqrt{\log B}}.}
\]
This counts true norms across the entire grid. [Balog–Wooley, Lemma 2.1](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf#page=4)

### What compensation on genuine anchors would require

For the finite-prime model, put \(k=(S_0-S_i)/(5g)\) for a contributing label. At each inert prime \(p\ne7\), normalize the joint local pass probability for \(u,u+k\) by the square of the single pass probability. A single fails with probability \(1/(p+1)\), so the normalized joint factor is at least \(1-p^{-2}\). At \(2\), \(8\mid k\), and \(u\equiv1\bmod4\) alone gives a normalized factor at least \(1\). Split primes contribute \(1\). The product of these common weights is at least \(1/2\), uniformly over labels and finite panels. Thus the normalized whole-grid contrast is at least \(7\eta/16+o(1)\) with the \(7\)-factor left as a raw pass probability. The comparison is label by label and uses no independence of exponent phases.

For the **actual** anchor restriction, let \(\Gamma_r=\operatorname{Cov}_r(\beta(u),W)\) under the same uniform target measure. Since both classes have unit anchor residue, their anchor densities are \(8\kappa/(7\sqrt{\log B})\) with relative error \(O(1/\log B)\). The conditional mean identity gives
\[
\frac{\sqrt{\log B}}{K}
\left(\mathbb E_{r_0}[W\mid\beta(u)=1]
      -\mathbb E_{r_-}[W\mid\beta(u)=1]\right)
=
\kappa\eta+\frac{7}{8\kappa}\frac{\log B}{K}
(\Gamma_{r_0}-\Gamma_{r_-})+o(1).
\]
So cancellation at leading order requires
\[
\Gamma_{r_0}-\Gamma_{r_-}
=-\left(\frac{8\kappa^2\eta}{7}+o(1)\right)\frac{K}{\log B}.
\]
A lower bound strictly above that threshold would suffice. The missing input is the **signed grid average of the two-norm correlation** \(\beta(u)\beta(u+k)\) between these two specified classes. Bounds on the two counts separately do not supply that comparison. The finite-prime contrast gives no conclusion about the total true-anchor variance or near-full matching. [Plaksin on norm pairs](https://www.mathnet.ru/eng/mzm5142), [Kimmel–Kuperberg on true indicators and weighted correlations](https://www.cambridge.org/core/journals/journal-of-the-institute-of-mathematics-of-jussieu/article/positive-density-for-consecutive-runs-of-sums-of-two-squares/05BEA94BD4A0FC3DCE55B113B4540F22)

### Exact same-target replay

On one 12,475-bit target in the blocked class, \(S_0\) and \((796,1086)\) have genuine ordinary-height witnesses. The label \((812,1086)\) fails at exact \(7\)-depth one.

```python
from math import isqrt

a, b = 7864, 5368
A, B = 3**a, 5**b
assert a % 2 == b % 2 == 0 and 39*A < 40*B and 125*B < 122*A
S0, P, S3, U = A+25*B, A+125*B, 729*A+B, 729*A+625*B
r = (pow(3, a+4, 49) + pow(5, b+2, 49) + 7) % 49
R = [(pow(3, a+4*i, 49) + pow(5, b+2+6*j, 49)) % 49
     for i in range(21) for j in range(7)]
assert R.count(r) == 7
assert sum(s % 7 == r % 7 and s != r for s in R) == 42

x, y = 796, 1086
assert a <= 10*x and 3*(x+16) <= a and (x-a) % 4 == 0
assert b <= 5*y and 3*y <= b and (y-b-2) % 42 == 0
S, T = 3**x+5**y, 3**(x+16)+5**y
d = (isqrt(B//45) | 1) + 1800
z = ((S0-S)//45-d*d-1)//2
v = isqrt((2*S3-P-S0)//45-(z//d)**2)
v += (z-v) % d
u = (z-v)//d
n = S0+45*(u*u+v*v)
assert n.bit_length() == 12475 and 2*S3-P < n <= U
assert n % 49 == r == 45 and (n-T) % 49 == 7 and n > T
for label, p, q in [(S0, u, v), (S, u+d, v+1)]:
    p, q = sorted((3*abs(p), 3*abs(q)), reverse=True)
    X, Y = 2*p+q, p-2*q
    assert n == label+X*X+Y*Y and S3 < label+X*X <= U
```

The finite progression split and the same-target control were independently replayed in BigInt: seven exact mod-49 matches, forty-two depth-one failures in the 147 sampled coarse labels, and the two positive norm witnesses. The unanchored result concerns actual norms. The normalized local anchored contrast concerns the finite-prime model only.
