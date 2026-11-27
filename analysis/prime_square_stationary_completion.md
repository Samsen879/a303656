# Prime-square stationary completion for the semiprime collision problem

Part of the [balanced-semiprime second moment](https://github.com/Samsen879/a303656/pull/71). Here (H) is the logarithm of the target height, and the interval under study tracks actual base-nine exponents; this is a spectral reduction, not a target coverage assertion.

The narrow Fourier mass from characters that miss either prime-square lifting digit is \(O(\sqrt H)\), below the required \(H/(\log H)^5\) scale. For characters primitive at both prime squares, completion gives an exact formula with one surviving coarse exponent per frequency. That formula also gives a counter to an absolute-value completion argument: even though the untwisted complete sum vanishes, the absolute completion bound is already of order \(H\) on an interval of length \(\asymp H\).

### The characters missing a lifting digit are controlled

Let \(H=\log X\), take balanced inert primes \(p,q\asymp\sqrt H\) in the same interval as before, and suppose \(9\) lifts at both prime squares. Write \(s=pq\), \(M=s^2\), \(r=\operatorname{ord}_s(9)\asymp H\), and \(R=sr=\operatorname{ord}_M(9)\). Let \(J\) be the actual \(O(H)\)-length exponent interval with the nonunit values \(1-9^e\) omitted. For \(G=(\mathbb Z/M\mathbb Z)^\times\), put
\[
S_J(\chi)=\sum_{e\in J}\chi(1-9^e).
\]

Fix **any** lifting digit of \(\chi\) at \(p\), allowing all other character components to vary. The resulting characters form a coset of the characters factoring through \(pq^2\). Orthogonality gives
\[
\frac1{|G|}\sum_{\chi\text{ with that digit}}|S_J(\chi)|^2
=\frac{|J|}{p}.
\]
Indeed, equality of the values \(1-9^e\bmod pq^2\) forces the exponent difference to be a multiple of \(qr\gg H\), so only equal exponents contribute. The same argument gives \(|J|/q\) at \(q\). Taking the zero digit at either prime bounds all imprimitive contributions by \(O(\sqrt H)\), even before restricting to the narrow frequency window.

### Exact completion for the doubly primitive characters

Write \(\chi(9)=e^{2\pi i\alpha/R}\). Split an exponent as \(e=e_0+ru\), where \(0\le e_0<r\). At a prime \(v=p,q\), this is an iterated step along the smaller local period \(r_v=\operatorname{ord}_v(9)\), since \(r_v\mid r\). For unit \(1-9^{e_0}\), the lifting digit changes exactly by
\[
F_v(1-9^{e_0+ru})-F_v(1-9^{e_0})
\equiv-rF_v(9)\frac{9^{e_0}}{1-9^{e_0}}\,u\pmod v.
\]
Here \(F_v(z)=(z^{v-1}-1)/v\bmod v\). This follows by expanding \(9^{ru}\) modulo \(v^2\). [Bourgain, Ford, Konyagin and Shparlinski, *On the divisibility of Fermat quotients*](https://doi.org/10.1307/mmj/1281531459)

Complete the sum over the \(R\)-cycle with twist \(e^{2\pi i\nu e/R}\), setting its summand to zero at nonunits. For a character primitive at both squares, the two lift sums over \(u\bmod p\) and \(u\bmod q\) vanish unless
\[
9^{e_0}\equiv\frac{\nu}{\nu+\alpha}\pmod s,
\]
with both \(\nu\) and \(\nu+\alpha\) units modulo \(s\). There is at most one such \(e_0\bmod r\). When it exists, the complete twisted coefficient is exactly
\[
s\,\chi(1-9^{e_0})e^{2\pi i\nu e_0/R}.
\]
In particular, the coefficient vanishes at \(\nu=0\) and at every frequency divisible by \(p\) or \(q\).

**Why absolute completion is insufficient.** In one block \(0\le\nu<s\), exactly \(r-r/r_p-r/r_q+1\asymp H\) frequencies survive. The correspondence is the bijection \(\nu=\alpha z/(1-z)\bmod s\) for the eligible \(z=9^{e_0}\). For an ordinary exponent interval \(I\) of length \(N\asymp H\) with \(N\le r/4\), its unnormalized Fourier coefficient has magnitude \(\gg N\) for \(0\le\nu<s\). Consequently, these frequencies alone contribute \(\gg Ns/R\cdot r\asymp H\) to the absolute-value completion bound. The cancellation needed for the narrow mass must involve the surviving phases.

More explicitly, let \(e_\nu\) denote the unique surviving exponent when it exists, and use the unnormalized interval transform \(\widehat{1_I}(\nu)=\sum_{e\in I}e^{-2\pi i\nu e/R}\). The remaining estimate is
\[
\frac1{|G|}
\sum_{\substack{\chi\ \mathrm{primitive\ at\ both\ squares}\\
                 \|\alpha/R\|\le(\log H)^5/H}}
\left|
\frac1r\sum_{\nu:\,e_\nu\ {\rm exists}}
\widehat{1_I}(\nu)\,\chi(1-9^{e_\nu})e^{2\pi i\nu e_\nu/R}
\right|^2
\ll \frac{H}{(\log H)^5}.
\]
This is a phase-sensitive estimate on the completed stationary contributions, with both prime axes coupled through \(e_\nu\). I did not establish it or the supply of lifted pairs needed for target coverage. [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### Exact inline replay

At \(p=19,q=23\), take the character whose phase is \(F_{19}(z)/19+F_{23}(z)/23\). Its restriction index is \(\alpha=16137\bmod43263\). In the block \(0\le\nu<437\), exactly \(80\) frequencies survive. At \(\nu=36\), the sole surviving coarse exponent is \(e_0=1\), and the two digit slopes are \(10\bmod19\) and \(9\bmod23\). The standard-library replay verifies these exact digit and frequency statements.

```python
from math import gcd

p, q, r = 19, 23, 99
s, R = p*q, p*q*r

def F(z, v):
    return (pow(z, v-1, v*v) - 1) // v % v

def slope(e, v):
    z = pow(9, e, v)
    return -r*F(9, v)*z*pow(1-z, -1, v) % v

def survivors(nu):
    return [e for e in range(r)
            if gcd(1-pow(9, e, s), s) == 1
            and all((slope(e, v) + nu*pow(s//v, -1, v)) % v == 0
                    for v in (p, q))]

assert [F(9, v) for v in (p, q)] == [17, 11]
assert [slope(1, v) for v in (p, q)] == [10, 9]
alpha = r*(q*17 + p*11) % R
assert alpha == 16137 and 36*pow(36+alpha, -1, s) % s == 9
assert survivors(36) == [1]
assert survivors(0) == survivors(p) == survivors(q) == []
assert sum(bool(survivors(nu)) for nu in range(s)) == 80
for v in (p, q):
    for u in range(s):
        assert (F(1-pow(9, 1+r*u, v*v), v)-F(1-9, v)) % v == slope(1, v)*u % v
```
## Double orthogonality and a necessary full-log Fejér test

The two character averages can be performed exactly. Averaging over characters with a fixed restriction to the base-\(9\) orbit leaves a joint CRT log. Averaging over restriction indices with fixed lifting digits then leaves a short geometric sum in the **coarse** log. That second average alone still costs \(\Omega(H)\) if the surviving terms are charged by absolute value. A positive-kernel calculation gives a sharper necessary test: the **full** CRT logs must have few close pairs at scale \(H/(\log H)^5\).

### Exact double orthogonality

Put \(H=\log X\), \(s=pq\), \(M=s^2\), \(r=\operatorname{ord}_s(9)\asymp H\), and \(R=sr\). Assume the orders lift at both balanced primes. Write \(\mathrm e(x)=\exp(2\pi i x)\), and use restriction indices \(\chi(9)=\mathrm e(\alpha/R)\). Doubly primitive characters correspond to \(\gcd(\alpha,s)=1\).

For each eligible \(e\bmod r\), set \(z_e=1-9^e\bmod M\), \(\beta_e=9^e/(1-9^e)\bmod s\), and let \(U_e\) be the actual set of integers \(u\) with \(e+ru\) in the exponent interval. If \(a=\alpha\bmod s\), the stationary formula gives
\[
S_I(\chi)=\sum_e\chi(z_e)W_e(a),\qquad
W_e(a)=\sum_{u\in U_e}\mathrm e(-a\beta_e u/s).
\]
The two local lifting conditions are both retained in the single residue \(\beta_e\bmod s\).

Let \(\Gamma=\langle9\rangle\bmod M\). Averaging \(|S_I(\chi)|^2\) over the extensions of a fixed \(\alpha\) keeps exactly the pairs with \(z_e/z_f\in\Gamma\). For such a pair let \(L_{ef}\bmod R\) be its full log. Its surviving phase is \(\mathrm e(\alpha L_{ef}/R)\). Writing \(\alpha=a+sb\), the normalized narrow mass is therefore exactly
\[
\frac1R\sum_{\substack{a\bmod s\\(a,s)=1}}
\sum_{z_e/z_f\in\Gamma}
W_e(a)\overline{W_f(a)}\,\mathrm e(aL_{ef}/R)
\sum_{\substack{b:\\a+sb\ \text{in the narrow band}}}
  \mathrm e(bL_{ef}/r).
\]
This formula keeps the actual interval through \(U_e\) and the exact band endpoints through the inner sum. In a band made of full digit blocks, expanding \(W_e\overline{W_f}\) also evaluates the \(a\)-sum by inclusion–exclusion over \(p,q\), with phase numerator \(L_{ef}-r(\beta_e u-\beta_f v)\). The lift and interval information survives in that numerator. [Dirichlet character orthogonality](https://kskedlaya.org/ant/chapter-4.html)

### What the second average can and cannot save

Take an interval of length \(\asymp r\) lying inside one coarse period, so that each retained exponent has one lift and \(|W_e(a)|=1\). Let \(B\asymp(\log H)^5\) be the length of the \(b\)-sum. The projection of \(\Gamma\) modulo \(s\) has bounded index, and the lifting hypothesis makes \(\Gamma\) contain the entire reduction kernel. Thus equal coarse cosets already imply a full log exists.

In each coarse coset, partition its log circle into \(O(B)\) arcs of length at most \(r/(100B)\). Pigeonholing gives \(\gg r^2/B\) off-diagonal pairs with \(\|L_{ef}/r\|\le1/(100B)\). For every such pair, the \(b\)-sum has magnitude \(\gg B\). Charging those terms by absolute value after the \(b\)-average therefore costs
\[
\gg \frac{\varphi(s)}R\frac{r^2}{B}B\asymp H,
\]
above the required \(H/(\log H)^5\). This obstruction comes **after** fixed-restriction orthogonality and the geometric-sum average. It leaves cancellation in the remaining digit phases open.

There is also a positive-kernel test for the actual incomplete interval. Take all eligible actual exponents \(i,j\in I\), including their lifts, and let \(L(i,j)\bmod R\) be the full log of \((1-9^i)/(1-9^j)\) when it exists. With \(A=\lfloor R(\log H)^5/H\rfloor\), triangular weights \(1-|\alpha|/A\) yield the nonnegative Fejér kernel in \(L(i,j)/R\). Every pair with circular log distance at most \(R/(10A)\) contributes \(\gg A/R\) to the weighted normalized mass. Hence the desired narrow-mass estimate **requires**
\[
\#\{(i,j)\in I^2:\ L(i,j)\text{ exists and }
               |L(i,j)|_R\le R/(10A)\}
\ll \frac{H^2}{(\log H)^{10}}.
\]
The imprimitive mass is \(O(\sqrt H)\), so including it in this necessary test does not change the budget. The new counting problem concerns short distances between **full lifted logs** of actual exponent values. Small coarse-log distance is insufficient. I did not establish this count or a supply of lifted prime pairs. [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### New exact character replay

With \(p=19,\ q=23\), take \(e=10,f=16\). The ratio has full log \(39898\bmod43263\) and coarse log \(1\bmod99\). The character
\[
\chi(z)=\mathrm e\!\left(7F_{19}(z)/19+12F_{23}(z)/23\right)
\]
is primitive at both squares, with restriction index \(\alpha=99\). Its phase on the ratio is \(\mathrm e(131/437)\). Moving \(\alpha\) by \(437\) keeps both digit components and advances the pair phase by just \(\mathrm e(1/99)\). This is an exact example of a slowly rotating term in the \(b\)-average whose full log is far from zero. The integer replay checks these identities.

```python
from math import gcd

p, q, r = 19, 23, 99
s, M, R = p*q, (p*q)**2, p*q*r

def F(z, v):
    return (pow(z, v-1, v*v) - 1) // v % v

z = lambda e: (1-pow(9, e, M)) % M
a, b = z(10), z(16)
L = 39898
assert (a, b) == (118571, 64255) and gcd(a*b, s) == 1
assert a*pow(b, -1, M) % M == 114503 == pow(9, L, M)
assert L % r == 1 and L % s == 131

alpha = r*(q*7*F(9, p) + p*12*F(9, q)) % R
assert alpha == 99
assert (q*7*(F(a, p)-F(b, p)) + p*12*(F(a, q)-F(b, q))) % s == 131
for i in range(r):
    shifted = (alpha+s*i) % R
    assert gcd(shifted, s) == 1
    assert (shifted*L-alpha*L) % R == s*i % R
```
## Single-scale equivalence for the full-log criterion

The Fejér criterion is **necessary and sufficient at one full-log scale**. The longer-distance terms do not require separate estimates. For the balanced lifted layer, the narrow Fourier budget is equivalent to bounding the number of ordered exponent pairs at full-log distance \(H/(\log H)^5\) by \(O(H^2/(\log H)^{10})\). I did not establish that arithmetic bound for the growing moduli.

### A single-scale equivalence

Let \(H=\log X\), \(M=(pq)^2\), \(G=(\mathbb Z/M\mathbb Z)^\times\), and \(\Gamma=\langle9\rangle\) of order \(R\). Use the actual exponent interval \(I\), retaining \(e\) when \(z_e=1-9^e\bmod M\) is a unit. Keep multiplicities. Inside each coset of \(\Gamma\), choose an origin and give \(z_e\) its full log coordinate in \(\mathbb Z/R\mathbb Z\). Define \(C(D)\) to count ordered pairs in the same coset with circular log distance at most \(D\), including the diagonal.

For \(2\le A\le R/4\), let \(\mathcal M(A)\) be the normalized mass of \(|\sum_{e\in I}\chi(z_e)|^2\) over characters with \(\chi(9)=\exp(2\pi i\alpha/R)\) and \(|\alpha|\le A\). Then, with absolute constants,
\[
\boxed{\quad \mathcal M(A)\asymp \frac AR\,C(R/A).\quad}
\]

For the lower bound, average over the extensions of each restriction and use triangular weights of bandwidth \(A\). The resulting Fejér kernel is \(\gg A\) at log distances at most \(R/(10A)\). For the upper bound, twice the triangular weight of bandwidth \(2A\) majorizes the sharp frequency cutoff. Its kernel is \(O(A(1+A|L|_R/R)^{-2})\) at full log difference \(L\). [NIST DLMF, Fejér kernel](https://dlmf.nist.gov/1.15.E15)

The step that closes the comparison is
\[
C(kD)\ll(k+1)C(D),\qquad k\ge1.
\]
Partition each log circle into arcs of lengths between \(D/2\) and \(D\). If their occupancies are \(n_j\), then \(\sum n_j^2\le C(D)\). A distance at most \(kD\) joins only \(O(k+1)\) neighboring arcs for each arc. Applying \(2n_i n_j\le n_i^2+n_j^2\) proves the bound. It compares the two constant-factor scales in the lower bound and makes the dyadic upper tail summable.

For the lifted balanced layer, \(R\asymp H^2\) and \(A\asymp R(\log H)^5/H\). This gives the stated equivalence. The imprimitive contribution is \(O(\sqrt H)\) by orthogonality modulo \(pq^2\) and \(p^2q\), so the same criterion applies to the doubly primitive mass at the required scale. The comparison itself uses no lifting assumption.

### Order and thinning costs

If \(N\) eligible exponents remain, equality \(z_e=z_f\bmod M\) holds exactly when \(e\equiv f\bmod R\). Consequently,
\[
C(0)\ge N^2/R.
\]
At the bandwidth above, a family with \(N\asymp H\) and \(R=o((\log H)^{10})\) therefore fails the narrow-mass budget. More generally, if \(N_0\) exponent values lie in log arcs of width \(D\) occupying only \(K\) bins across all cosets, their contribution to \(C(D)\) is at least \(N_0^2/K\). These are full-order and concentration obstructions. In the large-order lifted case, the period bound alone leaves room for the desired spacing.

The comparison also quantifies what a generic thinning argument buys. On the eligible exponents, join two distinct vertices if their full-log distance is at most \(D\) in the same coset. The random-order independent-set argument guarantees a separated subset of size at least \(N^2/C(D)\). At \(N\asymp H\), even the desired bound \(C(D)\ll H^2/(\log H)^{10}\) guarantees only a subset of order \((\log H)^{10}\) by this argument. Keeping all \(5\)-exponents would then retain only a vanishing fraction of the base-\(9\) axis. A thinning proof needs a stronger structural estimate to retain a constant fraction of the witnesses. I did not obtain one. [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### New exact inline replay

The replay checks two actual exponent intervals, with \(e\) corresponding to the label \(3^{2e}+5\). For \(s=437\), the square-modulus period is \(43263\). For \(s=77\), the period is \(105\), and the interval \(1\le e\le420\) repeats each eligible residue four times. The latter gives \(C(0)=896=4\cdot224\) exactly.

```python
from math import gcd

def replay(s, N, distances):
    M = s*s
    logs, x = {}, 1
    while x not in logs:
        logs[x] = len(logs)
        x = x*9 % M
    R = len(logs)

    values = [(1-pow(9, e, M)) % M for e in range(1, N+1)]
    units = [z for z in values if gcd(z, s) == 1]
    pair_logs = []
    for z in units:
        for w in units:
            k = logs.get(z*pow(w, -1, M) % M)
            if k is not None:
                pair_logs.append(min(k, R-k))
    return R, len(units), [
        sum(k <= D for k in pair_logs) for D in distances
    ]

assert replay(437, 150, [0, 10, 20, 40, 80]) == (
    43263, 122, [122, 132, 132, 138, 146]
)
assert replay(77, 420, [0, 1, 2, 4, 8]) == (
    105, 224, [896, 896, 896, 896, 896]
)
```