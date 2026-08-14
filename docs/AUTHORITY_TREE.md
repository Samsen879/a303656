# Authority tree

The repository separates immutable evidence from derived public views.

```text
authority/
├── frozen/
│   └── FREEZE_RECEIPT.json
├── candidates/
│   ├── ...V2_CANDIDATE.zip
│   └── ...V2_FINAL_FREEZE_CANDIDATE.zip  ← frozen by receipt
├── raw/
│   └── immutable historical/source authority ZIPs
├── audits/
│   ├── independent audit ZIPs
│   └── Master V1 pre-final ZIP
└── manifests/
    ├── WEB_AUTHORITY_CUSTODY.json
    └── scoped current-source manifests
```

## Precedence

1. The frozen web-accepted mathematical scope.
2. Exact raw artifact bytes and SHA256 identities.
3. Independent audit artifacts.
4. Frozen Master V2 ledgers and freeze receipt.
5. Generated public indexes.
6. Historical repository reports and exploratory notes.

A generated index never upgrades a theorem. A local report never replaces the frozen authority. A repaired derivative never impersonates its raw parent.

## Why the frozen ZIP still says “candidate”

The exact bytes were produced before independent acceptance. After exact-hash review, the accepted bytes were frozen through `FREEZE_RECEIPT.json`. Rebuilding the ZIP merely to change the internal status would create a different, unaudited object.
