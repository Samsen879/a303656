# Primary-source literature audit

Accessed 2026-09-10. This is a theorem-scope audit, not a claim of exhaustive coverage of the literature. No source found in this search supplies the missing uniform theorem for the literal pair (3,5). In particular, an almost-all statement, a fixed-shift correlation, and a weighted representation correlation are not interchangeable.

## L1. 原问题与计数

**OEIS A303656**, Zhi-Wei Sun; https://oeis.org/A303656 .  
**OEIS A303429**, successful exponent-pair count; https://oeis.org/A303429 .

A303656 counts quadruples with 0<=a<=b. Its entry states the conjecture and reports verification through 2.4*10^11 by Jiao-Min Lin in 2022. This external reported verification is not newly independently certified here. The present code checks its first 90 listed terms. The positivity question agrees with the unweighted exponent-pair support, although the counts differ.

## L2. Artyom Radomskii — Variants of Romanoff's theorem

Primary text: https://arxiv.org/html/2504.09954v6  
Version checked: v6, 2026-07-13. The author's given name in the primary source is Artyom.

Theorem 1.1 permits multiplicity in the sequence B. Under density and uniform pair-upper-bound hypotheses for A, and a small-prime congruence-average hypothesis for B, it gives

    #{n<=X:r(n)>=c1 B(X)/eta(X)}
      >=c2 X B(X)/(B(X)+rho_B(X)eta(X)).

This is a positive-proportion conclusion, not every-n or almost-all. The assumptions need verification for the desired sequences; applying the displayed scaling alone is insufficient. The literal sums-of-powers family has the expected B(X) scale log^2 X, and eta=sqrt(log X) gives the familiar log^(3/2) many-representation scale.

Example 2 uses odd primitively representable two-square integers. Corollary 1.1 also treats a single polynomial-exponent power and gives positive density in the linear-exponent case. No effective universal threshold for A303656 is supplied. The repository's separately formulated dyadic version is inherited authority, not silently identified with the paper's n<=X statement.

## L3. Kaisa Matomäki and Maksym Radziwiłł — Multiplicative functions in short intervals II

Primary text: https://arxiv.org/html/2007.04290 .

Corollary 1.2(i): for an appropriate multiplicative set N, a positive constant delta exists so that intervals of length h0/density(N;X) containing at most delta*h0 elements have at most

    O_{alpha,epsilon}(X h0^(-1/2+epsilon))

exceptional starting points, for 2<=h0<=X. For two squares the natural length is comparable to h0 sqrt(log X). Section 1.3 discusses this specialization. Corollary 1.1 supplies an asymptotic form with another power-saving exceptional-set estimate.

These are consecutive-interval averages with exceptions, not bounds on the O(log^2 n) residuals at one fixed n. The error does not become less than one at a polylogarithmic h0, and the exponent grid is not an interval. There is therefore no effective A303656 closure threshold to extract from these statements.

## L4. James Maynard — Sums of two squares in short intervals

Primary text: https://arxiv.org/html/1910.13384 .

Theorem 2.2 produces many intervals with unusually many two-square integers. Theorem 4.1 gives, for an admissible collection of k linear forms with k<=(log X)^(1/5) and specified coefficient restrictions, at least X exp(-sqrt(log X)) values of the varying argument where at least sqrt(k)/C forms are two-square integers.

The quantified conclusion is “many arguments,” not every argument. Its linear forms are dense functions of the varying argument, unlike the fixed-n exponent rectangle. Constants and sufficiently-large thresholds do not yield a finite verification threshold for our equation. This work also warns against replacing genuine local distribution by a universal short-interval asymptotic.

## L5. David J. Platt and Timothy S. Trudgian — On the sum of two squares and at most two powers of 2

Primary paper: https://arxiv.org/pdf/1610.01672 .

Theorem 1, read from the original PDF: 535903 is the smallest integer greater than one not representable as two squares plus at most two nonnegative powers of 2. All integers

    2^alpha * 1151121374334, alpha>=0,

also fail. Pages 1 and 2 were visually checked, including the theorem and the scaling argument's setup.

