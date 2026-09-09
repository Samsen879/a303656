# SQD Phase F reference bundle

Read `REPORT.md` before interpreting data.

**Authority caveat:** the required Phase E ZIP was not available. This bundle proves an independent exact-closure theory in the verified Phase D basal-B7 class. It does not falsely claim a verbatim Phase E reconstruction or an actual base-5 SQD counterexample.

Replay with Python 3.10 or newer (standard library only):

```bash
python verify_sqd.py --out replay_results
```

The default is an inclusive vertex/prime bound of 1,000,000, states of size at most four, and an integer-instantiation cap of 6*product(R) <= 1,000,000. This is a small reference computation, not a general B7 enumeration or a proof that unresolved cyclotomic cofactors are squarefree.

`results/states.json` records A(R), J(R), all proper closed substates, bounded primitive prime factors, and explicit factorization-completeness status. Uninstantiated large integers remain exactly specified by the cyclotomic expression. Numeric values/cofactors use SHA256 of the unsigned big-endian integer bytes. The report proves the unlimited mathematical statements; finite replay alone does not prove those statements.

`results/toy_same_root.json` is actual arithmetic at **base 3589**, not at base 5. `results/toy_cyclotomic_critical.json` is a general cyclotomic counterexample at base 19, not B7. `results/abstract_marked_model.json` is deliberately abstract and does not assign any actual square-dividing prime.

The source inventory is metadata and read-scope disclosure, not a claim that original source bytes were downloaded and hash-replayed locally. No GitHub write action was performed. No project status or route promotion was changed.
