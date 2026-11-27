# Growing distinct-exponent matchings in every natural progression modulo 480

**The prime hypothesis can be removed in every residue class modulo \(480\).** There are absolute constants \(\eta,\gamma>0\) such that, for every class \(a\bmod480\) and all sufficiently large \(X\), at least \(\eta X\) integers \(X/2<n\le X\) in that class have at least \(\gamma\sqrt{\log X}\) true two-square remainders \(n-3^c-5^d\). The witnesses lie in the \(n/4\) box and have pairwise distinct \(c\)-labels and pairwise distinct \(d\)-labels.

In particular, this holds on a positive relative proportion of the composite progression \(n\equiv50\pmod{480}\). That progression is disjoint from \(n=5p+52\) by reduction modulo \(5\).

### Uniform first moment

For each \(a\bmod480\), choose \(c_0\in\{1,2\}\), \(0\le d_0<8\), and \(0\le e\le3\) so that
\[
a-3^{c_0}-5^{d_0}\equiv 2^e\pmod{2^{e+2}},
\qquad 3\nmid a-3^{c_0}-5^{d_0}.
\]
First choose the parity of \(d_0\) to avoid \(3\). For odd \(a\), take \(e=0\) and choose the parity of \(c_0\) modulo \(4\) through \(3^{c_0}\bmod4\). For even \(a\), the three residues \(a-2,a-4,a\bmod8\) meet both \(\{2,4\}\) and \(\{0,6\}\), the available offset residues for even and odd \(d_0\), respectively. This chooses \(e\in\{1,2,3\}\) and the parity of \(c_0\). Varying \(d_0\) by \(2\) runs through every lift of its power’s residue modulo \(8\) to modulo \(32\). Both congruences persist when either exponent increases by \(8\).

For \(1\le H\le(\log X)/100\), use the rectangle
\[
c=c_0+16H+8i,\qquad d=d_0+8j,\qquad 0\le i,j<H.
\]
All \(K=H^2\) cells are active throughout \(X/2<n\le X\) for large \(X\). The \(3^c\) gaps exceed the full \(5^d\) span, so the offsets are distinct. In each cell,
\[
m=\frac{n-3^c-5^d}{2^e}>0,\qquad m\equiv1\pmod4,\qquad 3\nmid m.
\]

