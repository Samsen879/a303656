# A free-coordinate three-label family at ordinary height

The prior [four-label rotation](FOUR_BALANCED_LABELS.md) chooses one \(t=(5^{b-j+1}-3z)/4\) for each \(j\). There is a different construction with an entire interval of free \(t\)'s, using
\[
 24650=1+157^2=5^4+155^2=5^6+95^2.
\]
Keep \(A=3^a,B=5^b\) in the same balance range \(0.9<B/A<1.1\), with \(b\ge3\), and set \(F=5^{b-3}\), so \(B=125F\). For any even \(t\in[20F,40F]\) let
\[
 n=3^c+24650F^2+t^2,\qquad c=0\ \text{or}\ c=2a-2.
\]
The actual three labels \((c,2b-6),(c,2b-2),(c,2b)\) have positive residuals \((157F)^2+t^2,(155F)^2+t^2,(95F)^2+t^2\), respectively. The latter choice of \(c\) makes all exponent scales logarithmic in \(n\).

These \(n\) lie strictly inside the original ordinary interval \((\max(A^2,B^2)+1,A^2+B^2)\). Indeed \(24650F^2=1.5776B^2\), \(t^2\le0.1024B^2\), and \(3^c\le A^2/9\) for \(a\ge3\); the balance bounds give both inequalities directly. The \(10F+1\) choices give distinct odd \(n\), with \(F\asymp\sqrt n\). This does not keep the high-3 label of the old four-label construction automatically.

## Why the old construction has a different count

In the original progression \(a\equiv3,b\equiv2\bmod8\), each balanced pair \(A,B\) has exactly \(b/2\) distinct rotation targets, since the negative \(t\) decreases strictly over the odd \(1\le j<b\). The \(a\)-blocks are disjoint and each contributes \(O(\log X)\) below \(X\). Irrational rotation equidistribution gives the proportion \(\log(11/9)/(8\log5)\) of hits in the \(a\)-progression, and each hit has \(b/2=a\log3/(2\log5)+O(1)\). Summing by parts over \(a\le(\log X)/(2\log3)\), with at most \(O(1)\) boundary blocks partially used, gives
\[
 N_{\rm rot}(X)\sim\frac{\log(11/9)}{1024\log3(\log5)^2}(\log X)^2
\]
for that original fixed rotation only. Even if one changes the rotation for fixed labels while requiring the exposed coordinate \(C=5^{b-j}\), an identity \(z^2+t^2=w^2+C^2\) forces \((w-t)(w+t)=z^2-C^2\ne0\). Thus \(|t|\) has only divisor-many candidates at fixed \(a,b,j\), not a free interval by this identity.

```python
from math import isqrt
D=11**2-5**2
ts=[(D//d-d)//2 for d in range(1,isqrt(D)+1)
    if D%d==0 and (D//d-d)%2==0]
assert sorted(851+t*t for t in ts if (851+t*t)%2 and
              730<851+t*t<1354)==[855,951]
a,b=331,226
A,B,F=3**a,5**b,5**(b-3)
assert 9*A<10*B<11*A and B==125*F
for c in (0,2*a-2):
    for t in (20*F,30*F,40*F):
        n=3**c+24650*F*F+t*t
        assert max(A*A,B*B)+1<n<A*A+B*B and n%2==1
        assert all(n-3**c-5**(2*b-6+e)==(u*F)**2+t*t
                   for e,u in ((0,157),(4,155),(6,95)))
```
