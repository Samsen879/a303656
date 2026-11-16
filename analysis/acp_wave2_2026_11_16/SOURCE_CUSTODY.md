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
   environment (Python 3, gmpy2 2.3.2, numpy 2.5.3, ortools). Result:
   **`ALL CERTIFICATES REPLAYED`, exit code 0.** Every value matches the
   producer report:
   - 24/24 Phase-1 validation checks, including the frozen C21 comparison;
   - catalogue: 5709 primes certified, `G = ∏ p^e`; the brute-force scan of
     inert `p < 1.1·10^8` finds exactly 4160 primes with `H < 32768`, all listed;
     the modular completeness route passes;
   - independent fibre-statistics recomputation passes;
   - Theorem A bounds `0.6830 / 0.7733 / 0.7454 / 0.7874` (classes 00/01/10/11);
   - Theorem R Haar-only `K = 29`: worst budget `0.995116` (class 10, `(13,13)`);
     `K = 146`: worst budget `0.998929` (class 11, `(83,83)`);
   - Proposition H horizon at 473899;
   - Lemma L4 brute force for `M ≤ 23` and the `M = 23..47` census;
   - one-parameter controls: the `β`-line coverings for `N = 315` and `N = 3465`
     are found again, the `α`-line for `N = 315` is again infeasible, and the
     time-limited instances again report UNKNOWN, as expected.
   The full log is kept as
   [`results/producer_replay_quick_2026-11-16.log`](results/producer_replay_quick_2026-11-16.log).

Neither check verifies the analytic parts of the arguments: Lemmas L1–L4,
Theorem F, the induction behind Theorem R, or C21's (H1)/(H2).
