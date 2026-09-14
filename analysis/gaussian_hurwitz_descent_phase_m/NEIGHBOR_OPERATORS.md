# Complete norm-5 operator classification

## N1. Norm-5 elements

All Hurwitz elements of norm 5 are exactly:

* the 48 signed permutations of (2,1,0,0);
* the 96 signed permutations of (3,3,1,1)/2.

For integral coordinates this follows by solving a²+b²+x²+t²=5. For half
coordinates solve A²+B²+X²+T²=20 with all coordinates odd: the only squared
pattern is 9+9+1+1. Hence this list is complete, not a prime scan.
The 24 units are the eight signed coordinate axes and the sixteen
(±1,±1,±1,±1)/2.

Let R={1±2i,1±2j,1±2k}. On either side, R is a full list of six unit-associate
classes:

    {alpha∈H:N(alpha)=5} = disjoint union_(r∈R) U r
                       = disjoint union_(r∈R) r U.

Multiplying the six representatives by the 24 explicitly listed units verifies
144 distinct results on each side. This finite verification is reproduced by
both implementations. Equivalently, the corresponding six kernels or images
modulo 5 are the six projective lines over F5.

## N2. All two-sided transformations

For every alpha,beta of norm 5 define

    T_(alpha,beta)(q)=alpha q beta/5,

with domain exactly those q∈H for which the output is in H. Then

    N(T(q))=N(q),
    T^(-1)(q')=bar(alpha) q' bar(beta)/5.

Both formulas are exact. There are 144²=20,736 ordered parameter pairs and
10,368 distinct rational linear operators. To see that the only duplication
is a simultaneous sign, suppose alpha q beta=alpha' q beta' for all q.
Then alpha'^(-1)alpha q=q beta' beta^(-1) for all q. Taking q=1 and then the
basis elements shows the common factor is central; equality of norms makes
it ±1. Thus (alpha,beta) and (-alpha,-beta) are the only two parameters for
one operator.

Modulo units on the output, it is enough to apply the 36 maps r q s/5 with
r,s∈R: write alpha=u r, beta=s v and absorb u,v into the finite symmetry
orbit. The full producer nevertheless constructs all 10,368 matrices; the
second implementation uses only these 36 associate-class maps.

## N3. Exact congruence classification

At 5 use i↦diag(2,-2), j↦[[0,-1],[1,0]]. This yields an algebra isomorphism

    F:H/5H → M2(F5),
    F(a+bi+xj+tk)=[[a+2b,-x-2t],[x-2t,a-2b]] (mod 5).

Half-coordinates use 2^(-1)=3 modulo 5. Each norm-5 element has rank-one
reduction. With A=F(alpha), B=F(beta), Q=F(q), the exact legal-move criterion is

    alpha q beta∈5H  ⇔  A Q B=0
                      ⇔ Q(im B)⊆ker A.

For the 36 kernel/image line pairs, the number of legal pairs is:

| rank Q | number of residues Q | legal associate-class pairs |
|---|---:|---:|
| 2 | 480 | 6 |
| 1 | 144 | 11 |
| 0 | 1 | 36 |

Proof of the final column: an invertible Q maps each line to exactly one line;
for rank one, one input line is killed (six output choices) and the other five
must use the unique image line (five choices); zero kills every input line.
The counts of Q are |GL2(F5)|=480 and (5²-1)²/(5-1)=144 for rank one.

For a directly inspectable associate table, write a line as the span of its
listed vector in F5²:

| representative r | ker F(r) | im F(r) |
|---|---|---|
| 1-2i | (0,1) | (1,0) |
| 1+2i | (1,0) | (0,1) |
| 1-2j | (1,2) | (1,3) |
| 1+2j | (1,3) | (1,2) |
| 1-2k | (1,1) | (1,4) |
| 1+2k | (1,4) | (1,1) |

Each side runs through all six projective lines.

The producer checks all 625 H-basis residue vectors. For literal parameter
pairs, multiply the final column by 24². No heuristic divisibility or hidden
higher 5-adic test is being substituted for this criterion.

## N4. Matrix implementation and 2-adic guard

Use doubled Hamilton coordinates X=2q, A2=2alpha, B2=2beta. Let

    L(a,b,x,t)=[[a,-b,-x,-t],[b,a,-t,x],
                [x,t,a,-b],[t,-x,b,a]],
    R(a,b,x,t)=[[a,-b,-x,-t],[b,a,t,-x],
                [x,-t,a,b],[t,x,-b,a]].

Then with C=L(A2)R(B2),

    X'=CX/20,    C^T C=400 I.

Legal Hurwitz output requires CX divisible by 20 in every coordinate and
X' all of one parity. For a genuine H input, the latter follows from the
ring criterion, and the program checks it explicitly. Integral (Lipschitz)
output is equivalent to CX divisible by 40 coordinatewise. See INTEGRALITY.md.
The inverse operator is C^T/20, and every transpose occurs in the list.

As a warning, a small subfamily can preserve the wrong quantity identically:
conjugation by r=1+2i gives

    r(a+bi+xj+tk)bar(r)/5
      = a+bi+((-3x-4t)/5)j+((4x-3t)/5)k.

Its legal domain has t≡3x (mod 5), but it preserves x²+t² exactly. Studying
only this one conjugation would not test the full proposed mechanism.

## Scope

The classification is complete for alpha q beta/5 with N(alpha)=N(beta)=5.
It does not classify all rational orthogonal maps, state-dependent maps with
other denominators, or all possible identities that change c.
