# One original signed side and two actual square sums at a fixed separation

This adds a nonzero **original positive-side** weight to the true two-norm problem of [FIXED_SHIFT_TRUE_NORM_PAIRS.md](FIXED_SHIFT_TRUE_NORM_PAIRS.md). It does not control the signed weight on the other side.

Choose the actual shifts \(s=3^c+5^d,\ t=3^{c+24}+5^d\) in the ordinary box from [FIXED_NONZERO_SHIFT_BUCKET.md](FIXED_NONZERO_SHIFT_BUCKET.md), write \(h=t-s\), and set \(M=480480\). Use the following nine distinct primes: four of scale \(X^{0.017}\) and two of scale \(X^{0.021}\), with product \(B\), two of scale \(X^{0.175}\), with product \(P\), and one of scale \(X^{0.54}\), denoted \(p\). The first eight are \(1\bmod M\); the last is \(450061\bmod M\). Use disjoint intervals of fixed positive relative width small enough that all products \(z=BPp\) lie between \(5X/4\) and \(4X/3\). Then \(n=s+z\equiv319055\bmod M\), \(z,z-h\in[X,3X/2)\) for large \(X\), and \(z\) is a true norm. The factor intervals give a unique decoding of each \(z\); by the prime number theorem in fixed progressions there are \(|\mathcal P|\asymp X/(\log X)^9\) such products.

## The other residual has norm representations on average

For \(m=z-h\equiv1\bmod4\), complementary divisors give
\[
 r_2(m)=8\sum_{j\mid m}\chi_4(j)\omega(j/\sqrt m),
\]
where the smooth cutoff is 1 below \(1/2\), 0 above 2, and \(\omega(v)+\omega(1/v)=1\). The modulus condition is \(z\equiv h\bmod j\). The primes of \(h\) and \(M\) can be omitted from \(j\): the prescribed negative residue is a unit mod \(M\), and the factors of \(z\) tend to infinity whereas the support of \(h\) is fixed. Write \(E=\operatorname{rad}(Mh)\).

Use [Blomer–Grimmelt–Li–Rydin Myerson, Proposition 5.1](https://arxiv.org/pdf/2111.01601#page=15) with its short variable \(B\asymp X^{0.11}\), long variable \(Pp\asymp X^{0.89}\), modulus variable \(j\ll\sqrt X\), \(a_1=h\ne0,\ a_2=1\), and added modulus \(M\) in the averaged \(d\)-slot of that proposition, taking its divisor \(a_3=1\). Here its small \(\eta\) may be fixed below \(0.11\); the remaining powers \(\delta(\eta)>0\) accommodate the fixed modulus and a sufficiently large fixed logarithmic power for the conductor cutoff. Split \(\chi_4(j)\) into the two reduced residue classes mod 4. The product sequences are divisor-bounded and the small-variable coprimality hypothesis with \(a_2=1\) is automatic. The estimate applies to rectangular prefixes in the two variables by restricting their coefficients, and to divisor prefixes by summing dyadic ranges. On the normalized product box the cutoff has bounded mixed variation in the three variables, so partial summation preserves an error \(O_J(X(\log X)^{-J})\) for any fixed \(J\), by choosing the conductor cutoff power large enough.

For \((j,M)=1\), a nonprincipal small-conductor character on the \(j\)-slot has negligible sum over \(p\) by Siegel–Walfisz: fix the other eight primes, use the fixed residue on \(M\) and conductor at most a power of \(\log X\), and use \(p\gg X^{0.54}>j\) to avoid the induced character's additional \(p\)-coprimality exceptions. The fixed product residue makes the sum of characters on the \(M\)-slot effectively a density of 1 on the chosen product support, not \(1/\varphi(M)\). For the principal term, omitting the potential exclusions \((j,z)>1\) costs a power-saving relative error, since each of the nine prime factors \(\ell\mid z\) grows by a positive power of \(X\) and \(\sum_{j\le 2\sqrt X,\ell\mid j}1/\varphi(j)\ll \log X/\ell\).

Consequently
\[
 \sum_{z\in\mathcal P}r_2(z-h)=8 C_E|\mathcal P|+O_J(X(\log X)^{-J}),\qquad
 C_E=\sum_{(j,E)=1}\frac{\chi_4(j)}{\varphi(j)}>0.
\]
For the smoothed limit, use \(j/\varphi(j)=\sum_{e\mid j}\mu^2(e)/\varphi(e)\) and the bounded partial sums of \(\chi_4(j)1_{(j,E)=1}\), giving \(O_E(X^{-1/4})\) at cutoff of size \(\sqrt X\). The constant is \(L(1,\chi_4)\prod_{\ell\mid E}(1-\chi_4(\ell)/\ell)\prod_{\ell\nmid E}(1+\chi_4(\ell)/(\ell(\ell-1)))\), positive by absolute convergence of the last product. Using \(\sum_{m\asymp X}r_2(m)^2\ll X\log X\) (the one-form case of the [corrected Henriot upper bound](https://doi.org/10.1017/S0305004114000280), by the same local calculation as [the deduplication note](DEDUPLICATED_TRUE_NORM_SHIFT_COUNT.md)), Cauchy–Schwarz gives \(\gg X/(\log X)^{19}\) **distinct** \(n\) with both true norms for each fixed allowed \(c,d\).

## The original complete grouping on the positive side

For \(R=X^{1/4}\), let \(T_R(m)=\sum_{j\mid m,\ j\le R}\mu(j)\log(R/j)\). The grouping is \(-\sum_a T_R(z/a)/\log(z/a)\), with legal \(a\mid z,\ X^{1/16}\le a\le X^{1/8}\). Such \(a\) divide \(B\); \(B\) and each \(B/\ell\) are legal. If \(C=B/a\), \(Cp_i<R\) for either individual middle prime \(p_i\), but \(P>R\) and \(p>R\), so the elementary Möbius expansion gives \(\log(P/R)\) for \(C=1\), \(-\log\ell\) for \(C=\ell\), and zero when \(C\) contains at least two primes. Thus the complete positive-end weight is
\[
 -\frac{\log(P/R)}{\log(Pp)}+\sum_{\ell\mid B}\frac{\log\ell}{\log(\ell Pp)}.
\]
After multiplication by \(\log(Pp)/\log X\), its lower limit is at least \(-1/10+(0.11)(0.89)/(0.89+0.021)=34/4555>0\). This certifies the original positive weight, while leaving the negative-side sign or even nonvanishing open.
