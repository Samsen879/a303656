# A norm identity controls the inert Delta-prime obstruction

On the actual even-c G1 family let D=B−A=−(2/5)((3^(c/2))²+1), L=4A−2B, C=B−L, q=7/(2*13^4), lambda=Dq², R=BC−lambda². Set K=(B+C−lambda−BC/lambda)/4, h=z+K/z, r=(h+L/h)/2 and Y=(h−L/h)/2. The exact algebraic identity is
```
(z−K/z)^2 − D*(q+r*Y/(D*q))^2
= (r²−B)*(2−(r²+C)/lambda).
```
It follows by replacing (z−K/z)^2 by h²−4K and Y² by r²−L. For each inert p≥17, D is a unit, as −1 is a nonsquare. Outside the six fixed primes, form a finite modulus from A, the numerator of B, and the numerator of R, deleting their fixed-prime parts and the support of the numerator of D. At each prime of that modulus take z a unit and avoid the zeros of
```
(z²+K)(z²−K)*((z²+K)²+L*z²)*((z²+K)²−L*z²).
```
This is monic of degree 12 with integral coefficients at these primes. Among 1,…,13 some value works per prime; CRT can combine the requirements, or one can split primary supports with gcds. Then h,r,Y,z−K/z are units at these primes.

If an inert p≥17 has v_p(Delta)>0 for Delta=r−B/r, the construction excludes p|B by the existing unit choice. Thus r is a unit, r²=B mod p and Y²=C mod p. If D were nonsquare, the identity would force z−K/z=0 and rY=−lambda mod p, hence p|R. This contradicts the unit choice at primes of R. (At p not already in the modulus, h and z−K/z are automatically integral when r is a unit: a pole of h=z+K/z makes r a pole, while a zero of h with unit L also makes r a pole; if L is nonunit, r unit still implies h and z integral.) Therefore H=Delta²+4D is a unit square. This removes the specific exceptional source studied in EXCEPTIONAL_DELTA_CIRCLE_OBSTRUCTION.md, not all possible obstructions to a global anchor.

At the smallest tested label u=23 the literal discriminants for retaining six previously chosen h phases pass:

```python
from fractions import Fraction as F

A = 5**562 + 3**188 - 131779
B = F(5**563 + 3**189 - 658897, 5)
D, C = B - A, 3*B - 4*A
lam = D * F(7, 2*13**4)**2
K = (B + C - lam - B*C/lam) / 4
for p, h, v, unit in (
    (2,1,0,1), (3,2,0,1), (5,1,0,1),
    (7,1,-2,1), (11,1,0,3), (13,4,-8,3),
):
    x = (h*h - 4*K) * F(p)**(-v)
    mod = 8 if p == 2 else p
    assert x.numerator * pow(x.denominator, -1, mod) % mod == unit
    assert v % 2 == 0
    assert unit == 1 if p == 2 else pow(unit, (p-1)//2, p) == 1
```

This note addresses the inert Delta source outside the six pinned places; it asserts no uniform fix for r poles, split primes, individual angle numerators, or global integer anchors in the growing family.
