# Growing shared-cubic panels with a true norm and an outside-panel obstruction

Let $X$ be sufficiently large, $Y=\lfloor\log X/100\rfloor$, and let the panel consist of inert primes $p\in(Y,2Y]$ with the orders $R_p,S_p$ of $9,25$ each divisible exactly once by $3$ and both at least $\sqrt Y/100$. This panel can be chosen with $\Theta(Y/\log Y)$ members. In the splitting field $\mathbb Q(\zeta_{36},\sqrt[3]3,\sqrt[3]5)$, the prime $7$ is unramified and its Frobenius class forces $p\equiv7\bmod36$ and both $3,5$ to be noncubes modulo $p$ (check at 7). The field has degree at most $108$, so Chebotarev's theorem gives at least $(1/108+o(1))Y/\log Y$ such primes. Low-order exceptions divide the product of $(9^j-1)(25^j-1)$ for $1\le j\le\sqrt Y/100$. The logarithm of this product is at most $(\log225)(Y/20000+O(\sqrt Y))$, so exceptions cannot exhaust this class.

For fixed $n\bmod p$ let $O_p(n)$ be the number of occupied cubic coarse blocks of the exponent period. By the root-pair bound, if $n$ is nonzero, the number of periodic roots is at most $O_p(n)+1$; if $n=0$ it is zero, since both summands are nonzero squares and $p$ is inert. Each periodic root has at most $\lceil I/R_p\rceil\lceil J/S_p\rceil$ copies in the strict $n/4$ box of even exponents, with $I,J=\Theta(\log X)$ for $n\in[X,2X)$. Since $R_p,S_p\le2Y$, the ratio of this multiplicity to $IJ/(R_pS_p)$ stays bounded. In particular the contribution of double occupancy is uniformly $O(\sum_p 1/(R_pS_p))=O(1/\log Y)$ as a fraction of the box.

Averaging occupied blocks over $n\bmod p$ gives $\sum_b O_p(b)\le R_pS_p$. Choose $b_p\notin\{0,2,10\}$ with $O_p(b_p)\le R_pS_p/(p-3)$. To realize the choices on one integer, pick an inert prime $q\in(2\log X,3\log X]$ and require $n\equiv10+q\bmod q^2$. In the local moduli the residue of $n-2$ is a unit and is a sum of squares: the finite field norm is surjective, and the solution lifts at $q$ since one derivative is a unit. Apply CRT to the two coordinates. The modulus $M=q^2\prod_p p$ is $o(\sqrt X)$, since the prime product divides $\binom{2Y}{Y}$. A first coordinate in $[\sqrt X,\sqrt X+M)$ and a second in $[0,M)$ then give $n=2+u^2+v^2$ in $[X,2X)$. The panel hits only $O(1/\log\log X)$ of its strict even-exponent box by the chosen occupation bounds. Its origin is an actual norm, whereas the cell with original exponents $(2,0)$ has no panel divisor but is blocked by $q$ at valuation one. The low-occupation construction is existential in each height interval, not a bound for every $n$, and does not settle A303656.

Finite companion replay: $263$ is the computed simple upper bound for the three-prime union, while a different $263$ occurrence denotes the actual outside-panel inert prime at the witness. The same numerical value is coincidental.

```python
from math import isqrt
P=(43,79,223)
t=1267650600228229401496703966007
N=2+(43*79*223*t)**2
X,Y=75,52
assert 4*9**(X-1)<N<=4*9**X and 4*25**(Y-1)<N<=4*25**Y
total=0
details=[]
for p in P:
    order=lambda a:next(r for r in range(1,p) if pow(a,r,p)==1)
    R,S=order(9),order(25)
    roots=[(i,j) for i in range(R) for j in range(S)
           if (pow(9,i,p)+pow(25,j,p)-N)%p==0]
    blocks={(i%(R//3),j%(S//3)) for i,j in roots}
    details.append((R,S,len(blocks),len(roots)))
    total+=len(roots)*((X+R-1)//R)*((Y+S-1)//S)
assert details==[(21,21,10,11),(39,39,19,19),(111,111,55,55)]
assert total==263
assert N.bit_length()-1==239 and (N-10)%263==0 and (N-10)%263**2!=0
primes=[p for p in range(3,240,4) if all(p%q for q in range(2,isqrt(p)+1))]
assert len(primes)==28 and all((N-10)%p for p in primes)
```
