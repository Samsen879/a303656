# Source custody and independent replay

Integrated 2026-09-14 from `A303656_N0_C279_closure.zip` in Windows Downloads.
Archive SHA256:
`47eab66e1a31e9f15349e21086275a15902a04fccf9179cda95acc66867d91ce`.
Safe-list PASS: five regular members, no unsafe paths, duplicates or symlinks.
Internal manifest: NOT PRESENT. Integration-side hashes of all original bytes
are recorded in SOURCE_RECEIPTS.json; no producer manifest PASS is claimed.
Original ZIP and extracted members are preserved, not committed or edited.

Inventory: PROOF.md documents ordinary Pocklington and the proved elementary
cubic exclusion; certificate.json contains eight recursive proof nodes and
two candidates; verify.py is the producer checker; receipt.json and
mutation_receipt.json are untrusted producer claims, not certification inputs.
No separate producer independent checker is present. Producer replay PASS.

Only certificate.json is copied byte-identically as PRIMALITY_CERTIFICATE.json
(SHA256 `cbea670f55001afeb8f6adf6005e127a905bb3d8d7ab7413d553b79a9156c2a3`).
Both repository checkers and proof/summary files are integration-authored;
closure_result.json is derived exact arithmetic. All selected exact payload
hashes and Gate A PASS are in SOURCE_RECEIPTS.json. Both independent rigorous
implementations replay PASS, before branch creation; producer PASS is only a
reproduction cross-check, never the independent certification authority.

External factor provenance CHECKED: Cunningham main table
[Table5- row279](https://homes.cerias.purdue.edu/~ssw/cun/pmain126.txt)
contains `247114592858611.P112`. Cunningham supplies candidate split provenance.
The local proof does not depend on the P112 label. Supplied Appendix/history
links remain hints only; those extra links were not independently checked.
Local primality, product identity, orders and multiplicities are independently
certified offline. No factoring search or network dependency exists in tests.

Live base main: `7945045af0ef48bdff7dc04249ca7fcf7bafdc80`;
tree: `0ac75f0aa7e3fa2f66160d7bf05065ef328d222c`. Root STATUS unchanged.
Gate A: C279_CLOSURE_CERTIFIED. Integration replay uses the commands in README.
