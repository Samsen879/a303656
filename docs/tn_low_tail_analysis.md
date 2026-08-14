# Read-only low-tail analysis of the validated T(n) pilot

Task: **READ-ONLY LOW-TAIL ANALYSIS OF VALIDATED T(n) PILOT**

Starting commit: `73fbec48fb1343de9e6fa7cf2bcc84e86837955b`

Conclusion: **VALIDATED READ-ONLY LOW-TAIL ANALYSIS**

## Scope and classification

Every statistic in this report comes from the already committed, three-way
validated 300,000 rows:

- PILOT-A: `[2,200002)`, 200,000 rows;
- PILOT-B: `[240000000001,240000100001)`, 100,000 rows.

No counting executable was invoked. No new integer, interval, continuation,
CRT class, residue class, or factorization campaign was examined. Existing
pilot outputs and certified baseline artifacts were not rewritten.

All findings below are **finite computational observations**. They are not a
global theorem, necessity statement, counterexample, or authority for a broad
campaign.

## Input integrity and canonical source

The three `counts.csv` files for each interval were first checked byte for
byte. Their SHA256 values match the validated pilot report:

```text
PILOT-A  cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d
PILOT-B  2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773
```

Every low-T SHA256 matches its adjacent `summary.json`, and all three low-T
record sets become equal after removal of the implementation identity field.
Only after these checks, `bitset/counts.csv` was selected as the canonical
read-only source for each interval. The analysis metadata retains all role
hashes.

## Definitions

For sorted values `x[0] <= ... <= x[N-1]`, every reported quantile uses the
empirical inverse-CDF nearest-rank definition

```text
Q(p) = x[ceil(p*N)-1],  0 < p <= 1.
```

There is no interpolation. The reported median is `Q(0.5)`. Population
variance is

```text
(1/N) * sum_i (T_i - mean)^2.
```

Means and variances retain exact rational numerator/denominator fields;
standard deviations use a 60-digit Decimal square root and are serialized to
15 decimal places.

## Basic statistics

| Statistic | PILOT-A | PILOT-B |
|---|---:|---:|
| Rows | 200,000 | 100,000 |
| Minimum | 1 | 16 |
| Maximum | 41 | 118 |
| Mean | 18.631400000000000 | 61.102430000000000 |
| Population variance | 33.258204040000000 | 291.167038095100000 |
| Population standard deviation | 5.766992633947090 | 17.063617380119023 |
| Median | 18 | 60 |
| Distinct T levels | 40 | 98 |

Quantiles:

| p | PILOT-A | PILOT-B |
|---:|---:|---:|
| 0.1% | 5 | 24 |
| 1% | 7 | 29 |
| 5% | 10 | 35 |
| 10% | 11 | 39 |
| 25% | 14 | 47 |
| 50% | 18 | 60 |
| 75% | 23 | 76 |
| 90% | 26 | 84 |
| 95% | 28 | 88 |
| 99% | 31 | 95 |
| 99.9% | 35 | 103 |

PILOT-A and PILOT-B are at completely different numerical scales. Moreover,
the active exponent-pair count ranges from 1 to 95 in PILOT-A but is 407 for
every PILOT-B row. Raw T values therefore should not be compared as though
their opportunity denominators were equal. The available low records retain
`T/active-pair-count` explicitly.

## PILOT-A lower tail

- Minimum `T=1` occurs exactly at `n=2,3,5,25`.
- Counts at `T=1,2,3` are `4,8,44`; cumulative `T<=3` is 56 of 200,000.
- Cumulative counts are 497 at `T<=5`, 14,129 at `T<=10`, and 124,858 at
  `T<=20`.
- The four sole-winner records are:

| n | active pairs | T/active | sole `(c,d)` | shift | remainder | canonical `(a,b)` |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | `(0,0)` | 2 | 0 | `(0,0)` |
| 3 | 1 | 1 | `(0,0)` | 2 | 1 | `(0,1)` |
| 5 | 2 | 1/2 | `(1,0)` | 4 | 1 | `(0,1)` |
| 25 | 6 | 1/6 | `(1,1)` | 8 | 17 | `(1,4)` |

