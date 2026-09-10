# A303656_B31_BRANCHING_PHASE_G

E-level, narrowly scoped obstruction-route pruning. **No base-5 B31^odd member or emptiness proof.** GitHub read only.

## Read

`REPORT.md` gives the Chinese synthesis and source boundaries. `THEOREMS.md` gives G1–G5 with proofs. `COUNTERMODELS.md` gives complete variable-base fixtures. `SOURCE_BINDING.json` and `SOURCES.md` distinguish live authority, inherited results and current deductions. `results.json` freezes conservative claim flags.

The four core reports, the B7 theorem file and the four integration notes were read. The user's stronger all-auxiliary-files directory reading requirement was not fully completed. No repository-native replay is claimed.

## Offline verification

Python 3.10+; standard library only:

```bash
python3 verify.py --output fresh_verification.json
python3 -O verify.py --output fresh_optimized.json
```

Both outputs should match `verification_log.json`. The verifier proves every used prime recursively with complete p−1 Lucas certificates, verifies exact orders, exact lifting valuations, entire closures, antichains, tame/wild tests and corruption rejection. It does not prove the universal G1–G5 statements by enumeration.

Verify local checksums:

```bash
sha256sum -c SHA256SUMS.txt
```

The manifest excludes itself and covers all original delivery members. Fresh output files created by a user are not part of the original manifest.

## Optional regeneration and discovery

`generate_evidence.py` requires SymPy only for constructing evidence; probable-prime screening is not the proof authority. Regenerate into a separate scratch directory and check with the standard-library verifier:

```bash
python3 generate_evidence.py --output-dir /tmp/b31g-regenerated
python3 verify.py --evidence /tmp/b31g-regenerated/evidence.json
```

`replay_discovery.py` reproduces only the recorded finite 80000-candidate modular domain. It is not needed to trust any theorem or certificate, and produces no unbounded absence/squarefree conclusion. Its hard cap matches the original gate.

```bash
python3 replay_discovery.py --output fresh_discovery.json
```

## Nonclaims

B31^odd empty: NOT PROVED. Actual base-5 member: NONE CERTIFIED. Exactly-seven: NOT KILLED. N>=8: NOT PROVED. A303656: UNRESOLVED. No GitHub writes, Codex execution, large-scale factorization, repository integration, independent-author review, or proof-assistant formalization.
