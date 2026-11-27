# A sign-safe sieve detector and the cost of using an upper weight

Let $S$ be the actual screened prime set and let $h(p)$ count divisors from a prescribed band of inert primes of $p^2+2188$. Write $H$ for its independent unit-class center. For any pointwise upper weight $W\ge1_S$, put $L=\sum W-|S|$ and $D_I(W)=\sum W(h-H)$. Since $h\ge0$,
$$
 D_I(1_S)\le D_I(W)+HL .
$$
Thus even a centered upper weight incurs a cost proportional to the excess mass, which is not eliminated by a cancellation statement for that weight.

For a signed lower weight $w^-\le1_S$ normalized to equal 1 on $S$, multiplying by $1-h$ is not a valid lower estimate when $h\ge2$. The exact example below has two small inert factors excluded by the candidate sieve and two larger factors inside the tested band. A squarefree divisor expansion of $w^-$ supported below $\sqrt X$ must have coefficients $-1$ on both individual small primes if normalized as a standard lower sieve. Their pair product exceeds the support, so the negative value $w^-=-1$ at this rejected input is multiplied by $1-h=-1$. The positive result does not represent a genuine surviving input.

The sign-safe second-order detector is $P(h)=1-h+\binom h2$, nonnegative at every nonnegative integer $h$. It equals the zero-hit indicator at $h=0,1,2$ and is at most 3 for $h\le4$. If $h\le4$ on $S$ and $T_4$ bounds the number of members with $h\ge3$, then for $B_j=\sum_p w^-(p)\binom h j$ one has
$$
 \#\{p\in S:h(p)=0\}\ge B_0-B_1+B_2-3T_4 .
$$
The inequality uses nonnegativity to handle the negative values off $S$. It does not bound the pair term $B_2$: paired large moduli are precisely the additional correlation needed by this lower-weight route. A zero-hit result for an incomplete band would still not certify a norm.

```python
from math import isqrt
X,p=195862,195863
a,b,q,r=191,227,811,1091
assert all(n%4==3 and all(n%d for d in range(2,isqrt(n)+1))
           for n in (p,a,b,q,r))
assert p*p+2188==a*b*q*r
assert all(n**100<X**49 for n in (a,b))
assert all(n*n>X and n**10<X**9 for n in (q,r))
assert (a*b)**2>X
```
