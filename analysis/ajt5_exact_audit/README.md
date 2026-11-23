# Bounded AJT5 audit, round 1

**A303656: UNRESOLVED. No general proof or new interval record.**
This is an independently implemented, explicitly authorized finite experiment
from `main` at `f6fe000b84c349f6a0f2b64dcf47db39bd799c0c`. It uses no code or
authority from unmerged PR #50. It leaves the frozen authority unchanged.

The two native replays agree entry by entry, but the supplied reference's
**second counting-gate survivor count is not reproduced**. The literal gate
leaves **2**, not 47. Enlargement stopped; this package preserves that bounded
negative comparison rather than changing the gate or assuming its answer.

## Experiment and results

For integers `n>1`, define

```text
D(n) = {d >= 0 : n - 5^d = a^2 + b^2 + 3^c, a,b,c >= 0}.
AJT5: D(m) nonempty => D(5m+r) intersects (D(m) union (D(m)+1)),
      m >= 2, 0 <= r <= 4.
```

Every `m=2..10,000,000` and all five `r` were tested: **49,999,995 cases**.
The largest child is **50,000,004**. The historical `+6` variant is outside this
experiment. All powers and bounds use exact integer arithmetic and guarded
multiplication. Both squares may be zero; residual zero is a valid sum of
two squares. Since `3^0=1`, no negative residual is admissible.

All 9,999,999 parent masks are nonempty. The failure counts below are thus
nonvacuous. Counts and minima are computed, never fed into the engines.

| Quantity, indexed by r | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Combined AJT5 failures | 0 | 0 | 0 | 0 | 0 |
| Same-branch failures | 9653 | 3 | 2 | 1612 | 1 |
| Plus-one-branch failures | 2 | 8836 | 719 | 2 | 201 |
| Minimum same-branch failure m | 5 | 3 | 2016 | 16 | 112 |
| Minimum plus-one-branch failure m | 4 | 20 | 16 | 7963079 | 5 |
| First gate survivors | 106 | 12 | 43 | 38 | 21 |
| Both literal gates' survivors | **1** | **1** | **0** | **0** | **0** |
| Supplied second-gate reference | **32** | **4** | **1** | **4** | **6** |
| Cases with exactly one directed bridge | 7 | 2 | 2 | 2 | 2 |

The reference also agrees with the two exact probes:

```text
m=1676569, r=0: D={1,3,7}, E={0,4,6}, sole bridge 3 -> 4.
m=7963079, r=3: D={0,1,2,4,6,7,8,9}, E={0,4,6}.
                No plus-one bridge; same bridges 0->0, 4->4, 6->6.
```

The second probe reproduces the previously falsified `L5,3` branch and
does not falsify AJT5. The absence of a finite combined failure is not a
uniform transfer theorem.

## Counting gates and the discrepancy

Let `L=floor(log_5(m))`, obtained by integer powers, `D=D(m)`, `E=D(5m+r)`.
Then `D` is contained in `[0,L]` and `E` in `[0,L+1]`, since
`5m+r < 5^(L+2)` for `r=0..4`. Let `k` be the number of consecutive runs of
`D`. Define signed defects

```text
delta1 = |D| + k + |E| - (L+2)
P      = (E union (E-1)) intersect [0,L]
delta2 = |D| + |P| - (L+1)
```

Here `E-1={e-1:e in E}`, including `-1` before intersection. A case survives
a gate precisely when its defect is **<=0**. The second count in this audit
is conditional on surviving the first gate.

**First gate proof.** Translating each consecutive run of `D` one step right
adds exactly one new element to `D union (D+1)`. Hence that union has size
`|D|+k` inside the universe `[0,L+1]`, of size `L+2`. If `delta1>0`, it must
intersect `E` by the pigeonhole principle. That intersection is a bridge.

**Second gate proof.** An exponent `d in [0,L]` has a possible bridge to `E`
exactly when `d in P`. Both `P` and `D` lie in a universe of size `L+1`.
If `delta2>0`, pigeonhole gives `D intersect P` nonempty, hence a bridge.

