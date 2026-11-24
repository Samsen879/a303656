# AJT5 round 3: exact row-local information ablation

**A303656: UNRESOLVED.** This is a finite information-ablation experiment,
with no general proof, arithmetic counterexample, new interval record, or
change to frozen authority. It is based on R2 draft [#52](https://github.com/Samsen879/a303656/pull/52)
at exactly `10d9b86b5183aac65e4755d439ea018a17fa00f5`, stacked on
`research/r2-ajt5-gate-certificates`. R1/R2 evidence and the historical R1
discrepancy are preserved. No unmerged ACP #50 code is used.

## Fixed arithmetic inputs and artificial information loss

The corpus is **all 534 PB2 margin-one rows** from R2's
[`critical.csv`](../ajt5_gate_certificates/results/critical.csv), rather than
the separate 530-row augmented cohort. Its SHA256 is
`f1ea69807c1bf72ef3c78bf1489f259423eff3c8aa336cb2a9a3d4377cccf83a`.
The checker compares input bytes directly with the immutable R2 commit, runs
R2's stored-evidence verification, and validates complete arithmetic
certificates for every parent and child. Positive bits have exact nonnegative
square witnesses; negative bits have complete admissible-c coverage with
positive exact odd valuations at primes congruent to 3 modulo 4. Residual zero
is representable. The certificate file SHA256 is
`25cd4230cf7bc6586b0cf6afbe5a8651d19d89266b84d39116158b9475f13a53`.

Key-list completeness derives from R2's original full replay. R3 does not
independently repeat that 50-million-entry scan or claim new coverage. It
verifies that exact frozen roster and all its arithmetic masks. There is no
interval enlargement; the original bounds are `2<=m<=10,000,000`, `r=0..4`.
Only the explicitly named small controls are additionally regenerated.

For each row independently, `n=5m+r`, `L=floor(log_5 m)` by integer powers,
`U=[0,L]`, `V=[0,L+1]`, and full arithmetic masks `D=D(m)`, `E=D(n)`, choose
retained witnessed subsets `empty != A subset D`, `B subset E` (B may be
empty). Put

```text
F36 = {i in U : m-5^i = 24 mod36}, disjoint D
Q   = (B union (B-1)) intersect U
S   = A union (A+1)
gF  = |S| + |B| - |V|
h_b = |A intersect U_b| + |Q intersect U_b| - |U_b|
      + |(F36 minus Q) intersect U_b|, b=0,1.
```

Minimize `k=|D minus A|+|E minus B|`, subject to `gF<=0`, `h_0<=0`, and
`h_1<=0`. All nonpositive sufficient margins, including equality zero,
mean **UNKNOWN**. Omitted arithmetic positives remain unknown information;
they never become negative facts. The separate retained-bridge diagnostic
enumerates actual directed edges `a->b`, `b=a` or `b=a+1`, equivalently
`A intersect Q` nonempty. Bridge existence does not enter optimization.

## Finite findings

| Minimum deletions k | Keys |
| --- | ---: |
| 1 | 136 |
| 2 | 228 |
| 3 | 169 |
| 4 | 1 |

The sum of row minima is **1,103**. There are **3,232 optimal states**:
**2,370 with actual retained bridges**, and **862 without retained bridges**.
Of the 534 keys, 160 have no bridge in any optimum, 166 have bridges in every
optimum, and 208 have mixed optimum states.

The unique four-deletion key is `(5644037,1)`:

```text
D={0,2,3,5,6,8,9}, E={0,4,5,10}, F36={1,7}, L=9.
106 tied optimum states; 90 have retained bridges.
```

All supplied Web R3 expectations match the fresh computations. They are
stored separately in [comparison.json](results/comparison.json) and enter only
after optimization. No expected count selects inputs, stops enumeration, or
sets the DP optimum. A mismatch preserves its evidence and stops extension.

## Independent minimality and complete ties

The [producer](../../src/ajt5_ablation.py) sweeps indices `i=0..L+1`. Its DP
state records previous A/B bits, whether A is nonempty, accumulated
`|S|+|B|`, and the two parity margins. At index i it finalizes membership in
`S` at i and in `Q` at i-1. These depend only on the current and previous
bits. Equal states have identical allowable suffixes. A strictly more costly
prefix at the same state cannot produce an optimum; **every equal-cost path
is retained**. Final constraints select the globally minimal cost and all
tied retained-mask pairs.

The independent oracle walks the entire Cartesian product of powersets by
cardinality combinations, uses literal Python sets to form S and Q, and
evaluates the three inequalities directly. It shares no DP transitions,
state pruning, prefix costs or popcount gate arithmetic. For **every one of
the 534 rows**, both cost and the complete sorted set of ties must agree.
There is no heuristic cutoff or early stop. Tiny-domain exhaustive tests also
compare every mask pair across several residue patterns.

[keys.csv](results/keys.csv) stores all 534 minima, tie counts, retained-bridge
counts, complement-recovery counts, and per-key canonical state hashes.
[report.json](results/report.json) stores aggregates and the full canonical
state-stream SHA256:

```text
16aaeed05628e3d917cf1af7dd3ea3cd495fa4bab99253e327befe1c5f9c0374
```

Canonical states are sorted by `(m,r,A-mask,B-mask)`. Each line is sorted-key
compact JSON with one trailing newline, including margins, directed edges,
complement margins and weight gaps. All 3,232 lines can be generated on
demand; they are not checked into the repository. Hashes provide integrity,
not signatures or external attestations. Review is computational/AI, with no
human mathematical review or proof-assistant formalization.

## Exact-complement and fixed-weight recovery

On the optimal states use **true arithmetic negatives** `N=U minus D` and
`H=V minus E`, from the complete R2 certificates. These are never `U minus A`
or `V minus B`. The two strengthened parent margins replace F36 by N:

```text
hN_b = |A intersect U_b| + |Q intersect U_b| - |U_b|
       + |(N minus Q) intersect U_b|
gFH  = gF + |H minus S|.
```

Positive hN is reduced-universe pigeonhole. For gFH, B avoids H, so
`|S minus H|+|B| > |V minus H|` is exactly `gFH>0`. Thus a positive margin
certifies a retained bridge. The OR of the two parent margins and gFH
recovers **2,346 of 2,370** bridge states. All **24 residual states** occur
at the unique four-deletion key.

For these last 24 only, use the two fixed nonnegative weights
`w_up(i)=i+1` at odd i and zero at even i, and
`w_down(i)=L+1-i` at odd i and zero at even i. At least one gap

```text
sum_(i in A) w(i) + sum_(i in Q minus F36) w(i)
                    - sum_(i in U minus F36) w(i)
```

is strictly positive in each of the 24. Since A avoids F36, a positive
weighted gap implies intersection by weighted pigeonhole. This elementary
sufficiency argument does **not** assert universal positivity for arithmetic
masks, optimal ablations or larger L. Weights were fixed in the brief; no
weights were fitted. No new universal transfer theorem is claimed.

## Controls and strict mod-144 child negatives

[controls.json](results/controls.json) includes reviewable exact or witnessed
controls. At `(7721762,3)`, withholding only child bit 3 makes all R2 sufficient
gates UNKNOWN while an actual retained bridge remains. The complete masks
are unchanged arithmetic facts.

The row-local interpretation is essential. At `(2,0)`, the only nonempty A
is `{0}`, S is `{0,1}`, and `gF<=0` forces the retained child mask at 10 to
be empty. At `(10,0)` the parent retained mask is required to be nonempty.
Identifying these as one global retained mask is infeasible. Both keys
already belong to the fixed 534-row corpus.

The separate [small-modulus tool](../../src/ajt5_modular.py) generates
`S2(M)={a²+b² mod M}` and the **entire** `3^c mod M` orbit, including its
preperiod, until the first repeated residue. For M=144 it obtains
`[1,3,9,27,81,99]`, cycle start 2, and exactly these forbidden residues:

```text
15,24,60,87,96,111,132,141.
```

A strict negative t means **no c in the entire orbit passes**. All component
residue conditions refer to the same original c; separate existential c's
modulo factors are insufficient. For example 141 passes each of the separate
mod-9 and mod-16 tests, yet fails mod-144. The separately named bounded
admissible-c function considers only `3^c<=t`; it is not an entire-orbit
certificate. A modulo pass supplies no positive witness (e.g. t=57).

`verify_residue_gate` takes exact nonnegative witness subsets and a list of
strictly certified child-negative exponents. It regenerates the residue
data, checks every asserted negative, validates all witness equations, and
accepts only `gFH>0`. It counts the two sides separately; direct bridge
intersection is confined to diagnostics/tests. Invalid or nonpositive data
returns UNKNOWN. The cap is `2<=M<=512` and the original parent bound; this
tool is not an expanded arithmetic scan.

At `(82,0)`, `A={0}`, `B={0,1}`, all old margins `gF,gB,PB2,PB36` are zero.
Child e=3 has `410-125=285=141 mod144`, so `H={3}` is strictly negative and
`gFH=1`. This is a witnessed sufficient certificate independent of the full
child mask. Exact witness validation explicitly allows square residual zero.

## Reproduction and validation

Python 3.10+ suffices for new R3 work; there are no new dependencies. From the
repository root with the R2 commit present in Git history:

```bash
python3 scripts/run_ajt5_ablation.py --work-dir reproduce_work/r3-fresh --emit-states
python3 src/verify_ajt5_ablation.py analysis/ajt5_ablation/results
python3 tests/ajt5_ablation_tests.py
python3 src/verify_ajt5_reports.py analysis/ajt5_exact_audit/results
python3 src/verify_ajt5_gates.py analysis/ajt5_gate_certificates/results
python3 tests/ajt5_tests.py
python3 tests/ajt5_gate_tests.py
python3 scripts/verify_public_repository.py
python3 scripts/privacy_scan.py --reject-domain gmail.com
```

The generator requires a fresh directory. `--emit-states` writes the canonical
stream outside committed evidence; omit it for aggregate-only generation.
Web expectation mismatch returns 2 after preservation. A DP/oracle mismatch
preserves the first row's arithmetic masks, costs, tie counts and first
differing pair. The stored checker replays all optima and all controls.

Tests cover full tie equality, complement/weighted soundness on abstract
masks, preperiod and same-exponent modular semantics, strict versus bounded
negatives, modular-pass limitations, nonnegative and zero-residual witnesses,
unknown-at-zero behavior, malformed or malicious certificates, duplicates,
scope caps, and semantic artifact tampering even after rehashing manifests.
CI adds the R3 suite alongside existing R1/R2, authority, privacy and identity
checks. [receipt.json](results/receipt.json) records generation command,
runtime and source/input hashes. [validation.json](validation.json) records
the checks actually run before publication.

## Limits and R4 target

Ablation makes positive information unavailable; it does not realize a new
arithmetic mask. In particular, the 862 optimum states without a retained
bridge are not AJT5 counterexamples. The full masks in the fixed corpus all
have bridges. Exact-complement recovery needs authoritative negative facts;
missing witness bits alone never supply them. Finite positivity of the fixed
weights supplies no fitted universal conclusion.

A useful R4 target is a **genuine arithmetic undercount** rather than another
artificial deletion: either find a realized complete-mask gate miss within
the authorized corpus, or develop a proof that explicitly accounts for
nonlocal unit-residual losses. A scoped exact 14-prime certificate is another
separate research target if its hypotheses and coverage can be independently
certified. Prime lower-bound and ACP ideas remain separately **unverified
research leads**, and are not integrated as theorems here. No enlarged scan
is proposed by this PR.
