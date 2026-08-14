# Current mathematical and computational state

State date: 2026-07-15 (Asia/Shanghai)

Task: **EXACT P4 MOD-8-LIVE COVERAGE LANDSCAPE AUDIT**

Source commit U: `ee5bef63b02277786fe9c01ae9ff44233d889883`

Results commit V: the commit containing this document.

## Mathematical status

The global A303656 problem remains **UNRESOLVED**.  No proof or certified
counterexample is claimed.

Validation conclusion:

> **VALIDATED EXACT P4 MOD-8-LIVE COVERAGE LANDSCAPE**

Interpretation label:

> **MOD-8-LIVE COVERAGE STRICTLY IMPROVES THE KNOWN P4 LANDSCAPE**

This label applies only to fixed-P4 CRT classes with `n congruent 34 mod 40`.

## Exact findings

- The authenticated 407-pair domain partitions into `|D8|=107` and
  `|A8|=300`; duplicate shift pairs `(1,2)` and `(3,0)` remain distinct.
- Three independent counts and a standalone residue proof certify that every
  D8 pair leaves residue 6 modulo 8, impossible for two squares.
- CAL-227, CAL-216, G=231 common, and CAL-230 reconstruct to H8 values 199,
  189, 184, and 183 respectively.
- Both independent enumerators exhaust all 28,227,969 tuples.  H8 ranges from
  32 to 201; 468 tuples maximize it, with first tuple `(2,13,50,5)`.
- There are 21 distinct maximizing full masks and 570 distinct full masks in
  the H8>=199 top band.  The t3=2 maximum is also 201 with 468 argmax tuples.
- All 468 maximizing classes are class-level fresh and retain 25,345 fresh
  activation-cell integers after excluding the complete prior registry.
- All 21 maximizing masks are new relative to the frozen 13-mask authority;
  a balanced future panel is feasible without viewing T.  This is feasibility
  only and does not authorize an integer census.
- No integer T evaluation, factorization, direct oracle, empirical score,
  fifth-prime input, or P5/P6 search occurred.  All 25 corruption mutations
  were rejected.

Machine-readable artifacts are under
`analysis/p4_mod8_live_landscape/results/`; the full report is
`docs/exact_p4_mod8_live_coverage_landscape.md`.
