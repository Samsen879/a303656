# Exact rigidity for common-coordinate 5-axis gaps 0, 4, and 6

Fix one integer \(n\), one 3 exponent \(c\), and one shared square coordinate \(t\). Put \(K=n-3^c-t^2\). If \(K-5^e,K-5^{e+4},K-5^{e+6}\) are squares, then \(e=2s\) and \(K=24650\cdot5^{2s}\), and **exactly** \(d=2s,2s+4,2s+6\) have \(K-5^d\) square. Thus the free family in [FREE_THREE_LABEL_HEIGHT_BLOCK.md](FREE_THREE_LABEL_HEIGHT_BLOCK.md) is rigid while this same \(c,t\) is held fixed.

For nonnegative roots \(U,V,W\) of the three differences, one has \(U^2-V^2=624\cdot5^e\). Put \(L=(V-W)/2,\ R=(V+W)/2\); they are positive integers because \(V^2-W^2=24\cdot5^{e+4}\), and \(LR=6\cdot5^{e+4}\). Let \(h=\min(v_5(L),v_5(R))\). If \(2h\le e\), put \(E=e-2h\). One reduced factor retains \(5^{E+4}\), so \(V'=V/5^h\ge5^{E+4}\), while \(U/5^h\) is integral. Its square equals \(V'^2+624\cdot5^E\), strictly between \(V'^2\) and \((V'+1)^2\), a contradiction. Thus \(2h>e\). It follows that \(v_5(U^2)=e\), making \(e=2s\). Both factors divided by \(5^s\) are multiples of 5 and have product 3750; their possible sums are \(125,155,175,265,385,755\). The replay checks that only 155 gives a square after adding 624 to its square. This gives the claimed \(K\).

For \(d\ge2s\), divide by \(5^{2s}\) and check the seven nonnegative candidates for \(d-2s\); larger exponents exceed \(K\). For \(d<2s\), the difference has 5-adic valuation \(d\), so \(d\) must be even, say \(d=2s-2r\) with \(r\ge1\). After dividing out the square factor the condition becomes
\[
 X^2-986Y^2=-1,\qquad Y=5^{r+1}.
\]
The unit \(\alpha=157+5\sqrt{986}\) has norm \(-1\) and inverse in \(\mathbb Z[\sqrt{986}]\). Every positive solution element reduces by powers of \(\alpha\) into \([1,\alpha)\). Any element in this interval of norm \(\pm1\) has a \(\sqrt{986}\) coefficient from 0 to 4, using its two real conjugates; the four nonzero candidates are ruled out below, so the original element is an odd positive power \(\alpha^m\). For its positive \(\sqrt{986}\) coefficient \(Y_m\), the leading binomial contribution is \(5m157^{m-1}\). Every remaining odd-index term \(\ell\ge3\) has 5-adic valuation at least \(v_5(m)+\ell-v_5(\ell)>v_5(m)+1\), from \(\binom m\ell=(m/\ell)\binom{m-1}{\ell-1}\). Consequently \(v_5(Y_m)=1+v_5(m)\). If \(Y_m\) were a 5-power it would be at most \(5m\), impossible for \(m>1\) by the leading term and positivity. The remaining \(Y_1=5\) would give \(r=0\). No lower label is possible.

This rules out a fourth label only with the same \(c,t\) and the stated gaps, not other representations of the actual target.

```python
from math import isqrt

def sq(n):
    return n >= 0 and isqrt(n)**2 == n

P = (5**6 - 5**4)//4
V = {d + P//d for d in range(1, isqrt(P)+1)
     if P%d == 0 and d%5 == (P//d)%5 == 0}
assert V == {125, 155, 175, 265, 385, 755}
assert {v for v in V if sq(v*v + 624)} == {155}
assert [d for d in range(7) if sq(24650-5**d)] == [0, 4, 6]
assert 157**2 - 986*5**2 == -1
assert not any(sq(986*y*y+s) for y in range(1,5) for s in (-1,1))

A, B, F = 3**331, 5**226, 5**223
assert 9*A < 10*B < 11*A
for t in (20*F, 40*F):
    n = 1 + 24650*F*F + t*t
    assert max(A*A,B*B)+1 < n < A*A+B*B and n%2
    for j,u in ((0,157), (4,155), (6,95)):
        assert n-1-5**(446+j) == (F*u)**2+t*t
```
