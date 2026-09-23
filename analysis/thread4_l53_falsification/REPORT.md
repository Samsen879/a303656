# `L5,3` falsification report

## Exact source definition

The Thread 4 packet defines

```text
S_2 = {x^2+y^2 : x,y in Z}
T_3 = S_2 + {3^j : j>=0}
D(m) = {d>=0 : m-5^d in T_3}
```

Its candidate lemma is:

> For every representable integer `m>=2`, some `d in D(m)` satisfies
> `d+1 in D(5m+3)`.

Equivalently,

```text
D(m) nonempty => (D(m)+1) intersect D(5m+3) nonempty.
```

Thus the exact first-failure domain is every integer `m>=2` with `D(m)`
nonempty.  There is no parity or congruence restriction.

## Candidate 1: certified failure

`m=7,963,079`:

| d | 5^d | m-5^d | in T_3? | Witness / exact reason |
|---:|---:|---:|:---:|---|
| 0 | 1 | 7,963,078 | yes | `1446^2+2311^2+3^12` |
| 1 | 5 | 7,963,074 | yes | `1172^2+2567^2+3^0` |
| 2 | 25 | 7,963,054 | yes | `166^2+2817^2+3^2` |
| 3 | 125 | 7,962,954 | no | every `3^c` residual has an odd valuation at a prime `3 mod 4` |
| 4 | 625 | 7,962,454 | yes | `402^2+2793^2+3^0` |
| 5 | 3,125 | 7,959,954 | no | every `3^c` residual has an odd valuation at a prime `3 mod 4` |
| 6 | 15,625 | 7,947,454 | yes | `106^2+2817^2+3^6` |
| 7 | 78,125 | 7,884,954 | yes | `9^2+2808^2+3^2` |
| 8 | 390,625 | 7,572,454 | yes | `738^2+2651^2+3^2` |
| 9 | 1,953,125 | 6,009,954 | yes | `688^2+2353^2+3^0` |

`5m+3=39,815,398`:

| d | 5^d | 5m+3-5^d | in T_3? | Witness / exact reason |
|---:|---:|---:|:---:|---|
| 0 | 1 | 39,815,397 | yes | `614^2+6280^2+3^0` |
| 1 | 5 | 39,815,393 | no | exhaustive valuation ledger |
| 2 | 25 | 39,815,373 | no | exhaustive valuation ledger |
| 3 | 125 | 39,815,273 | no | exhaustive valuation ledger |
| 4 | 625 | 39,814,773 | yes | `2404^2+5834^2+3^0` |
| 5 | 3,125 | 39,812,273 | no | exhaustive valuation ledger |
| 6 | 15,625 | 39,799,773 | yes | `3108^2+5490^2+3^2` |
| 7 | 78,125 | 39,737,273 | no | exhaustive valuation ledger |
| 8 | 390,625 | 39,424,773 | no | exhaustive valuation ledger |
| 9 | 1,953,125 | 37,862,273 | no | exhaustive valuation ledger |
| 10 | 9,765,625 | 30,049,773 | no | exhaustive valuation ledger |

Therefore

```text
D(m)             = {0,1,2,4,6,7,8,9}
D(5m+3)          = {0,4,6}
D(m)+1           = {1,2,3,5,7,8,9,10}
intersection     = empty
```

The complete per-`c` factorization blockers are retained in
`results/membership_details.json`; the table does not replace that ledger.

Both integers are nevertheless represented:

```text
7,963,079  = 1446^2 + 2311^2 + 3^12 + 5^0
39,815,398 =  614^2 + 6280^2 + 3^0  + 5^0
```

The failure is specifically a failure of the transfer lemma.

## Candidate 2: certified failure

`m=8,984,426`:

| d | 5^d | m-5^d | in T_3? | Witness / exact reason |
|---:|---:|---:|:---:|---|
| 0 | 1 | 8,984,425 | no | exhaustive valuation ledger |
| 1 | 5 | 8,984,421 | yes | `1425^2+2637^2+3^3` |
| 2 | 25 | 8,984,401 | no | exhaustive valuation ledger |
| 3 | 125 | 8,984,301 | no | exhaustive valuation ledger |
| 4 | 625 | 8,983,801 | yes | `84^2+2996^2+3^6` |
| 5 | 3,125 | 8,981,301 | yes | `1983^2+2247^2+3^1` |
| 6 | 15,625 | 8,968,801 | no | exhaustive valuation ledger |
| 7 | 78,125 | 8,906,301 | yes | `804^2+2874^2+3^2` |
| 8 | 390,625 | 8,593,801 | no | exhaustive valuation ledger |
| 9 | 1,953,125 | 7,031,301 | yes | `368^2+2626^2+3^0` |

`5m+3=44,922,133`:

| d | 5^d | 5m+3-5^d | in T_3? | Witness / exact reason |
|---:|---:|---:|:---:|---|
| 0 | 1 | 44,922,132 | yes | `1167^2+6600^2+3^5` |
| 1 | 5 | 44,922,128 | yes | `934^2+6637^2+3^1` |
| 2 | 25 | 44,922,108 | no | exhaustive valuation ledger |
| 3 | 125 | 44,922,008 | yes | `955^2+6634^2+3^3` |
| 4 | 625 | 44,921,508 | no | exhaustive valuation ledger |
| 5 | 3,125 | 44,919,008 | no | exhaustive valuation ledger |
| 6 | 15,625 | 44,906,508 | no | exhaustive valuation ledger |
| 7 | 78,125 | 44,844,008 | yes | `1553^2+6514^2+3^1` |
| 8 | 390,625 | 44,531,508 | no | exhaustive valuation ledger |
| 9 | 1,953,125 | 42,969,008 | yes | `710^2+6515^2+3^9` |
| 10 | 9,765,625 | 35,156,508 | no | exhaustive valuation ledger |

Hence

```text
D(m)         = {1,4,5,7,9}
D(5m+3)      = {0,1,3,7,9}
D(m)+1       = {2,5,6,8,10}
intersection = empty
```

## First-failure audit

Engine A enumerates `x^2+y^2` directly, forms `T_3` by exact bitset shifts by
all relevant `3^c`, and scans every integer from 2 through 7,963,079.  It
applies the implication only where `D(m)` is nonempty.  Result:

```text
first failure: 7,963,079
smaller failures: 0
representable source integers tested through failure: 7,963,078
```

The last count equals the entire integer interval size because every scanned
integer happened to be representable; the algorithm did not assume this.

Engine B independently factors every candidate residual and applies the exact
sum-of-two-squares criterion.  It shares neither the support table nor the
membership implementation with Engine A.  Both engines agree on every listed
support set.

Observed full-scan benchmark on the audit host:

```text
wall time: 0.09 s
peak RSS: 14,720 KiB
compiler: g++ -O3 -std=c++17
```

These measurements are informational, not certificate inputs.

## Historical and logical scope

The producer packet's exact bounded check of `2<=m<=5000` found no failure and
remains valid.  The later exhaustive scan extends that domain and finds the
first failure; the earlier record is preserved rather than rewritten.

Certified conclusion:

```text
L5,3 IS FALSE.
```

Not established:

- impossibility of the minimal-counterexample program;
- impossibility of every 5-adic transfer;
- impossibility of other representation-selection lemmas;
- a counterexample to A303656.
