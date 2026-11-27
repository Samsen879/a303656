# Capped endpoint profiles at a fixed logarithmic matching threshold

**Capping the representation weights gives a profinite limit for the endpoint energy.** This yields a bound for every fixed logarithmic matching threshold \(\delta>0\):
\[
\mu(F=0)\ \le\ \liminf_X\Pr_X(\nu_X<\delta\log X)
\ \le\ \limsup_X\Pr_X(\nu_X<\delta\log X)
\ \le\ \mu(F^2\le\delta G).
\]
Here \(\Pr_X\) samples \(X<n\le2X\), \(F\) is the verified single-witness profile, and \(G\) is an explicit profile built from the two one-axis averages. The upper bound has a finite-modulus approximation with a controlled error. The exact sublogarithmic exception density remains the lower endpoint \(\mu(F=0)\). [Verified exception-density baseline](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e)

### Removing the diagonal contribution

Use the same rectangle \(X^{1/8}\le3^c\le X^{1/4}\), \(X^{1/3}\le5^d\le X^{1/2}\). Write \(L_3,L_5\) for its side lengths, so
\[
a_3=\lim L_3/\log X=1/(8\log3),\qquad
a_5=\lim L_5/\log X=1/(6\log5).
\]
Every cell is active for large \(X\). Replace its weight by \(w=\min(r_2(n-3^c-5^d),(\log X)^{9/10})\). The positive-weight graph stays the same.

The cap loses \(o(1)\) in the normalized first moment, uniformly in the shift. Indeed,
\[
\sum_{m\le Y} r_2(m)^{3/2}\ll Y(\log Y)^{\sqrt2-1}.
\]
To see the exponent, put \(g=(r_2/4)^{3/2}\). The identity for \(\log m\) as a sum over exact prime powers and multiplicativity give
\[
\sum_{m\le Y}g(m)\log m
\le \sum_{u\le Y}g(u)\sum_{p^k\le Y/u}g(p^k)k\log p
\ll Y\sum_{u\le Y}\frac{g(u)}u.
\]
The inner sum is \(O(Y/u)\) by Chebyshev and polynomial prime-power growth. The Euler product for the last sum is \(O((\log Y)^{\sqrt2})\), since \(g(p)=2^{3/2}\) on split primes and zero on inert primes. Splitting at \(\sqrt Y\) proves the bound. The lost weight above the cap consequently has mean \(O((\log X)^{\sqrt2-29/20})=o(1)\). In a squared row mean, the capped diagonal contributes \(O((\log X)^{9/10}/L_5)=o(1)\), and likewise for columns.

### The endpoint profile

