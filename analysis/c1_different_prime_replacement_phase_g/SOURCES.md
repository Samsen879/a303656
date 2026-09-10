# Source register — pinned immutable authority

All paths below refer to `Samsen879/a303656` at commit `c6ca0dc061783ab993be6fa077c8f66cd730e28c`, tree `57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06`. The final live branch recheck was unchanged. Each required PR was individually checked with `merged=true`; the exact merge receipts are in `SOURCE_BINDING.json`.

These are connector-based readings, not a full local checkout or independent upstream byte/hash replay. The core mathematical texts listed as full were read through overlapping ranges to address truncated long responses. **All auxiliary/generated files of the five required directories were not read.** No repository-native tests or historical large computations were replayed.

## [S1] `STATUS.md`

Git blob: `2ba295c0ada0d19b4e7f7d7871312d0696a785d2`.

Read scope: full.

Use: PAUSED/NONE/UNRESOLVED; no large computation authorization.

## [S2] `analysis/c1_order_dag_phase_c/THEOREMS.md`

Git blob: `0c86de426dc932a13a4d7cccb198e4ef3bd7c811`.

Read scope: full mathematical text.

Use: Theorems7.1-7.2: seven-origin normal form, disjoint full basins, proper regular descendants; Theorem12.1 conditional completion; inventory corollary scoped.

## [S2R] `analysis/c1_order_dag_phase_c/REPORT.md`

Git blob: `b5af58bdef3624042a43072aede255d9d4f400ea`.

Read scope: full report via overlapping ranges.

Use: Chinese explanation of source normal form and nonclaims.

## [S3] `analysis/c1_b7_branching_phase_e/THEOREMS.md`

Git blob: `cd57a36f00ff8dcb63bc7efebf979097b6f6e9af`.

Read scope: full mathematical text.

Use: E1 exact support closure; E2 maximal antichain; E3/E3.1 exact square-hit iff; E6 actual regular diamond; E8 scope.

## [S3R] `analysis/c1_b7_branching_phase_e/REPORT.md`

Git blob: `790e231ae40865cfd09aef8b2432338920c110da`.

Read scope: full report via overlapping ranges.

Use: Closed-state, finite-size and provider interfaces.

## [S3A] `analysis/c1_b7_branching_phase_e/PROOF_AUDIT.md`

Git blob: `02bff9f2d44313f3bd7efe858049a06f561640cd`.

Read scope: full.

Use: Regular vs nonregular, exact states vs ambient, abstract model vs arithmetic, read/replay boundaries.

## [S4] `analysis/c1_closed_state_sqd_phase_f/REPORT.md`

Git blob: `c4643ec5ce8c2e52e01e6a62bfa347b99b8da640`.

Read scope: full report via overlapping ranges.

Use: F4 exact-root iff; F6 coprimality/no migration; stopping rule; certificate-specific successor-domain gap.

## [S4B] `analysis/c1_closed_state_sqd_phase_f/DEPENDENCY_BINDING.json`

Git blob: `6da0bd3b5ad49f247783a4989841b70f784728d0`.

Read scope: full.

Use: Merged reconciliation of exact symbols with PhaseE; BOUND_TO_MERGED_REPOSITORY.

## [S5] `analysis/c1_private_provider_charging_phase_d/THEOREMS.md`

Git blob: `005b893f25d19695eb77adbf0cbbbf09efb56597`.

Read scope: full mathematical text.

Use: D1 center ancestry; D2 support confinement; D3/D4 frozen simultaneous width; D5 equality7=7.

## [S5R] `analysis/c1_private_provider_charging_phase_d/REPORT.md`

Git blob: `da6c7b743fd6995895b6ad53f79197b1a6ad0767`.

Read scope: full report via overlapping ranges.

Use: Provider witness, hybrid release and common-state distinctions; model scope.

## [S6] `analysis/c1_seven_basin_global_shared_state_phase_e/REPORT.md`

Git blob: `d85dca43ca3184ffe5f26534673e2ea037ea9e42`.

Read scope: full mathematical report via overlapping ranges.

Use: E1 arbitrary-basin filling; E2 one-state CRT; E3 parity persistence; E4 O31; E5 full BOTH sufficiency for actual prescribed arithmetic basins allowing legal K/E.

## [S7] `analysis/c1_b31_odd_phase_f/REPORT.md`

Git blob: `eb0777a6593ab72711187d0c57403d7784dba79a`.

Read scope: partial: opening verdict and normal-form/O31 reconstruction, requested lines1-190 (long output truncated).

Use: First-relay summary used only as provenance for chosen actual regular labels; fresh certificates supplied in this package.

## Authority reconciliation

The older PhaseF producer report states that PhaseE source packages were not available in that producer session. This is historical provenance, not the final integration status. The currently merged `DEPENDENCY_BINDING.json` explicitly maps good state, closure, A, J, W, Z and primitive normalization to PhaseE, reports PASS, and marks the dependency BOUND_TO_MERGED_REPOSITORY. PhaseE owns closed-state theory; PhaseF owns normalized coprimality/no-migration.

## Arithmetic vs structural authority

S6 E5 is sufficient only for prescribed **actual** arithmetic basins, with legal state choices permitted. In this package it is used as an actual conditional theorem in G3. In the finite countermodel, its event-algebra construction is separately specified and checked under formal root kernels; that use is not a claim that S6 has instantiated the seven roots.

The numerical regular labels in the new countermodel are verified by new frozen certificates. The finite model is not a new factorization ledger for the unknown terminal integers, nor a replay of every arithmetic restriction elsewhere on current main.
