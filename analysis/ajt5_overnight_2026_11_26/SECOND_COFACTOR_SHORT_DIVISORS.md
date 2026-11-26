# A second legal cofactor: the short part of the divisor expansion

Use the positive marked products \(z=Kp\) of [ONE_SIGNED_SIDE_TRUE_NORMS.md](ONE_SIGNED_SIDE_TRUE_NORMS.md), so \(K\asymp X^{0.46}, p\asymp X^{0.54}, |\mathcal P|\asymp X/(\log X)^9\). Fix the actual ordinary shift pair and nonzero separation \(h\). For a split prime \(a\in(X^{1/16},2X^{1/16}]\), the negative end \(z-h\) has \(a\) as a legal cofactor whenever \(a\mid z-h\). The intended negative-side norm weight is \(r_2((z-h)/a)\) at exact valuation 1. This note evaluates its *short signed divisor part*, not the full norm weight.

The contribution lost by deleting \(a^2\mid z-h\) is negligible at the intended main scale \(X/(\log X)^{10}\): ignoring primality and all restrictions on \(z\) gives \(O(X^{15/16}+X^{1/16})\) pairs \((a,z)\), and the absolute divisor sum at each is \(O_\epsilon(X^\epsilon)\). The full divisor cutoff \(\sqrt{(z-h)/a}\) is of order \(X^{15/32}\). Thus the once-divisible layer reaches a combined modulus of order \(X^{17/32}\), not the larger square-deletion modulus.

For fixed \(0<\theta<83/400\), let \(E=\operatorname{rad}(480480h)\). On \(d\le X^\theta\) the smooth relative cutoff is identically 1 for sufficiently large \(X\), and
\[
 8\sum_a\ \sum_{\substack{d\le X^\theta\\(d,Ea)=1}}\chi_4(d)
       \#\{z\in\mathcal P:ad\mid z-h\}
 =8|\mathcal P|\sum_a C_{Ea}/a+O_J(X(\log X)^{-J}).
\]
The right side is of order \(X/(\log X)^{10}\), where \(C_F=\sum_{(d,F)=1}\chi_4(d)/\varphi(d)>0\) is the constant of the preceding proof.

Indeed, for each fixed \(K\), the prime \(p\) must lie in one reduced class mod \(480480\,ad\) when \((K,ad)=1\); if these are not coprime there is no hit since \((ad,h)=1\). The original fixed residue and each admissible \(K\) give the same stock prime count on its fixed residue mod 480480. The combined modulus satisfies \(ad\ll X^{1/16+\theta}<X^{0.27}\), below the square-root limit of the \(p\) scale by a power. Apply [Bombieri–Vinogradov](https://doi.org/10.1112/S0025579300005313) with maximum reduced residue (and interval endpoint) for each \(K\). A modulus in this range has only a bounded number of prime divisors \(a>X^{1/16}\), so replacing the pair sum by modulus errors costs a constant. Summing \(O(X^{0.46})\) possible \(K\)'s and using arbitrary logarithmic savings gives the claimed error. For the principal term, missing divisors with \((K,d)>1\) cost a relative power-saving by the reciprocal-totient estimate for each growing prime factor of \(K\). The divisor tail \(\sum_{d>X^\theta,(d,Ea)=1}\chi_4(d)/\varphi(d)\) is \(O_E(X^{-\theta/2})\) uniformly in \(a\), using the \(d/\varphi(d)\) convolution and bounded partial sums after the fixed support and the one prime \(a\) are excluded. Replacing \(1/\varphi(a)\) by \(1/a\) has a power-saving total difference.

The missing part is \(X^\theta<d\ll X^{15/32}\) with the oscillating character and the smooth cutoff on \(d\sqrt{a/(z-h)}\). The long modulus is \(ad\) with an identified growing prime factor \(a\). No upper bound small enough to exclude cancellation of the short main term is established here. Even a full norm lower bound with that cofactor would still require auditing the original negative grouping sign.
