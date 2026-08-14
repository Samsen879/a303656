# Weighted fixed-P4 transferability audit

Date: 2026-07-14 (Asia/Shanghai)

Classification: **EXACT FINITE COMPUTATION WITH EMPIRICAL PANEL WEIGHTS**.
The global A303656 problem remains **UNRESOLVED**.

Source commit K: `196413213fa832e55ce83a6d128e1b0a3b9fafda`

Results commit L: the commit containing this document and the compact
`analysis/p4_weighted_transferability/results/` artifact set.

## Scope

The audit reads only the existing 4,838-point fixed-P4 census and the already
validated 407-pair residue landscape. It does not evaluate a new integer,
change the activation cell, add a prime, enlarge the exponent domain, or
select a class adaptively. Empirical weighted scores are not proofs.

## Provenance repairs

The backend mask files have different complete SHA256 values:

- A: `dbed9a87ff10bbe14dc8df8eb46d2c91b73e2a2708ad09bbf4bd40551d0dfcc4`;
- B: `b013d3857a3cb92d409851413cd6b8e23f85c0923bad9d9a2bdbc93a181ce6bf`.

Their 128-byte headers contain different backend slots and adapter identity
digests. Removing the whole header from each file leaves identical ordered
51-byte mask payloads, SHA256
`8a32a0d4b7842f10836c66287d0fb05124397357b2737ded64b7ff02f6be8d1b`.
Decoding every mask to one byte per bit in point-major/pair-major order gives
the common SHA256
`c58c28586fcbf222e2c06a771b1b19123a208f023ebdac77e8d02763e9710dfd`.

`direct_oracle_selection_manifest.json` freezes all 457 previously selected
points and their reasons. It independently confirms all 87-class minima and
tied argmins, every declared low-T point and representative, and the T=15
point `n=196653638594`. No weighted result feeds into this manifest.

## Exact folds and weights

ODD contains MAX-001, MAX-003, ..., MAX-083; EVEN contains MAX-002,
MAX-004, ..., MAX-084. Each has 42 classes, with 2,334 and 2,337 points.
The pool has all 4,671 G=231 points. `exact_weight_table.csv` stores the three
winner numerators and denominators for every one of the 407 exponent pairs,
plus class prevalence. `frequency_analysis.json` stores exact rankings,
per-pair fold differences, requested top-k overlaps, and exact L1 difference.

## Complete weighted landscape

Both independent programs enumerate all

`9*49*121*529 = 28,227,969`

tuples, with no G restriction. Enumerator A is residue-centric and accumulates
only set bits. Enumerator B is pair-centric, builds nonzero lifts and partial
unions, and scans all 407 pair positions when accumulating scores. They agree
on ordered digest, maxima, argmax counts/firsts/digests, constrained results,
target scores/ranks, and top distinct masks.

| weights | maximum | argmax tuples | lex-first tuple | G |
|---|---:|---:|---|---:|
| ODD | `57979/2334` | 140 | `(1,9,21,21)` | 219 |
| EVEN | `58181/2337` | 140 | `(1,9,21,21)` | 219 |
| POOL | `116160/4671` | 140 | `(1,9,21,21)` | 219 |

All three rows share the same coverage mask. The exact cross-fold regrets are
zero and each opposite-fold rank is 1.

For `t3=2`, all three objectives again share one mask: lex-first tuple
`(2,13,32,13)`, G=222, 68 argmax tuples, with maxima `33238/2334`,
`33272/2337`, and `66510/4671`.

The existing G=231 common mask has weighted numerator zero for each fold,
because its 231 persistently covered pairs never win in the G=231 panel from
which the weights are defined. Relative to that mask, the weighted optimum
adds 134 pair identities and loses 146. Exact lists and CAL-216/227/230 ranks
are in `transfer_report.json`.

The weighted optimum has 86 covered pairs with nonzero pooled weight. Its top
8, 16, and 32 pooled contributions have exact score shares `1381/10560`,
`28601/116160`, and `3107/7260`. Fold ordering is reported without qualitative
extrapolation: exact Spearman rho is `1398223/1404557`, exact L1 difference is
`799559/909093`, and top-k overlaps are stored for k=16,32,64,96,116.

## Frozen future artifact

The union of the top eight distinct masks under each objective plus CAL-216,
CAL-227, CAL-230, and one G=231 common-mask representative deduplicates to 12
masks. `candidate_manifest.json` uses the lexicographically first `t3=2`
representative when one exists and explicitly records absence for eight masks.
No integer belonging to these possible future classes was evaluated.

All 12 negative mutations were rejected with return code 2. Protected
baseline hashes are unchanged. Raw command output remains external; compact
return-code metadata is committed.

## Validation conclusion

**VALIDATED WEIGHTED FIXED-P4 TRANSFERABILITY AUDIT**
