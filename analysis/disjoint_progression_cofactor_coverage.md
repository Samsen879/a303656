# Positive-fraction coverage from disjoint exponent progressions

The stripped-cofactor selector certifies a **positive fraction of the distinct targets \(n\equiv3\pmod4\)** in every sufficiently large dyadic interval for each fixed \(0<a\le1/2\), with screen \(B(n)=\lfloor\sqrt n/(\log n)^a\rfloor\). More generally, the construction below certifies
\[
\gg_a X\min\{1,(\log X)^{1-2a}\}
\]
distinct targets in that class on \([X,2X]\). Different \(5\)-exponents give disjoint target progressions. Within each progression, a second moment charges collisions between the \(3\)-power labels. This establishes coverage of a positive fraction for the stated range. Universal coverage remains open. The related incidence upper bound is in [draft #65](https://github.com/Samsen879/a303656/pull/65).

### Separate the \(5\)-exponents before counting overlaps

Put \(L=(\log X)^a\), choose a power \(s=3^j\) with \(2L\le s<6L\), and set \(Y=X/s^2\). Use actual targets and labels of the form
\[
n=5^d+s^2M,\qquad (c,d)=(2j+2e,d),\qquad
m=s^2(M-9^e).
\]
Take \(M\in[5Y/4,3Y/2]\), \(9^e\le Y/8\), and \(5^d\le X/8\). These choices keep \(n\in[X,2X]\) and \(m\ge9X/8\).

Require \(u=M-9^e\) to have all its prime factors \(1\bmod4\). Such \(u\) are odd primitive two-square norms. For large \(X\), the screen strips exactly \(s^2\) from \(m\), and
\[
u\le \frac{3X}{2s^2}\le \frac{3X}{8L^2}
  <q_1q_2.
\]
Here \(q_1,q_2\) are the first two inert primes above \(B(n)\), so their product exceeds \(n/(\log n)^{2a}\). Also \(M\equiv2\pmod4\) and \(n\equiv3\pmod4\).

By lifting the exponent, \(\operatorname{ord}_{3^{2j}}(5)=2\cdot3^{2j-1}\). Use the first
\[
D=\min\!\left\{2\cdot3^{2j-1},\,1+\lfloor\log_5(X/8)\rfloor\right\}
\]
values of \(d\). Their residues \(5^d\bmod s^2\) are distinct, so **no target is counted in two different \(d\)-progressions**. It remains to prove that \(\gg Y\) distinct \(M\) work within each progression.

### Charge collisions between the remaining labels

Let \(F(M)\) count the exponents \(e\) for which \(M-9^e\) has all prime factors \(1\bmod4\). There are \(K\asymp\log Y\) available exponents. For every \(e\), the allowable interval of cofactors contains \([5Y/4,11Y/8]\). Wirsing’s theorem for the indicator of integers supported on split primes gives \(\asymp Y/\sqrt{\log Y}\) such cofactors in that common interval. Thus
\[
\sum_M F(M)\gg K Y/\sqrt{\log Y}.
\]
The same theorem bounds each diagonal contribution by \(O(Y/\sqrt{\log Y})\). [Wirsing’s original theorem](https://doi.org/10.1007/BF01351892)

For \(e\ne f\), apply a standard upper-bound sieve to the two translates. At each inert prime there are two forbidden classes except when that prime divides \(9^e-9^f\), in which case there is one. The prime \(3\) contributes a bounded factor and can be omitted for this upper bound. The collision count for the pair is
\[
\ll \frac{Y}{\log Y}
 \prod_{\substack{p\mid 9^{|e-f|}-1\\p\ge7,\ p\equiv3\ (4)}}(1+2/p).
\]
Indeed, the base product over inert primes has size \(O(1/\log Y)\) by Mertens’ theorem in the progression. At a colliding prime the correction is \((p-1)/(p-2)\le1+2/p\). The sieve bound is uniform in the forbidden residues. [Tao and Teräväinen, Lemma 3.2](https://doi.org/10.1112/jlms.12663) · [Davenport, *Multiplicative Number Theory*](https://link.springer.com/book/9780387950976)

The product has bounded mean as the exponent difference varies. To see this, expand it over squarefree \(r\), with weight \(2^{\omega(r)}/r\). The condition \(r\mid9^k-1\) holds at most \(K/\operatorname{ord}_r(9)\) times for \(1\le k\le K\). The resulting series of weights divided by the order converges. For orders at most \(T\), all eligible \(r\) divide \(\prod_{k\le T}(9^k-1)\), whose logarithm is \(O(T^2)\). Their total weight is bounded by the Euler product over primes dividing that integer. The primes below \(T^2\) contribute \(O((\log(2T))^2)\) by Mertens’ theorem. The primes above \(T^2\) contribute a bounded factor, since there are \(O(T^2/\log T)\) of them. Dyadically summing this weight bound with the reciprocal order proves convergence.

Each exponent difference occurs at most \(2K\) times. Consequently,
\[
\sum_M F(M)^2
 \ll \frac{KY}{\sqrt{\log Y}}+\frac{K^2Y}{\log Y}
 \ll Y\log Y.
\]
Cauchy–Schwarz now gives \(\gg Y\) **distinct** \(M\) with \(F(M)>0\). Summing over the disjoint progressions gives \(\gg DY\), the claimed target bound. For \(a>1/2\), this particular construction has a precise limitation. Its selected \(5\)-exponents occupy only \(O((\log X)^{1-2a})\) of the classes modulo \(s^2\), even if every eligible \(M\) works. The mixed-factor refinement below proves positive-fraction coverage through \(a=3/4\).

### Sharp same-target control

At \(a=1/2\) and \(n=5{,}117{,}651\), the screen is \(575\), and the first two unscreened inert primes are \(587,599\). Their product is \(351{,}613\). Both labels below strip exactly \(9\), and both cofactors are \(1\bmod4\).

| Label \((c,d)\) | Positive residual | Stripped cofactor | Result |
|---|---:|---:|---|
| \((4,9)\) | \(3{,}164{,}445=642^2+1659^2\) | \(351{,}605\) | Accepted |
| \((2,9)\) | \(3{,}164{,}517=9\cdot587\cdot599\) | \(351{,}613\) | Rejected at equality, with two odd inert valuations |

~~~python
from decimal import Decimal, localcontext
from math import isqrt

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def norm(m):
    return any(a*a+isqrt(m-a*a)**2==m for a in range(isqrt(m//2)+1))

n=5117651
with localcontext() as ctx:
    ctx.prec=60
    v=Decimal(n)/Decimal(n).ln()
    assert 575**2<v<576**2
B=575
p=[p for p in range(3,600,4) if prime(p)]
out=[j for j in p if j>B]
assert out==[587,599]
def strip(u):
    for q in p:
        if q>B: break
        e=0
        while not u%q:
            u//=q; e+=1
        assert e%2==0
    return u
m=[n-3**c-5**9 for c in (4,2)]
assert m==[3164445,3164517]
assert [strip(v) for v in m]==[351605,351613]
assert [norm(v) for v in m]==[True,False]
~~~

## Mixed factors extend the distinct-target result to a = 3/4

The mixed-factor construction extends positive-fraction coverage from \(a\le1/2\) to **every fixed \(0<a\le3/4\)**. In every sufficiently large interval \([X,2X]\), a positive fraction of the distinct targets \(n\equiv3\pmod4\) pass the stripped-cofactor selector with \(B(n)=\lfloor\sqrt n/(\log n)^a\rfloor\). The construction uses both actual exponent axes. A two-factor version has exactly zero cross-factor intersections, even though the square factors share primes.

### Separate the target progressions

Write \(s=3^j7^k\), \(A=3^{2j}\), \(C=7^{2k}\), and \(Y=X/(AC)\). For \(1/2<a\le3/4\), choose
\[
A\asymp\log X,\quad A\le(\log X)/10,\qquad
AC\asymp_a(\log X)^{2a},\quad AC\ge4(\log X)^{2a}.
\]
Rounding to the indicated prime powers costs only constant factors. The existing pure-\(3\) construction supplies \(a\le1/2\).

Use one full period of \(d\) modulo \(A\), of length \(2A/3\). The residues \(5^d\bmod A\) are distinct and \(5^d\le X/8\) for large \(X\). The order of \(3\bmod C\) is \(r=6\cdot7^{2k-1}\). Choose even \(c_0\) in \([2j,2j+r)\), and use actual exponents \(c=c_0+re\) with \(3^c\le X/8\). The values \(3^{c_0}\bmod C\) run through \(r/2\) distinct residues.

For each \((d,c_0)\), use
\[
n=5^d+3^{c_0}+ACM,\qquad
m=n-5^d-3^{c}=AC(M-h_e),\qquad
h_e=\frac{3^{c_0+re}-3^{c_0}}{AC}.
\]
The numerator is divisible by \(A\) and \(C\), and \(h_e\equiv0\pmod4\). The target class modulo \(A\) determines \(d\), then the class modulo \(C\) determines \(c_0\). Thus distinct cells are disjoint. For a family with two square factors, use \(C\) and \(49C\), assigning even \(d\) to one and odd \(d\) to the other. The common modulus \(A\) still separates every cross-factor pair. Each factor retains a constant fraction of the cells.

Take \(5Y/4\le M\le3Y/2\) and require \(u=M-h_e\) to have all its prime factors \(1\bmod4\). Then \(u\) is an odd primitive two-square norm, \(n\in[X,2X]\), and \(m\ge9X/8\). The screen strips exactly \(AC=s^2\). Since \(u\le3X/(8(\log X)^{2a})\), it lies below the product of the first two unscreened inert primes for large \(X\). Also \(M\equiv1\bmod4\), so the targets are \(3\bmod4\). [Repository theorem assets, AUX-01](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

### Bound overlaps within each progression

Each cell has \(K\asymp\log X/r\asymp_a(\log X)^{2-2a}\) exponents. The first moment for the number \(F(M)\) of successful exponents is \(\gg KY/\sqrt{\log Y}\), using Wirsing’s theorem for integers supported on split primes. The diagonal contribution to \(\sum_M F(M)^2\) is \(O(KY/\sqrt{\log Y})\). For two different exponents, the upper-bound sieve gives \(O(Y/\log Y)\) times the correction
\[
\prod_{\substack{p\mid 3^{r|e-f|}-1\\p\equiv3\ (4),\ p\nmid21}}(1+2/p).
\]
The primes \(3,7\) cost only a bounded factor. For every other inert prime, the two forbidden classes coincide only if it divides \(3^{r|e-f|}-1\). [Wirsing’s mean-value theorem](https://doi.org/10.1007/BF01351892) · [Tao and Teräväinen, sieve upper bound, Lemma 3.2](https://doi.org/10.1112/jlms.12663)

The necessary new estimate is that this correction has **bounded mean uniformly in \(k\)**. Expand the product over squarefree \(b\) with weights \(2^{\omega(b)}/b\). A term occurs for exponent differences divisible by \(\operatorname{ord}_b(3^r)\). To bound the resulting reciprocal-order sum, consider primes \(p\nmid21\) with \(\operatorname{ord}_p(3^r)\le T\), and write \(\operatorname{ord}_p(3)=7^v w\), \(7\nmid w\). Since \(r=6\cdot7^{2k-1}\), one has \(w\le6T\).

- For \(v\le J=\lfloor\log_7 T\rfloor\), all such primes divide \(\prod_{w\le6T}(3^{7^Jw}-1)\), whose logarithm is \(O(T^3)\). Splitting its prime divisors at \(T^3\) and using Mertens’ bound gives an Euler product \(O((\log(2T))^2)\).
- For \(v>J\), the primes satisfy \(p\equiv1\bmod7^v\) and divide \(\prod_{w\le6T}(3^{7^v w}-1)\). Below \((7^vT)^2\), the harmonic sum over that progression is \(O((1+v+\log T)/7^v)\). Above it, the logarithm of the product bounds the number of prime divisors and gives \(O(7^{-v})\) for their reciprocal sum. Summing over \(v>J\) costs \(O(1)\).

The same Euler-product bound therefore controls the total weight of squarefree \(b\) with order at most \(T\). Dyadic summation after division by the order converges uniformly. This gives the stated bounded mean and hence
\[
\sum_M F(M)^2\ll KY/\sqrt{\log Y}+K^2Y/\log Y.
\]
At \(a\le3/4\), \(K\gg\sqrt{\log Y}\). Cauchy–Schwarz yields \(\gg Y\) distinct successful targets per cell. There are \(\asymp AC\) disjoint cells, giving \(\gg_a X\) distinct targets overall.

For \(a>3/4\), the first moment already bounds this specific construction by \(O_a(X(1+(\log X)^{2-2a})/\sqrt{\log X})=o(X)\). That bound applies to the two-factor version too. It leaves open constructions using more factors or different allocations of the exponent periods.

### Independent exact check

The replay verifies the sharp mixed-factor input at the same actual target, and separated classes for two factors sharing a prime.

~~~python
from decimal import Decimal, localcontext
from math import isqrt

n = 23459
with localcontext() as ctx:
    ctx.prec=60
    q=Decimal(n)
    assert 27<q.sqrt()/q.ln()**Decimal('0.75')<28
B = 27
primes = [p for p in range(3, 60, 4)
          if all(p % t for t in range(2, isqrt(p) + 1))]
assert [p for p in primes if p > B][:2] == [31, 43]
assert n - 3**4 - 5 == 21**2 * 53 == 42**2 + 147**2
assert 53 < 31 * 43

even_d = {pow(5, d, 9) for d in (0, 2, 4)}
odd_d = {pow(5, d, 9) for d in (1, 3, 5)}
assert len(even_d) == len(odd_d) == 3
assert even_d.isdisjoint(odd_d)

for k in (1, 2):
    C = 7**(2*k)
    r = 6 * 7**(2*k - 1)
    assert pow(3, r, C) == 1
    assert len({pow(3, c, C) for c in range(2, 2+r, 2)}) == r//2
~~~
