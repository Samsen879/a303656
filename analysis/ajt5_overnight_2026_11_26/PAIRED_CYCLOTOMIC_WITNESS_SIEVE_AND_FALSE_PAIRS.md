# Paired cyclotomic witnesses: small-range summability and truncated-order false positives

**The paired sieve gives reciprocal summability in a larger proved range, and the minimum possible witness gap \(6\ell\) is attained.** In the exponential range, a sieve that checks primality, the same-half congruences, the product bound, and every cofactor-primary order test up to \(\lfloor\ell/20\rfloor\) still admits false pairs for every sufficiently large prime \(\ell\).

### Exact same-half constraints

For an odd prime \(\ell>5\), write
\[
25^\ell-9^\ell=16H_-H_+,\qquad
H_-=\frac{5^\ell-3^\ell}{2},\qquad H_+=\frac{5^\ell+3^\ell}{8}.
\]
The halves are odd, coprime, and both \(1\bmod3\). Consequently, if an inert prime occurs to odd valuation in one half, another distinct inert prime occurs to odd valuation in that same half.

Set \(g_-=5/3\) and \(g_+=-5/3\) modulo a candidate prime \(q\). For \(q\mid H_\pm\), \(g_\pm\) has exact order \(\ell\). Indeed, its \(\ell\)th power is \(1\), and \(g_\pm\ne1\). In particular \(q=2u\ell+1\). For inert \(q\equiv2\bmod3\), the square condition on \(g_\pm\) gives
\[
\begin{array}{c|c}
\text{half}&q\bmod60\\ \hline
H_-&11,17,53,59\\
H_+&17,23,47,53
\end{array}
\]
by \((3/q)=-(-1/q)\) and quadratic reciprocity for \(5\). All inert witnesses have the same \(u\bmod3\), since \(2u\ell+1\equiv2\bmod3\). Thus distinct witnesses are at least \(6\ell\) apart. At \(\ell=269\), the two primes \(2153\) and \(3767\) attain equality in \(H_+\), each with valuation exactly one.

### The paired counting bound

For \(\ell\in(X,2X]\), the number of prime \(\ell\) with a witness pair \(q_1=2u\ell+1,\ q_2=2v\ell+1\), \(u\ne v\), is
\[
\ll \frac{XUV}{(\log X)^3}
\quad\text{if }u\le U,\ v\le V,
\qquad
\ll \frac{XUW}{(\log X)^3}
\quad\text{if }u\le U,\ 0<v-u\le W\le U.
\]
The constants are absolute. These are upper bounds for actual pairs because the count can relax both order and valuation.

For fixed \(u,v\), sieve the three forms \(n,2un+1,2vn+1\). At primes \(p>3\), they have three distinct roots except when \(p\mid uv(u-v)\). At \(p=3\), a full set of roots makes the triple impossible in this interval. Put \(F(a)=\prod_{p>3,\,p\mid a}p/(p-3)\). The Selberg upper sieve at \(z=X^{1/12}\) gives
\[
\ll \frac{X}{(\log X)^3}F(u)F(v)F(|u-v|).
\]
For uniformity in the coefficients, the squarefree modulus error is at most its number of root classes. The sieve weights have absolute value at most one, so the total error is \(O(z^4)\). To bound the denominator below, retain only moduli coprime to \(6uv(u-v)\). Removing the exceptional primes from the generic denominator costs at most \(F(u)F(v)F(|u-v|)\). The generic denominator is \(\gg(\log z)^3\), as follows by comparing it with \(\sum_{d<z,\,(d,6)=1}\mu^2(d)3^{\omega(d)}/d\). The Dirichlet series for the coefficients factors as \(\zeta(s)^3\) times a series absolutely convergent at \(1\) with positive value there. [Selberg’s sieve paper](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1950.1/ICM1950.1.ocr.pdf)

Expanding \(F(a)^3\) over squarefree divisors gives \(\sum_{a\le T}F(a)^3\ll T\), since the resulting mean-value Euler product has factors \(1+O(p^{-2})\). Hölder now gives the rectangle bound. For the band, use variables \(u,w=v-u\) and \(\sum_{u\le U}F(u+w)^3\ll U+W\).

