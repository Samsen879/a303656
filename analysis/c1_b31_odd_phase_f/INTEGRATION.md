# Phase F B31 odd integration

## Authority binding

Repository: `Samsen879/a303656` (ID `1333945235`). Research and integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`.

## Source custody and replay

`A303656_B31_ODD_PHASE_F.zip` has outer SHA256 `43252261d203d56be147b18374f4eb0c5a2be90e9fc54a1b02e808ca4e7eddf2`. Safe extraction, all 8 members, 7 protected hashes, and the default 160,000-candidate verifier passed. The producer payload is copied byte-for-byte; the transport ZIP is not committed.

## Phase E dependency binding

The producer session did not have the requested Phase E source package available. The producer source artifact and its historical source-gap statements are preserved unchanged. Repository integration independently reconciled its O31 interface against authenticated local Phase E Seven-Basin source from Draft PR #32. O31 remains E3 authority; this package owns the B31 arithmetic classification. `O31_SOURCE_RECONCILIATION: PASS`.

Local dependency reconciliation: PASS. Repository dependency status: BOUND_TO_MERGED_REPOSITORY. `merge_blocked=false`.

The required Phase E PR is merged and this branch is refreshed on Phase-E-complete main. `python3 -B verify_integration.py --require-merged-dependencies` is the mandatory merge gate.

## What is proved and not proved

New scope: exact first relay set `{878851, 625552508473588471}` (both regular); two-vertex B31^odd exclusion; eight-index three-vertex reduction; the general odd closed-state critical-integer criterion; and the conditional exactly-seven original-odd-row lower bound `>=17` when the nonregular-root count is exactly seven.

Boundaries: B31^odd empty: NO; actual B31^odd member: NONE; exactly-seven killed: NO; N>=8: NO; finite branching is not finite-depth global closure. No A303656 solution, certified counterexample, universal C=1 no-go, or N>=8 theorem is claimed.

## Repository-native replay

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`. Replay occurs only in a temporary source copy and never overwrites producer results.

## Project state

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