“Sole winner” applies only to these finite records. It does not mean the shift
or exponent pair is globally necessary.

## PILOT-B lower tail

The five smallest distinct T levels are:

| T | Total n count | Smallest n |
|---:|---:|---:|
| 16 | 1 | 240000005594 |
| 18 | 3 | 240000004802 |
| 19 | 5 | 240000044158 |
| 20 | 6 | 240000000968 |
| 21 | 23 | 240000001544 |

The complete first-25 lists are in `pilot_b_low_levels.json`. There is no row
with `T=17`. The cumulative counts at `T<=16,18,19,20,21` are respectively
`1,4,9,15,38` out of 100,000.

For the 100 fixed 1,000-wide blocks, local-minimum T values range from 16 to
26. Their frequencies are:

```text
16:1, 18:2, 19:5, 20:5, 21:16, 22:14,
23:20, 24:20, 25:11, 26:6
```

The ten fixed 10,000-wide block minima are:

```text
16, 20, 20, 21, 19, 20, 22, 19, 21, 18
```

All block boundaries are deterministic subdivisions of PILOT-B; no interval
was added.

## Global argmin neighborhood

For `n0=240000005594`, the inclusive 201-row window
`[n0-100,n0+100]` remains wholly inside PILOT-B.

- `T(n0)=16` and the point is a strict local minimum.
- It is the only `T=16` row in all of PILOT-B, so no same-value point exists on
  either side.
- The equal-value plateau containing `n0` has width 1; there is no wide
  plateau.
- Immediate deltas are `+32` on the left and `+63` on the right.
- Moving away from the argmin, the strict-increase prefix has two steps on the
  left and one on the right; neither side is globally monotone within the
  100-point half-window.
- The left/right half-window means are `59.46` and `60.51`.
- The full window mean is exactly `12013/201`, approximately
  `59.766169154228856`, which is `8797/201` or approximately
  `43.766169154228856` above the argmin.
- The window contains 65 distinct T values.

No polynomial fit or statistical model is used.

## Record lows and local minima

Strict records use `<` against all previously visited rows in the stated
direction. The first visited endpoint is always a directional record.

- PILOT-A left-to-right immediately records `n=2,T=1` and never improves.
- PILOT-B left-to-right records T values
  `52,37,29,25,23,20,18,16`, ending at the global argmin.
- PILOT-B right-to-left records
  `65,62,50,46,42,37,34,29,26,23,18,16`.
- Exact directional n values are in `record_lows.csv`.

For interior rows, strict minima use `<` on both neighbors and weak minima use
`<=`. Endpoints compare only to their one available in-interval neighbor and
are labeled explicitly. A plateau minimum is a maximal equal run of width at
least 2 that is strictly below every available boundary neighbor.

| Interval | Strict minima | Weak minima | Plateau minima | Maximum plateau width |
|---|---:|---:|---:|---:|
| PILOT-A | 62,693 | 72,207 | 4,085 | 4 |
| PILOT-B | 32,995 | 34,102 | 524 | 2 |

These high counts describe short-scale oscillation in the sampled sequence;
they do not identify mathematical obstructions.

## Existing winner-record frequencies

Only the already emitted 56 PILOT-A low records and the one PILOT-B argmin
record were used. Their winner totals are 152 and 16 respectively.

For PILOT-A, the most frequent source exponent pairs in these 56 records are:

```text
(1,1):20, (1,0):16, (3,1):11, (0,0):10, (0,1):10,
(1,3):7, (2,0):7, (3,2):6, (5,1):5, (3,3):4
```

The most frequent numerical shifts begin:

```text
8:20, 4:16, 32:11, 2:10, 6:10, 10:7, 128:7,
28:6, 52:6, 248:5
```

Exponent-pair and numerical-shift frequencies are stored separately. Shift 28
has two sources, `(1,2)` and `(3,0)`. Both source records are retained. It is a
duplicate winning numerical shift at `n=29,109,221` in the existing low-record
set.

