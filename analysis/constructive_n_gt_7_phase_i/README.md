# Constructive N>7 — frozen I7 closed; general possibility unresolved

FROZEN I7 / N=9 (1,5,3) ARCHITECTURE: CLOSED.
REASON: Sq(279)=EMPTY, while I7 requires |Sq(279)|>=3.
GENERAL N=9: UNRESOLVED. GENERAL N>7: UNRESOLVED.
ACTIVE PROMOTED ROUTE: NONE. A303656: UNRESOLVED.
Constructive N>7 is not logically excluded, but no architecture is promoted.

A formal certificate architecture is not an actual arithmetic instantiation.
A formal square-hit requirement is not a certified square hit. The frozen
formal N=9 schema is retained historically, but its arithmetic gate is false.
See [later exact C279 closure](c279_closure/README.md). The earlier bounded
OPEN search record is preserved, not erased or reinterpreted as negative proof.

See [ARCHITECTURE.md](ARCHITECTURE.md), [INSTANTIATION_GATES.md](INSTANTIATION_GATES.md),
[C279_GATE.md](C279_GATE.md), and [SOURCE_CUSTODY.md](SOURCE_CUSTODY.md).
Full source proofs and exact schemas are under `reference/producer/`.

Offline standard-library reproduction (Python 3.10+):

```sh
python3 -B analysis/constructive_n_gt_7_phase_i/verify.py
```

This replays stored finite inputs and semantic mutations in disposable copies.
It also independently replays the later exact closure certificates. It does
not factor targets, run a historical Wieferich scan, or evaluate the six other
order gates. No active route is promoted. Root STATUS.md is unchanged.
