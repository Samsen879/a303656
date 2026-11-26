# A true-order capacity bound and a complete weak phase cover

Consider a shared $\ell$ by $\ell$ exponent phase block, $\ell$ prime, with an inert prime $p$ and test $X\alpha^u+Y\beta^v\equiv n\pmod p$. Here both phase orders are exactly $\ell$ and $XY\ne0\pmod p$. Its root set is a partial matching: fixing one coordinate determines at most one of the other. If $p\nmid n$, there cannot be $\ell$ edges. Indeed that would use every row and column exactly once; summing the congruences gives $0\equiv\ell n\pmod p$, contrary to $\ell\mid p-1$ and $p\nmid n$. Therefore at most $\ell-1$ positions are divisible by this prime. On an $a$ by $b$ subset of rows and columns the cap is $\min(a,b,\ell-1)$. For positive $a,b$, $ab>m\min(a,b,\ell-1)$ therefore guarantees a survivor against $m$ such primes in that block. This is only a finite-panel first-divisibility claim. For the even-exponent 3,5 problem with $p>5$, if instead $p\mid n$, there are no roots: nonzero squares cannot sum to zero modulo $p\equiv3\pmod4$.

The numerical cap is attained for $\ell=3$: put $H=20930$ and restrict to exponents $(c,d)=(Hu,Hv)$. For the five primes $7,31,79,43,139$, $3^H$ and $5^H$ each have order $3$. Take
$$
n_t=2+(505707993+14242455829t)^2+8768372146^2 .
$$
Modulo these primes, the root counts are $2,2,2,2,1$ and their union is the full $3$ by $3$ block. This does not remove the actual square-sum witness at the origin. The only panel prime dividing $n_t-2$ is $139$, with valuation exactly $2$. The valuation holds for every integer $t$ because the first displayed square root is $139\bmod139^2$ and the second is $0\bmod139^2$. If $t\ge5^H$, all nine cells of the first block satisfy $3^c,5^d<n_t/4$. As $t$ grows, the same weak cover repeats in the active portion of the specified exponent sublattice. It provides no cover of the full exponent menu or odd-valuation cover even on this sublattice.

Replay (Python standard library):

```python
from itertools import product
from math import isqrt

P = (7, 31, 79, 43, 139)
H, a, b, M = 20930, 505707993, 8768372146, 14242455829
G = set(product(range(3), repeat=2))
assert all(p % 4 == 3 and all(p % j for j in range(2, isqrt(p)+1)) for p in P)
assert all(pow(z,H,p) != 1 and pow(z,3*H,p) == 1 for p in P for z in (3,5))
assert all(M % p == 0 for p in P)
assert (M % (139**2), a % (139**2), b % (139**2)) == (0,139,0)
n0 = 2 + a*a + b*b
R = [{(u,v) for u,v in G
      if (n0-pow(3,H*u,p)-pow(5,H*v,p)) % p == 0} for p in P]
assert set.union(*R) == G and list(map(len,R)) == [2,2,2,2,1]
assert [p for p in P if (n0-2)%p==0]==[139]
assert (n0-2)%139**2==0 and (n0-2)%139**3!=0
t=5**H
n=2+(a+M*t)**2+b*b
assert n>4*5**(2*H)>4*3**(2*H)
```
