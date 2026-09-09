# Phase E seven-basin global shared-state integration

## Authority binding and custody

Repository: `Samsen879/a303656` (ID `1333945235`). Research/integration base: `fd59aad038a09f2fc6df7039111408fa231c27dd`, tree `afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`. `A303656_SEVEN_BASIN_GLOBAL_SHARED_STATE_PHASE_E.zip` has outer SHA256 `16970c82ca66048d52d1430828413fd88b567f52bd4a82dd989247cb9328704a`; its actual inner root name is preserved. Safe extraction, all 8 members, the 7-entry manifest, and fresh mathematical JSON comparison (ignoring timing only) passed. Producer bytes are unchanged and the ZIP is not committed.

## Theorem role and exact scope

Repository role: **EXACTLY-SEVEN STATE-COMPATIBILITY / O31 AUTHORITY**. The source covers actual basin filling, seven-basin CRT gluing, parity deletion, O31 necessity, and complete-state sufficiency under O31. The iff is scoped to a prescribed actual exactly-seven arithmetic normal form, allowing legal K/E to be chosen. It is not an arbitrary frozen seven-root ledger statement.

Explicit boundaries: actual seven nonregular terminal roots are NOT INSTANTIATED; exactly-seven not excluded; N>=8: NOT PROVED; no actual complete C=1 certificate is supplied.

## Replay and project state

Run `python3 -B verify_integration.py` and `python3 -B -m unittest -v tests/test_integration_scope.py`.

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
