# Exact positive-half veto for (231,131)

The negative half (5^231−3^131)/2 has an exact Eisenstein norm certificate in FIXED_LOCAL_PANEL_CRT_OBSTRUCTION. The matching positive half fails. For J=(5^231+3^131)/8 the integer d=9400327471230275558448251633 is an exact unitary divisor (d divides J and is coprime to J/d), and d is 2 mod 3. All integers here are odd. Consequently some inert prime 2 mod 3 occurs to odd valuation in d and hence in J. No proof that d itself is prime is needed; this excludes J as a sum of a square and three times a square. Multiplying both exponents by 3 adds only odd cubic-quotient Eisenstein factors, so the inert odd valuation persists on all its cubing descendants. This eliminates this label, not every label with normalized phase 154/3. No new phase has been confirmed.

```python
from math import gcd

A, S = 5**231, 3**131
J, r = divmod(A + S, 8)
assert A > S and r == 0 and J % 2 == 1
d = 9400327471230275558448251633
q, r = divmod(J, d)
assert r == 0 and gcd(d, q) == 1 and d % 3 == 2
print("PASS")
```
