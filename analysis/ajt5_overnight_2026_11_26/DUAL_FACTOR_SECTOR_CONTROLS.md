# Three inert-factor sector controls and a two-diagonal density

In the determinant-$2188$ model of $p^2+2188=bqr$, moving a factor $s\mid b$ into the left block replaces $(q,br)$ by $(sq,(b/s)r)$. It can make both blocks large even when the original smaller factor cannot reach the required scale. It also changes the sieving conditions: every retained sieve prime dividing $s$ would wrongly remove the left block, and must instead be handled by its local divisibility condition.

For a good odd prime $\ell\nmid2188$ where $-2188$ is a square, uniform symmetric matrices of determinant $2188$ modulo $\ell^{\max(i,j,1)}$ have joint diagonal divisibility density
$$
 \Pr(\ell^i\mid a,\ \ell^j\mid c)=\frac{2\ell^{1-i-j}}{\ell+1},\qquad i+j>0.
$$
Indeed $ac-b^2=2188$, and each pair of admissible diagonal entries has $ac\equiv0\bmod\ell$ and exactly two unit choices of $b$ by Hensel lifting. Over the field the total number of determinant-$2188$ symmetric matrices is $\ell(\ell+1)$: the two roots of $b^2=-2188$ each give $2\ell-1$ diagonal pairs, and the other $\ell-2$ values each give $\ell-1$. Each field point has $\ell^{2(h-1)}$ lifts to modulus $\ell^h$, since the determinant hypersurface is smooth. These counts give the ratio above. At $\ell=13$, a single zero diagonal has density $1/7$; both zero have density $1/91$.

The replay verifies one real unbalanced example below $\sqrt X$, one just below $\sqrt X$, and one example where moving $13$ balances the blocks but keeping $13$ in the sieve would erase the target. The controls and local density do not prove a Bombieri–Vinogradov sector upper bound or a lower bound on true prime norms.

```python
from math import isqrt
from fractions import Fraction
def prime(n): return n>1 and all(n%j for j in range(2,isqrt(n)+1))
for p,b,q,r in [(22651,1,139,3691151),(619471,1,787,487603967),(907,13,67,947)]:
    assert all(prime(n) and n%4==3 for n in (p,q,r))
    assert p*p+2188==b*q*r
X=22650
assert X**49<139**100 and 139**200<X**99 and 3691151**10>(5**10)*X**11
X=619470
assert X**4999<787**10000 and 787**2<X and 487603967**10>(5**10)*X**11
assert (13*67)**10>906**9 and 947**10>906**9
l=13
D=2188
B=[(a,b,c) for a in range(l) for b in range(l) for c in range(l) if (a*c-b*b-D)%l==0]
assert Fraction(sum(a==0 for a,b,c in B),len(B))==Fraction(1,7)
assert Fraction(sum(a==c==0 for a,b,c in B),len(B))==Fraction(1,91)
```
