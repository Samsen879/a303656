# K4 survivor-incidence and coverage-adjusted audit

Date: 2026-07-13 (Asia/Shanghai)

Classification: **INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION ON THE
ALREADY VALIDATED 1,285-POINT PANEL; GLOBAL PROBLEM UNRESOLVED**

Source commit E: `7123d08d4060e30a0e89f7d9b04f799414f00335`

Source parent: `406677c3b095d2125a4a439c76b3a8d6788cb1da`

Results commit F: the commit containing this document and
`analysis/k4_survivor_incidence/metadata.json`. Metadata uses
`RESULT_COMMIT_CONTAINING_THIS_FILE`; the fresh-F replay resolves that sentinel
to the exact checked-out commit and requires E to be its direct parent.

## Scope and claim boundary

Only the previously validated panel was evaluated:

`n = 240000005594 + h + k*28227969`,

with `h in {-720,-360,0,360,720}` and every integer `-128 <= k <= 128`.
This is exactly 257 points per class and 1,285 unique integers, all in the
committed activation cell `[183968950234,246731069451]` with the same 407
active exponent pairs. No new integer, remaining progression point, alternate
class, changed prime, higher prime power, CRT system, or residue optimization
was evaluated.

The global A303656 problem remains **UNRESOLVED**. The ranks and rates below
are finite descriptive facts about this fixed panel, not statistical-
significance, causal, necessity, or global claims.

## Canonical exponent-pair order and packed format

The verifier independently regenerated the active domain in lexicographic
`(c,d)` order. `pair_order.csv` has 407 data rows and SHA256

`5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b`.

Duplicate shift 28 occurs at pair indices 19 and 51, corresponding to `(1,2)`
and `(3,0)`. Every other shift is unique.

Each mask file is exactly 106,719 bytes: a 64-byte little-endian header and
1,285 fixed 83-byte rows. A row contains `n`, `h`, `k`, active-pair count, `T`,
and 51 mask bytes. Bit `i` is the least-significant-bit-first bit for canonical
pair index `i`; the sole unused high bit must be zero. The reader rejects wrong
magic/version/width/count/hash/order, truncation, extra bytes, and popcount/T
mismatch. The complete layout is in `mask_manifest.json`.

## Backend identities and full equality

| Backend | Classification core | Core binary SHA256 | Mask SHA256 |
|---|---|---|---|
| A | generated prime table, deterministic uint64 trial division, Fermat two-square classification | `e7f7ddd9c43df63250997847ffba63355bf9f00a915175f26ebb097650f33123` | `cc71d841d9909d3d4f30826fccfe840455b1fac7c40a550e8e034deffb054b33` |
| B | deterministic uint64 MR7, deterministic-seeded Brent Pollard-Rho, independent factor map and Fermat classification | `f7532c2a05734451daf9113b2f7a59257ee6803e66e29a68766ec3e6c340c685` | `cc71d841d9909d3d4f30826fccfe840455b1fac7c40a550e8e034deffb054b33` |
| Direct oracle | factorization-free monotone two-square boundary enumeration, canonical least-a witnesses | `f9def5bb344cc51516970930ecb2fca010d147a6e55f1948989c6deab59cd7bf` | not applicable |

The two wrappers do not classify remainders. Backend A streams the unchanged
trial-division core's numeric diagnostic rows into positional bits. Backend B
independently builds a per-point `(c,d)` outcome map from the unchanged
MR/Pollard-Rho core and then projects that map onto the canonical order. No
factorization, valuation, classification, diagnostic parser, or mask loop is
shared between the wrappers.

All 1,285 rows agree in `n`, `h`, `k`, active-pair count, exact `T`, and every
one of the 407 bits. Both complete binary files are byte-identical. Every row
satisfies `popcount(mask)=T`, and the complete T vector matches the committed
K4 pilot.

## Direct-oracle verification

The unchanged factorization-free direct oracle was rebuilt from source and run
on the predeclared 73-point panel. Its complete winner list at every point is
identical to both masks. The verifier independently rechecked all 2,448
reported witnesses, including exponent identity, exact shift and remainder,
`0 <= a <= b`, and `a^2+b^2+3^c+5^d=n`. Fresh output also matches the committed
direct-oracle artifact after excluding only elapsed-time fields.

## Persistent-covered and uncovered sets

The verifier reconstructed every class's `C_h` directly from the four
`p^2` residue conditions, compared the exact pair lists to the committed K4
artifact, and checked every mask row. No pair in any `C_h` ever wins.

