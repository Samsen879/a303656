# Direct pointwise results — Phase I4

Status: self-contained derivations in this package, not independently refereed or merged authority. No universal representation theorem is asserted. “New” means new relative to the supplied I2 package; priority in the wider literature is not asserted.

## Definitions and imported authority

All logarithms are natural. Put
\[
 L=\log n,\quad C=\lfloor\log_3(n/4)\rfloor,\quad D=\lfloor\log_5(n/4)\rfloor,
 \quad m_{c,d}=n-3^c-5^d.
\]
Only the bulk rectangle is used, so \(n/2\le m_{c,d}<n\). Write \(u(m)=m/2^{v_2(m)}\), and let \(b(m)\) be the two-square indicator. Let
\[
 \mathcal A=\mathcal A_{23}(n)=\{(c,d):0\le c\le C,0\le d\le D,
 u(m_{c,d})\equiv1\pmod4,\ v_3(m_{c,d})\equiv0\pmod2\},\qquad M=|\mathcal A|.
\]
I2 supplies, uniformly in n,
\[
 M=\lambda(n\bmod24)(C+1)(D+1)+O(L^{5/3}),\qquad \lambda\ge7/32.
\]
In particular M is positive and of order \(L^2\) for all sufficiently large n. This is an input, not a new theorem here.

For positive q define \(A_q(n)=\sum_{(c,d)\in\mathcal A}1_{q\mid m_{c,d}}\). The cardinality counts exponent pairs, including any repeated residual values with their multiplicities.

## PW-01. A uniform, correlated, polylogarithmic divisibility model

For each fixed \(0<\alpha<1/4\), there are explicitly defined numbers \(\Gamma_q(n)\in[0,1]\), with \(\Gamma_1=1\), such that
\[
 \boxed{\sum_{\substack{q\le L^\alpha\\(q,30)=1}}
 |A_q(n)-M\Gamma_q(n)|\ll_\alpha L^{5/3+4\alpha/3}.}                 \tag{1}
\]
This holds for every sufficiently large n, not on average over n. The model is a finite joint exponent-period model; it is NOT asserted to be multiplicative in q, nor close to 1/q. It depends on the common truncation chosen below. Equation (1) is not a half-dimensional sieve theorem.

### Construction

Set \(U=L^{(1-\alpha)/3}\). Choose integers \(k\ge3,\ell\ge1\) so that \(2^k\asymp U\) and \(3^\ell\asymp U\), with absolute comparison constants. Discard the rows c<ell. On the remaining rectangle use the stricter predicates
\[
 v_2(m)<k,\quad u(m)\equiv1\pmod4,\quad v_3(m)<\ell,\quad v_3(m)\text{ even}.
\]
The first pair is decided modulo \(2^{k+1}\); the second pair modulo \(3^\ell\). A zero residue at either truncation is rejected. On c>=ell, the mod-\(3^\ell\) residual is n-5^d.

For \((q,30)=1\) set
\[
 T_c(q)=\operatorname{lcm}(\operatorname{ord}_{2^{k+1}}(3),\operatorname{ord}_q(3)),
\]
\[
 T_d(q)=\operatorname{lcm}(\operatorname{ord}_{2^{k+1}}(5),
 \operatorname{ord}_{3^\ell}(5),\operatorname{ord}_q(5)),
\]
where orders modulo 1 are 1. On a complete \(T_c(q)\times T_d(q)\) torus evaluate the truncated predicates and q|n-3^c-5^d, treating the mod-3 c-coordinate as zero. Let \(\rho_q\) be the fraction satisfying them. Define \(\Gamma_q=\rho_q/\rho_1\). For large n, \(\rho_1>0\), as proved below. The torus for q projects uniformly onto the local torus, so \(0\le\rho_q\le\rho_1\); no independence between different primes is assumed.

### Proof, including the local-truncation cost

