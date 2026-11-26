# A cyclotomic construction of sparse new observer primes

Fix an odd prime $r\equiv3\bmod4$ and $a\ge1$. The positive integer
$$
 A_{r,a}=(3^{r^a}+1)/(3^{r^{a-1}}+1)
$$
is $3\bmod4$: the alternating sum has $r$ terms, each $1\bmod4$, since $3^{r^{a-1}}\equiv-1\bmod4$. Thus it has at least one inert prime divisor $q\equiv3\bmod4$. Every prime divisor has $\operatorname{ord}_q3=2r^a$. To check this, write $x=3^{r^{a-1}}$. Modulo $r$ the quotient polynomial equals 1 at this $x$: if $r=3$ then $x=0$, and otherwise $x\equiv3$, $x+1\ne0$, and Fermat gives $(x^r+1)/(x+1)\equiv1$. Hence $q\ne r$. If $q\mid x+1$, evaluating the quotient at $-1$ would give $q\mid r$, a contradiction. Thus $x$ has order $2r$ modulo $q$; translating back to the order of 3 gives precisely $2r^a$. For example, $A_{7,1}=547$, and $A_{7,2}=857643277\cdot127522693159$ with the latter an inert prime of order 98.

Here is a related precise finite-to-sparse-infinite comparison. Use common Haar profinite exponents $C,D$, and a fixed nonnegative integrable baseline weight $F_T$ from a finite set of old observer primes $T$ (with the conventional dyadic factor, and at 3 the eventual base-5-only convention). An observer at prime $p$ reads powers through their residue rings, so its $C$ periods divide $\operatorname{ord}_p3$ times increasing powers of $p$ when $p\nmid3$. Take all inert $r>\max(T\cup\{6\})$ and choose one inert $q_r\mid A_{r,2}$. The $q_r$ are distinct by their exact orders, are outside $T$, and satisfy $q_r\ge2r^2+1$.

Condition on $D$, the parity of $C$, and all $C$ coordinates outside this set of $r$. The old weight is unchanged across the remaining coordinates: no period of an old observer can read these larger prime coordinates. Meanwhile, the single unit-failure condition $3^C+5^D\equiv n\bmod q_r$ reads just $C\bmod r^2$ at the new coordinate, hitting at most one of its $r^2$ values. For finitely many such primes, independence of the distinct *coordinates after this conditioning* gives a unit-success proportion at least $\prod_r(1-r^{-2})$. No independence of original unconditioned norm events is asserted.

Write $M_T=\mathbb E F_T$ and multiply by new factors $(1+1/q_r)$ times the indicator of even valuation or zero residual at $q_r$. Since the unit-success branch is included in the new factor's support, the extended mass is between
$$
 M_T\prod_r(1-r^{-2})\prod_r(1+1/q_r)
 \quad\hbox{and}\quad
 M_T\prod_r(1+1/q_r).
$$
Both products converge, so the same comparisons follow for the countable extension by dominated convergence. In particular this explicit sparse extension preserves the zero set of the finite baseline, even if its mass is zero. This is a statement about a profinite local model, not about finding a true integer norm or extending to all inert primes.

```python
from math import isqrt
q=127522693159
assert (3**7+1)//(3+1)==547
assert (3**49+1)//(3**7+1)==857643277*q
assert q%4==3 and all(q%d for d in range(2,isqrt(q)+1))
assert pow(3,98,q)==1 and pow(3,49,q)!=1 and pow(3,14,q)!=1
```
