# Factor-free joint-lift rejection on mixed short-order supports

Continue [short-order product capture](https://github.com/Samsen879/a303656/commit/7b3fbb0da95b09caa9cfce4b4c066165d489b4ec). For \(D>1\), let \(\operatorname{sat}_D(z)\) be the product of full prime powers in \(D\) whose primes divide \(z\). Starting with \(\gcd(D,z)\) and iterating \(g\mapsto\gcd(D,g^2)\) computes it without knowing the factorization. At each supported prime the valuation doubles up to the valuation in \(D\); unsupported primes remain absent.

Let each observed word \(W_j=3^{u_j}5^{v_j}\) have an order witness \(n_j\) on the saturated support \(D_j=\operatorname{sat}_R(W_j^{L H n_j}-1)\) and set \(M_j=L(n_j)_{7'}\), where \((n_j)_{7'}\) removes the powers of 7. Here \(L,H\) are as in the earlier capture, and the menu lists permitted lifts \(\lambda=(E,k)\) for a root \(x\) of order 343 on every prime of \(R\). On a prime in \(D_j\), the word raised to \(M_j\) has only 7-primary order. For a permitted lift, the corresponding projected equality is necessary. Put \(\Delta_{j,\lambda}=W_j^{M_j}-x^{M_j E(u_j+v_jk)}\). The prime-power rejection support proved by these observations is
\[
 J=\gcd_{\lambda}\operatorname{lcm}_j
 \frac{D_j}{\operatorname{sat}_{D_j}(\Delta_{j,\lambda})}.
\]
At each prime the lcm collects witnesses refuting a specified lift, while the gcd requires every permitted lift to be refuted. This does not conflate different permitted lifts on different primes. In particular absence of a lift working on a composite as a whole does not certify prime-by-prime rejection without this condition. Zero divisors do not compromise the formula.

## Independently replayed mixed-order example

For the exact pinned \(R,x\) below, the root equation and order are verified; the two proper coprime gcd supports cover \(R\) and have distinct prime local base-3 orders \(765971\) and \(2532083\). Their common order exceeds the stated capture bound. For the supplied tag \((30,59)\), the arithmetic checks reject each allowed lift separately at every prime of \(R\), without certifying primality of either gcd piece. This is exact tag-level rejection. Regeneration and exhaustiveness of the native tag menu, cohort-wide counts, and aggregate replay are not asserted here.

```python
from math import gcd, isqrt, lcm

R = 8703205831390420819770510177452311233617
x = 8299140966868213661066629058651983019237
assert pow(x,343,R) == 1 and gcd(R,pow(x,49,R)-1) == 1
assert (1+pow(x,93,R)-x-pow(x,47,R)) % R == 0

L, H = lcm(*range(1,20001)), 1
while L%7 == 0:
    L //= 7
while 7*H <= R//4_000_000_000:
    H *= 7

a,b = 765971,2532083
assert all(all(n%d for d in range(2,isqrt(n)+1)) for n in (a,b))
A = pow(3,L*H,R)
g,h = (gcd(R,pow(A,n,R)-1) for n in (a,b))
assert gcd(R,A-1) == 1 and 1<g<R and 1<h<R
assert gcd(g,h) == 1 and g*h == R and lcm(a,b) > 16384**2

M = L*lcm(a,b)
U,V = (pow(w,M,R) for w in (3,5))
assert pow(U,H,R) == pow(V,H,R) == 1
for E in range(30,343,49):
    assert gcd(R,U-pow(x,M*E%343,R),V-pow(x,M*59*E%343,R)) == 1
```
