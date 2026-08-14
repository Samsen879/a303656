# Project status

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
LOW-COST GENERIC THEOREM HUNTS: NOT ACTIVE
TARGETED RESTART: ONLY ON EXPLICIT RESTART GATE
LARGE-SCALE COMPUTATION: NOT AUTHORIZED
A303656: UNRESOLVED
```

There is **no general proof** and **no certified counterexample**.

## Frozen authority state

- Master Authority V2: `FROZEN`
- Frozen SHA256: `3033149749b1dbfb70ac73190d5323ee1817a219ce07c1e1913d1008c8629d35`
- Freeze receipt: [`authority/frozen/FREEZE_RECEIPT.json`](authority/frozen/FREEZE_RECEIPT.json)
- Private forensic scope-patch commit: `ac5dff25a30fc016a4df16daa7eb47fef2d6bcc2` (archival identifier; not expected to resolve in this public repository)

## What is established

- A direct dyadic positive-density theorem, with its stated positive-density-only scope.
- Several structural and route-specific negative theorems, each limited to the formal class named in the theorem index.
- Exact finite computations over explicit intervals and finite domains.
- Fail-closed restart conditions.

## What is not established

- Universal representability.
- A counterexample.
- An almost-all theorem sufficient to close the problem.
- CRW for any explicit fixed `(Q,E)`.
- HC-LT.
- Impossibility of every descent or every exceptional-set inverse method.

## Scope guards of particular importance

- N-004's `O(sqrt(X) log X)` scale is specific to the audited absolute-minor-spectrum / F3 localization mechanism; it is not a universal threshold for all future exceptional-set inverse methods.
- N-009 establishes arbitrarily large Helly obstructions on finite active-shift restrictions of arbitrarily large size; it does not prove unbounded Helly number for the complete `D(n)` actual-mask family.
