# A deterministic modular-power Gaussian gcd selector on a positive proportion

This responds to [the bounded squarecore obstruction](https://github.com/Samsen879/a303656/commit/43f38fd6edca7cadbfaeca745ffc66f7c22e5bea) by retaining the entire large nonsquare norm, rather than stripping it to a small cofactor. The deterministic verifier never needs to recognize primality. Prime residuals in a fixed progression are used only to prove a positive-proportion lower bound for its successes, including a matching of actual growing labels on each of those targets. This does not establish arbitrary-target coverage or improve the separate existing global lower-density estimate.

In the degree bound, the progression is ignored for the upper-bound sieve, which only enlarges the pair count. Differences in one fixed row or column are of the form \(a^e(a^j-1)/9\), so the singular-series factor costs at most a fixed extra factor from \(a\). Summing the reciprocal-order expansion over gaps gives bounded average; there are \(O(H)\) label pairs at each fixed gap in a row or column. The Gaussian gcd works over composite inputs whenever its modular square test succeeds, but the paired control demonstrates a true composite norm missed by that test. Both matched fixture winners, the failing norm and the exact omitted valuation were independently replayed.

**A modular-power test followed by a Gaussian gcd certifies a positive proportion of actual inputs.** For every sufficiently large dyadic scale \(X=2^H\), there are \(\gg X\) targets in \([X/2,X)\) with \(\gg H\) certified labels forming a matching between the two exponent axes. Each label retains a nonsquare norm factor of size \(\Theta(X)\). The selector takes the integer \(n\) as input and uses neither factorization nor a primality test.

### Deterministic selector

For \(H\) the bit length of \(n\), use
\[
\mathcal C_H=\{c:H/32\le c\le H/4,\ c\ge3,\ c\equiv3\bmod8\},\qquad
\mathcal D_H=\{d:H/32\le d\le H/4,\ d\ge1,\ d\equiv1\bmod72\}.
\]
The head is \(n\equiv1\bmod32,\ n\equiv14\bmod27,\ n\equiv0\bmod5\). For each label, put \(R=n-3^c-5^d\). Require \(R>0\) and units at the inert primes \(7\le p\le Y=\lfloor H/16\rfloor\). The head gives \(R\equiv1\bmod32\), \(v_3(R)=2\), and
\[
U=R/9\equiv217\bmod480 .
\]
Compute \(r=5^{(U-1)/4}\bmod U\). If \(r^2\equiv-1\bmod U\), calculate \(z=\gcd_{\mathbb Z[i]}(U,r+i)\) and return the coordinates of \(3z\).

The ideal \((U,r+i)\) is the kernel of the surjection \(\mathbb Z[i]\to\mathbb Z/U\mathbb Z\) sending \(i\) to \(-r\). Its index is \(U\), so \(N(z)=U\), even for composite \(U\). If \(U\equiv217\bmod480\) is prime, quadratic reciprocity gives \((5/U)=(U/5)=-1\), so the test always succeeds. Testing the whole menu has polynomial cost in \(H\). A failed square check leaves the norm status undecided.

### Why both axes contribute on a positive proportion of targets

Count an edge \((c,d)\) at \(n\) when \(U=(n-3^c-5^d)/9\) is prime in \([X/16,X/12]\), \(U\equiv217\bmod480\). Every such edge lies in the head and passes the full growing panel. All these targets lie in \([X/2,X)\) for large \(H\) because the shifts are \(o(X)\). Each of the \(\Theta(H^2)\) labels contributes \(\asymp X/H\) prime edges by the fixed-modulus prime number theorem. The total is \(\asymp XH\). [Fixed-modulus prime number theorem](https://doi.org/10.1112/S0010437X12000802)

Write \(r_c(n)\) and \(s_d(n)\) for the row and column degrees. Then
\[
\sum_{n,c}r_c(n)^2+\sum_{n,d}s_d(n)^2\ll XH.
\]
For a fixed row, the diagonal contributes \(O(X)\). The off-diagonal uses the uniform two-prime upper sieve with shift \(k=(5^{d'}-5^d)/9\), which bounds each count by \(O(XH^{-2}W(k)+1)\), where \(W(k)=\prod_{p\mid k,\ p>2}(1+1/(p-2))\). The column argument uses \(k=(3^{c'}-3^c)/9\). [Ding–Verwee, Lemma 3.2, v1](https://arxiv.org/html/2602.14368v1)

For either base \(a=3,5\), the average \(\sum_{j\le H}W(a^j-1)\ll H\) follows by expanding into squarefree divisors with weight \(w(d)=\prod_{p\mid d}1/(p-2)\). The sum \(\sum_d w(d)/\operatorname{ord}_d(a)\) converges. In fact, the divisors of order at most \(T\) use primes in \(\prod_{j\le T}(a^j-1)\). Its log is \(O(T^2)\). The weight product over primes up to \(T^4\) is polylogarithmic in \(T\) by the reciprocal-prime estimate, and the primes above \(T^4\) contribute a bounded factor. Dyadic summation proves convergence. This gives \(O(X)\) per row or column and the stated degree bound.

Delete edges incident to degrees above a sufficiently large fixed \(D_0\). The degree bound charges \(O(XH/D_0)\) deletions, leaving \(\gg XH\) edges. Each target now has at most \(D_0H\) edges, so \(\gg X\) targets have \(\gg H\) retained edges. A greedy matching keeps at least a \(1/(2D_0-1)\) fraction of those edges. Thus the same targets have \(\gg H\) distinct successful exponents on **each** axis.

The earlier gate can still fail at **every** positive label on these targets. With \(B=q_1q_2=O(H^2)\), the count for \(R=h t^2u\), \(u<B\), and \(h\) supported on primes through \(Y\), is at most
\[
O\!\left(H^2\sqrt{XB}\prod_{p\le Y}(1-p^{-1/2})^{-1}\right)
=X^{1/2+o(1)}
\]
across the entire positive exponent window. Removing these inputs leaves \(\gg X\) targets in the new theorem.

### Matched exact controls

The two inputs in the replay agree mod \(32\) and every panel \(p^3\). All four labels pass the panel. On both inputs the seed \((3,1)\) has exact valuation one at the omitted inert prime \(43\). The first input certifies \((11,73)\). The second has a genuine norm at \((11,73)\) that the base-\(5\) test misses, and certifies \((3,73)\) instead.

```python
from itertools import product
from math import prod

P = (7, 11, 19, 23, 31)
labels = tuple(product((3, 11), (1, 73)))

def gaussian_norm_coords(u, r):
    a, b, c, d = u, 0, r, 1
    while c or d:
        den = c*c + d*d
        x = (2*(a*c+b*d) + den)//(2*den)
        y = (2*(b*c-a*d) + den)//(2*den)
        a, b, c, d = c, d, a-x*c+y*d, b-x*d-y*c
    assert a*a + b*b == u
    return a, b

def remainder(n, c, d):
    return n - 3**c - 5**d

def certificate(n, c, d):
    R = remainder(n, c, d)
    if R <= 0 or R % 32 != 1 or R % 27 != 9 or any(R % p == 0 for p in P):
        return None
    u = R//9
    if u % 480 != 217:
        return None
    r = pow(5, (u-1)//4, u)
    if r*r % u != u-1:
        return None
    a, b = gaussian_norm_coords(u, r)
    assert (3*a)**2 + (3*b)**2 == R
    return abs(3*a), abs(3*b)

s = 3**11 + 5**73
u = 100000000000000000000000000015696506848848192712926297
v = 100000000000000000000000000004464548120212587070761837
good, other = s+9*u, s+9*61*v
assert (good-other) % (32*27*prod(p**3 for p in P)*43**2) == 0

for n, winner in ((good, (11, 73)), (other, (3, 73))):
    assert n % 5 == 0 and remainder(n, 3, 1) % 43**2 == 43
    for c, d in labels:
        R = remainder(n, c, d)
        assert R > 0 and R % 32 == 1 and R % 27 == 9
        assert all(R % p for p in P)
    assert [e for e in labels if certificate(n, *e)] == [winner]
    print(winner, certificate(n, *winner))

a, b = 249893234645421975900095581, 193786922361773612741164326
assert a*a + b*b == v
A, B = 3*(5*a-6*b), 3*(6*a+5*b)
assert remainder(other, 11, 73) == A*A+B*B
assert pow(5, (61*v-1)//2, 61) == 58  # -1 would be 60
assert certificate(other, 11, 73) is None
```

The density theorem concerns certificates within one fixed head and a valuation mask applied per label. It does not establish that an arbitrary input has a certifiable label, or that a preassigned old label survives the growing panel.
