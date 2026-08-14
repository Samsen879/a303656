# Raw, repaired, and superseded artifact lineage

## Rules

- `raw`: immutable historical bytes, including disclosed defects.
- `repaired`: a new derivative with a new filename and hash, plus an explicit repair map.
- `audit`: an independent inspection or adjudication artifact; it does not impersonate its source.
- `candidate`: generated authority package awaiting or recording review.
- `frozen`: exact bytes accepted through a freeze receipt.
- `superseded`: retained for provenance but not used as the active public authority.

## Active chain

```text
17 locally recovered exact-hash authorities
        +
3 restored web-custodied exact-hash authorities
        ↓
Phase 0 evidence alignment
        ↓
Phase 0.5 custody and manifest reconciliation
        ↓
Master Authority V2 final-freeze candidate
        ↓ exact-hash acceptance
FREEZE_RECEIPT.json
        ↓
Master Authority V2: FROZEN
```

## Known historical defects

- 12 logical illegal-control-character defects represented by 48 Phase-0 physical copies: 11 form-feed defects and one backspace defect.
- 20 stale nested-manifest entries in the bounded refreshed bundle: 12 log copies and eight structured result copies. Scientific payload comparison matched 20/20; raw bytes remain unchanged.
- The root `SHA256SUMS.txt` contains two historical direct-scanner hashes from private forensic commit `1158fdb`; private forensic commit `5fe0ee4` legitimately changed those sources. These archival identifiers are not expected to resolve in the public repository. Use `authority/manifests/CURRENT_DIRECT_SCANNER_SHA256SUMS.txt` for current source hashes.
- Historical positive-density input SHA256 `1d8bb9b45cb556d4693b568d42b10af386de88e734094d1af5f0396c9c243ff8` remains absent. It was not reconstructed.

No publication-clean repaired derivative was created during Phase 0.5. Defects are disclosed rather than silently normalized.
