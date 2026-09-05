# A303656 Phase 3 — arithmetic realizability of prefix frontiers

This repository-native integration contains:

- `REPORT.md`: theorem statements, proofs, beta<=3 classification, two-anchor criteria, and audit interpretation;
- `tools/phase3_reference.py`: standard-library exact reference implementation;
- `results/l3_beta_le_3_literal_catalog.json`: all 1431 parameter-labelled l=3 candidates through beta=3, each marked individually;
- `results/l67_beta_le_3_compressed_catalog.json`: exact formula-level status partition for l=67;
- `results/resource_scan_B10000000.json` and `results/prime_lists/`: complete bounded resource audit;
- `results/actual_67_beta_1_2_3_embeddings.json`: fourteen exact shared-residue anchor-fiber checks;
- `results/common_residue_audit.json`: rigid valuation criterion checks and dynamic difference-set scan;
- `results/summary.json`: compact verdict and hashes.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/phase3_reference.py --output-dir results
```

Authority remains:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

It was safely reconstructed from
`A303656_PREFIX_FRONTIER_REALIZABILITY_PHASE_A.zip` (the requested local
label included `(1)`) with outer SHA-256:

```text
60780334b892445d966a0224e1e6eb8ca2acba6b4bad1bb67b8baf168f8d24ab
```

The theorem is restricted to one anchor and one fixed lower-coordinate fiber.
The `q <= 10^7` resource inventories are exact finite data only.

Repository checks:

```bash
python3 -m unittest discover -s tests -v
python3 tools/finalize_integration.py --verify
```
