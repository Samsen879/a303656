# A303656 — Thread 3 research packet

**Date:** 2026-09-21. **Status:** proofs developed in this note; independent review pending.

This packet is not a universal representation proof or a counterexample to A303656. It does not modify the repository or any frozen authority.

Pinned repository: `Samsen879/a303656` at
`8f17e88e517720f61f3c21d58d91c04cd6fa11b5`, tree
`811a274b1f671412305c8565fcd79e9d41c0189b`.

## Contents

- `research_report_zh.md`: complete Chinese report, identity catalogue, state diagrams, proofs, scope boundaries, restart lemma and verdict.
- `verify_thread3.py`: bounded exact symbolic/arithmetic replay.
- `certificate.json`: actual successful replay output, not a formal certificate for the analytic/asymptotic theorems.
- `replay_stdout.json`: concise replay receipt.
- `PROOF_AUDIT.md`: adversarial review checklist and claim-status map.
- `sources.json`: exact external references and the input each supplies.
- `SHA256SUMS.txt`: hashes for all other files in this packet.

## Replay

```sh
python verify_thread3.py --N 20000 --output replay_certificate.json
```

Requires Python 3.10 or newer, NumPy and SymPy. Actual replay environment:
Python 3.13.5, NumPy 2.3.5, SymPy 1.14.0.
No network access, account credentials, API keys or GitHub writes are used.
The script deliberately restricts N to 1,000–200,000.

The default run checks norm matrices for 1 <= K <= 100, six catalogue identities,
the centered-quadric determinant, 18 grid recurrences, three exhaustive residue
sections, two nonlinear theta identities (including recurrence-only reconstruction
through index 512), independent coefficient computations, exact countermodels,
and two finite-field determinant witnesses. No sampled coverage is promoted to
a theorem.

## Mathematical claims

**M:** distinct integer dilates of the counting function F, together with 1,
are linearly independent over C(x). The proof uses log-periodic Fourier modes,
not a finite coefficient search.

**M+:** no finite proper rational-linear mixed-dilation vector system containing
F exists. The proof includes the Ore common-multiple and matrix-elimination steps.

**Q:** a one-step, all-source upper bound for integer-weighted two-square source
states: almost every multiple of 15 lacks an incoming bounded-degree rational
chart of the specified fixed-affine type. This uses ESS and Landau.

**Q*:** for a finite witness-propagating system with positive definite binary
rational quadratic states, positive rational power weights, fixed affine scales
K >= 2, bounded-degree rational charts and finite seeds, the set of reachable
original integers has density zero. The last-defect proof is elementary apart
from basic quadratic-field norms and polynomial algebra; it does not use ESS
or Landau. Witness continuity is essential: arbitrary re-selection of a different
representation from an index alone is not a free operation in this model.

**Q†:** a weaker zero-density bound survives exponent-dependent carries when
every successful step strictly increases the integer index; finite integer
scales K>=1 are allowed. Coordinate-dependent carries are not covered.

**R:** the proposed Boolean window decoder is **unproved**. It would imply the
original conjecture together with eight explicit base cases. It is not positive
progress by itself.

All no-go conclusions have the scopes stated in the report. In particular,
counting non-Mahler behavior does not imply nonautomatic support, and failure of
a rule catalogue to reach n does not make n a counterexample.
