# Phase F four-vertex B7 integration

## Authority binding

Repository: `Samsen879/a303656` (ID `1333945235`). Research and integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`.

## Source custody and replay

`A303656_B7_FOUR_VERTEX_PHASE_F.zip` has outer SHA256 `0494af95826e91e498ba833b4b27aea8b95875edf43b4105e7a6bb62ce0c54e1`. Safe extraction, all 31 members, all 30 protected hashes, standard verification, full bounded probe replay, and GMP p-1 replay passed unmodified in a fresh temporary source copy. Authenticated CSV/log/text/C++ sources are retained; no compiled binary is committed.

## Phase E dependency binding

The producer session did not have the requested Phase E source package available. The independent reconstruction and source-gap statements are preserved unchanged. The integration layer reconciled fork/serial classification, first-relay set, and fixed-state critical-integer interface against E1 Draft PR #30, with E2 #31 and E4 #33 as supporting dependencies. `FOUR_VERTEX_CLASSIFICATION_RECONCILIATION: PASS`. E1 owns the geometry classification; this package adds explicit aggregates, the full fork arithmetic table, partial certified serial materialization, and bounded factor/probe evidence.

Local dependency reconciliation: PASS. Repository dependency status: BOUND_TO_MERGED_REPOSITORY. `merge_blocked=false`.

The required Phase E PRs are merged and this branch is refreshed on Phase-E-complete main. `python3 -B verify_integration.py --require-merged-dependencies` is the mandatory merge gate.

## What is proved and not proved

Fork: 15 proper states and 120 distinct terminal indices, EXHAUSTIVE. The exact aggregate is `F_(r,s)=((5^(42rs)-1)(5^42-1))/((5^(42r)-1)(5^(42s)-1))` under source definitions. Serial: 28 certified proper states and 448 terminal indices, NOT EXHAUSTIVE. Its aggregate is `S_(r,s)=(5^(42rs)-1)/(s(5^(42r)-1))` under source scope. The 23 relays through 1e10 are complete for the stated bounded search; five additional large relays are certified. All 90 admitted terminal factors have valuation one.

Boundaries: full S_r census: NO; all serial states enumerated: NO; complete four-vertex exclusions: 0; actual B7 member: NONE; all fork states closed: NO; all serial states closed: NO; all four-vertex B7 closed: NO. No A303656 solution, certified counterexample, universal C=1 no-go, or N>=8 theorem is claimed.

## Repository-native replay

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`. The verifier runs both ordinary and full native producer gates in a disposable source copy.

## Project state

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
