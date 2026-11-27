# A stronger lower bound on actual rational anchor height

Use the notation $U,V=U^q,x=cV,c=365,A,F,g=\gcd(F,A),M=F/(4g)$ in CYCLOTOMIC_RATIONAL_ANCHOR_HEIGHT.md. For a reduced parameter $t=n/b$ producing an integral $w$, the following stronger bound holds in the same positive-$q$, plus-sign chart:
$$
 |n|^3\ge \frac{V^2}{8000\cdot366\,gAb}.
$$
For fixed $k$ (so $U,A$ are fixed) this requires $\max(|n|,b)\gg_k U^{2q/3}$. It is a necessary bound for actual anchors only; it neither gives existence nor resolves the optimal exponent.

Besides the quotient $I=(n^2+b^2)(An^2+(4x-A)b^2)/M\in\mathbb Z$, the five-adic factorization gives $m=(2n^2+2\varepsilon nb+b^2)/V\in\mathbb Z_{>0}$ for one $\varepsilon\in\{\pm1\}$. We also have $b^2\mid A$. Indeed at 5 and 73 the valuations of $r=A/x$ and $H=F/x$ are equal and negative (at 73 both are exactly $-1$), so if $t$ is not a unit one of the two square terms in the numerator has a unique strictly lowest valuation, incompatible with integral $w$. At all other primes $r,H/2$ are integral, so $rt^2$ cannot have a pole and the square of any denominator factor of $t$ divides $A$. Since $V>13A$, the positive integer $m$ and this denominator bound imply $|n|\ge2b$.

Put $z=\varepsilon b/n$, $u=m/n^2$, $\rho=b^2/m$, and $f=2+2z+z^2$, so $u=f/V$. Let $D=f^2-4uf/c+Au^2/c^2=f^2F/x^2$ and $\Delta=c^2I/(gm^2)-(A+8c\rho)$. Substituting $x=cf/u$ into $IF=4g(n^2+b^2)(An^2+(4x-A)b^2)$ gives
$$
 D\Delta=-z\,[A(8+8z+4z^2+5z^3)+8c\rho f(2-z)]
 +(A+8c\rho)(4uf/c-Au^2/c^2).
$$
For $|z|\le1/2$ one has $5/4\le f\le13/4$, $D\ge25/32$, and the square bracket is between $3(A+c\rho)$ and $65(A+c\rho)$, by bounding the displayed polynomials on this interval. The last term has absolute value at most $(104/c)(A+c\rho)u$ since $0<A<4x$.

If $\Delta=0$, this forces $|z|\le104u/(3c)<140/(cV)$ and hence $|n|>V$. Otherwise, whenever $|n|\le V$, the nonzero integer $gm^2\Delta=c^2I-g(Am^2+8cmb^2)$ has magnitude at least 1. The identity bounds its magnitude by $100gm^2(A+c\rho)(|z|+u)$. Using $\rho\le A$, $u<4/V\le4b/|n|$, and $m<4n^2/V$, this is at most $8000(1+c)gAb|n|^3/V^2$. This proves the lower bound; $|n|>V$ already satisfies it. The integer gap, not just the availability of a congruence root, is the additional ingredient.
