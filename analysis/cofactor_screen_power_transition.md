# Stripped-cofactor recognition at power-sized inert-prime screens

The stripped-cofactor selector has a sharp transition among fixed screen exponents. With \(B(n)=\lfloor n^\beta\rfloor\), it certifies only a density-zero set of targets for every fixed \(0<\beta<1/2\). At \(\beta=1/2\), it recognizes every positive residual that is a sum of two squares, and the project’s existing positive-density theorem applies. The transition concerns recognition of individual residuals. Existence of a successful label for every \(n\) remains open. [Repository theorem index, P-001](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

### Construction with both exponents growing

For each actual positive residual \(m=n-3^c-5^d\), screen primes \(p\equiv3\pmod4\) through \(B\). Reject any odd screened valuation. Strip the full powers of \(2\) and the screened primes, leaving \(u\). With \(q_1<q_2\) the first two inert primes above \(B\), accept when \(u\equiv1\pmod4\) and \(u<q_1q_2\). If an unscreened odd valuation remained, the congruence would require at least two distinct unscreened odd valuations, forcing \(u\ge q_1q_2\). This is the project’s parity and size argument applied to the stripped cofactor. [Repository theorem assets, AUX-01](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

Fix \(0<\beta<1/2\), and set \(\gamma=2\beta/(1-2\beta)\). For each large \(k\), use
\[
A=3^{2k},\qquad c=2k,\qquad k\le d\le\lfloor\log_5 A\rfloor,
\]
and choose any prime \(\ell\equiv1\pmod4\) in \([A^\gamma/4,A^\gamma/2)\). Define
\[
n=5^d+A(1+\ell).
\]
The label \((c,d)\) leaves \(m=A\ell\), and the screen strips exactly \(3^{2k}\) for all sufficiently large \(k\). Thus \(u=\ell\). Since \(\ell^{1-2\beta}<A^{2\beta}\), we have
\[
u=\ell<(A\ell)^{2\beta}<n^{2\beta}<q_1q_2.
\]
The final inequality uses the integer screen boundary, which gives \(q_i>n^\beta\).

Both \(c\) and the minimum allowed \(d\) tend to infinity. The raw residual satisfies \(m/n\to1\) uniformly, since \(5^d\le A\). The choices of \(d\) give distinct residues \(5^d\bmod A\), and the choices of \(\ell\) give distinct targets for each \(d\). The fixed-progression prime number theorem supplies \(\asymp_\beta A^\gamma/\log A\) primes in the prescribed interval, while there are \(\asymp\log A\) choices of \(d\). Hence each block gives \(\asymp_\beta A^\gamma\) distinct certified targets on scale \(X=A^{1+\gamma}\), equivalently \(\asymp_\beta X^{2\beta}\). [Davenport, *Multiplicative Number Theory*, Chapters 20–22](https://link.springer.com/book/9780387950976)

### Sparsity and the borderline

For \(n\in[X,2X]\), the prime number theorem in \(3\bmod4\) gives \(q_1q_2\ll X^{2\beta}\). Every accepted residual has the form \(m=2^\epsilon s^2u\), with \(\epsilon\in\{0,1\}\), \(m\le2X\), and \(u\le Y=CX^{2\beta}\). Even allowing every positive \(u\le Y\), the number of possible residual values is
\[
O\!\left(\sqrt X\sum_{u\le Y}u^{-1/2}\right)=O(\sqrt{XY}).
\]
Each residual and actual label determine one target. There are \(O((\log X)^2)\) labels below \(2X\), so the number of accepted target-label pairs, and therefore of certified targets, is \(O(X^{1/2+\beta}(\log X)^2)=o(X)\). The count includes all positive residuals and uses no assumptions about independence or how the stripping varies with the label. [Davenport, *Multiplicative Number Theory*, Chapters 20–22](https://link.springer.com/book/9780387950976)

**Logarithmic refinement.** An accepted \(u\) is itself a sum of two squares. The Landau bound and partial summation give \(\sum_{u\le Y,\,u\text{ a norm}}u^{-1/2}\ll\sqrt{Y/\log Y}\). This improves the fixed-\(\beta\) upper bound to \(O_\beta(X^{1/2+\beta}(\log X)^{3/2})\). It also gives density zero for the nearer-borderline budget \(B(n)=\lfloor\sqrt n/(\log n)^a\rfloor\) when \(a>3/2\). The refinement below settles sparsity at the endpoint \(a=3/2\); distinct-target behavior for \(0<a<3/2\) is not settled here. [Repository theorem assets, K2-N1](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

At \(\beta=1/2\), both \(q_i>\sqrt n\), so \(q_1q_2>n>m\). Every norm therefore passes the height test as well as the local tests. Conversely, every accepted residual is a norm by the parity argument. The project’s P-001 gives positive dyadic coverage at this screen. Its growing count of admissible pairs also ensures positive residuals there, since a zero residual allows at most one \(d\) per \(c\), hence only \(O(\log X)\) zero pairs. [Repository theorem index, P-001](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

### Same-target controls and independent replay

Use \(n=402631\) and \(\beta=1/4\). Then \(B=25\) and \(q_1q_2=31\cdot43=1333\). Each row clears the screened valuations and leaves \(u\equiv1\pmod4\).

| Label \((c,d)\) | Residual \(m\) | Cofactor \(u\) | Outcome |
|---|---:|---:|---|
| \((4,8)\) | \(11925\) | \(1325\) | Accepted, \(m=30^2+105^2\) |
| \((2,8)\) | \(11997\) | \(1333\) | Equality rejection, \(m=9\cdot31\cdot43\) |
| \((2,1)\) | \(402617\) | \(402617\) | Height rejection despite \(m=236^2+589^2\) |

The first two labels both strip \(9\). The change \(3^4-3^2=72\) lowers the cofactor by \(8\). The third label separates failure of the certificate from failure of the two-square condition. The standard-library replay checks square representability directly by integer square roots, independently of the valuation screen.

```python
from math import isqrt

def prime(p):
    return p > 1 and all(p % j for j in range(2, isqrt(p) + 1))

def norm(m):
    return any(a*a + isqrt(m - a*a)**2 == m
               for a in range(isqrt(m // 2) + 1))

def screened(n, c, d, b):
    m = n - 3**c - 5**d
    assert m > 0
    u = m // (m & -m)
    for p in range(3, b + 1, 4):
        if prime(p):
            e = 0
            while u % p == 0:
                u //= p
                e += 1
            assert e % 2 == 0
    return m, u

n = 402631
b = isqrt(isqrt(n))
q = [p for p in range(3, 100, 4) if p > b and prime(p)][:2]
assert b == 25 and q == [31, 43]
rows = [screened(n, c, d, b) for c, d in [(4, 8), (2, 8), (2, 1)]]
assert rows == [(11925, 1325), (11997, 1333), (402617, 402617)]
assert [norm(m) for m, u in rows] == [True, False, True]
assert [u % 4 == 1 and u < q[0]*q[1] for m, u in rows] == [
    True, False, False
]
```
## Refinement at logarithmic screens

**The endpoint \(a=3/2\) is sparse.** For the screen \(B(n)=\lfloor\sqrt n/(\log n)^a\rfloor\), the number of accepted target-label pairs with \(X\le n\le2X\) is
\[
\Theta_a\!\left(
\frac{X(\log X)^{3/2-a}}{\sqrt{\log\log X}}
\right)
\qquad (0<a\le3/2).
\]
The upper bound also bounds the number of distinct targets, giving \(O(X/\sqrt{\log\log X})\) at the endpoint. For the whole displayed range, the matching lower bound holds even with distinct actual labels and targets restricted to \(n\equiv3\pmod4\). It counts incidences, so a positive fraction of distinct targets in that class remains unproved.

### Where the extra saving comes from

For an actual positive residual \(m=n-3^c-5^d\), reject odd valuations at screened primes \(p\equiv3\pmod4\). Strip the full powers of \(2\) and of those primes. The selector accepts the cofactor \(u\) when \(u\equiv1\pmod4\) and \(u<q_1q_2\), where \(q_1,q_2\) are the first two inert primes above the screen. Any remaining obstruction would require two distinct inert primes with odd valuations, whose product is at least \(q_1q_2\). [Repository theorem assets, AUX-01](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

Put \(L=(\log X)^a\). The fixed-progression prime number theorem bounds \(q_1q_2\ll_a X/L^2\) uniformly on the dyadic interval. Every accepted residual has the form
\[
m=2^\epsilon s^2u,\qquad \epsilon\in\{0,1\},
\]
where every prime divisor of \(s\) is \(3\bmod4\) and \(u\) is a two-square norm. The restriction on \(s\) is essential. Wirsing’s theorem applied to the indicator of integers supported on the primes \(3\bmod4\) gives a count asymptotic to \(C_-t/\sqrt{\log t}\), with \(C_->0\). The same conclusion holds for support on primes \(1\bmod4\). Both applications use prime density \(1/2\) and bounded prime-power values. [Wirsing’s original theorem](https://doi.org/10.1007/BF01351892) · [Davenport, *Multiplicative Number Theory*, Chapters 20–22](https://link.springer.com/book/9780387950976)

For \(s\le L\), multiply the count of eligible \(s\) by the Landau upper bound for norms \(u\ll X/L^2\). For \(L<s\le X^{1/4}\), apply the norm bound at \(2X/s^2\) and use partial summation to bound the sum of \(s^{-2}\) over inert-supported \(s>L\) by \(O(1/(L\sqrt{\log L}))\). For \(s>X^{1/4}\), summing the unrestricted bound \(2X/s^2\) costs \(O(X^{3/4})\). Altogether the number of candidate residual values is
\[
O_a\!\left(\frac{X}{L\sqrt{\log X\,\log L}}\right).
\]
There are \(O((\log X)^2)\) actual labels below \(2X\), giving the incidence upper bound. In particular, the improvement comes from the prime support of the stripped square factor. No cancellation between labels is needed. [Repository theorem assets, K2-N1](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

### Matching incidences in one residue class

Take inert-supported \(s\in[2L,3L]\), and take \(u\) supported on primes \(1\bmod4\) in
\[
[X/s^2,\;3X/(2s^2)].
\]
These \(u\) are odd primitive two-square norms. In the Gaussian factorization, choosing just one conjugate above each split prime gives a representation with coprime coordinates. The two disjoint prime supports make \(m=s^2u\) determine \(s\) and \(u\) uniquely. The screen eventually contains every prime dividing \(s\), and
\[
m\in[X,3X/2],\qquad u\le3X/(8L^2)<q_1q_2
\]
uniformly for targets in \([X,2X]\) when \(X\) is large. The two Wirsing counts give \(\asymp_a X/(L\sqrt{\log X\,\log L})\) such residuals. [Wirsing’s original theorem](https://doi.org/10.1007/BF01351892)

Use even \(c\) and all \(d\) with \(3^c,5^d\le X/8\), requiring \(c\ge\lceil2\log_3\log X\rceil\). There are \(\asymp(\log X)^2\) labels, all \(2\bmod4\), and they are distinct. In a collision with \(c<c'\), one would have \(v_3(5^{|d-d'|}-1)=c\). If \(|d-d'|\) is odd the valuation is zero, and otherwise it is \(1+v_3(|d-d'|)\le\log_3\log X+O(1)\), below the chosen \(c\). Adding each label to each constructed residual gives the matching incidence lower bound in \(n\equiv3\pmod4\). A single label already gives \(\gg_a X/(L\sqrt{\log X\,\log L})\) distinct targets in that class. Any stronger coverage claim from this construction needs control of how often different labels certify the same target.

### Cost of excluding small residuals

The project’s actual-label interval bound I2-D1 shows that discarding all \(0\le m\le H\), for \(1\le H\le X/2\), can lose at most
\[
O\!\left((H+1)\bigl(1+\log(X/H)\bigr)\right)
\]
targets in \([X,2X]\). The bound includes zero residuals and counts a target even if it has another certificate. At \(H=X/(\log X)^{2a}\) the loss is \(O_a(X\log\log X/(\log X)^{2a})=o(X)\), globally and relative to any fixed residue class. The matching incidence construction above uses only \(m\ge X\). [Repository theorem assets, I2-D1](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

### Exact endpoint control

At \(a=3/2\) and \(n=1965131\), the unrounded screen lies between \(25.41\) and \(25.42\), so \(B=25\) and \(q_1q_2=31\cdot43=1333\). Both labels clear the screened valuations and strip exactly \(9\).

| Label \((c,d)\) | Residual \(m\) | Cofactor \(u\) | Outcome |
|---|---:|---:|---|
| \((4,9)\) | \(11925=30^2+105^2\) | \(1325=5^2\cdot53\) | Accepted |
| \((2,9)\) | \(11997=9\cdot31\cdot43\) | \(1333\) | Rejected at equality |

~~~python
from decimal import Decimal, localcontext
n=1965131
with localcontext() as ctx:
    ctx.prec=60
    x=Decimal(n)
    unrounded=x.sqrt()/x.ln()**Decimal("1.5")
    assert Decimal("25.41")<unrounded<Decimal("25.42")
ex=[screened(n,c,9,25) for c in (4,2)]
assert ex==[(11925,1325),(11997,1333)]
assert [norm(m) for m,u in ex]==[True,False]
~~~
