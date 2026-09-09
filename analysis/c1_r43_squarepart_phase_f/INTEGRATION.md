# Phase F r=43 square-part integration

## Authority binding

Repository: `Samsen879/a303656` (ID `1333945235`). Research and integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`.

## Source custody and replay

`A303656_R43_SQUAREPART_PHASE_F.zip` has outer SHA256 `03ed72c8f42afa123464c63a128ac72624db00ff4d672de822ec4d653cde630f`. Safe extraction, all 66 members, all 65 protected hashes, mutation replay, independent C++/GMP verification, deterministic positive ECM, and both 1e12 trial progressions passed via `bash replay.sh --trial`. Replay used a fresh temporary source copy. `SYMPY_LICENSE.txt` and `THIRD_PARTY_NOTICES.md` are retained; `ecm_reference.cpp` is not official GMP-ECM.

## Phase E dependency binding

The producer session did not have the requested Phase E source package available. Its historical provenance statements are preserved unchanged. The integration layer reconciled against E2 Draft PR #31 and E4 Draft PR #33. E2 `cofactors/C_903.txt` and F3 `C903.txt` are byte-identical at SHA256 `07dff3e4b33a6e893c24f83f07dbac243b48c25b3f48b334c821035064804e7b`; E2 `cofactors/C_1806.txt` and F3 `C1806.txt` are byte-identical at SHA256 `39cbbcdb3b186c1672471af958ec63bd5f91967b8bd7d7c37857a11f79a4eb44`. Both hard object gates PASS.

Local dependency reconciliation: PASS. Repository dependency status: BOUND_TO_MERGED_REPOSITORY. `merge_blocked=false`.

The required Phase E PRs are merged and this branch is refreshed on Phase-E-complete main. `python3 -B verify_integration.py --require-merged-dependencies` is the mandatory merge gate.

## What is proved and not proved

The new certified C1806 factor is `147304138944416276237689`: prime, exact order 1806, `1 mod 4`, multiplicity one. The remaining R1806 cofactor is 314 digits / 1040 bits and proven composite; C903 remains 333 digits / 1103 bits and proven composite. Remaining dangerous factors retain the source bounds/order filters.

Boundaries: 903 CLOSED: NO; 1806 CLOSED: NO; r=43 family empty: NO; squarefree: NOT PROVED. Negative ECM or randomized misses are not squarefree proof. No A303656 solution, certified counterexample, universal C=1 no-go, or N>=8 theorem is claimed.

## Repository-native replay

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`. The integration verifier runs the full producer `--trial` gate in an isolated temporary copy and rejects `.local-bin` or binaries in committed bytes.

## Project state

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
