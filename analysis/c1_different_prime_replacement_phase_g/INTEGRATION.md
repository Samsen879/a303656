# Phase G different-prime replacement route audit

## Authority and custody

This directory integrates the byte-preserved producer payload from
`A303656_DIFFERENT_PRIME_REPLACEMENT_PHASE_G.zip` (SHA256
`9bd8afb6cda33bae6e6d066f4bda33f2b10a9a67b8fe89fcbaa1ce0167f206b5`).
The archive was safely listed, contained 14 regular files under one root, had
no absolute/traversal paths, duplicate members, links, or special files, and
its 13-entry `SHA256SUMS.txt` verified. The transport ZIP is not committed.

Integration base: `c6ca0dc061783ab993be6fa077c8f66cd730e28c`, tree
`57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06`. Dependency reconciliation is
recorded in `DEPENDENCY_BINDING.json`; merged repository authority wins over
any broader producer wording.

## Accepted mathematical role

Within a hypothetical actual complete exactly-seven normal-form certificate,
the B7 basin contains the 7-gateway and the seven original-root basins are
pairwise disjoint. Therefore a different original nonregular root in that
same certificate cannot supply a second B7 exact state. This conditional
in-certificate theorem does not assert that such a certificate exists.

Separately, the supplied finite abstract model satisfies the stated structural
reduct while having no cheaper external nonregular B7 replacement. Its formal
endpoint atoms and formal square-hit marks are not primes or divisibility
claims. Thus certificate-specific different-prime SQD is not derivable from
the current structural authority alone.

`ABSTRACT MODEL != ACTUAL ARITHMETIC CERTIFICATE`.

Route status: `DEAD AT CURRENT STRUCTURAL AUTHORITY`. This is not a claim that
the route is mathematically impossible in fixed base 5. External base-5
arithmetic forcing remains unresolved. Same-root migration is already
impossible by Phase F and is not a new Phase G theorem identity.

## Replay

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_integration.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v tests/test_integration_scope.py
```

The integration verifier checks the producer manifest and inventory, binds the
merged dependencies, replays the source in an isolated temporary directory,
and requires all 12 producer mutation controls to be rejected.

## Nonclaims and project state

```text
B7 EMPTY: NOT PROVED
EXACTLY-SEVEN: NOT KILLED
N>=8: NOT PROVED
A303656: UNRESOLVED
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
```
