# A balanced fixed-conductor obstruction to a quaternary output bridge

The coset in the claim is \(\mathbb Z^2\times A(1+30\mathbb Z)\times B(1+30\mathbb Z)\), with quadratic form \(X^2+Y^2+3U^2+5V^2\). Here primitive local means some coordinate is a unit over the specified \(\mathbb Z_p\).

For every fixed \(K>0\), there are infinitely many actual pairs \(A=3^u,\ B=5^v\) with \(A<B<2A\) for which \(n>KI\), where \(I=900AB\). The target \(n\) has a primitive point in the specified coset over every \(\mathbb Z_p\), and no integer point in that coset. All nine central branches have positive residuals, eight with nonzero corrections. Every constructed target also has an explicit Sun representation.

A short standalone integer certificate follows the proof.

### Finite obstruction and actual CRT

Choose \(30\mid a\), \(a\ge90\), \(a^2>900K\), and set
\[
n=(aB)^2+T^2+A^2+B^2,\qquad
U=A(1+30z),\quad V=B(1+30w).
\]
When \(T<A<B<2A\), we have \(n/B^2<a^2+3\). Thus every possible integer point is covered by the finite box defined by
\[
3(30|z|-1)^2<4(a^2+3),\qquad
5(30|w|-1)^2<a^2+3.
\]
The nine central branches are active because their last two coordinates contribute at most \(8\cdot31^2B^2<a^2B^2\). Also \(n/I>a^2/900>K\). The intrinsic conductor is \(30\), the order of the shift \((0,0,A,B)\) modulo the coset lattice.

For each box row put
\[
d_{zw}=25a^2+34-27(1+30z)^2-125(1+30w)^2\equiv2\pmod5.
\]
The prime selection works for both signs of \(d=d_{zw}\):

- For \(d>0\), take \(p\equiv-5\bmod4d\). For each odd prime \(\ell\mid d\), reciprocity gives \((\ell/p)=(5/\ell)=(\ell/5)\). If \(d\) is even, \(p\equiv3\bmod8\) gives the same factor for \(2\) as at \(5\). Hence \((d/p)=(d/5)=-1\).
- For \(d<0\), take \(p\equiv-1\bmod4|d|\). Every prime factor of \(|d|\) contributes \(+1\) by reciprocity and the supplementary law for \(2\). The minus sign contributes \((-1/p)=-1\).

Both progressions are reduced, so Dirichlet supplies distinct primes \(p>5\), one per row. Each has \(p\equiv3\bmod4\), so \(-d\) is a nonzero square modulo \(p\). For a root \(r\), choose \(e\bmod p\) by
\[
2re\equiv1-(r^2+d)/p\pmod p.
\]
Then \((r+pe)^2+d\equiv p\bmod p^2\). Combine all these residues with \(T\equiv a\bmod60\) by CRT. Choose an even period \(P\) divisible by every \(p(p-1)\). For \(A=3^{1+Ph}, B=5^{1+Pk}\), each row keeps \(A\equiv3,\ B\equiv5\bmod p^2\), so its actual residual has \(p\)-valuation exactly one. Such a residual cannot be two squares, since divisibility by \(p\equiv3\bmod4\) would force both square coordinates to be divisible by \(p\). [Dirichlet’s theorem, with proof](https://kskedlaya.org/ant/chap-primes-in-ap.html#theorem-4-2)

There are infinitely many balanced exponent pairs. Along convergents \(h/k\) to \(\log5/\log3\),
\[
\big|\log(B/A)-\log(5/3)\big|<P\log3/k.
\]
The right side tends to zero and \(A\to\infty\), giving \(T<A<B<2A\).

### Primitive local points

At \(p=2,3,5\), fix the last coordinates at \(U=A,V=B\) and put \(R=n-3A^2-5B^2\).

| Place | Primitive solution |
|---|---|
| \(2\) | \(R\equiv2\bmod8\), since \(a,T\) are even and congruent modulo \(4\). Take \(X=1\), and use the odd square root \(Y^2=R-1\). |
| \(3\) | \(R\equiv2\bmod3\). Take \(X=1\), and lift \(Y^2=R-1\equiv1\bmod3\). |
| \(5\) | \(R\equiv-2A^2\bmod5\). Take \(X=2A\), and lift \(Y^2=R-4A^2\equiv-A^2\bmod5\). |
| \(p\notin\{2,3,5\}\) | Both coset steps are units. Start with \(U=0,V=1\bmod p\) and solve \(X^2+Y^2=n-5\bmod p\). Two translates of the square set intersect because each has size \((p+1)/2\). Lift along \(V\), whose derivative is \(10V\), a unit. |

The real point follows from the positive central residual. At a branch’s certificate prime, the branch can fail while the whole \(p\)-adic coset still represents \(n\): that prime does not constrain \(U,V\).

### Fully expanded native control

With \(A=3^{10}\), \(B=5^7\), \(a=90\), and \(T=1770\), the target is
\[
49\,448\,069\,995\,426
=7\,031\,250^2+1770^2+3^{20}+5^{14}.
\]
It has \(n>9I\), all nine central branches active, and 11 active branches in total. This short replay checks every active branch and its inert valuation. The two bounds at the start exclude all rows outside the displayed box.

```python
from math import isqrt

A, B, a, T = 3**10, 5**7, 90, 1770
n = (a*B)**2 + T*T + A*A + B*B
assert n == 49448069995426 and T < A < B < 2*A
assert n > 9*900*A*B and T % 60 == a % 60
assert 3*119**2 > 4*(a*a+3) and 5*59**2 > a*a+3

P = {(-2,0):7, (-1,-1):17351, (-1,0):7919, (-1,1):27803,
     (0,-1):19, (0,0):31, (0,1):7, (1,-1):7,
     (1,0):7, (1,1):107, (2,0):31}
active = set()
for z in range(-3,4):
    for w in (-1,0,1):
        R = n - 3*(A*(1+30*z))**2 - 5*(B*(1+30*w))**2
        assert R != 0
        if R > 0:
            active.add((z,w))
            p = P[z,w]
            assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
            assert R%p == 0 and R%(p*p) != 0
assert active == set(P)
assert {(z,w) for z in (-1,0,1) for w in (-1,0,1)} <= active
```

The frozen controls \(41\) and \(449\) also check out. For \(n=36A^2+5B^2\) with \(A\le B\), the residual \(33A^2\) is too small to reach any corrected branch and has \(v_{11}=1\). Its separate Sun representation is \((3A)^2+(2B)^2+3^{2u+3}+5^{2v}\).

The obstruction rules out a uniform threshold of the form \(n>KI\) for this coset bridge, even at fixed conductor and with balanced, active branches. It leaves adaptive label choices open. The genuine Sun representations above make the distinction explicit.
