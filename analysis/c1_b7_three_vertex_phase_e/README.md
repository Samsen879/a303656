# A303656 B7 three-vertex closure — Phase E

**12/48 indices closed; seven new. r43 still open at903 and1806.**
No actual nonregular terminal, no empty-three-vertex theorem, no B7 emptiness,
no N>=8, no GitHub writes.

Read `REPORT.md`, then `THREE_VERTEX_ORDER_TABLE.md`. Machine-readable evidence:
`order_table.json`, `arithmetic_records.json`, `primality_certificates.json`,
`small_relay_inventory.json`. Exact333/337-digit priority remainders are in
`cofactors/`; four priority cyclotomic integers are in `cyclotomic_values/`.

## Offline replay (Python3.11+, standard library only)

```sh
python -B check_manifest.py
python -B verify.py --suite core --self-test
python -B verify.py --suite cofactors-a
python -B verify.py --suite cofactors-b
```

All three verifier suites were executed with PASS; results are preserved in
`verification_*.json`. `python -B verify.py --suite all --self-test` combines them.
No internet, repository checkout, CAS or probabilistic primality oracle needed.
Optional `discovery/` is not imported by any verifier and requires extra libraries.

For exact source/read-only authority and what was NOT read/replayed, see
`AUTHORITY.json`, `SOURCE_BINDING.json`, `SOURCES.md`.
This is a standalone research artifact, not a repository-native integration/PR.

## Evidence boundaries

14 remaining cofactors are proven composite;22 are exact symbolic integers
whose PRP/compositeness status is not tested. None is declared squarefree.
341 prime-proof nodes include certificate ancestry, not341 new terminal primes.
The extra low-order gate proves B7 root order>=889 and, if basin size>=4,
root order>=2287; it does not prove basin size>=4 for allB7.
