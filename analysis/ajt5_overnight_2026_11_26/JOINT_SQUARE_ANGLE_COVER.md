# One square condition for both moving angle coefficients

Use the circle and notation in QUARTIC_LOCAL_ANGLE_FILTER.md. For a rotating point (X,Y), m=(X−S)/2 and s=Y/Delta. Suppose it lies on the added rational condition
```
-m/r = xi² + kappa² Y²
```
for a fixed nonzero rational kappa. Enlarge the fixed exceptional set to include the primes where kappa is not a unit. At a nonexceptional prime dividing the angle denominator of the circle rotation (the nu branch), the previous direct anchor still applies. Otherwise, when m is divisible by p, Y²=−4A mod p is a unit and the new condition gives −1=(xi/(kappa*Y))² mod p. This suffices for the m branch. When s is divisible by p, -m/r is already a square modulo p by the same condition. Thus one rational square condition handles both moving numerator tests. The remaining checks are at the fixed exceptional set and include the required mod-30 progression.

With half-angle eta, write P=(S+X0)*eta²+2Y0*eta+S−X0 and J=Y0*(1−eta²)+2X0*eta. Then -m/r=P/(2r*(1+eta²)), Y=J/(1+eta²), and the condition is the degree-at-most-four equation
```
z² = (1+eta²)*P/(2r) − kappa²*J² .
```
It is an added sufficient condition, not an equivalence for every valid angle.

An exact rational base point over the already known fixed label (10,4;11,5):
```python
from fractions import Fraction as F
A = 5**10+3**4-131779
B = F(5**11+3**5-658897,5)
r,m,s,kappa = F(3,5),F(-1206998652,145),F(3489913905,3492286517),F(-38497,232660927)
X,Y = 2*m+r+B/r, s*(r-B/r)
assert X*X+Y*Y == (r+B/r)**2-4*A
assert -m/r-kappa*kappa*Y*Y == F(75760,29)**2
```
The fixed-label rational point is independently checked. This note does not certify the rank of the covering curve or solve the exceptional-prime conditions uniformly on a growing label family.
