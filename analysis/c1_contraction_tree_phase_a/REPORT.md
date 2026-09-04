# Final report

## 1. Exact authority binding

The task was executed against the immutable GitHub state:

```text
repository: Samsen879/a303656
repository ID: 1333945235
main SHA: 29fee0317b268d2b2747f9564efc445fdd6da7f9
main tree: 0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55
```

The SHA and tree were verified before mathematical work.  No GitHub repository, Issue, branch, commit, PR, workflow, or history was modified.

The bound status remains:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

## 2. Dependency lemmas independently checked

The following prior dependencies were reconstructed rather than accepted by label:

1. prime-power lifting
   `ord_(p^K)(5)=w_p p^max(0,K-s_p)`;
2. rigid/dynamic fatal normal form, including the unresolved zero center;
3. arbitrary-entanglement reverse CRT;
4. strict ascending order-dependency DAG;
5. exact beta-one aligned pair contraction;
6. the three two-adic regimes.

Direct multiplicative-order tests, full-period enumeration, reverse-CRT escape comparison, and square-sum residue enumeration passed.  See `PROOF_DEPENDENCIES.md` and `results/dependency_recheck.json`.

## 3. Formal contraction state

`DEFINITIONS.md` defines:

- contraction state and provenance;
- active lower cylinder;
- unresolved center;
- rigid-shell alignment;
- actual saturation set;
- exact contraction edge;
- general and admitted residual systems;
- contraction depth and rank;
- terminal/root cover;
- soundness invariant;
- hereditary exact shell decomposability.

The invariant preserves common residues, fail-closed local zeros, accepted valuation parity, exact periodicity, reverse-CRT meaning, and anchor tags.

## 4. Termination verdict

The ascending DAG is sufficient for triangular dependence, but not by itself for an arbitrary syntactic rewrite.

Exact maximal-coordinate contraction terminates because every edge removes one coordinate.  Its depth is at most the number of prime coordinates.  A point-cylinder tree has at most

```text
sum_{k=1}^m product_{i<k} |X_i|
```

saturated internal fibers, hence a crude `<=(m+1)U` total bound.

Additional requirements for a row-level procedure are strict rank descent, finite branching, full removal of the contracted coordinate, and branch-local event reuse.

Semantic universal projection is confluent; naive global pair consumption is not.

## 5. Completeness-to-contraction verdict

The chain splits as follows:

```text
complete simultaneous certificate
=> actual saturated odd fiber for a selected anchor       PROVED SEMANTICALLY

density saturation D+R>=1
=> actual fiber coverage                                  FALSE

actual fiber coverage
=> beta-one aligned pair                                  FALSE IN ABSTRACT GRAMMAR

aligned beta-one pair
=> sound lower contraction                                PROVED

exact contraction
=> residual remains admitted                              NOT PROVED
```

Therefore the candidate is true only under an exact semantic reading that allows arbitrary lower macro-events.  The strong admitted-class reading requires an extra structural hypothesis.

## 6. Counterexample and corrected theorem

### Explicit arithmetic defect

For the admitted fixed-anchor `67/20771` pair:

```text
aligned rigid digit: union 67/67;
misaligned rigid digit: budget 1 but union 66/67.
```

Both formal lower residual congruence systems are the same after deleting the `67` factor.  Alignment is therefore independent data required for soundness.

### Smallest abstract counterexamples in the enumerated grammar

- coordinate size `3`: density budget `1` without coverage;
- coordinate size `3`: exact cover by three rigid singletons without a beta-one pair;
- coordinate size `9`: beta-two center requiring three rigid singleton shells.

### Corrected theorem

Every finite complete triangular cover has a finite exact semantic contraction tree.  A compact admitted-class tree follows conditionally from hereditary exact shell decomposability with branch-local reuse and admitted residual closure.

This is Outcome C together with an unconditional semantic theorem.

## 7. Exact computation domain

No unbounded prime search was performed.

Arithmetic domains:

- `11 -> 67 -> 20771` full period: `228470` exponents;
- exact `d==0 mod 310` chain cylinder: `737` exponents;
- aligned and misaligned `67`-fibers: `67` digits each;
- local-zero period: `6` exponents;
- two-adic boundary periods: `55` and `110`;
- every common residue modulo `2^K` for `K=2,...,10`, with exact two-anchor unsafe-density counts.

Abstract domains:

- odd coordinate sizes through `11` for density/coverage search;
- odd coordinate sizes through `9` for no-beta-one cover search;
- exact `3^2` multiple-shell model;
- all `4096` subsets of a `2 x 3 x 2` product for projection-order invariance.

All rational densities are stored as exact numerator/denominator pairs.

## 8. Test results

The deterministic suite contains `15` tests covering:

- lifting formula;
- reverse CRT;
- full-period chain replay;
- aligned/misaligned soundness;
- local-zero fail-closed behavior;
- deliberate corruption detection;
- no two-adic row;
- `K_2=2` safe and unsafe constant boundaries;
- `K_2>=3` genuine coordinate hazard;
- exhaustive two-anchor lemma replay for all residues through `K_2=10`;
- semantic contraction soundness;
- beta-one and beta-two counterexamples;
- residual nonclosure;
- branch-local reuse;
- exhaustive order invariance.

The generated result is `results/test_results.json`.

## 9. Deterministic hashes

- Internal file hashes: `SHA256SUMS.txt`.
- Machine-readable file manifest: `manifest.json`.
- Outer deterministic ZIP hash: adjacent external `.zip.sha256` sidecar.

The ZIP is generated with sorted paths, normalized permissions, fixed timestamps, and standard-library `zipfile` archiving (`ZIP_STORED`).  Generated results, manifest, and checksums are produced by scripts and are not manually edited.

## 10. Unresolved logical gaps

1. Completeness has not been shown to imply hereditary exact shell decomposability.
2. Exact saturation sets need not remain in the admitted row grammar.
3. Multiple-shell and `beta_p>1` arithmetic classification remains open.
4. No compact effective bound in the number of rows, rather than in `U`, was obtained.
5. No invariant prevents both fixed-anchor roots from being covered.
6. A common two-anchor contraction tree is not implied by two separate fixed-anchor trees.
7. No local escape is promoted to an actual sum-of-two-squares representation.
8. No complete finite `C=1` certificate was found or ruled out.

## 11. Recommendation for repository integration

Recommend a **repository integration audit**, not direct theorem promotion.

Potentially integrable objects:

1. exact semantic triangular contraction theorem;
2. actual-odd-saturated-fiber corollary for the two-adically selected anchor;
3. aligned/misaligned `67/20771` counterexample as a mandatory regression test;
4. branch-local reuse requirement;
5. hereditary exact shell decomposability as the next structural gate.

Do not integrate wording that says completeness automatically yields a beta-one tree or an admitted residual system.  A repository-native implementation should be independent of this Python code and should replay the frozen examples before any stronger claim.

## 12. Final verdict

```text
TARGETED PARTIAL ADVANCE
```

The phase identifies a rigorous semantic tree theorem, proves a real arithmetic defect in the density-to-alignment bridge, and isolates the exact missing structural hypothesis.  It does not establish a complete certificate or a universal no-go.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```
