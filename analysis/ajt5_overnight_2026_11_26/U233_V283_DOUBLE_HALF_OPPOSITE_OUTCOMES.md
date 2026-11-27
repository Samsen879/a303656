# One full norm half and one inert veto at (233,283)

For A=5^233,S=3^283 the negative half H=(A−S)/2 has an exact integral Eisenstein norm. A scalar cube root z=11^((H−7)/21) modulo H satisfies z²+z+1=0, converting to a square root of −3 by 2z+1; the Euclidean descent below recovers the actual coordinates and checks them back against H.

The positive half J=(A+S)/32 nonetheless has the odd unitary divisor 57862200044964278147≡2 mod 3. Coprimality with the quotient ensures at least one inert prime has odd valuation in all of J, whether or not this witness is separately proved prime. Thus this label and its cubic descendants are vetoed. No new phase or overall density was established.

```python
from math import gcd, isqrt

A, S = 5**233, 3**283
H, J = (A-S)//2, (A+S)//32
assert 2*H == A-S > 0 and 32*J == A+S and H%2 == J%2 == 1

assert (H-7)%21 == 0
z = pow(11, (H-7)//21, H)
assert (z*z+z+1)%H == 0
r = (2*z+1)%H
a, x = H, min(r,H-r)
while x*x > H:
    a, x = x, a%x
y = isqrt((H-x*x)//3)
assert x*x+3*y*y == H

p = 57862200044964278147
assert J%p == 0 and gcd(p,J//p) == 1 and p%3 == 2 and p%2 == 1
```