For each c, the equation \(5^d\equiv n-3^c\pmod{2^k}\) has at most one residue class of d modulo \(2^{k-2}\). The equation modulo \(3^\ell\) has at most one class modulo \(2\cdot3^{\ell-1}\). Consequently the number B of pairs lost from the true local survivor set is bounded by
\[
 B\le \ell(D+1)+(C+1)\left({D+1\over2^{k-2}}+1\right)
 +(C+1)\left({D+1\over2\cdot3^{\ell-1}}+1\right)
 \ll L\log U+L^2/U.                                             \tag{2}
\]
These are upper bounds for the union of losses; overlaps cause no problem.

Write \(X=C-\ell+1\), \(Y=D+1\). For any [0,1]-valued function periodic with periods T and S, tiling an X-by-Y rectangle by complete period rectangles gives
\[
 |\text{count}-XY\cdot\text{period density}|\le XS+YT.
\]
The unfilled boundary has at most this area; the complete blocks are exact. Since
\[
 T_c(q)\ll Uq,\qquad T_d(q)\ll U^2q,
\]
we obtain, uniformly for the q in (1),
\[
 A_q=XY\rho_q+e_q,\qquad |e_q|\ll B+LU^2q.                       \tag{3}
\]
This also holds for q=1. The I2 estimate and (2)–(3) imply \(\rho_1=\lambda(n\bmod24)+o(1)\), uniformly. Thus it is bounded below for large n.

Now \(A_q-M\Gamma_q=e_q-\Gamma_q e_1\). Summing and using \(0\le\Gamma_q\le1\), for T=L^alpha we get
\[
 \sum_{q\le T,(q,30)=1}|A_q-M\Gamma_q|
 \ll TL^2/U+TL\log U+LU^2T^2.
\]
The first and last terms have exponent \(5/3+4\alpha/3<2\); the middle term is smaller. This proves (1). For example alpha=1/8 gives an \(O(L^{11/6})\) aggregate remainder through \(q\le L^{1/8}\). These are very small moduli, not n^theta. QED.

### Explicit failure of multiplicativity after local correction

Take k=4, ell=3, and the residue signature of n=358990. Exact torus counts give
\[
 \rho_1=7/48,\quad \Gamma_7=11/63,\quad
 \Gamma_{19}=8/189,\quad \Gamma_{133}=0.
\]
Thus \(\Gamma_{133}\ne\Gamma_7\Gamma_{19}=88/11907\). This is a finite local-model calculation, not a limiting-density assertion. It explains why (1) cannot simply be plugged into a multiplicative sieve.

## PW-02. Sparse-sample granularity blocks a polynomial absolute-error model

Let \(1\le m_1,\ldots,m_M\le n\) be any multiset, and let \(0<a<b\le1\) be fixed. Let P be the primes \(n^a<p\le n^b\), p=3 mod 4. Let N_p denote either the number of m_i divisible by p, or the number with v_p(m_i) odd. Let \(g(p)=1/p\) or \(g(p)=1/(p+1)\). Then
\[
 \boxed{\sum_{p\in P}|N_p-Mg(p)|
 \ge M\sum_{p\in P}g(p)-{M^2\over a n^a}.}                       \tag{4}
\]
More generally, the subtracted term can be \((M^2/a)\max_{p\in P}g(p)\) for any nonnegative g.

**Proof.** Each m_i has fewer than 1/a distinct prime divisors exceeding n^a. Thus at most M/a primes in P divide any sample member. For every other prime N_p=0, and its absolute error is exactly Mg(p). Subtracting the possible model mass on the hit primes proves (4). No independence or equidistribution is used.

For the application \(M\asymp(\log n)^2\), Mertens' theorem in the fixed progression 3 mod 4 gives
\[
 \sum_{n^a<p\le n^b,p\equiv3(4)}g(p)={1\over2}\log(b/a)+o(1),
\]
so
\[
 \sum_{p\in P}|N_p-Mg(p)|\ge\left({1\over2}\log(b/a)+o(1)\right)M. \tag{5}
\]
The only external analytic ingredient is this standard fixed-modulus Mertens formula; see LITERATURE.md, L6. In particular an o(M) absolute-remainder hypothesis against either random-integer model is FALSE on a polynomial prime band, even for our exact grid. This does not rule out signed estimates, specially supported sieve weights, or an orbit model whose mass fails the hypotheses of (4).

