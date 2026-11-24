# AJT5 round 2: parity and certified residue gates

**A303656 remains UNRESOLVED. No general proof, counterexample, theorem-status
change, or new interval record.** This bounded research package is stacked on
R1 PR #51, verified head `9e371d1ef47138de880208eebf4a81e276aa80c1`, branch
`research/r1-ajt5-exact-audit`. It uses no unmerged ACP PR #50 changes.
R1 reports and frozen authority are unchanged.

For nonnegative integers `a,b,c,d`, let

```text
D(n) = {d >= 0 : n - 5^d = a² + b² + 3^c}, n > 1.
AJT5: D(m) nonempty => some d in D(m), e in D(5m+r) have e=d or e=d+1.
```

The parent bound is exactly `2 <= m <= 10,000,000`, `r=0..4`; the largest
child is `50,000,004`. There is no enlargement. All endpoints and powers are
integer-exact. Since `3^0=1`, exponents with `5^d=n` are in the coverage but
cannot be members. A square residual of zero is valid and cannot be blocked.

## Results and evidence boundaries

| Quantity | Reproduced result |
| --- | --- |
| Nonvacuous pairs | 49,999,995 |
| PB2 nonpositive pairs | 0 |
| Minimum PB2 | 1 |
| PB2 margin-1 pairs, by r | `[119,91,130,122,72]`, total 534 |
| Minimum combined parity/mod-36 margin PB36 | 1 |
| PB36 margin-1 pairs, by r | `[119,89,130,120,72]`, total 530 |
| Mod-36 alone nonpositive pairs | 70; minimum -1 |
| Literal old gates' survivors among the frozen 220 | 2, distribution `[1,1,0,0,0]` |
| Lambda < 3 among the frozen 220 | 47, distribution `[21,5,7,12,2]` |
| Mod-36 margin among the frozen 220 | `1:9, 2:37, 3:122, 4:50, 5:2` |
| Independently constructed selected complete masks | 1,080 |

The two R1 native membership engines were rebuilt and rerun; their complete
S2, T and D tables agree entry by entry and match the preserved R1 raw hashes.
The new [native postprocessor](../../src/ajt5_gate_scan.cpp) shares that D
table. At every nonvacuous pair it compares two separately structured gate
calculations: popcounts/bit masks, and an individual-exponent walk without
popcounts or predecessor bit unions. This is **independent postprocessing of
shared input**, not a third independent full membership computation.

The [Python checker](../../src/verify_ajt5_gates.py) reconstructs all 1,080
selected masks by witnesses and exact prime valuations, and recalculates
selected gate arithmetic using literal sets. The selected certificates prove
their rows. Exhaustive pair counts and completeness of the 534/530 corpora
require the full native replay; selected certificates do not establish those
coverage claims alone. Integrity manifests are hashes, not signatures or
external attestations. All review here is computational/AI, not a human
mathematical review or formal proof-assistant verification.

## Sufficient gates and their proofs

Put `L=floor(log_5 m)`, `U={0,...,L}`, `V={0,...,L+1}`, `D=D(m)`,
`E=D(5m+r)`, and `P=(E union (E-1)) intersect U`. Indeed
`5m+r <= 5(5^(L+1)-1)+4 = 5^(L+2)-1`, so the child exponent universe is V.
A bridge is equivalent to `D intersect P` being nonempty. The old margins
are `gF=|D|+runs(D)+|E|-(L+2)` and `gB=|D|+|P|-(L+1)`; **strictly positive**
is the sufficient threshold. Zero does not pass.

### Parity pigeonhole gate PB2

For `U_b={i in U:i%2=b}`, define

```text
kappa_b = |D intersect U_b| + |P intersect U_b| - |U_b|
PB2     = max(kappa_0,kappa_1).
K       = max(gF,PB2).
```

If either kappa is positive, two subsets of that parity universe have total
size exceeding its size, so they intersect and give a bridge. The verifier
counts D and P separately; accepting this inequality needs no D-and-P
intersection test. Since `kappa_0+kappa_1=gB`, `gB>0` implies `PB2>0`.
Thus K logically dominates both literal old gates. PB2 alone need not
dominate gF: abstract `L=3, D={0,3}, E={0,1}` has `gF=1`, `gB=PB2=0`.
These arbitrary masks are a logical control, not an actual arithmetic case.

### Certified mod-36 exclusions

