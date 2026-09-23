# A303656 — Thread 4: direct minimal-counterexample lifting audit

**Date:** 2026-09-21. **Repository access:** read-only. No remote changes.

Pinned authority: `Samsen879/a303656`, main
`8f17e88e517720f61f3c21d58d91c04cd6fa11b5`, tree
`811a274b1f671412305c8565fcd79e9d41c0189b`.

## Executive disposition

**Overall: HEDGE.** There is no proof of universal representability and no
counterexample to A303656 in this report. There is no established contraction
of the original exceptional set.

The principal mathematical deliverable is a complete classification of a
natural, but precisely restricted, universal lifting problem. With
`S_2={x^2+y^2:x,y in Z}` and `T_3=S_2+{3^j:j>=0}`, for `lambda in {1,5}` and
`K>0`,

> `lambda*S_2+K` is contained in `T_3` if and only if `K` is a power of 3.
> If `K` is not a power of 3, infinitely many actual norms `S` fail membership.

Consequently, for a given source representation
`m=x^2+y^2+3^c+5^d`, a universal lift to `5m+r` retaining the natural target
5-exponent `d+1` exists for all source square pairs exactly when `(r,c)=(4,0)`.
For every other `r in {0,...,4}` and every corresponding fixed `c`, there are
infinitely many failing source representations, even if the target square
coordinates and target 3-exponent are completely unrestricted.

This is a **KILL** result for the universal arbitrary-source, natural
5-exponent-preserving lifting claim. It is not a KILL result for changing both
exponents, selecting another source representation, or using the full
minimal-counterexample hypothesis.

Other deliverables: exact consequences of minimality; classification of all
integer Gaussian translations by an affine-line equation; a density-zero
no-go for bounded translations from finitely many neighbors; a coherent
infinite eight-neighbor adversarial model; a fixed-affine two-source fusion
no-go; and one precise, unproved representation-selection lemma for the
residue `5m+3`.

These are self-contained derivations in this report, not claims of established
repository authority, historical priority, formal proof-assistant checking,
or independent human peer review.

## Authority and source boundary

The live `STATUS.md` says PAUSED, no active promoted route, no general proof,
and no certified counterexample. Its warning that existing negative theorems
are confined to their stated formal classes is preserved here.

Read: `analysis/gaussian_hurwitz_descent_phase_m/README.md` and `REPORT.md`.
The latter explicitly limits existing M-D3 to finite four-dimensional additive
moves and bounded positive target exponents from specified initial states.
It does not already establish the unbounded-target-exponent norm obstruction
proved below, nor a no-go for all genuine minimal-counterexample methods.
No old certificate formalism is used in the proofs here.

For conventional background, the sum-of-two-squares criterion is stated in
Kimmel–Kuperberg, *Positive density for consecutive runs of sums of two squares*,
arXiv:2406.04174v1, Introduction. The crucial negative direction also follows
immediately from `-1` being a quadratic nonresidue at a prime `p=3 mod 4`.
The external source does not supply the new lifting classifications below.

Source locations:

- `https://github.com/Samsen879/a303656/blob/8f17e88e517720f61f3c21d58d91c04cd6fa11b5/STATUS.md`
- `https://github.com/Samsen879/a303656/blob/8f17e88e517720f61f3c21d58d91c04cd6fa11b5/analysis/gaussian_hurwitz_descent_phase_m/REPORT.md`
- `https://arxiv.org/html/2406.04174v1`
- `https://oeis.org/A303656`

## A. Exact consequences of minimality

Write `R(n)` for the set of normalized representations `(x,y,c,d)` with
`0<=x<=y`, and write `R_c(n)` for those with the specified 3-exponent `c`.
Suppose `N>1` is the least counterexample. The precise hypothesis is

`R(m) != empty` for every `2<=m<N`, and `R(N)=empty`.

The lower bound 2 is essential: neither 0 nor 1 has a representation.

