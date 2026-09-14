# Primary-source theorem acquisition and attempted adaptation

Public-source check: 2026-09-10. Source statements below are separated from this package's deductions. PDFs were inspected at the relevant mathematical pages, including screenshots for displayed formulas. No retrieved theorem proves the required lower tail for a fixed target and two logarithmic-length literal orbits. This is a report of this search, not a theorem of literature nonexistence.

## L1. Kurlberg: incomplete geometric-orbit exponential sums

Pär Kurlberg, *Bounds on exponential sums over small multiplicative subgroups*, arXiv:0705.4573. Source: `https://arxiv.org/pdf/0705.4573`, Theorems 1.1 and 5.1; PDF pp. 2, 13.

For every fixed alpha>0 there is beta(alpha)>0. If p is prime, g has order at least T modulo p, and H={g^t:0<=t<T} with T>p^alpha, then every nontrivial additive character satisfies
\[
 |\sum_{x\in H}\psi(x)|\ll_\alpha T p^{-\beta(\alpha)}.
\]
The complete-subgroup theorem has the corresponding hypothesis |H|>p^alpha. Uniformity is in p, the character and eligible g, with alpha fixed.

**Adaptation:** apply g=3 or 5, T=C+1 or D+1, only when the order and length conditions actually hold. At p=n^theta, T=O(log n)<p^alpha for every fixed positive alpha. Formally allowing alpha to tend to zero does not retain the theorem's fixed constants. Thus this candidate can address some polylogarithmic moduli, not the polynomial prime range needed for completion. It does not directly cover arbitrary composite moduli or the local-filtered double sum.

## L2. Friedlander–Wooley: a genuine pointwise semi-linear sieve and pair completion

John B. Friedlander and Trevor D. Wooley, *On Waring's problem: two squares and three biquadrates*, arXiv:1211.1823v2. Source: `https://arxiv.org/pdf/1211.1823`, Theorem 1.1 and Section 3, especially (3.1)–(3.3), PDF pp. 5–6.

Theorem 1.1 assumes RH for L(s,chi_{2n}) and L(s,chi_{-2n}) and Elliott–Halberstam. It gives the stated representation for large n with 8 not dividing n, n not 2 mod 3 and n not 14 mod 16. Their model includes A={N-2p^2:p=1 mod 3, p<sqrt(N/2)}. Taking z=N^(1/2-epsilon), distribution level D=N^(1/2-epsilon/2), and s=log D/log z, their sifted lower bound has a sqrt(s-1) factor. Their large-prime-pair upper bound has an (s-1)^(3/2) factor, permitting completion when s is sufficiently close to 1.

**Adaptation:** the pairing mechanism is relevant, not transferable as an estimate. Their variable p runs over a polynomial-length prime range and their remainder is an arithmetic-progression prime-count error controlled by EH. Our 3^c+5^d sample has only O(log^2 n) points. AUX-01 supplies the identity here, but no counterpart of their pair-count saving or prime-distribution estimate. The quoted theorem is conditional and concerns a different representation problem.

## L3. Friedlander–Iwaniec: what the large sieve actually measures

John B. Friedlander and Henryk Iwaniec, *Remarks on the Bombieri–Davenport Large Sieve Inequalities*, arXiv:2409.19634. Source: `https://arxiv.org/pdf/2409.19634`, equation (1.1); also inspected Proposition 2.2, PDF p. 4.

For arbitrary complex a_j supported on an integer interval of length N>1,
\[
 \sum_{q\le Q}{q\over\phi(q)}\sum_{\chi\bmod q}^{*}
 |\sum_j a_j\chi(j)|^2\le(N+Q^2)\sum_j|a_j|^2.
\]
The star means primitive characters; no special distribution assumption on a_j is needed. This is uniform in the interval position and Q.

**Adaptation:** sparse support reduces the rightmost energy, not the ambient interval length N. Marking bulk residuals therefore does not turn the N term into M=O(log^2 n). The inspected primitive-two-square variant is also an upper bound for an already norm-supported coefficient sequence; it cannot supply its nonempty support. Neither statement directly controls the signed modulus sum in (D3). A new, specifically sparse and signed estimate could differ from these bounds; it is not ruled out.

## L4. Malavika–Ramaré (2026): exponential sums on a sifted norm sequence

