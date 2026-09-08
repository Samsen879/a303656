# A303656 private-provider charging — targeted Phase D

**Outcome:** center-provider ancestry, root-basin support confinement, and a frozen-state single-frontier shadow-width charging theorem. Exactly seven is **not** excluded; seven unit basin capacities match seven obligations at the terminal rank-3 frontier.

Start with `REPORT.md` (Chinese). `THEOREMS.md` contains full English proofs of D1–D5. `PROOF_AUDIT.md` separates actual, abstract, and conditional claims. `SOURCE_BINDING.json` records pinned GitHub sources and the reading boundary. `results.json` is the deterministic output of the standard-library standalone `reference.py`.

## Reproduce

Python 3.10 or newer, standard library only. Do not run with `-O`.

```sh
python3 -B verify_bundle.py --replay
```

Or generate a fresh output without modifying the frozen results:

```sh
python3 -B reference.py --output /tmp/a303656-provider-phase-d-results.json
cmp results.json /tmp/a303656-provider-phase-d-results.json
```

The verifier validates the local checksums and optionally recomputes the reference output in a temporary directory. It does not contact GitHub, replay repository CI, or formally verify the proofs. `REPLAY.json` records the performed byte-identical local replay. This is not independent-author or different-language verification.

`COMPUTATION_SPEC.md` and its addendum were recorded before their respective computations. The beta-one contraction engine and the separate deeper shadow-width enumeration have different explicitly bounded scopes. All synthetic fixtures are ABSTRACT; the seven-root upstream chains remain CONDITIONAL, not actual rows.

The bundle is an offline research artifact, not repository integration, a PR, or theorem promotion.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
