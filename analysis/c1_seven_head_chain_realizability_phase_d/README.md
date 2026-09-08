# A303656 seven-head completion-chain Phase D — read-only evidence bundle

Start with REPORT.md. Outcome: Level C with D partial data; all seven terminal
chain-existence questions remain OPEN. No complete actual C=1 certificate is present.

## Offline mathematical replay

```bash
python3 verify.py
python3 regression_tests.py
```

The default verifier uses Python standard library only. It independently checks
recursive full-(N-1) Lucas certificates, exact orders and valuations, exact factor
identities, actual head-row coverage, conditional compressed covers, recorded
search streams and the huge-31 Python replay. No network/repository code imports.

## Rerun both complete bounded factor-search implementations

Requires g++ and GMP development headers/libraries already installed:

```bash
python3 verify.py --replay-search
```

This compiles in a temporary directory and reruns the 14 matching uint128/GMP
search domains. The underlying methods are fixed-index cyclotomic preimage
searches, not a generic scan for nonregular primes. Recorded stdout is deterministic;
execution wall times are not. All integers in the uint128 implementation satisfy
its explicit uint64 candidate bound. The GMP implementation supports larger primes.

## Rebuild discovery outputs (not needed to verify)

```bash
python3 build_evidence.py
python3 write_report.py
```

Discovery additionally uses SymPy. Its probable-prime screening of the 121- and
171-digit cofactors is NOT an independent primality certificate. No terminal
hypothesis is filled from those values. The report and evidence retain OPEN.

## Main files

REPORT.md: mathematical report and all requested final flags.
SOURCES.md / AUTHORITY.json: source provenance and frozen live-main metadata.
evidence.json: 33 arithmetic nodes, 66 primality proof nodes, exact-order/lifting
witnesses, 19 factor families, conditional rows and seven terminal exclusion proofs.
verify.py / verification.json: independent checker and actual execution result.
regression_tests.py / regression_results.json: six fail-closed mutation checks.
search/ and replay_search/: exact candidate-domain logs from both native cores.
large31_independent_replay.json: Python arbitrary-precision third-core check.
cofactors/: exact remaining integers for moderate exponent targets.
ecm/: bounded stage-1 exploratory receipts, never absence proofs.
SHA256SUMS.txt: payload integrity; not a replacement for mathematical verification.

No binary, executable build product, nested archive, author email, or local Git
checkout is bundled. Source-repository CI/test receipts are not claimed as freshly
reproduced. No GitHub writes were performed.