| h | `|C_h|` | `|U_h|` | covered winner incidences |
|---:|---:|---:|---:|
| -720 | 214 | 193 | 0 |
| -360 | 182 | 225 | 0 |
| 0 | 216 | 191 | 0 |
| +360 | 198 | 209 | 0 |
| +720 | 209 | 198 | 0 |

## Class-level residual survival

The residual rate is total winner incidences divided by `257*|U_h|`.

| h | winner incidences | possible uncovered incidences | residual rate | never | `>=10%` | `>=25%` | `>=50%` | `>=75%` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -720 | 12,298 | 49,601 | 0.247938549626015604524102336646 | 0 | 193 | 102 | 0 | 0 |
| -360 | 14,030 | 57,825 | 0.242628620838737570255079982706 | 0 | 225 | 100 | 0 | 0 |
| 0 | 11,976 | 49,087 | 0.243974983193106117709373153788 | 0 | 191 | 90 | 0 | 0 |
| +360 | 13,490 | 53,713 | 0.251149628581535196321188539087 | 0 | 209 | 121 | 0 | 0 |
| +720 | 12,582 | 50,886 | 0.247258577997877608772550406792 | 0 | 198 | 95 | 0 | 0 |

For the target with `k=0` removed, incidences are 11,960 of 48,896 and the
rate is `1495/6112 = 0.244600785340314136125654450262`; 96 pairs meet 25%,
none meet 50%, and no target-uncovered pair never wins. Exact per-pair counts,
first/last winning k, longest run, and frequency histograms are in
`class_pair_frequencies.csv` and `metadata.json`.

## Pairwise common-uncovered comparisons

For each control, `I_h = E \ (C_0 union C_h)`. These comparisons never include
a pair guaranteed forbidden in one class but not the other.

| control h | `|I_h|` | target mean / median | control mean / median | mean difference | matched negative / zero / positive |
|---:|---:|---:|---:|---:|---:|
| -720 | 132 | 32.1867704280 / 32 | 32.6926070039 / 32 | -130/257 = -0.5058365759 | 124 / 18 / 115 |
| -360 | 161 | 38.8210116732 / 38 | 39.1167315175 / 39 | -76/257 = -0.2957198444 | 122 / 16 / 119 |
| +360 | 144 | 35.5175097276 / 35 | 36.2529182879 / 35 | -189/257 = -0.7354085603 | 139 / 16 / 102 |
| +720 | 137 | 33.4863813230 / 33 | 33.9416342412 / 34 | -117/257 = -0.4552529183 | 140 / 16 / 101 |

The target mean is lower for all four controls and negative matched
differences outnumber positive ones for all four. The restricted-count median
is lower for controls -360 and +720, but tied for -720 and +360. Under the
declared strict criterion requiring lower mean and lower median, the answer to
“lower on every `I_h`” is therefore **no**. Leaving out `k=0` preserves the
same pattern: all four means remain lower, the same two medians are tied, and
negative differences still outnumber positive differences.

Every individual k row and both all-k and leave-anchor-out exact summaries are
in `pairwise_common_uncovered.json`.

## Five-way common-uncovered comparison

`I_all = E \ union_h C_h` contains 46 pairs. The fixed thresholds
`restricted_T <= 10,20,30,40` were declared in source before result
inspection.

| h | mean | median | population SD | min and argmin k | q10 / q25 / q50 / q75 / q90 | counts `<=10/20/30/40` |
|---:|---:|---:|---:|---|---|---|
| -720 | 11.4980544747 | 12 | 3.7718231548 | 2 at -48 | 7 / 9 / 12 / 14 / 16 | 100 / 253 / 257 / 257 |
| -360 | 11.4513618677 | 12 | 3.7797546002 | 3 at -122,-88 | 6 / 9 / 12 / 14 / 16 | 97 / 256 / 257 / 257 |
| 0 | 11.2762645914 | 11 | 4.0796473173 | 3 at -34,32,38,73,110 | 6 / 8 / 11 / 14 / 17 | 109 / 255 / 257 / 257 |
| +360 | 11.7821011673 | 12 | 3.8723793274 | 2 at 22 | 7 / 9 / 12 / 14 / 17 | 100 / 253 / 257 / 257 |
| +720 | 11.6070038911 | 12 | 3.9061496925 | 1 at -56 | 6 / 9 / 12 / 14 / 17 | 100 / 255 / 257 / 257 |

Without the anchor, the target mean is 11.3046875, median 11, population SD
4.0621318944, and minimum 3 at the same five nonzero k values. The target mean
and median remain lower than every control with and without the anchor. Thus
the answer to “lower on `I_all`” is **yes** on this fixed panel.

## Hard-survivor sets

Within target `U_0`:

