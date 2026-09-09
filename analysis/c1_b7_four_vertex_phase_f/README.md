# Four-vertex B7 Phase F research bundle

Read REPORT.md first. Result: Level D, independent reconstruction from Phase D. The required Phase E ZIP was not present. No complete four-vertex state was closed; full S_r census remains incomplete.

## Verify existing certificates and data

```bash
python3 verify.py
```

The verifier uses only the Python standard library and does not invoke a probable-prime oracle. It checks the SHA256 manifest when present. Big integer digit counts use rigorous rational logarithm intervals, not unguarded floating-point rounding.

## Fresh exact replays

```bash
python3 verify.py --replay-probes --replay-pminus1
```

Requires g++ with C++17; the p−1 replay also needs GMP headers and libraries. Compilation occurs in a temporary directory, not the repository. Bounded replays use the SAME discovery implementations; they are not independent exhaustive-coverage implementations. All resulting prime/order/lifting certificates have a separate standard-library verifier.

## Regenerate research tables (optional)

```bash
python3 build_results.py
```

Requires SymPy for discovery-only factorization used in creating recursive Pocklington certificates. The final primality proofs do not depend on SymPy's probable-prime decisions. This rewrites deterministic data plus timing records and invalidates the existing manifest; ordinary verification does not regenerate files.

## Scope

- 15 fork regular proper-states, 120 distinct terminal indices: exhaustive.
- 28 certified serial regular proper-states, 448 distinct terminal indices: NOT exhaustive.
- The 23 relays <=10^10 are the full output of the stated bounded AP search.
- Five additional large relays come from fixed-SHA input factors and are freshly certified. Each exceeds 10^12, so no terminal above it can enter the <=10^12 terminal probe.
- No actual nonregular B7 member; zero complete state exclusions.
- 215 recursive primality certificate nodes; 90 admitted terminal factors all valuation one.
- No GitHub writes, no repository-native tests, no Phase E original-payload hash audit.

CSV files are machine-readable integers; very large integers must be loaded as arbitrary-precision integers or strings, not spreadsheet floating point. The canonical numerical serialization used for aggregate/cofactor hashes is minimal-length unsigned big-endian bytes, with no prefix.

FILES: relays.csv/json, states.csv/json, indices.csv/json, fork_factors.csv/json, serial_factors.csv/json; prime_certificates.json; materialized_aggregates.json; pminus1_results.json; exact raw probe CSVs/logs; C++ sources; verifier and discovery builder; source binding and validation records.
