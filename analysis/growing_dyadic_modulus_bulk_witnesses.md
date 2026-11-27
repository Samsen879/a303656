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

## Polynomial short windows and moduli

**A polynomial short-window bound follows unconditionally from the prime number theorem for powerful moduli.** Fix \(0<\varepsilon<5/12\). For all sufficiently large \(X\), every interval \((T,T+H]\) with \(X\le T\le2X\) and
\[
QX^{7/12+\varepsilon}\le H\le X,\qquad Q=27\cdot2^k,\quad k\ge3,
\]
contains \(\gg_\varepsilon H/Q\) distinct deletion-robust targets in **each** prescribed class \(b\bmod Q\). The constants are uniform in \(T,H,k,b\). The witnesses use the two original exponent windows from draft PR #86, and their ordinary residuals are at least \(n/2\). [Draft PR #86](https://github.com/Samsen879/a303656/pull/86/files)

In particular, for \(Q\le X^{5/12-\varepsilon}\), a run inside \([X,2X]\) without a robust target has length \(O_\varepsilon(X^{7/12+\varepsilon})\) **measured in consecutive members of the prescribed class**, or \(O_\varepsilon(QX^{7/12+\varepsilon})\) in integer distance. The estimate is unconditional in this joint range. For a specified \(n\), taking \(T=n\) and \(b=n\bmod Q\) certifies a later target in that class. Its residuals differ from those of \(n\) by a positive multiple of \(Q\), so the theorem leaves representability of the specified \(n\) open.

### Local choices and the first moment

Put \(L=\log X\). Use the actual exponents
\[
X^{1/8}\le3^c\le X^{1/4},\qquad
X^{1/3}\le5^d\le X^{1/2}.
\]
For a class \(b\bmod Q\), fix \(c\bmod2\) and \(d\bmod18\) at modulus \(216\) alone. Here is the local check. For \(c\ge3\), the choices of the two parities give \(3^c+5^d\bmod24\) in \(\{4,8,10,14\}\). Subtracting one of these from \(b\) gives a residual class in \(\{1,5,13,17,2,10\}\) except when \(b\bmod24\) is \(2,4,8,22\). In the first four residual classes use \(D=1\), and in the last two use \(D=2\). In the four exceptional target classes, \(b-18\) is a unit modulo \(27\). Since \(5\) has order \(18\) modulo \(27\), choose \(5^d\equiv b-18\bmod27\). The parity of \(d\) is determined by \(b\bmod3\). For \(b\bmod24=2,4,8,22\), respectively, the required parities of \(c\) are even, odd, even, odd, giving residual \(2\bmod8\). The residual is therefore \(18\bmod216\), and \(D=18\) works.

In every case, with \(\lambda=3^c+5^d\) and \(q=Q/D\), the quotient class
\[
u\equiv r_\lambda=(b-\lambda)/D\pmod q
\]
is reduced and is \(1\bmod4\). Each exponent axis still has \(\asymp L\) choices. The \(\asymp L^2\) labels are distinct because successive permitted \(5^d\) differ by more than the entire span of the \(3^c\) axis. For a given label the core interval is
\[
\frac{T-\lambda}{D}<u\le\frac{T+H-\lambda}{D}.
\]
It has length \(H/D\) even if \(H<\lambda\). Uniformly in the window, \(n-\lambda\ge n/2>0\) for large \(X\).

To count cores, choose \(0<\tau<\varepsilon/4\) and a sufficiently small fixed \(\delta>0\) in terms of \(\tau\). Take \(A\le X^\tau\) among squarefree products of primes \(p\le X^\delta\) with \(p\equiv1\bmod4\). Their reciprocal sum is \(\asymp_\varepsilon\sqrt L\). Indeed, the unrestricted product \(\prod_p(1+1/p)\) has that order by Mertens in the split class. Under the normalized reciprocal weights the expected \(\log A\) is \(\sum_p\log p/(p+1)\ll\delta L\). Markov’s inequality therefore keeps a fixed fraction of the weight below \(X^\tau\). [Williams, *Mertens’ Theorem for Arithmetic Progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf)

