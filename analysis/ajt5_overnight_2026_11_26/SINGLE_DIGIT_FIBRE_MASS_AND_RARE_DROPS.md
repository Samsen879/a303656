# Single-digit fibre mass and a summable tail for catastrophic phase drops

**The actual \(3,5\) survivor fibres give a faster unconditional rate.** Write \(\log_j\) for the \(j\)-fold iterated logarithm. For some absolute \(c>0\),
\[
\Pr\!\left(0<\alpha_z<\frac1{\log z}\right)
\ll \exp\!\left[-c\sqrt{\log_3 z\,\log_4 z}\right].
\]
This is faster than every inverse power of \(\log_3 z\). The key bound is stronger at the prime-read scale. If \(J_q\) denotes a drop from a positive normalized head \(H_{q^-}\) to \(H_q<H_{q^-}/q\), including a drop to zero, then
\[
\boxed{\quad
\sum_{q>T}\Pr(J_q)\ll
\exp\!\left[-c\sqrt{\log T\,\log\log T}\right].
\quad}
\tag{1}
\]
In particular, almost surely only finitely many such drops occur. This uses the actual prime-power factors of the two orders and the shared survivor family. It requires no assumption on the number of common Wieferich primes.

### A mass bound from a single order digit

Let \(q\ge7\) be inert. Choose an odd prime power \(D=r^a\) dividing \(\operatorname{ord}_q(b)\) for \(b=3\) or \(5\). Vary just digit \(a-1\) of the \(r\)-primary coordinate of that exponent. The \(r\) choices give distinct shifts mod \(q\). The 2-adic support tests are unaffected by an odd-primary digit. An older inert prime \(p\ne r\) reads this digit only if \(D\mid\operatorname{ord}_p(b)\). Let \(\mathcal D\) be the set of older inert readers and put \(S_D=\sum_{p\in\mathcal D}1/(p+1)\).

Remove those readers and, if \(r\) is inert and \(b\) is a unit there, remove the source row at \(r\). The reference family \(\Omega\) passing all remaining rows is invariant under the digit variation. If \(\Omega\) has zero measure, the old head is zero. Otherwise normalize its measure to 1.

For an inert unit source, put \(h=a-1+v_r(b^{r-1}-1)\). The shift mod \(r^h\) is fixed along each digit orbit by LTE. Given \(n_r\), let \(V\) be the reference mass with even valuation below \(h\), and \(I\) the mass matching mod \(r^h\). The exceptional readings \(V<I\) have probability at most \(r^{-\lceil h/2\rceil}\). In the tree of shift masses, at each even depth below \(h\) the target child must contain more than half its parent's mass. Otherwise the sibling mass at that depth alone is at least \(I\). Each even depth therefore has at most one choice, and each odd depth at most \(r\). For a split or nonunit source use \(V=1,\ I=0\), since the source imposes no constraint on this digit.

