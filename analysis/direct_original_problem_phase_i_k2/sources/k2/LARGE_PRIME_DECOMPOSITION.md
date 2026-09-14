# Definitions, inherited structure, and the size split

All logarithms are natural. Exponent pairs, including repeated shifts, are counted
with multiplicity. This is **not** the weighted count of choices of `(a,b)`.

Let
\[
\mathcal D(n)=\{(c,d)\in\mathbb Z_{\ge0}^2:3^c+5^d\le n\},\qquad
m_{c,d}=n-3^c-5^d.
\]
Write `b(m)` for the two-squares indicator, with `b(0)=1`, and
\[
R(n)=\sum_{(c,d)\in\mathcal D(n)}b(m_{c,d}).
\]
For positive `m`, the local set `G` imposes
\[
\operatorname{oddpart}(m)\equiv1\pmod4,\quad
v_3(m),v_7(m),v_{11}(m)\in2\mathbb Z.
\]
Zero passes every filter. Denote its cardinality by `H=G(n)`.
Every norm passes these necessary tests, so **R_G(n)=R(n)**.

The accepted Phase K input is
\[
H=\rho(n)J(n)+O((\log n)^{9/5}),\quad
J(n)=(\lfloor\log_3n\rfloor+1)(\lfloor\log_5n\rfloor+1),\quad
\rho(n)\ge\rho_0=1869/12800.
\]
In particular, for all sufficiently large n,
\[
 a_0(\log n)^2\le H\le J(n),\qquad
 a_0=\frac{1869}{25600\log3\log5}>0.                       \tag{D1}
\]
The initial threshold depends on the constant in the inherited error; it is not
made effective here. Hash verification of the input is not an independent proof
of all its mathematics.

## Exact least-bad decomposition

For a failed positive survivor define
\[
K(m)=\prod_{\substack{p\equiv3\ (4)\\v_p(m)\text{ odd}}}p,
\qquad P(m)=\min\{p:p\mid K(m)\}.
\]
For a norm use `P=NONE`. Since the odd part is 1 mod 4, the number of primes
in this squarefree kernel is even. A failure therefore has at least two distinct
kernel primes, all at least 19. If `p=P(m)` and `q` is the next kernel prime,
\[
p<q,\qquad pq\le m\le n,\qquad p<\sqrt n.                 \tag{D2}
\]
Consequently
\[
R(n)=H-\sum_{\substack{19\le p<\sqrt n\\p\equiv3\ (4)}}N_p^G(n).
                                                                    \tag{D3}
\]
The empty range `p>=sqrt(n)` is elementary inherited structure, **not** a newly
closed nontrivial range.

Define `T(t;n)` as the number of members of G with no odd-valuation bad prime at
most `t` (including norms and zero). At an eligible prime p,
\[
N_p^G(n)=T(p^-;n)-T(p;n).                                  \tag{D4}
\]
This is the exact least-prime/Buchstab-style partition. It includes all the
conditioning on earlier primes. It does not itself estimate its successive jumps.

## A proof-driven size split

Set
\[
z(n)=\max\{19,2H\},\qquad y=n^{1/4}.
\]
For sufficiently large n, `z<y`; D1 gives `z` of order `(log n)^2`. The first
cutoff is chosen at the **integer-distance transition**: for p>2H the putative
unconditioned mean H/(p+1) is below 1/2. The second cutoff is the exact inherited
kernel transition to a unique pair. These are audit cutoffs, not a claim of a
successfully optimized completion sieve.

The three disjoint contributions are
\[
F_s=\sum_{19\le p\le z}N_p^G,
\quad F_m=\sum_{z<p\le y}N_p^G,
\quad F_v=\sum_{y<p<\sqrt n}N_p^G,
\]
where the prime congruence is understood. Thus `R=H-F_s-F_m-F_v`.

- Small-large primes: exact finite orbit formulas are available for specified
  moduli. No uniform accumulated least-bad estimate for this growing cutoff
  has been proved. Finite periodicity does not supply independence over products.
- Medium primes: individual fibers are small relative to H, but there is no
  aggregate saving. The absolute-remainder obstruction applies to standard
  smooth local models in this range.
- Very large primes: the unique-pair identity below is available; its total
  incidence has no established strict saving.

Changing z to `(log n)^A` for any fixed A does not bridge the gap to y=n^(1/4).
No positive range-total conclusion is inferred from this observation.

## Inherited quarter-cutoff identity (Phase J, not a new K2 theorem)

Among members of `T(y;n)`, with y=n^(1/4), a failure has exactly two kernel primes
p<q>y. Four such primes would have product greater than n. Each of p,q has
valuation exactly one: an odd valuation at least three would give p^3 q>n.
The remaining quotient is a norm. Hence
\[
m=pq u,\quad p<q,\quad p,q\equiv3\pmod4,\quad p,q>n^{1/4},
\quad u\in\mathcal S_2,\quad u<\sqrt n.                    \tag{D5}
\]
Conversely, if a positive locally admissible residual has such a factorization,
the size condition prevents p or q from dividing u, and it fails precisely at
this kernel pair. The pair is unique **within that residual**.

Let V_y(n) count exponent pairs satisfying D5, once per pair. Then
\[
R(n)=T(y;n)-V_y(n),\qquad V_y(n)=F_v.                       \tag{D6}
\]
Neither `T(y;n)>0` nor `V_y<T(y;n)` has been obtained from the Phase K input.
Writing D6 is not counted as new completion progress.
