# OEIS A303656: computations and proof-route audits

In 2018 Zhi-Wei Sun conjectured ([OEIS A303656](https://oeis.org/A303656)) that every integer `n > 1` can be written as

```text
n = a² + b² + 3ᶜ + 5ᵈ,  with a, b, c, d ≥ 0.
```

The conjecture had previously been verified for all `1 < n ≤ 2.4 × 10¹¹` (Jiao-Min Lin, reported by Sun on OEIS in 2022). This repository extends that verification, maps which proof strategies fail and why, and keeps every claim tied to the evidence behind it.

> **Current status: UNRESOLVED.** There is no general proof and no certified counterexample. Active work is paused; see [STATUS.md](STATUS.md).

## Main results

### Finite verification beyond 2.4 × 10¹¹

Two independently written C++ scanners enumerate the original representation directly. Both checked every integer in

```text
240000000001 ≤ n ≤ 241600000000
```

that is, the 1.6 billion consecutive integers immediately after the previously verified bound, and found no counterexample. Across the five explicitly manifested datasets, independent implementations cover at least 1.853 billion distinct integers. These are exact finite computations and are not a proof of the conjecture. See [Finite computations](docs/FINITE_COMPUTATIONS.md) for every interval and domain.

### Structural results and route closures

The [theorem index](docs/THEOREM_INDEX.md) records 18 results, each with an explicit scope limit:

- **5 proved results.** For example, a positive proportion of every sufficiently large dyadic interval has at least order `(log X)^(3/2)` representations. This result is largely subsumed by work of Radomskii and implies neither an almost-all nor a universal result.
- **3 conditional implications.** For example, a proved high-cutoff bad-tail bound, combined with one further hypothesis that is still open, would give an exceptional set of size `o(X)`.
- **10 negative structural theorems.** Each one shows that a specific proof route cannot work as stated. Examples include finite-state affine descent, uniform private-witness suppression, and the audited theta-series pointwise route.

Later audits closed further routes, including an exact falsification of one minimal-counterexample transfer lemma at `m = 7,963,079` and a no-go result for fixed-complexity rational recursions. See [STATUS.md](STATUS.md) and the [route map](docs/ROUTE_MAP.md).

### How the results were produced and checked

The proofs and route audits were developed with AI models and cross-checked by separate AI models. These are the "independent audits" referred to throughout the repository. No human mathematician has reviewed them, they have not been refereed, and they have not been formalised in a proof assistant. Please read them as carefully scoped candidate arguments. The finite computations are reproducible from source.

## Start here

- [Project status](STATUS.md): what is established, what is not, and why work is paused
- [Theorem index](docs/THEOREM_INDEX.md) and [route map](docs/ROUTE_MAP.md)
- [Finite computations](docs/FINITE_COMPUTATIONS.md)
- [Reproduction guide](REPRODUCE.md)
- [Post-freeze theorem and route index](docs/POST_FREEZE_THEOREM_AND_ROUTE_INDEX.md)
- [Detailed historical report (Chinese)](REPORT_zh.md). Paths it cites at the root now live under [`archive/runs/`](archive/runs/README.md).

## Quick verification

The default check is network-free and does not rerun the multi-billion search:

```bash
python3 scripts/verify_public_repository.py
```

It verifies the frozen record's hash, archive and manifest rules, ledgers, scope guards, and the generated documentation. [REPRODUCE.md](REPRODUCE.md) describes the optional finite-computation replays, from a quick stored-evidence check up to the full 1.6-billion-integer scan.

## Evidence labels

Every result carries one label, so finite, conditional and proved claims are never mixed. The labels are `PROVED`, `PROVED NEGATIVE STRUCTURAL THEOREM`, `ACCEPTED CONDITIONAL IMPLICATION`, `CERTIFIED FINITE COMPUTATION`, `INDEPENDENTLY AUDITED FINITE COMPUTATION`, `SPECULATIVE WATCH`, `STOPPED ROUTE`, `SUPERSEDED`, `ARTIFACT DEFECT` and `UNRESOLVED`.

## Frozen record and provenance

The accepted state of the project is a single archive, `MASTER AUTHORITY V2`, frozen by SHA256 in [`authority/frozen/FREEZE_RECEIPT.json`](authority/frozen/FREEZE_RECEIPT.json):

```text
3033149749b1dbfb70ac73190d5323ee1817a219ce07c1e1913d1008c8629d35
```

The generated indexes in `docs/` are derived from it. The archive's filename still says `FINAL_FREEZE_CANDIDATE` because it was hashed before acceptance, and rebuilding it to change that label would create a different object.

This public repository has a fresh Git history. Some records cite commit IDs from the private research history, and those are not expected to resolve here. See [provenance boundary](docs/PROVENANCE_BOUNDARY.md), [authority tree](docs/AUTHORITY_TREE.md) and [artifact lineage](docs/ARTIFACT_LINEAGE.md).

## Repository layout

```text
docs/          Theorem index, route map, finite computations, provenance notes
analysis/      Individual research threads and audit packages
authority/     Frozen, candidate, raw and audit archives with custody manifests
src/           Scanner and analysis source code
bin/           Prebuilt binaries (reproduction rebuilds everything from src/)
scripts/       Verification, documentation and build scripts
tests/         Cross-checks and unit tests
output/, logs/ Stored results and run logs
baseline/, cert/  Earlier verification bundle and no-counterexample certificate
archive/runs/  Earlier reproduction and validation run directories
```

## Citation and license

If you use this work, please cite the frozen record and its SHA256 (see [CITATION.cff](CITATION.cff)). Repository-authored code and documentation are under the [MIT License](LICENSE). Raw and externally supplied archives are kept as evidence and are not relicensed by being stored here; see [NOTICE](NOTICE).
