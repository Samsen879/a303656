# Local angle criterion for the quartic construction

In the two-norm quartic construction set S=r+B/r, Delta=r−B/r, H=S²−4A, start at a rational point on X²+Y²=H, and rotate by a rational half-angle a/b in lowest terms. Let nu=a²+b², m=(X−S)/2, s=Y/Delta. Exclude the fixed primes 2,3,5 or primes where the starting coordinates are not integral, or A,B,r,Delta,H are not units. At each other prime, use
```
2mQ(su) = m²/s² + 2mru² + s²(1+u²)(B+r²u²),  with u=t/s.
```

* If p|nu, it splits, and the two Gaussian coordinate factors of the rotation have valuations ±v_p(nu). Because the original point has unit norm, v_p(m)=v_p(s)=−v_p(nu). At u=a/b, the factor 1+u² has valuation v_p(nu), so Q is integral.
* If p does not divide nu and v_p(m)>0, then s is a unit since otherwise the circle would force 4A=0 modulo p. For an integral Q, negative v_p(u) is impossible, and reduction of the identity requires u²=−1 or u²=−B/r² mod p. If either is a square, Hensel lifting gives an exact p-adic root of that factor, hence an integral Q.
* If p does not divide nu and v_p(s)>0, then m is a unit. Rewriting the numerator as (m+rt²)²/s²+(r²+B)t²+Bs² shows that an integral Q is possible iff t²=−m/r mod p is solvable. Again an exact Hensel lift suffices.
* If both m and s are units, t=0 suffices.

The integrality tests are open in t at any local point found this way, so they can be met on rational approximants. For a fixed rational angle, after clearing denominators this yields an exact finite prime-by-prime test, using the literal quartic congruence at the remaining exceptional primes. CRT can combine finitely many compatible local angle and parameter choices, but changing the angle can introduce new primes through moving m and s. The fixed-angle criterion is not an unrestricted global construction.

Actual moving-coefficient controls (independently run with Python):

```python
from fractions import Fraction as F

A = 5**58 + 3**20 - 131779
B = F(5**59 + 3**21 - 658897, 5)
g = F(2, 21)
C = 4*A - 2*B
R, Z = (g+C/g)/2, (g-C/g)/2
r, S, D = B/R, B/R+R, B/R-R

def point(a):
    c, d = F(1-a*a,1+a*a), F(2*a,1+a*a)
    return (c*r-d*Z-S)/2, (d*r+c*Z)/D

def mod(x, p):
    x = F(x)
    return x.numerator*pow(x.denominator,-1,p) % p

a, b = 74882319375477717109655458905248537, 683912041660384391081062552665248537
m, s = point(a)
assert mod(s,19) == 0 and mod(-m/r,19) == 12
assert mod(m,23) == 0 and mod(B,23) == 16
m, s = point(b)
assert mod(s,19) == 0 and mod(-m/r,19) == 8**2 % 19
assert mod(m,23) and mod(s,23)
assert b % 29**2 == 12
t = s*b
w = -((m+r*t*t)**2/s**2 + (r*r+B)*t*t + B*s*s)/(2*m)
assert w.denominator % 29 != 0
```
