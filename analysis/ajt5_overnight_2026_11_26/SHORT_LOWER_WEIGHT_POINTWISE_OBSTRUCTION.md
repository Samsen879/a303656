# A real two-small-factor obstruction for any short pointwise lower weight

For the set $A$ of distinct small inert factors at an input, let $W(A)=\sum_{d\mid\prod A}\lambda_d$, with real coefficients supported on $d\le D$. Assume $a=\lambda_1>0$ and require $W(A)\le1_{A=\varnothing}$ on the actual inputs. If the singleton modes $\{u\},\{v\}$ occur then $\lambda_u,\lambda_v\le-a$. For a double mode,
$$
 W(\{u,v\})\le-a+\lambda_{uv}.
$$
Thus making this mode nonnegative requires $D\ge uv$. This does not depend on the rule choosing a first forbidden prefix, and it does not use a synthetic independence assumption.

At the actual interval $X=2682<p<2X$, work class $p=3\bmod4$, the three primes in the replay give singleton modes $\{11\},\{19\}$ and the double mode $\{11,19\}$ for a small-prime cutoff $X^{1/2-10^{-6}}$. Specifically, the double-mode prime $2683$ also has both $131,263$ in the large band $(\sqrt X,X^{1-10^{-3}}]$. With $D\le\sqrt X$ the product $11\cdot19$ is unsupported, so this double hit contributes at most $-a$ to the signed pair statistic. An upper estimate on four-factor inputs already inside the sifted set cannot erase this negative contribution on an actual outside input. The example rules out a universal short pointwise repair, not a successful averaged estimate.

```python
from math import isqrt
X=2682
rows=((2707,(11,13,13,3943),{11}),
      (3359,(19,593951),{19}),
      (2683,(11,19,131,263),{11,19}))
for p,F,small in rows:
    assert X<p<2*X and p%4==3
    for n in (p,*F):
        assert all(n%d for d in range(2,isqrt(n)+1))
    prod=1
    for n in F:
        prod*=n
    assert p*p+2188==prod
    assert {q for q in F if q%4==3 and q*q<X}==small
    assert all(q**100<X**49 for q in small)
assert 209**2>X and 131**2>X and 263**10<X**9
```
