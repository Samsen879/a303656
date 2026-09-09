# A303656 r=43 Phase F — reproducible evidence

Read `REPORT.md` first. Result: one new certified prime factor of reconstructed
C1806, leaving a 314-digit composite remainder. Neither order is closed.
The two Phase E ZIPs were unavailable; their original manifests and historical
factor inventories were NOT authenticated. Exact inputs are independently rebuilt.

## Reproduce the positive arithmetic evidence

On a system with Python 3, a C++ compiler, and GMP development headers:

```bash
bash replay.sh
```

This runs a Python-standard-library verifier, compiles/runs an independently
implemented C++/GMP verifier, and reproduces the positive ECM curve. It does
not launch the full negative factorization campaign.

To also repeat both exact arithmetic-progression trial exclusions through 10^12:

```bash
bash replay.sh --trial
```

For a Python-only fast check:

```bash
python3 verify_python.py --mutations
```

`primality_certificates.json` / `.tsv` contain 34 recursive Lucas nodes.
`arithmetic_audit.json` contains exact values, hashes, orders, lifting residues,
composite witnesses, and bounds. `campaign_manifest.json` binds each ECM log
to its exact input, bounds, completed curves, and sigma seeds. It distinguishes
initial factor reconstruction, normalized-C campaigns, the new remainder,
and duplicate positive replay. One timed-out batch and its completion are both
retained and counted correctly.

Generator scripts (`reconstruct.py`, `build_certificates.py`) additionally need
SymPy; they are not necessary for either fast verifier. They overwrite generated
outputs, so run them in a copy if preserving this evidence snapshot is required.

No compiled executables are included. `replay.sh` builds into `.local-bin`.
`ecm_reference.cpp` is NOT official GMP-ECM: see THIRD_PARTY_NOTICES.md.
Negative randomized/ECM outcomes are not squarefree certificates. The live repo
was read only; repository-native tests and Phase E ZIP replay were not performed.
