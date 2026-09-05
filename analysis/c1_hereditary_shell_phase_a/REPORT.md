# A303656 C=1 hereditary exact shell decomposability — targeted Phase A

## 0. Status and authority

This research was performed read-only against:

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 1100eb5ba01d90e5b1001be0bdfa464860fdbb92
main tree: ad1269916bf420c564e34887a96c808033fe538b
```

The authority state remains:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The source study was read-only. This repository-native integration adds only
this analysis directory on a dedicated audit branch and does not modify
`STATUS.md`, authority records, workflows, or `main`.

## 1. Final verdict

```text
TARGETED STRUCTURAL ADVANCE

HEREDITARY PROVENANCE-CYLINDER CONTRACTION: PROVED
LITERAL ROW-ONLY HEREDITARY CLOSURE: FALSE
UNQUALIFIED ADMITTED-ROW CLOSURE: NOT CLAIMED
```

The phrase “admitted residual grammar” must be fixed before a yes/no answer is
well-defined.

1. In a literal **row-only grammar**, in which a residual must be a union of
   stripped guards of individual existing rows and no derived conjunction
   macro is allowed, hereditary closure is false.  The aligned arithmetic
   `(67,20771)` beta-one pair is a minimal-by-row-count genuine witness.

2. In the minimal **provenance-cylinder grammar** forced by the already
   accepted beta-one contraction—finite families of CRT-cylinder macros, each
   produced as the intersection of the stripped guards of an exact covering
   subfamily—hereditary exact shell decomposability is automatic for every
   finite admitted fixed-anchor system.

For a fixed-anchor finite triangular admitted system, exact maximal-coordinate
contraction is therefore hereditarily closed only in the explicitly defined
provenance-cylinder residual grammar below. This does not assert closure of an
unqualified admitted-row grammar. It does not prove that a complete certificate
exists, does not rule one out, and does not resolve A303656.

## 2. Guarded-slice normal form

Fix one anchor `c`, a reachable state, and its maximal odd coordinate `p`.
All predicates below are interpreted relative to the state's current lower
cylinder `Gamma`.  Split any finite macro disjunction—and, when necessary,
any finite family of active logarithm classes—into separate clauses.  Write
the active domain as

```text
Y x X_p,
X_p = Z/p^beta Z.
```

After keeping disjunctive clauses separate, every rank-`p` event has the exact
factorization

```text
E_i = G_i x A_i.
```

Here `G_i` is a compatible `p`-free lower CRT cylinder and `A_i` is fixed,
independent of the lower assignment:

- for the original dynamic row `p`, `A_i` is its admitted shell bundle about a
  fixed center and `G_i` is the active logarithm condition modulo `w_p`;
- for an original rigid row `q` assigned to `p`, if
  `e=v_p(w_q)`, then `A_i` is one depth-`e` `p`-cylinder and `G_i` is the
  corresponding congruence modulo `w_q/p^e`;
- for a previously derived macro-cylinder, factor its modulus at `p`; its
  `p`-part is a rigid slice and its remaining part is the lower guard.

The factorization is arithmetic, not semantic point enumeration.  It follows
from CRT and from the exact exponent congruences of the row normal form.  In
particular, the dynamic center and every rigid digit are fixed in one common
CRT coordinate system.

## 3. Canonical cover-clause formula

Let the rank-`p` slices be `A_1,...,A_r`.  Define the exact cover hypergraph

```text
C_p = {I subset {1,...,r}:
       union_{i in I} A_i = X_p,
       no proper subset of I covers X_p}.
```

For `I in C_p`, put

```text
G_I = intersection_{i in I} G_i.
```

Each `G_I` is empty or one compatible `p`-free CRT cylinder.  Its modulus is
an LCM of stripped row/macro moduli and its residue is obtained by exact
non-coprime CRT.

### Theorem — canonical exact cover-clause elimination

```text
Sat_p = union_{I in C_p} G_I.                 (1)
```

Equivalently, in Boolean notation,

```text
1_{Sat_p}(y)
 = OR_{I in C_p} AND_{i in I} 1_{G_i}(y).    (2)
