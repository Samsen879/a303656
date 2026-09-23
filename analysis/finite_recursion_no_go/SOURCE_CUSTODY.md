# Source custody

Selected transport artifact:

```text
Source location: Windows Downloads directory
Requested name: a303656_thread3_bundle(1).zip
Actual located name: a303656_thread3_bundle.zip
Size: 43,476 bytes
mtime: 2026-09-21 19:34:00.811239800 +0800
SHA256: b9e7b1d4acd0cb99d5dd0965aa0c900ae4228c3cffe886af75854405eba2e0c5
ZIP CRC test: PASS
Internal SHA256SUMS.txt: PASS for all seven covered members
```

The eight original archive members are preserved byte-for-byte under
`source/producer_packet/`.  The producer script remains a comparison
implementation and is not imported by `tools/reference_audit.py`.

The packet was extracted only in a temporary directory before integration.
No packet member was executed against repository paths.  The producer replay
wrote its regenerated certificate to `/tmp`.
