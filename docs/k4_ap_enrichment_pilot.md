# K4 arithmetic-progression enrichment pilot

Date: 2026-07-13 (Asia/Shanghai)

Classification: **INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION; GLOBAL
PROBLEM UNRESOLVED**

Source commit C: `44bb1f9996dab4a71a9249e1f4b12111f5bb1beb`

Source parent: `2f87e5fa431eb96166eed57809013dee84b492d2`

Results commit D: the commit containing this document and
`analysis/k4_ap_pilot/metadata.json`.  A Git commit cannot contain its own hash,
so metadata uses `RESULT_COMMIT_CONTAINING_THIS_FILE`; fresh replay resolves
that sentinel to the exact checked-out D and verifies that C is its direct
parent.

## Scope and outcome

This pilot evaluated only

`n(h,k) = 240000005594 + h + k*28227969`

for `h in {-720,-360,0,360,720}` and every integer `-128 <= k <= 128`.
That is 257 points per class and exactly 1,285 unique integers.  No CRT system,
adaptive point, alternate residue, higher prime power, neighboring-class scan,
or complete-cell scan was used.

The two independent factorization backends agree on all 1,285 exact `T`
values.  A factorization-free direct oracle verifies all 73 required deduplicated
points and all 2,448 winner records and canonical witnesses at those points.
The leave-anchor-out comparisons retain the target's lower empirical T
distribution and higher empirical lower-tail frequency.  This is a finite
enrichment observation on the fixed panel, not a theorem or an independent-
sample significance test.

## Reproduced core and panel guards

- Both committed greedy orderings begin `[3,7,11,23]`.
- `P4={3,7,11,23}`, `M4=3^2*7^2*11^2*23^2=28227969`.
- `n0 mod M4=5813156`.
- The committed target P4 persistent union has exactly 216 of 407 active
  exponent pairs.  The committed four-prime stage count is reproduced rather
  than manually reselected.
- Activation cell: `[183968950234,246731069451]`.
- Panel range: `[236386824842,243613186346]`; all 1,285 points lie in the cell.
- Every point has 407 active exponent pairs and 406 distinct shifts.  Shift 28
  retains both `(c,d)=(1,2)` and `(3,0)`.
- The five residues modulo M4 are `5812436, 5812796, 5813156, 5813516,
  5813876`, all distinct.  Every control offset is zero modulo 360.

## Backend identities and equality

| Path | Independent method | Binary SHA256 | Result |
|---|---|---|---|
| A | generated prime table, deterministic uint64 trial division, explicit valuations, Fermat criterion | `f0ae6bedbb520344ad9be264eaa8c9544961fdcf67872291ffb5267c8e93c2dd` | 1,285/1,285 complete |
| B | deterministic uint64 MR7, deterministic-seeded Brent Pollard-Rho, independent factor map and Fermat criterion | `3129e92a08b6279c965f5a1d481678a4bb7952caae80f01a0029ecd97807e9cd` | 1,285/1,285 complete |
| Direct | factorization-free monotone two-square enumeration, least-a canonical witness | `20cf88690a6829a8c16ff0987b399e58d8302ae8bd9950c69f21478cc5a5310a` | 73/73 points complete |

Backend A and B count files have the same SHA256,
`dad853ae1b385ef44ef67b442d5b3b82c78614a4fc99c77530ba6903ede49e23`.
The independent pointwise comparison has 1,285 rows and zero mismatches in
`n`, `h`, `k`, `T`, or active-pair count.

## Exact class summaries

Quantiles below use the inverse empirical CDF, `x_(ceil(p*n))`; no
interpolation is used.  The q-vector order is
`1%,5%,10%,25%,50%,75%,90%,95%,99%`.  Exact per-class histograms are in
`analysis/k4_ap_pilot/class_summaries.json`.