```

### Proof

If `y in Sat_p`, the active slices at `y` cover `X_p`.  Since the active family
is finite, it contains an inclusion-minimal covering subfamily `I`; then
`y in G_I`.

Conversely, if `y in G_I`, every event indexed by `I` is active and their exact
slices cover `X_p`, so `y in Sat_p`.

No inactive-row conditions are required: coverage is monotone under adding
more active fatal events.  This is why the formula uses only positive guard
conjunctions and why branch-local row reuse is sound.

The union in (1) may have overlapping clauses.  If the contraction formalism
requires disjoint children, refine all lower guards to their common finite CRT
modulus, partition the union into disjoint residue cylinders, and attach to
each refined cylinder any cover clause that contains it.  This is an exact
Boolean-algebra refinement of named CRT guards; it does not introduce an
arbitrary semantic point predicate and it preserves the selected fiber-cover
witness.

The members of `C_p` are exactly the prime implicants of the monotone Boolean
coverage function in the guard-activity variables.  They form an antichain, so
one contraction step produces at most

```text
binomial(r,floor(r/2))
```

cover clauses by Sperner's theorem.  This is a row-count bound independent of
`|X_p|`, although iteration can still grow exponentially.

## 4. Provenance-cylinder residual grammar

Define the smallest grammar `G_prov` with the following objects and rules.

1. Original admitted dynamic shell events and rigid row cylinders are atoms.
2. A derived event is a compatible CRT cylinder carrying its parent state,
   eliminated coordinate, exact covering subfamily, and parent provenances.
3. The derived cylinder is created only by equation (1): intersect the exact
   `p`-free guards of a subfamily whose actual `p`-slices cover `X_p`.
4. Alternative clauses may remain as an overlapping disjunction.  When
   disjoint children are required, only the common-modulus CRT refinement
   described after equation (2) is allowed; no arbitrary lower subset may be
   inserted.
5. The same row/provenance may occur in several clauses.  Rows are not
   destructively consumed.
6. Duplicate or absorbed clauses may be removed only after exact cylinder-set
   equality/inclusion checks.

This grammar is syntactically and provenance-wise narrower than arbitrary
semantic DNF: every clause has a named exact fiber-cover witness and every
modulus/residue is inherited by CRT from actual row or prior macro data.  For
a particular system its realized cylinder algebra may happen to separate all
lower points, but no point predicate may be inserted without such provenance.

## 5. Hereditary closure theorem

### Theorem — hereditary provenance-cylinder contraction

For every finite admitted fixed-anchor odd-coordinate system passing its
appropriate `K_2=2` boundary, exact maximal-coordinate contraction in
`G_prov` is finite, sound, and hereditarily exact-shell decomposable.

### Proof

Induct on the number of active coordinates.

At maximal `p`, the guarded-slice normal form applies.  Equation (1) replaces
all rank-`p` events by finitely many provenance-cylinder macros.  Every output
macro has no `p`-dependence.  The standard contraction identity retains all
lower-rank events and proves exact equivalence.

A nonempty output macro is one CRT cylinder.  At its next largest coordinate
it factors again as a lower guard times one rigid cylinder.  The only possible
original dynamic event at that coordinate remains its admitted shell bundle.
Thus every child has the same guarded-slice normal form and lies in `G_prov`.
The active-coordinate count strictly decreases.  Induction completes the
proof.

For each exact cover clause, delete redundant top events.  The resulting
fiberwise irredundant cover is exactly one of the centered prefix-frontier
configurations already classified on main: one centered rigid cylinder, rigid
prefix frontiers in unaccepted side branches, and an optional essential
single dynamic shell bundle.  Derived macros count as rigid cylinders with
provenance; no synthetic prime is asserted.

A derived provenance macro may geometrically induce a rigid cylinder slice at
a later coordinate. This does **not** make that macro a new actual arithmetic
prime row. It remains a derived geometric rigid cylinder with provenance; no
synthetic prime is asserted and actual-prime realizability theorems cannot be
applied to it as though it were an original row.

Therefore the prefix-frontier classification is hereditary after adjoining
provenance-cylinder macros.

## 6. Exact obstruction criterion for any narrower grammar

Let `A_<p` be any proposed residual grammar on the lower domain.  For a state
at maximal `p`, calculate the canonical residual predicate

```text
Phi_p = OR_{I in C_p} AND_{i in I} G_i.
```

The state is one-step admitted-decomposable in `A_<p` if and only if `Phi_p`
has an exact `p`-free, provenance-valid representation in `A_<p`.  It is
hereditarily decomposable if and only if the same condition holds at every
recursively produced state.

Equivalently, a grammar closes uniformly on the present arithmetic class once
it (i) contains every stripped row guard, (ii) is closed under the compatible
finite intersections indexed by exact slice covers, (iii) allows the finite
OR of the resulting clauses, and (iv) lets every resulting CRT cylinder factor
at the next coordinate with provenance retained.  `G_prov` is the smallest
such positive CRT-cylinder closure.  Failure of any required meet gives an
explicit obstruction predicate `Phi_p`.

This is the requested necessary-and-sufficient criterion.  It distinguishes:

```text
semantic set equality
from arbitrary DNF
from abstract p-adic shell classification
from arithmetic/provenance realization.
```

### Row-only specialization

If `A_<p` allows only unions of individual stripped row guards, then

```text
Phi_p must equal a union of some G_i.
```

When the guards realize independent activity patterns, this is possible only
if a singleton top event covers the whole fiber.  A valid dynamic row never
does so because it excludes a local-zero center, and a rigid depth-positive
cylinder is proper.  Hence row-only closure is generically impossible.

## 7. Minimal genuine arithmetic row-only counterexample

At anchor `c=1`, use

```text
p=67, K_p=2, r_p=4, E_p={1}, w_p=22, s_p=1;
q=20771, K_q=2, r_q=20775, E_q={1},
w_q=10385=155*67, s_q=2.
```

The coarse period is `U=228470`; after removing the `67` coordinate, the lower
period is `3410`.

On the lower assignment `d==0 (mod 3410)`, the dynamic row covers 66 digits,
excludes its exact local-zero center, and the rigid row covers precisely that
center.  Thus the fiber is an exact `66+1` partition.

The stripped guards are

```text
G_67:     d==0 (mod 22),
G_20771:  d==0 (mod 155).
```

Direct enumeration of all `3410` lower assignments gives

```text
Sat_67 = G_67 intersection G_20771
       = {d==0 (mod 3410)}.
