# Partial norm certificates for (231,31)

For A=5^231 and S=3^31, the negative half (A−S)/2 contains coprime exact Eisenstein norm blocks 175456243 and 19724425849; the positive half (A+S)/8 contains block 366829. The replay verifies integer coordinates and that the remaining factors (143 and 155 decimal digits) are composite and nonsquare. Neither half has a full classification from these facts; no new ray was certified.

For an odd v and any D|5^231+ε 3^v with gcd(D,30)=1, w=5^116 3^(-(v−1)/2) mod D has w²=−15ε. Thus square roots of 5ε and −3 convert via r↦w/r when the denominator is a unit. A short norm probe gcd(D,x²−c y²) is usable as a modular root certificate only when y is a unit on its selected block. The finite replay independently recovers the known positive split block and contrasts the separately rejected (231,131).

```python
from math import gcd, isqrt, lcm

A, S = 5**231, 3**31
M, P = (A-S)//2, (A+S)//8
assert 2*M == A-S > 0 and 8*P == A+S and M%2 == P%2 == 1
a, b, d = 175456243, 19724425849, 366829
assert a == 7996**2 + 3*6097**2
assert b == 119971**2 + 3*42156**2
assert d == 479**2 + 3*214**2
assert gcd(a, b) == 1

for H, f, digits in [(M, a*b, 143), (P, d, 155)]:
    C, rem = divmod(H, f)
    assert rem == 0 and gcd(C, f) == 1 and len(str(C)) == digits
    assert C%3 == 1 and isqrt(C)**2 != C and pow(2, C-1, C) != 1

z = pow(2, lcm(*(k for k in range(1, 710) if k%3)), P)
assert gcd(P, z*z+z+1) == d and (2*z+1)%d == 35995

J, rem = divmod(A+3**131, 8)
q = 9400327471230275558448251633
assert rem == 0 and J%q == 0 and gcd(q, J//q) == 1 and q%3 == 2
```
