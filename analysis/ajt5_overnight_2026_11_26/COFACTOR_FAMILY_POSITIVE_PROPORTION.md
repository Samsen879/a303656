# Positive proportion of many non-origin witnesses in the explicit cofactor family

For each sufficiently large multiple \(k\) of 42, consider the targets \(k\le T<2k,\ T\equiv106\bmod196\) and actual integers \(n=5^k+9^kT\). A positive proportion of these \(T\)'s has \(\gg\sqrt{\log k}\) distinct true witnesses among the labels \((c,d)=(2k+2e,k)\), where \(e\equiv1\bmod21,\ k^{1/3}\le9^e\le k/4\). This concerns the specified arithmetic family and not all \(n\). The actual origin fails, as established in [the cofactor construction](MOVING_SQUARE_FACTOR_COMPRESSION.md). The residuals are \(9^k(T-9^e)\), and the cofactor is positive, \(1\bmod4\), and below \(2k\); hence the finite panel in the linked note certifies true norms on these rows.

Write \(r(T)\) for the number of true cofactors on the row and \(H\asymp\log k\) for the number of allowable \(e\)'s.

## First moment

For each \(e\), every norm in \([k,3k/2)\) of residue \(97\bmod196\) supplies a permitted \(T\) by adding \(9^e\). Such norms have count \(\gg k/\sqrt{\log k}\). To see the residue-class lower bound, let \(N(X)\) count all positive two-square norms up to \(X\), using the [classical Landau asymptotic as recorded by Kurlberg and Ueberschär](https://arxiv.org/abs/1311.1396). The count of odd norms coprime to 7 is exactly \(N(X)-N(X/2)-N(X/49)+N(X/98)\), by the inert-prime parity criterion. This has a positive leading constant and gives the same lower order on any fixed positive-ratio interval.

For each possible residue \(s\bmod196\) of such a norm, fix a norm multiplier \(M_s\equiv97s^{-1}\bmod196\). The target is \(1\bmod4\) and a unit modulo 7; represent it modulo 7 by the finite-field norm, lift a nonzero coordinate modulo 49, and arrange one odd and one even coordinate by CRT. Add the same large multiple of 196 to the first coordinate of every multiplier to ensure \(M_{\max}/M_{\min}<3/2\). Multiplying norms of residue \(s\) in \([k/M_{\min},3k/(2M_{\max}))\) by \(M_s\) puts every image in the desired interval and class. The interval has fixed positive relative length and each image has only bounded multiplicity. Thus \(\sum_T r(T)\gg k\sqrt{\log k}\).

## Uniform pair sieve

For two distinct shifts with difference \(h\), substitute \(T=106+196t\) in the cofactor equations. On a \(t\)-interval of length \(X\asymp k\), at \(p\equiv3\bmod4,\ p\ne7\) forbid valuation exactly one for either cofactor. Modulo \(p^2\) the union has \(\rho(p)=2(p-1),p,p-1\) classes for \(p\nmid h,\ p\parallel h,\ p^2\mid h\), respectively: in the last two cases the divisible-by-\(p\) cosets coincide, and only the excluded lift to depth two can differ. Put \(g(p)=\rho(p)/p^2,\ w(p)=g(p)/(1-g(p))\), extended multiplicatively to squarefree products of the sieving primes.

Here is an elementary upper-bound sieve with a uniform constant in \(h\). Take \(R=X^{1/12}\) and sieve primes at most \(z=R^\epsilon\), for a sufficiently small fixed \(\epsilon>0\). Let \(G=\sum_{d\le R}w(d)\) on their squarefree products. The square of a Selberg divisor sum with \(\lambda_1=1\) majorizes survival. Its main term is
\[
 X\sum_{d,e}\lambda_d\lambda_e g([d,e])
   =X\sum_j \frac{u_j^2}{w(j)},\qquad
 u_j=\sum_{j\mid d}\lambda_d g(d).
\]
This diagonalization follows by expanding \(1/g((d,e))\) as the divisor sum of \(1/w(j)\). Set \(u_j=\mu(j)w(j)/G\) for \(j\le R\) and zero beyond. Inversion gives \(\lambda_1=1\) and
\[
 |\lambda_d| = \frac{\prod_{p\mid d}(1+w(p))}{G}
       \sum_{\substack{b\le R/d\\(b,d)=1}}w(b)\ \le1 .
\]
The inequality follows by expanding the product as a sum over divisors of \(d\); the resulting distinct indices are at most \(R\). The main term is \(X/G\), while CRT class counts modulo \([d,e]^2\) contribute total error at most \(O(R^6)=O(\sqrt X)\).

In the unrestricted finite Euler product \(\prod_{p\le z}(1+w(p))\), the expected value of \(\log d\) under the product weights is \(\sum_{p\le z}g(p)\log p=O(\log z)\). For sufficiently small \(\epsilon\), at least half its weight lies at \(d\le R\). The reciprocal-prime estimate in the inert progression gives \(G\gg\log X/\prod_{p\mid h,\ p\equiv3(4),\ p\ne7}(1+1/p)\): the generic local factor is \(1+2/p+O(1/p^2)\), while the loss at \(p\mid h\) is at most \((1+1/p)(1+O(1/p^2))\). This uses the arithmetic-progression Mertens estimate \(\sum_{p\le z,\ p\equiv3(4)}p^{-1}=(\log\log z)/2+O(1)\). Thus the pair count is \(O((X/\log X)\prod_{p\mid h,\ p\equiv3(4)}(1+1/p))\), uniformly in the difference; the sieve error is smaller.

## Average correction and conclusion

Set \(B=9^{21}\), so the differences are a power of 9 times \(B^j-1\), \(j=|e-f|/21\). The correction from 3 is bounded. Expanding the remaining product gives an average at most a constant because
\[
 \sum_m (m\,\operatorname{ord}_mB)^{-1}<\infty
\]
over squarefree products of the allowed inert primes different from 3 and 7. Indeed if \(\operatorname{ord}_m B\le u\), all prime factors of \(m\) divide \(\prod_{j\le u}(B^j-1)\), whose logarithm is \(O(u^2)\). The product of \(1+1/p\) over these prime factors is \(O(\sqrt{\log(3u)})\): below \(u^2+2\) use the same progression estimate, and above it the total reciprocal contribution is bounded by the logarithmic factor budget divided by \((u^2+2)\log(u^2+2)\). Summing over dyadic order intervals proves convergence. Counting each \(j\le H\) with its actual multiples gives total correction \(O(H)\).

There are \(O(H)\) pairs for each difference \(j\). Inserting the uniform pair bound and allowing the trivial \(O(kH)\) diagonal gives \(\sum_T r(T)^2=O(k\log k)\). The first moment implies that \(T\)'s with \(r(T)\) below a sufficiently small constant times \(\sqrt{\log k}\) consume at most half the first moment. Cauchy–Schwarz on the rest gives \(\gg k\) such \(T\)'s. There are \(\Theta(k)\) allowed targets \(T\), completing the assertion. This uses neither independence of the shifts nor a pointwise density claim for arbitrary integers.
