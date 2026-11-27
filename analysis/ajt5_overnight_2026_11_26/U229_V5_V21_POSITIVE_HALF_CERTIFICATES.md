# Exact new U229 half norms at V=5 and V=21

At A=5^229, the actual positive odd halves (A+3^5)/8 and (A+3^21)/8 both have full integer Eisenstein norm certificates. The replay constructs scalar cubic roots on the complete halves, turns them into square roots of −3 and uses Euclidean descent to reconstruct and verify the coordinates. No inference of the norm relies on a factorization claim alone.

For V=5 the negative half (A−3^5)/2 has the odd unitary divisor 1523853359980073≡2 mod 3, so some inert prime appears to odd valuation on that half. The whole actual label and its simultaneous cubing descendants are therefore excluded despite the positive-half proof. The corresponding negative half for V=21 remains open. Neither label has created a new phase; (229,93) positive status is unchanged.

```python
from math import gcd, isqrt, lcm, prod

A = 5**229
for v, base, leaves in [(5,6,(31,1861,166660051)), (21,12,(199,))]:
    J, rem = divmod(A+3**v, 8)
    d, rem2 = divmod(J, prod(leaves))
    assert rem == rem2 == 0 and J%2 == 1
    E = lcm(d-1, *(q-1 for q in leaves))
    while E%3 == 0:
        E //= 3
    z = pow(base,E,J)
    assert (z*z+z+1)%J == 0
    r = (2*z+1)%J
    a,x = J,min(r,J-r)
    while x*x > J:
        a,x = x,a%x
    y = isqrt((J-x*x)//3)
    assert x*x+3*y*y == J

H, p = (A-3**5)//2, 1523853359980073
assert H%p == 0 and gcd(p,H//p) == 1 and p%3 == 2 and p%2 == 1
```
