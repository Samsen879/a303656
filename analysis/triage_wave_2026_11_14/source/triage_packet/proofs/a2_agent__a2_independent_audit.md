# A2 independent proof audit

Scope: A2 weighted profinite support theorem and R1 corrections. Not the integer L2 transfer and not C21.

## Verdict

ACCEPT WITH SOURCE/EXPOSITION CORRECTIONS on the visible proof. No decisive gap found in A2 §§2–6 after independent line-by-line review. This is a scoped referee result, not a proof of LP, POS, almost-all, or the original conjecture.

## Objects

E=Zhat^2, exponent prior product Haar; T_b(alpha)_p=0 when p=b and b^alpha otherwise. mu=(T_3+T_5)_*H^2. nu=Law(U^2+V^2). rho=mu*nu=F H. f_q=pi E[F|mod q], f_inf=pi F; mu_q is a probability mass function and beta_q=#ordered square-coordinate pairs/q.

## Proof checks

1. Global Romanoff sum sum_{(d,5)=1}1/(d ord_d 5)<infinity gives F in L2 via Gauss sum and finite Parseval; powers of 5 contribute 5/4, so no missing prime-power term.
2. Harmonic smooth-order tail is proved uniformly in cutoff y using Pomerance-Shparlinski in a finite range to X0=y^(8loglogy), then exact-order prime count for ord<=sqrt(X0), then Rankin for larger smooth orders. Fixed bounded y handled by finite Euler products. No extrapolation of the cited range to infinity.
3. P-rough conductor tail sum sum_(d,prod_{ell<=P}ell)=1 [d r_P(ord_d 5)]^-1 is uniformly bounded. Majorizing by unrestricted prime powers is legitimate and cannot omit squareful denominators. The separate full conductor sum carries an O(log P) factor; it is not used for the uniform conditional tail estimate.
4. Fix all low exponent primary coordinates theta=(alpha_ell,beta_ell)_(ell<=P). Tail exponents remain independent Haar. Conditioned power orbit modulo q has cardinality r_P(ord_q 5); full Parseval is q/r_P. This holds for all theta, not just almost every theta.
5. Uniform L2 tail kernels g_theta mix with the exact nonnegative weights k_theta(x)=prod_(p<=P) B_p(x_p-s_p(theta)). Weighted Cauchy-Schwarz yields E[F^2|F_P] <= C0 E[F|F_P]^2 with C0 independent of P and x. All dependencies of low output lie in low exponent primary coordinates because ord_(p^k)(b)|p^(k-1)(p-1).
6. Conditional Paley-Zygmund plus Levy differentiation gives {F=0}=union_P{F_<=P=0} a.e.
7. The finite-modulus bridge is independently valid. Condition on alpha mod M3 and beta mod M5 with M_b killing all tame orders in finite prime set S, then write alpha=a+M3 gamma, beta=b+M5 delta. At each p, unit-base power law is additive Haar on b^a+p^(k_b,p)Z_p. The sum is Haar on a ball at depth K_p=min(k_3,p,k_5,p). Own-base depths are infinity; other base guarantees finite K_p for p=3,5. For p=2, M3 even yields k_3,2>=3 and k_5,2>=2. Different p use independent gamma_p,delta_p after conditioning. Thus mu_S and rho_S are invariant under an open additive subgroup; finite marginal is locally constant and exactly a finite quotient pullback.
8. Consequently {f_inf=0}=union_q{f_q=0}=G\supp(rho) a.e., and POS iff LP. LP remains open.

## External citation repair

Pomerance–Shparlinski, Smooth Orders and Cryptographic Applications, Theorem 3, printed p.344: lower y=exp(sqrt(log x * loglog x)), NOT exp(sqrt(log x)*loglog x). The A2 working range is narrower and still valid. General fixed integer base extension is explicit on printed p.346 and independently follows from #prime divisors with order t = O_b(t). R1 repairs the source Theorem 1 shell upper index to floor(log(y/z)) and separates bounded u. These are sufficient; no GRH added. Primary source: https://math.dartmouth.edu/~carlp/PDF/paper128.pdf .

## Exact independent core check

At q=120, eventual 3 cycle length4 and eventual 5 cycle length2, min(F_120)=7/15 at residues50,70,80,100; E F_120=1; E F_120^2=107/96. q=240,360,600 give exact pullbacks. Proof of core stabilization: M3=4,M5=2 => K2=3,K3=1,K5=1, so m({2,3,5})=120. This is a finite arithmetic check plus an explicit lifting proof, not evidence for LP outside the core.

## Adversarial countermodel confirming necessity of the bridge

Let A_j be the all-zero event in disjoint Z2 digit blocks of lengths j+1, j>=1. W=6 sum_j 2^-j 1_Aj is continuous, nonnegative, bounded, mean1. Every finite-modulus conditional mean is strictly positive because of unused future blocks. For full-prime filtration containing Z2, relative conditional L2 holds with constant1 since W is already measurable. Yet H(W=0)=prod_j(1-2^-(j+1))=0.5775761901732... . Hence continuity and full-prime relative L2 alone fail; the local constancy established in A2 is genuinely used.

## Transient ordinary rows

All split prime factors, including5, can be deleted from an eventual finite-zero criterion because beta_(p^k) is positive everywhere. If the resulting modulus is3^C m with (m,15)=1, then every ordinary pair c>=C and every d>=0 belongs to the eventual support modulo that modulus. The zero therefore confines any actual witness to c<C. It does not remove those transient rows. C=0 would kill every row and give a genuine modular counterexample; the theorem does not establish such a zero.
