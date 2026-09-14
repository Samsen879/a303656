# Defect heights, finite barriers and non-results

For the precise finite symmetry group G of INTEGRALITY.md and a G-orbit O,
define bad5(s)=s/5^v5(s) for POSITIVE s, and

```text
H_bad(O)   = min bad5(q_i^2+q_j^2)
H_Omega(O) = min Omega(bad5(q_i^2+q_j^2)).
```

Minima range over actual integral members of O and unordered coordinate pairs
with positive norm; zero pairs and half-integral members are excluded.
Omega counts prime factors with multiplicity. Targets have H_bad=1 and
H_Omega=0, and the converses here hold by the DEFINITION of these orbit heights,
not by a sufficiency theorem for kappa5.

At1175, q0=(1,3,3,34), alpha1=(-2,0,0,-1), beta1=(-2,0,1,0)
give q'=(-11,15,10,27). The signed permutation `(x,-a,b,t)` gives
(10,11,15,27). With alpha2=(-2,0,1,0), beta2=(-2,0,0,-1),
the next output is(1,2,9,33). Swapping coordinate pairs then gives the literal
terminal q=(9,33,1,2), with N(w)=5. Norms remain1175 throughout.

The lower certificate is the COMPLETE induced component at H_bad<13:
orbits{8,9}, both height2 and nonterminal. All exits have height>=13.
The path8->34->6 has heights2->13->1, attaining the lower bound. No claim
about a different height or a path changing c follows.

At81 the primitive q=(2,2,3,8), orbit5, is target-accessible but all its
one-step quotient neighbors3,4,5 have Omega height1. The path5->4->1 has
Omega heights1->1->0. This is a separate strict-decrease counterexample.

M-D1 blocks ANY target-terminating well-founded fixed-shell descent from
ARBITRARY states because some allowed components are target-free. M-D4 does
not say that no height function exists on an accessible component. A BFS
distance height would already assume target accessibility and does not solve
the original existence problem. Neither result rules out cross-shell,
S-arithmetic, state-dependent, automorphic or nonlinear mechanisms.
