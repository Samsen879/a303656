# Exact fixed-P4 residue landscape

Date: 2026-07-14 (Asia/Shanghai)

Classification: **INDEPENDENTLY REPRODUCED EXACT FINITE COMBINATORIAL
OPTIMIZATION; GLOBAL A303656 PROBLEM UNRESOLVED**

Source commit G: `653e6fb3591d3ada44a69decdbd9e22f1c15e856`

Source parent: `b76d097081ac2b5704bbd234e3eaf25ba9564502`

Results commit H: the commit containing this document and
`analysis/p4_residue_landscape/metadata.json`. The metadata uses the sentinel
`RESULT_COMMIT_CONTAINING_THIS_FILE`; fresh-H replay resolves it to the exact
checked-out commit and requires G to be its direct parent.

## Scope and claim boundary

This task optimizes only

`G(t3,t7,t11,t23) = |C(3,t3) union C(7,t7) union C(11,t11) union C(23,t23)|`

over the fixed square residue moduli `9,49,121,529`. It did not evaluate
`T(n)`, run a two-square executable, scan an arithmetic progression, add or
replace a prime, optimize a new prime set, or launch a CRT candidate search.
CRT work below is exact reconstruction and activation-cell counting for the
already reported maximizing tuples only; no reconstructed integer was
evaluated.

The independently regenerated domain is the same 407 lexicographically
ordered exponent pairs throughout `[183968950234,246731069451]`. The two
pairs `(1,2)` and `(3,0)` with duplicate shift 28 remain separate. The fixed
modulus is

`M4 = 9*49*121*529 = 28227969`.

## Independent enumerators

Enumerator A constructs every exact-one set residue-centrically as packed
407-bit masks and uses direct four-level lexicographic enumeration. Enumerator
B constructs masks pair-centrically by adding the `p-1` nonzero `p`-lifts for
each pair and prime, builds `(t3,t7)` and `(t11,t23)` partial unions, and
crosses them in canonical order. The implementations share no coverage or
enumeration helper.

Both enumerators produced exactly the same results:

| Landscape | tuples | minimum | maximum | argmax count | stream SHA256 | argmax SHA256 |
|---|---:|---:|---:|---:|---|---|
| Full P4 | 28,227,969 | 57 | 231 | 156 | `19c546957f7c5ef82ecfd552edf5a31b1f33fdc86397a0b92a38a4aca40d608c` | `81734726245a8bf936118126f22486ae03d032af4bee732a19a07106db8bc711` |
| `t3=2` | 3,136,441 | 171 | 231 | 84 | `fd409acfc3f35aa8e333d654a94f5d06c3093f6c5ffd3207adadfe64ed12310c` | `f83d2400cd684dbcc5027d82dcd0d053fdf64521a770b12231cdc259adade825` |

The exact histograms are `full_histogram.csv` and `t3eq2_histogram.csv`.
The first 100 maximizing tuples, rather than a 28-million-row table, are in
`maximizers.json`.

## Canonical byte stream

Every full-stream row is exactly 10 bytes:

`struct <5H: t3,t7,t11,t23,G`.

All five fields are unsigned 16-bit little-endian integers. Rows are in
lexicographic tuple order with `t23` varying fastest. There is no header,
trailer, or platform padding. The final row count is 28,227,969. The `t3=2`
digest uses the same row format and induced order for 3,136,441 rows.

Argmax digests concatenate only the four unsigned 16-bit little-endian tuple
coordinates, eight bytes per maximizing tuple, in lexicographic order; `G` is
not included.

## n0 rank and local landscape

The committed anchor reconstructs as

`n0=240000005594`, tuple `(2,41,74,504)`, `G=216`.

| Landscape | `G>216` | `G=216` | `G<216` | descending rank interval | exact midrank percentile | gap to max | maximizer? |
|---|---:|---:|---:|---:|---:|---:|---|
| Full | 463,150 | 134,605 | 27,630,214 | 463,151–597,755 | `923250550/9409323` percent | 15 | no |
| `t3=2` | 244,123 | 54,713 | 2,837,605 | 244,124–298,836 | `286496150/3136441` percent | 15 | no |

The percentile is defined exactly as
`100*(count below + count equal/2)/total`; it is a midrank descriptive
percentile, not a probability.

Exact local optima are:

| Allowed change | maximum | gain | argmax count | lexicographically first |
|---|---:|---:|---:|---|
| Exactly one coordinate | 227 | 11 | 6 | `(2,41,50,504)` |
| At most two coordinates | 230 | 14 | 4 | `(2,7,32,504)` |
| `t3=2`, other coordinates arbitrary | 231 | 15 | 84 | `(2,7,50,17)` |

`local_landscape.json` records the first 100 modifications and the exact
newly covered and lost exponent pairs for each.

## Subset optima

All 15 nonempty subsets were optimized exactly. `coverage/bit` is descriptive
only; it is not the mathematical objective.

