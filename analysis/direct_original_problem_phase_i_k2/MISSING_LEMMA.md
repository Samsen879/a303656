# ML-K2 — UNPROVED, program PAUSED

Use source K's inclusive D(n), b(0)=1, and G=G23711 with full2/3/7/11 local
tests. For failed positive residuals in G, N_p^G(n) counts pairs whose LEAST
odd-valuation bad prime is p. The events form an exact disjoint partition.
No bad prime below19 remains. L2 forces an even positive number of distinct
defects; the least is strictly less than sqrt(m)≤sqrt(n). Hence exactly
`R(n)=G(n)-sum_{19<=p<sqrt(n),p=3mod4}N_p^G(n)`.

The remaining quantitative target is:

```text
exists N0 forall n>=N0:
sum_{19<=p<sqrt(n), p=3mod4} N_p^G(n) <= G(n)-G(n)/log(n).
```

ML-K2 is NOT proved. Source K gives eventually G≥a0(logn)², with
a0=1869/(25600 log3 log5)>0. IF ML-K2 held, the exact partition would give
R≥G/logn≥a0logn>0, so every sufficiently large n is represented.
This conditional implication is inspectable in the original
[MISSING_LEMMA.md](sources/k2/MISSING_LEMMA.md), with notation in
[LARGE_PRIME_DECOMPOSITION.md](sources/k2/LARGE_PRIME_DECOMPOSITION.md).
No effective N0 or certification below it is provided. Positivity of R does
not imply this stronger quantitative target.

DISTANCE FROM CURRENTLY CHECKED METHODS: LARGE (research assessment).
The small-prime local structure is rigorous, but collective large-prime
completion is open. Stronger fixed-fraction/atom-free smooth/absolute-error
templates have scope-qualified impossibility proofs. This does not prove
that all direct methods are impossible. DIRECT ORIGINAL-n PROGRAM: PAUSED.
Active promoted route NONE; no successor, new scan or theorem invention authorized.
