# Unmarked norm-pair matching in every class modulo 480480

For each class \(b\bmod480480\), a positive proportion of the integers \(n\in[X,2X]\) in that class have two true **composite** square-sum residuals at \((c,d),(c+24,d)\), with the same ordinary exponent and residual windows as in [the original matched result](POSITIVE_PROPORTION_TWO_AXIS_NORM_PAIRS.md). More precisely there are \(\gg_\epsilon X\) such \(n\) in each fixed class that admit \(\gg_\epsilon(\log X)^{2-2\log2-\epsilon}\) paired rows disjoint on both axes. For each class the row gcd can be fixed at \(2^e\), \(0\le e\le3\), and is one for every odd class. Constants can be made uniform over these finitely many classes. This is not a density-one or pointwise result.

## Local phases

Fix \(d\bmod2\) so that \(b\not\equiv5^d\bmod3\). The finite test below shows that one can choose \(c,d\bmod8\) obeying that parity and
\[
 b-3^c-5^d\equiv 2^e\bmod 2^{e+2},\qquad b\not\equiv 3^c\bmod5.
\]
Here \(v_2(3^{24}-1)=5\), so the other residual has the same valuation and odd part modulo four. In the three lifts of \(c\bmod8\) to \(c\bmod24\), each of 7 and 13 forbids at most one choice: \(3^8\) has order three modulo either prime. On lifting \(d\) by steps of 24, the powers of 5 have orders \(5,3,135\) modulo \(41,73,6481\), respectively. Their union of forbidden classes has proportion at most \(1/5+1/3+1/135<1\). We use, for example, progressions \(c\bmod120,d\bmod3240\). The final \(c\)-lift by multiples of 24 can avoid both zero residuals at 11: the five choices cycle through an orbit of length five and each endpoint forbids at most one. The odd support of \(3^c(3^{24}-1)\) is exactly \(\{3,5,7,13,41,73,6481\}\); all these primes have now been avoided at both endpoints. When the required progression specifies only \(n\bmod480480\), pick one refinement (for example, the same representative \(b\) modulo \(41\cdot73\cdot6481\)) before selecting the phases.

~~~python
from math import gcd
for b in range(32):
    for b5 in range(5):
        for parity in (0,1):
            assert any((b-3**c-5**d) % (1<<(e+2)) == 1<<e
                       and b5 != pow(3,c,5)
                       for e in range(4) for c in range(8)
                       for d in range(parity,8,2))
for p,o in ((7,3),(13,3)):
    assert pow(3,8*o,p)==1 and pow(3,8,p)!=1
for p,o in ((41,5),(73,3),(6481,135)):
    assert next(j for j in range(1,p) if pow(5,24*j,p)==1)==o
~~~

## Uniform row mass, without marker primes

Normalize the two residuals by \(2^e\). Denote their coordinate vectors by \(P_+,P_-\), and write \(A=P_+-P_-, W=P_++P_-\). The desired linear equation is \(A\cdot W=3^c(3^{24}-1)/2^e\). At odd primes dividing the fixed modulus, each norm target is representable: if their reductions differ, their vectors are distinct, and at a common nonzero norm we can choose opposite vectors. At 2 both normalized norms are \(1\bmod4\). Any such target can be represented modulo the needed power of 2 with a prescribed odd axis: choose the even coordinate 0 or 2 using the norm modulo 8, then lift the odd square. Choose opposite odd axes for the two vectors. This makes \(A\) primitive at the fixed modulus and ensures \(W\equiv A\bmod2\) coordinatewise.

Now use the [primitive-vector CRT line argument](FIXED_SHIFT_TRUE_NORM_PAIRS.md): take primitive \(A\) in a sufficiently small fixed box of side \(\asymp\sqrt X\); for each, choose \(W\) in its prescribed CRT class on the exact line, by Bézout. The parallel displacement is negligible since the shift is \(O(X^{1/4})\). The perpendicular step is a fixed multiple of \(\|A\|\), small enough to fit in a fixed interval of length \(\asymp\sqrt X\). Choose that interval so both \(2^e\|(W\pm A)/2\|^2\) lie in the original residual window. The CRT parity gives integer vectors, multiplication by \(2^e\) preserves their being two-square norms (multiply the Gaussian coordinates by \((1+i)^e\)), and their gcd is exactly \(2^e\). Thus each row has \(\gg X\) ordered representation pairs.

For odd classes the pairs with a prime residual can be removed at \(O(X/\log X)\) mass per row. A prime in the residual size window has \(r_2\le8\) and no prime divisor below \(X^{1/10}\), so use the latter roughness indicator for that endpoint in the [corrected Henriot majorant](DEDUPLICATED_TRUE_NORM_SHIFT_COUNT.md), retaining \(r_2/4\) for the other endpoint. Its growth constants are uniform. At good primes up to the cutoff the combined local factor is \(1+(\chi_4(p)-1)/p+O(p^{-2})\); above it the factor is \(1+\chi_4(p)/p+O(p^{-2})\). The extra Mertens factor gives the stated saving. For even classes the residuals are already composite in the height window. No prime marker is needed.

## Deduplication and matching

Use the nonnegative \(r_2\) product with these additional masks. The two-form upper moments and first-moment mass are as before. Distinct rows give four distinct shifts by their exponent boxes and the disjoint \(c,c+24\) phases. The different-\(d\) mean discriminant bound uses exactly the previous order proof, with base \(5^{3240}\) in place of \(5^{120}\); the equal-\(d\) pairs again number \(O((\log X)^3)\). Thus the first/second moment, the per-row truncation, and the squared weighted degree bounds from the original matched result all apply. This proves the count of distinct targets and the matching size. The estimates do not give an asymptotic variance or growth-modulus claim.