Let `F={d in U : m-5^d = 24 mod36}`. Then `D intersect F` is empty.
To see this put `t=m-5^d=24 mod36` and consider every admissible `3^c<=t`.
If c is even, `t-3^c=3 mod4`, which is not a sum of two squares. If `c=1`,
the residual is `3 mod9`; if c is odd and at least 3, it is `6 mod9`.
In both odd cases its exact 3-adic valuation is 1, an obstruction because
`3=3 mod4`. All these classes are nonzero; residual zero is never excluded.

Work in the reduced universe `U minus F`. The D side is unchanged and the P
side has size `|P|-|P intersect F|`. Pigeonhole gives

```text
delta36 = gB + |F minus P| > 0  => bridge.
```

This is an individual sufficient gate. At the certified control `(784,0)`,
`delta36=0` while `gF=1`. The OR with gF must be distinguished from delta36
alone. The full histogram includes 70 nonpositive delta36 cases even though
PB2 is positive throughout this corpus.

Removing F separately within each parity gives the additional margin

```text
q_b  = kappa_b + |(F minus P) intersect U_b|
PB36 = max(q_0,q_1).
```

This follows by the same reduced-universe argument. Each q is at least its
kappa. Also `q_0+q_1=delta36`, so PB36 dominates both PB2 and delta36 as a
sufficient test. Retaining gF in an OR preserves the abstract gF control.
The mod-36 augmentation raises four PB2 margin-1 pairs above 1:
`(758549,1), (1153373,3), (1752049,3), (5644037,1)`.

### Two old hard cases, independently certified

| m,r | D | E | kappa_0,kappa_1 | F minus P | delta36 | q_0,q_1 |
| --- | --- | --- | --- | --- | ---: | --- |
| 102917,1 | `{0,4,5,6}` | `{0,4,8}` | `1,-1` | `{1}` | 1 | `1,0` |
| 1676569,0 | `{1,3,7}` | `{0,4,6}` | `-2,1` | `{2,8}` | 1 | `0,1` |

[examples.json](results/examples.json) contains complete and small partial
positive certificates for these cases. [hard_ledger.csv](results/hard_ledger.csv)
enumerates all admissible `(d,c)` pairs for the four related integers
`102917,514586,1676569,8382845`: **469 alternatives, 45 actual square witnesses,
424 positive residuals with exact odd valuation blockers, no zero residuals**.
The checker enforces complete coverage, the exact equations, primality,
`p=3 mod4`, and exact odd valuation. Tests also include a separate residual-zero
witness and reject its mutation into a blocker.

## Non-circular certificates and route separation

[ajt5_gates.py](../../src/ajt5_gates.py) exposes `verify_gate(record)`.
The schema is `{schema:1,m,r,mode,parent,child,summary}`. With `mode=complete`,
the two sides are R1's complete `n,mask,by_d` certificates. Every admissible d
is covered; present bits carry `[a,b,c]`, and absent bits cover **every**
admissible c by a prime/valuation blocker. With `mode=lower`, each side is
`{n,witnesses:[[d,a,b,c],...]}`; only exact witnessed bits are counted.
Missing bits are unknown, never inferred absent. Duplicate bits, malformed
values, incorrect equations, summaries or integer bindings are rejected.

The checker recomputes d counts, run count, e count, p counts, parity-universe
sizes and excluded-outside-P counts. It requires the supplied side-specific
summary to match exactly. Positive acceptance uses only those counts and the
strict margins; the verifier does not compare D against P to accept a gate.
For lower subsets, the same proofs apply to those subsets: a bridge between
proved bits is a bridge between full masks. The gF run formula applies to
the lower D itself, without presuming its run count is a lower bound on the
full D run count.

Outputs and future routes stay separate:

* A verified positive margin returns `SUFFICIENT_BRIDGE`.
* If every tested margin is nonpositive, the result is `UNKNOWN`. Invalid
  certificates and out-of-campaign inputs also return `UNKNOWN`. None of
  these outcomes falsifies AJT5 or A303656.
* The separate `classify_exact` route requires complete certified masks. A
  nonempty parent with empty bridge disproves AJT5 only, if the child still
  has some representation. It never serves as a positive gate.
* An empty E, proved with full certified admissible exponent coverage, is an
  actual A303656 counterexample at the child. Partial emptiness is UNKNOWN.

No such counterexample occurs here. Abstract small tests use direct bridges
as an independent soundness oracle, outside the accepting verifier.

## Accounting without rewriting history

On the **frozen 220 first-gate survivors**, define

```text
lambda = min sum_(i in X) (1_E(i)+1_E(i+1)),
         X subset U, |X|=|D|, runs(X)=runs(D).
```

