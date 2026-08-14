# Direct scanner provenance contract

This contract applies to every new formal test/reproduction output from
`search_twosquares_bitset` and `search_twosquares_clean`. It does not authorize
regenerating legacy certified outputs.

## Fixed identities

| Slot | `implementation_id` | Executable | Method |
|---|---|---|---|
| x | `search_twosquares_bitset` | `search_twosquares_bitset` | `direct_two_squares_bitset_x_outer` |
| y | `search_twosquares_clean` | `search_twosquares_clean` | `clean_room_direct_two_squares_y_outer` |

The identities are not interchangeable. Mathematical equality of two JSON
files does not satisfy this contract if both came from one implementation.

## Required manifest binding

An adjacent `a303656-direct-scanner-provenance-v1` manifest records and the
auditor verifies:

- implementation id and method;
- executable filename, absolute path, and SHA256;
- source filename, absolute path, SHA256, and exact Git commit;
- compiler command and full compiler version;
- GMP version used by the independent oracle/toolchain record (the two direct
  scanner executables themselves do not link GMP);
- exact scanner CLI argument vector;
- `low`, `high`, `C`, and `D`, identical in CLI, manifest, and output;
- UTC generation timestamp, scanner return code, and elapsed seconds;
- output, candidate sidecar, stdout, and stderr paths plus SHA256 values.

The auditor also requires distinct x/y executable hashes and distinct x/y
source hashes, the same interval in both slots, matching mathematical fields,
consistent candidate sidecars, and the scanner's documented 0/1 return-code
convention. Missing files, fields, hashes, or identities fail closed.

## Required generation and audit

Use `src/direct_scanner_provenance.py run` separately for x and y. Then use
`audit-pair` with both manifests and the expected exact source commit. Raw
stdout, stderr, return codes, and elapsed time of these commands must be stored
by the command logger.

A qualifying test suite must also demonstrate both negative cases:

1. put the y manifest in the x slot and the x manifest in the y slot; the audit
   must return nonzero and identify an implementation identity/provenance
   mismatch;
2. change an output without changing the recorded hash; the audit must return
   nonzero and identify an output SHA256/provenance mismatch.

The harness counts an expected rejection as PASS only after explicitly checking
the nonzero return code and the diagnostic. It restores the original output and
reruns the positive audit afterward.

## Build correspondence

The manifest is necessary but not sufficient by itself to prove compiler
provenance. The accompanying clean-build log must therefore:

- start from a named Git commit in a new isolated source directory;
- reject an existing build directory;
- record exact compiler/linker commands and versions;
- hash the source and resulting binaries;
- record GMP package/archive hash, extraction/include/library paths, and linked
  runtime version for the independent oracle;
- record `ldd` and/or `readelf` output;
- preserve every command, stdout, stderr, return code, and elapsed time.

Together, the isolated build record, source hashes, binary hashes, and output
manifests bind the tested executable to the reviewed source as far as this
repository's reproducibility process can establish. This is computational
provenance, not a formal proof of compiler correctness.

## Legacy baseline

Stored certified outputs predate this schema. They contain distinct method
strings and runner summaries with scanner/source hashes, but they are not
retrofitted with new fields because changing them would violate baseline
preservation. New runs must use this contract; old artifacts retain their
existing, explicitly weaker provenance classification.
