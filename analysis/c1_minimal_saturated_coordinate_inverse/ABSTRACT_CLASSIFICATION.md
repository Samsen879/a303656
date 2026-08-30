# Abstract classification — review index

The full, byte-authenticated `ABSTRACT_CLASSIFICATION.md` and its complete
proofs are contained in the deterministic package documented in
`PACKAGE_PARTS.md`. This browsable file is intentionally only an index; it is
not a substitute for the authenticated proof text.

## Rational layer

For masses

```math
D_k=(l-1)l^{-k},\qquad R_k=l^{-k},
```

scale a finite multiset to common denominator `l^h`, let `Delta` be the excess
above `l^h`, and let `mu` be the least scaled atom weight. The package proves:

```math
\text{deletion-minimal saturation}\iff 0\le\Delta<\mu.
```

It derives the exact carry recurrence, the atom-depth bound `h <= N-1`, the
unique shortest equality chain, and the unique two-atom equality

```math
D_1+R_1=1.
```

For one actual dynamic row plus one rigid row, exact equality therefore forces
the beta-one outer shell plus one aligned center cylinder.

## Exact-cover layer

After fixing the anchor and all lower coordinates, retained rigid cylinders in
a row-minimal cover form a prefix-free family. Every pointwise minimal fiber
cover is classified by one of:

1. a center cutoff with complete prefix codes on uncovered side subtrees;
2. a proper unresolved-center refinement;
3. a rigid-only complete prefix code.

The classification is finite and effective for fixed `(l,beta,m,J)`, with
recurrence

```math
F_l(0)=1,\qquad F_l(h)=1+F_l(h-1)^l,
```

but there is no beta-independent finite literal list of diagrams.

## Certificate extraction

Completeness—not the mass inequality alone—forces the coordinate decision tree
to stop at some odd coordinate and fixed lower assignment where the actual
assigned events cover the whole fiber. Deleting redundant rows then produces
one of the classified pointwise frontiers.

The converse is false: one pointwise frontier does not imply a complete local
certificate, a common two-anchor system, or two-square representability.

For theorem statements and proofs, reconstruct the authenticated package:

```bash
python3 unpack_repository_package.py /tmp/a303656-coordinate-inverse
```
