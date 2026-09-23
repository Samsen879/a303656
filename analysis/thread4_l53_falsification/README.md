# Thread 4 `L5,3` exact falsification

```text
L5,3 TRANSFER LEMMA: CLOSED / FALSE
MINIMAL-COUNTEREXAMPLE PROGRAM: HEDGE / UNRESOLVED
A303656: UNRESOLVED
```

The exact first failure in the packet's stated domain is

```text
m = 7,963,079
5m+3 = 39,815,398
D(m) = {0,1,2,4,6,7,8,9}
D(5m+3) = {0,4,6}
(D(m)+1) intersect D(5m+3) = empty
```

The first-failure scan exhausts every integer `2 <= m <= 7,963,079`, applying
the lemma only when `D(m)` is nonempty.  Two independent membership engines
agree: direct support enumeration/bitsets and exact prime-valuation criteria.

- [REPORT.md](REPORT.md): definition, complete candidate tables, first-failure audit and scope.
- [results/l53_falsification_certificate.json](results/l53_falsification_certificate.json): final machine certificate.
- [results/membership_details.json](results/membership_details.json): witnesses and exhaustive valuation blockers.
- [REPRODUCE.md](REPRODUCE.md): offline replay.
- [SOURCE_CUSTODY.md](SOURCE_CUSTODY.md): packet provenance.

The original packet is preserved byte-for-byte under `source/producer_packet/`.
Its `m<=5000` no-failure result remains valid historical finite evidence; its
then-unproved `L5,3` candidate is superseded by this exact falsification.
