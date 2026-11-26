# Ordinary-row exponent steps: a row-count bound and a sharp three-step control

Use natural parity seed steps two on each axis (a fixed seed step 18 on the base-5 axis can also be preserved in the general bound). All candidate moves are forward, and positivity is checked independently from residue feasibility. Every panel prime is inert, greater than 3, and at least one base is ordinary there.

## A bound depending only on row count

For \(s\) rows put \(U_0=18,\ U_{j+1}=U_j3^{3sU_j}\). If the forward rectangle of width \(sU_s\) exponent units from a compatible seed is strictly active, two exponents within that rectangle can be chosen to have even valuations at all the panel rows. In particular the number of necessary steps is bounded for a fixed number of rows independently of their prime sizes.

Maintain strides \(M_3,M_5\) preserving all processed rows and the seed, initially bounded by \(U_0\), and process in increasing prime order. With \(r\) rows left, if every remaining row has \(\operatorname{ord}_p(3^{M_3})>r\), the \(r+1\) shifts \(0,M_3,\ldots,rM_3\) along one axis have distinct base-3 powers at each row. Each row forbids at most one point; choose a shift making them all units. Otherwise some remaining prime divides \(3^{jM_3}-1\) for \(1\le j\le r\), so the smallest remaining prime is at most \(3^{sU_j}\) when \(j\) rows have already been processed (with the product-order exponent here any integer up to \(r\)). The strides accumulated from smaller primes and seed are coprime to the current prime. Move on an ordinary base using a multiple of the current stride and current mod-prime order to reach exact valuation two when needed; the step parameter can be chosen below \(p^2\) by LTE. Update both strides using the valuation-preservation periods modulo \(p^3\). Each increase in the exponent and each new stride is bounded by \(U_{j+1}\), since the newly introduced factors are at most \(p^2(p-1)\). Thus there are at most \(j\) individual increments plus at most \(rM_3\) terminal displacement, together bounded by \(sU_s\). This bound is deliberately coarse; it is not a threshold for numerical height.

## The smallest number of rows that can force three steps

In any strictly positive \(3\times3\) rectangle of parity increments, both \(9\) and \(25\) have order at least three mod any inert \(p>3\): the factors of \(9^2-1\) and \(25^2-1\) have no such prime. Accordingly a row can collide with at most three cells, and a three-cell collision is a permutation \(\pi\) of the columns. Eliminating the initial power ratio in that event requires
\[
p\mid10(25^{\pi(1)}-25^{\pi(0)})-(25^{\pi(2)}-25^{\pi(0)}).
\]
The six integers have only the inert prime factors \(7,47,251\) above 3. The unique permutation admitting 251 requires the ratio of initial powers \(3^{c_0}/5^{d_0}\equiv176\bmod251\). But \(176^{125}=-1\) whereas \(3^{125}=5^{125}=1\bmod251\). Thus at most two distinct rows can collide at three cells. Three rows can jointly cover at most eight cells, so **three rows never force more than two steps of size two** in an active rectangle.

Four ordinary rows can force three steps. Use \(Q=\{7,19,31,571\}\), \(c_0=4,d_0=3\) and \(n=3^4+5^9+40618766139049^2+33055105668720^2\). For \(c=4+2i,d=3+2j\), the \(0\le i,j<3\) table of exact once-dividing primes is
\[
(19,7,571),\quad(7,19,31),\quad(31,571,7).
\]
All nine are positive and satisfy the natural seeds. The point \(i=0,j=3\) is independently a true norm by the displayed construction, making the finite-panel step gap exactly three. This concerns a finite panel and starting label, not existence of unrestricted representations.

```python
from itertools import permutations
from math import isqrt
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
pows=[1,25,625]
dets=[(P,10*(pows[P[1]]-pows[P[0]])-(pows[P[2]]-pows[P[0]])) for P in permutations(range(3))]
assert {p for _,D in dets for p in range(7,abs(D)+1,4) if D%p==0 and prime(p)}=={7,47,251}
assert [P for P,D in dets if D%251==0]==[(1,2,0)]
assert (-600*pow(8,-1,251))%251==176
assert pow(176,125,251)==250 and pow(3,125,251)==pow(5,125,251)==1
n=3**4+5**9+40618766139049**2+33055105668720**2
for i,row in enumerate(((19,7,571),(7,19,31),(31,571,7))):
    for j,p in enumerate(row):
        r=n-3**(4+2*i)-5**(3+2*j)
        assert r>0 and r%8==1 and r%3!=0 and r%p==0 and r%(p*p)!=0
for p in (7,19,31,571):
    assert prime(p)
    assert all(pow(b,p-1,p*p)!=1 for b in (3,5))
```