```

In the lower domain the four row-only unions have sizes

```text
0, 155, 22, 176,
```

whereas `Sat_67` has size `1`.  Therefore it cannot be represented by a union
of existing individual row guards.  It is represented exactly by one
provenance clause, the already sound pair-contraction residual.

This witness is minimal by row count: one valid odd-row event cannot cover a
whole odd fiber.  An independent exhaustive search of every
`q==3 (mod 4)`, `q!=5`, `q<=500000` found exactly the base-5 nonregular primes
`20771` and `40487`; hence `20771` is the smallest eligible rigid-row prime.
The second hit has largest order prime `653`, not an admitted dynamic prime.

This is a counterexample only to uniform row-only residual closure.  The
pair system itself is not a complete two-anchor certificate, so it does not
refute a statement quantified only over the presently unknown class of
complete certificates.  It is not a counterexample to `G_prov` and not a
counterexample to the contraction-tree strategy.

## 8. Local-zero preservation

The dynamic slice used in equation (1) is its exact fatal shell set, not its
mass.  Its unresolved center is absent.  A cover clause enters `C_p` only if
other actual rigid or derived macro slices cover every omitted center cell.
The resulting macro records a union-of-witnesses fact; it never changes the
valuation status of the dynamic row.  Thus local zero is preserved
hereditarily.

## 9. Two-adic interaction

- No two-adic row: no extra event is inserted.
- `K_2=2`: the event is constant in `d`; process it before odd contraction.
- `K_2>=3`: it depends only on the genuine coordinate two, which is lower than
  every odd coordinate.

For an odd coordinate `p`, write the lower two-adic predicate as `B(y)` and
the union of rank-`p` events as `T(y,z)`.  Then

```text
forall z [B(y) or T(y,z)]
 = B(y) or forall z T(y,z).
