# 2026-11-26 AJT5 research checkpoint

**Scope:** A303656 is unresolved. This checkpoint records candidate results from independent computational research runs and includes a small, exact boundary replay. It does not modify the repository's frozen authority or replace a full certificate.

## Common-prime obstructions

For integers `m >= 2` and `r = 0,...,4`, pair the nonnegative residuals
`P = m - 5^d - 3^c` and `C = 5m+r - 5^e - 3^f`, with `e=d` or `e=d+1`. A finite set `Q` of distinct primes congruent to 3 modulo 4 blocks a pair if at least one **positive** residual has an odd valuation at a prime in `Q`. Zero survives. The same set `Q` must be used for the entire menu. Survival against `Q` is not a two-square certificate.

| Setting | Reported lower bound on a complete blocking set | Evidence status |
| --- | ---: | --- |
| 3 allowed | 28 | Budget 27 excluded by independent reconstruction and integer replays. The two reconstructors use different finite-to-tail seams. |
| 3 excluded | 38 | Budget 37 excluded in a separate reconstruction, with two tail verifiers and a freshly recomputed finite prefix. |
| 3 allowed, newest candidate | 29 | A cloud run and its own replay report budget 28 excluded. Independent cross-track reconstruction is pending. |

For budget 27, the independent reconstruction reports a common normalized root cap of `1,172,027,091`, with 145,935 digit / closed-mask / mod-27 cases and 132,006 terminal leaves. Its independently enumerated finite-to-tail seam has 2,998 distinct integer/digit pairs. Those numbers describe that reconstruction, not the separate cloud tree.

## Exact small replay included in this PR

Run:

```sh
python3 analysis/ajt5_overnight_2026_11_26/verify_boundary.py
```

The script exhausts all active labels up to a fixed normalized-root cap for one explicit integer, one digit, and one set of 27 primes. At cap `1,172,027,090` the set blocks every pair. At the next root, a pair survives the set, but both residuals still fail the genuine two-square condition, through explicit primes outside the set. A separate exact zero-residual example checks that zero is allowed at the active boundary. This verifies the pointwise controls, **not** the completeness or minimality of the global bounds. The full trees and the separately reported finite family with its first genuine bridge at root `1,220,703,260` are not packaged in this PR.

## Direct analytic route (separate model)

The current research treats the 3- and 5-power exponents as shared variables across local conditions; the prime constraints are not assumed independent. It reports that, almost everywhere in the profinite model, a zero of the limiting mass must already arise from a finite set of conditions. An additional reported sufficient criterion rules out finite zeros when the support contains at most 44 inert primes that are Wieferich to **both** bases 3 and 5 (64 if the support omits 3). These are statements about the shared-exponent local model, not integer bridge counts or pointwise representability.

[Dorais–Klyve, §4.1](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf#page=7) is a published finite search for the two bases through `970,453,984,500,000`. The two base-3 candidates below that cutoff fail the base-5 test. This does not bound the number of common primes globally. The priority is a structurally uniform finite-positivity proof or a genuine finite obstruction, followed by auditing the transfer to a density-one result. A density-one result would still leave the pointwise conjecture unresolved.

## Next verification work

- Publish complete, sanitized replay packages for the large-scope audits separately; leave result status explicit until then.
- Separate mask completeness, row activation and exact valuations into a proof-checker interface. A Lean soundness theorem for that interface could verify what an accepted certificate implies without replacing the bulk search.
- Prefer structural improvements or genuine countercontrols over increasing a support budget by one more prime without a reusable argument.
