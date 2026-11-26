# A true protected norm in every sufficiently large active interval

Start with the persistent residual progression of PERSISTENT_NEAR_COVER_RESIDUAL.md, in which one may extend nested CRT conditions to cover all but an arbitrarily small periodic fraction of both columns while protecting t=0 in the first column. In fact the protected row is a unit at every guard prime for any work parameter p. Take each stage mod M fixed before increasing the window, and choose the genuine quadratic progression of GUARDED_NORM_PROGRESSION.md for that class. This gives p=k+(v²−547)/k, v=v0+kM*j. For fixed stage, consecutive sufficiently large p have gaps O(sqrt(p)). Thus for every sufficiently large N some member lies in 3^N/3<p<2*3^N/5, where both columns have exactly 0≤f<2N active.

At stage s with periodic missed fraction ≤1/s, the first N even rows miss at most N/s+D_s, where D_s is a fixed common period. Taking stages sufficiently slowly makes this o(N) while maintaining log M=o(N) and any given divergent budget g(N). The same actual m simultaneously has genuine parent norm p² and true child at the protected row. No uniform growing-modulus threshold or infinite prime p claim follows. Conversely one can add p≡31 mod 47² (coprime to these guard moduli), still find work primes in each interval by the prime number theorem for a fixed progression, and force the protected row to fail with v47=1. This converse concerns the selected protected row only.

The following exact pair in one activation window uses the same E=28 blocked row. It gives a two-factor witness and a prime failure, not a general almost-prime existence theorem.

```python
from math import isqrt

q, N, v = 37547, 27, 1612577
C = (10941, 10937)
p, b = v*v-546, 2606043689219
assert p == 863*3013215041
for r in (q, 863, 3013215041, b, 131):
    assert all(r % d for d in range(2, isqrt(r)+1))
assert p % (4*q*q) == b % (4*q*q) == 775406987
for c in C:
    for j in range(5):
        assert pow(5*(9**j-c), (q-1)//2, q) == q-1
    assert all(3**53 < 5*r*r+c < 3**54 for r in (p, b))
for r in (p, b):
    assert 3**(N-1) < r and 5*r < 2*3**N
    d = 5*r*r+C[0]-9**14
    assert d % q == 0 and d % (q*q) != 0
x, y = 2*(p-2)-2*v, (p-2)+4*v
assert x*x+y*y == 5*p*p+10940
assert (5*b*b+10940) % 131 == 0 < (5*b*b+10940) % 131**2
```
