# Single-integer certificate input

Run `python3 src/ajt5_integer_certificates.py PATH` on one UTF-8 JSON object. Every handled input failure emits one JSON object on stdout. A request for `--help` prints the command usage. The arithmetic formats and witness requirements are defined in the [R4 specification](../ajt5_integer_certificates/README.md#concrete-integer-submissions).

| Exit | JSON status | Interpretation |
|---:|---|---|
| 0 | `VERIFIED_NO_BRIDGE` or `VERIFIED_EMPTY_D` | All required evidence checks succeeded. |
| 1 | `REFUTED` | A valid submission establishes a bridge, a positive target, or an empty parent for a claim requiring a positive parent. |
| 2 | `INVALID` | Bad invocation, unreadable source, malformed record or false submitted arithmetic. A source I/O failure has a reason beginning with `cannot read certificate`. |
| 3 | `PARTIAL` | All submitted arithmetic checked, with insufficient evidence to decide the claim. |
| 4 | `UNKNOWN_RESOURCE` | An input cap, exhausted memory or exhausted file descriptors prevented verification. |

The checker reads at most 8 MiB plus one byte to detect overflow. Numeric tokens must be integers of at most 4,096 bits in magnitude. It rejects duplicate keys, trailing data, nonfinite or fractional numeric tokens, booleans in integer fields and repeated evidence. The nesting limit is 64. Every supplied atom is checked, including atoms immaterial to the verdict. The child `n=5m+r` is derived internally. For the largest admitted parent `m=2⁴⁰⁹⁶−1` and `r=4`, this gives `n=5·2⁴⁰⁹⁶−1`, at most 4,099 bits. A standalone EMPTY_D claim supplies its own n under the 4,096-bit input cap.

A row with `x < 5^d+3^c` is inactive (NOT_ACTIVATED in a fixed-window audit). Submitting that index as arithmetic evidence gives INVALID. Equality gives residual zero, which accepts the square witness (0,0). Negative evidence requires a strictly positive residual. For example, 60 accepts either 15 or 3 as its unitary divisor congruent to 3 modulo 4. Distinct submitted divisors may share an explanatory prime. Complete coverage refers to every active index of the specific input. A finite block can leave uncovered columns or exponents, and the active range varies with the input. PARTIAL and UNKNOWN_RESOURCE leave the mathematical claim open.

The [CLI regression suite](test_checker_cli.py) checks both failure and arithmetic outcomes, including independent square identities at all five children of m=2. Run it with `python3 -O analysis/ajt5_frontier/test_checker_cli.py`.
