# Two short periods cannot supply large norm support for most targets

For X<=n<2X require each active power to be at most n/4 and suppose D divides R=n−3^c−5^d with R/D<= (log X)^A. Apart from a fixed finite support, suppose the primes of D have common 3-period u and common 5-period v, not necessarily the same, both <=C log X. Their primes divide gcd(3^u−1,5^v−1). [Corvaja–Zannier, Corollary 1](https://arxiv.org/pdf/math/0311030) bounds this by X^o(1) uniformly, because the positive powers of 3 and 5 are multiplicatively independent and the height is O(log X). Bounded pairs are harmless. Hence the gcd has o(log X/log log X) distinct prime factors, by the factorial lower bound for a product of distinct primes. Including the fixed exceptional support and allowing arbitrary prime-power saturation still leaves X^o(1) divisors D<=2X for each period pair: each exponent has O(log X) choices.

There are polylogarithmically many periods and actual offsets. For each divisor/offset combination, D>=X/(2(log X)^A), so the target congruence supplies only O((log X)^A) integers in the band. Consequently this entire construction covers at most X^o(1) targets, even when the periods depend on n. A large squarefree block needs at least one period not bounded by C log X; long periods require a separate theorem about their least active representatives.

The exact controls use 13*17*37 and real bases 3 and 5. At 499449 an active remainder is 19²+706². At 504753 each prime separately has a hit in the box, but the joint congruence first needs d=68 with c<=10, whereas height allows d<=7. This rules out only the proposed divisor in that box; it does not exclude other representations.

```python
from math import lcm, prod

P = (13,17,37)
Q = prod(P)
def order(g,p):
    return next(k for k in range(1,p) if pow(g,k,p)==1)

U,V = (lcm(*(order(g,p) for p in P)) for g in (3,5))
assert (U,V) == (144,144)
assert tuple(next(j for j in (1,2) if pow(2,2**j*9,p)==p-1)
             for p in P) == (1,2,1)

good,bad = 499449,504753
assert good-3**3-5**4 == 61*Q == 19**2+706**2
assert 4*max(3**3,5**4) <= good
assert bad-good == 24*13*17 and good%24 == bad%24 == 9

def hit(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m == 0

assert 4*3**10 <= bad < 4*3**11 and 4*5**7 <= bad < 4*5**8
box = [(c,d) for c in range(11) for d in range(8)]
assert all(any(hit(bad,c,d,p) for c,d in box) for p in P)
assert [(c,d) for c,d in box if hit(bad,c,d,37)] == [(1,4)]
assert not any(hit(bad,c,d,Q) for c,d in box)
assert [(c,d) for c in range(11) for d in range(V)
        if hit(bad,c,d,Q)] == [(3,68)]
assert not any(hit(bad,c,d,Q) for c in range(U) for d in range(8))
print("True norm at one target; joint CRT phase above height at the other")
```
