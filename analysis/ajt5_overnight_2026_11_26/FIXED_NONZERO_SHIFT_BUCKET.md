# A nonzero-shift bucket in the actual two-axis exponent window

This provides a fixed-offset subproblem for [the three-prime phase calculation](CROSS_SPECTRUM_THREE_PRIME_TAIL.md). It preserves ordinary integer height and uses the same \(n\) on both sides. It does not provide a prime-pair estimate.

Let \(c_+\equiv26,\ c_-\equiv50,\ d_+,d_-\equiv50\bmod120\), with both ends in
\[
 X^{1/8}\le3^c\le X^{1/4},\qquad X^{1/3}\le5^d\le X^{1/2}.
\]
Write \(s=3^{c_+}+5^{d_+},\ t=3^{c_-}+5^{d_-}\), \(h=t-s\). Modulo 11 both bases have order 5, so \(s=4,\ t=2,\ h=9\bmod11\). In particular there is no zero separation anywhere in the box or its compatible periodic phase model.

For all sufficiently large \(X\), choose a \(c_+\) for which \(c_-=c_++24\) is also in the box. The separation
\[
 h=3^{c_+}(3^{24}-1),\qquad 3^{24}-1=2^5\cdot5\cdot7\cdot13\cdot41\cdot73\cdot6481
\]
occurs for each of the \(\asymp\log X\) permitted common \(d=d_+=d_-\). These are all the exponent pairs with this separation. If the two \(d\)'s differ, their powers differ by at least \((5^{120}-1)X^{1/3}\) in magnitude, whereas the 3-powers change by at most \(X^{1/4}\); hence they cannot yield this \(h\). If the \(d\)'s agree, the positive difference of two 3-powers uniquely determines their exponents, first by its 3-adic valuation and then by its magnitude. The difference is fixed within each box, not asserted to be independent of \(X\).

For proposed coefficients \(D_+,D_-\) pairwise coprime with each other and with \(M=480480\), the congruences
\[
 n_*\equiv319055\pmod M,\qquad n_*\equiv s\pmod {D_+},\qquad n_*\equiv t\pmod{D_-}
\]
determine a progression \(n=n_*+MD_+D_-j\). The terminal quotients are then
\[
 b_+(j)=(n_*-s)/D_++MD_-j,\qquad
 b_-(j)=(n_*-t)/D_-+MD_+j .
\]
This is one shared integer parameter \(j\), with the relevant interval imposed on \(n\) and each residual. In particular \(D_+b_+(j)-D_-b_-(j)=h\) identically. A true mixed prime count needs the product of the two primality indicators along this progression; separate projection counts cannot supply that product.

```python
from math import prod
X,c,cc,d=2**329,26,50,50
assert all(X<= (3**z)**8 and (3**z)**4<=X for z in (c,cc))
assert X<=(5**d)**3 and (5**d)**2<=X
s,t=3**c+5**d,3**cc+5**d
assert (s%11,t%11,(t-s)%11)==(4,2,9)
assert t-s==717897987689310722941920
assert 3**24-1==prod((2**5,5,7,13,41,73,6481))
assert [319055%m for m in (672,65,11)]==[527,35,0]
```
