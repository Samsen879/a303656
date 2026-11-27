# Compress the native (17,188) ideal without splitting its support

If z=x^172 at the native order-343 support, then z²=x and 1−z²+z^34−z^376=−(1−z)(z^33−z−1). The factor 1−z is a unit at that support, so g(T)=T^33−T−1 is an equivalent addressed equation. The norm in the degree-33 quotient is the determinant of multiplication by Φ_343(T) and equals the actual R. For h=1,7,49, the norm of the corresponding powered-root elimination remains R: substituting T^h into Φ_(343/h) gives Φ_343(T), so the nested resultant has the same value up to sign. At h=49 the degree-five cyclotomic representative has coefficients checked below; this is a lower-degree representation, not a factorization.

At each original supporting p, the address-labeled valuation profile of the native ideal divided by v_p(R) is the same single unit vector. Conjugation permutes these coordinates, relative norms sum fibers, and ideal multiplication, sum, and intersection apply addition, minimum, and maximum across the identical profiles. Those operations within the named cyclotomic towers preserve identical normalized profiles on every p, hence their norm support on the original primes cannot give a strict factor block. The true mixed-sign (31,295) remainder has the same singleton profile at 343,49,7 despite a mix of 1 and 3 mod 4 factors. Address uniqueness is therefore not a sign filter.

A genuinely sign-sensitive additional operation is gcd(M, ∏_(j=0)^342 (H(x^j)^2+1)); only split-sign primes can appear because a factor requires a square root of −1. For H(Y)=B+Y this can also be written as the norm of (i−B)^343−1. The eight listed shifts and two polynomial choices all give gcd 1 on each of two genuine remainders. This is an exact finite boundary for those expressions; no closure of (17,188) follows.

```python
from math import gcd, prod
from sympy import Poly, resultant, symbols

T,Y = symbols('T Y')
R = 626751537547263614426465772417729978972491
x = 252568635021313874012910903862214825457075
g = T**33-T-1
for h in (1,7,49):
    phi = Poly(sum(Y**(49*j//h) for j in range(7)),Y)
    P = Poly(resultant(g,Y-T**h,T),Y).monic().rem(phi)
    assert abs(resultant(phi,P,Y)) == R
    assert P.eval(pow(x,172*h,R)) % R == 0
assert tuple(P.nth(i) for i in range(6)) == (-32997189,-65911126,-24166065,-13300322,-57198484,-42836485)

for M,X,u,v in [(R,x,17,188),
    (421761845597*402997726421332771,68693850624006015651041237082,31,295)]:
    assert pow(X,343,M)==1 and gcd(M,pow(X,49,M)-1)==1
    def f(t):
        return (1-t+pow(t,u,M)-pow(t,v,M)) % M
    values = {b:f(pow(X,b,M)) for b in range(1,343) if b%7}
    for n in (343,49,7):
        for a in range(1,n):
            if a%7:
                assert gcd(M,prod(z for b,z in values.items() if b%n==a))==(M if a==1 else 1)
    z = pow(X,172,M)
    pts = [pow(X,j,M) for j in range(343)]
    for B in (0,1,z,1+z,1-z,3,5,3*pow(5,-1,M)%M):
        assert gcd(M,prod(((B+t)**2+1)%M for t in pts))==1
    for H in (f,lambda t:(pow(t,33,M)-t-1)%M):
        assert gcd(M,prod((H(t)**2+1)%M for t in pts))==1
```