```

Hence odd-coordinate contraction commutes exactly with the two-adic event.
The reference checker exhaustively verified the Boolean identity and more
than one million exact two-adic period-independence cases for `K_2=2,...,5`.

## 10. Two anchors

Hereditary closure holds separately for `c=0` and `c=1` without changing any
shared row residue.  A simultaneous proof object may be the disjoint tagged
union of the two provenance trees.

A common untagged residual tree is not automatic.  The actual shared-residue
system

```text
r_67=2,
r_20771=13471
```

has an exact `66+1` fiber at both anchors, but direct enumeration gives

```text
c=0: Sat_67={2728 mod 3410},
c=1: Sat_67={1639 mod 3410}.
```

Thus shared rows and shared residues do not force shared residual cylinders.
A node-by-node identical untagged residual tree requires the two
anchor-specific canonical residual predicates to agree at every matched state;
that is an additional joint criterion, not a consequence of separate
completeness.  More permissive notions of a “common tree” must retain explicit
anchor tags and should not be conflated with this equality requirement.

## 11. Exact reference computation

The independent standard-library checker is
`hereditary_shell_classifier.py`; it imports no repository code.

### Prefix-frontier counts

The exact recurrence

```text
P_0(x)=x,
P_h(x)=x+P_{h-1}(x)^l
```

tracks complete rigid frontiers by row count.  It was used through `beta=5`
for `l=3,5,7`.  Full parameter-labelled counts rapidly become enormous; the
numbers of templates using at most 12 rows are:

| l | beta=1 | beta=2 | beta=3 | beta=4 | beta=5 |
|---:|---:|---:|---:|---:|---:|
| 3 | 2 | 16 | 304 | 2021 | 6147 |
| 5 | 2 | 15 | 51 | 85 | 139 |
| 7 | 2 | 6 | 12 | 19 | 31 |

All coefficients and the untruncated full counts are in `results.json`.

### Abstract exact covers and independent subset brute force

For `l=3,beta=2`, all `2^12=4096` rigid-cylinder subsets were checked in each
dynamic case—not merely the minimal covers:

| dynamic shells | all exact covers | exact partitions | row-minimal covers |
|:--|--:|--:|--:|
| none | 729 | 8 | 8 |
| `J={0}` | 2304 | 2 | 2 |
| `J={1}` | 972 | 4 | 4 |

Every row-minimal cover matched the prefix-frontier criterion.  Full subset
enumeration was also completed at `beta=1` for `l=3,5,7`.

- `l=3,beta=3`: every candidate with at most six rigid rows was checked for
  `J` equal to `empty,{0},{1},{2},{0,2}`.
- `l=5,beta=2`: every candidate with at most six rigid rows was checked for
  `J` equal to `empty,{0},{1}`.

### Guarded-slice residual checks

Exact set identities were checked for:

```text
5184 two-row guard assignments;
1728 rigid-only three-row assignments;
1728 branch-local-reuse assignments;
10000 deterministic prefix-frontier assignments.
```

There were zero provenance-DNF failures.  Among the two-row cases, 422
nonempty exact residuals were not representable by a union of the two
individual row guards.

A separate three-level audit generated 5,000 triangular systems on coordinate
sizes `3 x 5 x 7`, contracted them recursively by cover clauses, and compared
the final root value with direct enumeration of the full product.  It included
1,866 complete systems, created 3,412 derived clauses, and had zero recursive
mismatches.

### Admitted-row-labelled catalog, arithmetic search, and replay

The bounded label audit keeps abstract templates separate from actual row
supply.  Through `q<=500000`, coordinates `3` and `7` admit a dynamic row but
have no eligible rigid resource; coordinate `5` is not an admitted dynamic
prime and also has no rigid resource.  Coordinate `67` has the genuine
resource `q=20771` and therefore an actual beta-one pair.  The other hit,
`q=40487`, is assigned to `653`, where the dynamic partner is inadmissible
because `653==1 (mod 4)`.

- exact prime search: 20,806 candidate primes through `500000`, with the full
  searched-prime list authenticated by SHA-256 in `results.json`;
- nonregular hits: `20771`, `40487`;
- no direct rigid resource with largest order coordinate `3`, `5`, or `7` in
  this bounded domain;
- all `228470` coarse exponents checked against the product formulas for the
  `67` dynamic guard/shell and `20771` rigid guard/slice;
- exact `67/20771` lower residual: one class modulo `3410`;
- exact two-anchor residuals: `2728` and `1639` modulo `3410`;
- local-zero center count and rigid alignment checked cell by cell;
- no floating-point coverage or mass decision was used.

## 12. Final verdict and route effect

```text
TARGETED STRUCTURAL ADVANCE

A hereditary exact contraction theorem is proved for the explicitly defined
provenance-cylinder residual grammar.

This does not prove closure of a literal actual-prime-row grammar.
```

```text
Does this strengthen the existing C=1 route?  YES, structurally.
```

It replaces the unproved hereditary-decomposition hypothesis by a canonical
construction for the explicitly defined `G_prov` grammar. This repository
addition is a scoped theorem record, not a claim that the project has promoted
the route or that literal actual-prime rows are hereditarily closed.

```text
Does this close the structural gate?  YES for G_prov;
                                  NO for literal row-only closure.
```

The beta-one contraction already requires a conjunction residual, so the
row-only reading is too narrow for the existing route.

```text
Does this kill the contraction-tree strategy?  NO.
```

It validates finite exact structural contraction but gives no invariant that
prevents a covered root.  Clause growth can be exponential, arithmetic
resources remain scarce, and the two anchors need not share residuals.

```text
Is the arithmetic existence/no-go question still open?  YES.
```

The smallest unresolved lemma after this phase is no longer hereditary
closure.  It is:

> Can the two anchor-tagged provenance contraction trees of a genuine finite
> admitted system both reach covered roots, subject to the shared-residue,
> local-zero, order-support, and two-adic constraints?

No complete certificate and no universal no-go is produced here.
