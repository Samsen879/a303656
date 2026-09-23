# Finite rational recursion no-go audit

```text
FINITE FIXED-COMPLEXITY RATIONAL RECURSION:
ROUTE-PRUNED UNDER EXPLICIT HYPOTHESES
A303656: UNRESOLVED
```

This directory records the independent adjudication of the 2026-09-21
Thread 3 packet.  The accepted result is a theorem about narrowly specified
proof architectures.  It is not a proof of A303656, not a counterexample, and
not a claim that every finite recursion is impossible.

The strongest accepted statement is Q*: from finitely many seeds, a finite
witness-continuous system of positive-definite binary rational quadratic
states, fixed affine index maps with integer multipliers at least two, and a
uniformly bounded finite catalogue of rational coordinate charts reaches only

```text
O(sqrt(X) (1+log X)^6 + (1+log X)^(r+2)) = o(X)
```

original-state integers up to `X`.  Here `r` is the number of distinct primes
dividing the fixed transition multipliers.  Q-dagger gives a weaker bound for
strictly index-increasing, exponent-dependent carries and fixed multipliers
`K >= 1`.

Start with:

- [THEOREMS.md](THEOREMS.md) for exact statement sheets;
- [PROOF_AUDIT.md](PROOF_AUDIT.md) for the independent proof disposition;
- [ROUTE_SCOPE.md](ROUTE_SCOPE.md) for the killed/not-killed matrix;
- [REPRODUCE.md](REPRODUCE.md) for offline commands;
- [SOURCE_CUSTODY.md](SOURCE_CUSTODY.md) for packet provenance.

The packet is preserved under `source/producer_packet/`.  Its program is a
comparison implementation only.  `tools/reference_audit.py` is an independent,
standard-library verifier and imports no packet code.
