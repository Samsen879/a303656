# Third mechanism: c-changing identities and bounded-lift obstruction

## Exact representation-dependent identity

Let (n,c,q) be a state, with q=(a,b,x,t)∈Z⁴, N(q)=n-3^c. If

    b-t-1=3^c,

define

    c'=c+1,   q'=(a,b-1,x,t+1).

Direct expansion gives

    N(q')-N(q)=(-2b+1)+(2t+1)
                 =-2·3^c=3^c-3^(c+1).

Thus n is exactly preserved and the output remains integral. This genuinely
uses the actual representation, not a residue-density claim. For example,

    n=48, c=0, q=(6,3,1,1)
       → c'=1, q'=(6,2,1,2),

producing 48=6²+2²+3+5. It is only a conditional identity, NOT a descent:
there is no proved availability condition for all states, no strict arithmetic
height, and no general terminal theorem.

At n=17,c=0,M=16, every H representation has integral absolute coordinate
pattern (0,0,0,4) or (2,2,2,2). No signed coordinate difference equals 2,
so b-t-1=1 cannot hold in any symmetry orbit or fixed-norm 5-neighbor component.
This disproves universal availability of this identity from an arbitrary state.
It does not make n=17 a counterexample: 17=3²+2²+3+1.

## M-D3. Bounded-displacement/bounded-exponent lifts cannot be universal

Fix a finite set V⊂Z⁴ and an integer C≥1. Choose r≥1 so large that

    2^r > max_(v∈V) N(v)+3^C-1.

For n=4^r+1, c=0, no representation q∈H with N(q)=4^r admits a lift

    q'=q+v, v∈V,   c'∈{1,...,C},

preserving n. Empty V is trivially excluded.

Proof. Every H representation of 4^r is q=2^r u with u a Hurwitz unit. Here is
an elementary proof of that shell classification. A half-integral Hurwitz
point has odd norm. For an integral point of norm divisible by 8, all four
coordinates must be even: square residues modulo 8 exclude one or two odd
coordinates, and four odd squares sum to 4 modulo 8. Repeatedly divide by 2
until norm 4, whose only patterns are (±2,0,0,0) and (±1,±1,±1,±1).
These are precisely twice the units. Consequently each coordinate of q is
an integer multiple of 2^(r-1).

The required norm identity would be

    2<q,v>+N(v)=1-3^c',

so N(v)+3^c'-1 would be divisible by 2^r. That is a positive integer smaller
than 2^r by the choice of r, a contradiction. Preceding the attempted lift by
any legal fixed-norm neighbors or allowed symmetries does not help: the state
still lies on the same classified shell. Postcomposing by a norm-preserving
symmetry cannot change the necessary norm equation either.

This theorem only excludes **uniformly bounded** additive changes and exponent
jumps from arbitrary representations. It says nothing about unbounded,
representation-dependent displacement, general nonlinear maps, or a lemma
whose hypotheses specifically exploit an unknown minimal counterexample.
The exhibited n are not asserted to be counterexamples.

## What varying c actually fixes, and what remains

A fixed-norm obstruction need not survive changing c. For instance, n=50 has
M=49 at c=0 and M=47 at c=1; both shells are target-free. At c=2,

    50=6²+2²+3²+1,

so M=41 contains a target. This is direct finite arithmetic, not an original-n
scan. It shows that merely allowing one change c=0→1 is insufficient.

Assuming a least original counterexample gives representations of smaller
integers, but no identity here lifts one of those guaranteed representations
back to n while retaining exactly two squares, one 3-power, and one 5-power.
Accordingly no minimal-counterexample descent has been established.
