# Cubic-panel occupation moments and a fixed-class typical bound

Use the growing panel in GROWING_CUBIC_PANEL.md. For one prime $p$, let $H=\langle9\rangle$, $K=\langle25\rangle$, of orders $R,S$, and $g=|H\cap K|$. Write $T(b)$ for the number of roots $u+v=b$ with $(u,v)\in H\times K$, and $O(b)$ for the number of occupied blocks under cosets of the order-three subgroup in each axis. There are no roots at $b=0$ (both inputs are nonzero squares and $p$ is inert). For $b\ne0$ the unique possible double-root block is $(-b\mu_3,-b\mu_3)$: its two roots use the two nonidentity cubic roots, whose sum is $-1$. It is accessible precisely when $-b\in H\cap K$. Thus $T(b)-O(b)=1_{-b\in H\cap K}$. If $D_H(z)$ and $D_K(z)$ count ordered differences, then
$$
 \sum_b O(b)=RS-g,\qquad
 \sum_b O(b)^2=\sum_z D_H(z)D_K(z)-2gT(-1)+g.
$$
The identity for $\sum T(b)^2$ is obtained by matching differences, and $T$ is constant on $-(H\cap K)$ by scaling.

Fix a modulus $W$ and any single residue class. For large $X$, $W$ is coprime to the panel product $Q$ and $Q\le4^Y$, where $Y=\lfloor\log X/100\rfloor$. The joint phase distribution of integers in this class in $[X,2X)$ has relative error $O(Q/N)$ against the uniform product distribution, where $N$ is the size of the progression segment: each of the $Q$ phases occurs either $\lfloor N/Q\rfloor$ or $\lceil N/Q\rceil$ times. Put $Z=\sum_p O_p(n)/(R_pS_p)$ and $\mu=\sum_p(1-g_p/(R_pS_p))/p=\Theta(1/\log Y)$. Each summand is bounded by $B=100/\sqrt Y$, since fixing one exponent forces at most one root modulo the other axis order. For independent uniform phases the convexity inequality $e^{\lambda u}\le1+u(e^{\lambda B}-1)/B$ for $0\le u\le B$ gives
$$
 \Pr(Z\ge t)\le \exp(-(t\log(t/\mu)-t+\mu)/B),\qquad t>\mu.
$$
Multiplying by $1+O(Q/N)$ transfers this bound to the actual interval and residue class. With $t=2\mu$, the exceptional proportion is $\exp(-\Omega(\sqrt{Y}/\log Y))$. Outside it, the strict even-exponent box has at most $O(1/\log Y)$ of its cells hit by a panel prime, by the truncated-box bound and the single extra root per prime. This is a typical finite-panel statement. All-point occupation would require bounding the sum of the local maxima; every joint phase occurs for large $X$.

The two actual integers in the replay share their residue modulo 63, height interval, box size and the panel residues modulo the squares of $43,79,223$. At exponents $(2,0)$, one is a genuine norm and the other fails at the outside prime $263$. Thus those observations alone cannot certify a genuine norm.

```python
from itertools import product
from collections import Counter
from math import isqrt,prod

p=31
def powers(a,p):
    return {pow(a,j,p) for j in range(p-1)}
H,K=powers(9,p),powers(25,p)
T=Counter((a+b)%p for a,b in product(H,K))
H0={pow(a,3,p) for a in range(1,p)} # only used to validate cubic phase length
assert len(H0)==10 and len(H)%3==len(K)%3==0
D=[]
for U in (H,K):
    D.append(Counter((a-b)%p for a,b in product(U,U)))
phase={(pow(a,3,p),pow(b,3,p),(a+b)%p) for a,b in product(H,K)}
O=Counter(z for _,_,z in phase)
assert all(T[b]==O[b]+((-b)%p in H&K) for b in range(p))
assert (sum(D[0][z]*D[1][z] for z in range(p)),T[p-1],
        sum(O.values()),sum(v*v for v in O.values()))==(87,2,42,78)
panel=(43,79,223)
Q=prod(panel)
minus=2+(Q*1267650600228229401496703966007)**2
plus=10+939906129562517623222790907638107157**2+3061626106977**2
assert minus%63==plus%63==20
for n in (minus,plus):
    assert 2**239<=n<2**240
    assert 4*9**74<n<=4*9**75 and 4*25**51<n<=4*25**52
assert all((plus-minus)%p**2==0 for p in panel)
assert (minus-10)%263==0 and (minus-10)%263**2!=0
small=[p for p in range(3,240,4) if all(p%q for q in range(2,isqrt(p)+1))]
assert len(small)==28 and all((minus-10)%p for p in small)
```
