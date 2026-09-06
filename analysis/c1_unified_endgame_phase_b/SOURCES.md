# Source binding and reading scope

All repository file links below are pinned to
`44e522dd6e88504e2b9829f0b27359e6c45a76ff`.

## Live authority reads

GitHub connector reads confirmed PR #14, #15 and #16 as merged, the main branch
SHA and tree, and the pinned STATUS.md. A later `refs/heads/main` read returned
the same SHA. No write actions were invoked.

- Repository: https://github.com/Samsen879/a303656
- PR14: https://github.com/Samsen879/a303656/pull/14
- PR15: https://github.com/Samsen879/a303656/pull/15
- PR16: https://github.com/Samsen879/a303656/pull/16
- Pinned STATUS: https://github.com/Samsen879/a303656/blob/44e522dd6e88504e2b9829f0b27359e6c45a76ff/STATUS.md

## Mathematical sources

**[S0] STATUS.md.** Project state, authority boundary, and absence of a general
proof or certified counterexample. Entire file read.

**[S1] Original formal class.**
`analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md`.
Git blob: `2a788348cf9abdce43f47809b7b6fd6cb8f3f04d`.
Entire file read. Defines admitted rows, coarse fatality, periods, boundary
handling, coordinate deficit and order dependency.

**[S2] PR11 common-residue report.**
`analysis/c1_two_anchor_common_residue_phase_a/REPORT.md`.
Git blob: `2711299b58f5c3b9f67c117af0df4ae3cd3357ec`.
Lines 1--205 read, including dynamic same-lower exclusion and common-fiber
rigid-only classification.

**[S3] PR12 arithmetic realizability report.**
`analysis/c1_prefix_frontier_realizability_phase_a/REPORT.md`.
Git blob: `cb2f117f5b2e3f2bdd54f4bfe11f6414eed4570b`.
Lines 50--455 read. Includes original definitions, dynamic parity, centered
frontier classification, final induced ambient gate, and the one-anchor
necessity/sufficiency proof. The old original inverse-theorem source paths
listed there were not all downloaded afresh as separate local files.

**[S4] PR13 hereditary shell report.**
`analysis/c1_hereditary_shell_phase_a/REPORT.md`.
Git blob: `260d7160f6b2321cdc6f7f1212986b898461980e`.
Lines 60--255 read: guarded-slice factorization, exact cover clauses, hereditary
provenance grammar and its distinction from original-prime realizability.

**[S5] PR14 two-root provenance report.**
`analysis/c1_two_root_provenance_phase_a/REPORT.md`.
Git blob: `5b816092c33ea53078c9422482edd223a13b5bc3`.
Lines 1--380 read, together with the merged PR metadata/body. Includes blocker
escape, joint reverse CRT, uniform capacity assignment, charge/configuration
formulation and failed naive macro invariants.

**[S6] PR15 synchronization report.**
`analysis/c1_two_anchor_sync_phase_a/REPORT.md`.
Git blob: `382cc8069efb7f7d1eab9ad8fb92e1cb0ddd1568`.
The first report fetch exposed the opening definitions and theorem ladder;
explicit subsequent reads covered lines 220--420 and 440--610. These include
S1--S4 proofs, abstract complete countermodels, actual SPLIT, and the scope of
pooled-lower obligations.

**[S7] PR16 Kraft--Hall report.**
`analysis/c1_kraft_hall_phase_a/REPORT.md`.
Git blob: `c7c41d7432255b437b3a9fbdcc8d5b4ccc2a080f`.
Lines 1--565 read. Includes resource definitions, active Kraft, corrected
ancestor accounting, one-anchor converse, configuration inequalities,
cyclotomic exclusions, paired graph/resultant and joint scope limits.

Each path resolves under the pinned URL prefix
`https://github.com/Samsen879/a303656/blob/44e522dd6e88504e2b9829f0b27359e6c45a76ff/`.
The paths and blob identifiers are also machine-recorded in
`results/source_binding.json`.

## What was and was not authenticated

The above Git blob identities came from GitHub connector metadata. Full source
files were not assembled into a local Git checkout, and their Git hashes were
not independently recomputed from a local complete source archive. This bundle
therefore does not claim a repository-wide integrity audit, replay of all old
results, or coverage of every historical report.

The new laboratory does not import repository code. It rechecks specific exact
arithmetic identities and examples using the standalone source in this bundle.
Different mathematical representations are cross-checked, but this is one
author/environment, not two independently staffed implementations.

The SHA-256 hashes of the user-provided task and project text files are recorded
as input custody only. Those project files are not republished in the bundle.