As \(n\) runs through the progression, \(m\) runs through an interval in one class modulo \(480/2^e\), with \(N=X/960+O(1)\) terms. For squarefree \(r\) supported on inert primes \(q\ge7\), the divisibility count is \(N/r+O(1)\), uniformly in the cell. Apply the half-dimensional lower sieve at \(z=X^{3/5}\), level \(D=X^{4/5}\). Its dimension is \(1/2\), the parameter \(4/3\) is above the sifting limit \(1\), and the total remainder error is \(O(D)\). This gives \(\gg X/\sqrt{\log X}\) survivors per cell. [Half-dimensional lower sieve, Theorem 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

Each survivor is a true norm: \(m\le X\) permits at most one inert factor \(\ge z\), counted with multiplicity, while \(m\equiv1\bmod4\) requires an even number. Thus \(m\) has only split prime factors, and \(2^em\) is a sum of two squares. The first moment is \(\gg XK/\sqrt{\log X}\), with a constant independent of the cell, \(a\), and \(H\). This replaces the prime-indexed large-factor subtraction with a sieve cutoff above \(\sqrt X\). [Prime-indexed baseline](https://github.com/Samsen879/a303656/commit/790206b361b0a1387ab451769061e7406df6ca61)

### Joint bound and target count

For distinct offsets \(F,G\), let \(\Delta=F-G\). At an inert prime \(q\ge7\), reject valuation exactly one at either remainder. On the target progression the coordinate modulo \(q^2\) is unrestricted. The rejected union has size \(2(q-1)\), \(q\), or \(q-1\), according as \(v_q(\Delta)=0,1,\) or at least \(2\). The same uniform Selberg square as in the prime-indexed overlap proof applies to these classes, with the primality test removed. Support \(X^{1/20}\) gives CRT error \(O(X^{1/2})\). The resulting upper bounds for a single true norm and a pair of true norms are respectively
\[
\ll \frac{X}{\sqrt{\log X}},\qquad
\ll \frac{X}{\log X}
\prod_{\substack{q\mid\Delta\\q\equiv3\ (4),\ q\ge7}}(1-1/q)^{-1}.
\]
[Verified Selberg overlap argument](https://github.com/Samsen879/a303656/commit/8074e7521723ac324f1226656a6fd4e3fc3a59f9)

The product has bounded mean over ordered distinct cell pairs. Since \(\log(2|\Delta|)\ll H\), primes above \(H+2\) contribute a bounded factor. Expanding the rest by the largest contributing prime bounds the product by
\[
\ll 1+\sum_{\substack{q\le H+2,\ q\mid\Delta\\q\equiv3\ (4)}}
\frac{\sqrt{\log(2q)}}q .
\]
Fixing three indices, \(q\mid\Delta\) allows at most one class for the fourth modulo \(\operatorname{ord}_q(5^8)\) when that index is on the \(5\)-axis. The proportion is at most \(1/\operatorname{ord}_q(5^8)+1/H\). The order is \(\gg\log q\), making the first contribution summable over primes. The endpoint term is \(O(\sqrt{\log(2H)}/H)\).

Consequently, the hit count \(M(n)\) satisfies
\[
\sum_n M(n)^2\ll \frac{XK}{\sqrt{\log X}}+\frac{XK^2}{\log X}.
\]
Together with the first moment, Cauchy–Schwarz gives \(\gg X\) targets with \(M(n)\gg K/\sqrt{\log X}\) whenever \(K\gtrsim\sqrt{\log X}\). Greedy deletion of the chosen row and column costs at most \(2H-1\) hits per witness. Taking \(H=\lfloor(\log X)/100\rfloor\) proves the distinct-axis claim. This is a positive lower relative density result. Density one remains open.

### Exact composite controls

In the phase \(n\equiv50\bmod480\), both \((2,0)\) and \((10,8)\) use \(e=3\). At \(n=1562930\) their remainders are \(102^2+1246^2\) and \(210^2+1034^2\). At \(n=1563890\) both pass the \(\{3,7,11\}\) panel, but the second has \(v_{43}=1\). A third control has \(v_7=2\) and is a true norm outside the stricter lower-sieve count.

```python
from math import isqrt

def F(c, d):
    return 3**c + 5**d

def phase(a):
    for e in ((0,) if a % 2 else (1, 2, 3)):
        for c in (1, 2):
            for d in range(8):
                r = a - F(c, d)
                if r % 3 and r % (4 << e) == 1 << e:
                    return c, d, e
    raise AssertionError(a)

for a in range(480):
    c, d, e = phase(a)
    for i in range(2):
        for j in range(2):
            r = a - F(c+8*i, d+8*j)
            assert r % 3 and r % (4 << e) == 1 << e
assert phase(50) == (2, 0, 3)

def m(n, c, d):
    assert n % 480 == 50 and 4*max(3**c, 5**d) <= n
    r = n - F(c, d)
    assert r > 0 and r % 32 == 8 and r % 3
    return r // 8

def prime(q):
    return q > 1 and all(q % d for d in range(2, isqrt(q)+1))

u, v = m(1562930,2,0), m(1562930,10,8)
assert u == 5*41*953 and v == 37*3761
assert all(prime(q) and q % 4 == 1 for q in (5,41,953,37,3761))
assert 8*u == 102**2+1246**2 and 8*v == 210**2+1034**2

u, v = m(1563890,2,0), m(1563890,10,8)
assert all(u % q and v % q for q in (3,7,11))
assert v == 41*43*79 and prime(43) and v % 43**2
assert m(25490,2,0) == 7**2*65
assert 8*m(25490,2,0) == 98**2+126**2
print("480 phases and all exact composite controls passed")
```

All bounds above count actual integer targets; each residue class contributes a positive lower proportion even on each large dyadic interval. In the pair calculation a factor of \(2^e\) cannot change any inert valuation. The omitted primes 2, 3 and 5 are already settled by the head or are split. A positive first moment together with a comparable upper second moment yields a positive fraction, not a variance small enough for density one. The primary sieve formula has fixed dimension \(1/2\) and fixed parameter \(4/3\); for this unweighted progression the \(O(1)\) remainders are summed up to \(D\), without a prime-distribution hypothesis.