When \(V\ge I\), restore the readers. Averaging over their still-unread target coordinates, the expected mass removed from the \(V\)-family is at most \(VS_D\). Markov bounds the probability that they remove more than \(V/4\) by \(4S_D\). The reference family and source target are independent of the removed readers' target coordinates. On the remaining readings, any single terminal residue contains at most \(V/r\) of the original \(V\)-family, by digit injectivity. Hence the actual old survivors outside any terminal residue have relative mass at least
\[
\frac{3V/4-V/r}{V+I}\ge\frac5{24}.
\]
The denominator bounds the entire old survivor mass in \(\Omega\). If \(V=I=0\), the old survivor mass is zero. This gives a mass bound for the whole family, extending the earlier reset argument for the existence of a surviving phase. [Earlier depth-reset argument](https://github.com/Samsen879/a303656/blob/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

A drop below \(1/q\) requires more than \(q/(q+1)\) of the old survivors to share \(n_q\bmod q\), since every noncolliding phase passes the new row. At most one residue does that, and \(n_q\) is independent of all the old reads. We obtain
\[
\Pr(J_q)\le \frac1q\min\{1,D^{-1/2}+4S_D\}.
\tag{2}
\]
The \(D^{-1/2}\) term can be omitted for split or nonunit sources. Brun–Titchmarsh and partial summation give \(S_D\ll(1+\log\log q)/\varphi(D)\), since every reader is \(1\bmod D\). [Montgomery–Vaughan](https://doi.org/10.1112/S0025579300004708)

### Summing over terminal orders

In a dyadic block \(U<q\le2U\), put \(v=\log U\) and \(B=\exp(\sqrt{v\log v})\). Since the terminal prime is inert, the 2-part of either order is at most 2. If either order has a prime-power factor above \(B\), (2) gives \(q^{-1}O(\exp[-c\sqrt{v\log v}])\). Otherwise \(\operatorname{ord}_q(5)\) is \(B\)-smooth. Orders at most \(U^{1/3}\) account for \(O(U^{2/3}/\log U)\) primes by grouping divisors of \(5^o-1\) by order.

For the remaining primes, the \(B\)-smooth part of \(q-1\) is at least \(U^{1/3}\). It has a divisor \(m\) between \(U^{1/6}\) and \(BU^{1/6}<\sqrt U\). Take \(s=(\log v)/(4\log B)\) and the nonnegative multiplicative weight \(g(r^j)=r^{js}-r^{(j-1)s}\). Since \(\sum_{d\mid m}g(d)=m^s\), Brun–Titchmarsh bounds the count by
\[
\ll\frac U{\log U}U^{-s/6}
\sum_{d\ B\text{-smooth}}\frac{g(d)}{\varphi(d)}.
\]
The logarithm of the Euler product is \(O(sB^s\log B)=O(v^{1/4}\log v)\), by summing its local increments
\((r^s-1)/[(r-1)(1-r^{s-1})]\).
The factor \(U^{-s/6}\) contributes \(\exp[-\sqrt{v\log v}/24]\). Thus the small-factor branch also has reciprocal charge \(O(\exp[-c\sqrt{v\log v}]/v)\). Summing the dyadic charges proves (1).

### From rare drops to low positive mass

Here are the transfer details. Take \(L=\log_2 z\), a power of two \(S\asymp\sqrt L\), and \(Y=\exp(\sqrt L/8)\). Beyond \(S\), a drop below \(1/q\) costs the error in (1). On a positive branch avoiding these drops, clip each downward log loss to \(\log q\). This leaves the actual downward losses on that branch. If \(r_q(a)\) is the old survivor fraction with shift \(a\bmod q\), the clipped loss is at most \((1+1/q)r_q(n_q\bmod q)\log q\), by the convex secant bound. Its conditional mean is \(O(\log q/q)\). The exponential secant with parameter \(1/\log Y\), iterated over the reads, bounds the probability of a total clipped loss exceeding \(\sqrt L\log Y=L/8\) by \(O(e^{-\sqrt L})\). The verified positive floor \(H_S\ge2^{-6S}\) then puts every head between \(S\) and \(Y\) above \(e^{-L/4}\) on the remaining positive branches. [Verified positive-head floor](https://github.com/Samsen879/a303656/commit/140d8a38fc7afc5b2ec5374760078a7040700a26)

Use checkpoints \(x_{j+1}=x_j^K\) through \(Y\), with \(x_0=S\) and \(K=\lceil\sqrt{\log L\log\log L}\rceil\). Uniform conditional \(L^2\) gives a fixed probability \(p_0>0\) of \(H_{x_{j+1}}\ge H_{x_j}/2\) from each positive head. At such a transition \(x\to y\), the relative-family variance for the unread primes is \(O(e^{-cK})\). To see this, the same smooth-divisor calculation above with smooth cutoff \(x\) and \(s=1/\log x\) gives a row excess \(O(e^{-c\log y/\log x})\). Restricting the second phase draw from \(A_x\) to \(A_y\) costs \(\alpha_x/\alpha_y\ll\sqrt K\) on the transition, by \(D_x\asymp(\log x)^{-1/2}\). The other order terms use the largest-prime expansion. [Conditional second moment](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e) · [Relative-family variance argument](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

At the first successful transition, Chebyshev costs \(O(e^{-cK})\) for \(H_z\) to fall below half the new head. The low positive event requires this, since its \(H_z\) threshold is \(O(e^{-L/2})\). A positive branch with no successful transition costs \((1-p_0)^k\), where \(k\asymp\log L/\log\log L\). Adding (1) at \(S\) gives the stated rate. For any fixed earlier finite residue class, the same rate holds with a constant depending on its measure.

The zero-atom identity also gives a direct consequence of (1): the mass of modular obstructions still undetected at cutoff \(z\) is \(O(\exp[-c\sqrt{\log z\,\log\log z}])\). A later first zero on a positive branch requires a \(J_q\). The low-mass rate improves the error in the verified logarithmic matching transfer at its stated coefficient. Pointwise coverage remains open. [Zero atom and finite obstructions](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e) · [Matching transfer](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

### Exact arithmetic replay

The replay passed. The \(3\)-digit orbit gives terminal shifts \(15,21,19\bmod43\). Two actual targets agree modulo 4 and all listed old primes other than 3. At 3, one target leaves just one of the three digits and the other leaves all three. Both targets have a true norm at the first cell in the ordinary-height box. This checks why the source-row term in (2) is needed.

```python
from math import prod

q, c, d, step = 43, 300, 440, 110
old = (7, 11, 19, 23, 31)
X = 5**1320
M = 18 * prod(old)
u = M * ((5**660 + M - 1) // M)

def shifts(p):
    return [(pow(3,c,p)+pow(5,d+step*j,p)) % p for j in range(3)]

assert shifts(q) == [15, 21, 19]
assert [p for p in old if len(set(shifts(p))) > 1] == [7, 19, 31]
assert len(set(shifts(9))) == 3

for w, want in [(3, [2,1,1]), (3+4*q*prod(old), [0,0,0])]:
    n = 3**c + 5**d + u*u + w*w
    assert X < n <= 2*X and X <= 3**(8*c) and 3**(4*c) <= X
    vals = []
    for j in range(3):
        b = 5**(d+step*j)
        t = n - 3**c - b
        assert X <= b**3 and b*b <= X
        assert t > 0 and t%4 == 1 and all(t%p for p in old)
        if j == 0:
            assert t == u*u + w*w
        v = 0
        while t%3 == 0:
            v, t = v+1, t//3
        vals.append(v)
    assert vals == want
```

Independent BigInt replay verified both true norm controls, the exact three terminal shift residues, and source valuations (2,1,1) versus (0,0,0). The new tail controls the difference between finite-panel and limiting obstruction mass; it does not estimate the finite-panel subtotal more sharply, so the verified numerical exception bound is unchanged.