For every `h>0` with `N-h>=2` and every `(x,y,c,d) in R(N-h)`,

`x^2+y^2+h` is not a sum of two squares.

Otherwise keeping both exponent terms gives a representation of `N`.
Likewise, for every feasible target exponent pair `(C,D)`,

`x^2+y^2+h+3^c+5^d-3^C-5^D`

must either be negative or fail the sum-of-two-squares criterion. This
universal failure statement is exact, but is only a rewriting of target
nonrepresentability until some source feature is forced independently.

### Immediate forbidden features in *every* neighbor representation

| h | Forbidden coordinate feature | Forbidden source exponent feature |
|---|---|---|
| 1 | a zero square coordinate | — |
| 2 | equal square coordinates | `c=0` |
| 3 | a square coordinate equal to 1 | — |
| 4 | a zero coordinate, or coordinate difference of absolute value 1 | `d=0` |
| 5 | a coordinate equal to 2 | — |
| 8 | a coordinate equal to 1, or coordinate difference of absolute value 3 | `c=0` |
| 9 | a coordinate equal to 4 | — |
| 24 | a coordinate equal to 5, or coordinate difference of absolute value 11 | `d=0` or `c=1` |

Signed intermediate coordinates are harmless because absolute values preserve
squares. The diagonal feature uses

`(x+1)^2+(y-1)^2-(x^2+y^2)=2(x-y)+2`.

The exponent features use `3-1=2`, `5-1=4`, `9-1=8`, `25-1=24`, and
`27-3=24`.

More generally, whenever the source integer is at least 2,

- every representation of `N-3^c(3^k-1)` avoids the source 3-exponent `c`;
- every representation of `N-5^d(5^l-1)` avoids the source 5-exponent `d`;

for positive `k,l`. These are genuine restricted-profile omissions. They do
not make the source integer a counterexample to the original equation.

For odd represented `m`, reduction modulo 4 also forces: `m=1 mod 4` has odd
`c`, and `m=3 mod 4` has even `c`. This fixes parity, not an exact exponent.

## B. Strongest exact lifting theorem

### B1. Norm plus one power-of-three classification

Let `lambda in {1,5}` and let `K>0` be an integer. Then

`[for every S in S_2, lambda*S+K lies in T_3] <=> [K=3^j for some j>=0]`.

If `K` is not a power of 3, there are infinitely many counterexamples `S`.
In fact the counterexamples can be supplied by a full-rank congruence class
of source coordinates, and hence by an explicit one-parameter subfamily.

#### Elementary local norm lemma

For an odd prime `p` and a unit `u modulo p^2`, there are integers `a,b` with
`a^2+b^2=u modulo p^2`.

Modulo `p`, the set of squares has `(p+1)/2` elements. The two sets of residues
`squares` and `u-squares` therefore intersect. Since `u` is a unit, the chosen
pair does not have both coordinates zero modulo `p`. Adjust a nonzero
coordinate by `p*t`; its square changes by a freely selectable multiple of
`p` modulo `p^2`, completing the lift. The same reasoning in particular shows
that every unit modulo 9 is a norm.

#### Sufficiency

If `K=3^j`, use `S in S_2 => lambda*S in S_2`. For `lambda=5`,

`5(x^2+y^2)=(x-2y)^2+(2x+y)^2`.

#### Necessity: create an odd 3-adic valuation

Assume `K` is not a power of 3. Put `k=v_3(K)`. We impose local conditions on
actual source coordinates such that `T=lambda*(x^2+y^2)+K` has a fixed odd
3-adic valuation `t`.

If `k` is odd, take `t=k` and require both `x,y` to be divisible by
`3^((k+1)/2)`. Then the norm term is divisible by `3^(k+1)` and `v_3(T)=k`.

If `k=2e` is even, put `x=3^e*u`, `y=3^e*v` and impose

`lambda*(u^2+v^2)+K/3^k = 3 (mod 9)`.

