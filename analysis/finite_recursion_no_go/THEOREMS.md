# Exact statement sheets

These sheets preserve the packet's quantifier order.  The complete original
wording and proofs are in `source/producer_packet/research_report_zh.md`.

## M

```text
NAME: M — mixed-dilation linear independence
EXACT STATEMENT: For every finite list of distinct positive integers
K_1,...,K_s, the functions 1,F(x^K_1),...,F(x^K_s) are linearly independent
over C(x).  Equivalently, p_0(x)+sum_j p_j(x)F(x^K_j)=0 with complex
polynomials p_j forces every p_j=0.
DOMAIN: analytic functions on |x|<1, equivalently their convergent power
series; coefficient relations lie in C(x).
QUANTIFIERS: every finite list of pairwise distinct fixed positive integers.
FIXED PARAMETERS: the selected K_j and the counting series
F=theta(x)^2 L_3(x)L_5(x).
VARIABLE PARAMETERS: x.
DEPENDENCIES: theta radial asymptotic, Gamma has no zeros, absolute Fourier
summability, log(3)/log(5) irrationality.
EXCLUDED DEGENERACIES: repeated K_j are combined first; only finite linear
combinations; exact counting equality, not support equality.
CONCLUSION: no nontrivial scalar rational mixed-dilation equation for F.
CLAIMED COROLLARIES: no finite-order scalar Mahler equation for any fixed
integer base k>=2; finite H_(u,v) subfamilies are C(x)-linearly independent.
```

## M+

```text
NAME: M+ — finite rational-linear mixed-dilation system no-go
EXACT STATEMENT: No finite-dimensional function vector Y having F as a
coordinate satisfies Y(x)=b(x)+sum_{K in Kset} A_K(x)Y(x^K), where Kset is a
fixed finite set of integers K>=2 and every entry of b and A_K lies in C(x).
Finite initial coefficient exceptions merely add polynomial forcing.
DOMAIN: finite vectors of analytic/formal counting series with rational
coefficient functions.
QUANTIFIERS: no such finite Y, finite Kset, matrices, or forcing exist.
FIXED PARAMETERS: vector dimension, Kset, matrices and forcing.
VARIABLE PARAMETERS: x and coefficient index.
DEPENDENCIES: M plus two-sided Ore localization after adjoining finitely
supported rational powers x^(1/N).
EXCLUDED DEGENERACIES: nonlinear or Boolean systems; non-meromorphic forcing;
singular, information-free K=1 implicit equations not reducible to the stated
normal form.
CONCLUSION: the stated finite linear closure cannot contain F.
CLAIMED COROLLARIES: B13 cannot be completed to a finite system of this exact
linear rational mixed-dilation form.
```

## Q

```text
NAME: Q — zero-density one-step incoming images
EXACT STATEMENT: Take finitely many source states
m=a^2+b^2+A_s3^c+B_s5^d+C_s with positive INTEGER A_s,B_s and integer C_s.
Each final edge has n=K_e m+R_e with fixed integer K_e>=2,R_e, and outputs the
original state using, for every fixed (c,d,u,v), at most a uniform J rational
charts in (a,b), each of uniformly bounded degree D.  Coefficients may depend
on the exponent tuple and guards are arbitrary.  Then the set L_R(X) of
possible one-step outputs satisfies
#(L_R(X) intersect 15N)=O_R,D(X/sqrt(log X)+sqrt(X)(log X)^4)=o(X).
DOMAIN: successful integral outputs of those one-source rational charts.
QUANTIFIERS: every fixed finite catalogue with uniform J,D.
FIXED PARAMETERS: states, edges, K,R,J,D.
VARIABLE PARAMETERS: representations and four nonnegative exponents.
DEPENDENCIES: norm-defect rigidity; ESS finite-rank unit equations; Landau's
two-squares counting bound.
EXCLUDED DEGENERACIES: fractional source weights, K=1, unbounded chart count or
degree, algebraic-root/floor lookup, coordinate-dependent carries, multi-source
construction.
CONCLUSION: almost every multiple of 15 has no incoming edge in the class.
CLAIMED COROLLARIES: no induction using only these edges and finite bases
covers all integers.
```

## Q*

```text
NAME: Q* — zero density for the complete reachable set
EXACT STATEMENT: There are finitely many states
n=q_i(z)+A_i3^c+B_i5^d+C_i, z in Z^2, c,d>=0, where q_i is a centered
positive-definite binary rational quadratic form (rational cosets allowed),
A_i,B_i are positive rationals and C_i is rational.  There are finitely many
rules n'=K_e n+R_e with fixed integer K_e>=2 and fixed R_e.  For each fixed
input/output exponent tuple, the output coordinates are supplied by at most a
uniform J rational charts of uniformly bounded degree D; coefficients and
guards may depend arbitrarily on the tuple.  Starting from finitely many
(state,index) bases and propagating the actual output witness to the next edge,
the original-state reachable set obeys
#(Reach intersect [1,X])=O_R(sqrt(X)(1+log X)^6+(1+log X)^(r+2))=o(X),
where r is the number of distinct prime divisors of the fixed K_e.
DOMAIN: all finite witness-continuous paths in this catalogue.
QUANTIFIERS: every fixed finite catalogue and finite base set.
FIXED PARAMETERS: states, forms, weights, rules, K,R,J,D and bases.
VARIABLE PARAMETERS: path, witnesses, guards and exponent choices.
DEPENDENCIES: generalized norm-defect rigidity, grid-zero bound, final-defect
decomposition, finite rational-lattice denominators, convergent smooth-number
sum sum_S S^(-1/2).
EXCLUDED DEGENERACIES: witness reselection oracle at an index, unbounded chart
number/degree, coordinate-dependent index map, algebraic-root choice,
multi-witness transition, infinitely many rules, nonbinary/nonquadratic states.
CONCLUSION: Reach has density zero.
CLAIMED COROLLARIES: such a system cannot prove coverage of all integers or of
any positive-density subset by finite-seed witness generation.
```

## Q-dagger

```text
NAME: Q-dagger — monotone exponent-dependent-carry extension
EXACT STATEMENT: Retain Q*'s states, bounded charts, finite catalogue, finite
bases and witness continuity, but permit
n'=K_e n+R_e(c,d,u,v), K_e an integer >=1, where the rational carry is arbitrary
after the four exponents are fixed.  Require every successful step to satisfy
n'>n.  Then
#(Reach intersect [1,X])=O_R(sqrt(X)(1+log X)^(r+6)
 +(1+log X)^(r+2))=o(X).
DOMAIN: all finite strictly index-increasing witness paths.
QUANTIFIERS: every fixed finite catalogue satisfying the stated uniform bounds.
FIXED PARAMETERS: finite state/rule catalogue, fixed multipliers, J,D,bases.
VARIABLE PARAMETERS: exponent-dependent carry, guards, witnesses and paths.
DEPENDENCIES: Q* rigidity and sparse-repair bound; monotonicity bounds the last
repair index by X.
EXCLUDED DEGENERACIES: nonmonotone index paths, coordinate-dependent carry,
unbounded distinct multipliers/charts/degrees, witness oracle, multi-source
construction.
CONCLUSION: Reach has density zero with the displayed weaker logarithmic power.
CLAIMED COROLLARIES: exponent dependence alone does not evade the no-go.
```
