# Residual covariance outside a prescribed panel on engineered strides

**A fixed low-prime panel can leave covariance of order \(K^2/b\) in the actual norm count.** For any prescribed finite residue panel, I can construct a compatible full \(3,5\) grid on which an inert prime outside the panel depresses the conditional mean number of true alternatives by a fixed factor. This gives a residual variance after centering on the panel. It concerns a family of compatible grids with chosen strides. The result for the original fixed strides remains separate.

### A residual outside any fixed panel

Let \(M_0\) encode the low-prime residues to be conditioned on, and put \(D=M_0^2\). Choose a sufficiently large inert prime \(p\) with \(p\nmid 30D\varphi(D)\). Set
\[
s=\min\{v_p(3^{p-1}-1),v_p(5^{p-1}-1)\},
\qquad \nu\in\{0,1\},\quad k=s+\nu\ \text{odd}.
\]
Choose a split prime \(q\) with \(p-1\mid q-1\) and \(v_p(q-1)=\nu\). Linnik gives such a \(q=p^{O(1)}\) by taking \(q\equiv1\bmod\operatorname{lcm}(4,p-1)\) and \(q\equiv1+p^\nu\bmod p^{\nu+1}\). This choice works at either parity of the initial lifting depth. [Linnik’s theorem](https://arxiv.org/abs/0906.2749)

Use \(C=5q\) and choose the full lower exponent rectangle with
\[
x\equiv a\pmod H,\qquad y\equiv b+2\pmod J,
\]
where
\[
H=\operatorname{lcm}\bigl(2,\varphi(CD/3^{v_3(CD)})\bigr),\qquad
J=\operatorname{lcm}\bigl(2,\varphi(CD/5^{v_5(CD)})\bigr).
\]
Every label \(S_i=3^x+5^y\) is \(S_0\bmod CD\). Both axes grow as \(b\to\infty\), with \(p,q,D\) held fixed. Sample genuine anchors in the ordinary window on \(n=S_0+Ct\). Inside the low-prime cell \(D\mid t\), write \(t=Du\) and \(h_i=(S_0-S_i)/(CD)\). The anchor condition is exactly that \(u\) is a norm, and \(W(u)=\sum_i\beta(u+h_i)\) counts true alternatives.

Both strides are multiples of \(p-1\) and have \(p\)-adic depth \(\nu\). LTE gives \(p^k\mid h_i\) throughout the grid. Modulo \(p^{k+1}\), the normalized difference \(h_i/p^k\) is linear in the two exponent indices, with at least one unit coefficient. Hence \(p^{k+1}\mid h_i\) selects exactly one residue modulo \(p\) on one axis for each position on the other axis.

Now restrict further to \(p^{k+1}\mid u\). The power \(p^{k+1}\) is a square, so the anchor is still genuinely a norm after division. Every label outside the selected residue has \(v_p(u+h_i)=k\) and fails. The surviving \((1/p+o(1))K\) labels reduce to actual two-norm tests after division by \(p^{k+1}\).

### Why the mean drops for true norms

In the whole \(D\)-cell, Plaksin’s pair lower bound gives
\[
\mu_D=\mathbb E[W\mid D\mid t]\gg K/\sqrt b .
\]
The expectation is over genuine anchors. The normalized interval has fixed positive proportional length, and all shifts are positive and below its left endpoint. The lower-bound constant is independent of \(p,q\). [Plaksin, p. 145](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=rus&paperid=5142&wshow=paper)

On the deeper \(p\)-cell, Henriot’s two-form upper bound gives
\[
\mu_{D,p}\ll_D \frac{(\log(2p))^{A}}{p}\,\frac K{\sqrt b}
\]
for a fixed \(A\). The factor \(1/p\) is the exact affine thinning of the labels. The discriminant average costs only a power of \(\log p\). In detail, for a varying base \(g\) with step \(L\), squarefree divisors of effective order at most \(T\) use primes dividing \(\prod_{d\le T}(g^{Ld}-1)\). The reciprocal Euler product with any fixed weight \(1+A_0/\ell\) is \(O((\log(2LT))^{A_0})\), by splitting the primes at the logarithm of that product. Dyadic summation gives an order-weighted bound \(O((\log(2L))^{A_0})\). The surviving fibers have step \(pH\) or \(pJ\), and their lengths tend to infinity. The divisor-tail truncation from the preceding moment argument makes the one-class rounding error \(o(1)\) for each fixed \(p\). Since \(q=p^{O(1)}\), the log-stride cost is polylogarithmic in \(p\). Henriot applies to the two distinct monic shifts in the rescaled proportional interval. [Henriot, Corollary 2](https://arxiv.org/pdf/1102.1643#page=7) · [Erratum](https://doi.org/10.1017/S0305004114000280)

Choose \(p\) large enough that \(\mu_{D,p}\le\mu_D/2\), then let \(b\) grow. Among true anchors in the \(D\)-cell, the deeper cell has relative mass \(\rho=p^{-(k+1)}+o(1)\), by the norm count and division by the square \(p^{k+1}\). The variance explained by this split is
\[
\frac{\rho}{1-\rho}(\mu_D-\mu_{D,p})^2\gg_{D,p}K^2/b .
\]
The \(D\)-cell itself has positive mass among true anchors and lies inside the zero residue class modulo \(M_0\). Hence the expected residual variance after centering on \(t\bmod M_0\) is still \(\gg_{D,p}K^2/b\). The off-diagonal centered sum has this same lower order, since the diagonal is at most \(K=o(K^2/b)\). [Landau–Ramanujan count](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf)

This establishes a failure of the small-covariance criterion on these grids. It leaves the near-full matching question open, since a count can fluctuate at this scale and still be large on most targets.

### Standalone exact control

This uses \(p=7,\ q=13,\ C=65,\ D=9\). It constructs one ordinary true anchor in the deeper cell, a genuine alternative, and a neighboring blocked alternative at the same \(n\). It also verifies the one-in-seven phase rule.

```python
from math import isqrt

a,b,C,D,p,H,J = 7864,5368,65,9,7,48,72
A,B = 3**a,5**b
assert 39*A < 40*B and 125*B < 122*A
S0,P,S3,U = A+25*B,A+125*B,729*A+B,729*A+625*B
x,y = 808,1338
assert (x-a)%H == (y-b-2)%J == 0

G = C*D*p*p
S = 3**x+5**y
assert (S0-S)%G == 0
h = (S0-S)//G
lo = (2*S3-P-S0)//G
d = (isqrt(B//G)|1)+2
assert (h-d*d-1)%2 == 0
T = (h-d*d-1)//2
v0 = isqrt(lo-(T//d)**2)
v = v0+(T-v0)%d
u = (T-v)//d
n = S0+G*(u*u+v*v)
assert 2*S3-P < n <= U and (n-S0)%G == 0

assert 63**2+42**2 == G//5
for label,z,w in [(S0,u,v),(S,u+d,v+1)]:
    r,s = sorted((abs(63*z-42*w),abs(42*z+63*w)),reverse=True)
    P1,P2 = 2*r+s,r-2*s
    assert n-label == P1*P1+P2*P2 and S3 < label+P1*P1 <= n

assert (n-3**x-5**(y+J))%49 == 35  # exact odd depth at 7
for i in range(7):
    residues = [(n-pow(3,x+H*i,49)-pow(5,y+J*j,49))%49
                for j in range(7)]
    assert sorted(residues) == list(range(0,49,7))
```

The displayed finite control was independently replayed in BigInt, including the full same-target seven-by-seven residue check. Its small p illustrates the filtering mechanism; it is not a numerical validation of the asymptotic mean-drop constants.
