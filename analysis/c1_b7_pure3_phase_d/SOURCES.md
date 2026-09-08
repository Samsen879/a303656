# Source map and reading scope

All repository sources below were read through the read-only GitHub connector at the fixed main SHA.

- `analysis/c1_order_dag_phase_c/THEOREMS.md` — 完整数学正文；主要依赖 §§1–7、12–13
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_order_dag_phase_c/THEOREMS.md
- `analysis/c1_order_dag_phase_c/REPORT.md` — 完整报告正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_order_dag_phase_c/REPORT.md
- `analysis/c1_order_dag_phase_c/PROOF_AUDIT.md` — 完整审计正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_order_dag_phase_c/PROOF_AUDIT.md
- `analysis/c1_blocker_deficient_core_phase_b/DEFINITIONS.md` — 完整定义正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_blocker_deficient_core_phase_b/DEFINITIONS.md
- `analysis/c1_blocker_deficient_core_phase_b/THEOREM_AUDIT.md` — 完整证明/审计正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_blocker_deficient_core_phase_b/THEOREM_AUDIT.md
- `analysis/c1_pooled_lower_cover_phase_b/README.md` — 完整
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_pooled_lower_cover_phase_b/README.md
- `analysis/c1_pooled_lower_cover_phase_b/REPORT.md` — 完整报告正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_pooled_lower_cover_phase_b/REPORT.md
- `analysis/c1_kraft_hall_phase_a/REPORT.md` — 完整报告正文，含跨次读取的正文续页
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_kraft_hall_phase_a/REPORT.md
- `analysis/c1_seven_prime_audit_phase_b/README.md` — 完整
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_seven_prime_audit_phase_b/README.md
- `analysis/c1_seven_prime_audit_phase_b/SEVEN_PRIME_INDEPENDENT_PROOF.md` — 完整独立重证正文
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_seven_prime_audit_phase_b/SEVEN_PRIME_INDEPENDENT_PROOF.md
- `STATUS.md` — 完整
  https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/STATUS.md


## Live receipts
The live main branch was read at both the start and the end of the session; SHA/tree remained unchanged. PRs 21–25 were individually confirmed merged, with their main-base/merge chain recorded in SOURCE_BINDING.json. STATUS remained PAUSED / NONE / UNRESOLVED.

## Limits
Not every auxiliary or generated file in the five requested directories was individually read. No repository-native replay, no complete local checkout, no 2e9 scan replay. The report does not claim that these were performed. The new verification is standalone, with no repository implementation imported.

## External primary arithmetic source
Cunningham main table, pmain126.txt:
https://homes.cerias.purdue.edu/~ssw/cun/pmain126.txt

Selected base-5 minus/plus entries were used as discovery or cross-check hints. For certified exclusions, the numerical prime factors are proved locally by recursive full-(n-1) Lucas certificates and their full product is checked independently. A table's P label is not itself treated as a local certificate. The 301/602 exploratory product decompositions are explicitly not part of the certified exclusions.

## Novelty and independence
"New" denotes a deduction beyond the actually read repository statements, not a claim to mathematical literature priority. The source proofs and this proposed extension still require independent-author mathematical review. Different computational cores were checked in one author/session, not by two independent research teams.
