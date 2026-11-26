# A split-prime phase forces signed cancellation between two divisor tails

Use the actual separated grid and cofactor band in [the pair lower bound](FIXED_COFACTOR_BAND_PAIR_LOWER_BOUND.md), with \(c=2+24i,\ d\equiv2\bmod24\). Restrict \(i\bmod5\) to 0 or 1 and \(n\equiv14\bmod25\) in addition to \(n\equiv527\bmod672\). Then the shifts in the two selected classes are \(9\) and \(4\bmod25\), respectively, so each residual \(n-s\) has exact \(v_5=1\).

For sufficiently large fixed \(y\), then \(X\to\infty\), the block has \(\gg XK_X^2/(\log X\log(3y))\) ordered distinct-shift pairs of residuals \(5ab,5a'b'\), with \(a,a'\) the specified small squarefree cofactors (all factors split and above \(y\)), \(b,b'\) large split primes, and \(\gcd(ab,a'b')=1\). In particular \(\gcd(a,a')=\gcd(aa',s-t)=1\), so these parameters still occur in the divisor-tail expansion on the original cofactor progression. They are **not** jointly prime values of the two candidates \(L_1,L_2\): both candidates are divisible by 5. The residuals themselves are true squarefree two-square norms.

For the size of this block, the earlier first- and second-moment proof applies with the extra fixed congruences: after division by 5 each offset gives a reduced class for \(ab\) modulo \(5\cdot672\). Fixing one allowed exponent class leaves a step \(120\) in \(c\) and still a logarithmic grid width. The first moment follows from the same cofactor-band reciprocal weight and the fixed-modulus prime number theorem. Cauchy–Schwarz gives the untrimmed pair bound before removing pairs sharing another prime. For this removal use the earlier Rieger argument on the two norms divided by 5, and then by the common prime. The divisor averages still use an injective mod-order condition, now for \(3^{120}\); the tail and endpoint error budget is \(O(\log(3y)/\sqrt y+(\log\log X)/\sqrt{\log X})\) after normalization by \(XK_X^2/\log X\). The fixed \(y\) can therefore be chosen large enough for strict positive mass. Both permitted exponent classes may be included by summing over their finitely many phase pairs.

Let \(E_R(L)=\sum_{d\mid L,\ d>R}\mu(d)\log(R/d)\). Pick fixed powers \(R_i=X^{\delta_i}\) with \(0<\delta_i<5/16\). On this block \(L_1=5b,L_2=5b'\), with \(5<R_i<\min(b,b')\) for large \(X\). The large divisors on each side are the prime \(b\) or \(b'\), and its product with 5. Put \(w=(\log(5b)\log(5b'))^{-1}\). The **only** noncoprime divisor pair is \((5b,5b')\) and its contribution is \(w\log(5b/R_1)\log(5b'/R_2)\), uniformly bounded below by a positive constant. The sum over the other three pairs is \(w(\log5)^2\) minus this contribution, uniformly bounded above by a negative constant. The sum of both parts, however, is just \(w(\log5)^2\) per pair. Summing even with the trivial block count \(O(XK_X^2)\) gives \(O(XK_X^2/(\log X)^2)\), below the relevant main scale. Consequently estimates treating both parts by absolute values discard necessary cancellation already on this actual growing subfamily. This is not an estimate for the full signed tail.

## Exact true-residual control

```python
from math import gcd,isqrt,log
n=10167641817839
b,bp=89715011641,70121667709
r,s=n-3**26-25,n-3**2-25
assert (n%672,n%25)==(527,14)
assert (r,s)==(5*17*b,5*29*bp) and gcd(r,s)==5
assert r==2761462**2+10179**2 and s==3101293**2+741366**2
for p in (b,bp):
    assert p%4==1 and all(p%d for d in range(2,isqrt(p)+1))
R=1785
assert 5<R<min(b,bp)
D=((b,-1),(5*b,1)); E=((bp,-1),(5*bp,1))
total=sum(u*v*log(R/d)*log(R/e) for d,u in D for e,v in E)
assert abs(total-log(5)**2)<1e-10
assert [gcd(d,e)>1 for d,u in D for e,v in E]==[False,False,False,True]
```
