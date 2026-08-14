# Phase 0 finding disposition

| Finding | Disposition | Evidence |
|---|---|---|
| 17 exact-match web artifacts | RESOLVED | Imported under authority/raw with exact hashes and Git custody. |
| 3 locally missing web artifacts | RESOLVED | Exact downloaded bytes imported; hashes/CRC pass. |
| Master V1 pre-final scope | RESOLVED_FOR_CANDIDATE_PREPARATION | Preserved as pre-final; V2 candidate remains pending web freeze. |
| 2 root manifest mismatches | RESOLVED | Stale manifest after legitimate tracked 5fe0ee4 update; current manifest added. |
| 20 nested manifest mismatches | RESOLVED_SEMANTICALLY_NOT_BYTEWISE | 12 logs + 8 JSON; scientific payload 20/20 match; raw ZIP preserved. |
| 48 physical illegal bytes | RESOLVED_AS_DISCLOSED_RAW_DEFECTS | 12 logical defects; no raw repair. |
| authority untracked at frozen HEAD | RESOLVED_FOR_REPOSITORY_CUSTODY | Imported on reconciliation branch; historical generation provenance remains missing. |
| CRW/N-004/finite Markdown/recursive scan | PENDING_MASTER_V2 | Resolved by V2 generator/validator phase. |
