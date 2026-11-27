# A sharp cutoff for the first inert obstruction in the K = 10940 family

Let $p>547$ be an odd prime and let $F=p^2+2188$. If $F$ is not a sum of two squares, it has at least one prime $q\equiv3\bmod4$ of odd valuation satisfying
$$
 q\le p+2-2\sqrt{p-546}.
$$
The existence of such a divisor is exactly an obstruction to the norm; multiplying $F$ by $5$ leaves the obstruction unchanged.

Indeed, $F\equiv1\bmod4$ and $F$ is odd, so the number of inert primes of odd valuation is even. Choose two, $q<r$. If $qr<F$, then $qr\le F/3$, hence $q\le\sqrt{F/3}<2p/3\le p+2-2\sqrt{p-546}$ for $p>547$.

If $qr=F$, then $\Delta=q+r-2p$ is positive by the arithmetic–geometric mean inequality and is divisible by four. Writing $a=p-q$, the factorization gives $a^2+2188=(p-a)\Delta$. Using $\Delta\ge4$ gives $(a+2)^2\ge4(p-546)$. Also $q\le\sqrt F<p+2$ for $p>547$, so $a+2>0$ and the cutoff follows.

Equality holds for the prime triple $(p,q,r)=(57667,57191,58147)$: here $\Delta=4$, $p-546=239^2$, and both obstructions exceed $0.99p$. This is a limit on a cutoff that inspects only inert primes much smaller than the input. It makes no claim about how often this boundary occurs, a lower bound for norm-producing prime inputs, or A303656 itself.

```python
from math import isqrt
p,q,r = 57667,57191,58147
for v in (p,q,r):
    assert v % 4 == 3 and all(v % j for j in range(2,isqrt(v)+1))
assert p*p + 2188 == q*r
assert q+r-2*p == 4 and p-546 == 239**2
assert q == p+2-2*239 and 100*q > 99*p
```
