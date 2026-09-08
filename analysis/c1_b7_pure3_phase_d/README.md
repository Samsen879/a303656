# A303656 B7 Phase D — research and exact certificates

Read **REPORT.md** for the mathematical definitions, proofs, scope distinctions, and full final verdict.

**Result:** Complete first-extension relay gate
`{43,127,379,7603,19531,519499}`, all regular; 48 exact orders for the three-vertex basin subclass, five excluded by complete certified cyclotomic factorization. Arbitrary branching B7 basin filling is proved conditionally on an actual nonregular B7 root. No actual B7 root or complete certificate is supplied.

**Not proved:** B7 emptiness; incompatibility with every other permitted basin; total nonregular lower bound eight; A303656.

## Reproduce
Python 3.10+; standard library only; no network:
```bash
python verify.py --self-test
python verify.py --output fresh_results.json
```
`verification_results.json` and `verification_log.txt` record the executed replay. These are not repository-native tests.
`SHA256SUMS.txt` protects all delivered payload files except itself.

## Files
- REPORT.md: complete Chinese mathematical report.
- arithmetic_certificates.json: complete prime/product/order/lifting data.
- verify.py: independent certificate checker and 14 regression tests.
- SOURCE_BINDING.json / SOURCES.md: live authority, read-file map, and explicit limitations.
- PROOF_AUDIT.md: adversarial scope checks.
- discovery_only_301_602.json: unpromoted, partially certified arithmetic hints; not used by verifier exclusions.

No GitHub writes. No route promotion. PROJECT: PAUSED. ACTIVE PROMOTED ROUTE: NONE. A303656: UNRESOLVED.