| Class | Points | Min and all argmins `(k,n)` | Max | Mean | Population SD | Median | q-vector |
|---|---:|---|---:|---:|---:|---:|---|
| target, anchor included | 257 | 16 at `(0,240000005594)` | 75 | 46.5992217898832684824902723735 | 12.372575397324616806278181910714630301154548961359 | 46 | 23,27,30,38,46,55,64,67,74 |
| target, anchor removed | 256 | 22 at `(-96,237290120570)` | 75 | 46.71875 | 12.247727786716195628692064066970045373337029353884 | 46 | 24,27,30,38,46,55,64,67,74 |
| control -720 | 257 | 19 at `(-34,239040253928)` | 78 | 47.8521400778210116731517509728 | 12.694614398227218896559021953334567750488833298315 | 46 | 25,28,31,38,46,58,66,69,75 |
| control -360 | 257 | 27 at `(78,242201786816)` | 92 | 54.5914396887159533073929961089 | 13.063166080396739664902400404278789035993838195632 | 55 | 29,34,37,46,55,64,74,77,81 |
| control +360 | 257 | 24 at `(-32,239096710946)` and `(38,241072668776)` | 81 | 52.4902723735408560311284046693 | 13.633077433760790922653886378592930380071431222385 | 52 | 25,30,34,43,52,62,72,76,80 |
| control +720 | 257 | 16 at `(88,242484067586)` | 76 | 48.9571984435797665369649805447 | 12.588137393841205548486397115962180444480967086300 | 48 | 24,29,32,40,48,57,67,70,75 |

Threshold entries are exact `count/point_count` proportions in order
`T<=16,18,20,25,30`:

| Class | Exact counts and proportions |
|---|---|
| target, anchor included | `1/257, 1/257, 1/257, 11/257, 29/257` |
| target, anchor removed | `0/256, 0/256, 0/256, 10/256, 28/256` |
| control -720 | `0/257, 0/257, 1/257, 5/257, 22/257` |
| control -360 | `0/257, 0/257, 0/257, 0/257, 6/257` |
| control +360 | `0/257, 0/257, 0/257, 3/257, 15/257` |
| control +720 | `1/257, 1/257, 1/257, 5/257, 18/257` |

Anchor removal eliminates the already-known `T=16` target point, but it does
not eliminate the target's lower-tail excess at `T<=25` or `T<=30` versus any
individual control in this fixed panel.

## Matched-k comparison

| Aggregate | Points | Mean target minus control median | Median | Negative / zero / positive | Unique / tied minima | Below all four | Below at least three | Longest negative run |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchor included | 257 | -2265/514 = -4.40661478599221789883268482490 | -5 | 199 / 2 / 56 | 81 / 16 | 81 | 159 | 20 |
| anchor removed | 256 | -2219/512 = -4.333984375 | -5 | 198 / 2 / 56 | 80 / 16 | 80 | 158 | 20 |

The complete matched rows, including all four control values, control median,
range, target rank, and flags, are in
`analysis/k4_ap_pilot/matched_k_comparison.csv`.

## Persistent core by residue class

These are p-squared persistent sets, independently reconstructed for each
class; they are not static-odd-valuation relabels.  Each listed guaranteed set
is constant for all 257 k values in its class.

| h | residues mod `(9,49,121,529)` | persistent covered | covered current losers at k=0 | uncovered | per-prime `(3,7,11,23)` | multiplicity histogram |
|---:|---|---:|---:|---:|---|---|
| -720 | `(2,7,80,313)` | 214 | 214 | 193 | `(143,62,35,19)` | `1:174,2:36,3:3,4:1` |
| -360 | `(2,24,77,144)` | 182 | 182 | 225 | `(143,52,0,20)` | `1:150,2:31,3:1` |
| 0 | `(2,41,74,504)` | 216 | 216 | 191 | `(143,48,47,20)` | `1:180,2:31,3:4,4:1` |
| +360 | `(2,9,71,335)` | 198 | 198 | 209 | `(143,50,26,16)` | `1:163,2:33,3:2` |
| +720 | `(2,26,68,166)` | 209 | 209 | 198 | `(143,46,43,19)` | `1:170,2:36,3:3` |

