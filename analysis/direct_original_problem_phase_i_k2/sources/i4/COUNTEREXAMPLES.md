# Adversarial checks, countermodels, and finite tests

No counterexample to A303656 was found or claimed. The countermodels below invalidate proposed general-purpose steps, not the literal-base conjecture. All numerical outputs are reproduced by reference.py; no new global n-scan was performed.

## CE-01. A large locally correct bulk sample can fail everywhere

For arbitrarily large N, choose M=floor((log N)^2) consecutive integers i for which
\[
 m_i=77(924i+1)\in[N/2,N].
\]
Such a block exists for all sufficiently large N: this arithmetic progression has a fixed positive step, whereas M is only logarithmic squared. Each m_i is odd and 1 mod 4. Also 3 does not divide m_i, and
\[
 v_7(m_i)=v_{11}(m_i)=1,
\]
because 924 is divisible by 7 and 11. Thus every member passes the 2/3 norm predicates but fails the two-square test. The members can be chosen distinct.

Consequences: bulk size, local 2/3 correction, and M of order log-squared alone do not prevent total coverage. They cannot imply ML-D2. The special arithmetic relation m=n-3^c-5^d must supply new information. This construction is not a grid of that form.

## CE-02. ML-D2 is stronger than the existence of one successful row

At N=1002, take the multiset with one member 576 and forty members 1001. Both numbers lie in [N/2,N], pass L2 and L3, and
\[
 576=2^6\,3^2,\qquad1001=7\cdot11\cdot13.
\]
The first is a two-square norm; the others are not. Nevertheless the positive divisor-mass ratio is enclosed by
\[
 2.3566623177854104556557068695298122932450153875344685130079529
 <\frac{\mathcal D(2/\log N)}{\mathcal D(1/\log N)}
 <2.3566623177854104556557068695298122932450153875344685130079726.
\]
In particular it exceeds 2. This prevents calling ML-D2 merely an equivalent rewriting of R>0 for arbitrary bulk samples. It also prevents deriving ML-D2 from a single representation without additional control of the other rows. This is a multiset countermodel, not an actual base-(3,5) exponent rectangle.

## CE-03. A different literal-base grid can violate the proposed inequality

As an adversarial one-target benchmark, take n=535903 and replace both bases by 2. There are 324 pairs with each power at most n/4. Exactly 23 pass the same local 2/3 predicates, and none is a two-square norm. The script checks these rows directly and obtains
\[
 2.6127155724595313203489132210559709236844643787549275805977963
 <\frac{\mathcal D_n(2/\log n)}{\mathcal D_n(1/\log n)}
 <2.6127155724595313203489132210559709236844643787549275805978114.
\]
This exceeds 4/sqrt(e), as PW-03 requires for an all-failing sample. The larger fact that 535903 is a full counterexample for at most two powers of 2 is a theorem of Platt–Trudgian; see LITERATURE.md, L7. Our benchmark checks only the stated single bulk rectangle.

This does NOT assert that the I2 uniform density theorem remains true for bases (2,2). It is not a counterexample to A303656 or to ML-D2 for bases (3,5).

## CE-04. Local correction does not make the prime model multiplicative

In the truncated local torus with k=4, ell=3, and n=358990,
\[
 \rho_1=7/48,\quad \Gamma_7=11/63,\quad\Gamma_{19}=8/189,\quad\Gamma_{133}=0.
\]
All four values are exact rational counts. Thus joint prime divisibility cannot be replaced by the product of the two individual densities. The script also checks signatures 2, 410258, 530230 and 9481394, and the prime-power modulus 49. These fixed truncations are a falsification test of multiplicativity, not an assertion about limiting densities.

## CE-05. A signed square diagonal cannot be discarded

For u=9,
\[
 \sum_{h\mid9}\chi_4(h)=1-1+1=1.
\]
The exact hyperbola identity is 2*chi_4(1)+chi_4(3)=2-1=1. Replacing the diagonal by +1 would give the incorrect answer 3. See DIVISOR_SWITCH.md.

## CE-06. The polynomial absolute-remainder target is false, not merely unproved

PW-02 supplies an unconditional asymptotic counterargument to the proposed random-integer local models. For any fixed 0<a<b<=1 and any M of order (log n)^2,
\[
 \sum_{n^a<p\le n^b,p\equiv3(4)}|N_p-Mg(p)|
 \ge\big(\tfrac12\log(b/a)+o(1)\big)M,
\]
for g(p)=1/p or 1/(p+1), and for either divisibility or odd-valuation incidence N_p. This result applies to the actual base-(3,5) grid as well. It is not a no-go theorem for signed remainder sums or arbitrary sieve weight supports.

## Finite stress panel: old targets, new inequalities

The existing I2 factorization panel contains 35 target entries. Thirty-two have a nonempty bulk A23 set. Their 415 locally corrected bulk rows were checked without extending the original scan.

| n | n mod 24 | Bulk exponent pairs | Bulk A23 pairs | Successful bulk pairs | D(2/log n)/D(1/log n) |
|---:|---:|---:|---:|---:|---:|
| 358990 | 22 | 88 | 16 | 2 | 1.410693342502290 |
| 410258 | 2 | 88 | 15 | 2 | 1.054283586097660 |
| 530230 | 22 | 88 | 12 | 1 | 1.604823302198122 |
| 9481394 | 2 | 140 | 20 | 2 | 1.431561992939726 |

The maximum ratio in this 32-target panel is 1.604823302198122..., at n=530230. All 32 ratios are enclosed below 2 using interval arithmetic at 60 decimal digits. This is finite evidence only: it provides no uniform bound, no growth law, and no effective threshold.

At n=9481394, the task's 150 active pairs refer to the FULL active domain. The bulk rectangle in this package contains 140 pairs; its A23 set contains 20. These domains must not be conflated.

The scripts also check 625 exact local Taylor moments (v=0,...,24 and degrees 0,...,24) and 148 failing old-panel rows to which the quarter-cutoff pair identity applies. Neither finite test replaces the general proofs in POINTWISE_THEOREMS.md.

## Numerical and source-audit limitations

The inequalities on each finite panel target are checked with mpmath interval arithmetic, not inferred from rounded decimals. Exact integer factorization products and primality by trial division are independently checked for this small panel. The supplied archive's 2946 factorization rows, 1584 distinct prime factors, seven manifest entries, and ten NPZ array byte hashes were also validated.

This audits internal consistency and the supplied finite records; it does not re-run or newly certify the entire prior 10^7 scan. No probabilistic factorization output is silently treated as a proof. There is no claimed finite certificate for all sufficiently large n.
