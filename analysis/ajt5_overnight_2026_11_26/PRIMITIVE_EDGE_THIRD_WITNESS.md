# Primitive sector edges isolate the noncollinear third-witness problem

Use the original \(3,5\) shift set in [critical sector overlap](CRITICAL_SECTOR_DISTINCT_RESIDUALS.md), whose shifts all lie in an interval of length \(H=O(X^{1/3})\). Pull the rotated sector back by \((4-3i)/5\). All points from either sector are then on \((1/5)\mathbb Z^2\). Consider two witnesses to the same \(n\) at \(P,P+D\), where the difference \(D\in\mathbb Z^2\) is primitive and \(D\ne0\). If \(\|D\|^2>25H\), every other lattice point on that line has squared norm outside the same residual interval, except possibly the given endpoints.

To see this, let \(Q=P+tD\). Primitivity and the grid imply \(t\in(1/5)\mathbb Z\). Put \(A=\|P+D\|^2-\|P\|^2\), so \(|A|\le H\). The squared norm difference is
\[
 \|Q\|^2-\|P\|^2=tA+t(t-1)\|D\|^2.
\]
For \(t\in(1/5)\mathbb Z\setminus\{0,1\}\), direct inspection on \(0<t<1\) gives \((1+|t|)/(|t||t-1|)\le12\), and for \(t\le-1/5\) or \(t\ge6/5\) the ratio is also at most 12. Hence the quadratic term exceeds \(H+|t|H\) under the asserted hypothesis. But all possible residuals at the given \(n\) have pairwise differences at most \(H\). This excludes every third position on the primitive line. The threshold 25 is intentionally conservative; the condition holds in particular for \(\|D\|\asymp\sqrt X/(\log X)^2\) and large \(X\).

For the density question, suppose a chosen constructible subfamily of such primitive distinct-shift witness pairs has counts \(W(n)\) with \(\sum W(n)\gg X\), and write \(Z(n)\) for the total witness count across both sectors. If \(\sum W(n)Z(n)=O(X)\), then restricting to any sufficiently large fixed \(Z(n)\le K\) keeps \(\gg X\) pairs, each on an integer of bounded multiplicity. This would give positive lower density for actual hit integers. The only non-endpoint triples to be bounded in this criterion are noncollinear, by the previous paragraph. This note proves the geometry and the conditional counting implication, not the requisite upper bound or any small-\(C\) asymptotic.

## Exact noncollinear control

At \(X=2^{42}\) and \(n=4484534701797\), three distinct squarefree norms occur at valid shifts. Two points are in the near-axis sector and the third is in the rotated sector. After pulling back the third, the three points are noncollinear. The edge from the first to the third is primitive.

```python
from math import gcd,isqrt
n=4484534701797
for a,b,p,f in [(2117672,1,25,(5,896906939917)),
                 (2117672,5,1,(16741,267877349)),
                 (2117671,2058,5,(5,896906939921))]:
    assert n-3**7-p==a*a+b*b==f[0]*f[1] and f[0]!=f[1]
    assert all(all(q%d for d in range(2,isqrt(q)+1)) for q in f)
    assert 900*b<a
a,b=2117671,2058
assert (4*a-3*b,3*a+4*b)==(5*1692902,5*1272249)
assert gcd(1,2057)==1 and 0*2057-4*(-1)==4
```
