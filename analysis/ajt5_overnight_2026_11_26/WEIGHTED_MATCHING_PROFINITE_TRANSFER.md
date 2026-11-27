# Weighted matching and the profinite zero-atom bound

**The profinite zero-atom upper bound transfers to every matching size \(J(X)=o(\log X)\).** Let \(F\) be the verified profinite limit for the weighted single-witness count, and let \(\nu_X(n)\) be the largest number of true witnesses with pairwise distinct \(c\)-labels and pairwise distinct \(d\)-labels in its ordinary-height rectangle. Then
\[
\limsup_{X\to\infty}\frac1X
\#\{X<n\le2X:\nu_X(n)<J(X)\}
\le \Pr_{\rm Haar}(F=0).
\]
Unconditionally, in **every** residue class modulo \(480\), a positive relative proportion have \(\nu_X(n)\gg\log X\). This improves the verified \(\sqrt{\log X}\) matching size on a positive proportion. [Single-witness profinite limit](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md) · [Previous matching theorem](https://github.com/Samsen879/a303656/commit/35e2e16123e1c8cdf65be33a7046aeba1d9bfb96)

### Transfer through weighted rows and columns

Use the original intervals \(X^{1/8}\le3^c\le X^{1/4}\) and \(X^{1/3}\le5^d\le X^{1/2}\). Their \(T\asymp(\log X)^2\) offsets are distinct and active for \(X<n\le2X\) once \(X\) is large. Give cell \((c,d)\) weight \(w_{cd}(n)=r_2(n-3^c-5^d)\), where \(r_2\) counts signs and order. Set
\[
A_X=T^{-1}\sum_{c,d}w_{cd},\qquad
E_X=\sum_c\Big(\sum_d w_{cd}\Big)^2+
     \sum_d\Big(\sum_c w_{cd}\Big)^2 .
\]
The endpoints of a maximum matching cover every positive-weight cell. Cauchy–Schwarz on those endpoints gives the deterministic inequality
\[
(TA_X)^2\le 2\nu_X E_X.
\]

The needed same-axis estimate is \(\mathbb E_X E_X\ll(\log X)^3\), where the mean is over the dyadic target interval. The diagonal follows from \(\sum_{m\le Y}r_2(m)^2\ll Y\log(2Y)\). Off the diagonal, Chamizo’s uniform two-shift formula bounds the mean product by \(O(\sigma_{-1}(|h|))\) for \(0<|h|\ll\sqrt X\). In one row or column, \(|h|=b^u(b^k-1)\) for \(b=3\) or \(5\). The \(b^u\) factor costs a bounded multiplier. [Chamizo, Theorem 1.1 and Corollary 1.5](https://link.springer.com/article/10.1007/s00009-021-01959-3)

For completeness, \(\sum_{k\le L}\sigma_{-1}(b^k-1)\ll L\). Bound the divisor sum by \(\prod_{q\mid b^k-1}(1-1/q)^{-1}\). Primes above \(L\) cost a bounded factor, since \(\log(b^k-1)=O(L)\). Expanding the remaining product by its largest contributing prime bounds its mean by
\[
\ll 1+\sum_{q\nmid b}\frac{\log(2q)}{q\,\operatorname{ord}_q(b)}.
\]
This series converges. In \([U,2U)\), primes of order at most \(U^{1/3}\) divide \(\prod_{j\le U^{1/3}}(b^j-1)\), so there are \(O(U^{2/3}/\log U)\). They contribute \(O(U^{-1/3})\), and the larger orders contribute the same bound. Thus the off-diagonal weight in a row or column of length \(L\) is \(O(L^2)\).

For every \(\tau>0\) and \(J\ge1\), the deterministic inequality and Markov’s inequality now give
\[
\Pr_X(\nu_X<J)
\le \Pr_X(A_X\le\tau)+O\!\left(\frac{J}{\tau^2\log X}\right).
\]
Take \(X\to\infty\) with \(J=o(\log X)\), using the verified convergence in distribution \(A_X\Rightarrow F\), then let \(\tau\downarrow0\). This proves the transfer.

For the unconditional logarithmic result, the finite conditional center satisfies \(\min_a F_{480}(a)=7\pi/15\), as checked below. The conditional first moment in each of the 480 classes therefore stays positive, and the bounded second moment of \(A_X\) gives a fixed positive proportion above a fixed \(\tau>0\). Discarding targets with \(E_X>C(\log X)^3\) for a sufficiently large fixed \(C\) still leaves a positive proportion in each class. The deterministic inequality then gives \(\nu_X\gg\log X\).

### The remaining lower tail and a fixed-modulus obstruction

The shortest missing input for density-zero exceptions in this transfer is **\(\Pr_{\rm Haar}(F=0)=0\)**. A fixed-modulus center still leaves real variance. In fact, the exact local projections give
\[
\|F_{3360}-F_{480}\|_2^2=\frac{2131}{1190700}\pi^2.
\]
The lattice-point first moment gives the same two finite conditional means for translated rectangles whose two side lengths tend to infinity. Thus an average of such rectangles still has a limiting mean-square error from \(F_{480}\) at least this large, by projecting onto modulus \(3360\). Disjoint exponent labels alone give no variance reduction for this shared component.

There is also a pointwise control for phase-locked rectangles. At \(n=1799880016\), every active cell with \(c\ge2\) and \(d\equiv0\pmod6\) has \(v_3(n-3^c-5^d)=1\). The disjoint active cells \((4,6)\) and \((6,12)\) therefore both fail, while \((2,1)\) has the true remainder \(2\cdot29999^2\).

```python
from collections import Counter
from fractions import Fraction

def norm_counts(q):
    squares = Counter(x*x % q for x in range(q))
    out = [0]*q
    for x, nx in squares.items():
        for y, ny in squares.items():
            out[(x+y) % q] += nx*ny
    return out

# Returns F_q / pi, using a full eventual exponent period L.
def profile(q, L, counts):
    shifts = Counter((pow(3,c,q)+pow(5,d,q)) % q
                     for c in range(L,2*L) for d in range(L,2*L))
    return [Fraction(sum(k*counts[(a-h) % q] for h,k in shifts.items()),
                     q*L*L) for a in range(q)]

N, M = norm_counts(480), norm_counts(7)
A = profile(480, 8, N)
B = profile(3360, 24, [N[t%480]*M[t%7] for t in range(3360)])
assert min(A) == Fraction(7,15)
assert all(sum(B[a::480]) == 7*A[a] for a in range(480))
assert sum((b-A[t%480])**2 for t,b in enumerate(B))/3360 == Fraction(2131,1190700)

n = 14 + 2*29999**2
assert n == 1799880016 and n % 9 == 4
for c,d in [(4,6),(6,12),(2,1)]:
    assert 4*max(3**c,5**d) <= n
assert all((n-3**c-5**d) % 9 == 3 for c,d in [(4,6),(6,12)])
assert n-3**2-5 == 2*29999**2
```

In the short \(k\)-average, divisibility along the sequence has proportion at most \(1/\operatorname{ord}_q(b)+1/L\); the latter contributes \(O(\log(2L)/L)\) after summing through \(L\). The matching estimate transfers the *zero-atom bound*, not the separate numerical bound on single-witness exceptions unless the zero atom is itself bounded by that number. The direction of the existing comparison does not justify that inference.
