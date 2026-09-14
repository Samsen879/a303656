# Constructive N>7 — open hedge

**HEDGE / UNINSTANTIATED / OPEN. A303656 remains UNRESOLVED.**

A formal certificate architecture is not an actual arithmetic instantiation.
A formal square-hit requirement is not a certified square hit. Survival of a
conditional N=9 architecture does not mean a complete N=9 certificate exists.

See [ARCHITECTURE.md](ARCHITECTURE.md), [INSTANTIATION_GATES.md](INSTANTIATION_GATES.md),
[C279_GATE.md](C279_GATE.md), and [SOURCE_CUSTODY.md](SOURCE_CUSTODY.md).
Full source proofs and exact schemas are under `reference/producer/`.

Offline standard-library reproduction (Python 3.10+):

```sh
python3 -B analysis/constructive_n_gt_7_phase_i/verify.py
```

This replays stored finite inputs and semantic mutations in disposable copies.
It does not factor targets, run a historical Wieferich scan, or certify unknown
terminal primes. No active route is promoted. Root STATUS.md is unchanged.
