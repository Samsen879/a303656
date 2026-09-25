# Scope and boundary examples

MF-R permits a fixed finite number of independent source conics, including
repeated source offsets, any rational degree and poles, and genuine dependence
on all source coordinates. The identity must hold over the full generic
product with `U,V` in its original `Q`-function field and target `X-T`.

It does **not** rule out arithmetic selection of witnesses, proper algebraic
compatibility loci, rational decoders valid only on such loci, non-rational
operations, growing source complexity, arbitrary multi-witness methods,
nonlinear target norms, or Boolean/support recursion. No global multi-witness
route conclusion follows.

## Complex-coefficient escape

If output coefficients are extended to `K(i)`, put `s=X-T` and

```text
U=(s+1)/2,   V=(s-1)/(2i).
```

Then `U^2+V^2=s` for every `T`. The **coefficient field Q / original fixed
field is essential**; an assertion with `U,V in K(i)` is false.

## Proper compatibility-locus escape

Let `A_1=0,A_2=4` and impose
`(a_1-a_2)^2+(b_1-b_2)^2=4`. For
`U=(a_1+a_2)/2,V=(b_1+b_2)/2`, the polarization identity yields

```text
U^2+V^2 = (2(X-0)+2(X-4)-4)/4 = X-3.
```

The compatibility equation defines a proper locus in the product, while
`3` is neither source offset. A rational decoder restricted to this locus
is therefore outside MF-R. The locus is nonempty over an algebraic closure:
for `X=4`, choose `(a_2,b_2)=(0,0)` and `(a_1,b_1)=(2,0)`.

## Norm-one dependence on multiple sources

The rational rotation

```text
c=(a_1^2-b_1^2)/(X-A_1),  d=2*a_1*b_1/(X-A_1),
U=c*a_2-d*b_2,             V=d*a_2+c*b_2
```

has `c^2+d^2=1` and `U^2+V^2=X-A_2`. It genuinely uses both sources
but produces an existing offset, as MF-R permits. Thus the theorem does not
say that rational multi-source dependence is absent.
