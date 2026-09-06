# Counterexamples, failures and scope boundaries

## 1. Actual arithmetic: common escape is not the correct primal

Take only the two-adic row K_2=2, r_2=1. At c=0 the local value is
1-1-5^d = 3 modulo 4 and is always rejected. At c=1 it is
1-3-5^d = 1 modulo 4 and is safe. Therefore there is no exponent simultaneously
safe at both anchors, but the simultaneous certificate is not complete.

This is an actual counterexample to the **wrong primal equivalence**, not a
counterexample to universal finite-certificate no-go. The distinguished
boundary anchor in the master theorem is c_*=1 and works for both parities.

## 2. Actual arithmetic SPLIT (source example, independently replayed)

Use original primes 67 and 20771, K=2, E={1}, shared residues

    r_67=2,  r_20771=20775.

Their orders are 22 and 10385=5*31*67, and their lifting exponents are 1 and 2.
U=L=228470. At lower y=0 modulo 3410 and z=d modulo 67, the fatal sets are

    anchor 0: z != 0, from row 67;
    anchor 1: z = 0, from row 20771.

Their union is full. Neither anchor's own fiber is full. At z=0 anchor 0
survives: its local zero is unresolved, not accepted. Thus the exact alive-
anchor game succeeds even though a common-safe continuation at this prefix
fails. This is not a complete certificate or a new falsification of actual H1.

Independent replay in this bundle compares the row normal forms with direct
modular powers on all 228470 exponent classes at both anchors. Individual
safe counts are 218219 and 218218; the common safe count is 207968.

## 3. Current blocker deletion without its exclusion is unsound

At the same lower point in Example 2, assign row 20771 to blocker coordinate
67. Before choosing z, that event is not preblocked. If it is simply removed
from the current top list, the dynamic row suggests z=0 as a common escape.
But z=0 is precisely the other anchor's rigid fatal digit.

The sound procedure checks F_67={0} jointly with the dynamic complement. It
correctly finds no common-safe z at this prefix. A top full-fiber Kraft budget
may not delete this current row while retaining a whole-fiber demand of one.

There is an additional implementation pitfall: blocking one anchor's rigid
event must not delete a different dynamic event of the same original q at the
other anchor. The test suite includes a synthetic, explicitly non-arithmetic
mixed-role row to detect this bookkeeping error.

## 4. Geometry: mass at least one still leaves a hole

At p=3,beta=2 take D=S_0(0), blocker F={1,2}, and no rigid rows.
The naive cost is 2/3+2/3=4/3. Yet the blockers lie entirely inside D, and the
whole center branch 0 modulo 3 survives. Consequently “hybrid cost >=1” is
not an exact cover theorem, much less a certificate of global criticality.

For a centered bundle of arbitrary allowed depth, absence of a rigid or
blocker cylinder containing its center leaves a hole regardless of the sum
of overlapping masses.

## 5. Actual arithmetic: a naive safe-budget plus deficit potential increases

Use a fixed anchor c=0, K=2,E={1}, original primes 31 and 20771, and

    r_31=2,
    r_20771=1+5*(1+20771)=103861.

At lower coordinates d=0 modulo 3 and d=1 modulo 5, the dynamic 31-row
forbids precisely z!=0 in z=d modulo 31. The original 20771 rigid logarithm
class is b=1 modulo 10385. Giving it blocker 31 adds F_31={1}, already inside
the dynamic forbidden set.

The actual current safe budget stays 1/31. The **unconditioned alive future
inventory** loses the row's rank-67 mass 1/67. Hence

    Phi = current safe measure + (fixed baseline - alive future rigid mass)

increases by 1/67. This falsifies the proposed nonincrease for this explicit
naive potential.

If “future capacity” had already been conditioned on the entire current
safe set, this row could already have capacity zero and the calculation
would not apply. Thus the example does not disprove every possible potential,
every choice of weights, or a more carefully conditioned amortization.

## 6. Abstract configuration gap: weighted Hall is not integral sufficiency

Demands are a,b at anchor 0 and u,v at anchor 1. Row Q1 allows either pair
(a,u) or (b,v); Q2 allows either (a,v) or (b,u). No one choice for each row
covers all four demands. But giving each of its two options weight 1/2
covers every demand fractionally.

Therefore every nonnegative weighted configuration-capacity inequality can
hold even though integral feasibility fails. This is an abstract row-state
example, not a realization by actual base-5 prime rows.

## 7. Actual order arithmetic: long descent need not reach 3

Start with the admitted prime p=11, with ord_11(5)=5. For any prime
p=3 modulo 4, p!=5,

    Phi_p(5)=1+5+...+5^(p-1) = 3 modulo 4.

It has a prime factor q=3 modulo 4 to an odd multiplicity. The factor cannot
be p, since Phi_p(5)=1 modulo p, and cannot be 5. Its exact order of 5 is p,
so q>p. Iterating gives arbitrarily long actual order-dependency chains whose
bottom odd coordinate is 5, not 3. A verified prefix is

    5 <- 11 <- 12207031,
    ord_11(5)=5, ord_12207031(5)=11.

Thus an order-DAG descent of arbitrary length alone does not force a
coordinate-3 terminal trap. This does not refute a theorem imposing additional
complete-critical-demand hypotheses. The master theorem obtains a small-rank
trap instead from a bound on original rigid origins.

## 8. Genuine nonregular boundary resource (source datum rechecked)

The actual prime 1645333507 has

    ord_q(5)=2*3^3*30469139,  s_q=2.

Both odd factors 3 and 30469139 are admitted row-prime labels. If those original
rows are present, this nonregular resource has no free direct odd coordinate.
It demonstrates why free-blocker existence cannot be universally inferred from
the two small known nonregular primes. It is not a complete certificate.

## 9. Abstract seven-leaf geometry, not an arithmetic sharpness example

The following ternary cylinders form an irredundant full frontier:

    C_1(0), C_1(1), C_2(2), C_2(5), C_3(8), C_3(17), C_3(26).

It has profile (2,2,3) and Kraft sum 2/3+2/9+3/27=1. It respects the purely
geometric seven-leaf depth tax and the shallow-head upper counts. We have
not constructed seven actual nonregular original primes, with compatible
linear lineages and shared residues, realizing this frontier or a complete
certificate. No arithmetic sharpness is asserted.

The earlier three abstract depth-one cylinders at coordinate 3 used in the
core extractor test violate the actual shallow original-resource restriction.
They test syntax and exact coverage only, not the main arithmetic theorem.

## 10. Resultant limitation, not a universal exclusion

For q=20771 at its original rank 67, the same-lower paired graph is empty at
Y=0 but nonempty at other actual lower classes. In this bundle, Y=7 has a
paired edge (33,57), for example. The total over all 155 lower classes is
33 edges, with histogram {0:127,1:24,2:3,3:1}.

The nonzero integer resultant confines paired resources for fixed ordinary
Y and fixed h; it does not give a uniform finite prime set as Y varies.
Nor may its h be replaced by the current depth of a descended macro without
proving that its original arithmetic hypotheses survive that contraction.
