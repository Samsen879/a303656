# P4 live top-band prospective gate v2

This document is the source-stage skeleton for the historical-exposure repair. Generated conclusions and candidate manifests live under `analysis/p4_prospective_gate_v2/results/`.

The implementation preserves the accepted fixed-P4 mod-8 landscape while separating design novelty from historical exposure. It never evaluates a new integer, invokes factorization, invokes a direct two-square oracle, or starts a P5/P6 search.

The only permitted execution decision in this stage is `PASS`, `FAIL`, or `NOT ESTABLISHED` for `P4_LIVE_TOP_BAND_PROSPECTIVE_GATE_V2`; no result authorizes a T census without a later independent audit.