## PW-03. Positive divisor transforms encode the number of odd valuation defects

Write \(\chi=\chi_4\). For odd u>=1 define
\[
 d_u(s)=\sum_{h\mid u}\chi(h)h^{-s},\qquad
 F_u(s)=u^{s/2}d_u(s)=\sum_{h\mid u}\chi(h)e^{s\log(\sqrt u/h)}.
\]
For real s>0, \(d_u(s)>0\). If u=1 mod 4, then F_u is an even entire function with nonnegative Taylor coefficients. Its order of vanishing at s=0 is exactly
\[
 k(u)=\#\{p\equiv3\pmod4:v_p(u)\text{ odd}\}.
\]
In particular k(u) is even, F_u(0)=r_2(u)/4, and if u is not a two-square norm then
\[
 \boxed{F_u(2s)\ge4F_u(s)\qquad(s>0).}                           \tag{6}
\]
More precisely, the factor 4 can be replaced by \(2^{k(u)}\).

### Proof

The local factor of d_u(s) at p^v||u is \(\sum_{j=0}^v(\chi(p)p^{-s})^j\). It is positive for s>0: in the alternating case it equals
\((1-(-p^{-s})^{v+1})/(1+p^{-s})>0\).

For x=s log p the corresponding factor of F_u is
\[
 P_v(x)=\sum_{j=0}^v e^{(v/2-j)x}\quad(p\equiv1\pmod4),
\]
\[
 E_v(x)={\cosh((v+1)x/2)\over\cosh(x/2)}\quad(p\equiv3\pmod4,\ v\text{ even}),
\]
\[
 O_v(x)={\sinh((v+1)x/2)\over\cosh(x/2)}\quad(p\equiv3\pmod4,\ v\text{ odd}).
\]
The quotients here equal finite exponential sums; their apparent complex singularities are removable.

P_v has only nonnegative even coefficients. For v=2r,
\[
 E_{2r}(x)=(-1)^r+2\sum_{j=1}^r(-1)^{r-j}\cosh(jx).
\]
Its constant is 1. Every nonconstant even coefficient is positive, because its numerator is a descending alternating sum of strictly decreasing positive powers, paired as positive differences. For v=2r+1,
\[
 O_{2r+1}(x)=2\sum_{j=0}^r(-1)^{r-j}\sinh((j+1/2)x),
\]
whose odd coefficients are all positive by the same pairing. Its first nonzero degree is 1. Multiplication of these series proves the coefficient and vanishing-order assertions. Since \(\chi(u)=(-1)^{k(u)}=1\), k is even. The value at zero is the standard divisor formula for r_2. Finally every nonzero term in a failing row has degree at least k>=2, so doubling s multiplies it by at least 4. QED.

## PW-C01. One precise missing lemma suffices for all sufficiently large n

For the ACTUAL literal-base grid, define the positive mass
\[
 \mathcal D_n(s)=\sum_{(c,d)\in\mathcal A}d_{u(m_{c,d})}(s)
 =\sum_{h\le n}\chi_4(h)h^{-s}A_h(n),\qquad s>0.                \tag{7}
\]
The equality holds since even h have chi_4(h)=0. This is not averaged in n and uses no factorization-dependent weight in A_h.

**Missing lemma ML-D2 (UNPROVED).** There exists N_* such that every integer n>=N_* satisfies
\[
 \boxed{\mathcal D_n(2/\log n)\le2\mathcal D_n(1/\log n).}        \tag{ML-D2}
\]
The constant 2 is fixed, as is the scale 1/log n. No threshold N_* is claimed.

**Conditional theorem.** ML-D2 and I2 imply representability for all sufficiently large n.

