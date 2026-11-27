# Arbitrarily large exact inert cover numbers on an active sublattice

For the actual bases 3 and 5, let a cell with exponents $(c,d)$ be active if both $3^c,5^d<n/4$. Fix a finite panel of inert primes and an integer $k\ge2$. There is a single actual integer $n$ with a true norm at $(0,0)$, and an active periodic subset visible to none of the panel primes, whose exact minimum inert cover number is $k$. The same number holds if the covering rule is weakened from odd valuation to divisibility.

Use the $k$ anchors $(2,2j)$ with offsets $h_j=9+25^j$, for $0\le j<k$. Put $G=\prod_{a=1}^{k-1}(25^a-1)$. Prescribe $n\equiv0\bmod p^2$ for the panel primes and all inert divisors of $G$. Any inert prime dividing two distinct residuals must divide $G$. Yet for such a prime, $h_j$ is nonzero: for $p>3$ it is the sum of two nonzero squares, and for $p=3$ it is $1\bmod3$. Thus no inert prime can cover two anchors.

Choose distinct inert primes $q_j>5$ outside the panel and outside the prime divisors of $G\prod_i(h_i-2)$, and prescribe $n\equiv h_j+q_j\bmod q_j^2$. Put $T=\operatorname{lcm}_j q_j(q_j-1)$. In the active subset with $c\equiv2\bmod T$ and $d\equiv2j\bmod T$ for some $j$, the prime $q_j$ has exact valuation one throughout its column class. These are even exponents, so no panel prime divides any residual there. Once the anchors are active, the $k$-prime upper cover and the one-per-anchor lower bound coincide. All congruences hold for the same $n$.

For a true integer, in each local class $n-2$ is a unit. Express it as a sum of squares in the finite field (the norm is surjective), then lift one nonzero coordinate to modulus $p^2$. Apply CRT to the two coordinates, obtaining a modulus $M$. If $M=o(\sqrt X)$, choose the first coordinate in $[\sqrt X,\sqrt X+M+1)$ and the second in $[0,M)$; this puts $n=2+u^2+v^2$ in $[X,2X)$ and keeps a true origin. The active box side lengths are comparable to $L=\log X$.

Even with the growing cubic panel in $(Y,2Y]$, $Y=\lfloor L/100\rfloor$, one can take $k=\lfloor\log L/(20\log\log L)\rfloor$ for all large $X$. The excluded nonpanel primes have number $O(k^2)$ by the logarithm of the product defining them. The prime number theorem in the fixed inert progression gives $q_j=O(k^2\log k)$, all smaller than $Y$ eventually. Hence $T\le L^{1/2}$ for large $X$. Taking prime squares for the panel costs $\log M\le2Y\log4+O(k^2+k\log k)$, by the binomial-coefficient bound for the product of primes in $(Y,2Y]$. This is $o(\sqrt X)$ on the modulus scale. Both axes contain $\gg L/T$ copies of each specified phase, so the blocked subset has $\gg kL$ cells, all missed by the panel. This is a sublattice, not the entire box, and the true origin demonstrates the distinction.

```python
from math import gcd
u,v=2661184570134077505,5527125708039134158
n=2+u*u+v*v
assert n==37631021908786794960485171687669393991
panel=(3,43,79,223)
z=[n-9-25**j for j in range(3)]
assert all(4*max(9,25**j)<n for j in range(3))
assert all(v%p for v in z for p in panel)
assert [v%p**2 for v,p in zip(z,(7,11,19))]==[7,11,19]
assert [gcd(z[0],z[1]),gcd(z[0],z[2]),gcd(z[1],z[2])]==[1,13,1]
```
