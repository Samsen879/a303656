# Post-freeze theorem and route index

This index records independently accepted work added after Master Authority V2.
It does not edit or supersede the immutable frozen ledger.  A303656 remains
**UNRESOLVED**.

| ID | Classification | Name | Scope | Route effect |
|---|---|---|---|---|
| PF-N-001 | PROVED NEGATIVE STRUCTURAL THEOREM | Mixed-dilation counting independence (M/M+) | Exact finite rational-linear systems containing the counting series F; fixed finite integer dilations | Rules out this counting-level linear closure, not Boolean or nonlinear recursion. |
| PF-N-002 | PROVED NEGATIVE STRUCTURAL THEOREM | Rational one-step incoming sparsity (Q) | Positive-integral two-square source weights; fixed affine targets; uniformly finite bounded-degree rational charts | Almost every multiple of 15 has no such incoming edge. |
| PF-N-003 | PROVED NEGATIVE STRUCTURAL THEOREM | Finite rational witness-recursion sparsity (Q*) | Finite seeds/states/rules, positive-definite binary rational forms, witness continuity, fixed `K>=2,R`, uniformly finite bounded-degree rational charts | Reachable original integers have density zero with the certified `sqrt(X) log^6 X + log^(r+2) X` bound. |
| PF-N-004 | PROVED NEGATIVE STRUCTURAL THEOREM | Monotone exponent-carry extension (Q-dagger) | Q* model with fixed `K>=1`, arbitrary exponent-dependent carry, and strict index increase | Reachable original integers remain density zero with the weaker `sqrt(X) log^(r+6) X + log^(r+2) X` bound. |

Evidence and exact boundaries: [finite recursion no-go audit](../analysis/finite_recursion_no_go/README.md).

## Triage wave 2026-11-14 (candidate results)

These entries retain their candidate and AI-only review qualifications; the
conditional synthesis was not separately refereed. They do not upgrade the
frozen ledger or establish LP. The subsequently supplied A2/R2/V/E2/L reports
and their version boundaries are recorded in the linked package's custody notes.

| ID | Classification | Name | Scope | Route effect |
|---|---|---|---|---|
| PF-P-001 | PROVED (candidate) | [A2 zero-set theorem](../analysis/triage_wave_2026_11_14/README.md#a-a2-zero-set-theorem-candidate-ai-refereed) | Profinite eventual-power norm profiles; candidate, AI-refereed | Zero-set equality a.e.; POS ⇔ LP. LP remains OPEN. |
| PF-P-002 | PROVED (candidate) | [V weighted integer L2 transfer](../analysis/triage_wave_2026_11_14/README.md#b-v-weighted-integer-l2-transfer-candidate-ai-refereed) | Weighted integer transfer; candidate, AI-refereed | Exceptional dyadic density bounded by Haar zero-set mass; POS ⇒ almost-all. |
| PF-N-005 | PROVED NEGATIVE STRUCTURAL THEOREM (candidate) | [C22 23-root necessary condition](../analysis/triage_wave_2026_11_14/README.md) | eventual-power model; candidate, AI-refereed; finite budgets machine-checked | A finite zero requires >=23 distinct inert p>3 with p² dividing q and joint base-3/base-5 Wieferich congruences. |
| PF-C-001 | ACCEPTED CONDITIONAL IMPLICATION (candidate; synthesis not separately refereed) | [Conditional almost-all synthesis](../analysis/triage_wave_2026_11_14/README.md) | almost-all only; LP open | If at most 22 joint inert Wieferich primes exist, A2 + V + C22 imply #{n <= X : R(n)=0} = o(X); every-n untouched. |

## ACP wave 2026-11-16 (candidate results)

AI-derived and machine-checked only; no human review. These entries do not
establish LP, do not upgrade the frozen ledger, and leave A303656
**UNRESOLVED**. Producer statements and labels:
[ACP package](../analysis/acp_wave2_2026_11_16/README.md); route summary:
[almost-all handoff](ALMOST_ALL_ROUTE_HANDOFF.md).

| ID | Classification | Name | Scope | Route effect |
|---|---|---|---|---|
| PF-P-003 | PROVED (candidate) | ACP existence-level equivalence (Lemmas L1, L2, Proposition P1) | Eventual-power model; inert primes treated as joint-nonregular ("pretend" model) | A finite zero exists iff some admissible parity class is covered by inert fibres; (N) ⇒ LP without C21's (H1)/(H2). |
| PF-P-004 | PROVED (candidate) | Exact-tiling structure (Lemma L4, Theorem F) | Fresh M-primary fibres; cosets of μ_M in F_p | An exact tiling by M traces forces M parallel lines of one type; the M = t frontier is not a structural obstruction. |
| PF-P-005 | PROVED (candidate; finite computation) | No covering below H_p = 16384 (Theorem A); pure-model 147-fibre bound (Theorem R, Q = ∅) | Pretend model; complete catalogue H_p < 32768 | Every covering needs ≥ 147 fibres and a prime with H_p ≥ 16384. |
| PF-C-002 | ACCEPTED CONDITIONAL IMPLICATION (candidate) | Theorem R(146), general case | Conditional on C21 (H1) rigidity and (H2) regular averaging; finite budgets machine-checked (class-11 margin ≈ 1.07e-3) | A finite zero needs ≥ 147 joint-nonregular primes (Haar-only conservative version: 30). The PF-C-001 hypothesis weakens from 22 to 146 (synthesis, not separately refereed). |
| PF-N-006 | PROVED NEGATIVE STRUCTURAL THEOREM (candidate) | Measure-method horizon (Proposition H) | Any measure, union bound or LP dual on fibre events | Fractional coverings exist once all inert primes up to 473899 are allowed: threshold-raising cannot reach LP; (N) needs an integrality argument. |