- `NEVER_WIN_TARGET`: 0 pairs;
- `SOMETIMES_WIN_TARGET`: 191 pairs;
- `FREQUENT_WIN_TARGET` (`>=25%`): 90 pairs;
- `VERY_FREQUENT_WIN_TARGET` (`>=50%`): 0 pairs.

The largest target survival count is 79/257 = 0.3073929961 for pair index 225,
`(c,d)=(13,4)`, shift 1,594,948. The next counts are 75/257 for indices 87,
221, and 280. There is no small near-universal hard core: survival is broad,
all 191 target-uncovered pairs win at least once, 90 reach 25%, and none reach
50%. `hard_survivor_pairs.json` records every target-uncovered pair, its
control statuses, `I_all` membership, and shift residues modulo each `p^2`.

## Cross-class pair profiles

All 407 canonical pairs have complete five-class counts, four-control mean,
target excess/deficit, persistent-covered flags, and three deterministic
rankings in `cross_class_pair_profiles.csv`.

The largest target excess is pair 225 `(13,4)`: target frequency
0.3073929961 versus mean control frequency 0.0651750973, excess
0.2422178988. It is persistently covered in three controls, so this raw rank
is not a common-uncovered comparison. The leading target deficits are pairs
that are persistently covered in the target; the coverage flags prevent those
ranks from being misread as secondary suppression. Ranks are descriptive, not
mathematical necessity.

## Coverage-adjusted interpretation

The raw target mean minus the mean of the four control means is
`-1124/257 = -4.37354085603112840466926070039`. On `I_all`, the corresponding
gap is only `-317/1028 = -0.308365758754863813229571984436`, a 92.9492882562%
reduction in absolute magnitude. Therefore the raw enrichment is explained
primarily by guaranteed P4 coverage under the predeclared 50% gap-reduction
rule.

There is still a lower target mean on every pairwise `I_h`, and the target is
lower in both mean and median on `I_all`. But two pairwise restricted medians
tie rather than fall below their controls. The fixed-panel evidence for a
secondary residue effect is therefore not uniform across the primary
pairwise comparisons.

Allowed coverage-adjusted conclusion:

> **MIXED / INCONCLUSIVE FINITE RESULT**

## Negative tests

All 14 required mutations reject with return code 2: changed ordering, changed
order hash, one flipped bit, row deletion, duplicated row, extra bytes,
truncated mask, incorrect popcount/T, class relabeling, point reordering,
persistent-covered winner, swapped backend identity, source-commit mismatch,
and baseline-hash mismatch. The persistent-covered mutation is specifically
rejected at `h=-720,k=-128` by the semantic covered-set guard.

## Provenance, resources, bugs, and risks

Fresh-E authoritative run:

- runner wall: 35.285073 s;
- children maximum RSS: 169,928 KiB;
- builds A/B/direct: RC 0/0/0;
- wrappers A/B: RC 0/0, 4.885564 s / 5.681134 s;
- direct oracle: RC 0, 19.463003 s;
- negative harness: RC 0 with 14 expected RC-2 cases;
- independent verifier: RC 0.

Raw diagnostics and logs stayed under `/tmp`; none are committed. The compact
artifact directory is about 1.1 MiB and contains no expanded 1,285-by-407 CSV
matrix.

Protected hashes are unchanged before and after: the 86-file baseline manifest
SHA256 is `4660e3e9c0757cc4c13ead7e683f84f17b00ef1e5c25fbdf25397d93f6153cb2`;
the 10-file prior-K4 manifest SHA256 is
`91a70d8ecc09792e23115d72351bf94c11646e6391a984a238d9b4429376f2b9`.

One format bug was discovered fail-closed: the first source attempt supplied a
7-byte magic to an 8-byte field, so `struct` NUL-padded it and the reader
rejected the header. It was replaced with explicit 8-byte ASCII `K4SMASK1`, E
was amended, and all authoritative outputs were regenerated from a new fresh
checkout. A separate initial replay command used an incorrectly expanded E
SHA and failed before any evaluation. Neither failed attempt contributed a
mathematical result. The fresh-F verifier path also initially treated the
already committed `verification_report.json` as an unexpected artifact; the
final source verifier instead accepts that one declared report, regenerates it
deterministically, canonicalizes its unavoidable commit-self-reference, and
requires byte equality with the committed copy.

Unresolved risks are conventional compiler/runtime/software trust, the shared
mathematical specification, the finite preselected panel, and direct-oracle
coverage limited to the declared 73 points. These do not change the exact
finite acceptance result, but they prevent global or significance claims.

## Conclusion

**VALIDATED K4 SURVIVOR-INCIDENCE AUDIT**
