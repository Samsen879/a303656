# Progression depth required for actual-label square-factor coverage

**A disjoint full-progression construction cannot pass \(a=3/4\), even with arbitrary growing odd prime support.** The obstruction is reuse of the same actual \(3/5\) label. More generally, at \(a=1\), a construction using stripped odd factors \(s\asymp\log X\) needs progression overlap depth \(\gg\sqrt{\log X}\) to certify a positive fraction of \([X,2X]\). This strengthens the balanced-star bound and applies to unbalanced families anchored at powers of \(3\) or \(7\). It concerns progression overlap. Genuine norm witnesses have a different overlap structure.

### A bound from reuse of actual labels

Put \(H=\log X\), \(L=H^a\), and take odd stripped factors \(c_0L\le s\le C_0L\), with fixed \(c_0,C_0>0\). An assigned cell for the actual numerical label \(\lambda=3^c+5^d\) is
\[
n\equiv\lambda\pmod{s^2}.
\]
The construction may also specify the exact \(v=v_2(n-\lambda)\) by adding \(n-\lambda\equiv2^v\bmod 2^{v+1}\). Let \(\Delta\) be the maximum number of assigned progression cells containing any target in \([X,2X]\).

For any fixed \((\lambda,v)\), the intersection of cells from distinct factors \(s_1,\dots,s_k\) is always compatible. Its modulus is
\[
2^{v+1}\operatorname{lcm}(s_1,\ldots,s_k)^2.
\]
For \(2^v\le\sqrt X\) and \(k\le K=\lfloor H/(10\log(2C_0L))\rfloor\), that modulus is less than \(X\), so the intersection meets the target interval. Thus if \(\Delta<K\), each \((\lambda,v)\) can be assigned to at most \(\Delta\) factors. This uses the actual common offset and works regardless of how the factors share primes.

