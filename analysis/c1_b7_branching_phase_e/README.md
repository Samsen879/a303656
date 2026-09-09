# A303656 B7 branching — Phase E research package

Main report: `REPORT.md` (Chinese). Full mathematical proofs: `THEOREMS.md`.
The central result is an exact closed-state / maximal-generator terminal gate,
with a primitive-only critical integer for each fixed state, a finite cardinality
recursion and complete four-vertex fork/serial formulas.
All 120 fork indices are materialized; serial factor sets are not.

The actual diamond prime 6717031 and shortcut prime 42743 are **regular** fixtures,
not B7 members. This package does not prove B7 empty or N>=8.

## Replay

Python 3.10 or later, standard library only; no network or repository checkout.
From this directory run:

```bash
python3 -B verify_bundle.py
python3 -B verify_bundle.py --replay
```

The first checks all protected SHA256 entries and the exact file set. The second
also invokes the standalone reference in a fresh temporary directory and compares
four deterministic outputs byte for byte with the sealed files. To inspect a
standalone fresh run directly:

```bash
python3 -B reference.py --output-dir /tmp/b7-phase-e-replay
```

The executable checks certify finite arithmetic and finite combinatorial instances;
they do not establish the universal mathematical theorems by sampling.

## Main files

`C4_FORK_120.txt` is the sorted full numeric fork family. The JSON companion keeps
its 15 first-relay-pair groups. `ACTUAL_REGULAR_CERTIFICATES.json` contains the
13 trial-division/order/lifting receipts; `results.json` also includes the compact
diamond Lucas certificate, abstract DAG counts, serial examples, and actual mask.
`SOURCE_BINDING.json` and `SOURCES.md` distinguish imports, live authority and actual
reading scope. `PROOF_AUDIT.md` registers the nonclaims. `DISCOVERY_ONLY.json`
records a bounded two-index discovery probe, not promoted absence evidence.

All new proofs and implementations were produced in the same session. No
independent-author or proof-assistant verification is claimed.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
