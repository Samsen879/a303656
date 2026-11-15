# Cross-model theorem: W6 indicator intensity is the bad-prime projection of the weighted density

## Verified definitions and exact references

Sources are local copies of the full reports, not the user's summary alone.

- `w6_report.txt`, lines 57–66: ordinary exponent-pair count preserves multiplicity; distinct shifts are only merged for support calculations.
- Lines 72–98: independent output Haar on I={2} union inert primes; T_2={0} union_{v>=0}2^v(1+4Z_2); T_p={0} union_{v>=0}p^(2v)Z_p^times; s_2=1/2, s_p=p/(p+1), q_y=product_{p in I_y}s_p.
- Lines 551–561: nu_infinity is the joint eventual shift law from growing exponent rectangles; W_y=q_y^-1 int product_{p in I_y}1_Tp(x_p-a_p) dnu_infinity(a).
- Lines 951–962: independently explicit planted-law construction takes (alpha,beta) Haar on Zhat^2, retains compatible multiplicative orders, and sets a_3=5^beta. There is no extra exponent conditioning, row truncation, or independent prime resampling of exponent phases.
- Lines 604–607: W_infinity is the L2 limit of this probability model. It is not an asserted limit of the ordinary integer statistic T_X=R_H/E R_H.
- `b_report.txt`, lines 327–345: split-factor zero-set reduction; lines 353–366: reduced weighted survivor formulation is exactly W6's W_y.

## Theorem

Let F=f_infinity/pi be the full weighted density constructed in A2/V, let F_bad be the sigma-field of complete coordinates p in I, and identify functions on G_I with their pullbacks to G=Zhat. Then

    W_infinity = E_H[F | F_bad]       in L2 and a.e.,
    {W_infinity=0} = {F=0}           modulo Haar-null sets.

Consequently POS_model iff POS, and after A2, both are equivalent to LP. This result does not prove LP and does not prove W6's unweighted SM or L2T.

## Proof, part 1: finite-prefix kernel identity

The local normalized indicator kernels equal the complete norm densities on bad primes:

    a_2(z)=s_2^-1 1_T2(z)=2 1_T2(z)=B_2(z),
    a_p(z)=s_p^-1 1_Tp(z)=(1+1/p)1_{v_p(z) even}=B_p(z),  p inert.

At z=0 the local density may be assigned the same value as the indicator kernel; changing a singleton never changes its Haar measure. Therefore the probability law defined by these kernels is exactly the corresponding norm law on bad coordinates.

For finite I_y and Q=product_{p in I_y}p^(k_p), conditional averaging each kernel over a residue cylinder gives exactly beta_(p^k). Boundary values are essential:

- Odd inert p, v_p(r)<k: beta_(p^k)(r)=(1+1/p)1_{v_p(r) even}.
- Odd inert zero cylinder r=0 mod p^k: beta_(p^k)(0)=1 for k even, and 1/p for k odd.
- At 2, if v_2(r)<=k-2, beta_(2^k)(r) is0 or2 according to oddpart mod4. On r=0 or2^(k-1) mod2^k it equals1.

Thus Tonelli and the joint shift prior give

    E[W_y | x mod Q]
      = int_{Zhat^2} product_{p in I_y} beta_(p^k_p)(x_p-T_3(alpha)_p-T_5(beta)_p) dH(alpha)dH(beta)
      = f_Q(x)/pi.

No primewise factorization of the shift law has been made. All cross-prime exponent correlations survive the integral. In particular T_3 has zero3-adic coordinate, matching W6's explicit a_3=5^beta; 5 is not in I.

The full weighted density has the same finite-quotient projections by definition. Let all k_p tend to infinity for fixed finite I_y. Conditional-expectation convergence identifies

    W_y=E[F | F_I_y].

Equivalently, direct dominated convergence works: each bad-prime beta sequence is uniformly bounded, there are only finitely many primes, and a translated residual-zero singleton has zero output Haar measure (Tonelli in shift and output). Taking y to infinity and using L2 martingale convergence gives W_infinity=E[F|F_bad].

## Proof, part 2: equality of zero sets requires more than conditional expectation

Write J for split primes. For every split prime p, its norm law nu_p has density

    B_p(z)=(1-1/p)(v_p(z)+1), z !=0,

which is finite and strictly positive Haar-a.e.; hence nu_p and H_p are mutually absolutely continuous.

Fix a finite A subset J. Replace only these noise factors by H_p, leaving the whole joint shift law mu and all other noise factors untouched. The old and new source measures are mutually absolutely continuous, including after taking their product with possibly singular mu. Pushforward by addition preserves mutual absolute continuity, so the resulting output rho^A is equivalent to rho.

Adding independent Haar at coordinates A makes those output coordinates Haar and independent of the rest. Thus the density of rho^A is

    F^A = E_H[F | sigma(x_p:p not in A)].

Since rho^A and rho are equivalent, their zero sets coincide modulo Haar-null sets. Therefore Z={F=0} has a version measurable without A, for every finite A subset J.

Choose a countable increasing exhaustion A_m of J. For almost every fixed bad-coordinate environment, the split-coordinate section of Z is a tail event under independent split-coordinate Haar. Conditional Kolmogorov zero-one implies its Haar measure is0 or1. Nonnegativity of F now says that this measure is1 exactly when its conditional mean E[F|F_bad] is0. Hence Z equals the pullback of {E[F|F_bad]=0}, as claimed.

Only finite replacements are asserted equivalent. The proof does NOT assume the infinite split-prime product is equivalent to Haar, and does NOT use an infinite positive product lower bound. Such an infinite lower product would generally collapse.

## Consequences and limits

1. W6's written statement that its positivity equivalence with weighted POS had not been established is an old missing interface now filled by the above proof.
2. W6's REG remains a sufficient arithmetic hypothesis, not an unconditional theorem. After A2, its qualitative model positivity goal is exactly LP.
3. Its SM hypothesis still concerns the ordinary integer statistic T_X=R_H/E R_H and the smaller profile W_infinity=E[F|F_bad]. Weighted V proves a different integer L2 theorem for ordered r_2 weights and full F. Zero-set equality does not identify second moments or transfer errors.
4. At finite core level the distinction is visible: E[(f_120/pi)^2]=107/96, whereas E[W_24^2]=155/144. Projection changes the quantitative profile although the full-limit zero sets agree by the separate proof.
5. No ordinary exponent witness is selected by this model identity; transient c-rows remain a separate issue for actual finite obstructions.
