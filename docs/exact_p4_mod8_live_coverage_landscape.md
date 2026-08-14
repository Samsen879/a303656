# Exact P4 mod-8-live coverage landscape

State date: 2026-07-15 (Asia/Shanghai)

Source commit U: `ee5bef63b02277786fe9c01ae9ff44233d889883`

Results commit V: the commit containing this document.

## Scope and conclusion

This audit is an **EXACT FINITE COMPUTATION** over the fixed prime set
`P4={3,7,11,23}` and only the CRT classes satisfying
`n congruent 240000005594 congruent 34 (mod 40)`, hence `n congruent 2
(mod 8)`.  It does not extend to historical panels with another residue
modulo 40 or to all integers.

Validation conclusion:

> **VALIDATED EXACT P4 MOD-8-LIVE COVERAGE LANDSCAPE**

Interpretation label:

> **MOD-8-LIVE COVERAGE STRICTLY IMPROVES THE KNOWN P4 LANDSCAPE**

The global A303656 problem remains **UNRESOLVED**.  No integer was evaluated,
and no T backend, factorization backend, direct two-square oracle, fifth-prime
input, empirical weight, or post-hoc score was used.

## Domain and mod-8 theorem

The authenticated activation cell is
`[183968950234,246731069451]`.  Exact activation inequalities give the
lexicographic `24*17=408` rectangle with only `(23,16)` excluded, leaving 407
ordered exponent pairs.  The equal shift 28 retains `(1,2)` and `(3,0)` as
two separate pairs.

For `n congruent 2 (mod 8)`, odd `c`, and even `d`,

`n - 3^c - 5^d congruent 2 - 3 - 1 congruent 6 (mod 8)`.

The quadratic residues modulo 8 are `{0,1,4}`, so sums of two squares have
residues `{0,1,2,4,5}` and never 6.  Direct parity enumeration, the closed
rectangle count `12*9-1`, and a literal residue table independently give
`|D8|=107`; therefore `|A8|=300`.  Ordered indices and mask digests are in
`results/authorities.json`.

## Authenticated baseline reconstruction

| mask | raw G | covered D8 | H8 | residual live | union with D8 |
|---|---:|---:|---:|---:|---:|
| CAL-227 | 227 | 28 | 199 | 101 | 306 |
| CAL-216 | 216 | 27 | 189 | 111 | 296 |
| G=231 common | 231 | 47 | 184 | 116 | 291 |
| CAL-230 | 230 | 47 | 183 | 117 | 290 |

All masks were reconstructed from exact prime-square persistence and matched
the authenticated frozen mask bytes.  The 60 G=231 exposed NEVER-WIN pairs
reconstructed from `pair_frequencies.csv` are exactly `D8` intersected with
the 176-pair exposed set.

## Full landscape

Both independent enumerators processed all `9*49*121*529 = 28,227,969`
tuples exactly once.

| quantity | exact value |
|---|---:|
| H8 minimum / maximum | 32 / 201 |
| global argmax tuple count | 468 |
| distinct maximizing full-mask count | 21 |
| first global argmax | `(2,13,50,5)` |
| t3=2 minimum / maximum | 153 / 201 |
| t3=2 argmax tuple count | 468 |
| first t3=2 argmax | `(2,13,50,5)` |
| distinct full masks with H8 >= 199 | 570 |

The ordered full H8 stream digest is
`7730d43abd177fe6e0ad77b20bfc3b7af860aed67b29c405f7ac061f5ec24fca`;
the t3=2 digest is
`42036cf645042f57ea02813133e6e53640663a3dc1d8ad265580d9427a86b6ab`.
The complete histogram, including its exact sum, is in `results/landscape.json`.
Among maximizers, raw G ranges over `{225,226,227,228,229}` and covered-dead
counts range over `{24,25,26,27,28}`.

`results/top_band_masks.json` reports every one of the 570 distinct full masks
with digest, bytes, H8, raw G, dead coverage, residual live count, tuple
multiplicity, first tuple, remaining-live c/d distributions, four baseline
symmetric differences, and class/integer freshness totals.

## Freshness and promotion feasibility

Every tuple defines a CRT class modulo `L4=1,129,118,760`.  Class freshness
is kept separate from integer freshness.  The complete prior registry remains
the authenticated 28 inclusive interval components plus 6,129 sparse points.

For the 21 maximizing masks, all 468 generating classes are new as designed
P4/P5 classes.  They contain 26,018 activation-cell members: 673 were already
evaluated and 25,345 remain fresh.  Each class has 55 or 56 activation-cell
members and 53--55 fresh members after registry exclusion.

For the full top band, 8,001 generating classes split into 90 previously
designed and 7,911 fresh classes.  They contain 11,561 previously evaluated
and 433,155 fresh integers.  Exact per-class CRT residues, counts, fresh
minimum/maximum, member digests, and fresh-member digests are in
`results/class_freshness_manifest.csv`.

All 21 maximizing masks are new relative to the 13 frozen base masks.
A T-blind balanced panel is feasible: across all 21 new maximizing masks the
equal-classes-per-mask bound is 4; choosing the best two masks permits 84
classes per mask, and the best-two equal-integers-per-mask bound is 4,550.
Thus the stated future-panel promotion gate is satisfied for design
consideration only.  No T census is authorized or performed by this result.

## Verification and artifacts

Enumerator A used 407-bit masks followed by A8 intersection.  Enumerator B
independently indexed only the 300 live pairs, constructed live-only masks,
and separately reconstructed dead/full masks.  Their pointwise canonical
stream digests, histograms, extrema, argmax sets, constrained slice, and all
top-band full masks agree.

All 25 required corruption cases returned nonzero.  Raw stdout, stderr,
return codes, certificates, and timings are outside Git in
`/home/samsen/code/a303656/archive/p4_mod8_live_landscape_raw_ee5bef6.tar.zst`
(SHA256 `3b3110a7bb74279405e352ed5b26a285ecbd8fa6deb21152095f6e32e497cca9`);
the compact command and hash manifests are committed under
`analysis/p4_mod8_live_landscape/results/`.
