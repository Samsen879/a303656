# Public/private provenance boundary

This public repository is a sanitized export with a deliberately new Git history. The complete research history is preserved separately as private forensic evidence because historical Git commit metadata contains personal information.

Commit identifiers described as **private forensic** are archival cross-references. They are retained to make custody reports intelligible, but they are not expected to resolve in this public repository and do not identify public commits.

Public scientific identity and authority are instead bound by:

1. the artifact filename;
2. the artifact SHA256 digest;
3. the relevant manifest and custody ledger;
4. the exact-hash freeze receipt in `authority/frozen/FREEZE_RECEIPT.json`.

The sanitized export does not rewrite, replace, or claim to reproduce the private historical commit graph. It also does not retroactively establish missing generation provenance. Raw authority bytes remain immutable, repaired derivatives require distinct hashes and explicit lineage, and A303656 remains **UNRESOLVED**.
