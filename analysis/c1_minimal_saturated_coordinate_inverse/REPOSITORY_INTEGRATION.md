# Repository integration note

This directory is a Draft-PR intake of an authenticated web-research package.
It adds only a new analysis module below
`analysis/c1_minimal_saturated_coordinate_inverse/`; it does not modify
`STATUS.md`, workflows, authority records, or existing analyses.

The complete package is losslessly represented by ten exact base64 Git blobs
under `package_parts/`. This packaging was chosen because the active connector
supports UTF-8 Git tree writes but not a direct local binary-file upload. The
reconstructed archive is protected by the SHA-256 recorded in
`PACKAGE_PARTS.md`.

The concise files at the module root are review entry points. Where a concise
index and the authenticated package differ in level of detail, the
reconstructed authenticated package is the authoritative research artifact.

The package preserves all theorem documents, source code, tests, bounded-search
records, and hashes. The three multi-megabyte generated catalogs are omitted
from the compact Git payload but remain authenticated by the original ZIP and
are exactly reproducible from frozen code and bounds; their digests and sizes
are recorded inside the reconstructed package.

No theorem statement is promoted merely by opening this PR. Independent proof
review and repository-native replay remain required.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```
