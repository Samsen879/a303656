# Exact computation specification

## Frozen objective

Test canonical support-to-guard equality; same-state idempotent reuse; exact minimal slice-cover elimination; private original providers; shared-origin prefix-LCA constraints; the k−1 support-growth charge; support-profile potential monotonicity; and all-enabled-original-subledger projection. Test failures of raw macro counts/masses, support deletion, unit-capacity packing, and submodularity. Recheck named actual arithmetic motifs without treating them as complete certificates.

## Complexity and benchmark

For n proper top events, build subset slice-unions by a 2^n table, then test minimality by removing each member. Upper work is O(n 2^n) plus lower-guard intersections. An explicit n≤18 hard gate prevents accidental large enumerations. The largest named ledger has m=15 rows; all 2^m enabled-origin subsets are compared at every state. Seeded fixtures have m≤7 and domains at most 3^2×5×7=315 points.

The first p=3 duplicated-frontier fixture is run and timed before the rest. The saved measurements in `run_metrics.json` are descriptive; no future runtime promise and no coverage decision depends on them.

## Named ABSTRACT fixtures

- Duplicate singleton supply, p=3,5,7: two original tokens per first digit.
- Nested exact partitions on 3×5 and 3×5×7.
- All 15 cells of 3×5 as pairwise-disjoint original rows.
- The source seven-leaf ternary depth-three frontier.
- A ternary beta-two dynamic outside-center bundle plus its three center cells.

Original masks and primitive log shadows are frozen and explicitly exported. All abstract state tokens have the value `frozen`; no per-branch state selection is performed. One separate negative-control test contrasts three frozen one-row states with the invalid independently-reselected branch relaxation.

112 seeded triangular systems, seed 20260906, cover m=1,...,7 with 16 cases each. The first coordinate alternates beta=1,2. At most one original dynamic bundle per coordinate is permitted. These are abstract normal-form tests; a dynamic label 5 in these fixtures is not an admitted arithmetic prime row.

## Private-provider triangle enumeration

For supports ab, bc, ac, exhaust every triple of whole/proper primitive p-cylinders on (p,beta)=(3,1),(3,2),(5,1),(7,1). Intersect the appropriate pairs, then ask whether all three resulting proper nonempty slices constitute an inclusion-minimal full cover. Total assignments 2989; no valid frontier.

## Exact actual arithmetic

Trial-division primality, exact multiplicative-order reduction and lifting valuation for 14 declared primes. Three K=2,E={1} 67/20771 state pairs are checked by modular powers over U=L=228470, for two anchors and two rows: 2741640 row-anchor-exponent comparisons.

For 1645333507 and its declared dependency primes, only exact prime/order/lifting arithmetic is performed. No enormous full-period enumeration, no prime scan, no claim of actual nonlinear recurrence.

## Independence and reproducibility boundaries

The direct point-mask projection checker does not use the cover-clause enumeration to decide truth. Both routines are nevertheless in one standalone implementation by the same producer; they are not independent authors or fully independent software stacks. The mathematical theorems are proved in the report, not inferred from finite test success.

`verify.py` performs a fresh isolated replay and compares deterministic result bytes. Runtime measurements are explicitly excluded from replay equality.
