# Adversarial proof audit — independent review requested

This is a review target list, not a claim that an independent audit has already occurred.
All references below are to `research_report_zh.md` in this packet.

## Claim-status map

| Item | Status in this packet | What the replay proves |
|---|---|---|
| A1–A7, B9, centered-quadric determinant | Explicit algebraic proofs and exact symbolic checks | Exact symbolic identities |
| B2/B4 positive grid | All-index algebraic/injection proofs | 18 truncated instances through 20,000 |
| B13 binary sections | All-index bijective proofs | All three sections through the specified target bound |
| B15–B18 nonlinear closure | Exact identities; not positivity-preserving, unbounded convolution fanout | Identities to 20,000; recursive reconstruction to 512 |
| M | Complete analytic proof in §4.2–4.5; independent review pending | Only finite-degree homogeneous/inhomogeneous exclusions |
| M+ | Complete operator-elimination proof in §4.8; independent review pending | Not mechanically certified |
| Q | Complete scoped proof using ESS/Landau; independent review pending | Countermodels only, not asymptotic counting |
| Q* | Complete last-defect path proof in §5.7; independent review pending | Quadric determinant only, not the asymptotic/path theorem |
| Q† | Monotone exponent-dependent-carry extension of Q*; review pending | Not mechanically certified |
| R | UNPROVED; conditional restart gate | No original-n verification is used to claim this lemma |
| Original A303656 | Not solved in this packet | No finite test is a universal proof |

## Critical attacks on M

Check the c=d=0 convention and the bilateral theta multiplicities first.

The exact periodization is P_b(y)=S_b(exp(-y))-h_b(exp(-y)); the minus sign is
important. Verify both functional equations, the derivative periodization,
and the Gamma Fourier coefficient. Gamma has no zeros on the relevant imaginary
lattice. Smooth periodic functions have absolutely summable Fourier coefficients.

After coefficient polynomials are expanded at x=1, verify the minimal vanishing
order and all cases for the rational forcing. The normalized error must tend to
zero even after division by the leading power of t.

For A*y^2+y*B(y)+C(y) -> 0, establish A=0, then B=0, then C=0. Do not assume that
the mixed frequencies have a uniform separation: they do not. Absolute Fourier
summability, followed by Cesaro averaging, is the justification actually used.

Verify uniqueness of every selected mixed frequency, distinctness of the phase
pairs and both Vandermonde arguments. The theorem is linear, not algebraic:
the H-grid has an exact rank-one quadratic identity.

## Critical attacks on M+

Check the coefficient field enlargement to rational Puiseux functions supported
on the finitely many prime factors of the scales. Every dilation must be an
automorphism there; no incorrect Noetherian claim for the polynomial Mahler
algebra is needed.

Verify the common-left-multiple and common-right-multiple dimension arguments
separately, using the appropriate left/right vector spaces. Verify that the
operator ring is a domain. These facts permit a two-sided Ore division ring.

If I-P were singular over that division ring, a common right denominator would
produce a nonzero polynomial right-kernel vector. Its lowest total operator-degree
cannot cancel, because all monomials of P have positive degree. This step is where
K>=2 is used.

Clear the inverse row on the LEFT to obtain B(I-P)=q e_F^t. Applying this identity
to the vector equation must give q.F in the Puiseux coefficient field. Finally,
verify that M's proof extends to coefficients meromorphic at x=1. Do not pretend
that a usual commutative determinant suffices.

## Critical attacks on Q

The source weights in Q are positive INTEGERS. A fractional state with weights
1/2,1/2 and scale 2 allows two simultaneously free exponent axes, so removing
that hypothesis from Q's one-step S-unit argument is invalid.

Check the decomposition into minimal vanishing subsums and the projective use
of ESS. Mixed-base ratios fix absolute exponent values. Check all singleton,
zero-constant and two-axis degeneracies. Only finitely many non-axis exponent
quadruples remain. Landau is used only for those fixed translated/dilated
norm supports. The result is about incoming rule images, not original exceptions.

