# A prescribed split factor and an independent stripping obstruction

At the fixed edge $K=10940$, put $F(v)=v^2+2188$. The identity
$$
 p=k+(b^2-547)/k \quad\Longrightarrow\quad
 F(p)=(p-2k)^2+(2b)^2
$$
gives true parent and child residuals $p^2$ and $5F(p)$ at $m=F(p)$ whenever the parameters are integral. It permits a fixed splitting factor not allowed by the simpler formula $p=b^2-546$.

In fact fix any $a>1$ all of whose prime factors are $1\bmod4$. There is an irreducible integer quadratic progression $p=aG(j)$, coprime cofactor $G(j)$ and $p\equiv3\bmod4$, giving true bridges while $F(G(j))$ always fails. Here is a construction. Choose an inert prime $\ell$ away from $a(a^2-1)2188$ for which $-547$ is a square (the two quadratic conditions give nonempty fixed residue classes). Choose a unit $q_0\bmod\ell^2$ with $v_\ell(F(q_0))=1$ by lifting a simple root modulo $\ell$ in a nonzero direction. Then
$$
 F(aq_0)=a^2F(q_0)-2188(a^2-1)
$$
is a unit modulo $\ell$. Combine $q_0\bmod\ell^2$ with $q_0\equiv1\bmod a$ and write $c=aq_0$ in that combined class. For each prime power dividing $a\ell^2$, solve $(2k-c)^2+(2b)^2=F(c)$ modulo that power with $k$ a unit. The right side is a unit at every such prime, and modulo a prime the norm circle has $p-1$ or $p+1$ solutions; at most two have $k=0$. A nonzero norm gives a nonzero derivative in at least one coordinate, permitting a lift. Thus the unit condition on $k$ is preserved.

Take a prime $k>\sqrt{547}$ in the resulting CRT class, additionally $k\equiv1\bmod4\cdot547$, by Dirichlet's theorem. Then $547$ has a nonzero square root modulo $k$ by quadratic reciprocity. Use CRT to take $b$ along an odd progression of step $2ka\ell^2$, agreeing with the chosen local $b$ residues at $a\ell^2$ and this square root modulo $k$. It follows that $G=p/a$ is an integer quadratic, is $3\bmod4$ and satisfies both cofactor congruences. Its discriminant has the negative sign of $547-k^2$, so it is irreducible. It has no fixed prime divisor: the prescribed cofactor residues at $a,\ell$ are units; at $k$ the reduced polynomial is nonconstant linear because the $b$ step contains exactly one factor $k$ and $b$ is nonzero modulo $k$; at any other odd prime its quadratic coefficient is a unit. At 2 the polynomial is odd. This establishes the desired true bridges and their stripping obstruction. By [Lemke Oliver, Theorem 1](https://lemkeoliver.github.io/papers/04-Quadratic.pdf#page=2), infinitely many cofactors in this progression are squarefree with at most two prime factors. Infinitely many prime cofactors would demand a prime-value result for this quadratic; none is asserted.

An exact paired control uses $a=41$, for which 546 is not a square modulo 41. Take $k=13$, $b=79+1066t$. Then $G(t)=2132t^2+316t+11$. At $t=0$, the working value is $451=41\cdot11$, and stripping works ($F(11)=47^2+10^2$). At $t=1$, the working value is $100819=41\cdot2459$ with prime cofactor; the true parent/child test at the working value passes, but $F(2459)=227\cdot26647$ has odd valuation at 227 and fails. Both controls depend on the same fixed edge.

```python
from math import isqrt
a=41
assert pow(546,20,a)==a-1
G=lambda t:2132*t*t+316*t+11
F=lambda p:p*p+2188
assert G(0)==11 and G(1)==2459
assert all(2459%d for d in range(2,isqrt(2459)+1))
assert F(a*G(0))==425**2+158**2 and F(G(0))==47**2+10**2
assert F(a*G(1))==100793**2+2290**2
assert F(G(1))==227*26647 and 26647%227!=0
```