The required norm residue modulo 9 is a unit, so the local norm lemma supplies
`u,v`. Then `v_3(T)=k+1`; put `t=k+1`, which is odd.

Thus, for **every** exponent `C>t`, a positive residual `T-3^C` has odd
3-adic valuation `t` and is not a sum of two squares. A negative residual is
already inadmissible. This disposes of the entire unbounded exponent tail.

#### Necessity: dispose of the finitely many remaining exponents

For each `0<=C<=t`, choose a distinct prime `p_C=3 mod 4`, different from 3,
satisfying

`p_C does not divide lambda*(K-3^C)`.

This is possible because `K-3^C` is nonzero and there are infinitely many
primes 3 modulo 4. Impose

`lambda*(x^2+y^2)+K-3^C = p_C (mod p_C^2)`.

The required source norm is a unit modulo `p_C`, so the local norm lemma
again supplies source coordinates modulo `p_C^2`. The Chinese remainder
theorem combines these requirements with the previous 3-adic source-coordinate
conditions. Each remaining residual now has `v_(p_C)=1`.

Hence no exponent `C>=0` succeeds. Varying one source coordinate by a common
modulus produces infinitely many actual norms, proving necessity.

**Proof boundary:** this obstructs an auxiliary ternary representation
`T=X^2+Y^2+3^C`; it is not a construction of an A303656 counterexample.
The source `m` and the intended target `N` may both have other full
representations.

### B2. Complete natural five-fold arbitrary-source classification

Fix `r in {0,1,2,3,4}`, `c,d>=0`. For

`m=x^2+y^2+3^c+5^d`,

seek a target representation of `5m+r` with its 5-exponent equal to `d+1`.
Allow the target 3-exponent and both target square coordinates to be arbitrary.
This is exactly the auxiliary problem

`5(x^2+y^2)+5*3^c+r = X^2+Y^2+3^C`.

By B1, success for every source square pair is equivalent to

`5*3^c+r = 3^C`.

The sole solution with `0<=r<=4` is `(r,c,C)=(4,0,2)`.
For `c=0`, the range is 5 through 9. For `c>=1`, `C>=1`, so reduction modulo 3
forces `r=0` or `r=3`. The first is impossible. In the second,
`5*3^(c-1)+1=3^(C-1)` is impossible at `c=1`, and for `c>=2` its left side is
1 modulo 3 and greater than 1, again impossible.

The positive identity is

`m=x^2+y^2+1+5^d`

`=> 5m+4=(x-2y)^2+(2x+y)^2+3^2+5^(d+1)`.

Every other fixed `(r,c)` has infinitely many failures. This includes
arbitrarily large `c`; it cannot be repaired by excluding finitely many
small source exponents. It does not exclude selection among different source
representations, different predecessor integers, or a target 5-exponent other
than `d+1`.

### B3. Neighbor variant with an unrestricted new 3-exponent

For a fixed `h>0` and source `c`, keeping `5^d` fixed while allowing arbitrary
new square coordinates and a new 3-exponent succeeds for every source norm
if and only if `3^c+h` is a power of 3. This is B1 with `lambda=1`.
For the listed shifts, the universal single-3-term possibilities are exactly
`h=2,c=0`; `h=8,c=0`; and `h=24,c=1`.

This is not a classification of lifts that also change the 5-exponent.

## C. Additional exact obstructions

### C1. No full congruence class can guarantee one of finitely many nonzero norm shifts

Fix a finite nonempty set `H` of nonzero integers, a modulus `M>=1`, and any
source-coordinate class `(x,y)=(a,b) mod M`. There are infinitely many points
in this class for which

`x^2+y^2+h` is not in `S_2` for every `h in H`.

For each `h`, choose a different prime `p_h=3 mod 4` not dividing `h*M` and
impose `x^2+y^2=p_h-h mod p_h^2`. The source norm is a unit locally, so solve
for source coordinates and apply CRT, retaining `(a,b) mod M`. Every shifted
norm has valuation exactly 1 at its assigned prime. Make the coordinates
large enough that all shifted norms are positive.

