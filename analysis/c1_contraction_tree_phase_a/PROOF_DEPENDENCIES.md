# Proof dependencies and independent rechecks

## Authority sources read at the bound revision

The following files were treated as source material, not as automatically true theorems:

```text
STATUS.md
analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md
analysis/c1_entangled_coordinate_deficit/THEOREM_AUDIT.md
analysis/c1_entangled_coordinate_deficit/QUANTIFIER_CROSSWALK.md
analysis/c1_entangled_coordinate_deficit/EVIDENCE_CLASSIFICATION.md
analysis/c1_entangled_coordinate_deficit/results/k2_boundary_replay.json
analysis/c1_nonregular_coarse_fatal_audit/README.md
analysis/c1_nonregular_coarse_fatal_audit/THEOREM_AUDIT.md
```

All paths are bound to commit
`29fee0317b268d2b2747f9564efc445fdd6da7f9` and tree
`0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55`.

## D1. Prime-power lifting

For an odd prime `p!=5`, let

```text
w_p = ord_p(5),
s_p = v_p(5^w_p-1).
```

Then

```text
ord_(p^K)(5) = w_p p^max(0,K-s_p).
```

Independent proof: an exponent returning to one modulo `p` is a multiple `w_p t`; odd-prime LTE gives

```text
v_p(5^(w_p t)-1)=s_p+v_p(t).
```

The least `t` reaching precision `K` is therefore `p^max(0,K-s_p)`.

The tests compare this formula with direct multiplicative-order computation for `p=3,7,11,31,67` and `1<=K<=4`.

## D2. Fatal normal form

Fix an active coarse logarithm `b mod w_p` and write

```text
u=(r_p-3^c)5^(-b),
d=b+w_p q.
```

If `h=v_p(u-1)<min(s_p,K)`, every lift has the fixed valuation `h`.  If `K<=s_p` and `u=1 mod p^K`, every lift is a local zero and is unresolved.  Otherwise `s_p<K`, and the principal-unit cyclic group gives a unique

```text
q_0 mod p^(K-s_p)
```

with

```text
v_p(u-(5^w_p)^q)=s_p+v_p(q-q_0)
```

until the zero class.  Freezing `beta_p` digits therefore gives accepted shells plus an unresolved center cylinder.  This reconstruction is used directly by set enumeration; no union-bound equality is substituted for the normal form.

## D3. Reverse CRT

With

```text
U=lcm(t_2,{w_p}),
L=lcm(t_2,{w_p p^a_p}),
a_p=max(0,K_p-s_p),
beta_p=v_p(U),
```

one has

```text
L/U = product_p p^max(a_p-beta_p,0).
```

For a fixed coarse class `x mod U`, the remaining lift choice for row `p` depends only on the corresponding `p`-power component of `k` in `d=x+Uk`.  If no row is coarse fatal, choose one safe component for each row and combine them by CRT.  The two-adic state is fixed because its period divides `U`.

A small two-row system is exhaustively tested for every coarse class, comparing “no coarse-fatal row” with “a full safe lift exists.”

## D4. Ascending dependency DAG

If `p|w_q`, then `p|q-1`, so `p<q`.  Hence the graph is acyclic.  For odd `p`,

```text
beta_p=max_q v_p(w_q).
```

This proves triangular dependence.  It does not prove that any saturated fiber is aligned, that a compact contraction exists, or that a chosen syntactic rewrite reduces the active rank.

## D5. Beta-one aligned contraction

For

```text
s_p=1, K_p=2, E_p={1}, beta_p=1,
```

the dynamic row covers `p-1` digits and leaves one local-zero center.  A rigid row with `p||w_q` selects one digit after non-`p` coordinates are fixed.  The fiber is covered exactly when the selected digit equals the center.  Only then may the pair be replaced by

```text
x==b_p (mod w_p),
x==b_q (mod w_q/p).
```

The package independently reproduces both the aligned and misaligned cases.  They have the same displayed lower congruences but different coverage, proving that the alignment datum is logically indispensable.

## D6. Two-adic boundary

A residue modulo `2^K` is tested independently by direct square-sum residue sets.

- no two-adic row: no boundary;
- `K_2=2`: period one, so safety is a constant precondition;
- `K_2>=3`: a genuine coordinate-two event.

The four boundary reference cases reproduce safe counts `55,55,0,55` for the no-row, safe-constant, unsafe-constant, and `K_2=3` systems respectively.  In addition, every common residue is exhaustively checked for `2<=K_2<=10`; the worst selected-anchor unsafe density is `0` at `K_2=2` and never exceeds `1/2` thereafter.

## Dependency classification

The lifting formula, fatal normal form, reverse CRT, ascending DAG, beta-one local lemma, and two-adic boundary are prior dependencies after independent recheck.  The new content of this package is:

- the exact semantic contraction theorem and bounds;
- the precise separation between semantic and admitted-class contraction;
- the arithmetic aligned/misaligned soundness counterexample;
- the branch-local reuse requirement;
- the hereditary exact-shell-decomposability conditional theorem.
