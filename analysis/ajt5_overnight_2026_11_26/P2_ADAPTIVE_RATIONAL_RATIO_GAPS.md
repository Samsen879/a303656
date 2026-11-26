# Rational-factor gaps remove a positive fraction of the P2 height interval

**Fixed or sublinear denominator cutoffs remove a vanishing fraction. Denominators of order \(\sqrt A\) remove a positive fraction.** On the pinned cofinal subfamily, the adaptive gcd-size test below removes exactly \(12/(13\pi^2)+o(1)\) of the ordinary interval by length, about **9.35%**. It removes between **9% and 10% of integer heights** for sufficiently large exponents. [Pinned second-pair result](https://github.com/Samsen879/a303656/commit/755c1ec9da2e8f3115576d4af65fc789941982a5)

### The rational gaps

Put \(W=\sqrt A\), \(D=f-e\), and \(\rho(K)=r(K)/v(K)\). The exact products are \(uv=d\) and \(rs=D\). The identity \(81d-D=12181B\) bounds their gcd, and the pinned phase gives \(\gcd(d,D)=13\) exactly.

For a reduced positive ratio \(p/q\), the gap test is
\[
|qr(K)-pv(K)|<1,\qquad q<v(K)/13.
\]
At an integer solution, the first inequality forces \(qr=pv\). Then \(r=pt,\ v=qt\), where \(t\mid\gcd(d,D)\), contradicting the second inequality. The ratios \(199/200\) and \(201/200\) both have centers in \(1001A<K<1099A\) throughout the pinned strip. Each gives a certified gap of radius \(16W/200\).

### How much the union removes

Write \(\kappa=K/A\), \(V(\kappa)=v(K)/W\), and \(I\) for the normalized ordinary interval. For a fixed cutoff \(Q\le W/4\), the fraction removed by denominators at most \(Q\) is
\[
\frac{12}{\pi^2}\frac{Q}{W}\,
\frac{1}{|I|}\int_I\frac{d\kappa}{V(\kappa)}
+O\!\left(\frac{\log^2(2Q)}{W}\right).
\]
Thus \(O(Q/W)\) is sharp as \(Q\to\infty\), and \(Q=o(W)\) gives a vanishing fraction of both length and integer heights.

The proof uses the ratio coordinate \(x=\rho(K)\), which decreases strictly. Its inverse in normalized height has bounded first and second derivatives, including at the lower endpoint after using \(\sqrt{\kappa-S_3/A}\) as a coordinate. A reduced ratio \(p/q\) cuts out a neighborhood in \(x\) of radius \(1/(qWV(\kappa))\). The neighborhoods are disjoint in this denominator range by the Farey separation \(1/(qq')\). Möbius inversion counts the reduced numerators against the inverse-height weight, and \(\sum_{q\le Q}\varphi(q)/q=(6/\pi^2)Q+O(\log(2Q))\) gives the formula.

For the **adaptive** cutoff \(q<v(K)/13\), partition the ratio interval into short pieces and sandwich the cutoff on each piece by its minimum and maximum. The local factor \(Q/W\) then tends to \(V(\kappa)/13\), cancelling \(1/V(\kappa)\). This gives the stated \(12/(13\pi^2)\) limit. Every denominator is at most \(21W/26\), and \(r/v<3\). Rounding each gap to integer heights changes the fraction by at most
\[
\frac{(3/2)(21/26)^2}{624(39/40)}+o(1)<0.00161+o(1),
\]
which gives the 9–10% bounds.

### The exact condition that remains

With denominators of order \(W\), Dirichlet approximation supplies a near-equality at every real height. The retained integer centers still need \(t\in\{1,13\}\), the true divisibilities \(qt\mid d,\ pt\mid D\), and the same-height identity
\[
\left(qt+\frac d{qt}\right)^2-
\left(pt+\frac D{pt}\right)^2=4e.
\]
On the short branches this is reversible and reconstructs the two remaining integer roots. For fixed \(w_*R\), it must also give \(qt=w_*R\ell\) with \(\ell\mid E\). The ratio gaps discard heights, while the exact divisor test still decides the retained centers.


The fixed-cutoff proof extends to \(Q\le 21W/26\), not just \(Q\le W/4\). Indeed \(v>4W\), and an intersection of the gaps of distinct reduced ratios would require \(1/(qq')<(1/q+1/q')/(4W)\), contrary to \(q+q'\le42W/26<4W\). This justifies using the same weighted estimate in the adaptive cutoff sandwich. In normalized ratio coordinate \(x\), the inverse height \(\kappa(x)\) is smooth up to the endpoint: its first derivative vanishes there after using \(\sqrt{\kappa-S_3/A}\) as local parameter. With the positive normalized length bounded below uniformly on the pinned strip, endpoint intervals only contribute the usual \(O(\log(2Q)/W)\) total error.

For each \(q\), summing the main gap widths over reduced numerators is a weighted Riemann sum. Möbius inversion gives error \(O(\tau(q)/(qW))\), summable to \(O(\log^2(2Q)/W)\), and summation of the main terms gives the displayed cutoff formula. Pointwise variation of the radius adds \(O(\log(2Q)/W^2)\) by its bounded derivative. This is a height exclusion on the P2 family only; it gives no new density bound on the original conjecture.

```python
from fractions import Fraction as F
from math import isqrt
b0,b1=F(39,40),F(122,125)
N=1331*468741
T,h,k=21112080,12416651,10186
a,b=N*h+1,N*k-2
assert 12181==13*937 and all(937%j for j in range(2,isqrt(937)+1))
for p,x,y in ((13,0,0),(937,638,143)):
    A,B=pow(3,a,p),pow(5,b,p)
    assert pow(3,N*T,p)==pow(5,N*T,p)==1
    assert ((2*A+150*B)%p,(162*A-31*B)%p)==(x,y)
def sqrt_bounds(x):
    w=10**7
    r=isqrt(x.numerator*w*w//x.denominator)
    return F(r,w),F(r+1,w)
def sum_root(K,i,j):
    const=(1,9,81,729)
    coeff=(25,625,125,1)
    return (sum(sqrt_bounds(K-const[t]-coeff[t]*b1)[0] for t in (i,j)),
            sum(sqrt_bounds(K-const[t]-coeff[t]*b0)[1] for t in (i,j)))
def ratio_interval(K):
    u0,u1=sum_root(K,0,1)
    v0,v1=sum_root(K,2,3)
    return ((162-31*b1)*u0/((2+150*b1)*v1),
            (162-31*b0)*u1/((2+150*b0)*v0))
assert ratio_interval(1001)[0]>F(201,200)
assert ratio_interval(1099)[1]<F(199,200)
assert F(3,2)*F(21,26)**2/(624*b0)<F(161,10**5)
assert 2*F(21,26)<4
# Rational pi bracket 3.14159<pi<3.14160 suffices for integer-height envelope:
assert F(12,13)/F(314160,100000)**2-F(161,10**5)>F(9,100)
assert F(12,13)/F(314159,100000)**2+F(161,10**5)<F(1,10)
print('OK')
```
