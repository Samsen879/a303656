# Exact negative-half veto for (231,149)

For A=5^231, S=3^149, the odd negative half H=(A−S)/2 has the exact odd unitary divisor 14827837412621237≡2 mod 3. The replay verifies both divisibility and coprimality with the quotient. Regardless of whether the divisor is factored, it supplies an inert prime to odd valuation in H and excludes the entire label and its synchronous cubic descendants. The cubic quotient is an odd Eisenstein norm, so it cannot change the parity at that inert prime.

The positive odd half (A+S)/32 has a genuine split-norm block 197217043774268118721 with the integer coordinates below. An exact scalar cubic-root gcd retrieves that block on the full positive half. This shows why a positive block on one side is not a two-half certificate. No new ray is claimed; U=231 still has unresolved V=13,31,295.

```python
from math import gcd

A, S = 5**231, 3**149
H, J = (A-S)//2, (A+S)//32
assert 2*H == A-S > 0 and 32*J == A+S
p, q = 14827837412621237, 197217043774268118721
assert H%p == 0 and gcd(p, H//p) == 1 and p%3 == 2 and p%2 == 1
assert J%q == 0 and gcd(q, J//q) == 1
assert q == 9384457961**2 + 3*6031832020**2
z = pow(2, (q-1)//3, J)
assert gcd(J, z*z+z+1) == q and (2*z+1)%q == 42345015726653516127
```
