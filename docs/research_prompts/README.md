# Research prompts (November 2026)

These are the prompts used for the two research waves recorded in
[`analysis/triage_wave_2026_11_14/`](../../analysis/triage_wave_2026_11_14/README.md)
and [`analysis/acp_wave2_2026_11_16/`](../../analysis/acp_wave2_2026_11_16/README.md).
They are kept so that a restart can reuse them. They are working material, not
evidence. **A303656: UNRESOLVED.**

Some numbers inside the prompts are snapshots of what was known when each wave
started; for example, wave 2 still says "23 roots". Before reuse, update the
shared context from [the handoff note](../ALMOST_ALL_ROUTE_HANDOFF.md).

## How a session prompt is assembled

Each session receives `shared context + lane text`. In the lane text, the line
`{{FOCUS}}` is replaced by one focus sentence, which selects a variant. Without
a variant, the line is deleted. Each session ends with a fixed RESULT CARD.
Claimed proofs then go through the referee template, and all cards go through
the triage template.

| File | Use |
|---|---|
| `wave1_00_shared_context.txt` | Shared context for wave 1 (problem, notation, closed routes, Round-1 results, rules, result card) |
| `wave1_lane_*.txt` | Wave-1 lanes A, B, V, E, C, P, L, W |
| `wave2_00_shared_context.txt` | Shared context for wave 2 (model, wave-1 chain, how C21/C22 work, the ACP dichotomy) |
| `wave2_D0_formalize_acp.txt`, `wave2_D1_prove_N.txt`, `wave2_D2_search_covering.txt` | Wave-2 tracks |
| `wave2_single_session_acp.txt` | Self-contained single-session version of wave 2 (formalize + search); this is the prompt that produced the ACP packet |
| `common_referee_template.txt`, `common_triage_template.txt` | Append after either wave's shared context, then paste the report or result cards at the end |

## Focus sentences for the variants

Replace `{{FOCUS}}` with one of these lines.

- A1: `ASSIGNED FOCUS for this session: strategy (A1), the branching-process / Kesten–Stigum analogy. Do Step 0, then spend most of your effort on (A1). Other sessions are covering A2–A4.`
- A2, A3, A4: the same sentence, naming (A2) a zero–one law, (A3) restriction to a controllable sub-measure, or (A4) self-similarity and Perron–Frobenius.
- B-num: `ASSIGNED FOCUS for this session: Part 1 (exact numerics) first and deepest, then Part 3 if the data points to failure; do Part 2 only as far as the data supports.`
- B-proof: `ASSIGNED FOCUS for this session: Part 2 (the lower bound). Do only as much of Part 1 as you need to test your inequalities numerically.`
- E1, E2, E3; C1, C2; P1, P2, P3: `ASSIGNED FOCUS for this session: option/track (X).`
- W1–W6: `SEED for this session: Wk (seed name).`
- D1a, D1b, D1c: `ASSIGNED FOCUS for this session: strategy (D1a), the Lovász Local Lemma.` (respectively Fourier tiling; gcd counting plus an exhaustive finite computation)
- D2a, D2b: `ASSIGNED FOCUS for this session: variant (D2a), catalogue search with exact coverage decisions.` (respectively the M = t frontier starting at M = 23)
