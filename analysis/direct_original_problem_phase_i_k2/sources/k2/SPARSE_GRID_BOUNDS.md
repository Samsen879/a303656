# Sparse-grid bounds and the absolute-remainder barrier

## K2-U1. An exact, elementary per-prime capacity

Put C=floor(log_3 n), D=floor(log_5 n), and for a prime p not dividing 15 let
`h_3=ord_p(3)`, `h_5=ord_p(5)`. A congruence `3^c+5^d=n mod p`, at fixed c,
either has no solution for d or has one residue class modulo h_5. The analogous
statement holds at fixed d. Since G is a subset of the full rectangle,
\[
S_p(n)\le\min\left\{
 (C+1)(1+\lfloor D/h_5\rfloor),
 (D+1)(1+\lfloor C/h_3\rfloor)\right\}.                    \tag{U1}
\]
The inequality includes the case p divides n. No subgroup equidistribution
assumption occurs in its proof.

Since `a^{h_a}>=p+1` for a=3,5,
\[
S_p(n)\ll \log n+\frac{(\log n)^2}{\log p}.                \tag{U2}
\]
Therefore, using Phase K, for every fixed B>0,
\[
\sup_{p\ge(\log n)^B}\frac{N_p^G(n)}{G(n)}
\ll\frac1{\log n}+\frac1{B\log\log n}=o(1).
\]
For p>=n^theta it gives `N_p^G=O_theta(log n)`. These are elementary individual
fiber bounds. **They do not imply that the union of the prime fibers occupies
o(G)**. No historical novelty and no success-level-C range closure are claimed.

For a unit composite modulus d, the analogous two order bounds hold with orders
modulo d. Its being a product of two bad primes does not supply a bound on the
number of available moduli d.

## Direct Fourier/energy check

On the full rectangle let A and B be the exponent-image multisets modulo p.
The fiber has exact Fourier expansion
\[
\frac{|A||B|}{p}+\frac1p\sum_{r\ne0}\widehat A(r)\widehat B(r)e(-nr/p).
\]
If p>=n^theta, order bounds make the multiplicity of each element in A or B
`O_theta(1)`. Parseval and Cauchy bound the absolute error by `O_theta(log n)`,
while the main term is `O((log n)^2/p)`. This agrees with U2 but is nowhere near
a positive pointwise main term in the large-prime range. It is not permissible
to replace the long containing subgroups by the short prefixes in a complete-group
theorem without proving a new truncation estimate.

## K2-N3(a). Integer-distance obstruction for ordinary local models

**General finite statement.** Let H be a positive integer, a_p any nonnegative
integers, and `0<=mu_p<=1/2`. Then
\[
 |a_p-\mu_p|\ge\mu_p.                                    \tag{E1}
\]
For a_p=0 this is equality; for a_p>=1 the left side is at least 1-mu_p>=mu_p.
There is no probabilistic hypothesis.

For uniform integers, the probability of an odd p-adic valuation equals
\[
\sum_{j\ge0}\frac{p-1}{p^{2j+2}}=\frac1{p+1}.
\]
Consider an attempted model `A_p=H/(p+1)+r_p`. Regardless of the actual integers A_p,
\[
 \sum_{\substack{2H<p\le Q\\p\equiv3\ (4)}}|r_p|
 \ge H\sum_{\substack{2H<p\le Q\\p\equiv3\ (4)}}\frac1{p+1}.       \tag{E2}
\]
Reference L2 gives, as H tends to infinity,
\[
\sum_{2H<p\le Q,\ p\equiv3(4)}\frac1{p+1}
=\frac12\log\frac{\log Q}{\log(2H)}+O(1/\log H).
\]
If H is of order `(log n)^2` and Q=n^theta for fixed theta>0, E2 is
\[
 \ge (1/2+o(1))H\log\log n.                              \tag{E3}
\]
Already Q=H^(1+epsilon) gives a lower bound
`( (1/2) log(1+epsilon)+o(1))*H`.
The same argument applies to a divisibility model with mean H/p, or with mean
H/(p-1) after shifting the lower threshold slightly.

**Scope.** The uniform-integer density 1/(p+1) has NOT been asserted to be the
actual density on the literal exponent grid. The theorem says that, even if one
chooses that smooth model, an unweighted absolute sum of all its errors cannot be
small at the proposed level. More generally it applies when model densities
are bounded above and below by positive constants times 1/p on a prime family
with the indicated reciprocal mass. A different, justified orbit-specific model
must be audited separately.

## K2-N3(b). Least-prime logarithmic conditioning does not repair the absolute error

Fix alpha>0 and constants 0<c_1<=c_2. Suppose a smooth least-prime model assigns
\[
 \frac{c_1H}{p(\log p)^\alpha}\le\mu_p\le
 \frac{c_2H}{p(\log p)^\alpha}
\]
for all p=3 mod 4 in `(T,Q]`, where `T=max(3,2c_2 H)` and Q=n^theta.
For all sufficiently large H each mu_p<=1/2. For any integer counts, including
`a_p=N_p^G(n)`, E1 gives
\[
\sum_{T<p\le Q,\ p\equiv3(4)}|a_p-\mu_p|
\ge c_1H\sum_{T<p\le Q,\ p\equiv3(4)}\frac1{p(\log p)^\alpha}.
                                                                    \tag{E4}
\]
Partial summation of the progression Mertens formula proves
\[
\sum_{T<p\le Q,\ p\equiv3(4)}\frac1{p(\log p)^\alpha}
=\frac{(\log T)^{-\alpha}-(\log Q)^{-\alpha}}{2\alpha}
 +O_\alpha((\log T)^{-\alpha-1}).                          \tag{E5}
\]
For completeness, write the reciprocal-prime summatory function as
`M(t)=(1/2)log log t+C+E(t)`, `E(t)=O(1/log t)`, and integrate
`(log t)^(-alpha) dM(t)`. The main integral is
`(1/2) int dt/[t(log t)^(alpha+1)]`; integration by parts bounds the E contribution
by `O((log T)^(-alpha-1))`, including both endpoints. This proves E5.

For H of order `(log n)^2`, E4 is
\[
 \Omega_{\alpha,c_1,c_2}\left(\frac{H}{(\log H)^\alpha}\right).
                                                                    \tag{E6}
\]
In particular it is **not** `o(H/log n)` for any fixed alpha. For the natural
half-dimensional alpha=1/2, the floor `H/sqrt(log H)` is also much larger than
the prospective witness scale `H/sqrt(log n)`.

This is the precise failure of the attempted repair: making the smooth main
terms summable does not make their absolute integer errors smaller than the
final witness margin. It does not rule out cancellation of the signed sum,
specially supported sieve weights, a different density model, or a genuine
bilinear/global argument tied to the common literal n.

## The exact rejected method class

The no-go applies to proofs that (i) replace the integer prime incidences by one
of the positive smooth comparable models above, and (ii) seek a final pointwise
witness by bounding the sum of **all** absolute per-prime discrepancies through
a polynomial-in-n cutoff by a quantity below the witness margin. Such an error
budget is mathematically impossible. It is not an impossibility theorem for
all half-dimensional sieves, all parity-sensitive weights, or all arithmetic
methods on sparse sets. A large upper bound for this crude error sum does not
prove that every optimally weighted or signed remainder must be large.
