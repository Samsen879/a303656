# Bounded T(n) pilot contract

Task: **BOUNDED T(n) PILOT WITH THREE-WAY EXACT VERIFICATION**

This contract defines a fixed, resource-capped architecture validation. It is
not a broad mining campaign, does not extend the certified interval, and does
not prove or disprove the global A303656 statement.

## Exact definition

For `n > 1`, let

```text
E(n) = {(c,d) in Z_{>=0}^2 : 3^c + 5^d <= n}

T(n) = sum over (c,d) in E(n) of
       1[n - 3^c - 5^d is a sum of two squares].
```

`T(n)` counts source exponent pairs. It does not count distinct numerical
shifts and does not count the number of two-square representations. Different
`(c,d)` pairs with the same shift contribute separately. Multiple `(a,b)`
representations of one remainder contribute only one for that source pair.
Every active source pair is processed; first-hit and saturated counting are
forbidden.

For every winning source pair, the canonical witness is the valid `0 <= a <= b`
with minimum `a`, then minimum `b`.

## Immutable formal intervals

All intervals are half-open:

| ID | Interval | Width |
|---|---:|---:|
| `PILOT-A` | `[2,200002)` | 200,000 |
| `PILOT-B` | `[240000000001,240000100001)` | 100,000 |

No formal pilot integer outside these 300,000 values may be added. Small
`FIXTURE-*` intervals are allowed only for property, fault-injection, and
resource-estimation tests.

## Three implementations

| Role | Immutable `implementation_id` | Counting core |
|---|---|---|
| bitset | `tn_bitset_annulus_v1` | Source-pair loop, a-outer annulus, packed per-pair dedup bits, bitwise integer square root |
| clean | `tn_clean_annulus_v1` | Independently coded source rectangle, b-outer annulus, byte dedup flags, binary-search integer square root |
| oracle | `tn_gmp_uv_oracle_v1` | GMP reference in transformed coordinates `u=b-a`, `v=b+a`, byte dedup flags |

The two production annulus/isqrt cores are not merged into a shared helper.
The GMP oracle calls neither production core and imports no production counting
code. The production executables share only `tn_pilot_output.hpp`, which owns
CLI parsing and output serialization, not enumeration or counting.

## Required artifacts

Each role has a separate output directory containing:

```text
metadata.json
counts.csv
low_t.jsonl
summary.json
provenance.json
verifier_report.json
```

`counts.csv` has exactly one `n,T` row for every integer in `[L,U)`. `low_t.jsonl`
contains every `n` with `T(n) <= 3` and every interval argmin. Each record has
the complete source-pair winner list and canonical witness equation fields.

`summary.json` contains the exact histogram, minimum, complete argmin summary,
`T=0/1/2/3` counts, active-pair range, and SHA256 values for the count and
low-T files. Metadata must state:

```text
obstruction_data_status: NOT_COLLECTED_IN_TN_PILOT
```

No losing-pair factorization or obstruction dataset is claimed in this pilot.

## Automatic provenance

`run_tn_pilot.py` accepts no source-commit or implementation-id parameter.
It obtains the commit with `git rev-parse HEAD`, obtains identity by executing
the binary with `--implementation-id`, and computes executable, source, and
output hashes itself. A dirty source tree is rejected unless `--allow-dirty`
is explicitly used for a non-acceptance fixture; such a run is marked
`formal_acceptance_eligible=false`.

The verifier checks the current binary hash and identity, current source-tree
commit/dirty state, source hashes, exact backend CLI, interval, all output
hashes, row completeness, reconstructed summaries, and every recorded witness.
After a successful three-way comparison it also records its own source path,
SHA256, and exact CLI. Audit-only replay requires that verifier to be the
checked-in `src/verify_tn_pilot.py` from the recorded source tree.

Mandatory expected-rejection tests cover:

- nonexistent caller `--source-commit` override;
- bitset/clean slot swap;
- provenance implementation relabel;
- output tampering;
- executable replacement.

An expected rejection passes only when the harness observes nonzero status and
the intended diagnostic.

## Execution discipline

Acceptance uses a fresh clean Git source clone/worktree, newly built binaries,
explicit inner and outer timeouts, and `/usr/bin/time -v` memory monitoring.
Raw command, stdout, stderr, return code, and elapsed/resource logs are retained.
Certified baseline hashes are checked before and after.

If any implementation reports `T(n)=0`, the record is only an
`UNVERIFIED CANDIDATE` until all three implementations and every active source
pair are checked. Even three-way agreement is reported only as
`CERTIFIED BOUNDED CANDIDATE PENDING SEPARATE THEOREM VERIFICATION` in this
pilot; it is not a global counterexample announcement.