The DP tracks used vertices, started runs, and the previous selected bit.
Independent exhaustive enumeration over tiny universes checks every feasible
summary and E. The reproduced histogram on the 220 is
`0:1, 1:7, 2:39, 3:120, 4:50, 5:3`. Thus lambda >= 3 leaves 47, with
`[21,5,7,12,2]`. This is a **different robust gate**, applied within the frozen
220; no full-corpus lambda histogram is claimed. Each vertex has at most two
directed bridge edges. Lambda >= 3 therefore guarantees that removing any
one vertex, on either side, still leaves a bridge. It is stronger robustness
than mere bridge existence; it is not asserted necessary for that robustness.

The historical claimed 47 had `[32,4,1,4,6]`. Its original code and full
roster have not been recovered. The cause of that difference remains
**NOT_ESTABLISHED**. Reproducing the number 47 for this other gate does not
recover or validate the historical gate. The literal old two-gate result
remains 2. R1's archived discrepancy is preserved exactly.

## Reproduction, validation, and receipts

Python 3.10+, Linux and a C++17 g++ compiler suffice; no new package is needed.
From the repository root:

```bash
python3 src/verify_ajt5_gates.py analysis/ajt5_gate_certificates/results
python3 tests/ajt5_gate_tests.py
python3 tests/ajt5_tests.py
python3 scripts/verify_public_repository.py
python3 scripts/privacy_scan.py --reject-domain gmail.com
```

Fresh full computation, with new directories:

```bash
git fetch origin main:refs/remotes/origin/main
python3 scripts/run_ajt5_audit.py --work-dir reproduce_work/r2-input-fresh
# Expected exit 2: R1 preserves the historical discrepancy, not a numerical failure.
python3 scripts/run_ajt5_gates.py --input-work reproduce_work/r2-input-fresh --work-dir reproduce_work/r2-gates-fresh
# Expected exit 0. A new mismatch stops and preserves its evidence.
```

[receipt.json](results/receipt.json) preserves the checked R1 head, shared raw
mask hash, source hashes, exact commands, return codes, environment and resource
measurements. [logs.json](results/logs.json) and the receipt preserve native
logs; [manifest.json](results/manifest.json) binds all stored results. Full raw
tables and compiled binaries remain in ignored work directories. Only small
reports, source and exact generated certificates are versioned. One setup
attempt stopped at R1 receipt generation because `origin/main` was missing;
the ref was fetched and both membership engines were rerun in a fresh
directory. No numerical mismatch was observed.
[validation.json](validation.json) records the pre-publication command list,
return codes and outputs against the source hashes in the receipt; the draft
PR records the final tested commit and remote CI result.

Tests cover abstract soundness (including the gF/PB2 non-dominance control),
DP versus exhaustive enumeration, single-vertex deletion robustness,
residue classes, exact power boundaries, zero residuals, invalid/altered
complete and partial certificates, missing/altered ledgers and reports, raw
table corruption and out-of-bound inputs. The CI workflow runs both R1 and
R2 quick suites plus the repository's authority, privacy and identity checks.

## Precise R3 adversarial target

Freeze [critical.csv](results/critical.csv)'s 534 `(m,r)` keys as the next
round's deterministic corpus; [nearest36.csv](results/nearest36.csv) retains
the 530 cases still at PB36=1. These are nearest-to-failure controls, not
counterexamples. Do not expand the parent bound.

The most valuable next experiment is to search for **actual arithmetic masks**
within this fixed corpus under deliberately restricted, witness-backed
information: delete each parent or child witnessed bit in turn and record
the first summary for which `gF<=0` and both `q_0,q_1<=0`. Save the smallest
such partial UNKNOWN certificate, together with the original complete
certificate, and identify a minimal additional witnessed bit or independently
proved forbidden class that restores positivity. This measures exactly what
the sufficient verifier needs without mistaking loss of information for an
AJT5 failure. A nonvacuous starting control is `(m,r)=(5,4)`, complete
`D={0}, E={0,2}`: withholding child bit 0 leaves nonempty lower subsets
`D'={0}, E'={2}` with every sufficient margin zero. The full child remains
represented and the complete pair has a bridge. For a genuine adversarial arithmetic target beyond certificate
ablation, seek a realized complete-mask pair with those same nonpositive
margins; none exists in the present bound. Only after such a gate miss would
complete bridge verification distinguish a true AJT5 failure from a weak
sufficient gate. No unbounded conclusion is inferred from these finite data.
