# Exact t3=2 fixed-P4 maximizer-class census

State date: 2026-07-14 (Asia/Shanghai)

Classification: **EXACT FINITE COMPUTATION**. The global A303656 problem
remains **UNRESOLVED**. No proof or counterexample is claimed.

Source commit I: `6d197965cdcf27f3abe1aa370e5132b9804f053a`

Source parent: `ae75d96358f9803cfac2c7d6ce46dfec0344e6b7`

Results commit J: the commit containing this document. A fresh-J replay must
resolve this sentinel and require I to be its direct parent.

## Fixed scope and panel

The computation used only `P4=[3,7,11,23]`, `M4=28,227,969`, activation cell
`[183968950234,246731069451]`, and the 407 active exponent pairs. It loaded the
84 committed, distinct, lexicographically ordered `t3=2` maximizers, checked
coverage 231 for each, and reproduced their digest
`f83d2400cd684dbcc5027d82dcd0d053fdf64521a770b12231cdc259adade825`.
It added exactly the three declared calibrations at G=216, 227, and 230.

The common condition is `n = 240000005594 (mod 40)`, equivalently residue 34
modulo 40. CRT with each fixed-P4 tuple gives one class modulo
`L=1,129,118,760`. All 87 residues are distinct. The exact ordered panel has:

- 87 classes: 3 calibrations followed by 84 maximizers;
- 4,838 unique points, all in the activation cell and in their declared class;
- 53 classes with 56 points and 34 classes with 55 points;
- minimum panel member 183,974,482,874 and maximum 246,727,600,994;
- SHA256 `3d4b2675df302b518ec5c32f7d63573604efbfee4143e6db16d4da80819af679`.

No formal integer outside this panel was evaluated. No prime, residue tuple,
interval, class, or adaptive continuation was added.

## Exact backends and direct oracle

Backend A used the deterministic trial-division/Fermat core
`k4_ap_backend_a_trial_division_v1` through the positional-stream adapter
`p4_census_backend_a_stream_adapter_v1`. Backend B used the deterministic
MR7/Brent Pollard-Rho/Fermat core
`k4_ap_backend_b_cpp17_mr7_brent_rho_v1` through the keyed-projection adapter
`p4_census_backend_b_keyed_adapter_v1`.

Both processed all 4,838 points and all 407 exponent pairs per point. They
agreed pointwise on every T value and every mask bit. Every packed mask has 407
bits, every popcount equals T, both exponent pairs producing shift 28 remain
separate, and no persistently covered pair is a winner. The packed-mask hashes
are:

- A: `dbed9a87ff10bbe14dc8df8eb46d2c91b73e2a2708ad09bbf4bd40551d0dfcc4`;
- B: `b013d3857a3cb92d409851413cd6b8e23f85c0923bad9d9a2bdbc93a181ce6bf`.

The factorization-free direct oracle selected the exact deduplicated declared
panel: every class minimum; every point with T at most 20 (including the
previously known threshold 16); first, median, and last in every class; each
calibration member nearest n0; and the nearest member of every maximizing
class. It checked 457 complete masks and 13,971 canonical least-a witnesses.
All checks passed. No T=0 point occurred.

## Calibration and coverage response

| Level | Points | Uncovered | Minimum | Mean | Median | Residual survival |
|---|---:|---:|---:|---:|---:|---:|
| CAL-216 `(2,41,74,504)` | 55 | 191 | 16 | 30.4545454545 | 30 | 0.1594478820 |
| CAL-227 `(2,41,50,504)` | 56 | 180 | 18 | 27.1607142857 | 27 | 0.1508928571 |
| CAL-230 `(2,7,32,504)` | 56 | 177 | 26 | 33.7142857143 | 33 | 0.1904761905 |
| G=231, all 84 classes | 4,671 | 176 | 15 | 33.3303361165 | 33 | 0.1893769098 |
| G=231, lexicographically first | 56 | 176 | 20 | 33.7500000000 | 34 | 0.1917613636 |

Relative to CAL-216, the aggregate G=231 mean-T reduction is
`-147761/51381 = -2.8757906619`: the sign is negative because the maximizing
aggregate mean is about 2.876 higher, not lower. Dividing by the 15 additional
covered pairs gives `-147761/770715 = -0.1917193775` per newly covered pair.
The adjacent observed reductions per new covered pair are 0.2994391972 from
216 to 227, -2.1845238095 from 227 to 230, and 0.3839495978 from 230 to the
G=231 aggregate. These four fixed levels do not identify a causal response.

## Aggregate G=231 census

There are 4,671 points across the 84 maximizing classes. The unique global
minimum is T=15 at:

`MAX-038`, tuple `(2,7,72,362)`, class point index 11,
`n=196653638594`.

This is a finite near-counterexample observation, not a counterexample. The
exact histogram is:

