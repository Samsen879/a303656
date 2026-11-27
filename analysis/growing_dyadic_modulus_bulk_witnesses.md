# Label-dependent core progressions for a growing dyadic modulus

There is an absolute \(c_*>0\) such that, for \(Q=27\cdot2^k\) with \(k\ge3\) and \(Q\le \exp(c_*\sqrt{\log X})\), every class \(b\bmod Q\) has a uniform positive fraction of targets in \([X,2X]\) with deletion-robust bulk witnesses. In the original two exponent windows, these targets retain \(\gg(\log X)^{3/2}\) witnesses and \(\gg\sqrt{\log X}\) edge-disjoint matchings of size \(\gg\log X\) after any permitted \(\epsilon\log X\) exponent-vertex deletions. The constants are independent of \(k,b,X\) in this range. Powers of \(2\) alone follow by taking one refinement modulo \(27\). [Draft PR #82](https://github.com/Samsen879/a303656/pull/82/files)

### Fix the valuation, vary the core progression

Put \(L=\log X\). Use the original windows
\[
X^{1/8}\le3^c\le X^{1/4},\qquad
X^{1/3}\le5^d\le X^{1/2}.
\]
For a class \(b\bmod Q\), choose the exponent classes **only at the fixed modulus \(216\)**. In the ordinary classes choose the parity box and \(d\bmod18\) so that the residual has \(v_2=0\) or \(1\), is coprime to \(3\), and has odd part \(1\bmod4\). In the four restored even classes, choose \(5^d\equiv b-18\bmod27\) with the required parity. This gives residual \(18\bmod216\). In all cases the box fixes a multiplier \(D\in\{1,2,18\}\), with \(\asymp L\) actual exponents on each axis.

For each actual label \(\lambda=3^c+5^d\) in that box, take residuals \(m=Du\) with \(u\) an odd squarefree norm in
\[
u\equiv (b-\lambda)/D\pmod{Q/D},\qquad X\le Du\le3X/2.
\]
The quotient class is reduced and is \(1\bmod4\). **It changes with the label.** Keeping \(D\) fixed handles the \(2\)-adic valuation, while allowing the progression to change retains the full size of both exponent axes. Adding the label gives \(n\in[X,2X]\) and the ordinary residual \(m\ge n/2\) for sufficiently large \(X\).

### Uniform first moment and class-restricted energies

For each label there are \(\gg X/(Q\sqrt L)\) cores in its own progression. To see this, use the draft’s squarefree split-prime product \(A\le X^{1/4}\), with primes at most \(X^\delta\) for a sufficiently small fixed \(\delta\). Its reciprocal sum is \(\asymp\sqrt L\). Complete \(u=Aq\) with a prime in \([X/(DA),3X/(2DA)]\), in the reduced class modulo \(Q/D\) determined by that label and \(A\). The large prime is unique in the product. [Williams, *Mertens’ Theorem for Arithmetic Progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf) · [Draft squarefree norm construction](https://github.com/Samsen879/a303656/pull/82/files)

The prime count here is uniform. For moduli \(2^j3^i\) with \(i\le3\), every real character is induced from a conductor dividing \(216\), since real characters on the \(2\)-part factor through modulus \(8\). Thus the possible exceptional real zeros come from a fixed finite list, separated from \(1\). The classical Dirichlet zero-free region and truncated explicit formula, with truncation height \(\exp(\sqrt{\log y})\), give an absolute error \(O(y\exp(-c_1\sqrt{\log y}))\) in the progression prime-power count for sufficiently small exponential modulus range. Here \(y\gg X^{3/4}\); taking \(c_*\) small makes the error smaller than the main term \(y/\varphi(Q/D)\). Removing prime powers gives \(\gg X/(AQL)\) choices of \(q\). Summing over \(A\) proves the per-label lower bound. [Davenport, *Multiplicative Number Theory*, Chapters 14–22](https://link.springer.com/book/9780387950976)

For the upper bounds, write the targets in the class as \(n=b+Qj\). The sieve variable \(j\) has interval length \(\asymp X/Q\). At every inert prime except \(3\), the core slope \(Q/D\) is invertible. For one label there is one forbidden class. For two distinct labels with gap \(h\), there are two forbidden classes except at primes dividing \(h/D\), where they coincide. The upper-bound sieve therefore gives, uniformly,
\[
\begin{aligned}
\text{one-label count}&\ll \frac{X}{Q\sqrt L},\\
\text{two-label count}&\ll \frac{X}{QL}\frac{|h|}{\varphi(|h|)}.
\end{aligned}
\]
The logarithm of the sieve interval is comparable to \(L\) throughout the asserted modulus range. The factor \(1/Q\) in the pair estimate comes from sieving **inside** the target class. [Tao and Teräväinen, Lemma 3.2](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12663)

The reciprocal-order gap sums from the draft remain \(O(L^4)\) for the full box and \(O(L^2)\) at a fixed vertex, since the varying bases are fixed powers of \(3\) and \(5\). If \(F(n)\) is the edge count and \(d_v(n)\) the vertex degrees, the resulting estimates are
\[
\sum_{n\equiv b\ (Q)} F(n)\asymp \frac XQ L^{3/2},
\qquad
\sum_{n\equiv b\ (Q)}F(n)^2\ll \frac XQ L^3,
\qquad
\sum_{n\equiv b\ (Q)}\sum_v d_v(n)^2\ll \frac XQ L^2,
\]
with all sums over \([X,2X]\). Cauchy–Schwarz and a degree-energy cutoff retain \(\gg X/Q\) distinct targets with \(F(n)\gg L^{3/2}\) and degree energy \(O(L^2)\). Deleting \(\epsilon L\) vertices costs \(O(\sqrt\epsilon L^{3/2})\) edges. Trimming degrees above \(C\sqrt L\) leaves a fixed fraction of the edges, and repeated maximal matchings then give the stated conclusion. [Radomskii, Lemma 3.1](https://arxiv.org/html/2504.09954v7#S3) · [Draft PR #82](https://github.com/Samsen879/a303656/pull/82/files)

For comparison, **one box frozen at the full \(2^k\) period** has only \(O(1+L/2^k)\) exponents per axis, since both bases have order \(2^{k-2}\bmod2^k\). With a bounded multiplier, its certified fraction is at most \(O((1+L/2^k)^2/\sqrt L)\) by the one-label bound. Positive-fraction coverage by that particular method requires \(2^k=O(L^{3/4})\). The label-dependent construction avoids that ceiling. The growing-modulus theorem still gives a positive fraction, with no pointwise claim.

### Exact same-target check

At \(X=10^{10}\), \(Q=27\cdot2^{16}\), take \(n=10000016714\equiv730442\bmod Q\). Both \((5,5)\) and \((3,5)\) lie in the actual windows and the same mod-\(216\) box. Their core classes modulo \(Q/18\) are different. The first gives
\[
n-3^5-5^5=18\cdot555556297=99111^2+13305^2,
\]
with \(555556297\) a split prime. The second leaves a bulk positive residual with \(v_7=1\). The following replay checks both. It illustrates actual labels but does not choose a numerical asymptotic threshold for the theorem.

```python
from math import isqrt

X, n = 10**10, 10000016714
Q, D = 27*2**16, 18
good = n - 3**5 - 5**5
bad = n - 3**3 - 5**5
u = good // D

assert n % Q == 730442 and n % 216 == 146
assert good % 216 == bad % 216 == 18
assert (u % (Q//D), (bad//D) % (Q//D)) == (40393, 40405)
assert good == D*555556297 == 99111**2 + 13305**2
assert u % 4 == 1 and all(u % j for j in range(2, isqrt(u)+1))
assert bad % 7 == 0 and bad % 49 != 0
assert X <= min(good, bad) <= max(good, bad) <= 3*X//2
assert all(3**(8*c) >= X >= 3**(4*c) for c in (3, 5))
assert 5**15 >= X >= 5**10
```
