# Divisor switching, positive deformation, and the unresolved signed aggregate

## Exact hyperbola formula: keep the diagonal sign

For m>0 let u be its odd part. On A23, chi_4(u)=1. Pairing h with u/h gives
\[
 {r_2(m)\over4}
 =2\sum_{h\mid u,\ h<\sqrt u}\chi_4(h)
   +1_{u=\square}\chi_4(\sqrt u).                                \tag{D1}
\]
The diagonal is NOT always +1. At u=9 it is chi_4(3)=-1, and the right side is 2-1=1. Removing it as a nonnegative term would be invalid.

The same pairing for the centered transform gives
\[
 F_u(s)=2\sum_{h\mid u,h<\sqrt u}\chi_4(h)
       \cosh\big(s\log(\sqrt u/h)\big)
       +1_{u=\square}\chi_4(\sqrt u).                            \tag{D2}
\]
This reduces the divisor range to sqrt(u), but does not make its summands nonnegative. Their total is positive for s>0 by the prime-factor argument in PW-03.

## What changed relative to the raw r_2 identity

The deformation
\[
 d_u(s)=\sum_{h\mid u}\chi_4(h)h^{-s}>0\quad(s>0)
\]
is positive even when u is not a norm. Its centered Taylor series records the number of odd valuation defects as its order of vanishing. Under the 2-adic norm condition that order is even. Thus the lowest possible failing degree is 2, creating the exact dilation gap 4 for F_u and 4/sqrt(e) for d_u at s=1/log n.

The single target ML-D2 is
\[
 \mathcal D_n(2/\log n)\le2\mathcal D_n(1/\log n)
 \quad\text{for every sufficiently large fixed n}.
\]
Its proved implication uses the strict separation 4/sqrt(e)>2. There is no average over n, no exceptional-set hypothesis, and no finite-prime completion assumption in that implication. All prime sizes enter the exact divisor transform.

## The exact analytic quantity still missing

Equivalently, ML-D2 asks for the following one-sided signed modulus sum to be nonnegative:
\[
 \boxed{\sum_{h\le n}\chi_4(h)
  \big(2h^{-1/\log n}-h^{-2/\log n}\big)A_h(n)\ge0.}              \tag{D3}
\]
This is a sufficient, quantitatively fixed condition, NOT a theorem in this package. It is stronger than the existence of one norm in a general bulk sample; the strictness test in COUNTEREXAMPLES.md demonstrates that distinction.

For h=n^theta with 0<=theta<=1, the kernel in (D3) is
\[
 2e^{-\theta}-e^{-2\theta}\in[2/e-e^{-2},1].
\]
Consequently this deformation does NOT truncate the large divisors. The missing cancellation extends over polynomial-sized moduli. The centered hyperbola formula reduces that to sqrt(u), still far above the level in PW-01. This is why a formal positive transform is not yet an analytic solution of the parity/lower-tail problem.

One may write A_h=M/h+r_h, but this is merely a definition of r_h, not an equidistribution theorem. The complete-period model from PW-01 is not M/h. In particular small-modulus and 2/3 conditioning correlations must not be silently absorbed into an asserted error term. PW-02 prevents a polynomial-range o(M) absolute bound for this random-integer model. A SIGNED bound can escape that no-go, but has not been established.

## Character expansion and the precise scale mismatch

On the unfiltered rectangle the exact additive-character formula is
\[
 A_h^{\rm rect}(n)={1\over h}\sum_{t\bmod h}e(-tn/h)
 \left(\sum_{c=0}^Ce(t3^c/h)\right)
 \left(\sum_{d=0}^De(t5^d/h)\right).
\]
It holds even if h is divisible by 3 or 5. Multiplicative-order estimates, however, require units, and h divisible by a base must be treated separately.

For A23, the exact formula instead has the local indicator INSIDE the double sum. It does not factor into the two displayed orbit sums. Truncating the 2/3 tests and expanding their periodic indicator into finitely many Fourier modes is legitimate, but introduces its periods, coefficients, and the discarded-pair error from PW-01. No zero-cost factorization is available.

For h near n^theta, each geometric orbit has length O(log n), far shorter than h^epsilon. A complete-subgroup estimate applies to a different set unless the available exponent interval includes a complete orbit. Completing an orbit with huge period cannot manufacture the missing sample length.

Likewise, embedding residuals or shifts into an interval and applying a classical large sieve uses the ambient integer interval length, of order n, not the O(log^2 n) number of occupied positions. If coefficients mark M distinct residuals, its energy factor is of order M, but the large-sieve constant still has an ambient n term. A specialized sparse large sieve might improve this; none of the retrieved theorems supplies the signed fixed-target bound (D3).

## Bounded auxiliary minorant

PW-04 cancels the quadratic defect term in F_u/τ(u). Its per-row error is at most
\[
 E(1)=(\cosh1-4\cosh(1/2)+3)/3
 =0.0108589246632402125243349917154578774700468799903979\ldots.
\]
A bound of E(1)M for the total error is not a positivity theorem. Nor is one allowed to insert an average value of r_2/(4τ(u)) into a fixed-n grid sum. This weight is retained as an explicit testable analytic tool, not as a claimed new support lower bound.

## Verdict

DIVISOR-SWITCH ROUTE: ADVANCED at the conditional-reduction level only.

The positive deformation, defect-order proof, dilation gap, and bounded minorant are established here. The actual fixed-target signed cancellation is BLOCKED. No old scoped negative theorem about theta/divisor methods is claimed to have been refuted; these results identify a new quantitative target without proving it.
