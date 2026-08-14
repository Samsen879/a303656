# Proposed T(n) obstruction-data schema

Status: **SCHEMA ONLY — DATA NOT COLLECTED**

```text
obstruction_data_status: SCHEMA_ONLY_NOT_COLLECTED
```

This document reserves a conservative schema for a future, separately
authorized, small obstruction fixture. No factorization, primality proof,
obstruction search, CRT search, residue search, or new integer scan was run in
the read-only low-tail analysis.

## Purpose and unit of data

One obstruction record describes one *losing exponent pair* `(c,d)` for a
fixed integer `n`: the active source pair has

```text
shift = 3^c + 5^d <= n
remainder = n - shift
representable = false
```

The record is not a T(n) winner and must not be confused with numerical-shift
deduplication. Distinct exponent pairs remain distinct records even if their
numerical shifts are equal.

## Proposed record

```json
{
  "schema": "a303656-tn-obstruction-record-v1",
  "n": "unsigned decimal integer",
  "c": 0,
  "d": 0,
  "shift": "3^c + 5^d as unsigned decimal",
  "remainder": "n - shift as unsigned decimal",
  "representable": false,
  "complete_factorization_status": "NOT_ATTEMPTED",
  "factorization": [],
  "odd_valuation_primes_3_mod_4": [],
  "canonical_obstruction_prime": null,
  "factorization_verifier": null,
  "factorization_provenance": null,
  "verification_status": "UNKNOWN"
}
```

### Required identity and arithmetic fields

- `n`: parent integer, encoded as canonical unsigned decimal text;
- `c`, `d`: nonnegative source exponents;
- `shift`: exact integer `3^c+5^d`;
- `remainder`: exact integer `n-shift`;
- `representable`: fixed to `false` only after the two-square obstruction has
  been verified under the status rules below.

The verifier must independently recompute both powers, the shift, subtraction,
and range condition. It must reject signed, noncanonical, overflowed, missing,
or inconsistent values.

### Factorization fields

`factorization` is an ordered array by increasing prime:

```json
{
  "prime": "canonical unsigned decimal",
  "exponent": 1,
  "prime_verification": {
    "status": "PROVEN_PRIME",
    "method": "named deterministic/proof-producing method",
    "certificate_path": "optional relative path",
    "certificate_sha256": "optional SHA256"
  }
}
```

The factorization verifier must check with exact integer arithmetic that the
prime powers multiply to `remainder`. A probable-prime test without the
declared assurance required by the future contract is insufficient for
`COMPLETE_FACTORIZATION_VERIFIED`.

`odd_valuation_primes_3_mod_4` lists the fully verified prime factors `q` for
which

```text
q mod 4 = 3
valuation_q(remainder) is odd.
```

The list is sorted numerically. `canonical_obstruction_prime` is the smallest
such verified prime. It remains `null` unless at least one qualifying prime and
its complete valuation are verified.

### Provenance fields

`factorization_verifier` reserves:

- implementation id and version;
- executable or script SHA256;
- independent verification command;
- exact return code;
- arithmetic backend and version.

`factorization_provenance` reserves:

- source commit and dirty state;
- exact command line;
- input/output SHA256;
- generation timestamp;
- CPU/OS/compiler/library information where relevant;
- certificate paths and hashes;
- whether the factorization was generated and checked by distinct tools.

## Status vocabulary

The status values are deliberately non-interchangeable.

### `COMPLETE_FACTORIZATION_VERIFIED`

Every listed base is proven prime to the required assurance, every exponent is
positive, the ordered prime powers multiply exactly to the remainder, and no
cofactor remains. This status alone does not assert a two-square obstruction;
the parity/congruence condition must also be verified.

### `PARTIAL_FACTOR_FOUND`

At least one exact nontrivial divisor has been verified, but a composite or
unknown cofactor remains, primality is incomplete, or some valuation is not
known completely. A partial factor cannot certify nonrepresentability merely
because it is congruent to 3 modulo 4: its full valuation and primality must be
established.

### `TWO_SQUARE_OBSTRUCTION_VERIFIED`

Exact verified data establish a prime `q congruent to 3 mod 4` with odd
valuation in the complete factorization of the remainder. The verifier checks
the valuation and the sum-of-two-squares criterion independently. Only then
may `representable=false` be treated as verified obstruction data.

### `UNKNOWN`

No complete conclusion is available. This includes not attempted, timeout,
resource failure, probable but unproved primality where proof is required,
unverified divisor, incomplete valuation, malformed certificate, or verifier
failure. `UNKNOWN` has no theorem-level meaning.

## Record-set metadata

A future collection must have a separate manifest containing:

```json
{
  "schema": "a303656-tn-obstruction-dataset-v1",
  "classification": "EXACT FINITE COMPUTATION",
  "interval_or_panel_contract": {},
  "selection_rule": "deterministic predeclared rule",
  "record_count": 0,
  "complete_coverage_claim": false,
  "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
  "records_sha256": null,
  "verifier_report_sha256": null
}
```

The status in this round remains exactly
`SCHEMA_ONLY_NOT_COLLECTED`. The recommended panel is a proposal only and does
not change it.