Both are sufficient counting tests. Neither asserts that actual masks always
satisfy its inequality. Nonpositive defects do not imply bridge failure, and
the two tests need not be nested. Indeed, the second gate alone leaves 89
cases over the whole scan, whereas applying it after the first leaves 2.
The abstract-mask unit test checks these implications for every pair of masks
at levels `L=0..5`, including empty masks.

The complete list surviving both literal gates is:

| m | r | L | D | E | delta1 | delta2 | Directed bridges |
| ---: | ---: | ---: | --- | --- | ---: | ---: | --- |
| 102917 | 1 | 7 | {0,4,5,6} | {0,4,8} | 0 | 0 | 0->0, 4->4 |
| 1676569 | 0 | 8 | {1,3,7} | {0,4,6} | -1 | -1 | 3->4 |

For the first row, `P={0,3,4,7}`: `4+4=8=L+1`. For the second,
`P={0,3,4,5,6}`: `3+5=8<L+1=9`. Both nevertheless have bridges.

The minimal reproducible **aggregate** discrepancy needs only the 220 rows in
[`hard_cases.csv`](results/hard_cases.csv), their exact mask certificates, and
the literal set calculation in the Python checker. A quick check prints
`gate2_rows: 2`. Both full native recounts independently give `[1,1,0,0,0]`.
There is no supplied list of the claimed 47 cases, so a particular reference
row cannot be identified as incorrect. This audit does not guess the source
of the difference or claim to have disproved a different unstated gate.

## Reproduction and verification scope

From the repository root, with Python 3.10+ and g++ supporting C++17, on Linux:

```bash
python3 src/verify_ajt5_reports.py analysis/ajt5_exact_audit/results
python3 tests/ajt5_tests.py
python3 scripts/verify_public_repository.py
python3 scripts/privacy_scan.py --reject-domain gmail.com
```

Fresh full replay, using a new output directory:

```bash
python3 scripts/run_ajt5_audit.py --work-dir reproduce_work/ajt5-fresh
```

**Expected full replay exit code: 2**, after preserving all evidence, because
the reference comparison disagrees. Native computations, complete table
comparison, and certificates must succeed first. Code 0 means all applicable
reference gates agree; code 1 indicates an error. Never treat exit 2 as a
successful reference match. Existing work directories are rejected.
`--max-m 200` runs a small replay and skips inapplicable full reference gates.
Both native engines and the wrapper reject bounds greater than 10,000,000.

1. [`ajt5_scan.cpp`](../../src/ajt5_scan.cpp) enumerates unordered square pairs
   `(a,b)` with `0<=a<=b`, marking the complete S2 support, including zero.
   It forms `T=S2+{3^c}` by immutable bitset shifts, then materializes every
   mask `D(n)` and scans all parents and children.
2. [`ajt5_valuation_replay.cpp`](../../src/ajt5_valuation_replay.cpp) uses the
   sum-of-two-squares criterion: every prime `p=3 mod 4` has even valuation.
   Its prime sieve deletes all exact odd-valuation multiples; zero remains
   valid. It tests T membership directly for each integer, builds masks in a
   different loop order, and compares **every** S2, T, and D entry with the
   first engine. It recounts defects, runs, predecessors, edges, failures and
   minima by walking individual exponents; summaries and CSVs must agree.
3. [`verify_ajt5_reports.py`](../../src/verify_ajt5_reports.py) checks all
   **418 selected complete masks** by explicit square witnesses and prime
   valuation blockers. It checks CSV arithmetic with literal Python sets,
   coverage, bounds, duplicates, hashes, source bindings and profiles. These
   selected certificates are not a third exhaustive 50-million-entry scan.
   First-failure minimality, all finite counts, and hard-list completeness
   derive from the two exhaustive replays, not the selected-mask checks.

The mutation tests reject bad witnesses, incomplete exponent coverage, missing
blockers, composite/wrong-class primes, incorrect or even valuations, residual
zero blockers, forged masks/bridges/failures, omitted or duplicate hard rows,
missing certificates, and corrupted/truncated/extended native tables. They
also compare every mask through `n=1004` with a direct small brute-force oracle
and reject malformed/out-of-campaign bounds. CI runs the quick checks only.