This rules out a guarantee based only on a fixed finite amount of congruence
information about arbitrary source coordinates. It does not rule out exact
lower-dimensional conditions such as a coordinate being zero or a prescribed
coordinate difference.

### C2. Classification and density bound for bounded Gaussian translations

For a translation `(x,y)->(x+u,y+v)`, the exact necessary and sufficient equation
for a fixed norm displacement `h` is

`2*u*x+2*v*y = h-u^2-v^2`.

For `(u,v)!=(0,0)`, let `g=gcd(u,v)>0`. Integer solutions exist precisely when
`h-u^2-v^2` is divisible by `2g`. Given one solution, all are

`x=x0+(v/g)t`, `y=y0-(u/g)t`.

This is a complete affine-line classification for integer translations;
it is not merely a collection of small examples.

Fix finite positive neighbor shifts `H` and a coordinate-move bound `B`.
The number of targets `n<=X` reachable from one of `n-h`, keeping both
exponents fixed, by some nonzero translation with `|u|,|v|<=B`, is

`O_(H,B)(sqrt(X)*(log X)^2)`.

For fixed `h,u,v,c,d`, the line has `O_(H,B)(sqrt(X))` source points in the
allowed square-coordinate box. There are `O((log X)^2)` exponent pairs.
The union bound proves the estimate. It remains valid if every source
representation and every integral norm-preserving reorientation is made
available first, since all such integral pairs are already counted.

Thus bounded coordinate translations with retained exponents cover a
zero-density set of targets. This is stronger than exhibiting a bad arbitrary
source witness. It is **not** a density bound for arbitrary refactorization of
the new norm, changing exponent terms, rational intermediate lattices with
unbounded denominators, or unbounded coordinate displacement.

### C3. A coherent infinite eight-neighbor adversarial model

For `H=(1,2,3,4,5,8,9,24)`, put `N(t)=t^2+36` and use the following actual
neighbor representations:

| h | y | c | d | `y^2+3^c+5^d=36-h` | target norm at t=7 |
|---|---:|---:|---:|---:|---:|
| 1 | 3 | 0 | 2 | 35 | 59 |
| 2 | 0 | 2 | 2 | 34 | 51 |
| 3 | 5 | 1 | 1 | 33 | 77 |
| 4 | 2 | 1 | 2 | 32 | 57 |
| 5 | 5 | 0 | 1 | 31 | 79 |
| 8 | 0 | 1 | 2 | 28 | 57 |
| 9 | 5 | 0 | 0 | 27 | 83 |
| 24 | 2 | 1 | 1 | 12 | 77 |

The source pair is `(t,y)` in every row. At `t=7`, `N=85`. The possible target
norms obtained by retaining a supplied exponent pair are `59,51,77,57,79,83`;
each fails by an odd valuation at an inert prime.

Set `L=9*49*59^2*79^2*83^2` and take `t=7+L*j`, `j>=0`.
Use primes `59,3,7,3,79,3,83,7` for the rows in order. Each valuation stays
exactly 1, so the failure persists along an infinite common progression.
All eight neighbor equations and all their difference equations hold
simultaneously. These are not independently fabricated or inconsistent
source witnesses.

Meanwhile every target is genuinely represented:

`N(t)=t^2+2^2+3^3+5^1`.

**Exact limitation proved:** finitely many supplied arbitrary neighbor
representations, even simultaneously consistent ones, need not contain an
exponent pair usable for the target. The model does not make the target a
counterexample, and does not block choosing other neighbor representations,
exponent exchange, or a nonlinear fusion rule. For example at `N=85`, the
cross-pair `(c,d)=(1,0)` already gives target norm 81.

### C4. Why multiplying a norm by 3 is strictly different

