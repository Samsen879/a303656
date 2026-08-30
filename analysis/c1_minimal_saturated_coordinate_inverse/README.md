# Minimal saturated odd-coordinate inverse classification — Phase A

This Draft-PR module prepares the local inverse theorem for independent
repository review. It does not promote a project route and does not claim a
complete `C=1` certificate or a solution of A303656.

## Review entry points

- `DEFINITIONS.md`: the three-layer formal model and minimality conventions;
- `ABSTRACT_CLASSIFICATION.md`: a concise theorem index and package locator;
- `COUNTEREXAMPLES.md`: exact adversarial separations and failure modes;
- `PACKAGE_PARTS.md`: deterministic reconstruction and validation commands;
- `REPOSITORY_INTEGRATION.md`: provenance and connector-transport boundary.

The complete authenticated package—including `REPORT.md`, the full theorem
proofs, `REALIZABILITY_AUDIT.md`, all three reference implementations, tests,
compact result records, manifests, and internal hashes—is losslessly stored in
`package_parts/`. Run:

```bash
python3 unpack_repository_package.py /tmp/a303656-coordinate-inverse
cd /tmp/a303656-coordinate-inverse/package
```

The reconstructed `tar.xz` has SHA-256:

```text
1aba57b1b27f9564e840f2271b50a3090598e18266c300142d77bde0f3276efc
```

The originating web-research ZIP has SHA-256:

```text
cf6e7a5dfb6287129fa1df501e4691c0d10fe2163d3572a2ca4502947fbaf9f1
```

## Structural result under review

The package proves, subject to independent referee review:

1. an exact rational deletion-minimal classifier `0 <= Delta < mu`;
2. the unique two-atom equality `D_1 + R_1 = 1`;
3. complete beta-one and beta-two exact-cover classifications;
4. an arbitrary-beta parameterized prefix-frontier inverse theorem;
5. an effective template-count recurrence;
6. an exact deduction from a complete admitted certificate to the occurrence,
   at some odd coordinate and fixed lower assignment, of a pointwise minimal
   classified frontier.

The package strictly separates:

```text
abstract rational budget
!= exact fiber cover
!= arithmetic realizability
!= complete two-anchor certificate
```

The local package verdict is:

```text
PROMOTABLE INVERSE THEOREM
```

Here `PROMOTABLE` means suitable for independent theorem review and possible
repository integration. It is not an authority-state change.

## Validation

From `/tmp/a303656-coordinate-inverse/package`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/integrity.py verify --root .
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/run_tests.py --root .
rm -rf tools/__pycache__ tests/__pycache__
PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/integrity.py verify --root .
```

The authenticated intake passed `24/24` tests, exact-fraction checks,
local-zero fail-closed tests, corruption tests, and deterministic replay.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```
