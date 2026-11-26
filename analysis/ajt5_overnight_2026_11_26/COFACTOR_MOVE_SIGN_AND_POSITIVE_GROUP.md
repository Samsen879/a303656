# Moving one allowed cofactor prime flips the tail sign without canceling the group

Use the \(3,5\) shift grid, \(n\equiv527\bmod672\), and cofactor band \([X^{1/16},X^{1/8}]\) of [the fixed cofactor-band note](FIXED_COFACTOR_BAND_PAIR_LOWER_BOUND.md). Put \(R=X^{1/4}\) and \(E_R=\Lambda-\Lambda_R\), where \(\Lambda_R(L)=\sum_{d\mid L,d\le R}\mu(d)\log(R/d)\).

Let a genuine residual on one side be \(Aqp_1p_2b\) with distinct split primes and \(A\) disjoint from the other factors, both \(A,Aq\) in the band, \(qp_i<R\), \(b>R\), and \(p_1p_2>qR\). Put \(m=p_1p_2b\). For \(L=qm\), the low divisors are \(1,q,p_1,p_2,qp_1,qp_2\), giving \(E_R(qm)=+\log q\). For \(L=m\) they are \(1,p_1,p_2\), giving \(E_R(m)=-\log(p_1p_2/R)\). Both \(L\)'s are composite. These are two choices of cofactor on the **same** residual, not two different labels or targets. Their normalized sum
\[
 \frac{\log q}{\log(qm)}-\frac{\log(p_1p_2/R)}{\log m}
\]
stays negative whenever the logarithmic difference on the numerators is positive, and stays below a fixed negative constant if that difference is \(\gg\log X\). Thus for a pair of coprime residuals of this type, moving the prime on only one side gives a negative contribution, while summing all four allowed choices on the two sides yields a positive contribution.

There is a growing block with these bounds. Fix \(y\) large and let \(X\to\infty\). Write \(A=A_0u_1u_2u_3\), with \(A_0\) a squarefree product of split primes in \((y,X^\xi]\), \(A_0\le X^{1/256}\), with \(\xi\) small fixed. Take the three distinct \(u_i\) from \([X^{1/44},X^{1/42}]\), \(q\) from \([X^{1/32},X^{1/24}]\), and distinct \(p_1,p_2\) from \([X^{5/32},X^{11/64}]\), all split. Order within each repeated interval to avoid multiplicity. These disjoint ranges put \(A,Aq\) in the band and force \(\log(p_1p_2/R)-\log q\ge(\log X)/48\). The prescribed product other than \(b\) has size at most \(X^\theta\) for a constant \(\theta<1/2\). For each shift, the fixed-modulus prime number theorem finds \(b\) in the reduced class ensuring \(n\equiv527\bmod672\), counting residuals in \([X,3X/2)\). The large \(b>\sqrt{2X}\) and all marked factor bands make the construction uniquely decodable. The \(A_0\) reciprocal mass is \(\gg\sqrt{\log X/\log(3y)}\) by Mertens in progressions with the same weighted Markov restriction as in [the coprime pair argument](COPRIME_LARGE_PRIME_PAIR_MASS.md); all remaining bands have positive limiting reciprocal mass. Cauchy–Schwarz over actual \(n\), followed by that note's same-gap common-prime Rieger subtraction, leaves \(\gg XK_X^2/(\log X\log(3y))\) distinct-shift coprime pairs. Shared primes must divide the actual nonzero gap, so none can be the large \(b\). Thus both the negative subblock and the positive four-choice sum have main-scale mass for sufficiently large fixed \(y\). This does not bound the full signed remainder across other factor patterns.

## Exact original-box replay

```python
from math import gcd,isqrt,prod
n=5733592082652431139663215
R=1547414
r,s=n-3**26-25,n-34
assert n%672==527 and R**4<=n<(R+1)**4 and gcd(r,s)==1
for residual,F in ((r,(53,17,5209,5573,219209110746173)),
                   (s,(37,29,7001,7193,106110150824429))):
    a,q,p1,p2,b=F
    assert residual==prod(F)
    assert all(p%4==1 and all(p%d for d in range(2,isqrt(p)+1)) for p in F)
    assert a**16>=n and (a*q)**8<=n
    assert max(q*p1,q*p2)<R<b and p1*p2>q*R
```
