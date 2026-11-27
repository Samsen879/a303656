# A positive capacity gap for a specified smooth-order strategy

Use the first column 5p²+10941−9^t, 0≤t<N, with work prime p in a fixed reduced inert residue class mod M, and a finite set of inert auxiliary primes independent of p. If one of these rows is blocked at every sufficiently large work prime, some auxiliary q must have a **finite odd valuation already locked** in the class. Otherwise at every auxiliary q we can choose a compatible finite even valuation and patch them by CRT in a reduced class. Indeed 10p is a unit at each auxiliary q and a reachable root can be lifted to any sufficiently large finite depth; when q is not constrained at all and q≥7 we can take a nonzero nonroot. Dirichlet then produces unbounded work primes avoiding the entire specified support. The prime 3 cannot hit this column for work primes p>3. Locking q costs at least q²|M, and can cover at most one phase mod n_q=ord_q(9).

Remove the phases of orders 9,27,5,7,11. The small-order factorisations in the replay show respectively one, one, one, one, three eligible inert primes; order 3 cannot hit and orders 1 and 13 have none. The remaining residues in the four pairwise coprime coordinates 27,5,7,11 have fractions s=(23/27,4/5,6/7,8/11), taking subsets of that exact size if necessary. Include s_13=1. A single allowed phase mod n pays at most relative density (1/n)·product(1/s_l for l|n among those five primes) on that remaining set: at each common coordinate, conditioning can increase the fraction by at most 1/s_l.

Suppose every cheap effective q (n_q log q<lambda*N, lambda>0 fixed) has a {3,5,7,11,13}-smooth order and supplies at most one prime per order, except order 11 allowed three and order 15 allowed two. The sum of remaining smooth-order conditional rates is V below. There are O((1+log N)^5) cheap smooth orders, so passing from the combined residue densities to counts incurs at most O((1+log N)^5) interval error, with the four initial periods fixed. The surviving count is at least (delta−o(1))*N where delta=2224433/259459200>0. For the expensive group the total first-power capacity is at most sum(N/n_q+1). Its first terms cost at most log M/(2*lambda), and the number of such primes is o(log M): their smallest possible q tends to infinity since n_q≤q and n_q log q≥lambda*N. Hence successful classes have log M≥(lambda*delta−o(1))*F for N=floor(F/2)+1. No restriction is imposed on the orders in the expensive group.

In a genuinely general hypothetical strategy with log M=o(F), choose the cutoff sqrt(N*log M) instead. The expensive group covers o(N) rows, so the same positive proportion must be paid by nonsmooth or over-repeated orders below that cutoff. It is still unknown whether such primes can accomplish this. This is a restriction on an actual support in a fixed reduced class, not a proof on all prime representatives, full activation, or the original conjecture.

Independent exact margin and small-order check:

```python
from fractions import Fraction as Q
from functools import cache
from math import gcd, isqrt, prod

@cache
def phi(n):
    return (9**n - 1) // prod(phi(d) for d in range(1, n) if n % d == 0)

for n, qs, u, v in [
    (3, (7,), (3, 2), (1, 0)),
    (5, (11, 11), (1, 0), (6, 5)),
    (7, (547,), (33, 2), (1, 0)),
    (9, (19,), (26, 9), (6, 1)),
    (11, (23, 67, 3851), (1, 0), (25, 6)),
    (13, (), (756, 475), (630, 41)),
    (15, (31, 271), (60, 31), (1, 0)),
    (27, (19927,), (243, 19682), (120, 71)),
]:
    assert gcd(*u) == gcd(*v) == 1
    assert phi(n) == prod(qs) * prod(a*a+b*b for a, b in (u, v))
    for q in qs:
        assert q % 4 == 3 and all(q % d for d in range(2, isqrt(q)+1))
        assert pow(9, n, q) == 1
        assert all(pow(9, d, q) != 1 for d in range(1, n) if n % d == 0)

assert phi(1) == 8 and 10941 % 7 == 0 and pow(5, 3, 7) == 6
s = dict(zip((3, 5, 7, 11, 13), map(Q, ("23/27", "4/5", "6/7", "8/11", "1"))))
def w(n):
    return Q(1, n) * prod(1/s[p] for p in s if n % p == 0)
V = prod(1+1/(s[p]*(p-1)) for p in s)
V += w(15) - sum(w(n) for n in (1, 3, 5, 7, 9, 11, 13, 27))
assert prod(s.values()) * (1-V) == Q(2224433, 259459200)
```
