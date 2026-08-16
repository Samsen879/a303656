# One-sided exponent strip: repository-native audit

This directory audits the narrowly admitted work from GitHub issue #2. It does
not promote a route and does not change the frozen authority state:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The fixed finite domain is `2 <= n <= 100,000,000`. Extending it, enlarging a
prime pool, or searching for a Wieferich/nonregular full cover is outside this
audit.

## Audited objects

1. Two source implementations rebuild the `S2`, `C3`, and `C5` byte arrays.
   The arrays are written only to a caller-supplied scratch directory and are
   never committed.
2. `periodic_verifier.py` checks complete finite periods and rejects unresolved
   valuation at the supplied precision.
3. `theorem_audit.py` independently checks the algebraic lemmas and a complete
   10,584-residue small model supporting the regular-lift no-go proof.
4. `test_corruptions.py` requires every named malformed or incomplete
   certificate to be rejected.

The Python dependency is declared by the repository root `requirements.txt`
(`numpy==2.5.1`). Missing NumPy is reported before any expensive replay starts.

## Commands

Fast, network-free source checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s analysis/one_sided_strip_audit/tests -p 'test_*.py'
```

Full fixed-domain replay, with raw arrays outside Git:

```bash
python3 analysis/one_sided_strip_audit/tools/replay.py \
  --N 100000000 \
  --scratch /tmp/a303656-one-sided-strip-100m \
  --expected analysis/one_sided_strip_audit/fixtures/expected_100m.json \
  --source-commit SOURCE_COMMIT \
  --output /tmp/finite_replay.json
```

The committed results record hashes, counts, records, commands, and return
codes only. Six 100,000,001-byte arrays are explicitly omitted.

After writing `REPORT.md` and the four core JSON results, finalize and verify:

```bash
python3 analysis/one_sided_strip_audit/tools/finalize.py \
  --results analysis/one_sided_strip_audit/results \
  --source-commit SOURCE_COMMIT --base-sha BASE_SHA --base-tree BASE_TREE
python3 analysis/one_sided_strip_audit/tools/verify_results.py \
  --results analysis/one_sided_strip_audit/results \
  --expected analysis/one_sided_strip_audit/fixtures/expected_100m.json \
  --source-commit SOURCE_COMMIT \
  --output analysis/one_sided_strip_audit/results/verification_report.json
```

## External packet defects

- The stopped issue #1 packet hard-coded `/mnt/data`. Because issue #1 is
  closed `STOP` with no implementation, that script is not imported here; the
  portability defect is recorded rather than silently repaired.
- The issue #2 external README named a nonexistent `raw_gzip/` directory. This
  audit states the omission explicitly.
- The issue #2 external runner did not fail early with a declared dependency.
  This audit binds NumPy to the root requirements and performs a preflight.