PILOT-B contributes only its one argmin record, with 16 distinct winner
source pairs; each occurs once in that one-record sample. Calling any of them
“frequent” would therefore be misleading. At the argmin, `T/active=16/407`,
approximately `0.039312039312039`.

“Frequently occurring winner pair,” “frequently occurring winning shift,”
“rare winner,” “sole winner,” and “low-tail support pair” are permitted finite
descriptions. None implies a mathematically necessary shift outside the
recorded sample.

## Recommended future obstruction fixture panel

No factorization was run. The deterministic proposal contains nine n values:

```text
PILOT-A: 2, 3, 5, 25
PILOT-B: 240000000968, 240000001544, 240000004802,
         240000005594, 240000044158
```

Selection is mechanical:

1. all four PILOT-A global argmin rows;
2. the smallest n at each of the five smallest distinct PILOT-B T levels;
3. continue through 10,000-wide blocks only if needed until at least two block
   minima are represented.

The selected PILOT-B values already cover block 0 through the global argmin
and block 4 through `240000044158`, so no additional row is added. The panel is
a future proposal, not collected obstruction data.

## Independent verification

`tests/verify_tn_low_tail_analysis.py` does not import the main analysis
script. It independently reparses the canonical counts, recomputes exact
histograms, all quantiles, minimum/argmin, directional records, strict/weak/
plateau minima, 1k/10k block selection, and winner-frequency counters.

It reports:

```text
status: PASS
PILOT-A histogram total: 200000
PILOT-B histogram total: 100000
winner totals: PILOT-A 152, PILOT-B 16
```

The main artifacts were also generated twice in separate directories and all
16 files were byte-identical.

The fail-closed fixture harness passes one valid input and rejects missing,
duplicate, out-of-order, out-of-range, malformed, signed, noncanonical, and
bad-header rows only when the analyzer returns nonzero.

## Command and raw-log policy

`analysis/command_manifest.json` is the concise checked-in command index. Its
55 raw records include exact shell-escaped commands, return codes, elapsed
wall-clock fields, byte counts, and stdout/stderr SHA256 values. Two nonzero
records are retained rather than hidden:

- `049_no_counting_invocation_audit`, rc 1, self-matched its own command text;
- `052_final_fail_closed_tests`, rc 2, omitted the required `--python`
  harness argument.

The corrected replacements are `050_no_counting_invocation_audit_fixed` and
`053_final_fail_closed_tests_fixed`, both rc 0. Neither nonzero record is a
counting, analysis, verifier, or data-integrity failure.

The 275 raw files are not committed individually. They are packaged as
`tn_low_tail_raw_logs_73fbec48fb1343de9e6fa7cf2bcc84e86837955b.tar.zst`
under `~/code/a303656/archive/`, SHA256
`772ccc757fade39e68bf99e9f9cf3bed467f30bb43847ef44002a93667d94cff`.
The compressed size is 34,653 bytes, the summed uncompressed file size is
176,550 bytes, and the uncompressed tar stream is 419,840 bytes.
`analysis/raw_log_archive.json` records the exact creation command and archive
metadata.

## Artifacts

The `analysis/` directory contains:

- `summary_statistics.json`, `histogram.csv`, `lower_tail_cdf.csv`;
- `pilot_b_low_levels.json`;
- `pilot_b_local_minima_1k.csv`, `pilot_b_local_minima_10k.csv`;
- `pilot_b_argmin_neighborhood.csv` and `.json`;
- `record_lows.csv`, `local_minima.csv`;
- `winner_pair_frequency.csv`, `winner_shift_frequency.csv`;
- `low_record_details.json`;
- `recommended_obstruction_panel.json`;
- metadata, artifact manifest, independent verifier report, concise command
  manifest, and external raw-log archive metadata.

The obstruction status is exactly:

```text
obstruction_data_status: SCHEMA_ONLY_NOT_COLLECTED
```

Certified baseline hashes and all 18 counts/low/summary input hashes are
byte-identical before and after the analysis. Exact conclusion:
**VALIDATED READ-ONLY LOW-TAIL ANALYSIS**.
