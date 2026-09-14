# Exact falsifications, including a compulsory-uphill primitive example

## M-D4. Norm 1175 has exact minimum barrier 13 from height 2

Use the symmetry quotient G and H_bad defined in the companion files.
Let q0=(1,3,3,34), so N(q0)=1+9+9+1156=1175. It is primitive in both L
and H and has kappa_5=1. Its G-orbit is index 8 in the frozen enumeration.

**Theorem.** The target is reachable from q0, but every legal path to a target,
allowing arbitrary intermediate Hurwitz states and all G symmetries, visits
an orbit with H_bad≥13. There is a path whose maximum H_bad is exactly 13.
In particular H_bad, log H_bad, and every strictly increasing reparameterization
of H_bad cannot give even a nonincreasing target path from this state.

### Exhaustive lower certificate

The component of q0 in the induced subgraph H_bad<13 consists of precisely
two G-orbits, indices 8 and 9. Both have height 2 and neither is a target.
Their complete lists of B4 shapes, in doubled coordinates, are:

    8: (2,6,6,68), (27,35,35,39), (29,33,33,41)
    9: (2,6,36,58), (7,15,45,49), (9,13,43,51).

In each orbit only the all-even shape is integral. Thus the associated
integer patterns are (1,3,3,34) and (1,3,18,29). All one-step neighbors are:

| source orbit | destination | integral absolute pattern | H_bad |
|---:|---:|---|---:|
| 8 | 3 | [6, 15, 17, 25] | 13 |
| 8 | 8 | [1, 3, 3, 34] | 2 |
| 8 | 9 | [1, 3, 18, 29] | 2 |
| 8 | 23 | [10, 15, 15, 25] | 13 |
| 8 | 24 | [6, 11, 17, 27] | 13 |
| 8 | 34 | [10, 11, 15, 27] | 13 |
| 9 | 1 | [3, 7, 21, 26] | 18 |
| 9 | 3 | [6, 15, 17, 25] | 13 |
| 9 | 5 | [3, 10, 15, 29] | 13 |
| 9 | 8 | [1, 3, 3, 34] | 2 |
| 9 | 9 | [1, 3, 18, 29] | 2 |
| 9 | 12 | [1, 15, 18, 25] | 13 |
| 9 | 23 | [10, 15, 15, 25] | 13 |
| 9 | 24 | [6, 11, 17, 27] | 13 |
| 9 | 32 | [7, 18, 19, 21] | 82 |
| 9 | 34 | [10, 11, 15, 27] | 13 |

The 36 representative maps rqs/5, with exact division and unit canonicalization,
certify this table. Its completeness also follows independently by applying
all 10,368 full matrices to the B4 shapes. Every exit from {8,9} has height
at least 13. Hence a path to a target (height 1) must cross that barrier.
This is a finite exhaustive proof with two independent implementations,
not a numerical density argument. The mathematical proof of operator
completeness is in NEIGHBOR_OPERATORS.md.

### Exact upper certificate

In Hamilton coordinates, put alpha1=-2-k and beta1=-2+j. Then

    alpha1 q0 beta1/5 = (-11,15,10,27).

A signed permutation gives q1=(10,11,15,27), orbit 34, H_bad=13. Now put
alpha2=-2+j and beta2=-2-k. Direct multiplication gives

    alpha2 q1 beta2/5 = (1,2,9,33).

This is orbit 6 and a target after swapping coordinate pairs, since

    1175 = 9²+33²+(1²+2²),   1²+2²=5.

All four parameters have norm 5; every division is exact and integral.
The orbit path is 8→34→6 and its heights are 2→13→1. Together with the lower
certificate, this proves the minimax barrier is exactly 13.

The statement is about fixed M, not paths that change c. It does not exclude
a different well-founded height, a larger jump not factored through the legal
integral intermediate states, or a representation-dependent c-changing map.

## H_Omega also fails on a primitive, target-accessible state

At M=81, q=(2,2,3,8) has H_Omega=1 and kappa_5=1. Its symmetry orbit is 5.
Its only quotient neighbors are 3,4,5, all with H_Omega=1. A target has height 0.
Thus there is no strict one-step decrease. A two-step target path is
5→4→1, whose H_bad heights are 8→4→1 but H_Omega heights are 1→1→0.
Changing from H_bad to Omega is not a successful repair.

## Other exact distinctions

At M=243 a height-2 state can require a plateau before a decrease; that alone
would not prohibit nonincreasing paths. The norm-1175 theorem is stronger:
a genuine increase is unavoidable. The producer records 163 strict local
minimum witnesses over the two tested heights; bottlenecks.py identifies 12
states with compulsory H_bad increase. Only the precisely stated finite
examples and the general content theorem are promoted, not a growth law for
barriers or distances.

At M=47 and M=49 the entire target set is empty. These are not original
A303656 counterexamples: 48=6²+2²+3+5 and 50=6²+2²+9+1.