In particular, for every fixed \(\eta>0\), the reciprocal sum over prime \(\ell\) having a same-half pair is finite in either of these ranges:

- Both witnesses are \(\le \ell\log\ell/(\log\log\ell)^{1/2+\eta}\).
- The gap is \(\le C\ell\) for fixed \(C\), and the smaller witness is \(\le \ell(\log\ell)^2/(\log\log\ell)^{1+\eta}\).

These follow by dyadic summation. The first improves the single-witness scale when both witnesses are available. The second allows a larger witness scale when the pair is close.

### A large-range failure of truncated order tests

The exact test for \(q=2u\ell+1\) is \(g_\pm^\ell=1\bmod q\). Equivalently, for every prime \(r\mid 2u\), test
\[
g_\pm^{(q-1)/r^{v_r(2u)}}=1\bmod q.
\]
The gcd of those exponents is \(\ell\). Even taking **all** such tests for \(r\le t=\lfloor\ell/20\rfloor\) leaves false pairs in each half for every sufficiently large prime \(\ell\).

For the plus half choose \(q\equiv23\bmod60\), and for the minus half choose \(q\equiv59\bmod60\). In either case impose \(q\equiv1\bmod\ell\), \(q\equiv2\bmod r\) for every prime \(7\le r\le t\), and
\[
q\equiv-1-4j\pmod{2^t},\qquad 0\le j<64.
\]
These are compatible reduced classes. The only prime \(r\le t\) dividing \(2u\) is \(2\), with valuation one, and the selected class modulo \(60\) ensures that \(g_\pm\) is a square.

The modulus is at most \(15\ell\,2^{3t}\), using \(\prod_{r\le t}r\le4^t\). Linnik’s theorem with exponent \(6\) gives 64 distinct prime candidates, each between \(2^{t-1}\) and \(O(\ell^6 2^{18t})\). Any two have product \(O(\ell^{12}2^{36t})<H_\pm\) for large \(\ell\). Yet fewer than 50 primes this large can divide \(H_\pm\), since \(2^{50(t-1)}>5^\ell>H_\pm\) eventually. Thus each half has at least two candidates that pass the entire truncated test and **do not divide the half**. This proves the failure of that relaxation uniformly in the large range. The distribution of actual large-witness pairs, and hence the density of admissible multipliers, remains open in this argument. [Xylouris’s published Linnik bound](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/150/1/83078/on-the-least-prime-in-an-arithmetic-progression-and-estimates-for-the-zeros-of-dirichlet-l-functions)

The following replay checks the sharp genuine pair and a false pair at the same \(\ell\).

```python
from math import gcd, isqrt

ell = 269
def prime(q):
    return q > 1 and all(q % d for d in range(2, isqrt(q) + 1))
def diff(m):
    return (pow(25, ell, m) - pow(9, ell, m)) % m

assert prime(ell) and 3767 - 2153 == 6 * ell
for q, a, b in [(2153, 1448, 227), (3767, 265, 687)]:
    assert prime(q) and q % 3 == 2 and (q-1) % (2*ell) == 0
    assert (pow(5, ell, q*q) + pow(3, ell, q*q)) % (q*q) == a*q
    assert diff(q*q) == b*q

for q, rem in [(10223, 9309), (123203, 62986)]:
    assert prime(q) and q % 60 == 23 and (q-1) % (2*ell) == 0
    assert gcd((q-1)//(2*ell), 30030) == 1  # all primes up to 13
    assert pow(-5*pow(3, -1, q), (q-1)//2, q) == 1
    assert diff(q) == rem
assert 10223 * 123203 < (5**ell + 3**ell)//8
```

Independent BigInt checked both valuation-one witnesses at the minimum gap, the two false candidates at the same prime exponent, and their product bound. This proves a limitation of the specified relaxed filter, not a limitation of all possible order-aware sieves or a density result for the full large range.