For every positive `S in S_2`, `v_3(S)` is even, so `3S` is **never** in `S_2`.
The only zero exception is `S=0`. Thus “usually not” can be sharpened to
“never for positive norms.”

Even retaining the naturally advanced 3-exponent and compensating with an
arbitrary new 5-exponent fails for whole infinite source families:

| r | source family m | residual after retaining `3^(c+1)` in `3m+r` |
|---|---|---:|
| 0 | `7^2+7^2+3^c+5` | 309 |
| 1 | `0^2+0^2+3^c+1` | 4 |
| 2 | `0^2+1^2+3^c+1` | 8 |

For 309, the admissible target powers of 5 are 1, 5, 25, 125. Their residuals
are 308, 304, 284, 184, obstructed respectively by primes 7, 19, 71, 23 to odd
valuation. For 4 the sole residual is 3; for 8 the residuals are 7 and 3.
Every source family is infinite as `c` grows. Again this is a no-go only for
the specified retained 3-exponent.

### C5. Fixed-affine fusion cannot universally combine two arbitrary representations

Here the scope is explicitly **real-algebraic universal affine identities**.
Fix constants `A1,A2,B`. Suppose a fixed affine map

`Z=L1*z1+L2*z2+b`, with `z1,z2,Z in R^2`,

satisfies `|Z|^2+B=N` for every sufficiently large real `N` and every pair of
points satisfying `|z1|^2=N-A1`, `|z2|^2=N-A2`.
Then one `Li` is zero, the other is orthogonal, `b=0`, and `B` equals the
corresponding source constant `Ai`.

Proof: vary the two angles independently. Mixed angular coefficients give
`L1^T L2=0`; second harmonics give `Li^T Li=ai*I`, `ai>=0`; first harmonics give
`Li^T b=0`. A nonzero block is invertible, so the mixed relation kills the
other block and the first harmonic kills `b`. Comparison of coefficients of
`N` gives `ai=1`, and comparison of constants gives `B=Ai`.

Thus direct elimination of the two norm equations does not supply a new
universal fixed-affine two-square construction. This proof does not claim
that all integer-specific formulas, branch conditions, source-dependent
coefficients, Gaussian gcd constructions, or nonlinear two-source methods
are impossible.

## D. One precise next lemma, not yet proved

Define the actual 5-exponent support

`D(m)={d>=0 : m-5^d lies in T_3}`.

Equivalently this is the set of 5-exponents occurring in representations of
`m` under the original equation.

The narrowly specified candidate is:

> **L5,3 — representation-selection transfer.** For every representable
> `m>=2`, there is a `d in D(m)` such that `d+1 in D(5m+3)`.

In symbols: `D(m)!=empty => (D(m)+1) intersects D(5m+3)`.

This is not the false assertion that every source representation lifts. It
allows selection among *all* representations of `m`. It also does not assume
all integers are representable: its hypothesis is only that this particular
source `m` is representable.

If proved, it gives an actual descent for the residue class `N=3 mod 5`:
nonrepresentability of `5m+3` implies nonrepresentability of `m`. Apart from
finitely many trivial base cases, a least counterexample could not lie in that
residue class. It would not settle the other four residue classes.

The bounded laboratory gives no failed source `m<=5000` for this exact `r=3`
selection statement. The same statement with `r=0,1,2,4` has explicit failures,
so it is wrong to generalize the candidate to all residues.

This is a theorem-first research gate, not permission to infer truth from the
finite test or to launch a large original-counterexample scan. Useful next
work must either prove L5,3, build an actual support-disjoint counterexample,
or find a structural obstruction to its quantifiers. An average overlap
estimate or a count of individually liftable representations is insufficient.

## E. What contraction is actually available?

### Exact, but exponent-locked, five-fold equivalence

Fix `c>=0`, assume `N=3^c mod 5`, and let

`m=(N+4*3^c)/5`.

Then

`R_c(m)!=empty`

is equivalent to the existence of a target representation of `N` with the
same `c` and with `d>=1`.

