# Targeted primary-source adaptation audit

Consulted 2026-09-14. Source-derived inputs and the present deductions are separate.
No paper below supplies ML-K2. URLs identify sources; no third-party paper text or
PDF is bundled. No claim is made to have reviewed every existing method.

## L1 — Landau counting input

E. Bank, L. Bary-Soroker, A. Fehm, *Sums of two squares in short intervals in
polynomial rings over finite fields*, arXiv:1509.02013, introduction §1.1, (2).
https://arxiv.org/html/1509.02013

The introduction records the classical integer asymptotic
`sum_{m<=x} b(m) ~ K x/sqrt(log x)`.
Only its upper bound is used, in K2-N1. This is a global count of integers,
not a pointwise statement on a sparse shifted exponential grid. The paper's
function-field results are not transferred to the integer problem.

## L2 — Mertens in the class 3 modulo 4

A. Languasco, A. Zaccagnini, *Computing the Mertens and Meissel-Mertens constants
for sums over arithmetic progressions*, arXiv:0906.2132, equation (1).
https://arxiv.org/html/0906.2132

For fixed coprime q,a it records
`sum_{p<=x,p=a mod q} 1/p = (log log x)/phi(q)+M(q,a)+O(1/log x)`.
Here q=4,a=3. The weighted tails in E5 and the infinitely many balanced prime
pairs are derived in this package; they are not quoted as new theorems of the paper.

## L3 — A genuine large-prime completion on a different sequence

P. Kurlberg, S. Lester, L. Rosenzweig, *Superscars for arithmetic point scatters II*,
Forum of Mathematics, Sigma 11 (2023), e37. DOI:10.1017/fms.2023.33.
https://doi.org/10.1017/fms.2023.33

Source facts: Theorem 2.1 uses `A_d=g(d)X+r_d`, dimension 1/2,
`s=log D/log z>=1`, and an absolute remainder bound. In the paper's Gaussian-sector
prime-convolution sequence, Theorem A.1 gives distribution to
`x^(1/2)/(log x)^B0`. Lemmas 2.2 and 2.5 provide respectively
`sqrt(delta)` and `delta^(3/2)` factors multiplying the common scale
`epsilon^2 eta^(-1/2) [Q0/phi(Q0)] x log log x/[phi(Q1) log^2 x]`.
Lemma 2.4 handles a shifted-prime Gaussian-sector count for odd q,Q at most
`x^(2/3-o(1))`. These are sums over long varying integer/prime sequences, not
a pointwise result for each fixed original n.

Present adaptation verdict: its cancellation between the two scales is relevant,
but its input sequence is essential. Removing the long variable and replacing it
by O(log^2 n) literal residuals does not preserve either the distribution theorem
or the Gaussian lattice count. K2-N3 rejects the straightforward absolute-error
substitution under comparable local densities; it does not invalidate the source
theorem or every possible switched-sieve implementation.

## L4 — Complete subgroup intersection, not short-prefix equidistribution

I. D. Shkredov, E. V. Solodkova, I. V. Vyugin, *Intersections of multiplicative
subgroups and Heilbronn's exponential sum*, arXiv:1302.3839v3, Theorem 2.
https://arxiv.org/html/1302.3839v3

For complete subgroups G0,G1 and nonzero additive shift, the k=1 conclusion is
`|G0 intersect (G1+mu)| <= 12(|G0||G1|)^(1/3)` under the theorem's size hypotheses.
These include `|G0||G1|<3^(-3/2)p^(3/2)`, `|G0|>6`, and for j=0,1
`(1/2)(|G0||G1|)^(1/3)<|Gj|<(1/8)(|G0||G1|)^(2/3)`.
There is no sieve dimension or level-of-distribution conclusion.

Present adaptation verdict: actual sets are prefixes of length O(log n), not
complete subgroups. Completion can introduce a power-of-p bound far exceeding
the elementary O(log n) fiber bound. Coset signs and p dividing n also require
care; the stated nonzero-shift result must not be used silently in those cases.
This theorem supplies no summed prime-coverage estimate for G(n).

## Reading boundary

Ford–Maynard's *On the theory of prime-producing sieves* was checked for its
Type-I/Type-II framework, but no result from it is an input to the proofs here.
The arXiv HTML endpoint labelled v1 displayed an internal 2026 date; no version
priority claim is made. The original Iwaniec 1976 paper's metadata was located,
but the attempted full-text download did not succeed. Its original text is not
represented as having been read. The usable half-dimensional theorem above was
read in the primary Kurlberg–Lester–Rosenzweig article itself.
