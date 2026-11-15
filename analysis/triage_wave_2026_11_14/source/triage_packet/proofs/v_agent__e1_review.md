# E1 referee scope memo

This is an independent scope/proof audit of REPORT_zh.md and proofs 01, 03, 05, 08 in the supplied E1 package. It is not acceptance of every theorem labelled PROVED in that package.

**Later interface update:** the subsequently refereed unit-noise support theorem applies to E1's exact C32 primitive profile. It now proves finite primitive positivity <=> primitive POS <=> MP-LT. Thus the separate quantitative lower-tail concern below is superseded by this new analytic input; E1's own finite primitive positivity remains OPEN, and original norm LP/POS is still a different gate. See e1_unit_noise_interface.md for the independent proof and the safe C22 corollary.

## 1. Fixed-core high-cutoff no-go: ACCEPT in stated scope

Fix W, a finite prime set C and 0<delta0<1/2. Uniformly for delta(X) in (0,delta0], z=X^(1-delta), 1<=D<=sqrt(X), and 0<=s<=X/2, let w_s be a real pointwise minorant of q_z on [X-s,2X-s]. It may depend arbitrarily on X,delta,s and the data m mod W; chi4(oddpart(m)); the **full** inert squarepart a3(m); all exact valuations at inert p<=D; and all exact valuations at primes in C. The proof gives

    sum (w_s)_+ <<_{W,C,delta0} D sqrt(X)/sqrt(log X) + X^(3/4).

Consequently for J comparable to log^2(X) shifts the fraction at which the sum of these minorants reaches kappa log^(3/2)(X) tends to zero if D=o(sqrt(X)). Delta need not tend to zero. There is no restriction that the weights be linear divisor sums or nonnegative.

The critical indistinguishability is valid even if a newly inserted large inert q already divides a3: replacing its even valuation 2e by 2e+1 leaves floor(v_q/2)=e. The second inserted prime is distinct. Fixed-AP prime existence puts the altered number in [1.1X,1.2075X], hence in every allowed shifted interval. The proof retains residue mod W, oddpart character, all visible valuations and the entire a3, while making q_z=0.

The sharper double-log expression in the main report and its claimed sharpness in proof 02 were not fully audited here. The weaker bound above suffices for the no-go claim selected for triage.

## 2. Growing W: accept specified extensions; reject unrestricted extrapolation

If W<=log^A(X), product(C)<=log^A(X), and D<=sqrt(X)/log^B(X) for fixed A,B>0, the argument survives with a factor exp(O_A(sqrt(log log X)))=log^{o(1)}(X). Siegel-Walfisz is applied only at prime scale >=X^(1/4), with modulus polylog(X). Thresholds need not be effective.

If the split primes occurring in W and C lie in a fixed finite set, arbitrary slow D=o(sqrt(X)) is also supported. Otherwise no uniform statement for arbitrary growing W and arbitrary slow D is valid.

The explicit counterexample in proof 03 works: L=log X, y=log L, f=log y, D=sqrt(X)/f. Choose split primes 4f^2<p<=y whose reciprocal sum tends to 1/2, with product W<=L. Then

    w_X(m)=1_{chi*(m)=1} q_D(m) 1_{gcd(m,W)>1}
          =1_{S2}(m) 1_{gcd(m,W)>1}       (m<=2X).

Indeed a nonsum of two squares with positive oddpart character must have at least two distinct odd-valuation inert primes q,r>D; the additional split divisor p>4f^2 forces pqr>4X. Landau plus finite-order Bonferroni yields a positive first moment asymptotic K(1-exp(-1/2)) X/sqrt(log X), uniformly over the allowed shifts. The package's positive-fraction aggregate conclusion additionally needs the actual indicator second moment; its source proof was not reread here, but the needed O(X log^3 X) bound also follows from the elementary exact-v1 upper sieve already independently reconstructed during the E2 audit and the all-composite Romanoff average.

## 3. Signed low-cutoff hybrid: covariance reduction supported, MP-LT remains OPEN

Proof 05 has a legitimate independent small-block beta=30 L2 estimate. It is not an L1-to-L2 substitution: terminal-chain bounds, both parities, followed by an exact Bernoulli/CRT second-moment calculation give an exponentially small relative L2 remainder. The ratio (30/29)^16/2 is <1.

