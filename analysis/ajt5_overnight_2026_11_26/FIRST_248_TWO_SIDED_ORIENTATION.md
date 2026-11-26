# Two-sided orientation inputs for unweighted correlations at the first root 248

Keep the fixed class and the shifts $H_d=5^{d+1}-239$, $d=4+kP$, $5^{d+1}\le\sqrt X$, from FIRST_248_PRIMITIVE_SIEVE_SEED.md. At a split prime away from the frozen modulus, take a single isotropic line $L_p$ and remove a representation pair $(V,S)$ when either $V$ or $S$ lies on this same line. Write $\Delta=S-V\ne0\bmod p$. Each single-side deletion count is $p(p-1)(1+1_{p\mid H_d})$ on the local solution set of size $p(p^2-1)$. The intersection requires $\Delta\in L_p\setminus\{0\}$ and $p\mid H_d$, in which case $V$ may be any point of the line. Inclusion–exclusion therefore gives the exact union density
$$
 g_d(p)=\frac{2+1_{p\mid H_d}}{p+1}.
$$
This is different from deleting both orientations on one vector. The former bounds eligible representation multiplicities on both norms, rather than on just one.

The exceptional shift-prime weights have bounded averages of every fixed exponential moment. In detail, put $L=\log X$. Let $h$ denote $H_d$ or $H_dH_e(H_d-H_e)$ for distinct shifts, with indices chosen uniformly as appropriate. For any fixed $C>0$,
$$
 \mathbb E\exp\left(C\sum_{p\mid h}\frac1p\right)=O_{P,C}(1).
$$
To prove this, the primes $p\in[R,2R)$ with $\operatorname{ord}_p(5)\le p^{1/4}$ all divide the product of $5^j-1$ for $j\le(2R)^{1/4}$. The logarithm of this product is $O(\sqrt R)$, so the inverse-prime sum over such primes converges by dyadic summation. The fixed prime 5 can also be ignored. For other primes, a divisor of $H_d$ imposes at most one exponent class modulo its order, and a divisor of $H_d-H_e$ forces the order to divide $d-e$. On the fixed step-$P$ progression of length $\asymp_P L$, each event thus has probability $O_P(p^{-1/4}+1/L)$, also when conditioning on the other index and excluding the diagonal. The sum over primes above $L^2$ is uniformly $O(1/(L\log L))$ since $|h|\le X^{3/2}$. Expand the remaining product $\prod_{p\mid h}\exp(C/p)$ by adding primes in increasing order. The increment at $p$ is bounded by $O_C((\log(2p))^C/p)$ times the divisor indicator, using Mertens' estimate for all prior factors. Averaging the increments gives a convergent sum from $p^{-1/4}$ and $O_C((\log L)^{C+1}/L)$ from the second term. This proves the bounded moment without treating divisor events as independent.

These are local and elementary inputs. An unweighted relative density theorem also needs uniform simultaneous-norm moment bounds; this note does not assert that asymptotic.

```python
for p, target in [(13,(2184,312,312,156,468)),(17,(4896,272,272,0,544))]:
    i=next(i for i in range(p) if (i*i+1)%p==0)
    n=l=r=b=0
    for a in range(p):
        for c in range(p):
            if (a,c)==(0,0):
                continue
            for x in range(p):
                for y in range(p):
                    if (2*(a*x+c*y)+a*a+c*c-2886)%p:
                        continue
                    left=(x+i*y)%p==0
                    right=(x+a+i*(y+c))%p==0
                    n+=1
                    l+=left
                    r+=right
                    b+=left and right
    assert (n,l,r,b,l+r-b)==target
```
