# Frozen computation specification

Authority: Samsen879/a303656, repository ID 1333945235.
Bound main: 44e522dd6e88504e2b9829f0b27359e6c45a76ff.
Bound tree: 6a30565826c8f988bfbb85e4098b78b2992d290c.
This file is frozen before this package's arithmetic or model runs.

## Targets

1. Six monotone two-anchor demands: FALSE, BOTH, A0, A1, EITHER, TRUE.
   Exhaust every top coverage word of length 1..4 and every lower coverage
   state; compare universal elimination with the typed-demand formula.
2. Row geometry: exact modular powers, clipped valuations (local zero never
   accepted), discrete logarithm guard and rigid/dynamic classification.
   Exhaust q=3,7,11 at K=2,3 and q=3 at K=4, all residues and all nonempty
   accepted-positive-odd-valuation subsets. No prime-cutoff search.
   Additional specified rows: 67, 20771, 40487, 1645333507.
3. Exact 67/20771 SPLIT replay, K=2, E={1}, r67=2, r20771=20775,
   U=L=228470. Enumerate the full original period and retain anchor tags.
   Also inspect r20771=96315155 and r40487=25919 as paired rigid examples.
4. Paired prefix-frontier grammar: exhaustive cylinder sets on 3^2,
   and deterministic paired-configuration models on 3^2 and 3x5.
   Compare prefix contraction with direct bitset / truth enumeration.
   Abstract models will never be labeled actual arithmetic systems.
5. Assigned-blocker Kraft theorem checks: verify the exact prime/order/lifting
   data for {20771,40487,1645333507}; check the assignment to coordinates
   {5,653,3}, using full prime-power projected blockers and dynamic slack.
   Test its finite combinatorial hypotheses against exhaustive small models.
6. Optional theorem-linked depth-4 coordinate-3 gate: factor Phi_81(5) and
   Phi_162(5). Discovery may use SymPy with bounded execution. Assert a new
   resource zero only after exact product checks and recursive primality
   certificates validated by a standalone integer verifier. Incomplete
   factorization will be reported as such, never as an absence result.
7. Test explicit false implications: pooled => BOTH; forgetting shared states;
   raw macro count as prime count; the unqualified two-adic pooled no-go.

## Scope and reproducibility

All decisions use integers, exact rational numbers, finite sets, or bitsets.
No floating-point feasibility, no large prime panel, no GitHub writes.
Frozen prime signatures are authenticated by modular order tests at each
prime divisor of the claimed order. Primality is proved by trial division or
recursive Lucas certificates, not an uncertified probable-prime claim.
Repository code is not imported. These are newly written reference programs,
not a claim to have replayed the entire repository.
Deterministic outputs omit timing fields. Tests are complementary formulations
by one author, not independently authored software stacks.
