# Refined cyclotomic divisors and a guarded single-prime exclusion

### The true-divisor restriction

Set \(r=3\), \(g=3\cdot7\cdot13\cdot17\cdot101=468741\), and \(n=1331g\). Take \(a=nh+1,\ b=nk-2\), with \(x=3^h,\ y=5^k\). Using homogeneous cyclotomic polynomials, the two actual divisors are
\[
w=\Phi_{2n}(x,y)\mid D_3,\qquad
R=\Phi_{2n/11}(x,y)\mid F_2.
\]
In fact,
\[
F_2=\prod_{j\mid g/3}\Phi_{726j}(x,y).
\]
These factors are pairwise coprime. Their primitive primes have orders \(726j\), and the exceptional primes dividing the indices are all below \(727\), the smallest possible prime of \(F_2\). An allocated prime power therefore belongs to just one of the two coprime factors \(R\) and \(F_2/R\).

Write the short factor as \(v=\ell wf\), with \(\ell\mid L=24D_0D_1C_2\) and \(f\mid F_2\). Put \(\tau=768000/1718717\). The cyclotomic product bounds \(2^{-32}A^\tau<w<2^{35}A^\tau\) and \(2^{-32}A^{\tau/11}<R<2^{33}A^{\tau/11}\), together with the bounds for \(L,F_2\), give the following for \(a\ge30000\).

| Allocation | Exact size obstruction |
|---|---|
| All of \(F_2\) goes short | \(v\ge wF_2>21\sqrt A/2\) |
| The short side takes nothing from \(R\) | \(v\le Lw(F_2/R)<4\sqrt A\) |
| The short side takes nothing from \(F_2/R\), with \(\ell\le4A^{1/200}\) | \(v\le \ell wR<4\sqrt A\) |

The replay checks the exponent margins with rational arithmetic. For an individual short-side power \(p^m\), once the rest of the penultimate share \(f_0\) is fixed, the exact necessary interval in the target subwindow is
\[
\frac{V(1100A)}{\ell w f_0}\le p^m<
\frac{V(1000A)}{\ell w f_0},
\qquad p\equiv1\pmod{726j}
\]
if the power comes from the factor indexed by \(j\).


For the size constants, use the previous \(L<72A^{13/363}\), \(\tfrac12 A^{20/363}<F_2<2A^{20/363}\), and \(A>2^a\). For odd \(m\) with the six prime divisors under discussion, the Möbius product of \(x^j+y^j\) bounds \(\Phi_{2m}(x,y)\) between \(2^{-32}\max(x,y)^{\phi(m)}\) and \(2^{32}\max(x,y)^{\phi(m)}\). In the pinned strip \(\max(x,y)^n=25B\in[22.5A,27.5A]\), giving the stated constants. The exclusion of a single allocated penultimate prime power is conditional on the displayed upper bound on \(\ell\), as well as on the actual prescribed highest share \(w\).

The short replay checks the size cutoffs and a real prime's exact order and exponent on the specified cofinal congruence progression \( (h,k)=(12416651,10186)\bmod21112080 \). No separate exact-quotient/local-square claim is made here. The ordinary window remains open outside the excluded branches.

```python
from fractions import Fraction as F
from math import prod,isqrt
ps=(3,7,11,13,17,101)
tau=prod((F(p-1,p) for p in ps),start=F(1))
assert tau==F(768000,1718717)
g=3*7*13*17*101
n=1331*g
M,h,k=21112080,12416651,10186
assert (n*h+1)%720==22 and (n*k-2)%720==4 and n*M%720==0
ma=(tau+F(20,363)-F(1,2),F(1,2)-tau+tau/11-F(33,363),
    F(1,2)-tau-tau/11-F(1,200))
assert all(30000*z>e for z,e in zip(ma,(37,75,70)))
p=727
assert all(p%i for i in range(2,isqrt(p)+1))
m=p*p
assert pow(3,M,m)==pow(5,M,m)==1
x,y=pow(3,h,m),pow(5,k,m)
z=x*pow(y,-1,p)%p
assert pow(z,726,p)==1 and all(pow(z,726//i,p)!=1 for i in (2,3,11))
Dhi=(pow(x,121*g,m)+pow(y,121*g,m))%m
# The actual D2 compares degrees 11*g and 121*g.
Dlo=(pow(x,11*g,m)+pow(y,11*g,m))%m
assert Dlo%p and Dhi%p==0 and Dhi
print("OK")
```
