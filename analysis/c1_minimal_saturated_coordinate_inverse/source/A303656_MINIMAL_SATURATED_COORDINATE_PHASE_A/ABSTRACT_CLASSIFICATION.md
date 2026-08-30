# Abstract and exact-cover classification

## 1. Atomic rational saturation theorem

Fix an odd prime `l`.  At denominator depth `e>=1`, let

```text
epsilon_e in {0,1},
n_e in Z_{>=0},
c_e=(l-1)epsilon_e+n_e.
```

Only finitely many terms are nonzero.  The dynamic-depth distinctness `epsilon_e in {0,1}` is forced by the genuine single dynamic row.  Define

```text
T=sum_e c_e/l^e.
```

### Theorem 1 — minimality forces equality

Among finite nonempty genuine mass multisets with `T>=1`, atom-minimality is equivalent to

```text
T=1.
```

Equivalently, if `B` is the largest used depth and

```text
h_0=1,
h_e=l h_(e-1)-c_e,
```

then

```text
h_e>=0 for 1<=e<B,
h_B=0.
```

#### Proof

If a rigid atom occurs at the largest depth `B`, the total excess `T-1` is an integral multiple of `l^-B`.  Atom-minimality makes it strictly smaller than the smallest atom `l^-B`; hence the excess is zero.

Otherwise the only largest-depth atom is one dynamic atom `(l-1)l^-B`.  Every coarser contribution has numerator divisible by `l` after multiplication by `l^B`, while the largest dynamic atom contributes `l-1 mod l`.  Minimality would require

```text
0<=l^B(T-1)<=l-2,
```

but this integer is congruent to `l-1 mod l`, impossible.  Thus the second case cannot occur.

Conversely, every positive atom in an exact equality is essential.  The recurrence is simply

```text
h_e=l^e(1-sum_(k<=e)c_k/l^k).
```

Nonnegativity follows from positivity of the remaining tail, and `h_B=0` is equality.  The converse is immediate.  QED.

### Repeated depths

Repeated rigid depths are allowed and are classified by `n_e`.  Repeating a dynamic depth is outside the formal model and destroys the theorem: two copies of `(l-1)/l` form a strict-excess minimal budget for every odd `l`.

### Kraft interpretation and depth bound

Replace each dynamic atom at depth `e` by `l-1` unit atoms `l^-e`.  Put

```text
M=sum_e n_e+(l-1)sum_e epsilon_e.
```

The equality is the `l`-ary Kraft equality.  It is realized by a complete `l`-ary prefix tree with `M` leaves.  A deepest path of length `B` forces at least `1+B(l-1)` leaves, so

```text
B <= floor((M-1)/(l-1)).
```

If `A=sum n_e+sum epsilon_e` is the original atom count, then `M<=(l-1)A`, hence

```text
B<=A-1.
```

Saturation alone has no absolute depth bound because `l^B` rigid atoms of mass `l^-B` give equality for every `B`.

## 2. Row-count corollaries

- At least two atoms are necessary.
- The unique two-atom equality is

```text
(l-1)/l + 1/l = 1.
```

- If the depth-one dynamic atom is absent, every atom has mass at most `1/l`; hence at least `l` atoms are necessary.  Equality in this lower bound forces `l` rigid depth-one atoms.

## 3. One dynamic row plus one rigid row

Let a single dynamic row contain denominator depths `E`, and let the only rigid row have depth `r`.

### Theorem 2 — bundled two-row equality

```text
sum_(e in E)(l-1)/l^e + 1/l^r = 1
```

if and only if

```text
E={1,2,...,r}.
```

#### Proof

The displayed set `E={1,...,r}` gives the telescoping identity

```text
sum_(e=1)^r (l-1)/l^e = 1-1/l^r.
```

Conversely, compare any candidate with this identity.  If some `k<=r` is the first missing dynamic depth, the lost mass is `(l-1)/l^k`.  Even adding every possible dynamic depth strictly beyond `r` recovers only

```text
sum_(e>r)(l-1)/l^e = 1/l^r <= 1/l^k < (l-1)/l^k,
```

so the total remains below one.  Therefore every depth `1,...,r` is present.  These terms together with the rigid mass already total one, so no deeper dynamic term can occur.  QED.

Because admitted dynamic shells satisfy the odd-valuation parity rule, consecutive shell depths cannot all occur when `r>=2`.  Therefore the unique admitted two-row **equality** pattern is the beta-one pair

```text
D=(l-1)/l,
R=1/l.
```

This does not forbid row-minimal two-row covers with strict excess: if the dynamic row accepts shell `j=0` and additional same-parity shells `j>=2`, a centered depth-one rigid row covers the fiber, and the deeper shells overlap it.

## 4. Exact `l`-adic inverse theorem

Fix `F=Z/l^beta Z`, a canonical center lift `zeta`, dynamic shell set `J subset {0,...,m-1}`, and finitely many rigid cylinders.  Suppose the row events cover `F`, and delete rows until the cover is irredundant.

### Theorem 3 — centered prefix-frontier classification

Exactly one rigid cylinder contains `zeta`; write it as

```text
C_e(zeta), 1<=e<=beta.
```

Every other rigid cylinder is disjoint from `C_e(zeta)` and lies in a unique shell `S_j(zeta)` with `j<e`.  Such a cylinder can occur only when `j` is not dynamically accepted.  For every unaccepted `j<e` and each of the `l-1` immediate side cylinders at depth `j+1`, the rigid rows inside that side cylinder form a complete prefix-code frontier.

If the dynamic row remains in the irredundant cover, then

```text
J intersect {0,...,e-1} is nonempty.
```

Conversely, every construction satisfying these conditions is a row-minimal full cover.

