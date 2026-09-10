# A303656 — Different-prime replacement, Phase G

**Do not import this package as an arithmetic counterexample.** It contains a finite countermodel to an explicitly specified structural reduct, actual certificates for its regular skeleton, and conditional mathematical theorems. The seven nonregular endpoints are formal and uninstantiated.

Main result: an actual exactly-seven certificate has only one B7 original origin; no other original root can supply a square hit in any B7 exact state. The finite model meets the selected structural/provenance/global-state conditions with B7 cost4 and no cheaper original B7 root. An independently supplied external actual B7 root can be transplanted after reconstructing one global state, but no such root is produced here.

## Read order

`REPORT.md` gives the verdict and scope. `MODEL.md` defines the formal reduct and missing arithmetic gates. `PROOFS.md` proves the auxiliary theorems and countermodel. `SOURCE_BINDING.json` and `SOURCES.md` document pinned authority and incomplete directory-wide reading. `PROOF_AUDIT.md` records semantic checks and nonclaims.

## Offline verification

Python 3.10 or later; standard library only. No network, external dependencies, factor search, repository checkout, or original source packages are needed for the finite replay.

```sh
cd A303656_DIFFERENT_PRIME_REPLACEMENT_PHASE_G
python3 -B verify.py --check-hashes
```

The default run recomputes every mathematical result and compares both `results.json` and `finite_model_data.json` to the frozen versions. It verifies all supplied regular-prime/order/lifting certificates, formal event kernels, one-state complete BOTH coverage, provenance, costs, exact-state incidence, and negative controls.

For a separate results copy:

```sh
python3 -B verify.py --out /tmp/phase_g_replay_results.json --check-hashes
```

`--write` is a producer-only flag: it regenerates the frozen data/results and therefore requires a new manifest if the inputs or verifier change. Normal review should not use it.

## Payload

- `model.json`: typed original rows, basin structure, ONE fixed state, declared formal root obligations, exact-state registry input.
- `arithmetic_certificates.json`: recursive full-(n−1) Lucas primality certificates and exact base-5 orders/lifts for actual regular labels.
- `finite_model_data.json`: exact strata, primitive-incidence records, contraction receipts, ancestry paths, shadow capacities, full profiles, deletion witnesses and mutation-test outcomes.
- `verify.py`, `results.json`: executable replay and frozen summary.
- Markdown/source-binding/audit files and `SHA256SUMS.txt`: mathematical argument, scope and provenance.

The manifest covers every payload file except itself. It authenticates this delivered package, not an unperformed byte-level replay of upstream repository sources. There are no source archives, generated executables, private credentials or Git writes.

## Critical distinctions

`FORMAL_ORIGINAL_NONREGULAR_ORIGIN` is a countermodel role, not a certified prime. `Hit_hat(Q,R)` is a formal mark, not a numerical claim `Q²|Z_R`. The regular subledger CRT value is numerical; the seven-root extension is symbolic. Actual endpoint prime/lifting checks performed: **0**.

The 80 registry states and22 cheaper states exhaust only a fixed eight-label universe; no inference about unlisted actual square hits is made. The impossibility of another in-certificate B7 original root is proved from basin disjointness, not a bounded search.

The overall requested strict different-prime SQD remains unproved. B7 emptiness, exactly-seven exclusion, N≥8 and A303656 are not claimed. All new proofs are subject to independent review before repository integration.
