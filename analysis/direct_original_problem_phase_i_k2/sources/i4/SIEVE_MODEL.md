# Fixed-n sieve model and its exact limitations

## Sequence, density and remainder

Use the multiset of bulk residuals indexed by A23(n), not a set of distinct integers. Its size M is asymptotic to a positive residue-class-dependent constant times (log n)^2. For q coprime to 30 define A_q by divisibility of those residuals. PW-01 constructs the finite, conditional joint-orbit density Gamma_q using the SAME 2-adic and 3-adic truncation for every q. It proves

\[
 \sum_{q\le(\log n)^\alpha,(q,30)=1}|A_q-M\Gamma_q|
 \ll_\alpha(\log n)^{5/3+4\alpha/3},\qquad 0<\alpha<1/4.
\]

This is genuine fixed-n control of an aggregate of moduli. It is not control at n^theta, nor a claim that these densities obey sieve axioms. In particular the example Gamma_133=0 while Gamma_7 Gamma_19>0 survives the joint local correction. Shared exponent-period factors are retained, not eliminated by integer CRT.

For comparison, on the UNFILTERED rectangle one can use complete periods ord_q(3), ord_q(5), with error O((C+1)ord_q(5)+(D+1)ord_q(3)). Applying that formula unchanged to A23 would be incorrect: the 2/3 predicates themselves have long or unbounded periods. PW-01 explicitly pays for their truncation and the discarded early c rows.

## Odd valuations are not divisibility

The exact identity is
\[
 |E_p|=\sum_{j\ge0}\big(A_{p^{2j+1}}-A_{p^{2j+2}}\big).
\]
It is a finite sum, since all m<n. For an intersection over several primes, expand a product of these differences; the necessary moduli are products of prime powers, not merely squarefree products. Period control at q<=T handles the terms whose complete modulus lies below T. It does not automatically dispose of higher valuation tails. The random-integer densities 1/p and 1/(p+1) are benchmarks, not established local densities for the exponent grid.

A standard multiplicative sieve could discard every p-divisibility event and thereby seek the smaller primitive-norm subclass, but that requires a positive multiplicative main model and controlled remainder. We have neither a proof of that main model for Gamma_q nor a completion estimate after the currently accessible polylogarithmic cutoff.

## Sieve dimension and the three prime ranges

For the independent benchmark g(p)=1/(p+1), the formal Euler product is of scale (log z)^(-1/2). This explains the proposed dimension 1/2; it does not establish that dimension for the actual Gamma_q. The complete-period conditional densities are correlated.

At a polylogarithmic cutoff, even a hypothetical successful half-dimensional sieve would leave roughly M/sqrt(log log n) candidates. That would still not force any of them to be norms. Between this cutoff and n^(1/4), the grid's individual geometric orbits have only O(log n) terms. The literature estimates requiring length >p^epsilon do not cover p=n^theta for fixed theta>0.

At y>=n^(1/4), AUX-01 turns each remaining failure into a unique p q r with two distinct large bad primes and a norm cofactor r<n/y^2. This is the correct pair/product switching geometry. Its counting function may still equal the full survivor count. No inequality reducing that possibility is proved.

The square-root completion from I2 is valid but inaccessible by simply extending the present absolute-error model. PW-02 proves that, against g(p)=1/p or 1/(p+1), a polynomial prime band necessarily contributes Omega(M) absolute error. That is much larger than M/sqrt(log n). The theorem does NOT say that every weighted sieve, every specially chosen support for its weights, or every signed aggregate is impossible.

## Least bad prime capacity

Let X=C+1 and Y=D+1. For p>=7, p=3 mod 4, let t_3=ord_p(3), t_5=ord_p(5). A fixed c gives at most one d-class modulo t_5, and a fixed d gives at most one c-class modulo t_3. Therefore, without any randomness,
\[
 |F_p|\le A_p\le\min\{X\lceil Y/t_5\rceil,
                           Y\lceil X/t_3\rceil\}.
\]
The middle quantity is for the filtered grid; the last bound comes from the unfiltered one, so remains valid after filtering. If both orders exceed the exponent lengths, this only bounds each prime's capacity by min(X,Y), not zero. Distinct medium or large primes may have separate witnesses.

The least-prime condition permits Buchstab-style subtraction of earlier defects, but evaluating that subtraction requires the same joint distributions and valuation information. Neither summing these elementary capacities nor summing M/p produces an anti-cover theorem.

## Verdict

HALF-DIMENSIONAL SIEVE ROUTE: BLOCKED.

There is a new explicit correlated pointwise model and a scoped impossibility theorem for a proposed large absolute-remainder model. There is no positive lower bound for the fully sieved support and no new exclusion of possible counterexample n. The entire sieve approach is not declared dead.