#### Proof

The dynamic event excludes `zeta`, so a rigid cylinder contains it.  Cylinders containing one point are nested; two such cylinders in an irredundant cover are impossible because the deeper one is contained in the shallower one.  This proves uniqueness.

Any other rigid cylinder that meets `C_e(zeta)` is nested with it.  If it contains `C_e`, it also contains `zeta`; if it is contained in `C_e`, it is redundant.  Hence it is disjoint.  Its first digit differing from `zeta` occurs at a unique `j<e`, so the cylinder lies wholly in `S_j(zeta)`.  If that shell is dynamically accepted, the rigid cylinder is redundant.

Every point of an unaccepted side branch must therefore be covered by rigid cylinders lying inside that branch.  Two intersecting `l`-adic cylinders are nested, so irredundancy forces a prefix-free family; completeness forces a complete frontier.  The dynamic row is essential exactly when it has a shell below `e`, outside the centered cylinder.  The converse follows by disjoint witnesses: the center witnesses the centered row, every frontier cylinder has its own branch cells, and an accepted shell below `e` witnesses the dynamic row.  QED.

### Overlap formula

The only overlap is

```text
A_J(zeta) intersect C_e(zeta)
  = union_(j in J, j>=e) S_j(zeta).
```

Consequently,

```text
sum of row masses
=1+sum_(j in J, j>=e)(l-1)/l^(j+1).
```

Every cell has multiplicity one or two.  Equality holds exactly when `J` has no accepted tail at or beyond `e`.

If accepted valuations may be pruned inside a row, deleting this overlap tail gives a valuation-minimal exact partition.  Deleting rows alone does not remove the tail.

## 5. Beta-one classification

For `beta=1`:

1. if `s_l` is odd and `J={0}`, the unique dynamic cover is the beta-one pair: `S_0` plus the centered depth-one digit;
2. with no essential dynamic event, the unique rigid-only cover is all `l` depth-one digits.

Thus an exact covered fiber need not contain a beta-one pair: the rigid-only partition is the smallest counterexample.

## 6. Beta-two classification

Odd-valuation parity permits at most one of `j=0,1`.

### Rigid-only

Each of the `l` depth-one digits is independently either selected as one rigid row or refined into all `l` depth-two cells.  The labelled count is

```text
2^l.
```

### Dynamic `J={0}` (`s_l` odd)

Exactly two templates occur:

1. `S_0` plus the centered depth-one cylinder;
2. `S_0` plus all `l` depth-two cells inside the center branch.

### Dynamic `J={1}` (`s_l` even, `m=2`)

The center is one depth-two cell.  Each of the `l-1` outer depth-one branches is independently coarse or refined into all `l` depth-two cells.  The labelled count is

```text
2^(l-1).
```

There is no overlap at `beta=2` because accepting both shells is arithmetically forbidden.

## 7. Arbitrary beta recurrence and effective count

Let `F_l(h)` be the number of complete frontiers of a rooted `l`-ary cylinder of remaining height `h`, allowing the root itself:

```text
F_l(0)=1,
F_l(h)=1+F_l(h-1)^l.
```

For fixed `beta,m,J,e`, the number of parameter-labelled templates is

```text
N(l,beta,m,J,e)
= product_(0<=j<e, j not dynamically accepted)
  F_l(beta-j-1)^(l-1),
```

provided the dynamic essentiality condition holds.  This is finite and effective for every fixed `beta`.

Using

```text
F_l(h)<=2^((l^h-1)/(l-1)),
```

one obtains a crude effective bound

```text
N <= 2^((l^beta-1)/(l-1)).
```

After summing over `e` and parity-admissible `J`, a fixed-`beta` catalog is bounded by

```text
beta * 2^m * 2^((l^beta-1)/(l-1)).
```

Here “parameter-labelled” retains `m` and the parity of `s_l`; two labels may induce the same cylinder set family.  There is no depth-independent finite literal list.  Rigid prefix frontiers have unbounded refinement depth, and row-minimal dynamic covers can carry arbitrarily deep overlap tails in one row.

## 8. Greedy actual-fiber witness

Order the rational-prime coordinates of `U` increasingly.  Assign each dynamic row `p` to coordinate `p` and each rigid row `q` to `P^+(w_q)`, as in the bound theorem.

### Theorem 4 — complete cover forces an actual odd fiber cover

At the anchor supplied by the exact two-adic lemma, a complete admitted certificate forces the following event:

> for some odd coordinate `l` and some assignment of every lower coordinate, the dynamic and rigid events assigned to `l` actually cover the entire `l`-adic fiber.

#### Proof

The selected anchor passes the constant `K_2=2` boundary when present.  For `K_2>=3`, the coordinate-two unsafe event has density at most one half, so one chooses a safe two-adic digit.  Odd rows contribute no full coordinate-two event.

Proceed increasingly.  Given lower coordinates, if the events assigned to the current coordinate do not cover its fiber, choose an uncovered digit.  Later coordinates cannot change any earlier assigned event.  If this succeeds at every coordinate, the resulting coarse class avoids every fatal event.  Existing reverse CRT then produces a full safe exponent, contradicting completeness.  Therefore the greedy construction stops at a genuinely covered fiber.  It cannot stop at coordinate two, so the coordinate is odd.  QED.

### Corollary — template occurrence in every complete certificate

Take a fiberwise irredundant subcover of the witness fiber and apply Theorem 3.  Hence every complete certificate contains, at the selected anchor and some lower assignment, one of the parameterized centered prefix-frontier templates.

This deduction is strictly stronger than the previously proved rational condition `D_{l,c}+R_{l,c}>=1`, but remains only a necessary structural condition.
