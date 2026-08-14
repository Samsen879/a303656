# Weighted fixed-P4 out-of-mask holdout census

This directory implements the corrected 13-mask deterministic holdout protocol.
The original 12 candidate objects remain unchanged and ordered; the only added
mask is read from the certified `t3eq2/pool` optimum in
`analysis/p4_weighted_transferability/results/weighted_maxima.json`.

The source commit contains no new `T(n)` result.  Its required order is:

1. build and verify the corrected frozen manifest;
2. exhaustively enumerate generating fixed-P4 tuples and exclude all prior
   formal T-panel CRT classes;
3. determine `r` and freeze the deterministic panel;
4. run the pre-evaluation verifier in a fresh source-commit checkout;
5. only then run both exact backends and the factorization-free oracle on every
   and only frozen panel point;
6. reconstruct exact summaries, structural censoring, and transfer diagnostics;
7. run corruption tests and the final verifier.

All rational values retain integer numerators and denominators.  The global
A303656 problem remains unresolved, and any `T=0` output is only an
`UNVERIFIED COUNTEREXAMPLE CANDIDATE` pending a separate certification gate.