E. Malavika and Olivier Ramaré, *Bounding the exponential sum on squares of some sifted sequences*, arXiv:2604.09448v1, 10 April 2026. Source: `https://arxiv.org/pdf/2604.09448`, Theorem 1.1, PDF p. 2.

Let b(j) indicate odd integers representable by two coprime squares. If (a,q)=1 and |alpha-a/q|<q^(-2), then for every epsilon>0,
\[
 {\sum_{j\le N}b(j)e(j^2\alpha)\over N/\sqrt{\log N}}
 \ll_\epsilon N^\epsilon\{q^{-1/4}+N^{-1/2}q^{1/4}+N^{-1/8}\}.
\]
It concerns a full integer range j<=N and quadratic phase j^2 alpha. The displayed bound is uniform subject to the approximation hypothesis; it is nontrivial only where the right side is small.

**Adaptation:** this is not a bound for b(n-3^c-5^d), nor for the linear-phase generating series of that support, nor for a signed h-average of A_h(n). It does show why a recent sifted-sequence result should be checked rather than omitted; its precise phase and support do not supply ML-D2.

## L5. Radomskii: latest version remains a counted-target result

Artyom Radomskii, *Variants of Romanoff's theorem*, arXiv:2504.09954v7, revised 27 August 2026. Sources: `https://arxiv.org/abs/2504.09954` and `https://arxiv.org/html/2504.09954v7`, Theorem 1.1. The supplied I2 literature cited v6; this check found v7. No statement in the old package was silently overwritten.

With A increasing, B a finite-multiplicity sequence, hypotheses include A(x)~order x/eta(x), dyadic regularity, A(x,r)<<[r/phi(r)]x/eta(x)^2, and a weighted collision bound for B over primes <=(log x)^alpha, fixed 0<alpha<1. The conclusion is
\[
 \#\{n\le x:r(n)\ge c_1B(x)/\eta(x)\}
 \ge c_2x\,{B(x)\over B(x)+\rho_B(x)\eta(x)}.
\]
Constants depend on the stated hypothesis constants and alpha.

**Adaptation:** the theorem controls how many targets are good, not each chosen target. Neither its prime-modulus collision range nor its quantifiers gives a bound on D_n(2/log n)/D_n(1/log n) for every n. No new density conclusion is claimed as progress in I4.

## L6. Fixed-progression Mertens input for PW-02

Zhen Chen and Junrong Luo, *Multiple Mertens theorems for arithmetic progressions*, arXiv:2512.07336v1. Source: `https://arxiv.org/pdf/2512.07336`, Theorem 1.3, PDF p. 4.

Only its classical fixed-modulus specialization is used:
\[
 \sum_{p\le x,p\equiv3(4)}p^{-1}={1\over2}\log\log x+A_{3,4}+O(1/\log x).
\]
Taking the difference at x=n^b and n^a yields the constant (1/2)log(b/a) in PW-02. The difference between 1/p and 1/(p+1) on that band is o(1). This is an actually applicable external input, not a substitute for any orbit distribution. The elementary finite inequality (4) does not need it.

## L7. Platt–Trudgian: adversarial caution about generic power-sum arguments

David J. Platt and Timothy S. Trudgian, *On the sum of two squares and at most two powers of 2*, arXiv:1610.01672. Source: `https://arxiv.org/pdf/1610.01672`, Theorem 1, PDF p. 1.

They prove that 535903 is the least integer greater than one not expressible as two squares plus at most two nonnegative powers of 2, and give infinitely many exceptions of the form 2^a times 1151121374334. This theorem is not about bases 3 and 5.

**Adaptation:** a single-target base-(2,2) benchmark checks that the new transform really detects all-failing exponential samples rather than mechanically returning a favorable ratio. It does not assert the I2 uniform 2/3 survival density for bases (2,2), and is not a counterexample to A303656. The literal bases must do essential work in any future proof of ML-D2.

## Acquisition result

The usable extraction is the large-prime-pair comparison template from L2, the fixed-modulus prime harmonic asymptotic in L6, and explicit range obstructions from L1/L3/L4. No cited result yields the missing signed fixed-target estimate. The gap is not a missing citation to a generic “half-dimensional sieve”; it is the absence here of a uniform inequality for (D3) on the actual two-orbit sample.