Complete \(u=A\ell\) with a prime \(\ell\equiv r_\lambda A^{-1}\bmod q\). The upper endpoint and length of its interval are
\[
Y=\frac{T+H-\lambda}{DA}\asymp X/A,\qquad h=\frac{H}{DA}.
\]
Here \(3\le h<Y\), \(\operatorname{rad}(q)\mid6\), and, with \(\eta=\varepsilon/2\),
\[
\frac{h}{\phi(q)}\ge\frac{H}{AQ}\ge\frac{X^{7/12+\varepsilon}}{A},
\qquad
\frac{h/\phi(q)}{Y^{7/12+\eta}}
\gg X^{\varepsilon/2}A^{-(5/12-\eta)}\longrightarrow\infty.
\]
Thorner and Zaman’s Corollary 3.1 and equation (3.2) thus give a weighted prime count asymptotic to \(h/\phi(q)\) for large \(q\). The squarefree part of \(q\) is bounded, so the corollary’s exceptional-zero exclusion applies above a fixed threshold. Its relative error tends uniformly to zero since \(\log(qY/h)=O(\log Y)\). For the remaining bounded moduli, Theorem 1.1 and Remark 1.3 give the same conclusion, since the finitely many possible exceptional zeros are separated from \(1\). This yields \(\gg_\varepsilon H/(AQL)\) primes. Each is split and larger than all prime factors of \(A\), so the resulting cores are squarefree and each has a unique such factorization. Summing over \(A\) gives \(\gg_\varepsilon H/(Q\sqrt L)\) cores per label. Each \(Du\) is a sum of two squares because \(u\) is a product of split primes and \(D=1,2,\) or \(18\) is a sum of two squares. [Thorner and Zaman, *Refinements to the prime number theorem for arithmetic progressions*](https://arxiv.org/pdf/2108.10878)

### Both energies inside the target class

Write \(n=b+Qj\). There are \(J\asymp H/Q\) consecutive \(j\)’s, with \(\log J\asymp L\). At an inert prime \(p\ne3\) the slope \(Q/D\) of every core is invertible. One label forbids one class of \(j\bmod p\). Two labels forbid two classes unless \(p\) divides their gap \(g=\lambda-\lambda'\), in which case the classes coincide. Applying the upper-bound sieve after translating the \(j\)-interval gives
\[
N_\lambda\ll J/\sqrt L,\qquad
N_{\lambda,\lambda'}\ll \frac{J}{L}\frac{|g|}{\phi(|g|)}.
\]
The pair bound uses \((p-1)/(p-2)\le (1-1/p)^{-1}(1+O(p^{-2}))\) for the coincident classes. Both estimates retain the factor \(1/Q\). [Tao and Teräväinen, Lemma 3.2](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12663)

The sum of the gap weights is \(O(L^4)\) over all ordered distinct labels and \(O(L^2)\) over ordered distinct labels incident to any fixed exponent vertex. To see the latter, fix one edge at that vertex and vary the other exponent. For a prime coprime to the varying base \(B\), there are \(O(1+L/\operatorname{ord}_p(B))\) occurrences of a prescribed residue. Radomskii’s Lemma 3.1 with \(s=1\) bounds the weighted sum over those \(O(L)\) gaps by \(O(L)\). The constant term in the occurrence bound contributes \(O(\log L)\), and \(\sum_{p\nmid B}(\log p)/(p\operatorname{ord}_p(B))<\infty\). For example, in \(P<p\le2P\) the primes of order at most \(P^{1/3}\) divide \(\prod_{j\le P^{1/3}}(B^j-1)\), giving \(O(P^{2/3}/\log P)\) such primes. The complementary orders give a summable dyadic contribution as well. Primes dividing the fixed base cost a constant factor. For the full gap sum, fix one label and the other label’s exponent on one axis, apply the same bound to the remaining axis, then sum. [Radomskii, Lemma 3.1](https://arxiv.org/html/2504.09954v7#S3)

Let \(F(n)\) be the number of norm edges in the bipartite graph on the two exponent axes, and \(d_v(n)\) its vertex degrees. Summing the single-label and pair bounds gives, over this window and class,
\[
\sum_n F(n)\asymp_\varepsilon J L^{3/2},\qquad
\sum_n F(n)^2\ll J L^3,\qquad
\sum_n\sum_v d_v(n)^2\ll J L^2.
\]
The first two estimates and Cauchy–Schwarz retain \(\gg_\varepsilon J\) targets with \(F(n)\gg_\varepsilon L^{3/2}\). The third lets us retain a positive fraction of those with degree energy \(O_\varepsilon(L^2)\). For each retained target, deleting any \(\rho_\varepsilon L\) exponent vertices costs at most \(O_\varepsilon(\sqrt{\rho_\varepsilon}L^{3/2})\) edges by Cauchy–Schwarz. Choose \(\rho_\varepsilon>0\) sufficiently small. Then remove vertices of degree above \(C_\varepsilon\sqrt L\), losing at most the degree energy divided by \(C_\varepsilon\sqrt L\). A sufficiently large \(C_\varepsilon\) leaves \(\gg_\varepsilon L^{3/2}\) edges and maximum degree \(O_\varepsilon(\sqrt L)\). Repeated greedy matchings yield \(\gg_\varepsilon\sqrt L\) edge-disjoint matchings of size \(\gg_\varepsilon L\). Each round can stop at that size, so the degree bound continues to guarantee the next round while a fixed fraction of the edges remains.

### The input needed for shorter windows

The limiting step here is the **lower first moment**. Both energy bounds already work whenever \(\log(H/Q)\asymp\log X\). In that range, it would suffice to prove a lower bound of order \(H/(Q\sqrt{\log X})\) for odd squarefree norms in the translated core progression above, uniformly in the window and class and averaged over the actual labels. For the prime-completion proof specifically, a sufficient replacement is a uniform lower bound \(\gg h/(\phi(q)\log Y)\) in the induced reduced classes at \(Y=(T+H-\lambda)/(DA)\), \(h=H/(DA)\), for products \(A\) retaining reciprocal mass \(\gg\sqrt{\log X}\). In this argument neither estimate is supplied below the stated joint range. A short-interval prime theorem without the prescribed progression does not supply it.

### Finite check of the uniform local boxes

The finite box selection uses only the following calculation. No small-scale test substitutes for the asymptotic sieve proof.

```python
from math import gcd
for b in range(216):
    choices = []
    for c in (3, 4):
        for d in range(18):
            m = (b - pow(3, c, 216) - pow(5, d, 216)) % 216
            for D in (1, 2, 18):
                if m % D == 0 and gcd(m//D, 216//D) == 1 and (m//D) % 4 == 1:
                    choices.append(D)
    assert choices
    if b % 24 in (2, 4, 8, 22):
        assert set(choices) == {18}
    else:
        assert any(D in (1, 2) for D in choices)
```
