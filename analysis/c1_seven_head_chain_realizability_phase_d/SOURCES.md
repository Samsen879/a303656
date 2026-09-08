# Sources and read scope

All source-derived statements are pinned to the main SHA in AUTHORITY.json.
These are read-only content/metadata observations, NOT a fresh repository-native
integration replay. A full local checkout/archive was not available; no claim
of fresh repository checksums, CI, or protected-file replay is made.

The task's four package directories were reviewed through their actual source
file contents in the complete PR file diffs (#20, #21, #22, #24), not merely their
PR bodies. The governing theorem, seven-prime report, shared-state proof excerpt,
and STATUS were fetched again by immutable current-main SHA. PR metadata was
separately refreshed to check the serialized merge chain #21--#25. #25 modifies
two Hybrid integration/test metadata files; it does not modify mathematical payload.

[S1] analysis/c1_order_dag_phase_c/THEOREMS.md, especially §§7,12,13.
Current Git blob: 0c86de426dc932a13a4d7cccb198e4ef3bd7c811.
[S2] analysis/c1_global_shared_state_phase_c/PROOF_DETAILS.md, especially C2/C3
(single shared state) and C9 (odd pooled scope, not simultaneous C=1).
Current Git blob: 5c6d4ebddcf7fb3ead3c21b130a2120ec7325211.
[S3] analysis/c1_hybrid_allocated_transitive_phase_c/; general tagged release
and coalescence in an escape policy do not override exactly-seven basin disjointness.
[S4] analysis/c1_seven_prime_audit_phase_b/REPORT.md and its actual arithmetic
certificates/proof/source files. Current REPORT blob:
50a9c03fed03a3471eab22b0527a8a789c19d2a7.
[S5] STATUS.md, current Git blob 2ba295c0ada0d19b4e7f7d7871312d0696a785d2.
[S6] Primary Cunningham Project table pmain126.txt, base 5 minus, exponent 191
and exponent 271 entries. Used as factor/cofactor hints only. Its P121/P171 labels
are not substituted for locally replayed primality certificates.

Pinned source locations:
```
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_order_dag_phase_c/THEOREMS.md
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_global_shared_state_phase_c/PROOF_DETAILS.md
https://github.com/Samsen879/a303656/tree/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_hybrid_allocated_transitive_phase_c
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_seven_prime_audit_phase_b/REPORT.md
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/STATUS.md
https://homes.cerias.purdue.edu/~ssw/cun/pmain126.txt
```

All Phase-D numerical assertions in REPORT.md are generated here and checked by
verify.py, except the exhaustive q<=2e9 inventory, whose exhaustiveness is imported
from [S4]. The four named inventory primes' primality/orders/valuations, including
the nonadmitted negative control, ARE independently recertified here.
No claim of literature novelty is made for newly explored factors.
