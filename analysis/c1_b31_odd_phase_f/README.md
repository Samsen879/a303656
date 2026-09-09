# A303656 B31^odd — Targeted Phase F

This is a local research/evidence bundle, not a GitHub integration or a proof-assistant formalization.

Start with `REPORT.md` (Chinese mathematical report with all requested sections).

**Source gap:** the named Phase E ZIPs were not attached or readable in this session. Live main remained Phase D at `fd59aad038a09f2fc6df7039111408fa231c27dd`. The O31 proof here is an independent reconstruction from pinned Phase C/D sources, not a claim to have read or authenticated Phase E.

Main results: the exact first-relay set `{878851,625552508473588471}`; exclusion of two-vertex basins; an exact eight-index three-vertex reduction; an arbitrary-branching closed-state square-hit iff; certified actual regular states; and a conditional lower bound of seventeen original odd rows when the nonregular root count is exactly seven.

No actual nonregular B31^odd member was found. Emptiness, exactly-seven impossibility, and N>=8 were not proved. Finite branching is not a global finite-state reduction.

## Reproduce

```bash
sha256sum -c SHA256SUMS.txt
python3 -B verify.py
```

The verifier uses only the Python standard library. It validates recursive full n-1 Lucas primality certificates, exact orders, exact lifting exponents, full small cyclotomic products, seven regular closed states, finite frontier/antichain checks, nine adversarial tests, and all 160,000 theorem-gated modular probe candidates. To omit only the bounded probe use `--skip-probe`.

`arithmetic_certificates.json` contains exact integers as strings. `verification_log.json` is the actual replay output. `source_binding.json` records the source boundary; `results.json` separates proved reductions from open targets.

The finite verifier does not establish the infinite-domain theorems: those depend on the written proofs in REPORT.md. Neither this session nor the accompanying code is an independent author/referee.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
