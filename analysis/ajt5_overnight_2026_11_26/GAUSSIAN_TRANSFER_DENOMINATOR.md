# The exact denominator obstruction for multiplicative norm transfer

For a fixed 5 exponent \(D\), put \(H=n-5^D\), and take distinct 3 exponents \(c,c'\) with \(R=H-3^c>0,\ R'=H-3^{c'}>0\). A Gaussian rational transfer \(z'=\alpha z/\beta\) between nonzero norm certificates forces
\[
 \frac{R}{\gcd(R,R')}\mid N(\beta),\qquad
 \gcd(R,R')=\gcd(R,3^{c'}-3^c).
\]
Indeed \(N(\beta)R'=N(\alpha)R\). If both residuals are already known to be true norms, this bound is attained, even for any fixed source \(z\). To see this, write \(g=\gcd(R,R')\). At every inert prime its valuation in \(g\) is even, so the matching inert factors can be extracted from \(z\); at a split prime the needed number of factors can be extracted from either conjugate in the factorization of \(z\). The prime above 2 uses the ordinary ramified factor. This gives a Gaussian divisor \(w\mid z\) of norm \(g\). Set \(\beta=z/w\) and take \(\alpha\) of norm \(R'/g\), which is also a norm by the same prime-factor criterion. Equality is a denominator characterization; it does not produce the missing target norm certificate by itself.

If \(H\le X\) and \(N(\beta)\le X^\theta\) with \(\theta\ge0\), the number of eligible integer centers \(H\) is at most \(O_\varepsilon((\log X)^2 X^{\theta+\varepsilon})\): there are \(O((\log X)^2)\) exponent pairs, \(g\) is a divisor of their nonzero difference of absolute value below \(X\), and \(R/g\le X^\theta\). Use the elementary divisor bound \(\tau(j)\ll_\varepsilon j^\varepsilon\). If the denominator norm has all its prime factors in a fixed finite set \(S\), then \(R/g\) also has that support and is at most \(X\). Its choices are bounded by \(O_S((1+\log X)^{|S|})\) by counting exponents. This makes the eligible centers \(X^{o(1)}\) for fixed \(S\).

A large denominator is possible at genuine adjacent points. At \(n=5418,D=3\) the residuals at exponents 5 and 7 are \(5050,3106\), of gcd 2, so the minimum denominator norm is 2525. In the odd-odd four-point family of [DIRECT_GAUSSIAN_NORM_TRANSFER.md](DIRECT_GAUSSIAN_NORM_TRANSFER.md), holding the starting 5 coordinate fixed gives two residuals whose difference is \(8\cdot3^c\); the starting residual is \(2\bmod8\) and coprime to 3. Thus their gcd is 2. The starting residual is at least \((25/3)3^c\), so the minimum denominator norm is at least \(25H/56\) even along unbounded ordinary exponents.

## Three actual points at a non-pure-power center

For any even \(a\ge22\) put \(H=2\cdot3^a\) and \(n=H+5^D\). The three \(c\) values \(a,a-2,a-18\), with the same \(D\), have Gaussian certificates
\[
 z_0=3^{a/2},\qquad z_1=(4+i)z_0/3,\qquad
 z_2=(4040+5409i)z_1/3^8 .
\]
Both divisions are integral. The matching norm identities use \(N(4+i)=17\) and \(17(4040^2+5409^2)=2\cdot3^{18}-1\). This non-pure-power example has three points; it does not give arbitrarily long chains.

```python
from math import gcd
r,t=45**2+55**2,9**2+55**2
assert (r,t,gcd(r,t))==(5050,3106,2)
assert 50**2+5**2==2525 and 32**2+23**2==1553
a=22
u,v=3**(a//2),0
for m in (0,2,18):
    if m:
        x,y,p=(4,1,3) if m==2 else (4040,5409,3**8)
        assert u%p==v%p==0
        u,v=(x*u-y*v)//p,(y*u+x*v)//p
    assert u*u+v*v==2*3**a-3**(a-m)
```
