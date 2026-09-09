# Phase E B7 branching integration

## Authority binding

Repository: `Samsen879/a303656` (ID `1333945235`). Research and integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`.

## Source custody and replay

`A303656_B7_BRANCHING_PHASE_E.zip` has outer SHA256 `49f0a811921877b7479405716166542918c9330b1c7848e0a9db2dd7b1f8a316`. Safe extraction, all 17 members, 16 protected hashes, the ordinary verifier, and fresh four-output byte-identical replay passed. The producer payload is copied byte-for-byte; the transport ZIP is not committed.

## Theorem role and scope

Repository role: **GENERAL B7 CLOSED-STATE AUTHORITY**. The source supplies the good regular closed-state formalism, maximal-generator antichain, exact `J(R)`, primitive-normalized critical integer, fixed-state square-hit equivalence, fixed-cardinality effective finiteness, four-vertex fork/serial structural classification, regular diamond/shortcut counterexamples, and the failure of uniform finite-depth reduction. In particular, finite branching is not finite depth.

Explicit boundaries: B7 empty: NOT PROVED; minimal B7 member three-vertex: NOT PROVED; a uniform finite critical family for all B7: NOT PROVED; SQD: NOT PROVED; N>=8: NOT PROVED; no certified counterexample and no universal C=1 no-go are claimed.

## Repository-native replay

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`. Replay occurs only in a temporary copy and never overwrites producer results. Generated binaries and transport archives are rejected.

## Project state

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
