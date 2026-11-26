# Coprime short-factor ratios and a bound on surviving P2 heights

**Two additional short-factor ratios give an exact intersection.** On an explicit cofinal refinement of the pinned phase, the heights surviving both ratio sieves are precisely the integer P2 solutions in the ordinary window. Their number is \(A^{o(1)}\), so their proportion among integer heights is at most \(A^{-1+o(1)}\). This bound leaves open whether the set is empty. [Pinned adaptive-gap result](https://github.com/Samsen879/a303656/commit/722b8ad0e0a71b0dfd71acf4782efc6b123c69fe)

### Two coprime ratios

Let \(S,P,Q\) be the real half-roots of rows \(0,2,3\), and set \(z=S-P\). Alongside the original short factors \(v,r\), we have the exact relations
\[
v+d/v=z+e/z=2S,\qquad r+D/r=2S-2z.
\]
The new edge product is \(e=z(S+P)\). The identities \(10d-e=25\cdot59B\) and \(25D+31e=10\cdot467A\) bound \(\gcd(d,e)\) and \(\gcd(D,e)\) by \(59\) and \(467\), respectively. Modular arithmetic on the cofinal refinement makes both gcds exactly \(1\).

For real \(U,V>1\), exclude a point when some integers \(p,q\) satisfy
\[
1\le q<V,\qquad |qU-pV|<1.
\]
The survivors are exactly the coprime integer pairs \(U,V\). If \(V\) is nonintegral, the \(\lceil V\rceil\) points \(jU/V\bmod1\) have a circular gap at most \(1/\lceil V\rceil<1/V\). If \(V\) is integral, survival forces all \(V\) circular gaps to equal \(1/V\), giving \(U\in\mathbb Z\) and \(\gcd(U,V)=1\).

Apply this test to \((z,v)\) and \((r,z)\). A joint survivor has integral \(v,z,r\) and \(\gcd(v,z)=1\). The common sum \(2S=v+d/v=z+e/z\) has reduced denominator dividing both \(v\) and \(z\), so it is integral. Then \(D/r=2S-2z-r\) is integral too. The four full roots are
\[
2S,\quad 2S-2v,\quad 2S-2z,\quad 2S-2z-2r.
\]
Conversely, a true solution passes both tests by the coprimalities of the edge products.

### Counting the exact centers

The original ratio still has \(v=qt,\ r=pt\), with \(t\in\{1,13\}\), and retains the same-height identity
\[
(v+d/v)^2-(r+D/r)^2=4e.
\]
Each short divisor of \(d\), \(e\), or \(D\) fixes at most one height. Thus the count is bounded by the **smallest** of the three true short-divisor lists restricted to the ordinary interval. Given the lists, their exact height intersection is a sorted merge. The standard divisor bound gives \(A^{o(1)}\) uniformly.

For fixed \(H=w_*R\), the true complementary earlier share \(E/\ell\) sharpens the bound. Write \(\alpha=1/121\), \(\lambda=395821/113435322\), and \(h(x)=-x\log x-(1-x)\log(1-x)\). Since \(E\ll A^\alpha\) and \(E/\ell\ll A^\lambda\),
\[
\#\{\text{surviving heights for }H\}
\le
\exp\!\left[
\bigl(\alpha h(\lambda/\alpha)+o(1)\bigr)
\frac{\log A}{\log\log A}
\right],
\qquad \alpha h(\lambda/\alpha)\approx0.00562808.
\]
Indeed, primes up to \(\log A/(\log\log A)^3\) contribute only \(\exp(o(\log A/\log\log A))\) exponent choices. The remaining prime factors of \(E\), counted with multiplicity, provide at most \((\alpha+o(1))\log A/\log\log A\) slots. The smaller complementary share uses at most \((\lambda+o(1))\log A/\log\log A\) of them. The binomial entropy bound gives the displayed coefficient.


For the cofinal refinement, keep \(h,k\) congruent to \(12416651,10186\) modulo \(T=\operatorname{lcm}(21112080,58,466)\), and also impose the prior divisibility by \(19\cdot23\) when using \(w_*\). The new period is coprime to \(19\cdot23\); thus these are compatible progressions and the usual irrational-rotation argument retains the balanced strip. The displayed two gcds are exactly one: the potential odd factors 59 and 467 from the two identities are both excluded by the residue test below, while \(e\) is odd and \(D\) is coprime to \(5A\).

For the small-prime factor count in the entropy bound, the crude \(O(\log A)\) exponent choices per prime below the stated threshold already give a negligible logarithmic count. Treat larger prime factors as indexed slots, which can only overcount distinct divisor values. No actual huge divisor list is asserted complete and no emptiness result follows.

```python
from fractions import Fraction as F
from math import gcd,ceil,log,lcm,isqrt
N=1331*468741
P,h,k=21112080,12416651,10186
T=lcm(P,58,466)
assert gcd(T,19*23)==1
for p,want in ((59,(39,17,36)),(467,(225,366,443))):
    assert all(p%i for i in range(2,isqrt(p)+1))
    assert pow(3,N*T,p)==pow(5,N*T,p)==1
    A,B=pow(3,N*h+1,p),pow(5,N*k-2,p)
    got=((2*A+150*B)%p,(162*A-31*B)%p,(20*A+25*B)%p)
    assert got==want and got[2]!=0
for a in range(5,40):
    for b in range(5,40):
        U,V=F(a,4),F(b,4)
        ok=all(abs(q*U-p*V)>=1 for q in range(1,ceil(V))
               for p in (q*U//V,q*U//V+1))
        assert ok==(U.denominator==V.denominator==1 and gcd(U.numerator,V.numerator)==1)
a=F(1,121)
ell=F(395821,113435322)
assert 0<ell<a/2
s=float(ell/a)
assert 0.00562807<float(a)*(-s*log(s)-(1-s)*log(1-s))<0.00562810
print("OK")
```