**Proof.** I2 makes \(\mathcal A\) nonempty, so \(\mathcal D_n(s)>0\). If every row fails, (6) and u<=n imply
\[
 d_u(2s)=u^{-s}F_u(2s)\ge4u^{-s/2}d_u(s).
\]
For s=1/log n this yields
\[
 \boxed{\mathcal D_n(2/\log n)\ge{4\over\sqrt e}\,
 \mathcal D_n(1/\log n)>2\mathcal D_n(1/\log n),}                \tag{8}
\]
contradicting ML-D2. Thus a bulk row is a norm. This proof applies to the worst mod-24 classes as well. QED.

The implication is proved; ML-D2 is not. It is stronger than mere positivity of a representation count. COUNTEREXAMPLES.md gives a locally correct bulk multiset containing a genuine norm but violating ML-D2. Conversely, the algebraic theorem applies to many bases; ALL literal-3/5 content still has to enter the proof of ML-D2. No claim that ML-D2 is easier than the original problem is justified yet.

## PW-04. An optional bounded fourth-order signed minorant

This auxiliary weight is separate from the unnormalized mass in ML-D2. Put
\[
 Z_u(s)=F_u(s)/\tau(u),\qquad
 \omega_{\kappa,n}(m)={4Z_u(\kappa/L)-Z_u(2\kappa/L)\over3}.
\]
For u=u(m)=1 mod 4 and m<=n,
\[
 \omega_{\kappa,n}(m)\le Z_u(0)={r_2(m)\over4\tau(u)}\le b(m),
\]
\[
 0\le Z_u(0)-\omega_{\kappa,n}(m)
 \le {\cosh\kappa-4\cosh(\kappa/2)+3\over3}
 ={\kappa^4\over96}+O(\kappa^6).                                \tag{9}
\]
Notice tau(u), not tau(m); the weight is not identical to the frozen nu_tau proxy.

**Proof.** By PW-03 write \(Z_u(s)=\sum_{j\ge0}a_{2j}s^{2j}\), a_{2j}>=0. The operator (4Z(s)-Z(2s))/3 preserves the constant, cancels the quadratic term, and subtracts every higher term. Also, from the finite divisor expansion,
\[
 a_{2j}\le{(\log u/2)^{2j}\over(2j)!}.
\]
Summing this majorant for j>=2 proves (9). The constant Z_u(0) is zero on nonnorms and, on norms, equals the product of 1/(v_p(u)+1) over p=3 mod 4, so it is at most 1.

For 0<kappa<=1, omega is positive on norms and nonpositive on nonnorms. For the former assertion, logarithmic differentiation of each local factor gives \((\log F_u)'(s)\le(3/4)\log u\): the good-prime bound is (v/2)log p, and the bad-even bound is ((v+1)/2)log p <=(3v/4)log p. Thus F_u(2s)/F_u(s)<=exp(3kappa/4)<4. This is an exact sign detector, but positivity of its SUM is not proved. A fixed O(M) total error in (9) does not establish the desired lower tail.

## AUX-01. Exact quarter-cutoff pair completion (not promoted as exceptional-set compression)

Let y>=n^(1/4), and restrict A to rows whose odd bad-prime valuations all occur above y; call this S_y. A failing member of S_y has exactly two distinct odd-defect primes p<q, both >y, each to exponent exactly one. Indeed k is a positive even integer; four distinct defects, or exponents at least 3 and 1, would give a product >y^4>=n. Therefore uniquely
\[
 m=pqr,\quad p<q,\quad p,q>y,\quad p,q\equiv3\pmod4,\quad b(r)=1,\quad r<n/y^2.
\]
Consequently the failing count equals exactly
\[
 |S_y|-R_{\rm bulk}(n)
 =\sum_{r<n/y^2}b(r)\sum_{\substack{y<p<q\\p,q\equiv3(4)}}
 \#\{(c,d)\in\mathcal A:n=3^c+5^d+rpq\}.
\]
This is a valid switching identity, not an upper bound. Neither a large enough S_y nor a small enough right-hand side is established here. At y>=sqrt(n), the failure count is zero, a size-completion fact already present in I2.