Let \(P_b f(n)=\int f(n-b^u)\,du\), with the eventual power distribution for \(b=3,5\). At a finite modulus \(Q\), set
\[
F_{b,Q}=\pi P_b\rho_Q,\qquad F_Q=P_3F_{5,Q}=P_5F_{3,Q},
\]
where \(\rho_Q(t)=Q^{-1}\#\{(x,y)\bmod Q:x^2+y^2=t\}\). The one-axis \(L^2\) limits \(F_b\) exist. The resulting endpoint profile is
\[
G=a_3^{-1}P_3(F_5^2)+a_5^{-1}P_5(F_3^2).
\]
The squares are taken before averaging over the other axis. [Local norm densities and correlation kernels](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md)

Here is the uniform approximation behind this limit. For a one-axis pair the difference has the form \(h=b^u(b^k-1)\). Chamizo’s formula applies uniformly at the actual shifts \(0<|h|\ll\sqrt X\). In its kernel, cutting away primes \(q>z\) changes the off-diagonal average by \(O(z^{-1/3})\): expand the divisor product by its largest selected prime and use
\[
\sum_{q>z}\frac{\log(2q)}{q\,\operatorname{ord}_q(b)}\ll z^{-1/3}.
\]
In a dyadic block \([U,2U)\), the primes of order at most \(U^{1/3}\) divide \(\prod_{j\le U^{1/3}}(b^j-1)\). There are \(O(U^{2/3}/\log U)\) of them, and the larger orders give the same \(O(U^{-1/3})\) block bound. The order count has no interval endpoint loss: among nonzero exponent differences, the proportion divisible by an order \(l\) is \(O(1/l)\). [Chamizo’s uniform two-shift formula](https://link.springer.com/article/10.1007/s00009-021-01959-3)

Take \(Q=Q(z)=\prod_{p\le z}p^{e_p}\), with \(p^{e_p}\ge z^3\) minimal. The local density projection has squared \(L^2\) error \(O(p^{-e_p})\). Away from the terminal zero classes the density is already determined, and on them the verified formulas give this bound by geometric summation. The correlation error has the same bound by orthogonality of the projection and translation invariance. Summing these finite-depth errors and the prime tail gives
\[
\|F_b-F_{b,Q}\|_2^2\ll z^{-1/3}.
\]
Indeed, for each fixed \(Q\), averaging the finite kernel over the actual exponent interval gives \(\|F_{b,Q}\|_2^2\) in the limit by periodicity. The uniform kernel tail bounds the martingale norms and their difference from the full off-diagonal limit.

The lattice-point first moment in each fixed class modulo \(Q\) gives the mixed moment of a capped row mean with \(F_{5,Q}(n-3^c)\), uniformly in \(c\). It tends to \(\|F_{5,Q}\|_2^2\). The capped row second moment has vanishing diagonal, and its off-diagonal limsup is at most \(\|F_5\|_2^2\) by the uncapped correlation bound. Subtracting the mixed moments gives a mean-square approximation error \(O(z^{-1/3})\) in the limsup. The column calculation is identical. Squaring the row and column means now costs \(O(z^{-1/6})\) in \(L^1\), by Cauchy–Schwarz. This proves joint convergence of the capped grand mean and weighted endpoint profile to \((F,G)\).

### A fixed logarithmic threshold

Write \(A_X\) for the capped grand mean, \(R_c,C_d\) for the capped row and column means, and
\[
G_X=\frac{\log X}{L_3}\frac1{L_3}\sum_c R_c^2+
     \frac{\log X}{L_5}\frac1{L_5}\sum_d C_d^2.
\]
A minimum row–column vertex cover has size \(\nu_X\) by Kőnig’s theorem. Applying Cauchy–Schwarz to the weights on that cover gives \(A_X^2\le(\nu_X/\log X)G_X\). Joint convergence and the closed event \(x^2\le\delta y\) give the stated upper bound. Finite eventual obstructions give the lower bound.

More explicitly, put \(G_Q=a_3^{-1}P_3(F_{5,Q}^2)+a_5^{-1}P_5(F_{3,Q}^2)\). For any \(u,v>0\), the upper tail is bounded by
\[
\frac{\#\{r\bmod Q:(F_Q(r)-u)_+^2\le\delta(G_Q(r)+v)\}}{Q}
+O\!\left(\frac{z^{-1/3}}{u^2}+\frac{z^{-1/6}}v\right).
\]
This is a residue-based tail bound rather than a Markov bound on the total energy. Since \(G\) is finite almost surely and \(G=0\) exactly where \(F=0\), for every \(\epsilon>0\) a fixed \(\delta>0\) gives an upper exceptional proportion at most \(\mu(F=0)+\epsilon\). I did not evaluate a numerical coefficient or prove an exact exception density at fixed \(\delta\). The result gives positive lower proportion and a controlled exceptional tail, while pointwise coverage remains open.

### Exact control

Modulo \(3\), \(P_5((F_{3,3}/\pi)^2)-(F_3^{\rm full}/\pi)^2\) takes values \(0,1/4,1/4\), where \(F_3^{\rm full}\) is the full two-axis center at modulus \(3\). Thus squaring the two-axis center loses an actual endpoint contribution. At \(X=10^6,\ n=1000002\), the ordinary-height rectangle has a true two-edge matching.

```python
from fractions import Fraction as F

rho = [F(sum((x*x+y*y-t)%3 == 0
             for x in range(3) for y in range(3)),3)
       for t in range(3)]
def P5(u):
    return [(u[(n-1)%3]+u[(n-2)%3])/2 for n in range(3)]

full = P5(rho)                # eventual 3^c is zero modulo 3
assert full == [F(4,3),F(5,6),F(5,6)]
assert [g-f*f for g,f in zip(P5([r*r for r in rho]),full)] == [
    0,F(1,4),F(1,4)
]

X,n = 10**6,1000002
assert X < n <= 2*X
for c,d,x,y in [(2,4,58,998),(3,3,43,999)]:
    a,b = 3**c,5**d
    assert X <= a**8 and a**4 <= X and X <= b**3 and b*b <= X
    assert 4*max(a,b) <= n and n-a-b == x*x+y*y
```

The lower and upper exceptional proportions need not coincide at one fixed positive \(\delta\). On the positive-\(F\) set, the finite nonnegative profile \(G\) makes the bound \(\mu\{F^2\le\delta G\}\) decrease to \(\mu(F=0)\) as \(\delta\) tends to zero. This is a controlled fixed-logarithmic threshold, not a numerical value of \(\delta\) or a pointwise result.
