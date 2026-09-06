# Frozen computation specification

User authorization: expand the prime scan, then independently re-audit the seven-nonregular-prime proof. No GitHub writes or authority promotion.

## Exhaustive scan
- Previous admitted panel: primes q <= 10,000,000, q = 3 mod 4.
- Target: every admitted prime 3 <= q <= 2,000,000,000, a 200-fold bound extension.
- Test: pow(5,q-1,q*q)==1. This is equivalent to s_q>=2 since ord_q(5)|q-1 and q does not divide (q-1)/ord_q(5).
- No precision/residue enumeration; only the nonregular-prime inventory.
- Implementation A: segmented Eratosthenes on all integer positions, binary modular exponentiation modulo q^2 with unsigned 128-bit multiplication.
- Implementation B: a separate odd-only segmented sieve and base-q digit-pair arithmetic for 5^(q-1) modulo q^2; all digit-pair products use checked 64-bit bounds for q<=2e9.
- Both record each 10,000,000 integer block: candidate count, sum of candidate primes, and hits. Residue-stream fingerprints are cross-check aids, not mathematical primality certificates.
- Small benchmark: <=10^7 before the enlarged run. Python integer pow independently verifies the <=10^7 baseline and all enlarged hits.
- Every hit: deterministic trial-division primality, full factorization of q-1, exact multiplicative-order certificate, and s_q via q^2 and q^3 tests (further lifts as necessary).
- Auxiliary all-prime check through 10^8 distinguishes nonadmitted base-5 hits from admitted resources.
- No extrapolation beyond 2e9. External lists are comparison evidence only, not scan inputs or exhaustiveness evidence.

## Review
- Frozen input SHA256: 4d75958f51ff27e7a0d4d50811c6f60fb1e0886745eeae1b292e5b9718f0653e.
- Reconstruct the proof without importing its reference code into the new verifier.
- Priorities: fixed-anchor parity lemma; coarse/full quantifiers; sparse cover lemma; origin injection and least-helper argument; complete order inventories at ranks 3 and 5; exact p=5 residual-clause count.
- Direct finite enumerations are supporting tests, not substitutes for unrestricted proofs.
- “Independent” means a fresh derivation and separately implemented checking code in this session, not a different human author, another model, or formal proof-assistant verification.
