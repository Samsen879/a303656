# OEIS A303656: evidence, computations, and route audits

This repository studies whether every integer `n > 1` can be represented as

```text
n = a² + b² + 3ᶜ + 5ᵈ,  with a,b,c,d ≥ 0.
```

> **Current status: UNRESOLVED.** There is no general proof and no certified counterexample.

The repository combines exact finite computations, independently audited structural theorems, negative route-closure results, and the frozen authority record used to keep their scopes separate. A finite verification is never presented as a universal proof.

## Start here

- [Current project status](STATUS.md)
- [Theorem and conditional-authority index](docs/THEOREM_INDEX.md)
- [Research route map](docs/ROUTE_MAP.md)
- [Certified and exact finite computations](docs/FINITE_COMPUTATIONS.md)
- [Authority tree](docs/AUTHORITY_TREE.md)
- [Raw/repaired artifact lineage](docs/ARTIFACT_LINEAGE.md)
- [Public/private provenance boundary](docs/PROVENANCE_BOUNDARY.md)
- [Public release receipt](authority/frozen/PUBLIC_RELEASE_RECEIPT.json)
- [Reproduction guide](REPRODUCE.md)
- [Detailed historical Chinese report](REPORT_zh.md)

## Strongest finite result

Two clean-room C++ direct scanners checked every integer in

```text
240000000001 ≤ n ≤ 241600000000
```

and found no candidate counterexample. This is a consecutive interval of 1.6 billion integers. Across the five explicitly manifested datasets, independent implementations cover at least 1.853 billion distinct integers. These are exact finite computations only.

## Frozen authority

The accepted Master Authority V2 object is bound by [`authority/frozen/FREEZE_RECEIPT.json`](authority/frozen/FREEZE_RECEIPT.json):

```text
SHA256 3033149749b1dbfb70ac73190d5323ee1817a219ce07c1e1913d1008c8629d35
MASTER AUTHORITY V2: FROZEN
A303656: UNRESOLVED
```

The ZIP retains its pre-acceptance `FINAL_FREEZE_CANDIDATE` filename and internal status. The external freeze receipt records the subsequent independent exact-hash acceptance without changing the accepted bytes.

The public repository has a deliberately new Git history. Commit identifiers recorded as private forensic provenance are archival identifiers and are not expected to resolve on GitHub; public scientific identity is carried by artifact filenames, SHA256 hashes, manifests, and the freeze receipt.

Publication authorization is recorded separately in [`authority/frozen/PUBLIC_RELEASE_RECEIPT.json`](authority/frozen/PUBLIC_RELEASE_RECEIPT.json). The original authority freeze receipt remains an immutable historical record of its own earlier release status.

## Fast verification

The default replay is network-free and does not rerun the multi-billion search:

```bash
python3 scripts/verify_public_repository.py
```

It verifies the frozen hash, recursive archive/manifest rules, authority ledgers, scope guards, generated public documentation, and stored audit JSON. See [REPRODUCE.md](REPRODUCE.md) for optional finite-computation replays.

## Evidence vocabulary

This repository distinguishes:

- `PROVED`
- `PROVED NEGATIVE STRUCTURAL THEOREM`
- `ACCEPTED CONDITIONAL IMPLICATION`
- `CERTIFIED FINITE COMPUTATION`
- `INDEPENDENTLY AUDITED FINITE COMPUTATION`
- `SPECULATIVE WATCH`
- `STOPPED ROUTE`
- `SUPERSEDED`
- `ARTIFACT DEFECT`
- `UNRESOLVED`

## License and archival material

Repository-authored code and documentation are available under the [MIT License](LICENSE). Raw and independently supplied authority archives are retained as scientific evidence and are not relicensed merely by being stored here; see [NOTICE](NOTICE).
