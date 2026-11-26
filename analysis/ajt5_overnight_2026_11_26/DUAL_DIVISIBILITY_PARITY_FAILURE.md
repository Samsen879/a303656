# Complete divisibility on both axes can still miss half-integrality

Use the two-axis reconstruction in [SYMMETRIC_RECONSTRUCTION_PRIME_POWER.md](SYMMETRIC_RECONSTRUCTION_PRIME_POWER.md). For \(q=1\), the reduced divisor conditions \(D/g\mid F(k/g,\ell/g)\) and \(D/f\mid F(h/f,j/f)\), where \(g=\gcd(k,\ell), f=\gcd(h,j)\), are necessary but not sufficient, even when imposed at full prime-power depth simultaneously.

Use shifts \((s_0,s_1,s_2)=(3^{10}+5^2,3^{10}+5,3^{10}+5^3)=(59074,59054,59174)\). With proposed direction \((h,k,j,\ell)=(13,41569,77,182494)\), both reductions have modulus \(D=828391\), and the two form residues are zero. Nevertheless the unique reconstructed rational coordinates are \(a=1290538395/2,\ b=362025/2\), so no integer placement with this direction realizes these shifts. Even the first norm-difference equation alone has an integer solution: the edge is primitive and \(\delta-P\) is even.

In general, for a primitive first edge, once \(\delta-P\) is even, let \((a_*,b_*)\) be an integer solution of \(-2ha+2kb=\delta-P\). All its integer solutions are \((a_*+kt,b_*+ht)\) with \(t\in\mathbb Z\). The second equation has change \(-2qDt\) along these solutions, so the exact joint integer criterion for the two norm equations is
\[
 2qD\mid j^2+\ell^2-q^2\gamma-2qja_*+2q\ell b_*.
\]
Check any desired sign, height, and, for \(q>1\), integrality of the third point's offsets separately.

As a true control for the same shifts, at \(n=366278248984909119\) the three norm points are \((605209237,168626),(605209224,210167),(605209189,294168)\). Its reduced leading coordinates are \(U=13,K=41541\). These examples concern exact integrality and make no distribution or moment claim.

```python
from fractions import Fraction as Q
from math import gcd
s,t,u=(3**10+5**c for c in (2,1,3))
assert (s,t,u)==(59074,59054,59174)
de,ga=s-t,s-u
h,k,j,l=13,41569,77,182494
P,T,D=h*h+k*k,j*j+l*l,k*j-h*l
assert gcd(h,k)==gcd(k,l)==gcd(h,j)==1 and D==828391
assert (de-P)%2==0
F=lambda r,w:P*w*(w-r)+r*de*w-r*r*ga
assert F(k,l)%D==F(h,j)%D==0
a=Q(l*(de-P)-k*(ga-T),2*D)
b=Q(j*(de-P)-h*(ga-T),2*D)
assert (a,b)==(Q(1290538395,2),Q(362025,2))
n=366278248984909119
points=((605209237,168626),(605209224,210167),(605209189,294168))
assert all(x*x+y*y+shift==n for (x,y),shift in zip(points,(s,t,u)))
assert gcd(13,48)==gcd(41541,125542)==1
```
