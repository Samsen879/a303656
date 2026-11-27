# A first-forbidden-prefix identity for the negative sieve weight

For a squarefree divisor sieve on the small prime factors of an individual input, order the factors in decreasing order. Suppose a truncated Möbius weight includes a divisor exactly when every prefix satisfies the prescribed support condition, and the first forbidden prefix always has even length. Let $\mathcal F$ be the set of these first forbidden prefixes, and $v(d)$ the last (smallest) prime in such a prefix $d$.

If $w^-(n)$ is the truncated signed sum over allowed divisors and $S$ the event of having no small prime divisor, then
$$
 w^-(n)=1_S(n)-
 \sum_{\substack{d\in\mathcal F\\d\mid n}}
 1_{\gcd(n,\prod_{\ell<v(d)}\ell)=1},
$$
where the product uses the same small-prime sieve set. To see this, subtract the excluded terms from the full Möbius sum. The excluded divisors group uniquely by first forbidden prefix; for one such prefix the remaining suffix is an arbitrary subset of the small input primes below $v(d)$. Its signed sum is the indicated coprimality test, and a prefix of even length contributes with sign $+1$. Thus every nonzero negative term carries the actual minimum factor of that input. Multiple different prefixes can contribute at one input.

Applied to the pair term in SIEVE_WEIGHT_SIGN_CALIBRATION.md, this identity reduces the negative part to a same-integer count of rejected prime inputs with a genuine minimal small inert factor and two exact large inert factor hits. A bound on four-factor inputs already *inside* the sifted set does not count these rejected inputs. The explicit example $2683^2+2188=11\cdot19\cdot131\cdot263$ has two small and two large inert factors at the indicated height. At a lower-sieve support below $\sqrt{2682}$ neither a divisor including both small factors nor its supersets can occur; the normalized weight at this input is $1-1-1=-1$, giving a negative pair contribution. The largest possible smaller block from partitioning the four primes into two pairs is only 2489, below $2682^{999/1000}$. This demonstrates both why the three-way correlation is real and why it need not fall in a very tightly balanced sector. No asymptotic lower or upper bound on the missing correlation follows from the example.

```python
from math import isqrt
X,p=2682,2683
a,b,q,r=11,19,131,263
assert all(v%4==3 and all(v%j for j in range(2,isqrt(v)+1))
           for v in (p,a,b,q,r))
assert p*p+2188==a*b*q*r
assert b**100<X**49 and q*q>X and r**10<X**9
assert (a*b)**2>X
u=max(min(a*b,q*r),min(a*q,b*r),min(a*r,b*q))
assert u==2489 and u**1000<X**999
```
