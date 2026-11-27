# A Gaussian gcd transfer with an unbounded exponent gap

Let a known Gaussian integer \(z\) certify \(R=N(z)\). Suppose the intended increment \(\Delta=R'-R\) and source residual satisfy
\[
 \Delta=gs^2,\qquad R=gt^2,\qquad (g,t)=1.
\]
Then \(w=\gcd_{\mathbb Z[i]}(z,g)\) has \(N(w)=g\), so \(w(t+is)\) certifies \(R'\) without factoring \(R'\). To see this, at each rational prime of \(g\) the norm of \(z\) has precisely the valuation of \(g\). The associated Gaussian exponents in \(z\) are individually no larger than their exponents in the rational integer \(g\), at split, inert, and ramified primes. The gcd extracts exactly these factors. If \((s,t)=1\), then \((R,R')=g\), and the multiplier denominator \(z/w\) has minimal norm \(t^2\) by [the denominator criterion](GAUSSIAN_TRANSFER_DENOMINATOR.md).

## Quantified original-power family

Take even \(j\ge2,c,D\), \(k=2^j\), and
\[
 g=\frac{3^{2k}-1}{2^{j+2}},\qquad s=2^{(j+2)/2}3^{c/2},
 \qquad n=3^{c+2k}+5^D+gt^2,\qquad t\equiv1\bmod3g,\quad t>0.
\]
Iterated difference of squares yields the explicit Gaussian integer
\[
 \delta=(1+i)\prod_{r=1}^{j}\frac{3^{2^{r-1}}+i}{1+i},
 \qquad N(\delta)=2\prod_{r=1}^j\frac{3^{2^r}+1}{2}=g.
\]
Each quotient is integral because its numerator has two odd coordinates. Hence \(t\delta\) certifies the source at \((c+2k,D)\); the increment on changing to \((c,D)\) is \(gs^2\). The congruence guarantees \((g,t)=(s,t)=1\), since \(g\) is even. The transfer works also from a different source certificate of the same residual.

Here \(g\equiv2\bmod8\) by the product formula (the first factor after the leading 2 is \(5\bmod8\), and all later factors are \(1\bmod8\)); also \(g\equiv2\bmod3\) by even \(j\). Thus \(H=n-5^D\equiv2\bmod3\) is not a pure 3-power. When \(c+2k>0, D\) is even, \(n\equiv4\bmod8\) and \(n\equiv0\bmod3\). These forbid \(n=3^u+5^v\): the first congruence forces odd \(u\), whereas for positive \(u\) the sum is a unit mod 3.

For large \(X\), choose the largest power of 4 at most \(\log_3\log X\) as \(k\), so \(g\le(\log X)^2\). Choose the largest even \(c,D\) with \(3^{c+2k},5^D\le X/4\), respectively, and take \(t\) in the congruence class with \(X/8\le gt^2\le X/4\). There are \(\gg\sqrt X/g^{3/2}\ge c_0\sqrt X/(\log X)^3\) distinct targets for an absolute \(c_0>0\). Their 3 and 5 exponents are of order \(\log X\), and the 3 exponent gap is of order \(\log\log X\). The denominator support cannot be captured by a fixed finite set of primes: such a restriction permits only polylogarithmically many \(t\le\sqrt X\). No arbitrary-target or arbitrary-length chain conclusion is claimed.

```python
from math import gcd, prod
for j in (2,4,6):
    k=2**j
    g=(3**(2*k)-1)//2**(j+2)
    assert g==2*prod((3**(2**r)+1)//2 for r in range(1,j+1))
    assert g%8==g%3==2
g,t,s=410,7,36
c,D,k=4,4,4
assert gcd(g,t)==gcd(s,t)==1
assert 3**(c+2*k)-3**c==g*s*s
n=3**(c+2*k)+5**D+g*t*t
assert n==552156
assert n-3**(c+2*k)-5**D==133**2+49**2
assert n-3**c-5**D==385**2+635**2
assert gcd(n-3**(c+2*k)-5**D,n-3**c-5**D)==g
```
