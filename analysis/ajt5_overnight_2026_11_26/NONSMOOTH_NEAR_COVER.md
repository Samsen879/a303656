# Small CRT cost can cover almost all indices with nonsmooth orders

Fix the two columns 5p²+C_e−9^t with C=(10941,10937), and any prescribed reduced inert work-prime class. For any prescribed divergent bound g(N), for every sufficiently large N there is an extension class of cost log M≤g(N)=not necessarily o(N); in fact one can require both log M≤g(N) and log M=o(N) by taking stages slowly. On N−o(N) indices in 0≤t<N both columns are forced to have some literal valuation 1. The auxiliary primes may all have orders greater than one and coprime to 3*5*7*11*13. This asserts density coverage, not full coverage.

Choose auxiliary primes q≡−1 mod 60060, excluding the finite fixed modulus and divisors of the column constants, and discard the exceptional density-zero set from [Pappalardi's rank-one multiplicative-order theorem](https://www.sciencedirect.com/science/article/pii/S0022314X9690044X). Then ord_q(9)/sqrt(q) tends to infinity and the harmonic sum of the retained primes diverges. For any fixed residue class of the exponent let I_q(t) indicate that (9^t−C_e)/5 is a nonzero square mod q. On that fixed class the orbit of 9 is a multiplicative coset of size L≫_class ord_q(9). Expand its indicator using multiplicative characters: each nontrivial translated quadratic sum is bounded by sqrt(q), by the Jacobi sum formula (the trivial or inverse-character exceptions are bounded by one). Consequently I_q has mean 1/2+O((sqrt(q)+1)/L) on the class. Partial summation of the prime number theorem in progressions gives the stated harmonic divergence after removing density zero.

The normalized harmonic averages of I_q thus converge weakly to 1/2 against every finite-period indicator on the profinite exponent space. They are uniformly bounded between zero and one, so approximation in L^1 extends this to any measurable indicator. If the unnormalized sum of I_q/q were finite on a positive-measure set, the averages would tend to zero there, a contradiction by dominated convergence. Hence the sum diverges almost everywhere, separately for either column.

At each q choose one uniformly random unit p mod q², independently across q. Conditional on I_q(t)=1, each of the two nonzero roots mod q has q−1 lifts giving valuation exactly one, so the payment probability is 2/q. If I_q(t)=0 this probability is zero. The expected uncovered measure of the two columns tends to zero by dominated convergence, so a finite simultaneous choice attains any desired coverage tolerance. Finite CRT combines its choices with the initial class. This reasoning uses no independence across exponent rows. At each stage fix all moduli first and take N sufficiently large before proceeding to that stage. This absorbs period discrepancy and enforces g(N), o(N), and even n_q log q<sqrt(N log M) for each auxiliary q. For a fixed stage the prime number theorem in progressions produces a work prime 3^N/3<p<2·3^N/5 for all sufficiently large N. Both columns then have precisely 0≤f<2N strictly active. No effective bound for switching stages is furnished, and no claim is made about the remaining rows' norm status.

Exact modular example:

```python
from fractions import Fraction as Q
from math import isqrt

p = 2512879132039
assert p % 4 == 3 and all(p % d for d in range(2, isqrt(p) + 1))
assert all(3**53 < 5*p*p + C < 3**54 for C in (10941, 10937))

for q, r, phases in [(103, 8, (8, 5)), (1871, 445, (2, 6))]:
    assert q % 4 == 3 and all(q % d for d in range(2, isqrt(q) + 1))
    assert pow(9, 17, q) == 1 and 9 % q != 1
    assert p % (q*q) == r
    for C, t in zip((10941, 10937), phases):
        residues = [(5*p*p + C - pow(9, t+17*j, q*q)) % (q*q)
                    for j in range(q)]
        assert all(x % q == 0 for x in residues)
        assert residues[0] != 0 and residues.count(0) == 1

assert sum(Q(q-1, 17*q) for q in (103, 1871)) == Q(22556, 192713)
```