The two full native engines take seconds and about 120 MiB peak RSS each on
the recorded host. Exact timings, compiler, CPU, commands, return codes,
source hashes, raw-table hashes and logs are in
[`replay_receipt.json`](results/replay_receipt.json) and
[`execution_logs.json`](results/execution_logs.json). Each engine is single
threaded. These timings describe one shared Linux host, not portable speed
guarantees. Raw tables occupy 112,500,012 bytes and remain in the ignored replay
directory; only small reports and certificates are versioned.

## File formats and custody

[`manifest.json`](results/manifest.json) binds every stored results file.
It is an integrity manifest, not a digital signature or external attestation.
All results are from this new implementation; no web transcripts, credentials,
prebuilt binaries or private source artifacts are included.

* `summary.json`: exhaustive counts, minima, signed defect histograms, and
  directed-bridge-edge histogram, all indexed by `r=0..4`. Histogram counts
  include vacuous cases; failure and hard-list counts exclude them. Here there
  are no vacuous cases. Unique means one directed edge, not one source vertex.
* `hard_cases.csv`: all 220 first-gate survivors, sorted by `(m,r)`, with
  decimal masks, signed defects and same/plus bridge **source** masks.
  A plus-source bit `d` denotes `d->d+1`. `gate2_hard=1` marks the two survivors.
* `minima.csv`: the ten branch minima, with complete mask certificates.
  `failures.csv`: combined failures (header only in this experiment).
  `probes.csv`: the two explicitly supplied probes.
* `certificates.jsonl`: one JSON object per certified `n`, sorted by `n`.
  `by_d` has one entry for every `5^d<=n`, including inadmissible top exponents
  with no available `3^c`. A present bit has entry `[a,b,c]` and the checker
  verifies the exact equation. An absent bit has a list `[[p,v],...]` in
  increasing `c` order for **every** `3^c<=n-5^d`; each pair certifies an exact
  positive odd valuation at a prime `p=3 mod 4`. An empty list certifies the
  case with no admissible `c`. Blockers for residual zero are always rejected.
  The checker reconstructs the mask from all alternatives.
* `hard_profile.json`: literal sets, all bridges and selected-blocker valuation
  features for the two actual survivors. The first certifying bad prime is
  selected deterministically; its histogram is not an invariant of all bad
  primes. Higher odd valuations are reported exactly, with `(d,c)` locations.
* `reference_comparison.json`: the unmodified supplied comparison gates and
  actual discrepancy. Reference constants exist only in the final comparison
  function, never in numerical generation or certificate construction.

Raw serialization is canonical: S2 and T contain indices `0..50,000,004`,
packed low bit first in each byte (`bit n = byte[n//8] >> (n%8) & 1`), with
unused high tail bits zero. Each file has 6,250,001 bytes. D contains one
unsigned 16-bit **little-endian** mask per n in increasing order; bit d means
`d in D(n)`, with all unused bits zero. It has 100,000,010 bytes. Hashes are
SHA256 of these exact bytes, not native word memory. The second replay checks
truncation, trailing bytes, tail bits and every entry, not just hashes.

## Limits and round 2 target

Uniform AJT5 remains open. **Conditionally**, a uniform AJT5 theorem plus the
verified bases `2..9` implies A303656 by strong induction: for `n>=10`, use
`m=floor(n/5)>=2`, `r=n-5m`, and `m<n`. The induction supplies nonempty `D(m)`;
AJT5 then supplies a child exponent. This implication alone proves nothing
about uniform AJT5. The finite scan establishes neither a new interval record
nor a characterization of all realizable masks.

The best round 2 target is to reconcile the original second-gate formula,
implementation and **actual list of the claimed 47** against these 220
certified rows. No enlargement is needed. Once that is resolved, compare
exact valuation features and bridge structure of the intended hard family.
The current two-case profile supports concrete checking, not a new general
discriminator or theoretical conclusion.