This supplies a rigorous adversarial comparison: the same order of magnitude log^2 X for the shift count can coexist with infinitely many failures. It does not give a counterexample or a no-go theorem for bases 3 and 5. There is no positive universal threshold in that analogous problem.

## L6. Tristan Freiberg, Pär Kurlberg and Lior Rosenzweig — Poisson distribution for gaps between sums of two squares and level spacings for toral point scatterers

Primary source: https://arxiv.org/abs/1701.01157 .

The paper formulates a two-squares analogue of the Hardy–Littlewood k-tuple conjecture and derives Poisson conclusions conditionally on that conjectural correlation input. This source cannot be cited as an unconditional pointwise lower-tail theorem on our growing exponential shift family. The old project outline invokes an indicator-level sieve upper bound; this audit does not turn that upper bound into signed covariance cancellation. No A303656 effective threshold follows.

## L7. Sary Drappeau and Berke Topacogullari — Combinatorial identities and Titchmarsh's divisor problem for multiplicative functions

Primary source: https://arxiv.org/abs/1807.09569 .

The shifted sums described there include sum f(n) tau(n-h), with the two-squares indicator among the functions f. This is not sum b(n)b(n-h). We do not import a uniformity-in-h range or a quantitative error formula that has not been checked in the full relevant theorem. This source was screened out as a direct replacement for the missing indicator covariance estimate, rather than name-dropped as a usable theorem.

## L8. Timothy Trudgian — Uchiyama's conjecture on sums of squares

Primary source: https://arxiv.org/abs/1712.07243 .

This concerns uniform gaps on the x^(1/4) scale. For this report the required qualitative comparison can be proved directly: with a=floor(sqrt(x)) and b=ceil(sqrt(x-a^2)), the sum a^2+b^2 is at least x and exceeds x by at most 2sqrt(2)x^(1/4)+1. Thus every interval slightly longer than that contains a norm.

That interval result does not align the available norm with n-3^c-5^d. I2-D1/I2-D2 show why treating one power as a fine translation does not supply that alignment. No transfer to a uniform sparse-grid theorem is established.

## L9. Additional sparse-variable and current-source screening

Yuhui Liu, https://arxiv.org/abs/2401.01355 , studies an every-sufficiently-large even-integer theorem with six dense prime-power variables and sixteen powers of 2. Removing all but two dense square variables and replacing sixteen sparse terms by the prescribed pair 3^c,5^d is not a specialization of that statement.

E. Malavika and Olivier Ramaré, https://arxiv.org/abs/2604.09448 , study exponential sums on squares of sifted sequences. The phase is n^2 alpha and the underlying support is not the required convolution b(n-3^c-5^d). No applicable transfer theorem was identified; the new result is not used as a black box.

These searches supply neither an every-n theorem for the literal equation nor a justified numeric finite closure threshold. That is a scope conclusion about what was found, not a claim that every analytic approach has been ruled out.

## Tool-by-tool applicability summary

| Tool/result | Quantity actually controlled or needed | Uniform in the original n? | Outcome here |
|---|---|---|---|
| Selberg / half-dimensional / Rosser–Iwaniec sieve | Fixed-n A_q(n) and a summed remainder budget are needed | The elementary periodic remainder is uniform but too large | No lower-bound closure |
| Dispersion / large sieve / bilinear forms | Cancellation across growing congruence/exponent families is needed | No applicable such theorem verified | Research target only |
| Indicator pair upper bounds | Sum over n of b(n-s)b(n-t) | Averaged in n | Positive density, not universality |
| MR short-interval theory | Consecutive-interval counts, with a quantified exceptional set | Almost all starts | Wrong sample geometry and quantifier |
| Romanoff-type theorem | Many n in a long range with many representations | Not every n | Reproduces positive-density scale |
| Classical short-gap theorem | Some norm in each interval of length O(x^(1/4)) | Yes, for interval existence | Does not hit the exponential shift grid |
| Gaussian multiplication | Multiplicative preservation of norm support | Exact | Mixed coefficients leave the shift language |
| I2-P1 in this package | Actual bulk exponent count passing L2 and L3 | Yes, error O((log n)^(5/3)) | Genuine local calculation only |

