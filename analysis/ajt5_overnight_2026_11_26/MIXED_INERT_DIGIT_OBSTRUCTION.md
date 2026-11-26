# A two-prime digit interaction defeats squarefree-modulus centering

In the two-axis \(3,5\) grid \(c,d\equiv2\bmod24\), \(X^{1/8}\le3^c\le X^{1/4}\), \(X^{1/3}\le5^d\le X^{1/2}\), normalize the number of true two-square residuals by its mean on \([X,2X)\cap\{n\equiv527\bmod672\}\). Call it \(Y_X(n)\). In that class every residual is a reduced class \(1\bmod4\) modulo 672. Put \(W_X=672\prod_{q\le z_X,\ q\equiv3(4),\,q\nmid672}q\) for any \(z_X\to\infty\) with \(W_X=o(X)\). Then for **any** real function \(C_X\) of \(n\bmod W_X\),
\[
\liminf_X\ \mathbb E_X[(Y_X-C_X)^2]\ \ge\ \frac{12}{203729515}.
\]
For example \(z_X=\lfloor\sqrt{\log X}\rfloor\) satisfies the assumption. This does not test a center with extra prime-power digits, nor does it prove positive-density failure of the conjecture.

## Fixed-modulus projection

Extend [the omitted-prime calculation](FIXED_CENTER_VARIANCE_OBSTRUCTION.md) to fixed powers of inert primes. The normalized local occupancy factor is \(f_q(t)=(1+1/q)1_{\{v_q(t)\ {\rm even}\}}\). For a prescribed finite digit class the expected factor is obtained by averaging \(f_q\) over higher digits. This also gives the asymptotic first moment for actual norms: divide by a fixed even power of \(q\) when the valuation is prescribed, and by \(q^{2j}\) (the first allowed even depth) when the class is zero at level \(2j\) or \(2j-1\). Apply the reduced-class Prachar estimate to the remaining unit restrictions. Imposing coprime fixed moduli multiplies the factors by CRT; contributions from uniform digit averages arise by removing the associated digit constraints before applying the same asymptotic. Uniformity here is only over finitely many fixed moduli and residue classes. In particular the increase from one to two known \(q\)-digits is
\[
1_{\{q^2\mid t\}}-\frac1q1_{\{q\mid t\}}.
\]

At \(q=11\) and \(23\), the two exponent cycles modulo 121 have lengths 5 and 55, and cycles modulo 23 have lengths 11 and 11. Enumerate the product of the two common cycles of length 55. Define \(B(u,v)\) as the number of actual offsets equal to \(u\bmod121\) and \(v\bmod23\), and \(A(a,v)=\sum_{u\equiv a\bmod11}B(u,v)\). The table's first marginal is uniform over the eleven lifts of each mod-11 class. Thus, after multiplication by the mod-23 factor \(1+1/23-1_{\{23\mid n-s\}}\), the change of normalized conditional mean between mod \(11\cdot23\) and mod \(121\cdot23\), both within the fixed base class, is
\[
 \psi(u,v)=\frac{A(u\bmod11,v)-11B(u,v)}{11\cdot55^2}.
\]
The square mean on the fixed product modulus is \(\sigma^2=12/203729515\), computed below.

The exact conditional first moment at the fixed modulus implies \(\mathbb E_X[Y_X\psi]\to\sigma^2\) and the ordinary interval count gives \(\mathbb E_X[\psi^2]\to\sigma^2\). For large \(X\), \(W_X\) contains one copy of 11 and 23, so within each residue class mod \(W_X\) the second 11-digit cycles regularly; \(\psi\) has average zero on that cycle. Consequently \(\|\mathbb E_X[\psi\mid W_X]\|_\infty=O(W_X/X)\). Project \(Y_X\) onto the info of \(W_X\): its centered remainder has covariance with \(\psi\) tending to \(\sigma^2\), since \(Y_X\ge0,\ \mathbb E_XY_X=1\). By Cauchy–Schwarz the remainder's squared norm has liminf at least \(\sigma^2\), and orthogonal projection minimizes the error of any such center. No growing-modulus asymptotic for true norms is used.

## Independent integer replay

```python
from collections import Counter
from fractions import Fraction
from math import gcd,isqrt
B=Counter()
for i in range(55):
    for j in range(55):
        B[(pow(3,2+24*i,121)+pow(5,2+24*j,121))%121,
          (pow(3,2+24*i,23)+pow(5,2+24*j,23))%23]+=1
A=Counter()
for (u,v),k in B.items():
    A[u%11,v]+=k
assert all(sum(B[u,v] for v in range(23))*11
           ==sum(A[u%11,v] for v in range(23)) for u in range(121))
assert (B[34,3],B[78,3],A[1,3])==(1,2,10)
sq=sum((A[u%11,v]-11*B[u,v])**2 for u in range(121) for v in range(23))
assert Fraction(sq,121*23*(11*55**2)**2)==Fraction(12,203729515)
n1,n2=51701519,16655
assert n1-n2==16*672*11*19*23
assert n1%672==n2%672==527 and gcd(527-34,672)==1
assert (n1%121,n1%23,n2%121,n2%23)==(34,3,78,3)
assert n1-34==858**2+7139**2 and n2-34==11*1511
assert 1511%4==3 and all(1511%d for d in range(2,isqrt(1511)+1))
```
