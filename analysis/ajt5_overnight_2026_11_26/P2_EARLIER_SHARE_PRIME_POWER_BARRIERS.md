# Further restrictions on the actual earlier-factor shares

For the fixed share \(H=w_*R\), **any divisor of \(E\) in the short-factor interval must take at least two distinct primes from \(D_1\)**. Its complementary share \(E/\ell\) must also contain at least two distinct primes. These restrictions hold on the pinned cofinal refinement for sufficiently large \(a\). The existence of an unrestricted divisor in the interval remains open. [Pinned two-sided margin result](https://github.com/Samsen879/a303656/commit/61d5c0a71466ec37ccfe17c1cdfd47ec2b974dbd)

### A bound on actual prime powers

With \(v=H\ell\) and \(u=d/v\), the required size exponents of the two earlier shares are
\[
\lambda_v=\frac{541661}{113435322},\qquad
\lambda_u=\frac{395821}{113435322}.
\]
On the \(19\cdot23\) refinement, write \(E=6(X^M+Y^M)\) in the refined bases, with \(M=11g\cdot19\cdot23\). For an odd prime \(p\ne3,5\) dividing the sum, let \(2j=\operatorname{ord}_p(X/Y)\). Then \(j\mid M\), and the exact depth is
\[
v_p(E)=v_p\!\left(\Phi_{2j}(X,Y)\right)+v_p(M/j).
\]
The first term accounts for the primitive factor. The second accounts for repeated occurrence at exceptional indices. Its prime-power multiplier is at most \(101\), since \(M\) is squarefree.

Consequently every full prime power in \(E\) is bounded by \(101\cdot2^{129}A^\beta\), where
\[
\beta=\frac{27648000}{8261872619}<\min(\lambda_v,\lambda_u).
\]
The strict size margins exclude a single-prime earlier share on either side. Even giving the short side all of \(24D_0\) and one full \(D_1\) prime power leaves it below \(4\sqrt A\), since \(1/1331+\beta<\lambda_v\).

### Whole polynomial factors also miss the interval

The degree obstruction survives **every fixed odd common-exponent refinement**, including rational factorizations exposed by square-root bases. Write the refined bases as \(X=3U^2,\ Y=V^2\). Every irreducible rational factor of
\[
(3U^2)^M+V^{2M}
\]
has even homogeneous degree. A root \(z=U/V\) generates the root of unity \(3z^2=\zeta\). If \(\zeta\ne-1\), its cyclotomic degree is even. If \(\zeta=-1\), the root has degree two.

A product of whole factors therefore has an integer degree in the \(X,Y\) size scale. The required short-share degree is half-integral, since \(2n\lambda_v=5958271\) is odd and stays odd after multiplication by a fixed odd refinement. On the balanced strip this excludes every whole-factor product at sufficiently large height. The unresolved step is to control **divisors of the integer values** of those factors.


The exceptional multiplier comes from lifting the \(p\)-valuation of \(X^j+Y^j\) by the odd index \(M/j\); since the order is exactly \(2j\), the valuation of \(X^j+Y^j\) is its primitive cyclotomic contribution. The prime powers at 2, 3 and 5 are bounded (valuations 3, 1 and 0 on the pinned parity, respectively). Fixed homogeneous cyclotomic factors have the indicated degree sizes on the balanced strip by the homogeneous product formula. Likewise any whole irreducible rational factor in \(U,V\) has magnitude comparable to its degree size there: the input ratio ranges over a compact positive interval, and none of the factors has a positive real zero. The result remains an asymptotic restriction, not an exclusion of arbitrary divisors.

The replay checks the exact exponents, half-integral degree, and a small true earlier divisor maintained on the cofinal progression. No separate exact-quotient/local-square claim is made here.

```python
from fractions import Fraction as F
from math import prod,gcd
n,g=1331*468741,468741
period,h,k=21112080,12416651,10186
ps=(3,7,11,13,17,19,23,101)
M=prod(ps)
assert M==11*g*19*23 and gcd(period,19*23)==1
beta=F(prod(p-1 for p in ps),1331*g*19*23)
sigma,tau=F(2344000,5156151),F(768000,1718717)
lv=F(1,2)-sigma-tau/11
lu=F(1,121)-lv
assert beta==F(27648000,8261872619)
assert (lv,lu)==(F(541661,113435322),F(395821,113435322))
assert beta<min(lv,lu) and F(1,1331)+beta<lv
assert (2*n*lv).denominator==1 and (2*n*lv).numerator==5958271
m=13*13*79
assert (pow(3,11*g*h,m)+pow(5,11*g*k,m))%m==0
assert pow(3,11*g*period,m)==pow(5,11*g*period,m)==1
print("OK")
```