## Critical attacks on Q*

1. **State normalization:** every binary positive definite rational quadratic
   polynomial is centered, and its residual constant is put into C_i. The
   source and target may have different imaginary quadratic splitting fields.
2. **Norm rigidity:** when eta!=0, the homogenized source conic has rank three
   and is absolutely irreducible. Conjugation in the TARGET splitting field
   fixes this prime polynomial, so any rational norm has even valuation there.
   Denominators do not evade the parity argument.
3. **Sparse repair:** after the four exponents are fixed, the rational chart is
   not an identity. Its cleared polynomial has degree <=4D+2. A total-degree-d
   polynomial has at most d*L zeros on an L-by-L characteristic-zero grid.
   Coefficients may depend on the exponents; only degree and chart count are
   uniformly bounded. A separate finite chart count for each exponent tuple is
   insufficient unless the bound is UNIFORM over those tuples.
4. **Last-defect representation path:** each output witness is the next input
   witness. An arbitrary oracle that changes exponents and norm at an already
   known index is NOT included. Finite index base cases have only finitely many
   witnesses because of positive definiteness and positive power weights.
5. **Tail bound:** after the last defect, q_final=S*q_*. Unroll the affine
   indices exactly to prove |m-n_final/S|<=R_max. Handle small/negative m by a
   finite additional norm set; do not assume R is nonnegative.
6. **Zero norms:** explicitly separate them; they lead only to the original
   lacunary shift set. Nonzero state norm values have a uniform positive lower
   bound because there are finitely many rational quadratic lattices.
7. **All paths:** use the convergent sum over smooth multipliers S of S^(-1/2),
   not an unjustified bound on the number of words in the transition graph.
   Word count can be exponential; distinct norm multipliers have much smaller
   complexity. Finite paths and cycles are all included in this argument.
8. **Conclusion:** the bound is on the catalogue's reachable integers, not the
   set of representable integers and not the counterexample set of A303656.

## Required adversarial boundary examples

- B13 has exhaustive guards and strictly smaller indices but does not close the
  auxiliary states. This prevents conflating one-step contraction with induction.
- Fixed c=0 gives a valid 21 -> 5 zero descent in that narrowed state, yet both
  original integers are represented with c=1. State labels cannot be discarded.
- A(x)=1/(1-x)+F(x) has every coefficient positive and still has no mixed-dilation
  rational linear relation. This is an unconditional countermodel to inferring
  any support obstruction from counting non-Mahler behavior alone.
- Q* does not exclude algebraic-root/integer-square-root choices, unbounded
  charts or coordinate-dependent carries, multi-witness constructions, or arbitrary
  nonquadratic states. Exponent-only carries with strictly increasing indices are
  covered by the weaker Q† bound, including K=1.
- A finite list of terminal TYPES is not a finite list of terminal INTEGERS.

## Expected independent disposition

For each claim, return either an explicit counterexample/gap with its exact scope,
or a line-by-line acceptance of the argument. Do not accept M/Q* merely because
the replay passes. Do not reject them merely because the original conjecture is
unresolved. Do not update frozen authority before independent adjudication.

## Check Q† separately

The carry may depend on all four exponents but not on the square coordinates
after those exponents are fixed. Every successful step must strictly increase
the integer index. This keeps the last repair index at most X. Count repair
norms, smooth multipliers, and final exponent pairs separately to obtain the
weaker logarithmic exponent r+6. Do not reuse the sharper X/S estimate without
the fixed bounded-carry hypothesis of Q*.

## Nonlinear finite closure is not a counterexample to M+

The four basic series Phi, Psi, L3, L5 do satisfy the exact finite nonlinear
system in B15–B17. Verify the triangular-number coefficient bijection, including
both factors of four. Isolating q_n introduces a subtraction and a convolution
with growing fanout. At n=2, positive 1 minus positive 1 equals zero. The system
is an exact coefficient algorithm, not a positive minimal-zero proof.
