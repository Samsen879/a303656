# Near-top split-prime switching to the distinct true-pair count

Switching to the small cofactor controls the last part of the reciprocal exactly on its natural scale. For the original grid and \(0\le\varepsilon\le1/4\),
\[
\boxed{\displaystyle
\left|[\Pi_0(B^{1-\varepsilon})-\Pi_-(B^{1-\varepsilon})]
      -(T_0-T_-)\right|
\ll \sqrt{\varepsilon+1/\log B}\,\frac{BK}{\log B}.}
\]
Here \(\Pi_r(Y)\) is the **raw** Gaussian proxy at cutoff \(Y\), \(T_r\) is the distinct true-pair count, and \(K\) is the original grid size. Thus a signed estimate near the top cutoff would transfer to the true count. The sign of that proxy at the required cutoff remains open.

### Exact switching

Use \(n=S_0+45u\) in the ordinary window and \(k=(S_0-S_i)/45\) for a label in the 147 compatible phases. Both \(u\) and \(u+k\) are \(\asymp B\). Write \(Y=B^{1-\varepsilon}\). On each side, a split prime \(p\ge Y\) is unique and has exponent one, since \(Y^2\gg B\).

Let \(C_r^{(0)}\) and \(C_r^{(1)}\) count true pairs with such a prime on the anchor or alternative side, respectively. Let \(D_r\) count true pairs with both. Expanding the two multiplicity factors gives the exact identity
\[
\Pi_r(Y)-T_r=C_r^{(0)}+C_r^{(1)}+D_r.
\]
An anchor mark switches to \(u=dp\), with \(d\ll B^\varepsilon\) a true norm, \(p\) a split prime, and the second test \(\beta(dp+k)\). The alternative mark switches to \(u+k=dp\) and the second test \(\beta(dp-k)\). The class constraint stays on the same target. For example, in the first switch it is \(S_0+45dp\equiv r\bmod49\).

### Uniform bound for small cofactors

For either switch and fixed \(d,k\), the count is at most
\[
\ll \frac{B}{d(\log B)^{3/2}}\,F(d)F(k),
\qquad
F(v)=\prod_{\substack{q\mid v\\q\equiv3\ (4)}}\left(1+\frac1{q-2}\right).
\tag{1}
\]
This bound holds with an absolute constant in the stated range of \(\varepsilon\).

To obtain (1), put \(c=(d,k)\) and use the primitive forms \(x\) and \((d/c)x\pm k/c\). Majorize the prime test by the indicator that \(x\) has no prime factor below \(B^{1/4}\). On the second form retain the even-valuation tests at inert primes outside \(c\). These are necessary tests for \(dp\pm k\). The interval for \(x\) has location and length \(\asymp B/d\), and the coefficient height is \(O(B)\), so the uniform multiplicative-function upper bound applies with fixed parameters. [De la Bretèche–Tenenbaum, Theorem 3.1](https://arxiv.org/pdf/2403.19320#page=4)

Below \(B^{1/4}\), a split prime contributes at most \(1-1/q\). With distinct roots, this follows from \((1-2/q)(1+1/q)\le1-1/q\). A shared or absent second root leaves only the first root to sieve. At a good inert prime the factor is at most \((1-2/q)(1+O(q^{-2}))\), since positive allowed valuation starts at two. At an inert prime dividing \(dk\), the loss relative to that factor is at most \(1+1/(q-2)\), up to \(1+O(q^{-2})\). This includes primes dividing \(c\): dropping the second parity test there restores at most the one-root factor \(1-1/q\). The primes above \(B^{1/4}\) change the upper bound by a bounded factor. These products give exponent \(3/2\) in (1).

The switched cofactor remains a norm, so
\[
\sum_{\substack{d\le D\\\beta(d)=1}}\frac{F(d)}d\ll\sqrt{\log(2D)}.
\]
In the Euler product, inert primes start at exponent two and split primes supply the square-root logarithm. Also \(F(k)\) has bounded mean on each of the 147 cells. Expand it over squarefree inert divisors \(h\), separating the fixed prime \(3\). For fixed \(y\), a hit \(h\mid k\) occupies at most one class modulo \(\operatorname{ord}_h(3^{84})\), giving frequency \(O(1/\log h+1/a)\). The divisor weights sum to \(O(\sqrt{\log(2t)})\) up to \(t\), so the \(1/\log h\) sum converges and the \(1/a\) term stays bounded. Summing (1), and using \(D_r\le \min(C_r^{(0)},C_r^{(1)})\), proves the displayed bound.

### The remaining signed step

In particular,
\[
\lim_{\varepsilon\downarrow0}\limsup_{B\to\infty}
\frac{\log B}{BK}\left|\Delta\Pi(B^{1-\varepsilon})-\Delta T\right|=0.
\]
A uniform positive margin for \(\Delta\Pi(B^{1-\varepsilon})\) as \(\varepsilon\downarrow0\) would suffice.

The available marked-modulus count has a different range. With \(X=\sqrt B\) and sieve level \(D=X^{1/20}\), its summed single-prime error is \(X^{3/2+o(1)}D^5Z^5\) for marks up to \(Z\). This estimate saves a power for \(Z<B^{1/40}\) with fixed slack. The cofactor switch controls primes near \(B\), leaving the intermediate primes between these ranges. Even at the top, the switch gives upper bounds on actual pairs. A signed estimate would need the prime–norm correlation with the class restriction retained. With two marks the exact equation is \(e q-dp=k\); after removing \((d,e)\), this asks for two primes on coupled linear forms in one parameter. Neither marginal prime distribution nor the switched upper bound supplies the signed comparison.

### Exact real controls

The replay produces a certified 1,134-bit split prime \(p>B\) with switched cofactor one. At the resulting \(r_-\) target, two labels in the **same phase** give a true norm and an exact \(131\)-valuation-one failure. Both alternatives are units at \(7\).

```python
from math import isqrt

a,b = 712,486
A,B = 3**a,5**b
S0,P,S3 = A+25*B,A+125*B,729*A+B
lo,hi = 2*S3-P,729*A+625*B
S,T = 3**76+5**104,3**76+5**146
k,rem = divmod(S0-S,45)
assert 39*A<40*B and 125*B<122*A and rem==k%8==0

M = 1<<567
pmin = (lo-S0)//45+1
d = 4*((isqrt(pmin+k)+4)//4+3550)
rhs = ((k-d*d)%M)//8
x,j = rhs%2,1
while j<564:
    j = min(2*j,564)
    mod = 1<<j
    x = (x-(2*x*x+x-rhs)*pow(1+4*x,-1,mod))%mod
c = M//2-1-4*x
p = c*c+d*d-k
assert B<p<M*M and p%M==1 and (p-1)//M%2==1
assert pow(3,(p-1)//2,p)==p-1

n = S0+45*p
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert lo<n<=hi and n%49==r==27
assert n-S==45*(c*c+d*d)
v,rem = divmod(n-T,45)
assert rem==0 and v%131**2==17030
assert (n-S)%49==(n-T)%49==47
```

The modular witness proves primality: for every prime divisor \(\ell\) of \(p\), the order of \(3\bmod\ell\) has exact \(2\)-depth 567, so \(\ell>M>\sqrt p\). Thus the anchor is a genuine split-prime norm. The two labels expose a difference in the actual switched norm test with the prime, cofactor, target class, and phase held fixed.

Independent BigInt rebuilt the 1134-bit prime certificate, both genuine representations, and the same-target exact odd-131 failure. The estimate is an upper bound for the top-prime discrepancy, not the signed intermediate-prime comparison.
