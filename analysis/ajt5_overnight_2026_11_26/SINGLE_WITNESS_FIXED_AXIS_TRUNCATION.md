# Truncation removes the one-axis diagonal

Fix \(c=C\) and \(d=j\bmod L\) in the [fixed-axis escape windows](SINGLE_WITNESS_FIXED_AXIS_ESCAPE.md). Let \(K\asymp_L\log X\) be the number of such exponents in \(X^{1/3}\le5^d\le X^{1/2}\). The ordinary representation weight has a diagonal second-moment term \(O(\log X/K)\), which need not vanish. The positivity-preserving truncation
\[
 w_X(m)=\min(r_2(m),(\log X)^{15/16}),\qquad
 Z_X(n)=\frac1{\pi K}\sum_d w_X(n-3^C-5^d)
\]
retains the same hit set and makes the diagonal negligible.

Indeed, for \(f=r_2/4\) the pointwise power \(f^{3/2}\) equals the Dirichlet convolution \(f*g\) with \(g\) nonnegative and multiplicative, supported on split prime powers. At split \(p\), \(g(p^j)=(j+1)^{3/2}-2j^{3/2}+(j-1)^{3/2}\) for \(j\ge1\); this follows by comparing generating series with \((1-t)^{-2}\). At inert primes and 2 the pointwise power leaves \(f\) unchanged, so \(g\) is trivial there. The coefficients are bounded and \(g(p)=2\sqrt2-2\). Summing first against the elementary \(\sum_{m\le Y} f(m)\ll Y\) and then bounding the remaining Euler product, using the reciprocal-prime sum for split primes, gives
\[
 \sum_{m\le Y}r_2(m)^{3/2}\ll Y(\log Y)^{\sqrt2-1}.
\]
The total mean discarded per shift is \(O((\log X)^{\sqrt2-1-15/32})=o(1)\). It is also \(o(1)\) on any fixed class after normalization by that class's proportion, because the loss is nonnegative. Meanwhile \(w_X^2\le(\log X)^{15/16}r_2\), so the averaged diagonal contributes \(O((\log X)^{-1/16})\).

## Consequence from the two-shift estimate

Let \(F_Q\) be the finite center defined exactly as in the [single-witness limit](SINGLE_WITNESS_PROFINITE_LIMIT.md), using just the fixed \(C\) and the eventual shift distribution for \(d=j\bmod L\), and omitting the factor \(\pi\) to match \(Z_X\). They are compatible conditional expectations. For fixed \(Q\), annular lattice counting and the \(o(1)\) first moment loss give the mixed moment \(\mathbb E_X[Z_XF_Q]\to\mathbb E[F_Q^2]\), also with a mask on any fixed CRT class dividing \(Q\).

For the *off-diagonal upper bound* use \(w_X\le r_2\), and the [Chamizo two-shift estimate](https://link.springer.com/article/10.1007/s00009-021-01959-3). Distinct index pairs collide at odd \(p\ne5\) only when their difference is a multiple of \(\operatorname{ord}_p(5^L)\), with frequency \(O(1/\operatorname{ord}_p(5^L))\) because pairs are distinct. The [order-tail argument](AVERAGED_SHIFT_DISCRIMINANT.md) then approximates the whole off-diagonal by the finite kernels in the iterated limit, precisely as for two growing axes. Together with the negligible truncated diagonal this proves, for a divisibility chain \(Q\) increasing to all prime powers,
\[
 \lim_Q\limsup_X\mathbb E_X\bigl[(Z_X-F_Q)^2\bigr]=0.
\]
Only an upper bound on off-diagonal truncated correlations is needed; the mixed moment supplies the missing projection. In particular for any fixed class \(A\) of positive measure, if \(\mu=\mathbb E[F\mid A]>0\), conditioning and Cauchy–Schwarz bound the upper miss proportion there by \(1-\mu^2/\mathbb E[F^2\mid A]\), where \(F\) is the \(L^2\) limit of the centers. A conditional limit of the truncated weights does not on its own prove that this miss bound is zero.

## Finite controls

Retain the original class modulus in lcm refinements even at split primes, where there is no veto but the normalized weight varies. The first checks below give different finite means on two refinements at 5 of one coarse class. The second control has positive mean on \(n=440\bmod1008\) with \(C=0,\ d=1\bmod84\), but six of its seven refinements modulo \(7056\) permanently fail by valuation one at 7. The remaining fine class contains arbitrarily large actual witnesses in the specified size window. These are local obstructions to one specific window, not to the full conjecture.

~~~python
from collections import Counter
from fractions import Fraction as F
from math import isqrt

def rho(q,n,d):
    # CRT factors, each independently counted at the fixed shift.
    mods=(16,9,7) if q==1008 else (16,9,7,5)
    ans=F(1)
    for m in mods:
        t=(n-1-pow(5,d,m))%m
        cnt=sum((u*u+v*v)%m==t for u in range(m) for v in range(m))
        ans*=F(cnt,m)
    return ans
assert rho(1008,8,1)==F(64,21)
assert (rho(5040,8,1),rho(5040,1016,1))==(F(256,105),F(192,35))
assert rho(1008,440,1)==F(8,21)
assert pow(5,84,7056)==1
classes=[440+1008*j for j in range(7)]
assert [v for v in classes if (v-6)%49==0]==[2456]
assert all((v-6)%7==0 for v in classes)
assert 2456==6+7**2+49**2
for d in (85,169):
    n=1+5**d+(7+7056*5**d)**2+49**2
    assert n%7056==2456 and 5**(2*d)<=n-1<=5**(3*d)

~~~