For each assignment, a certified residual has the form \(m=2^v s^2u\) with \(u\) an odd two-square norm. Landau’s bound gives \(O(X/(2^vL^2\sqrt H))\) possible cofactors for \(2^v\le\sqrt X\). Summing over \(v\) is geometric. The larger valuations cost \(O(\sqrt X)\) targets per label, since they require divisibility by a power of \(2\) exceeding \(\sqrt X\). There are \(O(H^2)\) actual exponent pairs, so when \(\Delta<K\) the number of distinct certified targets is at most
\[
O\!\left(\Delta XH^{3/2-2a}+\sqrt X\,H^2\right).
\]
The count includes even residuals with a nontrivial \(2\)-power in their square part. For disjoint cells, \(\Delta=1\). For positive-fraction coverage, it follows that \(\Delta\gg\min\{H/\log H,H^{2a-3/2}\}\), which at \(a=1\) gives the stated \(\sqrt H\) requirement. No assumption on lifted orders enters this bound. [Repository theorem assets, K2-N1](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

### Where overlapping constructions can recover the lost count

For a fixed offset \(\lambda\), the depth from a family of factors has an exact combinatorial expression. If \(D_\lambda(n)=\sum_s 1_{s^2\mid n-\lambda}\), then
\[
\sum_{X\le n\le2X}\binom{D_\lambda(n)}k
=\sum_{\substack{T\text{ a subset of factors}\\|T|=k}}
\#\{n\in[X,2X]: n\equiv\lambda\bmod \operatorname{lcm}(T)^2\}.
\]
Each term on the right is an exact count in one progression. A fixed exact \(2\)-valuation adds the compatible \(2\)-power modulus above.

For **genuine witnesses at one label**, this potentially deep CRT overlap disappears. Once \(n\) and \(\lambda\) are fixed, the positive residual determines its stripped odd factor uniquely by the full screened valuations. Thus reusing one actual label across many factors is necessary for beating the disjoint-cell ceiling and costs no same-label overlap in the norm count. The remaining problem is to control **different-label** norm intersections. I did not obtain a growing anchored family with that control, so the bound does not exclude positive-fraction coverage by overlapping constructions.

### Same-target replay

At \(n=309143\) and \(a=1\), the screen is \(43\), and the next two inert primes are \(47,59\). Two actual labels give different genuine factors:
\[
\begin{aligned}
309143-(3^0+5^0)&=21^2\cdot701=105^2+546^2,\\
309143-(3^2+5^5)&=33^2\cdot281=165^2+528^2.
\end{aligned}
\]
Both odd cofactors pass the cutoff \(47\cdot59\). The full cells intersect in \(42338\bmod53361\). At the same target and the first label, \(7^2\) also divides the residual, but assigning the stripped factor \(7\) would leave \(9\cdot701\). The screen must also strip \(3^2\), so that assignment supplies no second witness at that label.

The integer replay distinguishes assigned progression depth from genuine norm witness multiplicity.

```python
from math import gcd, isqrt, lcm, log

n = 309143
a, b = 3**0 + 5**0, 3**2 + 5**5
assert (a, b) == (2, 3134)
assert n-a == 21**2 * 701 == 105**2 + 546**2
assert n-b == 33**2 * 281 == 165**2 + 528**2
assert gcd(105, 546) == 21 and gcd(165, 528) == 33

B = int(n**0.5 / log(n))
inert = [p for p in range(3, 100, 4)
         if all(p % d for d in range(2, isqrt(p) + 1))]
assert B == 43 and [p for p in inert if p > B][:2] == [47, 59]
assert all(u % p for u in (701, 281) for p in inert if p <= B)
assert max(701, 281) < 47*59
assert (n-a) // 7**2 == 9*701

M = lcm(21**2, 33**2)
assert M == 53361 and n % M == 42338
assert [x for x in range(M)
        if (x-a) % 21**2 == 0 and (x-b) % 33**2 == 0] == [42338]
```
## Different-label overlaps: exact square support and the weighted criterion

Exact square support gives a stronger different-label overlap bound than CRT divisibility alone. **If two proposed stripped factors have different exponents at an inert prime \(p\), the label difference must have valuation exactly twice the smaller exponent.** This removes entire compatible CRT progressions before the norm sieve. The resulting weighted sum gives a necessary lower bound for any high-witness family and a sufficient upper bound for positive-fraction coverage. I did not obtain a growing family with the required upper bound.

### Different-label overlap with exact support

Put \(H=\log X\), \(L=H^a\), and work with odd targets. A witness \((\lambda,s)\) uses an actual label \(\lambda=3^c+5^d\) and a residual \(n-\lambda=s^2u>0\), where \(s\) is inert-supported and every prime factor of \(u\) is \(1\bmod4\). Thus \(s\) is determined uniquely by \(n-\lambda\). In particular, different factors assigned to the **same** label contribute zero off-diagonal norm overlaps.

For different labels \(\lambda,\mu\), put \(h=\mu-\lambda\). At each inert prime write \(\alpha=v_p(s)\), \(\beta=v_p(t)\). The necessary conditions are
\[
\begin{cases}
v_p(h)=2\min(\alpha,\beta),&\alpha\ne\beta,\\
v_p(h)\ge2\alpha,&\alpha=\beta.
\end{cases}
\]
They follow from \(h=s^2u-t^2v\) and the fact that \(u,v\) are units at inert primes. For instance, if \(p\) belongs to exactly one factor, the overlap vanishes whenever \(p\mid h\), even if both square-divisibility conditions hold.

For a pair that passes these conditions, write \(n=n_0+\operatorname{lcm}(s,t)^2w\). The two cofactors are affine forms in \(w\). The number \(\nu_p\) of forbidden classes modulo an inert prime \(p\) is exactly
\[
\nu_p=
\begin{cases}
1,&\alpha\ne\beta,\\
1,&\alpha=\beta\ \text{and }v_p(h)>2\alpha,\\
2,&\alpha=\beta\ \text{and }v_p(h)=2\alpha.
\end{cases}
\]
When the exponents differ, one form has unit slope and the other is a fixed nonzero residue. When they agree, both slopes are units, and their forbidden roots coincide precisely under the stricter valuation inequality.

For polylogarithmic \(s,t\), the upper-bound sieve therefore bounds the genuine overlap by
\[
\ll \frac{X}{H}\,
\frac{\gcd(s,t)^2}{s^2t^2}\,
\mathfrak S_{\rm ex}(s,t;h),
\qquad
\mathfrak S_{\rm ex}=
\prod_{\substack{p\equiv3\ (4)\\\nu_p=1}}\frac{p-1}{p-2}.
\]
Set the weight to zero when any exact-support condition fails. The product is finite for \(h\ne0\). The sieve is applied on the CRT progression, whose length is \(X\) divided by a polylogarithmic modulus. Thus the \(1/H\) factor is uniform in the labels and factors in this range. [Tao and Teräväinen, sieve upper bound, Lemma 3.2](https://doi.org/10.1112/jlms.12663)

### The weighted condition

For specificity, take assigned pairs \((\lambda,s)\) with distinct numerical labels \(\lambda\equiv2\bmod4\), \(\lambda\le X/8\), and \(2L\le s\le3L\). A label may be assigned to many factors. Write
\[
V=\sum_{(\lambda,s)}s^{-2},
\qquad
W=\sum_{\substack{(\lambda,s),(\mu,t)\\\lambda\ne\mu}}
\frac{\gcd(s,t)^2}{s^2t^2}\,\mathfrak S_{\rm ex}(s,t;\mu-\lambda),
\]
using the zero convention above. Restrict each witness to \(X\le s^2u\le3X/2\). Wirsing’s theorem gives a first moment \(\asymp XV/\sqrt H\) for the actual witnesses. Their cofactors are below the next-two-inert cutoff for large \(X\). Exact factor uniqueness gives
\[
\sum_n F(n)^2\ll XV/\sqrt H+XW/H,
\]
where \(F(n)\) counts witnesses. [Wirsing’s mean-value theorem](https://doi.org/10.1007/BF01351892) · [Repository theorem assets, AUX-01](https://github.com/Samsen879/a303656/blob/main/analysis/direct_original_problem_phase_i_k2/THEOREM_ASSETS.md)

This gives two distinct uses of \(W\).

- **Necessary for a large witness count:** Cauchy–Schwarz on \([X,2X]\) forces \(W\ge cV^2-C\sqrt H\,V\) for absolute positive constants in this layer. In particular, if \(V/\sqrt H\to\infty\), the compatible different-label pairs must supply \(W\gg V^2\).
- **Sufficient for distinct-target coverage:** If \(V\gg\sqrt H\) and \(W\ll V^2\), the same moment estimates give \(\gg X\) distinct targets. An upper bound on \(W\) at this scale remains unproved for a growing family past \(a=3/4\).

This weight charges exact local support across *different* residuals. Full progression depth can be large because one label is reused across factors, even though such reuse adds nothing to \(W\).

### Exact same-target replay

At \(n=4814483\), the actual labels \((4,1)\) and \((2,1)\) give
\[
\begin{aligned}
n-(3^4+5)&=63^2\cdot1213=1386^2+1701^2,\\
n-(3^2+5)&=33^2\cdot4421=462^2+2145^2.
\end{aligned}
\]
At the shared prime \(3\), the factor exponents are \(2\) and \(1\), and \(v_3(86-14)=2\), exactly as required. At \(a=1\), the screen is \(142\) and both cofactors pass the cutoff \(151\cdot163\).

For the control, assign factor \(7\) to the first label while keeping factor \(33\) for the second. Both CRT divisibilities still hold at the same target. But \(3\) now belongs to only one proposed factor and divides the label difference. Hence the entire common progression has zero overlap for **those assigned exact factors**. At this target the first proposed cofactor is \(81\cdot1213\), so the screen must strip the additional \(3^4\). The following replay verifies the same-target control.

```python
from math import gcd, isqrt, lcm, log

n = 4814483
a, b = 3**4 + 5, 3**2 + 5
s, t = 63, 33
assert n-a == s*s*1213 == 1386**2 + 1701**2
assert n-b == t*t*4421 == 462**2 + 2145**2
assert gcd(1386, 1701) == s and gcd(462, 2145) == t
assert (a-b) % 9 == 0 and (a-b) % 27 != 0

B = int(n**0.5 / log(n))
inert = [p for p in range(3, 180, 4)
         if all(p % j for j in range(2, isqrt(p) + 1))]
assert B == 142 and [p for p in inert if p > B][:2] == [151, 163]
assert all(u % p for u in (1213, 4421) for p in inert if p <= B)
assert max(1213, 4421) < 151*163

assert (n-a) % 7**2 == (n-b) % t**2 == 0
assert (n-a) // 7**2 == 81*1213
step = lcm(s*s, t*t)
assert (step // (s*s), step // (t*t)) == (121, 441)
```