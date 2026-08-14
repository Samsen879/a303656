# P4 MOD-8-LIVE Gate V2 Route-2 Closure

## Final decision

The independent audit decision is final for this gate:

```text
Exact H8 landscape: ACCEPT
Registry v2: REJECTED
Semantic verifier: REJECT / FIX REQUIRED
Gate V2: FAIL
Design A: Level 1 conditional candidate only
New T(n): NOT AUTHORIZED
Route: CLOSE_GATE_V2_ROUTE_2
A303656: UNRESOLVED
```

This is a bounded closure of Gate V2. It is not conjecture progress, a new
research route, or an execution authorization. No Gate V3 is created.

## Protected exact result

The audit accepts, and this closure preserves, the exact fixed-P4 mod-8-live
landscape:

- `H8_min = 32`;
- `H8_max = 201`;
- `argmax_count = 468`;
- lexicographically first argmax `(2,13,50,5)`;
- 21 maximizing full masks;
- 5 live projections;
- the protected global and `t3=2` histograms;
- maximizing-mask aggregate SHA256
  `3d6fb47adb745d5501a53f2dcfddbc1106e8f67cfa85ea0d1ce61d487102bce3`.

The exact landscape is not rejected or deprecated.

## Decisive closure facts

1. The repository registry v2 has 6,129 integer rows and zero E4 rows.
2. Independent reconstruction has 6,583 confirmed integer rows and 983 E4 rows.
3. Known omissions include 454 P5 Family-U integers, 73 K4 direct rows,
   457 P4 direct rows, and the PILOT-A/PILOT-B exact-T intervals.
4. The 52-way direct run lacks a numeric input universe, chunk bounds, runner
   identity, touched-set, and stage ledger.
5. Historical exposure is not established for all 384 Design A integers.
6. The semantic verifier reports 32 passing tests but still accepts 15 material
   bypasses identified by the independent audit.
7. Code repair cannot recover missing historical facts.

These facts reject registry v2 as an exposure authority and reject the semantic
verifier as a sound authorization verifier. They require Gate V2 to close as
`FAIL`, not `PASS` or `NOT_ESTABLISHED`.

## Supersession policy

Historical artifacts are retained byte-for-byte as an audit trail. The files
listed in `analysis/p4_prospective_gate_v2/DEPRECATED_ARTIFACTS.json` no longer
carry promotion, registry-completeness, verifier-soundness, full-recovery, or
execution-authorization authority. This closure metadata supersedes those
claims without deleting their evidence.

Design A is archived at Level 1 as a conditional candidate only. It is not
selected again, repaired, promoted, or authorized. No new integer panel and no
new `T(n)` value is produced by this closure.

## Final state

```text
GATE V2: CLOSED / FAIL
NEW T(n): NOT AUTHORIZED
OEIS A303656: UNRESOLVED
```