```text
15:1  18:1  19:1  20:9  21:12  22:19  23:51  24:65  25:74
26:117  27:192  28:223  29:298  30:326  31:331  32:368
33:353  34:369  35:320  36:318  37:282  38:230  39:203
40:139  41:111  42:89  43:64  44:45  45:25  46:21  47:9
48:3  49:1  50:1
```

The class-minimum distribution is
`15:1, 18:1, 20:9, 21:10, 22:13, 23:27, 24:14, 25:7, 26:1, 27:1`.
The numbers of classes whose minimum is at most 10, 12, 14, 16, 18, and 20
are respectively `0,0,0,1,2,11`. One class contains a point below the known
T=16 value.

Class means range from 32.2678571429 (`MAX-028`) to 34.4464285714
(`MAX-068`). Residual survival rates range from 0.1833400974 (`MAX-028`) to
0.1957183442 (`MAX-068`). Thus different CRT progressions produce visibly
different finite distributions even though their guaranteed covered set is
the same.

## Common uncovered core

All 84 maximizing tuples produce the same 231-bit persistent-covered mask,
with SHA256 `4f06ade9cb4e7612cdf690ea5c0b71173802073e9210979b474d00335f9d5c35`.
Consequently:

- `|I_84|=176`;
- 231 pairs are covered by at least one maximizer;
- the same 231 pairs are covered by all 84 maximizers;
- each pair's maximizer coverage count is therefore either 0 or 84;
- T_common equals T for every G=231 formal point, so its histogram is exactly
  the aggregate histogram above.

The full per-pair coverage counts and the explicit covered/uncovered index
sets are in `common_uncovered.json`.

## Winner frequencies

Among the 176 exposed pairs, 60 never win, 116 win on at least 10% of their
4,671 exposures, 103 win on at least 25%, and none wins on at least 50%.
Every exposed pair has exposure count 4,671 because all maximizers share one
covered mask. The five highest empirical frequencies are:

| Pair index | `(c,d)` | Shift | Winners/exposures | Frequency |
|---:|---:|---:|---:|---:|
| 402 | (23,11) | 94,192,006,952 | 1919/4671 | 0.4108327981 |
| 192 | (11,5) | 180,272 | 1914/4671 | 0.4097623635 |
| 62 | (3,11) | 48,828,152 | 1911/4671 | 0.4091201028 |
| 368 | (21,11) | 10,509,181,328 | 1898/4671 | 0.4063369728 |
| 130 | (7,11) | 48,830,312 | 1896/4671 | 0.4059087990 |

These are finite empirical observations. `pair_frequencies.csv` reports every
pair's exposure count, winner count, empirical frequency, persistent class
count, classes with a win, and maximum within-class frequency.

## Predeclared stopping interpretation

1. Yes, one G=231 point has T below 16: the T=15 point above.
2. No G=231 point has T=0.
3. The aggregate G=231 mean does not improve over CAL-216; it is about 2.876
   higher.
4. No. There is no aggregate mean improvement for the 15 extra guaranteed
   obstructions to explain, and the four observed levels are nonmonotone.
5. Yes. A common hard residual core of 176 pairs remains; in fact all 84
   maximizers have the same fixed covered set.
6. Yes at the finite class level: class means span about 2.179 and class minima
   span 15 through 27, despite identical persistent coverage.

Interpretation label:

> **FIXED-P4 MAXIMIZATION PRODUCES A STRICTLY LOWER FINITE T MINIMUM**

## Verification, provenance, and limits

The independent verifier reconstructed the panel, exact-one persistent sets,
all class summaries, aggregate summaries, common-uncovered analysis, winner
frequencies, direct selection, and every declared artifact hash. Eighteen
negative mutations each returned code 2, covering missing/extra classes,
changed tuple/G/CRT/order, missing/duplicate/out-of-cell/noncongruent points,
mask and popcount faults, persistent-covered winners, backend swap, source and
baseline mismatches, and truncated/extra mask bytes.

The authoritative fresh-I runner returned 0 in 34.718097 seconds. Backend A
used 9.301219 wall seconds; Backend B used 13.575400; the 32-thread direct
oracle used 10.281313. Recorded maximum child RSS was 236,928 KiB. The raw
archive is external at
`~/code/a303656/archive/p4_maximizer_census_raw_6d197965cdcf.tar.zst`, has 41
members, size 52,450,684 bytes, and SHA256
`b7979b3ba4ad33818b47994caa87bcb56aecc99b7a46848f4218c9caaac71ad0`.

One implementation defect was found before the authoritative run: the packed
mask reader initially rejected valid final-byte bits 1 through 6 instead of
only the unused high bit. That failed run was discarded and evaluated no point
outside the fixed panel; the check was corrected, regression-tested, and source
commit I was amended before the authoritative fresh-I run. Remaining limits are conventional source,
compiler, operating-system, exact-arithmetic implementation, SHA256, and
archive-retention trust. The computation is bounded and says nothing by itself
about integers outside the fixed panel.

## Exact validation conclusion

**VALIDATED T3=2 FIXED-P4 MAXIMIZER-CLASS CENSUS**
