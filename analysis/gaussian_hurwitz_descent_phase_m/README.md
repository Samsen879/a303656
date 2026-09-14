# Gaussian–Hurwitz representation-descent route audit

```text
ROUTE: GAUSSIAN–HURWITZ FIXED-NORM 5-NEIGHBOR DESCENT
STATUS: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

This is a scope-qualified route audit, not a Gaussian mainline promotion.
The natural move family is every legal `alpha q beta/5` with both parameter
norms equal to5, augmented by the explicitly specified finite symmetries.
Fixed-norm obstructions do not rule out genuinely cross-shell, S-arithmetic,
state-dependent, automorphic, non-5-denominator or nonlinear mechanisms.

Strongest positive assets: the complete natural norm-5 operator classification,
exact integrality/rank criterion, integral target recovery and conditional
exact c-changing identity. Strongest obstructions: M-D1 away-from-5 content
and infinite target-free components; M-D4 primitive accessible compulsory
uphill barrier; M-D2 fixed globally shape-preserving matrix subgroup; M-D3
bounded additive displacement/positive bounded exponent-lift no-go.

Read [REPORT.md](REPORT.md), [NOVELTY_MATRIX.md](NOVELTY_MATRIX.md) and the linked
byte-identical source proof files. Historical fact classification is not a
claim of novelty in quaternion theory. A script PASS certifies its finite
coverage, not the infinite written proofs or independent referee approval.

Reproduce from repository root:

```sh
python3 -B analysis/gaussian_hurwitz_descent_phase_m/verify.py
```

Python3.10+ standard library only; deterministic, offline, no original-n scan.
It runs the independent audit and minimax replay on disposable copies and
regenerates operators without reading a producer operator table.
Optional original43-shell producer replay, only with already available NumPy:

```sh
python3 -B analysis/gaussian_hurwitz_descent_phase_m/verify.py --with-producer
```

Source scripts write receipts: never run them against immutable committed
inputs in place. The wrapper supplies disposable input/output directories.
No packages are installed automatically. Root STATUS.md is unchanged.
