# Phase F closed-state SQD integration

## Authority binding

Repository: `Samsen879/a303656` (ID `1333945235`). Research and integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`.

## Source custody and replay

`A303656_CLOSED_STATE_SQD_PHASE_F.zip` has outer SHA256 `144cd916f6c6f2e3f5b04921ee4deadd98504c82e3d9a58a7f98c2df4a28345b`. Safe extraction, all 12 members, the exact 11-entry producer manifest, and fresh replay with all mathematical JSON outputs equal after ignoring only `runtime_seconds` passed. The producer payload is byte-preserved; the ZIP is not committed.

## Phase E dependency binding

The producer session did not have the requested Phase E source package available. Its Phase-D-based reconstruction and source-gap statements remain unchanged. The integration layer reconciled `good state R`, closure, `A(R)`, `J(R)`, `W_R`, `Z_R`, and primitive normalization against E1 Draft PR #30; E2 #31 and E4 #33 are supporting dependencies. E1 owns closed-state theory. F2 adds distinct-state normalized coprimality, raw deletion gcd structure, ambient `V_B` factorization, the no-migration theorem, and the SQD route audit.

Local dependency reconciliation: PASS. Repository dependency status: PENDING_MERGE. `merge_blocked=true`.

**MERGE STATUS: BLOCKED UNTIL THE REQUIRED PHASE E PRS ARE MERGED, THIS BRANCH IS REFRESHED ON NEW MAIN, AND STRICT DEPENDENCY REPLAY PASSES.** The future gate is `python3 -B verify_integration.py --require-merged-dependencies` after rebinding to Phase-E-complete main and setting `BOUND_TO_MERGED_REPOSITORY`.

## What is proved and not proved

Within the reconciled exact closed-state class, `R != T => gcd(Z_R,Z_T)=1`; hence a square-hit prime in one exact state does not even divide another. Same-root strict migration: IMPOSSIBLE.

Boundaries: different-prime replacement: UNRESOLVED; SQD-cost: UNRESOLVED; certificate-specific replacement: NOT PROVED; actual base-5 B7 SQD counterexample: NONE; minimal B7 root three-vertex: NOT PROVED; general B7 reduced to three-vertex: NO. Different-base examples are not base-5 B7 counterexamples. No A303656 solution, certified counterexample, universal C=1 no-go, or N>=8 theorem is claimed.

## Repository-native replay

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`.

## Project state

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
