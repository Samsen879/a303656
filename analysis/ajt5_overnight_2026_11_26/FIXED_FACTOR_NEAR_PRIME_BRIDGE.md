# A fixed-factor near-prime bridge and an obstruction to stripping the factor

For the fixed edge $K=10940$, use $F(p)=p^2+2188$. Put
$$
 b=13(2t+1),\qquad Q(t)=52t^2+52t-29,\qquad p=13Q(t)=b^2-546 .
$$
Then $F(p)=(p-2)^2+(2b)^2$ identically. At the same $m=F(p)$ the fixed parent residual is $p^2$ and the fixed child residual is $5F(p)$, an actual square sum by multiplication by $2+i$. The working parameter is always $3\bmod4$ and has valuation exactly one at 13, since $Q(t)\equiv-29\not\equiv0\bmod13$.

The actual input $t=9$ gives $p=60463=13\cdot4651$, with $4651$ an inert prime and child coordinates $(120428,61449)$. Yet for every $t\equiv9\bmod361$, replacing $p$ by its cofactor $Q(t)$ fails at the same fixed edge: $F(Q(t))\equiv342=18\cdot19\bmod361$, so its 19-adic valuation is exactly one. This obstruction is not automatic for other classes: $t=2$ gives prime $Q(t)=283$ with $F(283)=191^2+214^2$.

On the specified progression the polynomial $G(j)=Q(9+361j)$ has positive leading coefficient, is irreducible (the original discriminant $8736$ is nonsquare), and has no fixed prime divisor since $\gcd(G(0),G(1))=\gcd(4651,7138011)=1$. [Lemke Oliver, Theorem 1](https://lemkeoliver.github.io/papers/04-Quadratic.pdf#page=2) gives infinitely many squarefree values with at most two prime factors. Thus this progression yields infinitely many actual squarefree working parameters with at most three prime factors (including the fixed 13). Infinitely many *two*-factor parameters within this construction would require infinitely many prime values of $G$; that is not proved here. The stripping obstruction applies even at such prime values, if they exist. There is no unconditional asymptotic for actual prime working parameters in this note.

```python
from math import gcd,isqrt
def isprime(n):
    return n>1 and all(n%j for j in range(2,isqrt(n)+1))
Q=lambda t:52*t*t+52*t-29
F=lambda p:p*p+2188
p=13*Q(9)
assert p==60463 and Q(9)==4651 and Q(9)%4==3 and isprime(Q(9))
assert 5*F(p)==120428**2+61449**2
assert F(Q(9))%361==342 and F(283)==191**2+214**2
assert Q(2)==283 and isprime(283)
assert isqrt(8736)**2!=8736 and Q(370)==7138011
assert gcd(Q(9),Q(370))==1
```
