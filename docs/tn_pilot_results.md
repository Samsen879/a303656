# Bounded T(n) pilot results

Run date: 2026-07-13 (Asia/Shanghai)

Conclusion: **BOUNDED T(n) PILOT VALIDATED**

This conclusion validates the exact counting architecture on two fixed finite
intervals. It is not a broad campaign, not a proof of the A303656 statement,
not a counterexample claim, and not an extension or regeneration of the
certified baseline.

## Authority and source

- required starting commit:
  `5fe0ee472cdefa7a23a05616a56a024fe571e58a`;
- clean acceptance source commit:
  `2e38ac0a55cc8765f8e29e6ef4f1ec215ff8e9f9`;
- source archive SHA256:
  `35ca33cb104d8d3d40ca3cbb2e84c34312dff529bcaf55504e1fa193350d943e`;
- source clone: `/tmp/a303656_tn_acceptance_src_2e38ac0`, detached and
  clean before and after the runs;
- build directory: `/tmp/a303656_tn_acceptance_build_2e38ac0`.

Every formal role provenance derives its commit using `git rev-parse HEAD`,
queries its executable with `--implementation-id`, and records
`formal_acceptance_eligible=true`. No caller-provided source commit or
implementation name exists in the runner interface.

## Exact finite intervals and result

| ID | Half-open interval | Rows | Minimum T | Complete argmin set | T=0 | T=1 | T=2 | T=3 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| PILOT-A | `[2,200002)` | 200,000 | 1 | `2, 3, 5, 25` | 0 | 4 | 8 | 44 |
| PILOT-B | `[240000000001,240000100001)` | 100,000 | 16 | `240000005594` | 0 | 0 | 0 | 0 |

No other formal integer was scanned. The total pilot width is exactly 300,000.
No `T(n)=0` occurred, so the candidate-escalation branch was not triggered.

The three byte-identical count-array hashes are:

```text
PILOT-A counts.csv  cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d
PILOT-B counts.csv  2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773
```

The active source-pair range is 1 through 95 in PILOT-A and exactly 407
throughout PILOT-B. Exact histograms are retained in each `summary.json` and
can be reconstructed from each `counts.csv`.

## Three-way exact comparison

The compared implementation identities are:

| Role | implementation_id | Executable SHA256 |
|---|---|---|
| bitset-derived | `tn_bitset_annulus_v1` | `f460da0967aa1cc5b29b3b2b6e0d1900c231ff9b1f3356deb1aa747b2df5a914` |
| clean-annulus-derived | `tn_clean_annulus_v1` | `a6d18bfa3094a0406d9ca9d999e96c2b598496a9232e23a656ab2c9110f0bddf` |
| GMP oracle | `tn_gmp_uv_oracle_v1` | `9063c35d07215030cba7182c52fae30ad6ab94fdc0005e1a6a0114ca76f1665c` |

For each interval the verifier required byte-identical `counts.csv` files,
then parsed and compared all rows again. It independently checked the exact
header, contiguous row set, histogram, minimum, full argmin set, `T=0/1/2/3`
counts, active-pair range, summary hashes, required low-T selection, complete
winner list length, duplicate source keys, source powers and shift, remainder,
`a<=b`, equation fields, and minimum-a canonicality. Both verifier commands and
both subsequent audit-only provenance commands returned 0.

The implementation-specific `low_t.jsonl` hashes differ only because each row
binds its own implementation identity; normalized mathematical records were
equal:

| Interval/role | Path | SHA256 | Records |
|---|---|---|---:|
| A/bitset | `output/tn_pilot_20260713/pilot_a/bitset/low_t.jsonl` | `2ebc2093122f650ee3e2f8c8db1f08395b190cfe40137ba7dd2a6869b4f8eb2e` | 56 |
| A/clean | `output/tn_pilot_20260713/pilot_a/clean/low_t.jsonl` | `25ee4e9365f665da8139ed778a6696787af560cdaf725892918bc7f96e81bf15` | 56 |
| A/oracle | `output/tn_pilot_20260713/pilot_a/oracle/low_t.jsonl` | `d75128ccacbe23e8fca8f73b6f1b9396a7e615f0e879ae8a7e180d9811b9e35a` | 56 |
| B/bitset | `output/tn_pilot_20260713/pilot_b/bitset/low_t.jsonl` | `059865af7709da2592b2e23fbfa83c419a04d62c894360d81760298d8707fc51` | 1 |
| B/clean | `output/tn_pilot_20260713/pilot_b/clean/low_t.jsonl` | `26852a6ded24d69b962ea3490f1bc293c7aeec3a858d4218747ca4dfb869a950` | 1 |
| B/oracle | `output/tn_pilot_20260713/pilot_b/oracle/low_t.jsonl` | `0854f0a06901fe89fe0f0cdbaf13d383bbbcc81b7d051f014b41e94fa2f74a2e` | 1 |

Each role directory also contains `metadata.json`, `summary.json`,
`provenance.json`, `verifier_report.json`, `backend_stdout.log`,
`backend_stderr.log`, `backend_return_code.txt`, and
`backend_elapsed_seconds.txt`.

## Definition-specific positive tests

The optimized and ASan/UBSan property runs both returned 0 and checked:

- distinct source pairs `(1,2)` and `(3,0)` have the same shift 28 and remain
  two winner records;
- remainder 25 has representations `(0,5)` and `(3,4)`, but source `(0,0)`
  contributes once at n=27 with canonical `(0,5)`;