All six pairwise prime intersections and every multiply covered exponent pair
are recorded in `analysis/k4_ap_pilot/persistent_core_by_class.json`.

## Direct verification and negative tests

The direct panel contains the 55 fixed-k class points, every class argmin (six
points because class +360 has two argmins), every one of the 24 formal points
with `T<=25`, and n0, deduplicated to 73.  It processed all 407 pairs at each
point.  Exact T, complete winner lists, least-a witnesses, `a<=b`, and every
equation `a^2+b^2+3^c+5^d=n` pass.  The two source pairs for duplicate shift 28
remain distinct.

The unmodified artifact set passes with RC 0.  All 19 declared negative tests
return RC 2: duplicated n, omitted point, altered h, altered k, outside-cell
point, incorrect active-pair count, swapped backend identities, tampered T,
altered P4, altered M4, target/control relabel, source mismatch, binary
replacement, and malformed/overflow input for all three executables.  Parser
fixtures are rejected before output and therefore evaluate no off-panel T.

## Resource, archive, and provenance record

- Formal runner: 20.57 s wall, 25,720 KiB maximum RSS.
- Backend A: 2.17 s wall, 4,188 KiB maximum RSS.
- Backend B: 1.75 s wall, 4,096 KiB maximum RSS.
- Direct oracle: 16.48 s wall, 4,224 KiB maximum RSS.
- Largest build: backend B, 1.95 s wall and 170,696 KiB maximum RSS.
- Negative suite: 1.33 s wall, 25,600 KiB maximum RSS.
- Raw archive: `~/code/a303656/archive/k4_ap_pilot_44bb1f9996dab4a7_raw_20260713.tar.gz`,
  1,285,085 bytes, SHA256
  `88406fc6e596e7674a6329d1eb96c8be0a11b3870fc5bdada3cb1226607105c0`.
- Protected prior baseline/pilot manifest before and after:
  `4660e3e9c0757cc4c13ead7e683f84f17b00ef1e5c25fbdf25397d93f6153cb2`,
  86 files, zero mismatches.

The archive contains build/run time records, stdout/stderr, both panel inputs,
raw direct results, negative fixtures and return codes, environment data, and
the authoritative command/RC manifest.  Git contains only compact results and
the archive name/hash.

Two implementation defects were found fail-closed before the authoritative
run: strict compilation rejected a raw `__int128` spelling, and an abandoned
source attempt retained an extra `T` field while writing the direct CSV.  Both
were fixed, the latter gained a regression test, source commit C was rebuilt,
and every committed result was generated from a new checkout of corrected C.
The discarded attempt used only the same fixed panel and is retained in the
external archive.  No mathematical result was selected from it.

Remaining risks are ordinary implementation/compiler/runtime trust, shared
mathematical specification, and the intentionally tiny non-random five-class
panel.  The factorization backends share only input/output schema and CLI
shape, but all paths are conventional software, not formally verified.

## Command and return-code summary

| Command stage | RC |
|---|---:|
| initial `git rev-parse HEAD` | 0 |
| first strict direct build (raw `__int128`, intentionally retained failure) | 1 |
| corrected strict A/B/direct builds | 0 / 0 / 0 |
| implementation IDs, direct self-test, Python compile, runner regression | 0 / 0 / 0 / 0 |
| abandoned pre-C-final runner (direct CSV defect) | 1 |
| corrected source commit C and fresh worktree | 0 / 0 |
| authoritative 1,285-point runner | 0 |
| independent C verifier | 0 |
| negative-test harness | 0, containing one valid RC 0 and 19 expected RC 2 cases |
| external archive creation/copy/hash check | 0 / 0 / 0 |

Exact expanded commands, paths, and return codes are in the archive's
`command_manifest.json`; fresh-D build/replay commands and their return codes
are reported at handoff because D does not exist until this document is
committed.

## Conclusion

**VALIDATED K4 ARITHMETIC-PROGRESSION ENRICHMENT PILOT**