For fixed eta>0, the hybrid uses y=X^(1/2-eta), total level D=X^(1/2-eta/2), and a moving boundary w with log w comparable to log X/log log X. The vector sieve is signed and is only a minorant of the **primitive low-cutoff** indicator. Its normalization C_X is bounded below by c sqrt(eta)/sqrt(log X).

The moving large-block mean inequalities were cross-checked against Iwaniec 1976, Lemmas 16-17: the upper bound for the upper mean and the lower bound for the lower mean have errors depending on K but not on the lower defect L_w=O(log w). Thus the growing lower defect does not invalidate exactly the two inequalities used. No asymptotic equality for the moving-block mean is claimed or needed.

Coefficient Fourier expansion, conditional projection onto denominators dividing W, the exact CRT endpoint error, the convergent weighted Romanoff series, and the large-denominator Rankin bound are consistent. The diagonal crude collision bound O(J log X) is sufficient. For every fixed eta, all eta-dependent error terms vanish as X tends to infinity before any eta limit.

The remaining arithmetic input is exactly

    inf_{Q>=2,t>0} [ b_Q(t) + C T(Q)/t^2 ] = 0,      (MP-LT)

where b_Q is the lower-tail proportion of the finite C32 **primitive unit-avoidance** profile, and T(Q) is the proved analytic tail. The established exceptional-density inequality is

    limsup exception_fraction <= b_Q(t)+C T(Q)/t^2+C' eta/t.

Parameter order: choose fixed Q,t, then fixed eta sufficiently small, then X tends to infinity. Finite positivity of every profile does not supply the required quantile bound. A2 weighted norm positivity does not automatically give this primitive-profile condition: the norm model permits positive even valuations, while the primitive model forbids every inert divisor. The C32 repair removes extra 2-adic zeros but does not solve the odd-prime primitive positivity problem.

## 4. Spectral endpoint: ACCEPT as a finite identity/inequality

Proof 08's two-sided bound

    | sum_I |T-M_W|^2 - N S_W | <= D^2 S_W

and nonuniform refinement with (3/2)D sum q A_q^2 E_q follow from the Montgomery-Vaughan 1973 cosecant Hilbert inequalities. The relevant original Lemma 2, equations (2.1),(2.2), was visually checked in the primary PDF. Farey frequency separations are at least D^-2 and at frequency denominator q at least (qD)^-1. Two phase rotations cancel the factor 1/2 in the geometric-series denominator. This endpoint statement does not itself bound S_W or resolve lower quantiles.

## 5. Cross-lane conclusion

There is no E1/E2 conflict. E2's bounded exact-support triangular weight reads the full r2 factorization and lies outside E1's stated local-information class. E1's own signed low-cutoff hybrid also lies outside the high-cutoff pointwise no-go hypotheses and retains an explicit completion-tail error. There is no E3 conflict: its fixed-W classwise Cauchy ceiling and E2's growing outer modulus concern different limiting procedures.

The statements that must be rejected are: arbitrary growing-W no-go; all methods below sqrt(X) are impossible; the signed hybrid proves almost-all without MP-LT; or A2/V automatically discharges primitive MP-LT.

## Primary source locations actually checked

- Iwaniec, The half dimensional sieve, Acta Arith. 29 (1976), 69-95, hypotheses Omega1/Omega2 and Lemmas 16-17: https://matwbn.icm.edu.pl/ksiazki/aa/aa29/aa2914.pdf . Cached full text was readable although some direct PDF fetches returned 403; page 71 screenshot was readable. Lemmas 16-17 were read as indexed primary full text.
- Montgomery-Vaughan, The large sieve, Mathematika 20 (1973), 119-134, Lemma 2 and equations (2.1),(2.2): https://personal.science.psu.edu/rcv4/personal/Publications/large_sieve.pdf . Page 122 image checked.
- Kurlberg-Lester-Rosenzweig, Superscars for arithmetic point scatterers II, author PDF dated Oct. 10 2020, Lemmas 2.2 and 2.4: https://kurlberg.github.io/eprints/2dscar.pdf . Used to verify provenance of sqrt(eta) gain and eta^(3/2) completion mechanism, not as a substitute for this package's application-specific proof.

