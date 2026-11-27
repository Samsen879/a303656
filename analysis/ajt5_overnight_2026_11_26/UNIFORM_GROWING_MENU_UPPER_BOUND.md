# Uniform upper bounds for growing second-witness menus

**A growing menu of \(o(\sqrt{\log X/\log\log X})\) arbitrary cells succeeds on a vanishing fraction of the primes \(p\le X\), \(p\equiv1\pmod{12}\).** For consecutive rows, columns, or rectangular menus, the threshold improves to \(o(\sqrt{\log X})\) cells. Both bounds are uniform in the location of the menu inside the ordinary exponent height.

Here success means a positive two-square remainder at an active cell with \(c\ne3\) and \(d\ne2\) for \(n=5p+52\). The original cell \((3,2)\) already gives the norm \(5p\). Thus each success supplies a second witness with both labels changed. [Verified dual-exponent baseline](https://github.com/Samsen879/a303656/commit/b2f2f62254b46b7d702f870f8b9feaee79a53200)

### Uniform bound for arbitrary menus

Let \(\mathcal H_X\) be the distinct shifts \(h=52-3^c-5^d\) in a menu chosen at scale \(X\). Retain cells with both labels changed that are active for at least one \(p\le X\), where active means \(4\max(3^c,5^d)\le 5p+52\). Then \(0<|h|\le3X\) for sufficiently large \(X\). Write
\[
W(h)=\prod_{\substack{q\mid h\\q\equiv3\ (4)}}(1-1/q)^{-1}.
\]
If \(N(X)\) counts distinct successful targets, then
\[
N(X)\ll \frac{X}{(\log X)^{3/2}}\sum_{h\in\mathcal H_X}W(h),
\tag{1}
\]
with an absolute constant. A menu can vary with \(X\). For target-dependent choices, the bound applies to the union of their possible cells.

**Uniform sieve calculation.** For a fixed \(h\), sieve integers \(m\le X\) modulo \(q^2\). Reject \(q\mid m\), and for \(q\equiv3\bmod4\) also reject \(v_q(5m+h)=1\). When \(q\) is inert and \(q\nmid h\), the two tests reject \(q\) and \(q-1\) disjoint classes modulo \(q^2\). When \(q\mid h\), the valuation-one classes are already rejected by \(q\mid m\). The surviving local density is therefore \((1-1/q)^2\) in the first case and \(1-1/q\) otherwise. Every prime \(p>z\) with a positive norm remainder survives these tests at \(q\le z\).

To see the error is uniform, write \(g(q)\) for the rejected density, set \(T=X^{1/20}\) and \(z=T^\eta\) for a small absolute \(\eta>0\), and put \(b(q)=g(q)/(1-g(q))\), extended multiplicatively on squarefree integers. Define \(G=\sum_{r\le T,\,r\mid\prod_{q\le z}q}b(r)\). In the full Euler product for this sum, the normalized mean of \(\log r\) is \(\sum_{q\le z}g(q)\log q\ll\log z\). Choosing \(\eta\) small gives \(G\ge\frac12\prod_{q\le z}(1-g(q))^{-1}\) by Markov’s inequality.

For the Selberg square, use weights \(\lambda_d\) defined by
\[
\sum_{d:\,r\mid d}\lambda_d g(d)=\frac{\mu(r)b(r)}G
\]
on the same squarefree support. Möbius inversion gives \(\lambda_1=1\) and \(|\lambda_d|\le b(d)/g(d)\le d^2\). The identity \(g([d,e])=g(d)g(e)/g((d,e))\) diagonalizes the main quadratic form to \(1/G\). For each pair \(d,e\le T\), CRT counts the simultaneous rejected classes modulo \([d,e]^2\) with error at most \([d,e]^2\). The total weighted error is at most \(T^{10}=X^{1/2}\). Mertens’ products for all primes and [for \(3\bmod4\) in Williams, Theorem 1](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf) now give the single-cell bound in (1), absorbing the primes \(p\le z\) and the error.

Splitting \(W(h)\) at \(Y=\log(3X)\) gives \(W(h)\ll\sqrt{\log\log X}\). The primes through \(Y\) contribute the Mertens product, and the logarithm of the remaining factor is \(O(\log|h|/(Y\log Y))\). Dividing (1) by \(\pi(X;12,1)\sim X/(4\log X)\) proves the arbitrary-menu threshold.

### Consecutive exponent intervals

On a fixed \(c\)-row, let \(d\) range over any interval of \(L\) consecutive integers. The actual order of \(5\) gives the stronger estimate
\[
\sum_{\text{retained }d} W(52-3^c-5^d)\ll L+\sqrt{\log\log X}.
\tag{2}
\]
To prove it, discard the bounded product from primes \(q>Y\), then expand the remaining product by its largest selected prime. The product of all preceding factors is \(O(\sqrt{\log(2q)})\), so
\[
W(h)\ll 1+\sum_{\substack{q\le Y,\ q\mid h\\q\equiv3\ (4)}}\frac{\sqrt{\log(2q)}}q.
\]
For a given \(q\), the equation \(5^d=52-3^c\bmod q\) has either zero solutions or one class modulo \(\operatorname{ord}_q(5)\). It contributes at most \(L/\operatorname{ord}_q(5)+1\) occurrences, including at a translated interval. Since \(\operatorname{ord}_q(5)\ge\log(q+1)/\log5\), the coefficient of \(L\) is bounded by the convergent prime sum \(\sum_q1/(q\sqrt{\log q})\). The \(+1\) terms sum to \(O(\sqrt{\log Y})\). This proves (2).

The same proof applies to columns with base \(3\), absorbing the factor at \(q=3\) into the constant. Slicing a rectangle of side lengths \(L_3,L_5\) along its longer side gives a total weight
\[
\ll L_3L_5+\min(L_3,L_5)\sqrt{\log\log X}.
\]
Equation (1) then gives the \(o(\sqrt{\log X})\) area threshold. The full active box and menus above these scales remain outside the bound.

### Paired controls and replay

For the same menu \(\{(7,0),(7,1)\}\), \(p=2053\) succeeds at \((7,1)\), while \(p=3109\) fails at both cells with exact inert valuations \(v_{11}=1\) and \(v_7=1\). The original witness is active at both targets.

```python
from math import isqrt

def R(p, c, d):
    n = 5*p + 52
    assert p % 12 == 1 and all(p % q for q in range(2, isqrt(p)+1))
    assert 4*max(3**c, 5**d) <= n
    return n - 3**c - 5**d

def once(r, q):
    return r % q == 0 and r % (q*q) != 0

assert R(2053,3,2) == 67**2 + 76**2
assert R(2053,7,1) == 69**2 + 58**2
assert once(R(2053,7,0), 11)
assert R(3109,3,2) == 13**2 + 124**2
assert R(3109,7,0) == 13409 and once(13409, 11)
assert R(3109,7,1) == 13405 and once(13405, 7)

for d in (0, 1):
    h = 52 - 3**7 - 5**d
    for q in (2, 3, 5, 7, 11, 107):
        killed = sum(m % q == 0 or (q % 4 == 3 and once(5*m+h, q))
                     for m in range(q*q))
        assert killed == q + (q-1)*(q % 4 == 3 and h % q != 0)
print("Both menu controls and all local counts passed")
```

For clarity, in the quadratic-form diagonalization one uses \(1/g(m)=\sum_{r\mid m}1/b(r)\) on squarefree \(m\); substituting the displayed Selberg choice gives \(\sum_{r\le T}b(r)/G^2=1/G\), with the same supported primes as \(G\). The CRT discrepancy bound may use the entire modulus \([d,e]^2\) regardless of the shift, which is why it is uniform. For a rectangle of area \(A\), the additive term is at most \(\sqrt{A\log\log X}\); this is \(o(\sqrt{\log X})\) if \(A=o(\sqrt{\log X})\).
