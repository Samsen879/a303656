# Fixed cofactor bands and a two-prime conditional second-moment lower bound

Use \(M=672,\ n\equiv527\bmod M\) and the \(c,d\equiv2\bmod24\) separated two-axis grid in [the mixed-digit note](MIXED_INERT_DIGIT_OBSTRUCTION.md). Put \(U=\log X\), \(K_X=|\{s=3^c+5^d\}|\), \(N_X=|[X,2X)\cap\{n\equiv527\bmod M\}|\). Fix \(y\ge7\), and count only \(n-s=ab\) with \(X^\alpha\le a\le X^\beta\), \((\alpha,\beta)=(1/16,1/8)\), \(a\) a product of distinct split primes greater than \(y\), and \(b\) a split prime. This decomposition is unique, since \(b\) is larger than every other factor. Let \(T_X(y)\) count ordered distinct-shift pairs with both residuals in this class and coprime.

For sufficiently large fixed \(y\), the following lower bound is positive:
\[
\liminf_{X\to\infty}\frac{U T_X(y)}{N_XK_X^2}
\ \ge\ \lambda_y^2\,\frac{91648261}{91506250}
       -O\!\left(\frac{\log(3y)}{\sqrt y}\right),
\quad
\lambda_y=\frac{M C_y}{\varphi(M)}
  \int_\alpha^\beta\frac{du}{(1-u)\sqrt u}.
\]
Here \(C_y=\frac1{2\sqrt2}\prod_{p\equiv1(4)}(1-p^{-2})\prod_{p\equiv3(4)}(1-p^{-2})^{1/2}\prod_{p\le y,\,p\equiv1(4)}(1+1/p)^{-1}\). The subtraction uses the common-prime argument in [the earlier pair lower bound](COPRIME_LARGE_PRIME_PAIR_MASS.md). In particular \(y\) is chosen first and then held fixed; the estimate is not a pair asymptotic.

The Dirichlet series \(\prod_{p>y,p\equiv1(4)}(1+p^{-s})\) is \((\zeta(s)L(s,\chi_4))^{1/2}\) times an Euler factor absolutely convergent at \(1\); the residue constant after division by \(\Gamma(1/2)\) is \(C_y\). Selberg–Delange gives an asymptotic \(C_y A/\sqrt{\log A}\) for the count of eligible \(a\le A\). Partial summation, followed by the prime number theorem in the fixed unit class \(493a^{-1}\bmod M\) for \(b\) in \([(X-s)/a,(2X-s)/a)\), gives the first moment \((\lambda_y+o(1))K_X/\sqrt U\) per integer in the progression. The uniformity needed is over a fixed set of residue classes and intervals whose endpoints have ratio tending uniformly to two, since \(s=o(X)\) and \(a\le X^\beta\).

For \(q=11,23\), neither factor can contain \(q\). Conditioning on \(n\bmod q\), a given shift therefore has normalized local first factor zero at the collision class and \(q/(q-1)\) otherwise, again by the fixed-modulus prime number theorem. Averaging over actual shifts gives \(q(1-P_q(n))/(q-1)\), where \(P_q\) is the fraction of exponent phase pairs having the given offset. The square averages are respectively \(6259/6250\) and \(161069/161051\). The two exponent periods are 5 and 11 on both axes, so the joint conditional first moment factors by CRT on *both actual exponents*. Applying conditional Jensen produces the factor in the lower bound. The diagonal is negligible, and the common-prime subtraction for this narrower band is bounded by the same \(O(\log(3y)/\sqrt y)\) estimate as for the larger band. Since \(\lambda_y^2\asymp1/\log(3y)\), they give strict positivity for large fixed \(y\).

The missing step for a main term can be isolated. On admissible \(s\ne t,\ a,a'\) with \(\gcd(a,a')=\gcd(aa',s-t)=1\), take the CRT residue \(n=n_0+Maa'k\) assuring \(a\mid n-s,\ a'\mid n-t\). The two primes must then equal
\[
 L_1(k)=(n_0-s)/a+Ma'k,\qquad
 L_2(k)=(n_0-t)/a'+Mak.
\]
Even before evaluating the averaged singular series, one would need to bound the real discrepancy from the singular-series prediction, averaged over these *actual* shift pairs and cofactors, by \(o(XK_X^2/U)\). The two forms have proportional linear parts in the one variable; a theorem for pairwise linearly independent linear parts does not cover them. Neither a first-moment result nor the one-sided sieve bound gives this discrepancy.

## Finite controls

The finite cofactor example below uses the ordinary active box, not the asymptotic narrow rectangular grid.

```python
from fractions import Fraction
from math import gcd,isqrt
def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
weights=[]
for q,T in ((11,5),(23,11)):
    a=[0]*q
    for i in range(T):
        for j in range(T):
            a[(pow(3,2+24*i,q)+pow(5,2+24*j,q))%q]+=1
    weights.append(Fraction(q*sum((T*T-r)**2 for r in a),(q-1)**2*T**4))
assert weights==[Fraction(6259,6250),Fraction(161069,161051)]
assert weights[0]*weights[1]==Fraction(91648261,91506250)
X=96834161246447
small=[p for p in range(2,998) if prime(p)]
survivors=[]; true=[]
for k in range(128):
    n=X+331296*k
    a,b=5546605612829+19488*k,3339109008497+11424*k
    assert n%672==527 and 17*a==n-3**26-25 and 29*b==n-34
    if all(a%p and b%p for p in small):
        survivors.append(k)
        if prime(a) and prime(b):
            assert gcd(17*a,29*b)==1 and a%4==b%4==1
            true.append(k)
assert len(survivors)==10 and true==[0,9,64,110]
```
