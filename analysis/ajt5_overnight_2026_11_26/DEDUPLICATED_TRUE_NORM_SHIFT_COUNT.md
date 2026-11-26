# Deduplicating actual norm pairs across the common 5 exponent

In the setup of [FIXED_SHIFT_TRUE_NORM_PAIRS.md](FIXED_SHIFT_TRUE_NORM_PAIRS.md), the underlying construction gives \(\gg X\) ordered representation pairs per admissible common \(d\). Using analytic upper bounds on multiplicities, these yield
\[
 \gg_\varepsilon X/(\log X)^{\,2\log 2-1+\varepsilon}
\]
**distinct targets \(n\)** with at least one good \(d\). This is unweighted and does not give the original signed mixed moment or a density-one result.

## Uniform upper moments

Let \(t_1,\dots,t_k\) be distinct shifts of size \(O(\sqrt X)\), with \(k=2\) or 4, and put \(D=\prod_{i<j}(t_i-t_j)\ne0\). For fixed \(\lambda\ge1\), apply [Henriot's corrected Theorem 5](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nair-tenenbaum-uniform-with-respect-to-the-discriminant-erratum.pdf), an upper bound, to the primitive monic forms \(m-t_i\) and \(F=\prod_i (r_2(m_i)/4)^\lambda\). Its small power-growth condition holds for any fixed permitted positive growth exponent: the multiplicative weight on \(p^e\) is at most \((e+1)^\lambda\), bounded by an exponential in \(e\) and by a fixed constant times \(p^{\eta e}\) at each of finitely many small primes, with no constant needed at larger primes. The polynomial product has coefficient size \(O_k(X^{k/2})\); the length-\(X\) interval meets the theorem's size conditions with \(\alpha=\delta=1/4\) for large \(X\).

Extend the nonnegative divisor sum into its Euler product over \(p\le X\). The local factor is 1 plus the sum over all nonzero valuation vectors \((e_1,\ldots,e_k)\) of their joint exact congruence probabilities times the product weight. The modulus for such a vector is \(p^{1+\max e_i}\). In particular zero valuations at its other coordinates are imposed, as in the erratum. For a fixed maximum \(m\ge1\) the valuation events are disjoint and require membership in at most \(k\) residue classes mod \(p^m\). The entire contribution at this level is at most \(k(m+1)^{k\lambda}/p^m\). Hence every bad local factor is \(1+O_{k,\lambda}(1/p)\), uniformly even when the shift differences have growing prime-power valuation.

At \(p\nmid D\) at most one form vanishes mod \(p\). With \(f_\lambda(j)=(r_2(j)/4)^\lambda\), the combined Euler and sieve factor is \(1+k(f_\lambda(p)-1)/p+O_{k,\lambda}(p^{-2})\) for \(p>k\). At split primes \(f_\lambda(p)=2^\lambda\), and at inert primes it is zero. Using [Mertens' theorem in arithmetic progressions](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf), this proves
\[
 \sum_{X<n\le2X}\prod_i r_2(n-t_i)^\lambda
 \ll_{k,\lambda} X(\log X)^{k(2^{\lambda-1}-1)}
 \prod_{p\mid D}(1+C_{k,\lambda}/p).
\]
Small primes and harmless changes at interval endpoints can be absorbed or handled by slightly enlarging the interval. No lower bound from Henriot is used.

## Count distinct targets

Write \(W_d(n)=r_2(n-s_d)r_2(n-t_d)\) on the allowed class and actual residual window (including the chosen coprimality and exact 29/37 markers), and zero elsewhere. There are \(K\asymp\log X\) admissible \(d\)'s. For each \(d\) the shift difference \(h=3^c(3^{24}-1)\) has fixed prime support, so its \(\lambda\) moment is \(O_\lambda(X(\log X)^{2^\lambda-2})\), uniformly in \(c\). For distinct \(d,e\), all four shifts are different: the 5-power separation has absolute value greater than \(h\). Their discriminant prime support is contained in that of \(h g(g-h)(g+h)\), where \(g=5^e-5^d\); its absolute value is \(X^{O(1)}\). Splitting its prime factors at \(\log X\) gives \(\prod(1+C/p)\ll(\log\log X)^{C'}\) for fixed constants, using the ordinary prime reciprocal sum below the split and the bound on the number of larger factors. Apply the uniform bound with \(k=4,\lambda=1\) to get \(\sum_n W_d(n)W_e(n)\ll X(\log\log X)^{C'}\).

For \(H_0=(\log X)^{2\log 2+\varepsilon}\), remove the weights \(W_d(n)>H_0\). The lost first moment is at most \(O_\lambda(X(\log X)^{2^\lambda-2}/H_0^{\lambda-1})=o(X)\) by choosing fixed \(\lambda>1\) close enough to 1. The retained mass over all \(d\) is \(\gg XK\). Its summed second moment is \(O(XKH_0+XK^2(\log\log X)^{C'})\), using the cutoff on the diagonal and the four-form bound elsewhere. Cauchy–Schwarz now gives the distinct-target result. In particular the \(d\) multiplier is not counted as a new target when the same integer survives for two labels.
