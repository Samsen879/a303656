# Source custody — 2026-09-14

Base main SHA `fd8aa2d5dd2cff758f2eb021c486ff9e2c3d1f38`, tree
`325265d83abae42acadc59f8107d88d1375085be`, live re-bound for L0.

| Source | Identity | Internal manifest | Producer / integration replay |
|---|---|---|---|
| A303656_CONSTRUCTIVE_N_GT_7_PHASE_I.zip | SHA256 b13386a6a8ba5407b10ede8f6cafd123d1df08a746c50569c40b8e29e8fc22b8 | all25 PASS; safe-list PASS | verifier.py normal + optimized, all19 mutations rejected: PASS |
| A303656_C279_GATE_RESULT directory | directory manifest SHA in SOURCE_RECEIPTS.json; selected input hashes in SELECTED_PAYLOAD.json | full directory manifest PASS | verify_factors.py: PASS, OPEN, search_completion NOT_ESTABLISHED |

ZIPs were extracted only to temporary non-repository directories. Replay used
disposable working copies; original ZIP/directory sources were not modified.
Selected producer proofs, inputs and code are byte-identical; original transport
archives, duplicate reports, generated verifier runtime receipts, search logs
and binaries are not committed. The full original manifest was checked before
selection; `SELECTED_PAYLOAD.json` authenticates the committed subset, not a
claim that excluded files can be replayed from this directory.

Producer verifier PASS is exact finite evidence, not independent-author review
or proof of the unknown arithmetic hypotheses. Source import references S1–S9
point into merged main. The historical base5 bound is referenced from merged
Phase G, not rerun. `SOURCE_BINDING.json` is historical producer provenance;
its prior no-write policy and proposed factor benchmark are not L0 execution
instructions. L0 authorized integration only, no further factor research.

Integration command: `python3 -B analysis/constructive_n_gt_7_phase_i/verify.py`.
Normal/optimized finite BOTH replay, mutation rejection and C279 identity/mass
replay PASS. No certified factor or root was invented. Missing C279 measured
search completion is WITHHELD FROM PR as a search-performance conclusion.
