# A303656 TWO-NONREGULAR GLOBAL SHARED STATE — Phase D

Read `REPORT.md` for the Chinese report and `THEOREMS.md` for complete proof
statements and scope. `verified/RESULTS.json` contains the deterministic
reference outputs. `PROOF_AUDIT.md` records adversarial checks.

## Replay

Requirements: Python 3.10 or newer and SymPy. This session used SymPy 1.14.0.
No repository implementation is imported. No network or GitHub write is used.

```bash
python reference.py --output /tmp/a303656-two-root-replay
python - <<'PY'
import json
from pathlib import Path
assert json.loads(Path('verified/RESULTS.json').read_text()) == json.loads(
    Path('/tmp/a303656-two-root-replay/RESULTS.json').read_text())
print('deterministic outputs match')
PY
sha256sum -c SHA256SUMS.txt
```

The optional `--skip-resultants` flag runs only the standard-library audits;
it is NOT a full replay and produces a deliberately smaller result object.
SymPy is required only for two differently organized exact integer resultant
computations. Prime certificates for the named small primes and all factors
of the large gcd use deterministic trial division, not probable-prime flags.

`R67_7.hex` and `R67_8.hex` store the COMPLETE SIGNED resultants in hexadecimal.
They are text, not binary artifacts. Each is checked against both direct
resultant computation and the half-degree identity in THEOREMS Section 10.

`COMPUTATION_SPEC.md` predates the executed tests. `fiber_check.py` and
`resultant_explore.py` preserve the small discovery programs. The latter can
regenerate benchmark timing data and saved resultants; timings are not part
of the deterministic verification receipt. `reference.py` is the consolidated
replay and does not overwrite the supplied mathematical data.

## Boundaries

No actual whole odd pooled cover or complete C=1 certificate is claimed.
The separator iff still has global private-state quantifiers; it is not a
complete order-signature classification of every two-root overlap.
The actual two-root collision fixture has frozen root states; the same prime
pair was already covered by a stronger source P4 no-go.
The exactly-two fractional gap extension has deliberately inert nonregular
rows and is not a cooperative-cover example.

No full local repository checkout, repository-native test replay, external
independent software stack, or new prime scan is claimed. Read access was
through the GitHub connector on the pinned main snapshot.

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
