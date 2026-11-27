# Positive density of above-height signed targets in every even class

**Above-height signed witnesses have positive lower density in every even residue class modulo 12.** For every integer \(X\ge10^8\) and every even \(a\bmod12\), at least \(X/(4\cdot10^9)\) integers \(n\in[X,2X)\), \(n\equiv a\bmod12\), have a witness
\[
n=3^c+5^d-(x^2+y^2),\qquad
3X<3^c+5^d<76X,\qquad
4\mid x^2+y^2,\qquad 3\nmid n-5^d.
\]
One value of \(d\) serves the entire residue class in each interval. These witnesses rule out every finite tail obstruction at the targets they hit. [Signed-target criterion](https://github.com/Samsen879/a303656/commit/ddf0d3b817d4e34f49dc31f67a99e5e9446b6e19)

### Counting actual signed witnesses

Fix \(a\). Choose the least \(d\) of the parity for which \(5^d\not\equiv a\pmod3\) and \(5^d\ge3X\). Then \(5^d<75X\). Use the \(K\) positive exponents \(c\le T=\lfloor\log_3X\rfloor\) with \(3^c+1\equiv a\pmod4\). For each such \(c\), put
\[
m_c(n)=\frac{3^c+5^d-n}{4},\qquad
W(n)=\sum_c r_2(m_c(n)),
\]
where \(r_2\) counts ordered signed integer pairs. Here \(0<m_c(n)<19X\) and \(m_c(n)\equiv5^d-a\not\equiv0\pmod3\). A hit for \(m_c(n)\) gives the required coordinates by doubling both coordinates of its representation.

As \(n\) runs through the class, \(m_c(n)\) runs through one nonzero residue modulo \(3\) in an interval of length \(X/4\). Each nonzero norm residue uses four of the nine lattice classes modulo \(3\). Counting lattice points in the corresponding annulus gives, for each \(c\),
\[
\sum_{\substack{X\le n<2X\\ n\equiv a\ (12)}} r_2(m_c(n))
\ \ge\ \frac{\pi X}{9}-200\sqrt X\ \ge\ \frac X4.
\]
For the error bound, tile each lattice class by side-three squares and enlarge or shrink both annulus radii by \(3\). Both radii are at most \(\sqrt{19X}\).

For the second moment, write a difference of two norms as
\[
x^2+y^2-u^2-v^2=(x-u)(x+u)+(y-v)(y+v)=h.
\]
With all coordinates bounded by \(R=\lceil\sqrt{20X}\rceil\), let \(g=\gcd(x-u,y-v)\) for a nonzero difference vector. Then \(g\mid h\). At primitive sup norm \(s\), there are at most \(8s\) difference directions, and the affine line for \((x+u,y+v)\) has at most \(1+4R/s\) lattice points in the box. Summing over \(s\le2R/g\) gives at most \(96R^2/g\). The diagonal uses the same bound summed over \(g\le 2R\), plus \((2R+1)^2\) for the zero difference vector.

The off-diagonal shifts are \(h=(3^c-3^{c'})/4\). Their divisor factors are summable on average. With \(\sigma_{-1}(h)=\sum_{g\mid |h|}g^{-1}\),
\[
\sigma_{-1}(h)\le\tfrac32\sigma_{-1}(3^{|c-c'|}-1),
\qquad
\sum_{j\le T}\sigma_{-1}(3^j-1)\le 9376T.
\]
For the second inequality, expand \(\sigma_{-1}(m)\le\zeta(2)\sum_{g\mid m}\mu^2(g)/g\) and count multiples of \(\operatorname{ord}_g(3)\). The resulting order series is at most \(4688\). Indeed, all squarefree \(g\) of order at most \(U\) divide \(\prod_{j\le U}(3^j-1)\). The product of \(1+1/p\) over its prime factors is at most \(8(1+2\log U)^3\) for \(U\ge2\). For \(p\le U^2\), use the Euler product at \(1+1/\log(U^2)\). The reciprocals of the larger factors sum to less than \(2\), using the logarithm of the displayed product. Dyadic summation gives \(8\sum_{j\ge0}2^{-j}(2j+3)^3=4688\).

Using \(T\le3K\), \(R^2\le30X\), and \(\log(2R)\le7K\), these bounds give
\[
\sum_n W(n)\ge XK/4,\qquad
\sum_n W(n)^2\le250000000\,XK^2.
\]
Cauchy–Schwarz gives the stated count of **distinct targets**. The second-moment bound proves positive lower density and leaves full relative density on the even classes open. The requirement \(4\mid x^2+y^2\) makes every target in this construction even.

### Effect on the obstruction union

Let \(\mathcal B_{\rm tail}\) be the profinite union of finite certificates blocking every \(c\ge A,\ d\ge0\), over moduli and thresholds \(A\). Each finite subunion is periodic and disjoint from the signed hits. Its Haar mass in each even class is therefore at most \(1/12-1/(4\cdot10^9)\). Taking increasing finite subunions gives
\[
\mu(\mathcal B_{\rm all})\le \mu(\mathcal B_{\rm tail})
\le 1-\frac6{4\cdot10^9}.
\]
The repository’s density identity transfers the bound on \(\mu(\mathcal B_{\rm all})\) to the density of the original exceptional set. That inference uses the density identity. The above-height witnesses themselves have **negative** residuals in the original representation problem. [All-exponent density identity](https://github.com/Samsen879/a303656/commit/f108fd396480eaa4524b7aeea6d4dda794a7561c)

A small control is \(110=3^4+5^4-14^2-20^2\), with \(3^4+5^4=706\) and \(110-625\not\equiv0\pmod3\). The independent replay below checks actual witnesses in all six even classes and the explicit constant.

```python

from math import isqrt
from fractions import Fraction as Q

# Confirm the exact dyadic polynomial sum: sums of j^k/2^j for k=0..3.
assert 8*(8*26+36*6+54*2+27*2)==4688
# Ordered pair count plus the harmonic diagonal bound.
assert 96*30*3*3*9376 + (96*8+9)*30 < 250_000_000
assert Q(3,9)-Q(200,10_000)>=Q(1,4)
assert Q(1,4)**2/250_000_000==Q(1,4_000_000_000)

def witness(a,X=100):
    b=0
    while 5**b < 3*X or (5**b-a)%3==0:b+=1
    for c in range(1,6):
        if 3**c>X or (3**c+1-a)%4:continue
        s=3**c+5**b
        for n in range(X+(a-X)%12,2*X,12):
            t=(s-n)//4
            for x in range(isqrt(t)+1):
                y=isqrt(t-x*x)
                if x*x+y*y==t:return n,c,b,2*x,2*y
    raise AssertionError(a)

for a in range(0,12,2):
    n,c,d,x,y=witness(a)
    assert n%12==a and 100<=n<200
    assert n==3**c+5**d-x*x-y*y and 3*100<3**c+5**d<76*100
    assert (n-5**d)%3 and (x*x+y*y)%4==0
assert 110==3**4+5**4-14**2-20**2 and (110-625)%3
print("all six explicit classes and constants passed")
```

The signed count does not improve the separate verified numerical box-density ledger. Its independent content is a genuine above-height supply of certificates of non-obstruction, requiring neither an integer representation below the target nor an assumption on the unknown common exceptional primes.
