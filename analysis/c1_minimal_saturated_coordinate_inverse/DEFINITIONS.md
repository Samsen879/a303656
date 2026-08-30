# Definitions and scope

## 1. Authority and formal source class

This package is a read-only targeted Phase A analysis bound to:

```text
repository: Samsen879/a303656
repository ID: 1333945235
main SHA: 29fee0317b268d2b2747f9564efc445fdd6da7f9
main tree: 0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55
```

The project state remains:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The admitted odd rows, lifting quantities, coarse period `U`, full period `L`,
dynamic masses, rigid classes, two-adic boundary, and fail-closed local-zero
convention are exactly those of the bound `FORMAL_CLASS.md` and its theorem
audits. This package does not broaden that formal class.

## 2. Three non-interchangeable layers

### Layer 1: abstract rational budget

Fix an odd prime `l`. For depth `k>=1`, define the atomic masses

```math
D_k=\frac{l-1}{l^k},\qquad R_k=\frac1{l^k}.
```

Here `D_k` is the mass of one dynamic shell with valuation index `j=k-1`, and
`R_k` is the mass of one rigid cylinder of depth `k`. At this layer, positions,
overlaps, lower-coordinate activation, distinct-prime requirements, and
arithmetic realizability are deliberately forgotten.

A finite multiset of mass atoms is **budget-saturating** when its total is at
least one. It is **atom-deletion-minimal** when deleting any one mass atom
makes the total strictly smaller than one. This is not the same as deleting an
actual row: one dynamic row may bundle several shells.

### Layer 2: exact finite `l`-adic fiber

Let

```math
\Omega_{l,\beta}=\mathbb Z/l^\beta\mathbb Z.
```

For `1<=e<=beta` and `a mod l^e`, the rigid cylinder is

```math
C(e,a)=\{x\in\Omega_{l,\beta}:x\equiv a\pmod{l^e}\}.
```

Fix a dynamic depth `1<=m<=beta` and a center `z mod l^m`. For
`0<=j<m`, the dynamic shell is

```math
S_j(z)=\{x\in\Omega_{l,\beta}:v_l(x-z)=j\}.
```

For a shell set `J subset {0,...,m-1}`, the dynamic event is

```math
\mathcal D_J(z)=\bigcup_{j\in J}S_j(z).
```

In an admitted odd row,

```math
J=\{j:0\le j<m,\ s_l+j\in E_l\}.
```

Because `E_l` contains only positive odd valuations, all members of `J` have
one parity. The unresolved center cylinder `C(m,z)` is never dynamically
accepted.

A **pointwise fiber** means that the anchor and every coordinate smaller than
`l` have already been fixed. An assigned rigid row is then either inactive or
one cylinder `C(e,a)`. The same row may be inactive or give another cylinder
under another lower-coordinate assignment.

A family of retained rows is a **row-minimal exact cover** when its event union
is all of `Omega` and deleting any entire retained row creates at least one
uncovered cell. This is the minimality used by the inverse theorem.

An **exact partition** has multiplicity one at every cell. A **minimal
overlapping cover** is row-minimal but has multiplicity at least two somewhere.

### Layer 3: arithmetic realizability

For an admitted prime row `q`, put

```math
w_q=\operatorname{ord}_q(5),\qquad
s_q=v_q(5^{w_q}-1).
```

A rigid row assigned to coordinate `l` must satisfy

```math
P^+(w_q)=l,\qquad e=v_l(w_q),\qquad s_q>h
```

for some accepted positive odd `h`. In particular, a `K=2,E={1}` rigid row
requires `s_q>=2`.

A dynamic `l`-row has

```math
a_l=K_l-s_l>0,\qquad m=\min(a_l,\beta_l),
```

and its center is the principal-unit logarithm center supplied by the lifting
normal form. The exact local zero is unresolved and is never accepted.

An abstract frontier is **arithmetically realizable at one anchor and one
lower assignment** only after actual distinct primes, order depths, accepted
valuations, common lower congruences, and residues have been supplied. A
one-anchor realization does not imply common-residue compatibility at the
other anchor.

## 3. Prefix-code terminology

In the rooted `l`-ary residue tree, a node of depth `e` is a cylinder modulo
`l^e`. A finite set of nodes is a **complete prefix code for a rooted subtree**
when the nodes are pairwise incomparable and their cylinders partition that
subtree.

Let `F_l(h)` be the number of complete prefix codes of a full `l`-ary subtree
of remaining height `h`, with the subtree root itself allowed. Then

```math
F_l(0)=1,\qquad F_l(h)=1+F_l(h-1)^l.
```

The first term chooses the root. The second refines the root and independently
chooses a complete prefix code in each of its `l` children.

## 4. Evidence labels

- **PROVED**: a complete mathematical proof is supplied in this package.
- **EXACT FINITE COMPUTATION**: exhaustive only on the displayed frozen domain.
- **CONDITIONAL REALIZABILITY LEMMA**: a proof conditional on the existence of
  enough primes with named order/lifting properties.
- **BOUNDED ABSENCE**: never interpreted as a universal nonexistence theorem.

No statement in this package identifies a minimal coordinate frontier with a
complete `C=1` certificate, and no statement proves A303656.
