# One quantitative missing lemma — expressly UNPROVED

## ML-K2: logarithmically vanishing completion margin

There exists N0 such that for every integer n>=N0,
\[
\boxed{\displaystyle
\sum_{\substack{19\le p<\sqrt n\\p\equiv3\ (4)}}N_p^G(n)
\le G(n)-\frac{G(n)}{\log n}.}
                                                               \tag{ML-K2}
\]
This is a direct failure-count estimate, not a transform or a finite-local
surrogate. It is stated only to specify a single sufficient unresolved target.
It is **not** a theorem, an assumption used to certify progress, or an estimate
that the inspected literature nearly provides.

Why this target: K2-N1 rules out a fixed positive fraction, and even log-loss
powers below 1/2. The deliberately more forgiving exponent 1 is not excluded
by that counting argument. No optimality or independent evidence for its precise
coefficient or exponent is claimed. Positivity alone could hold even if ML-K2
were false.

## Complete logical implication

Accept Phase K. Then for sufficiently large n,
\[
G(n)\ge a_0(\log n)^2,\qquad a_0=1869/(25600\log3\log5)>0.
\]
If ML-K2 holds, the exact partition D3 gives
\[
R_G(n)=R(n)=G(n)-\sum_pN_p^G(n)
\ge\frac{G(n)}{\log n}\ge a_0\log n>0.
\]
Since R is an integer, a norm residual exists, hence there are nonnegative a,b,c,d
with `n=a^2+b^2+3^c+5^d`. This proves all sufficiently large n, conditional on the
unproved ML-K2. To finish the universal statement requires an effective threshold
and certified treatment below it. Neither threshold nor finite closure is
provided by this conditional implication.

By the inherited quarter identity, ML-K2 can equivalently be displayed as
\[
 V_{n^{1/4}}(n)\le T(n^{1/4};n)-G(n)/\log n.
\]
This is the **same single inequality**, not a second proposed lemma.

## Distance from verified methods: LARGE

The missing estimate must control the collective coverage at witness scale on
a fixed literal grid with only O(log^2 n) points. The inspected large-prime
completion theorem works on a long prime-convolution sequence with its own
distribution and Gaussian-lattice input. Those inputs have not been established
here. Elementary per-prime bounds do not control the union. Smooth absolute-error
models encounter the proved integer-distance barrier, even after logarithmic
least-prime conditioning.

There is no quantified bound on this literal sequence here that tends to the
right-hand side of ML-K2. This is not a declaration that no future arithmetic
method can work; it is a comparison with the explicit audited methods and inputs.

## Final gate

Status: **D, scoped method-obstruction audit; no A/B/C completion claim.**
Recommendation: **PAUSE DIRECT ORIGINAL-n PROGRAM.**
Next task: **NONE**. No automatic next phase, new scan, or Codex handoff.
