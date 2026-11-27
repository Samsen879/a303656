# Three independently checked arithmetic checkpoints

The checks here concern different interfaces. None of them establishes the pointwise theorem for \(a^2+b^2+3^c+5^d\).

## 1. Order and odd-inert parity for the seed (5,3)

For prime \(q>5\) let \(H_j^\pm=(5^{q^j}\pm3^{q^j})/(5^{q^{j-1}}\pm3^{q^{j-1}})\). The homogeneous cyclotomic factor is a unit modulo \(2,3,5,q\) (modulo \(q\), use the binomial congruence for the homogeneous quotient). For \(p\) dividing \(H_j^\pm\), a lower-order occurrence at level \(j-1\) would cancel from the quotient by LTE since \(p\ne q\). The order of \(5/3\bmod p\) is therefore \(q^j\) or \(2q^j\) for the minus or plus factor, respectively. Its shell valuation equals \(v_p(5^{p-1}-3^{p-1})\) by LTE since the complementary multiplier in \(p-1\) is coprime to \(p\). The shell is \(1\bmod3\); hence the number of distinct \(p\equiv2\bmod3\) occurring to odd valuation is even. The two signs and different levels have disjoint prime support by exact order. In particular an actual first-layer failure requires at least two inert odd-valuation factors in one signed shell.

The native primes 19 and 79 give the same shell residues \((49,19)\bmod60\). Both first-layer shells at 19 are \(x^2+3y^2\); at 79, the actual inert prime \(317=4\cdot79+1\) occurs exactly once in the plus shell. The congruence classes alone cannot force survival. This does not claim a new infinite admissible tower.

## 2. A certified three-factor control for the cubic band

Let \(Q=4\cdot10^9\). Suppose \(Q^3\le R<Q^4\) and all its prime factors exceed \(Q\) and are \(1\bmod686\). If a composite \(R\) has three factors counted with multiplicity, it has a factor in \(Q<a\le\lfloor R^{1/3}\rfloor,\ a\equiv1\bmod686\). Thus a unit gcd with the product of this progression forces a composite \(R\) to have two factors. A nonunit gcd does not by itself distinguish a semiprime from a triple; in the exact control below the factor \(d\) is in the progression and its complement splits by a square difference. This is a standalone exact control. No full cohort totals or aggregate replay are asserted here.

## 3. Exact quotient–remainder cells in the marked prime loss

Continue the fixed sharp window and marked incidence from [the two-sided digit-character calculation](https://github.com/Samsen879/a303656/commit/b1bd260a15c34a2b969a384d329a29b286cafb92). Here \(p=\lambda v=49gts-\kappa\), \(P\mid g\), \(P,t\) distinct primes, \(P>B^{57/250}\), \(t>B^{87/250}\), \(v>\lambda>B^{411/832}\) and \(p=O(B)\). Put \(N=\operatorname{round}(v/\lambda)\), \(d=v-N\lambda\), so \(1\le N\ll B^{5/416}\) and \(|d|\le\lambda/2\). Fixing \(g,t,N,d\), the congruence is
\[
 N\lambda^2+d\lambda+\kappa\equiv0\pmod{Pt}.
\]
For sufficiently large \(B\), \(N<P,t\); each modulus has at most two roots. At most one representative of each CRT residue lies in the \(\lambda=O(\sqrt B)\) band. Two represented roots cannot be reflected partners under \(x\mapsto-dN^{-1}-x\): \(N(\lambda_1+\lambda_2)+d>0\) and is \(O(B^{1/2+5/416})<Pt\). The same positive bound excludes a represented fixed point. Thus at most two represented roots are admissible in each cell, including when a discriminant vanishes modulo a prime. Reconstruct both \(v\) and \(s\) before applying the literal prime and window filters. Each split marked semiprime has at most two choices of designated factor.

With the row and \(t\) counting bounds \(O(B^{95699/384000})\) and \(O(B^{699/2000})\), the signed loss on \(N(1+|d|)\le B^{154093/384000-\epsilon}\) is \(O(B^{1-\epsilon}\log B)\) by a harmonic sum. The uniform sector \(|d|\le B^{3/8}\) is \(O(B^{1-71209/4992000})\). These are bounds by absolute counting for bounded twists, not equidistribution, and do not control the signed large-remainder complement. No finite full-band overlap, prime test on a marked-anchor example, or aggregate signed comparison is claimed here.

```python
from math import gcd, isqrt

def shell(q, s):
    return (5**q + s*3**q)//(5+s*3)

assert shell(19,-1) == 3038279**2 + 3*318864**2
assert shell(19,1) == 89884**2 + 3*889991**2
assert [(shell(q,-1)%60,shell(q,1)%60) for q in (19,79)] == [(49,19)]*2
assert 317%3 == 2 and all(317%x for x in range(2,isqrt(317)+1))
assert pow(5*pow(3,-1,317),79,317) == 316
assert shell(79,1)%317 == 0 and shell(79,1)%317**2 != 0
assert (pow(5,316,317**2)-pow(3,316,317**2))%(317**2) == 35504

R,d = 896149001679064126982634400756132643,259682487401
Q = 4*10**9
X,Y = 5254326915855,20531034691
p,q = (X-Y)//4,(X+Y)//2
assert Q**3 <= R < Q**4 and gcd(R,(d-686)*d*(d+686))==d
assert d*p*q==R and X*X-Y*Y==8*(R//d)
assert d**3<R<p**3<q**3
for x in (d,p,q):
    assert x>Q and x%686==1 and x%2 and all(x%j for j in range(3,isqrt(x)+1,2))

from fractions import Fraction as F
s = 1-F(95699,384000)-F(699,2000)
assert s==F(154093,384000)
assert s-F(5,416)-F(3,8)==F(71209,4992000)
```
