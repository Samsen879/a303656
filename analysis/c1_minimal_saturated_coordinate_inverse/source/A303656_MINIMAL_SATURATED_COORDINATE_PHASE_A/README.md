# A303656 minimal saturated odd-coordinate inverse classification — Phase A

## Verdict

```text
PROMOTABLE INVERSE THEOREM
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

This package gives a clean inverse theorem for the odd rational-prime coordinate mechanism behind

```text
D_{l,c}+R_{l,c} >= 1.
```

The main advance is stronger than the rational budget condition.  A complete finite admitted coarse certificate, at the anchor supplied by the existing two-adic lemma, must encounter an **actually covered odd `l`-adic fiber** during increasing-coordinate greedy selection.  Every fiberwise irredundant subcover of that fiber has an exact parameterized form:

1. one and only one rigid cylinder contains a fixed lift of the unresolved dynamic center;
2. every remaining rigid cylinder lies in an unaccepted side branch before that centered depth;
3. those side cylinders form independent complete `l`-ary prefix-code frontiers;
4. the dynamic row is essential exactly when it accepts a shell before the centered depth;
5. accepted shells at or beyond the centered depth are the only possible overlaps and have multiplicity two.

Thus a depth-independent finite list of literal templates is false, but fixed `beta` has a finite exact catalog and arbitrary `beta` has an effective recurrence.

This is not a complete `C=1` certificate, not a no-go theorem for all certificates, not a sum-of-two-squares theorem, and not a solution of A303656.

## Files

- `REPORT.md` — final audit and theorem ladder.
- `DEFINITIONS.md` — exact formal model and separation of levels.
- `ABSTRACT_CLASSIFICATION.md` — proofs of the rational and exact-cover inverse theorems.
- `REALIZABILITY_AUDIT.md` — order, lifting, common-residue, both-anchor, and local-zero constraints.
- `COUNTEREXAMPLES.md` — adversarial examples and hashes.
- `tools/rational_template_enumerator.py` — exact rational catalog.
- `tools/fiber_cover_checker.py` — exact fiber templates and bounded independent brute force.
- `tools/arithmetic_realizability_checker.py` — frozen actual-prime scan and known-pair checks.
- `results/` — generated machine-readable outputs; no generated JSON is hand-edited.
- `manifest.json`, `SHA256SUMS.txt` — internal integrity data.

The sealed test report records 26 passing tests.  The archive SHA-256 is emitted beside the ZIP so that the payload does not contain a self-referential checksum.

## Deterministic replay

From the package root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/reproduce.py --root .

python3 tools/verify_package.py --root .
```

Create the byte-deterministic ZIP:

```bash
python3 tools/make_zip.py \
  --root . \
  --output ../A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A.zip
```

The ZIP uses `ZIP_STORED`, sorted paths, fixed `1980-01-01 00:00:00` timestamps, and fixed Unix permissions.

## Frozen computations

- rational catalogs: `l in {3,5,7}`, denominator depth at most `5`, atom count at most `12`;
- rational independent brute force: `l=3`, depth at most `3`, at most `4` rigid atoms per depth;
- complete parameter-labelled fiber templates: `l=3, beta<=3` and `l=5, beta<=2` (labels retain `m` and `s_l` parity);
- independent cylinder-subset brute force: `l=3, beta=2`;
- independent constant-boundary replay: the frozen `K_2=2`, `U=5` obstruction;
- actual-prime scan: every prime `q<=500000` with `q==3 (mod 4)`, `q!=5`;
- known nonregular panel replay: `20771`, `40487`, `1645333507`.

Bounded absence is never promoted to a universal theorem.

## Authority binding

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 29fee0317b268d2b2747f9564efc445fdd6da7f9
main tree: 0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55
```

No GitHub, Issue, branch, commit, PR, workflow, or authority state was modified.
