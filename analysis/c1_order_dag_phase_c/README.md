# A303656 extremal order-DAG — targeted Phase C

Read THEOREMS.md for full proofs and PROOF_AUDIT.md for scope checks.

New proposed results relative to the frozen Phase-B stack:

* Exactly seven roots force a pure3, seven-origin (2,2,3) first nonlinear frontier.
* Its roots have disjoint actual regular admitted basins, all terminating at3;
  mandatory heads7,31,19,5167 plus three of six depth3 heads.
* For N<=12, H={q:T(q) subset {3,5}} has size>=7; equality forces the pure3 normal form.
* With the imported2e9 inventory this yields >=7 nonregular primes above2e9.
* A precise conditional prime-order-chain hypothesis suffices to construct a
  complete C1 certificate with7 roots, but those roots have NOT been instantiated.

The total-root lower bound is still7. A303656 is unresolved.

## Replay

```
python3 -B reference.py --output-dir /tmp/a303656-phase-c-replay
python3 -B -m unittest -v
python3 -B verify_bundle.py --replay
```

The verifier needs only the Python standard library. Discovery used SymPy and
source-supplied large factor candidates; all primes are independently certified
inside the reference verifier by complete recursive n-1 Lucas certificates.
Different code organization is not claimed to be an independent author/software
team. The original repository code is not imported.

The results are finite supporting checks, not exhaustive enumeration of arithmetic
certificates. Source inventory2e9 was read, not replayed. No GitHub writes.
