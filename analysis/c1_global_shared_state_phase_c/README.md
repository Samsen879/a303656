# A303656 shared-state Phase C — standalone research bundle

Read REPORT.md first. It contains all requested report sections and symbolic proofs.
The central new deductions concern a single nonregular row, an actual
fractional/integer configuration gap, and multi-use original rigid resources.
PROOF_AUDIT.md records adversarial checks and restrictions.

## Reproduce (Python 3.10 or newer, standard library only)

```bash
python3 -B verify_bundle.py
```

Or run the components:

```bash
sha256sum -c SHA256SUMS.txt
python3 -B reference.py --output /tmp/a303656-shared-state-results.json
cmp results.json /tmp/a303656-shared-state-results.json
python3 -B -m unittest -v
```

COMPUTATION_SPEC.md was written before the initial computations;
COMPUTATION_SPEC_ADDENDUM.md records additional scoped checks before execution.
results.json is deterministic. Test log elapsed times are not mathematical data.
The verifier checks package checksums, deterministic reference replay, and tests.
It does not verify the mathematical proofs formally or fetch/replay the repository.

The live source snapshot and source Git blob identifiers are in SOURCE_BINDING.json.
These are connector-derived receipts, not a local checkout or bundled source copy.
No repository-native integration, GitHub write, route promotion, complete certificate,
or A303656 resolution is claimed.
