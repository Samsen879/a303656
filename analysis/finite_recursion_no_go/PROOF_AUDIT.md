# Independent adversarial proof audit

## Disposition

```text
FINAL GATE: ACCEPT
PROMOTION CLASS: ROUTE-PRUNING THEOREM UNDER EXPLICIT HYPOTHESES
A303656: UNRESOLVED
GENERAL PROOF: NONE
CERTIFIED COUNTEREXAMPLE: NONE
```

The packet was treated as untrusted.  Its implementation was not read or
imported before the independent verifier was written.  No counterexample was
found inside the formal scopes of M, M+, Q, Q*, or Q-dagger.

## Step audit

| Claim or proof step | Verdict | Independent finding |
|---|---|---|
| M2--M4 periodization and Fourier coefficients | VALID | Both functional equations have the stated signs; differentiation gives the bilateral periodization; division by `i omega` gives `Gamma(i omega)/log b`, nonzero for nonzero modes. |
| M5--M7 radial extraction | VALID | The theta factor contributes `pi/(Kt)` and the lacunary sums retain the log-periodic terms.  After the minimal vanishing-order normalization all discarded terms are `o(1)`. |
| M7 almost-periodic limit | VALID | Absolute Fourier summability permits coefficientwise Cesaro means even though mixed frequencies have no uniform separation. |
| M8 phase separation | VALID | Irrationality of `log 3/log 5` gives unique mixed frequencies.  Grouping first by the 3-phase and then the 5-phase makes both Vandermonde matrices nonsingular. |
| M conclusion and H-grid corollary | VALID | Repeated dilations must be combined; with pairwise distinct dilations the proof covers all finite rational relations and meromorphic-at-1 coefficient extensions used later. |
| M+ coefficient-field enlargement | VALID | Every chosen dilation becomes an automorphism of the finite-prime Puiseux field; each actual coefficient belongs to one finite extension and is meromorphic at `x=1`. |
| M+ common multiples/Ore fractions | VALID | Degree-ball dimension growth supplies nonzero common left and right multiples; the iterated commuting skew-polynomial ring is a domain. |
| M+ matrix elimination | VALID | `I-P` has no right kernel because the least operator degree of a nonzero vector cannot be cancelled by positive-degree `P`.  Clearing the inverse row on the left yields a nonzero scalar operator relation for F, contradicting M. |
| Q1 norm-defect rigidity | VALID | A nonzero additive defect produces an absolutely irreducible rank-three homogenized conic.  Its conjugation-fixed valuation is odd on the right and even in a rational norm. |
| Q nonzero-defect count | VALID | For each exponent tuple and chart the cleared nonzero polynomial has bounded degree and only `O(sqrt X)` lattice zeros; four exponents contribute `O(log^4 X)`. |
| Q zero-defect classification | VALID | Minimal vanishing subsums plus ESS leave only a single 3-axis or 5-axis family; both axes cannot remain free because positive integral weights and `K>=2` would force K to divide powers of both 3 and 5. |
| Q zero-density incoming bound | VALID | Infinite axis families miss multiples of 15; the finitely many remaining exponent tuples reduce to translated/dilated two-square supports and Landau's `O(X/sqrt(log X))` bound. |
| Q optional catalogue-complexity corollary | VALID WITH CLARIFICATION | `J(X)` must mean total rule-chart incidence (or an equivalent total catalogue-size measure), not merely the maximum charts attached to one rule.  No repository status relies on this optional corollary. |
| Q* generalized quadratic rigidity | VALID | Over the target splitting field, a nonzero defect leaves a rank-three source conic, still irreducible; differing discriminants do not change the norm-valuation parity argument. |
| Q* sparse repair count | VALID | Positive definiteness bounds coordinates by `O(sqrt Y)` and positive weights bound each exponent by `O(log Y)`; arbitrary guards only select a subset. |
| Q* witness continuity and finite bases | VALID | Each fixed state/index has finitely many representations.  The theorem does not grant an oracle that replaces the propagated witness by an unrelated representation. |
| Q* last-defect decomposition | VALID | After the last nonzero defect, norms multiply by a smooth multiplier S.  Unrolling fixed affine carries gives `|m-n_final/S|<=R_max`; low m contributes only finitely many norm seeds. |
| Q* path/word count | VALID | The proof counts distinct norm multipliers, not transition words.  `sum_S S^(-1/2)` converges over the fixed prime set, eliminating any hidden exponential word factor. |
| Q* zero norm and final exponents | VALID | Zero norm yields only `3^c+5^d`; every fixed final norm has `O(log^2 X)` original exponent pairs. |
| Q*8 asymptotic | VALID | Summing `sqrt(X/S) log^4 X` and then the final exponent pairs gives `sqrt X log^6 X`; defect-free and bounded-repair tails give `log^(r+2) X`; both are `o(X)`. |
| Q-dagger | VALID | Strict index increase keeps the last repair below X.  Multiplying the repair catalogue by `O(log^r X)` distinct smooth multipliers and `O(log^2 X)` final exponent pairs gives the stated `r+6` exponent. |

## Adversarial cases checked

- repeated multipliers are deduplicated at the level of multiplier values;
- `K=1` identity cycles are outside Q* and require Q-dagger's strict increase;
- constant and zero coefficients do not evade the conic valuation argument;
- arbitrary guards can encode a target predicate but cannot create witnesses
  outside the finite bounded-degree chart images;
- negative fixed carries are covered by the normalized affine-tail estimate;
- rational cosets, imprimitive forms, coordinate zero, and forms with extra
  automorphisms do not affect positive definiteness, finite fibers, or the
  valuation parity argument;
- finite seed types are not silently treated as finitely many integers: the
  theorem explicitly starts from finitely many `(state,index)` bases and then
  includes all of their finitely many actual witnesses;
- no finite check is used as proof of M, Q, Q*, or Q-dagger.

## Independent computation

`tools/reference_audit.py` uses only the Python standard library.  At limit
5000 it independently checked 22,831 exact catalogue evaluations, all B2/B4
identities for nine `(u,v)` pairs, all B13 sections in its declared range,
B15/B16 through 5000, a bounded affine nonzero-defect search, the affine-tail
inequality through length nine, duplicate multipliers, and an excluded K=1
cycle.  The output is `results/reference_audit.json`.

The producer replay was also rerun with Python 3.12.3, NumPy 2.5.1 and SymPy
1.14.0.  Its JSON differs from the supplied certificate only in the recorded
Python and NumPy versions; all mathematical fields are identical.

## Correction retained by this integration

The optional Q8 wording is normalized to "total rule-chart incidence" in this
audit.  The five named theorems require no mathematical repair.  The frozen
authority ledger is not rewritten; this post-freeze audit is indexed separately.
