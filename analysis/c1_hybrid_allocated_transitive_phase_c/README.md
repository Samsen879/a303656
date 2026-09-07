# Hybrid allocated–transitive release — Phase C research/reference bundle

Read `REPORT.md` for the theorem, proof, temporal/coalescence audits, actual
arithmetic witnesses, exact submodular formulation, and limitations.

## Outcome

A general **sufficient** frozen-state full-depth tagged release theorem is
proved. It includes P4 and G1/G3 sufficient instances. An actual mixed-mechanism
plan and an actual regular-guard nonmatroid example are supplied.

No universal successful allocation, no strict whole-ledger separation from all
old plans, no new seven-prime bound, and no solution of A303656 are claimed.
Exact local unions and temporal rigid blocking were already in Phase B.

## Reproduce

Python 3.10+ standard library only. Do not use `-O`.

```sh
sha256sum -c SHA256SUMS.txt
python3 -B reproduce.py --output /tmp/a303656-hybrid-replay
```

The runner recomputes and byte-compares four mathematical JSON files.
It does not modify frozen results, fetch source material, or access GitHub.
The first source scripts have convenience mains that write their own result
files locally; use `reproduce.py` for a non-overwriting audit.

`REPLAY.json` records the performed fresh local replay. Its wall-clock time is
not a mathematical reproducibility criterion. This is a single-author Python
reference laboratory, not an independent-author review, different-language
reimplementation, proof-assistant proof, or repository-native integration.

## Files

`SOURCE_BINDING.json` records the live authority and pinned mathematical
reading. `COMPUTATION_SPEC*.md` record staged targets before their computations.
`actual_results.json` records the full frozen eight-row ledger, full-depth
assignments, CRT witnesses, mixed-anchor counterexample, and private-lift test.
`geometry_results.json` separates abstract finite regressions from arithmetic.
`resource_results.json` records the four actual regular guards violating
matroid exchange. `plan_results.json` includes temporal release receipts and
six rejected malformed plans.

Free exponent coordinate5 is not an actual admitted row; ord_5(5) is undefined.
The arithmetic helper explicitly rejects that invalid call. Arithmetic support
labels in the closure table are not automatically rows in the frozen ledger.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
