# Nonlinear core Phase C — read-only research/reference package

Start with `REPORT.md`. It contains the mathematical proofs, counterexamples, scope guards, and the requested final verdict. `SOURCE_READING.md` and `source_binding.json` identify the pinned repository sources; they are metadata/reading records, not a local repository snapshot.

The principal new deductions are the canonical log-guard identity, private-provider and shared-origin prefix-LCA constraints, and the arity-sensitive support-profile descent. These do **not** exclude a TRUE terminal residual. All small complete product-cylinder models are explicitly ABSTRACT, not actual arithmetic certificates.

## Reproduce

Python 3.10+ and the standard library are sufficient. No network or repository installation is needed.

```bash
python verify.py
```

The verifier checks the supplied SHA256 manifest when present, runs a fresh copy of `reference.py` in a temporary directory, and byte-compares the deterministic mathematical outputs `results.json` and `computed_summary.json`.

To regenerate directly in this directory:

```bash
python reference.py
```

This overwrites results and timing files. It does not modify any Git repository. `run_metrics.json` and the timing lines in `run_log.txt` are descriptive measurements, not deterministic mathematical outputs; fresh measurements need not match the supplied values. A full regenerated ZIP is not claimed byte-identical across different timing runs/platforms.

The checker uses assertions, so do not invoke Python with `-O` or `PYTHONOPTIMIZE` enabled.

## Files

`REPORT.md` — full Chinese mathematical report.

`PROOF_AUDIT.md` — producing researcher's adversarial audit; not an independent referee.

`COMPUTATION_SPEC.md` — bounded domains, exactness and complexity gates.

`reference.py` — standalone exact reference implementation, no repository code imports.

`results.json` — named fixture states, original shadow masks, macro supports/state tokens, typed witnesses and provenance IDs, actual arithmetic checks.

`computed_summary.json` — deterministic aggregate counters.

`authority.json`, `source_binding.json`, `SOURCE_READING.md` — frozen live-authority and reading metadata.

`verification.json` — fresh-replay receipt.

`SHA256SUMS.txt` — per-file hashes, excluding the manifest itself.

## Status

```text
RECURSIVE CLOSURE:
NO GENERAL CLOSURE, BUT NEW OBSTRUCTION FOUND
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
