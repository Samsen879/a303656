# C=1 nonregular coarse-fatal audit

This directory is the bounded repository-native audit admitted by GitHub issue
#4. It preserves the project status:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The audit independently checks four narrow theorem objects:

1. prime-power order, subgroup index, and the local valuation trichotomy;
2. the reverse CRT implication behind coarse-fatal factorization;
3. a closed fatal-set formula, including explicit `beta_p > 0` cases;
4. the order-decoupled shell-sparse corollary for the three admitted
   base-5 nonregular primes.

It does not search for more primes, scan integers, or search for a complete
certificate. A local-mask escape is not a two-square representation.

## Source checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s analysis/c1_nonregular_coarse_fatal_audit/tests -p 'test_*.py'
```

## Deterministic replay

Write results outside Git first:

```bash
python3 analysis/c1_nonregular_coarse_fatal_audit/tools/replay.py \
  --source-commit SOURCE_COMMIT \
  --output-dir /tmp/a303656-c1-coarse-results
```

The external source was supplied only as an extracted 21-file directory. Its
internal `SHA256SUMS.txt` passed, but the claimed outer ZIP byte with SHA-256
`8fb15f895b7968454f66a355774e9d69121d729dc26b16768a61998384272af7`
was not supplied and is not asserted as verified here. The supplied internal
manifest file itself has SHA-256
`90abe6a18b28c27f124d0e16fd0d057b87aa9f95b0fedcb6dc80867ed5c0cb73`.
