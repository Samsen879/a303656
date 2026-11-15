# B / W4 / A2 cross-audit

## Models and normalization

All three address the weighted eventual-power norm convolution, with f_q/pi mean one. However their auxiliary posteriors differ.

A2 uses full rho=mu*nu=F H. W4 uses the same full density, M_y=E[F|all complete prime output coordinates q<=y], with d eta_(p,x)(e) proportional to product_(q<p) B_q(x_q-T_q(e)) de. All earlier split outputs are retained, and higher p-adic digits of earlier outputs remain observed.

B first replaces all split-prime residual norm laws by Haar. Its survivor M_y=W_y mu(T_y), W_y=2 product_(p<=y,inert)(1+1/p), uses only complete 2-adic and inert-prime output histories. Its posterior is the exponent prior conditioned on T_y, equivalently indicator(T_y)/mu(T_y). Its 'whole posterior' is whole for this reduced model. B section3 proves equality of zero events between full and reduced densities; it does NOT identify these two posteriors pointwise.

## Hellinger criterion

For each model separately, write kappa_p=sum_a posterior_p(a)^2, V_p=(kappa_p-1/p)/p, and H_p=E[(sqrt(U_p)-1)^2|past]. Bounds c V_p <= H_p <= V_p+O(p^-2), with absolute c>0, are valid without a regularity hypothesis. Hellinger product lemma gives positive limiting density iff no finite extinction and sum H_p<infinity, equivalently sum V_p<infinity. No inverse-moment uniform integrability or independence of prime posteriors is assumed.

Important notation conflict: B C_p is kappa_p (collision probability), while W4 section9 C_p is I_p=1_{max posterior_p >1-1/p} (near-Dirac indicator). Never merge these C_p symbols.

B further restricts the collision series to simultaneous base-3/5 nonregular inert primes using a split product and its arithmetic recovery theorem. W4 restricts to sum_(p in W) I_p/p via predictable prime-hit events and an actual polynomial L2 convergence rate. The J_p hit events are independent under output Haar because their conditional probabilities equal deterministic1/p; arithmetic posteriors themselves are not independent.

## Interaction with A2

A2 proves full zero set equals union of finite-zero cylinders. Full-prime local constancy makes no finite extinction equivalent to surviving support, a.e. For B, split-factor deletion and its proved zero-event reduction transfer the same result to inert-only survivor filtration. Hence there is no extra infinite extinction on surviving support.

Therefore Hellinger/collision/near-Dirac summability on surviving paths is already a qualitative consequence of A2. With the reports' post-extinction convention posterior uniform and V_p=0, these series are in fact finite for Haar-a.e. environment globally: on finite-extinction paths only finitely many terms remain, and on survivors the product criterion applies. Thus summability is NOT a second independent qualitative gate beyond LP in the current combined wave.

The older conditional assumption sum_(p in W)1/p<infinity is no longer needed for qualitative finite-zero-set equality after accepting A2. It remains a valid sufficient condition within the older B/W4 arguments. Their sparse-exception theorem is not contradictory to the stronger unconditional A2 theorem.

## Factorial extinction

B's independent argument is sound on inspected text: conditional tail variance <=M_y A(y), A(y)=O(y^-1/2 polylog(y)); fixed K>2C gives a uniformly positive recovery chance from M_y>=y^-C, contradicting the conditional probability tending to1 on zero-limit paths. Stabilization Q_Iy | (3y^2)! and conditional Markov with summable pi/j^2 transfer this to f_(j!). All quantifier orders are correct.

A2 now implies a stronger fact: a.e. f_inf(x)=0 entails f_(j!)(x)=0 for all sufficiently large j, because a finite q-zero cylinder contains x and eventually q|j!. B's superpolynomial extinction dichotomy is therefore subsumed qualitatively. Its small-value, negative-log and inverse-moment diagnostics remain correctly stated quantitative sufficient criteria, not unconditional POS.

## W4 quantitative rate

Inspected proof of squared L2 rate ||F-M_y||_2^2 = O(y^-1/2 (1+log y)^3) is coherent. It integrates squared unnormalized posterior atom masses over all old outputs before applying the prior order bound. This order of integration is essential and legitimate; it never replaces a pointwise posterior by its prior. Local kernel tails satisfy exact ||B_p-beta_(p^s)||_2^2=p^(-s-1), uniformly in logarithmic depth. Factorial projection error is bounded by product L2 norm times 2^-v2(j!) + sum_(odd p<=j) p^(-vp(j!)-1). Splitting at sqrt(j) gives the claimed factorial squared L2 rate. This rate is new quantitative information not supplied by A2 alone.

## Status

B and W4 full texts support the reported weighted model criteria and quantitative statements in the inspected sections. Both explicitly leave ordinary-integer L2 transfer open. Neither should be counted as an independent proof of V or an unweighted model statement. Their old9-root and2-root finite bounds are superseded only within the same eventual-power finite-zero notion by a valid22-root C21 result.