| primes | modulus | bits | digits | maximum | argmax count | coverage/bit | first residues | cell points |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 3 | 9 | 4 | 1 | 143 | 1 | 143/4 | 2 | 6,973,568,802 |
| 7 | 49 | 6 | 2 | 62 | 1 | 62/6 | 7 | 1,280,859,576 |
| 3,7 | 441 | 9 | 3 | 185 | 1 | 185/9 | 2,7 | 142,317,730 |
| 11 | 121 | 7 | 3 | 55 | 5 | 55/7 | 50 | 518,695,201 |
| 3,11 | 1,089 | 11 | 4 | 183 | 6 | 183/11 | 2,50 | 57,632,800 |
| 7,11 | 5,929 | 13 | 4 | 109 | 8 | 109/13 | 7,50 | 10,585,616 |
| 3,7,11 | 53,361 | 16 | 5 | 219 | 6 | 219/16 | 2,7,50 | 1,176,180 |
| 23 | 529 | 10 | 3 | 22 | 8 | 22/10 | 11 | 118,642,948 |
| 3,23 | 4,761 | 13 | 4 | 159 | 11 | 159/13 | 2,11 | 13,182,550 |
| 7,23 | 25,921 | 15 | 5 | 83 | 10 | 83/15 | 7,75 | 2,421,285 |
| 3,7,23 | 233,289 | 18 | 6 | 198 | 64 | 198/18 | 1,7,23 | 269,032 |
| 11,23 | 64,009 | 16 | 5 | 75 | 45 | 75/16 | 50,37 | 980,520 |
| 3,11,23 | 576,081 | 20 | 6 | 196 | 222 | 196/20 | 2,50,17 | 108,947 |
| 7,11,23 | 3,136,441 | 22 | 7 | 128 | 80 | 128/22 | 7,50,75 | 20,010 |
| 3,7,11,23 | 28,227,969 | 25 | 8 | 231 | 156 | 231/25 | 1,7,50,14 | 2,224 |

The point count in the final column is for the lexicographically first
maximizing CRT class inside the fixed activation cell.

## CRT reconstruction and covered-pair comparison

The first global maximizer `(1,7,50,14)` gives
`r=17359678 (mod 28227969)`, has 2,224 cell members, and its nearest cell
member to n0 is `240011552116`.

The first `t3=2` maximizer `(2,7,50,17)` gives `r=22292606 (mod M4)`.
After imposing `n=n0 (mod 40)`, it gives
`361028234 (mod 1129118760)`, has 56 cell members, and its nearest cell member
to n0 is `239734205354`.

For the lexicographically first global, constrained, one-coordinate, and
at-most-two-coordinate maxima, the `(intersection,new,lost,symmetric
difference)` counts relative to n0 are respectively:

- global: `(89,142,127,269)`;
- constrained: `(161,70,55,125)`;
- one coordinate: `(194,33,22,55)`;
- at most two coordinates: `(169,61,47,108)`.

The complete pair lists and distributions by c and d are in
`coverage_comparison.json`. Both duplicate-shift-28 pairs are retained and
have matching covered/uncovered status in each tuple. Newly covered pairs are
guaranteed only for the corresponding CRT class and are not called permanent
obstructions elsewhere.

## Verification, resources, and provenance

The independent Python verifier regenerates all 407 pairs and all 708 residue
coverage sets, checks exact-one semantics and a valuation-3 exclusion witness,
rechecks selected coverages, histograms, argmax tuples/digests, n0, all subset
optima, CRT/count arithmetic, and every committed artifact hash. The negative
suite has 18 tests and rejects every required stream mutation, altered
histogram/argmax/n0, and valuation-3 inclusion.

Authoritative fresh-G resources:

- coverage generation: A 0.001563252 s / 3,456 KiB peak-to-date; B
  0.001579 s / 3,456 KiB;
- Enumerator A full: 2.13272919 s / 3,456 KiB; constrained slice
  0.243828154 s / 3,456 KiB; subsets 0.617818915 s / 3,456 KiB;
- Enumerator B MITM construction: 0.00298 s / 6,912 KiB; integrated full and
  constrained slice 1.540606 s / 6,912 KiB; subsets 0.106132 s / 6,912 KiB;
- independent verifier: 3.95 s / 34,504 KiB;
- complete fresh-G runner: 18.88 s / 213,344 KiB, exit 0. The peak is the
  compiler; the enumeration processes are much smaller.

All builds, tests, enumerators, verifier, artifact verifier, and self-check
returned 0. The single external raw archive is
`fixed_p4_residue_landscape_raw_653e6fb3591d.tar.zst`, SHA256
`07f56be0b8fce72c494c6db7dd47ae2389a4320080027b771fd84690499b9c9f`,
53,125 bytes, with 40 regular files totaling 167,703 raw bytes.

Protected input and certified-baseline files remain byte-identical; their
individual hashes are recorded in `metadata.json`.

## Discovered bugs and unresolved risks

The first fresh-G attempt passed mathematically but created an untracked
Python bytecode cache. It was discarded, the runner was changed to disable
bytecode writes, G was amended, and the authoritative fresh checkout remained
clean. During smoke integration, raw equality of descriptive wording between
the A/B certificates was also too strict; the verifier now compares exact
mathematical fields while independently enforcing both serialization
contracts. Neither issue changed a mathematical result.

LeakSanitizer cannot run under the environment's ptrace restrictions; both
enumerators nevertheless passed ASAN/UBSAN with leak detection disabled.
Remaining risks are conventional compiler/runtime/software trust and the
shared mathematical specification. This is a finite residue optimization, not
a proof or counterexample for the global problem.

## Conclusion

**VALIDATED EXACT FIXED-P4 RESIDUE LANDSCAPE**
