# Phase G B31 branching fixed-base route audit

## Authority and custody

This directory integrates the byte-preserved producer payload from
`A303656_B31_BRANCHING_PHASE_G.zip`, outer SHA256
`70257fc23dea17a752569ce88c170684cc7b6785d6213fca5e955d5c192c8b92`.
The ZIP contained 16 regular files under one root. Safe listing found no
absolute/traversal paths, duplicate members, links, or special files; all 15
entries in `SHA256SUMS.txt` verified. The ZIP is not committed.

The package is bound to main `c6ca0dc061783ab993be6fa077c8f66cd730e28c`,
tree `57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06`. Repository-source
reconciliation, including Phase F Theorems F2/F4, is recorded in
`DEPENDENCY_BINDING.json`; merged repository authority controls any conflict.

## Accepted role

This is a `B31 FIXED-BASE NECESSITY / GENERAL ROUTE AUDIT`, not a B31
emptiness theorem. The accepted route-pruning conclusions are:

- maximal-generator reciprocity sign constraints alone do not contradict the
  B31 order DAG;
- ordinary tame higher-power residuacity does not encode the q-primary,
  modulo-q-squared terminal square hit;
- the certified variable-base countermodels preserve only the explicitly
  audited first-order order/DAG/residue data while changing terminal
  regularity or nonregularity;
- consequently a future universal obstruction must add genuinely fixed-base-5
  or q-squared-sensitive arithmetic beyond those preserved generic invariants.

The negative scope is exactly the invariant set checked by `verify.py`. It does
not rule out all reciprocity, higher-reciprocity, norm, or cyclotomic-unit
methods. Infinite regular extension remains compatible with B31 emptiness; the
route audit neither establishes nor refutes that emptiness.

## Replay and mutation mapping

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_integration.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v tests/test_integration_scope.py
```

The isolated replay runs in normal and optimized modes. Required mutation
classes map to producer controls as follows: broken order to
`corrupt_exact_order`; broken all-odd flag to `terminal3_in_all_odd_rows`;
broken edge relation to `drop_maximal_generator`; broken residue symbol to
`wrong_edge_sign`; fake nonregular status to `fake_base5_member`.

The optional 80,000-candidate discovery replay regenerates the same count and
empty hit list. Its frozen file contains additional hand-authored scope fields
and an environment-specific time, so byte identity is neither expected nor
used as theorem evidence.

## Nonclaims and project state

```text
B31^odd EMPTY: NOT PROVED
ACTUAL B31^odd MEMBER: NONE
GLOBAL FINITE CRITICAL FAMILY: NOT PROVED
EXACTLY-SEVEN: NOT KILLED
N>=8: NOT PROVED
A303656: UNRESOLVED
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
```
