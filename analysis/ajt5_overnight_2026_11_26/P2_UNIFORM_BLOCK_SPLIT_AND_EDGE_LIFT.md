# Uniform whole-block exclusion and an independent-edge lift

**The ordinary window excludes every whole-cyclotomic-factor allocation, even when the common-exponent refinement grows.** More generally, both sides must receive a growing product of factors from split blocks. The independent \(02\) edge then gives an exact test modulo \(H^2\) that selects at most one earlier share per true edge divisor. The unrestricted split branch remains open. [Pinned six-character result](https://github.com/Samsen879/a303656/commit/41bdd8c096b7d71325bb357af5de431f2a14559f)

### What must split at ordinary height

Keep \(g=468741\), \(n=1331g\), \(a=nh+1,\ b=nk-2\), \(A=3^a,\ B=5^b\), and \(W=\sqrt A\). The four shifts are
\[
A+25B,\quad 9A+625B,\quad 81A+125B,\quad729A+B.
\]
For any common divisor \(q\mid h,k\), put \(n'=nq,\ X=3^{h/q},\ Y=5^{k/q}\), and \(Z=\sqrt{XY}\). Then
\[
E=6\prod_{j\mid n'/121}\Phi_{2j}(X,Y).
\]
After this substitution, \(H=w_*R\) and its complementary top product are products of other whole factors of \(X^{n'}+Y^{n'}\).

The uniform bound comes from normalizing by the geometric mean. Each cyclotomic factor divided by \(Z^{\varphi(2j)}\) is at least \(1\). For a conjugate root pair the normalized term is \(2\cosh(\log(Y/X))-2\cos\theta\), which increases from its value at \(X=Y\). The product of **all** the normalized factors is
\[
\sqrt{75B/A}+\sqrt{A/(75B)}<10
\]
on \(39/40\le B/A\le122/125\). Thus this bound is independent of the number of refined factors.

In any allocation of the actual divisor \(\ell\mid E\) across the displayed factors, separate the complete blocks from the portions of split blocks. The complete part on either side, including its prescribed top factors and its share of \(6\), has integer degree \(j\). Since \(n'\) is odd and \(Z^{n'/2}/W\in(1,2)\), a complete part of degree \(j\ge(n'+1)/2\) already exceeds \(W\sqrt Z\). A complete part of degree \(j\le(n'-1)/2\) is below \(120W/\sqrt Z\).

Here \(Y-X\ge1\) and \(0<\log(Y/X)<5/n'\) give \(Z>n'/10\). Consequently the high-degree case exceeds the ordinary upper bound \(33W\). In the low-degree case, reaching \(4W\) requires **a product greater than \(\sqrt Z/30\) from split blocks on each side**. This excludes whole-block allocations and, cofinally, any uniformly bounded split contribution.

### The independent-edge test

Take a true short divisor \(z\mid e=20A+25B\), and put \(L=z+e/z\). This is twice the first half-root. Require \(K=S_0+L^2\) to be ordinary. Write \(J=d/H\). The first edge must satisfy
\[
H\ell^2-L\ell+J=0.
\]
For the independent-edge shortcut, require that \(H\) contains full prime powers of \(d\), or check directly that \(\gcd(H,J)=1\). Under this explicit condition, \(\gcd(L,H)>1\) rejects the allocation. Otherwise the equation forces the unique lift
\[
r\equiv JL^{-1}\pmod H,\qquad
\ell\equiv L^{-1}(J+Hr^2)\pmod{H^2}.
\]
Since the ordinary factors are below \(33W\), \(L<66W\) and \(d<167A\), the absolute value of the quadratic is below \(4000A/H\). On the pinned share, \(H\asymp A^\mu\) with \(\mu=2344000/5156151+(768000/1718717)/11>1/3\). Thus \(H^3>4000A\) and \(\ell<H\) for sufficiently large balanced members. Congruence modulo \(H^2\) then forces exact equality and yields at most one candidate for actual divisibility by \(E\). Passing that check gives the first three integer roots. The fourth still requires \(L^2-4f\) to be an integer square.

This is where the six characters leave work. The split portions of the earlier factors must be true divisors of their integer values, and the independent edge needs a true short divisor of \(e\). In the refined bases \(e=60X^{n'}+Y^{n'}\) is Eisenstein at \(3\) after dehomogenizing, so further polynomial subdivision does not supply that divisor. The prior finite control verifies local roots at its own height.

```python
from fractions import Fraction as F
from math import gcd

n = 1331 * 468741
lo, hi = F(39,40), F(122,125)
mu = F(2344000,5156151) + F(768000,1718717)/11
assert n % 2 == 1 and n > 10 * 132**2
assert 4 < 25*lo/3 < 25*hi/3 < 9
assert 1 < 75*lo < 75*hi < 81
assert 1000*(3*mu-1) > 10 and 2**10 > 700
assert 33**2+66*33+167 < 4000

def lift(H, J, L):
    if gcd(H,L) != 1:
        return None
    r = J * pow(L,-1,H) % H
    return (J + H*r*r) * pow(L,-1,H*H) % (H*H)

# Synthetic exact edge test with two true divisors of e.
H,d,e = 7,364,111
z = 3
L = z + e//z
ell = lift(H,d//H,L)
assert ell == 2 and H*ell + d//(H*ell) == L
assert lift(H,d//H,1+e) is None
print("uniform size bounds and independent-edge lift checked")
```

For the uniform refinement, \(n'\) is odd because the pinned \(h\) is odd and its divisor \(q\) is odd. If \(t=\log(Y/X)\), then \(Y-X=2Z\sinh(t/2)<10Z/n'\); the nonzero integer difference gives the stated lower bound for \(Z\). Every complete block has an integer size degree, and the product of any subset of its normalized factors is at most the normalized product of all factors. This makes the exclusion uniform even when the refinement varies with \(h,k\). The edge-lift replay is a synthetic exact control, not a solution of the pinned equation.