- remainder zero contributes with `(0,0)`;
- selected activation thresholds pass at `s-1`, `s`, and `s+1`;
- n=10 has exact `T=4`, demonstrating no first-hit or saturation;
- all 98 fixture rows and normalized winner records agree among all three
  implementations.

The inherited independent GMP boundary suite was rebuilt from the same clean
source and also returned 0. It covers per-n marked sets, endpoints, annuli,
integer square-root neighbors, activation, uint64 parsing/arithmetic/overflow,
and the injected multiplicity seam.

## Expected-rejection tests

The negative harness itself returned 0 only after observing every required
rejection:

| Mutation | Expected result observed | Diagnostic summary |
|---|---|---|
| caller `--source-commit deadbeef` | rc 2 | unrecognized runner argument |
| bitset/clean slot swap | rc 1 | implementation manifest relabel/slot mismatch |
| implementation manifest relabel | rc 1 | implementation manifest relabel/slot mismatch |
| append forged count row | rc 1 | output tamper/hash mismatch: `counts.csv` |
| replace recorded bitset executable | rc 1 | executable SHA256/binary replacement mismatch |

Raw stdout, stderr, and return-code files are retained under
`output/tn_pilot_20260713/negative_tests/provenance_expected_rejections`.

## Fresh-build dependency provenance

Environment: Ubuntu 24.04.4 LTS on WSL2 x86-64, GCC 13.3.0, Python 3.12.3.
The locally extracted dependency was:

```text
archive: /tmp/libgmp-dev_2%3a6.3.0+dfsg-2ubuntu6_amd64.deb
SHA256: ffadf91b116cc2647ef213742ac1cbe80f450af14413c146df6e200f8c3c9a1a
extraction: /tmp/a303656_gmp_tn_20260713
include: /tmp/a303656_gmp_tn_20260713/usr/include
architecture include: /tmp/a303656_gmp_tn_20260713/usr/include/x86_64-linux-gnu
library: /tmp/a303656_gmp_tn_20260713/usr/lib/x86_64-linux-gnu
GMP runtime: 6.3.0
```

Exact optimized compile/link commands are preserved in command records
`066_build_bitset_acceptance`, `067_build_clean_acceptance`, and
`068_build_oracle_acceptance`. The oracle link uses the extracted static
`libgmpxx.a` and `libgmp.a`; `ldd` and `readelf` records are in commands 074 and
075. Sanitizer compile commands are records 077 through 079.

Formal outer resource measurements were:

| Command | `/usr/bin/time -v` elapsed | Max RSS KiB | rc |
|---|---:|---:|---:|
| PILOT-A bitset | 0.10 s | 19,796 | 0 |
| PILOT-A clean | 0.10 s | 19,712 | 0 |
| PILOT-A GMP oracle | 0.41 s | 19,612 | 0 |
| PILOT-A verifier | 1.74 s | 42,728 | 0 |
| PILOT-B bitset | 2.99 s | 19,564 | 0 |
| PILOT-B clean | 9.83 s | 19,444 | 0 |
| PILOT-B GMP oracle | 29.51 s | 19,336 | 0 |
| PILOT-B verifier | 3.54 s | 33,192 | 0 |

The role-local runner additionally records backend `perf_counter` elapsed
values. One WSL2 `/usr/bin/time` field for the fast negative harness was
malformed (`0:-3.80`); its rc and all mutation-specific rc/log files are intact.
No formal pilot elapsed field was malformed, and no cap was reached.

## Baseline integrity and exclusions

The five baseline hashes recorded in `docs/current_state.md` are identical
before and after; comparison command 104 returned 0. No certificate, existing
formal output, or official campaign log was modified. No full1p6b, interval
extension, CRT search, residue-class mining, or broad campaign ran.

Every metadata file states:

```text
obstruction_data_status: NOT_COLLECTED_IN_TN_PILOT
```

No losing-pair factorization or obstruction claim is made.

## Raw command evidence

Every build/test/formal command driven for acceptance has a dedicated directory
under `logs/tn_pilot_20260713` containing `command.txt`, `stdout.log`,
`stderr.log`, `return_code.txt`, and `time.txt`. Records 001--051 cover initial
authority, implementation pretests, fixtures, and sanitizer checks. Records
052--128 cover the source commit, fresh clone/dependency/build, inherited and
new positive tests, both fixed pilots, three-way verification, provenance
negative tests, baseline comparison, environment, argmin extraction, artifact
hashes, final provenance replay, JSON validation, and document whitespace
checks. The final records also confirm that every earlier log directory has all
five raw files, all 36 required role artifacts exist, and all six backend return
codes are zero.

Record 125 deliberately applied the generic whitespace checker to the raw-log
tree and returned 2 because raw CRLF source captures and shell command records
contain preserved trailing bytes. The scoped content check in record 128
excludes immutable raw logs, checks all staged documentation and pilot outputs,
and returns 0.

Two non-acceptance command-construction mistakes are retained, not hidden:
record 057 used a mistyped checkout SHA and returned 128 before corrected record
058; records 102/103 passed three operands to two-file `cmp` and returned 2
before correct pairwise comparisons 105--108 returned 0. Record 047 is a
diagnostic `git diff --no-index` whose rc 1 means “files differ,” not a failed
whitespace check. No formal build, pilot, verifier, positive test, negative-test
harness, or baseline-integrity command failed.
