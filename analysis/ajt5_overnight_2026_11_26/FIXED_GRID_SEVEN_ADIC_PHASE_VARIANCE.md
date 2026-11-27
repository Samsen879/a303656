# Mod-7 phase variance on the original fixed-stride grid

On the original \(C=5\) grid with steps \(4,2\) and even balanced exponents \(a,b\), **\(7\) gives a nonzero local variance after any fixed residue panel away from \(7\)**. It also gives a positive-order variance for an actual true-norm phase count after conditioning on \(t\bmod9\). The variance of the **total** true-norm count remains unresolved. Other phases could compensate for the loss in that bin.

### Exact local variance on the full grid

Let \(t=(n-S_0)/5\), condition on \(t\) being a genuine sum of two squares, and let \(K\) be the number of labels in the unchanged lower rectangle. Let \(V_7(n)\) be the fraction of those labels for which \(v_7(n-3^x-5^y)\) is even.

Both \(3^x\) and \(5^y\) traverse \(\{1,2,4\}\) modulo \(7\) on the original exponent steps. Among the nine ordered pairs, their sums hit \(0\) zero times, each nonzero square once, and each nonsquare twice. Also \(v_7(5^6-1)=1\), so the \(y\)-cycle lifts uniformly inside each root phase. Conditional on a root modulo \(7\), odd depth has limiting frequency \(7/8\). Truncation at any fixed power of \(7\), followed by increasing that power, makes this calculation uniform in \(n\). Thus
\[
V_7(n)=
\begin{cases}
1+o(1),& n\equiv0\pmod7,\\
65/72+o(1),& n\bmod7\text{ is a nonzero square},\\
29/36+o(1),& n\bmod7\text{ is a nonsquare}.
\end{cases}
\]

On genuine anchors, \(t\equiv0\bmod7\) has limiting mass \(1/49\), since it requires \(49\mid t\) and division by \(49\) preserves normhood. Each unit residue has mass \(8/49\). These masses persist in each positive-mass fixed residue cell with modulus coprime to \(7\). To apply the progression count to a nonunit cell, first fix the valuations at primes dividing the panel modulus, divide out those factors, and count reduced residue classes. The discarded valuation tails tend to zero. [Balog–Wooley, Lemma 2.1](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf#page=4)

Since \(S_0\not\equiv0\bmod7\), the resulting conditional variance of \(V_7\) is \(41/7938+o(1)\) when \(S_0\) is a square modulo \(7\), and \(143/31752+o(1)\) otherwise. Thus exponent equidistribution does not eliminate this finite-prime contribution. These constants describe the local test, not the full true-norm count.

### An actual covariance direction within the original grid

In the \(t\bmod9\) panel take the cell \(9\mid t\). Within the full grid, observe the phase bin
\[
\mathcal B:\qquad x\equiv a+4\pmod{84},\qquad y\equiv b+2\pmod{42}.
\]
It contains \((1/441+o(1))K\) labels. Every label in it is \(S_0\bmod45\) and has the same residue \(\sigma=3^{a+4}+5^{b+2}\bmod49\). Also \(\sigma\not\equiv S_0\bmod7\).

Let \(Z\) count **true** alternative norms in this bin. In the cell \(9\mid t\), divide the anchor and each bin remainder by \(45\). Plaksin’s pair lower bound applies to each positive shift \((S_0-S_i)/45\), which is below the left endpoint of the normalized macroscopic interval. It gives \(\mathbb E[Z\mid9\mid t]\gg K/\sqrt b\). On the subclass \(n\equiv\sigma+7\bmod49\), every bin remainder has exact \(v_7=1\), so \(Z=0\). This subclass has limiting mass \(8/343\) among the genuine anchors in the cell, since it specifies a unit residue of \(t/9\bmod49\). Consequently
\[
\operatorname{Var}(Z\mid9\mid t)\gg K^2/b .
\]
The diagonal is at most \(K\), so this is a positive-order centered three-norm sum in an actual phase direction. The grid and its strides remain fixed throughout. [Plaksin, theorem on p. 145](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=rus&paperid=5142&wshow=paper)

For the full true count \(W\) to have variance \(o(K^2/b)\) in this cell, the mean of \(W-Z\) on the blocked subclass must exceed its mean on the whole cell by \(\mathbb E[Z\mid9\mid t]+o(K/\sqrt b)\). That is the compensation still to be checked. The bin variance does not imply failure of near-full matching.

### Standalone replay

This constructs one ordinary true anchor. At that same integer, \((796,1086)\) gives a true alternative and \((812,1086)\) is blocked at exact depth one at \(7\). Both belong to the original \(4,2\) grid.

```python
from math import isqrt

a,b = 7864,5368
A,B = 3**a,5**b
assert 39*A < 40*B and 125*B < 122*A
S0,P,S3,U = A+25*B,A+125*B,729*A+B,729*A+625*B
S,T = 3**796+5**1086,3**812+5**1086
assert (796-a)%4 == (812-a)%4 == (1086-b-2)%2 == 0
assert (812-a-4)%84 == (1086-b-2)%42 == 0
assert (S0-S)%45 == (S0-T)%45 == 0

h = (S0-S)//45
d = (isqrt(B//45)|1)+1800
assert (h-d*d-1)%2 == 0
z = (h-d*d-1)//2
v0 = isqrt((2*S3-P-S0)//45-(z//d)**2)
v = v0+(z-v0)%d
u = (z-v)//d
n = S0+45*(u*u+v*v)
assert 2*S3-P < n <= U and (n-S0)%45 == 0
assert (n-T)%49 == 7 and (n-S0)%7 != 0

for label,r,s in [(S0,u,v),(S,u+d,v+1)]:
    r,s = sorted((3*abs(r),3*abs(s)), reverse=True)
    p,q = 2*r+s,r-2*s
    assert n-label == p*p+q*q and S3 < label+p*p <= n
```

Independent BigInt replay checked the two exact local variance fractions and the 12475-bit same-target positive and blocked controls. Even a,b are explicit in this statement; other parity patterns use different mod-7 phase counts. The local calculation and variance of one true-norm bin do not provide a lower bound on the variance of the full true-norm count.
