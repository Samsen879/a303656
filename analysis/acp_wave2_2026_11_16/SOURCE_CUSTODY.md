# Source custody

## Producer packet

Transport: user-uploaded `A303656_ACP_2026-11-16.zip`.
Size: **485170 bytes**.
SHA256: `17bfc265a30566bcfa47d5f61d9411e212c4379bf262d6b325da98ed932c2a7f`.

All 47 archive members are preserved byte-for-byte under `source/acp_packet/`,
with only the enclosing `acp/` directory removed. No member was edited. The
packet's own `SHA256SUMS` lists all other members, and every line passes, both
at integration time and in `tools/independent_checks.py`.

The separately uploaded `A303656_ACP_REPORT.md` is byte-identical to
`source/acp_packet/REPORT.md` and is therefore not stored twice.

The producer's summary message (its RESULT CARD and caveats) was uploaded as
text and is kept as `source/result_message.txt`
(SHA256 `095498fa41e99b3531fff058471ef994ca34eefe4ddded753a9713b5d8c05270`).

Producer: a separate Claude session, reported by the project owner as Claude
Fable 5.2, prompted with
[`docs/research_prompts/wave2_single_session_acp.txt`](../../docs/research_prompts/wave2_single_session_acp.txt)
and the 2026-11-14 triage packet as attachment.

## Integration checks

1. `tools/independent_checks.py`: written in this integration, standard library
   only, sharing no code with the packet. Result: `ACP_INDEPENDENT_CHECKS_PASS`
   (packet hashes; 18-prime `β`-line covering of `Z/315`; Proposition H horizon,
   19789 inert primes up to 473899, with directed-rounding bounds; Lemma L4 for
   `M ≤ 13`, `p < 3000`, with observed maxima equal to the producer's table;
   class `(0,0)` has no `z = 0` fibre point).
2. Producer replay: `run_all.sh` in quick mode, in a temporary copy, with
   `AUDIT` pointing to the 2026-11-14 triage packet, on a fresh Linux
   environment (Python 3, gmpy2 2.3.2, numpy 2.5.3, ortools). Status at the
   first commit of this integration: still running. Already PASS: the 24-item
   Phase-1 validation suite (including the frozen C21 comparison), the
   independent catalogue checks (5709 primes certified; brute-force scan to
   `1.1·10^8`; modular completeness route), the independent fibre-statistics
   recomputation, and the Theorem A certificates for classes `00` (0.6830) and
   `01` (0.7733). The final result is recorded in a follow-up commit.

Neither check verifies the analytic parts of the arguments: Lemmas L1–L4,
Theorem F, the induction behind Theorem R, or C21's (H1)/(H2).
