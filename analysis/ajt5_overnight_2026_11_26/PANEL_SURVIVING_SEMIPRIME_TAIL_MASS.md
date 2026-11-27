# Panel-surviving semiprime candidates carry positive signed-tail mass

Use \(n\equiv527\bmod672\), the fixed cofactor band, and the original separated \(3,5\) grid of [the pair lower-bound note](FIXED_COFACTOR_BAND_PAIR_LOWER_BOUND.md); denote its number of shifts by \(K_X\). Fix large \(y\) first and let \(X\to\infty\). There are
\[
 \gg \frac{XK_X^2}{\log X\,\log(3y)}
\]
ordered distinct-shift, same-\(n\) pairs with coprime residuals \(n-s=apb,\ n-t=a'p'b'\), where \(a,a'\in[X^{1/16},X^{1/8}]\) are squarefree products of split primes above \(y\), \(p,p'\in[X^{3/16},X^{7/32}]\) are split primes, and \(b,b'\) are larger split primes. Both residuals are true squarefree norms. The cofactor candidates \((n-s)/a,(n-t)/a'\) themselves are both semiprime, so their double-prime indicator is zero.

For each shift, use the prime number theorem in the fixed reduced class \(493(ap)^{-1}\bmod672\) at \(b\in[(X-s)/(ap),(2X-s)/(ap))\). Since \(ap\le X^{11/32}\), the smallest prime scale still grows as a fixed power and the interval ratios tend uniformly to two. The largest factor \(b\) is above \(\sqrt{2X}\); \(p>X^{1/8}\) is also larger than every factor of \(a\). Thus each qualifying representation contributes once. The reciprocal sum over \(a\) is \(\asymp\sqrt{\log X/\log(3y)}\) as in the linked note, while the reciprocal sum over \(p\) tends to \(\frac12\log(7/6)>0\) by Mertens in the split progression. The total first moment is \(\gg XK_X/\sqrt{\log X\log(3y)}\). Cauchy–Schwarz yields the stated pair scale before removing the diagonal and common factors. Any shared prime \(q>y\) divides the same actual nonzero gap \(s-t\) of size \(O(\sqrt X)\), so it cannot be a largest prime \(b\) or \(b'\). The [order-average and Rieger common-prime subtraction](COPRIME_LARGE_PRIME_PAIR_MASS.md) still applies to these squarefree norms after division by \(q\); on the normalized scale its upper bound is \(O(\log(3y)/\sqrt y+\log\log X/\sqrt{\log X})\). This is smaller than the first-moment-based lower bound for sufficiently large fixed \(y\).

Set \(R=X^{1/4}\) and \(E_R(L)=\sum_{d\mid L,\ d>R}\mu(d)\log(R/d)\). Each candidate \(L=pb\) passes the growing small-prime panel \(z\le\sqrt{\log\log X}\). The divisors at most \(R\) are 1 and \(p\); the prime \(b\) and \(pb\) both exceed \(R\). Therefore \(E_R(L)=-\log p\), and each product \(E_R(pb)E_R(p'b')/\bigl(\log(pb)\log(p'b')\bigr)\) is bounded below by a positive constant. This subfamily alone contributes positive main-scale mass for fixed \(y\); it cannot be discarded as an absolute error. This does not rule out signed cancellation with other admissible candidates and is not an estimate of the full pair correlation.

## Exact same-integer control

The example uses the ordinary active box rather than the narrower growing shape above. At \(n=10433679463055\), labels \((26,2),(2,2)\) give the checked coprime norms. The cutoff 1797 keeps just the two low divisors at each candidate, and both candidates avoid all primes at most 43.

```python
from math import gcd,isqrt,log
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
n=10433679463055
r,s=n-3**26-25,n-34
assert n%672==527 and 4*3**26<n and gcd(r,s)==1
assert r==17*449*1033907197==2739405**2+622474**2
assert s==29*457*787269257==3180339**2+564910**2
assert all(p%4==1 and prime(p) for p in (17,449,1033907197,29,457,787269257))
for p,b in ((449,1033907197),(457,787269257)):
    R=1797
    assert 43<p<R<b
    assert abs((-log(R/b)+log(R/(b*p)))+log(p))<1e-10
```
