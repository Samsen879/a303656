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