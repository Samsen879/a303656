# A rank-one shared-phase obstruction transfers to other bases

With bases 2 and 5, fix odd c,d and F0=n−2^c−5^(d+4), F1=n−2^(c+2)−5^d. The common finite-even valuation test at 3 and 7 fails exactly when n≡7 mod 9, 7|n, and 49 does not divide n.

At 3 both rows are units unless n≡1 mod 3. Writing c=1+2u,d=1+2v, both sums are 4+3(2u+v) mod 9, so simultaneous required depth-two fixes one line. At 7 both contact only when n≡0 mod 7, because the second sum is four times the first there. The common zero line is exactly the line selected by n≡7 mod 9 (see the table below). On that line the residual coupling is F1−4F0=−3n+2499*5^d, with 49 dividing 2499. Thus 49∤n prevents even valuations in both rows irrespective of higher digits. If 49|n, the two first lifts agree. At either prime, compatible required first lifts can be placed at valuation exactly two by avoiding at most two lines at the next pair of digits. The normal slope of each such line is nonzero since the relevant base lifts at 3 and 7 are ordinary. After the common step-6 phase is fixed the additional digits combine by CRT.

At the actual n in the replay, each label individually has a genuine square-sum representation, yet the prescribed joint seed fails. Changing just c parity admits a joint local witness. The integer also has a genuine original-base representation n=306²+1419²+3²+5². A simultaneous-label obstruction is therefore not an obstruction to the conjecture, which asks for a single representation.

```python
from itertools import product

P = list(product((1, 3, 5), repeat=2))
def S(c, d, m):
    return ((2**c + 5**(d+4)) % m, (2**(c+2) + 5**d) % m)

assert {t for t in P if S(*t, 9) == (7,7)} == \
       {t for t in P if S(*t, 7) == (0,0)} == {(1,3), (3,5), (5,1)}
assert 2499 % 49 == 0
n = 2107231
assert (n % 9, n % 49) == (7, 35)
assert 4 * max(2**19, 5**5) < n
assert n == 735**2 + 1197**2 + 2**17 + 5**5
assert n == 357**2 + 1407**2 + 2**7 + 5
assert all((n-z) % p for p in (3,7) for z in S(0,1,p))
```
