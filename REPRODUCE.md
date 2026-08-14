# Reproduction guide

All commands are run from the repository root. The levels below deliberately separate cheap authority verification from expensive mathematical computation.

## Level 0 — frozen authority and repository surface

Requirements: Python 3.10+ and standard-library `zipfile` support.

```bash
python3 scripts/verify_public_repository.py
```

This network-free check validates:

- the frozen Master Authority V2 SHA256;
- ZIP CRC, paths, internal manifests, JSON, UTF-8, and recursive control-character rules;
- the 20 disclosed stale nested-manifest entries and their reconciliation ledger;
- N-004 and N-009 scope guards;
- theorem, route, finite-computation, custody, and project-status consistency;
- generated public authority views.

It does not independently re-prove the mathematics or rerun multi-billion searches.

Equivalent wrapper:

```bash
./scripts/replay_public_repository.sh
```

## Level 1 — quick stored-evidence replay

System dependencies:

- Python 3
- a C++17 compiler
- GMP development headers/library
- `sha256sum`
- `unzip`

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
SKIP_STAGE0=1 LEVEL=quick ./run_reproduce.sh
```

Or:

```bash
RUN_QUICK_FINITE_REPLAY=1 ./scripts/replay_public_repository.sh
```

## Level 2 — historical Stage-0-inclusive quick replay

```bash
LEVEL=quick ./run_reproduce.sh
```

Raw historical packages can contain disclosed typography or stale-manifest defects. Their bytes must not be silently repaired. Consult `docs/ARTIFACT_LINEAGE.md` first.

## Expensive historical campaigns

Historical modes such as `certified10m`, `certified100m`, `full1b`, and `full1p6b` exist for provenance. They are not part of the default public replay and are not automatically authorized. The stored certified results should be checked through their manifests and independent verifiers before considering a rerun.

## Expected Level-0 conclusion

```text
repository_surface: PASS
recursive_authority_validator: PASS
frozen_authority_sha256: 3033149749b1dbfb70ac73190d5323ee1817a219ce07c1e1913d1008c8629d35
A303656: UNRESOLVED
```
