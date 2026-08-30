# Adversarial counterexamples and boundary cases

Every finite example below is reproduced in exact arithmetic by the tools and
serialized, with a content hash, in `results/counterexamples.json`.

## 1. Budget equality does not imply coverage

Take `l=3,beta=m=1`, center zero, and the outer dynamic shell `J={0}`. Its
mass is `2/3`. Add one rigid depth-one cylinder of mass `1/3`, but put it at
digit one rather than the center digit zero.

```math
D+R=2/3+1/3=1.
```

The rigid cylinder overlaps the dynamic shell, and the center digit remains
uncovered. This is the minimal counterexample to treating rational equality as
an exact partition.

## 2. Strict budget excess can still leave holes

Take `l=3,beta=m=3,J={0,2}`, center zero, and one misaligned depth-one rigid
cylinder at digit one. The rational mass is

```math
2/3+2/27+1/3=29/27>1,
```

but the center-side holes are not covered.

## 3. Exact fiber cover without a beta-one rigid digit

Take `l=3,beta=2,m=1,J={0}`. Cover the unresolved center digit by its three
depth-two children:

```text
C(2,0), C(2,3), C(2,6).
```

Together with the outer dynamic shell this is a row-minimal exact partition.
There is no depth-one center rigid row. Thus “every exact cover contains a
beta-one pair” is false. The correct object is a complete prefix-code
refinement.

## 4. Minimality does not imply disjointness from the dynamic row

Take `l=3,beta=m=3,J={0,2}` and retain the center cylinder `C(1,0)`. The
dynamic row has private outer-shell cells; the rigid row has private unresolved
center cells. Both rows are essential. However `C(1,0)` overlaps the accepted
inner shell `S_2(0)`, giving total mass `29/27` and multiplicity two there.

This does not break the frontier theorem: it is exactly a Family A cutoff with
an accepted shell below and another accepted shell at/after the cutoff.

## 5. Repeated rigid masses can saturate density but be redundant

At `l=3,beta=1`, take rigid residues `0,0,1`. Their masses total one, but the
union covers only digits zero and one. One duplicate is row-redundant and digit
two is a hole.

## 6. No depth-independent finite literal template list

For every `beta>=2`, the outer dynamic shell plus all `l^(beta-1)` depth-`beta`
leaves in its center is a distinct row-minimal exact partition. Depth and row
count are unbounded. Any correct arbitrary-beta theorem must be parameterized
or recursive.

## 7. Abstract cylinder label can fail arithmetic realizability

The abstract request “a depth-one rigid cylinder at coordinate `l=3` supplied
by `q=7`” satisfies the order-depth relation `w_7=6`, but `s_7=1`. There is no
positive odd `h<s_7`, so this labeled rigid row is impossible.

## 8. Anchorwise realizability does not justify gluing

The separately realizable same-log center-zero beta-one prescriptions require
`r_67=2` at anchor zero and `r_67=4` at anchor one, with analogous conflicting
residues for `q=20771`. They cannot be one common-residue system. This refutes
naive independent gluing. It does not refute all dual-anchor systems; a
separate common-residue positive example exists.

## 9. Pointwise saturation is not uniform lower-coordinate saturation

The actual common-residue `(67,20771)` pair closes one 67-fiber at lower class
`2728 mod 3410` for anchor zero and one at `1639 mod 3410` for anchor one.
This does not say that every lower assignment is saturated. A pointwise
frontier must not be silently promoted to a uniform lower-coordinate cover.

## 10. `K_2` boundary must not leak into the odd-coordinate model

For `K_2=2`, an unsafe row is a constant boundary obstruction even when two is
not a coordinate of `U`. For `K_2>=3`, it is a genuine coordinate-two event.
Neither case contributes a cylinder to an odd coordinate `l`. Mixing it into
an odd frontier would repeat the already-rejected boundary error.