The forward direction multiplies the source norm by 5 and the source
5-power by 5. The reverse direction divides the target norm by 5: an integer
sum of two squares divisible by 5 remains a sum of two squares after that
division, by Gaussian factorization or the prime-valuation criterion.

For nonzero residues, the following small exponent choices give small
predecessors, writing `N=5q+r`:

| r | c | m |
|---|---:|---|
| 1 | 0 | `q+1` |
| 2 | 3 | `q+22` |
| 3 | 1 | `q+3` |
| 4 | 2 | `q+8` |

There is no such `c` for `r=0`. For large enough `N`, these are genuinely
smaller integers. However minimality supplies `R(m)!=empty`, not
`R_c(m)!=empty`. A failure of the exponent-locked profile is not a smaller
counterexample to the original equation.

Concrete source-selection failures already occur at `(N,m,c)=(21,5,0)`,
`(47,31,3)`, `(23,7,1)`, and `(29,13,2)` respectively.

### Disposition

**Established original-counterexample contraction:** none.

**Established restricted-profile numerical shrinkage:** the exact equivalence
above, with predecessors bounded by `N/5+22` for nonzero residues.

**Conditional original-counterexample contraction:** L5,3 would supply
`N -> (N-3)/5` in the residue class 3 modulo 5.

These three statements must not be conflated.

## Computational laboratory and reproducibility

Run `python3 verify_thread4.py --output laboratory.json`.

The source interval is `2<=m<=5000`; target norm data extend only to 25004.
Every normalized source representation is enumerated: **76,886 tuples**.
An alternative loop ordering checks the entire source count vector.
The test is on lifting supports, not an argument from absence of small
counterexamples to the original conjecture.

For the natural 5-exponent shift, the numbers of source integers whose
**every** representation fails to supply a usable target 5-exponent are:

| target | number of failing m | first failing m |
|---|---:|---:|
| `5m` | 2 | 4 |
| `5m+1` | 15 | 20 |
| `5m+2` | 5 | 16 |
| `5m+3` | 0 in this interval | — |
| `5m+4` | 1 | 5 |

The complete failure lists and overlap-size histogram are in the JSON receipt.
Some failures are well beyond the very small boundary: e.g. `m=4556` fails
for `r=1`, yielding target 22781. This rules out interpreting all observed
failures as only the first few source integers.

The certificate generator also constructs and verifies 90 exact congruence
receipts: 44 nonuniversal cases with `lambda=5`, `0<=c<=8`, `0<=r<=4`, and 46
non-power-of-three constants with `lambda=1`, `1<=K<=50`. It checks the odd
3-adic valuation and every assigned inert-prime-square congruence. The infinite
quantifier is justified by the written proof, not by the number of receipts.

The same program checks the coherent eight-neighbor infinite family and the
three compensation counterfamilies. All bounded checks pass. This is a
separate loop-order audit and exact arithmetic replay by the same assistant,
not an independent researcher or a formal proof-assistant audit.

## F. Final verdict

- **KILL:** arbitrary-source natural `5^d -> 5^(d+1)` lifting as a universal
  five-residue mechanism, apart from the exactly classified positive state.
- **KILL:** a finite list of neighboring integers plus bounded integral
  coordinate translations retaining both exponent terms as an unconditional
  all-target lifting mechanism. This does not rule out additional hypotheses
  forcing a least counterexample into a special sparse set.
- **HEDGE:** exploiting the full minimality hypothesis through representation
  selection, source-dependent arithmetic, changing both exponents, or nonlinear
  fusion. None of the no-go results proves these general approaches impossible.
- **Next precise gate:** L5,3, with its exact representation-selection
  quantifiers and residue-specific contraction. It is unproved.

The strongest advance is a sharper boundary on what the minimal-counterexample
approach must add. Existence of arbitrary predecessor representations cannot
be silently upgraded to the exponent or coordinate control needed by a lift.
