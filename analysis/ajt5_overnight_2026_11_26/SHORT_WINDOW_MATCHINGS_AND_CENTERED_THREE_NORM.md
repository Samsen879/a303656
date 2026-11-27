# Short-window matchings and a centered three-norm criterion

The published bounds give a **uniform positive fraction in shorter intervals on compatible divisibility progressions**. They also identify a precise sufficient condition for a near-full fraction of true anchors: cancellation of the averaged, centered three-norm correlation. The available bounds control its size but do not give that cancellation. A real \(3\)-adic control shows that cancellation can fail for a thinned exponent grid. [Verified starting point](https://github.com/Samsen879/a303656/commit/aeec904554c9b6b1a13526cde55bc5ce5eacb1eb)

### Unconditional extension to shorter intervals

Keep the balanced ordinary window \(I=(2S_3-P,U]\), with \(A=3^a,\ B=5^b\) and
\[
S_0=A+25B,\qquad P=A+125B,\qquad S_3=729A+B,\qquad U=729A+625B.
\]
Fix any odd sum of two squares \(C\) divisible by \(5\), including \(C=45\). In the lower exponent rectangle from the baseline, $a/10\le x\le a/3$ and $b/5\le y\le b/3$, take
\[
x\equiv a\pmod{\operatorname{lcm}(2,\varphi(C/3^{v_3(C)}))},\qquad
y\equiv b+2\pmod{\operatorname{lcm}(2,\varphi(C/5^{v_5(C)}))}.
\]
For large \(a,b\), the powers of \(3\) vanish on the \(3\)-part of \(C\), and the powers of \(5\) vanish on its \(5\)-part. The other prime powers are preserved by the indicated periods. Thus all labels \(S_i=3^x+5^y\) are \(S_0\bmod C\).

Write \(t=(n-S_0)/C\), \(X=B/C\), and \(h_i=(S_0-S_i)/C\). For **every** interval \((z,z+Y]\) inside the normalized ordinary window with
\[
z^{5/6+\epsilon}<Y\le z,\qquad 0<\epsilon<1/6,
\]
there are \(\gg Y/\sqrt b\) true anchors having a distinct-axis matching of size \(\gg_C b\). This is a positive fraction of the true anchors in that interval.

Here is the range and moment check. The left endpoint satisfies \(z\asymp X\), with \(0<h_i<27X<z\). Plaksin therefore gives the first moment \(\sum \beta(t)W(t)\gg YK/b\), where \(\beta\) is the true norm indicator, \(W(t)=\sum_i\beta(t+h_i)\), and \(K=N_xN_y\). In Henriot’s upper bound one can take \(\alpha=4/5\) and \(\delta=1/8\). The distinct forms are monic, their product has coefficient norm \(O(X^3)\), and \(z^\alpha<Y\le z\). The baseline average of the discriminant factors is unchanged, since it depends on the label differences. Thus, writing \(D(t)=\sum_xW_x(t)^2+\sum_yW_y(t)^2\), the bounds are
\[
\sum\beta(t)W(t)^2\ll \frac{YK^2}{b^{3/2}},
\qquad
\sum\beta(t)D(t)\ll \frac{YK(N_y+\sqrt b)}{b^{3/2}}.
\]
The one-form bound gives \(O(Y/\sqrt b)\) anchors. The first and second moments give the matching lower bound for their number. A maximal matching of size \(m(t)\) covers the successful edges by its endpoints, so \(W(t)^2\le 2m(t)D(t)\). The baseline Cauchy–Schwarz argument now gives the claimed matches with \(Y\) in place of \(X\). Multiplication by a Gaussian integer of norm \(C/5\), followed by the \(2+i\) projection, puts each witness in the ordinary height window. For any positive integer $m$, the norm criterion at inert primes shows $\beta(Cm)=\beta(m)$, since $C$ has even valuation at every inert prime. The factor $C/5$ is also a norm. This proves a gap bound of order \(C X^{5/6+\epsilon}\) between successful targets on the compatible progression. [Plaksin, theorem on p. 145](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=rus&paperid=5142&wshow=paper) · [Henriot, Corollary 2](https://arxiv.org/pdf/1102.1643#page=7) · [Erratum](https://doi.org/10.1017/S0305004114000280)

### The precise near-full criterion

In one such interval, let \(M\) count true anchors. Let \(M_i\) count those also passing label \(i\), and \(M_{ij}\) those passing both \(i,j\). Define the signed sum
\[
\mathcal D=\sum_{i\ne j}\left(M_{ij}-\frac{M_iM_j}{M}\right).
\]
The mean \(\mu=M^{-1}\sum_iM_i\) is \(\asymp K/\sqrt b\). On the true anchors, the exact identity is
\[
\sum (W-\mu)^2=\mathcal D+\sum_i M_i(1-M_i/M).
\]
The diagonal is \(O(MK/\sqrt b)\). Thus for any \(\omega\ge1\), all but a fraction
\[
O\!\left(\frac{b\,\max(\mathcal D,0)}{MK^2}
        +\frac{\sqrt b}{K}+\frac1\omega\right)
\]
have matching size \(\gg K/[\omega(N_y+\sqrt b)]\). This follows from Chebyshev for \(W\), Markov for \(D(t)\), and the matching inequality above. In particular, \(\max(\mathcal D,0)=o(MK^2/b)\) would give growing matchings on \(1-o(1)\) of the genuine anchors by taking \(\omega\) to grow slowly. The same identity works after partitioning the anchors into local classes and centering within each class, provided the class means are large for all but \(o(M)\) anchors.

This criterion needs an averaged one-sided estimate, which is weaker than a pointwise shifted-norm asymptotic. Plaksin and Henriot alone give \(O(MK^2/b)\) for the second moment. They do not estimate the subtraction in \(\mathcal D\).

### Real obstruction and replay

For \(C=5\), thin the \(y\)-axis to \(y\equiv b+4\bmod6\). On genuine anchors with \(9\mid t\), every label in that phase has exact \(v_3(n-S)=1\), since \(3^x\equiv0\bmod9\) and \(5^{b+4}-5^{b+2}\) has depth one. In a full macroscopic window these are \(1/9+o(1)\) of the true anchors, by \(\beta(9u)=\beta(u)\) and Landau–Ramanujan. The thinned grid still has mean \(\asymp K/\sqrt b\) by Plaksin, so its variance is bounded below by a constant times \(K^2/b\). This is an actual covariance obstruction for that phase. The compatible \(C=45\) grid uses \(y\equiv b+2\bmod6\). [Landau–Ramanujan count](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf)

The replay constructs one ordinary true anchor on the \(C=45\) progression. At that **same integer**, two alternatives form a distinct-axis pair close to the top of the exponent range, not in the inner counting rectangle, while the wrong phase has the inert obstruction.

```python
a,b = 574422,392104
A,B = 3**a,5**b
S0,P,S3,U = A+25*B,A+125*B,729*A+B,729*A+625*B
assert 39*A < 40*B and 125*B < 122*A

u,v,r,s = 263175,256465,224385434475,222300473751
assert 1+u*u == 3**20+v*v and 1+r*r == 5**30+s*s
L,M = 3**((a-20)//2),5**((b-28)//2)
n = (1+u*u)*L*L + (1+r*r)*M*M
assert 2*S3-P < n <= U and (n-S0)%45 == 0

for x,p in ((a,v*L),(a-20,u*L)):
    for y,q in ((b+2,s*M),(b-28,r*M)):
        S = 3**x+5**y
        assert (n-S)%45 == 0 and n-S == p*p+q*q
        assert S3 < S+q*q <= n

x = (a+9)//10
x += (a-x)%4
y = (b+4)//5
y += (b+4-y)%6
for i in (x,x+4):
    for j in (y,y+6):
        assert (n-3**i-5**j)%9 in (3,6)
```

The near-full question for the compatible full grid remains open in this argument. The short-window result and the \(3\)-adic obstruction both condition on genuine anchor norms.

Independent exact replay used BigInt (target bit length 910448); the positive and wrong-phase assertions both pass. The short-window theorem concerns an asymptotic count, separate from the finite control above.
