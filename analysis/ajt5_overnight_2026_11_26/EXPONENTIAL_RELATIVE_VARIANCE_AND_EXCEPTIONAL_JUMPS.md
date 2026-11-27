# Exponential relative variance and the exceptional positive jumps

The unconditional contribution is the exponential relative-family variance bound (1). Equation (4) improves the low-positive-mass rate on the complement of a specified common-Wieferich jump event. That event's probability is not bounded here by a decaying function of the terminal cutoff. The full unconditional low-mass rate is therefore not upgraded in this note.

### A stronger relative-family estimate

Use the verified notation \(A_x\) for the surviving phase family, \(\alpha_x\) for its Haar mass, \(H_x=\alpha_x/D_x\) for the normalized head, and \(\mathcal G_x\) for the complete target reads through \(x\). For \(w\ge y\ge x^{16}\), on \(H_y>0\), I obtain
\[
\operatorname{Var}(H_w/H_y\mid\mathcal G_y)
\ll \frac{\alpha_x}{\alpha_y}
       \exp\!\left(-c_1\frac{\log y}{\log x}\right).
\tag{1}
\]
The previous estimate had \(\log x/\log y\) in place of the exponential. [Verified phase martingale and pair kernels](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

The improvement comes from estimating the smooth part of \(q-1\). In a dyadic block \(U<q\le2U\) above \(y\), put \(s=1/\log x\). If the \(x\)-smooth part of \(q-1\) is at least \(U^{1/6}\), it has a divisor \(m\) between \(U^{1/6}\) and \(xU^{1/6}\), hence below \(\sqrt U\). Define the nonnegative multiplicative weight
\[
g(r^a)=r^{as}-r^{(a-1)s}.
\]
Since \(\sum_{d\mid m}g(d)=m^s\), Brun–Titchmarsh bounds the number of such \(q\) by
\[
\ll \frac U{\log U}\,U^{-s/6}
\sum_{d\ \text{\(x\)-smooth}}\frac{g(d)}{\varphi(d)}
\ll \frac U{\log U}\exp\!\left(-\frac{\log U}{6\log x}\right).
\]
The Euler product in the middle is bounded uniformly: its local increment is
\((r^s-1)/[(r-1)(1-r^{s-1})]\ll s\log r/r\).
Summing the reciprocal charge of these primes over the blocks gives \(O(e^{-c_1\log y/\log x})\). Small orders of 5 and the remaining primes contribute \(O(y^{-1/6}\log y)\) by the existing largest-prime expansion. For the remaining primes the free part of the order exceeds \(U^{1/6}\). The resulting row bound is uniform in the first phase. Restricting the second draw from \(A_x\) to \(A_y\) costs the single factor \(\alpha_x/\alpha_y\) in (1). [Conditional order argument](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e) · [Montgomery–Vaughan](https://doi.org/10.1112/S0025579300004708)

### The faster bound and its exact exceptional event

At an inert read \(q\), write \(R_q=H_q/H_{q^-}\) when the previous head is positive. If \(r_q(a)\) is the previous survivor fraction with shift \(a\bmod q\), then
\[
(1+1/q)(1-r_q(n_q\bmod q))\le R_q\le1+1/q.
\]
When either base lifts ordinarily at \(q\), the exact update is \(R_q=1+1/q-r_q(n_q\bmod q)\ge1/q\). Thus a **positive** jump \(0<R_q<1/q\) requires both bases to be Wieferich at \(q\), and requires \(r_q(n_q\bmod q)>q/(q+1)\). At most one target residue can trigger it.

Let \(E(S,Y)\) be the event of at least one such positive jump for \(S<q\le Y\). It has a more selective bound than the reciprocal sum of common primes. With \(O_q=\max(\operatorname{ord}_q(3),\operatorname{ord}_q(5))\),
\[
\Pr(E(S,Y)\mid\mathcal G_S)
\le
\sum_{\substack{S<q\le Y\\q\ \mathrm{common\ Wieferich\ inert}}}
\frac1q\,
\Pr\!\left(0<\alpha_{q^-}<\frac{q+1}{qO_q}\,\middle|\,\mathcal G_S\right).
\tag{3}
\]
Indeed, fixing the other axis bounds an unrestricted shift fibre by \(1/O_q\), so \(r_q(a)\le1/(\alpha_{q^-}O_q)\).

Put \(L=\log\log z\) and \(Y=\exp(\sqrt L/8)\). For any fixed power-of-two starting cutoff \(S\ge2^{14}\), the resulting bound is
\[
\boxed{\quad
\Pr(0<\alpha_z<1/\log z\mid\mathcal G_S)
\le \Pr(E(S,Y)\mid\mathcal G_S)+O_S(L^{-c}).
\quad}
\tag{4}
\]

To prove it, clip the logarithmic loss at each prime to
\(\ell_q=\min(\log q,\log^+(1/R_q))\), using the cap at a zero and taking \(\ell_q=0\) after absorption. By the convex secant bound up to \(r=q/(q+1)\),
\(\ell_q\le(1+1/q)r_q(n_q\bmod q)\log q\). Thus its conditional mean is \(O(\log q/q)\). Applying the exponential secant on \([0,\log q]\) with parameter \(1/\log y\), then iterating over reads, gives
\[
\Pr\!\left(\sum_{S<q\le y}\ell_q>A\log y\,\middle|\,\mathcal G_S\right)
\ll e^{-A}.
\]
Here \(\sum_{q\le y}\log q/q=O(\log y)\). Use \(A=\sqrt L\) and checkpoints \(x_j=S^{16^j}\le Y\). On a positive terminal branch outside \(E(S,Y)\), the clipped losses are the actual downward log losses. Except on a set of measure \(O((k+1)e^{-\sqrt L})\), all \(k+1\) checkpoint heads are at least \(2^{-6S}Y^{-\sqrt L}\ge e^{-L/4}\) for large \(z\). The target low-mass threshold in \(H_z\) is \(O(e^{-L/2})\). [Verified finite-head floor](https://github.com/Samsen879/a303656/commit/140d8a38fc7afc5b2ec5374760078a7040700a26)

For completeness, the restart estimate on this longer grid works as follows. At each positive anchor draw an independent threshold \(u\in[\eta,2\eta]\) and restart on the first head below \(u\) times the anchor, testing the terminal head too. Uniform conditional \(L^2\) and Paley–Zygmund give a fixed chance \(p_0\) of finishing above half the anchor. At a crossing the conditional chance of that outcome is at most \(2u\), so the crossing probability is at most \(1-p_0/2\) for \(\eta=p_0/8\). After \(m\) checkpoints without crossing, the chance that the current ratio is within \(\delta\) above \(u\) is at most \(\delta/\eta\) by the independent draw. Away from this margin, (1) and the maximal inequality give probability \(O_\eta(\delta^{-2}e^{-c_2 16^m})\) of a later crossing. Balancing the two terms gives an exponential moment of the crossing length \(\ell\) with \(\mathbb E(e^{\lambda\ell}\mathbf1_{\rm crossing}\mid\text{anchor})\le1\) for some \(\lambda>0\). Iterating bounds terminal arrival by \(e^{-\lambda(k+1)}\). A positive terminal head below \(\eta\) times every checkpoint must arrive. Here \(k=\lfloor\log_{16}(\log Y/\log S)\rfloor\), giving (4).

### Exact \(3,5\) replay

At \(n=10000804849\), both cells are in the ordinary-height box for \(X=10^{10}\). The \((3,5)\) cell gives a true norm. The \((5,5)\) cell passes the old support tests but has valuation 1 at 11. The anchored family at 11 exhibits the sharp ordinary normalized loss \(1/11\), exactly at the boundary of the exceptional event in (3). This replay passed.

```python
from fractions import Fraction as F

n, X, d = 10000804849, 10**10, 5
b = 5**d
R, S = (n - 3**c - b for c in (3, 5))
assert X < n <= 2*X and X <= b**3 and b*b <= X
for c, t in ((3, R), (5, S)):
    assert X <= (3**c)**8 and (3**c)**4 <= X
    assert t % 4 == 1 and all(t % p for p in (3, 7, 19))
assert R == 100004**2 + 41**2 and S % 121 == 110

assert n % 11 == (3**5 + b) % 11
assert all(pow(a, 90, 11) == 1 for a in (3, 5))
assert pow(5, 90, 121) != 1
assert len({pow(5, 90*j, 11**3) for j in range(121)}) == 121
retained = F(10, 121) / (1 - F(1, 121))
assert retained == F(1, 12) and F(12, 11)*retained == F(1, 11)
```

The unconditional new result is (1). Equation (4) gives the faster rate on the stated complement and isolates an arithmetic quantity for upgrading it. A faster unconditional low-mass rate and pointwise coverage remain open.