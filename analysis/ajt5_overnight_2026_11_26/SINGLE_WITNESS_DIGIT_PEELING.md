# Digit peeling and a necessary saturated core for first blocking

Work in the single-witness growth limit. First select the two parities to pass 2 and give a unit at 3, as in [simultaneous avoidance](SINGLE_WITNESS_FOUR_TARGET_AVOIDANCE.md). For \(p>3\) inert, give each common Wieferich target the stronger requirement of a unit residual. For an ordinary earlier prime impose the sufficient test “unit or exact valuation two”. These tests read finitely many primary digits and passing them rules out first blocking if the terminal is one of the unit targets.

Let \(x\) be the primary coordinate at \(r\) of one exponent axis. Its outside reader load for a finite set of tests is
\[
 L_x=\sum_{p\ne r:\,\text{test }p\text{ reads }x} r^{-e_p},
 \qquad e_p=v_r(\operatorname{ord}_p(b)),
\]
where \(b\) is the base on that axial coordinate. Freezing all other coordinates, one wrong first residue forbids at most \(r^{-e_p}\) of a full grid. The full norm condition at an ordinary reader can only exclude less than the unit test used for this bound.

* If there is no remaining own test at \(r\) reading \(x\), and \(L_x<1\), remove every remaining test that reads \(x\), solve the rest, then choose \(x\) to hold all removed tests open.
* If the own test is ordinary and \(x\) is one of its ordinary axes, its allowed set in the same grid has measure at least \((r-1)/r^2\). This is all of the grid when the residual is a unit, and equals \((r-1)/r^2\) at a root: the first digit cancels at depth two, and all but one next digit make the valuation exactly two. Thus whenever \(L_x<(r-1)/r^2\), it is safe to remove all readers including the own test and then assign \(x\) after solving the rest.

Take at least two digits in the own-test grid and enough for all external readers. These steps can be applied in any order; every retained test is genuinely independent of the peeled variable. One may also peel blocks not containing an own-test restriction by the joint-order bound from the [weighted block test](SINGLE_WITNESS_SIX_TARGET_AVOIDANCE.md).

If a finite head first blocks, peeling cannot remove every test, since reversing the assignments would construct a passing phase. A nonempty remaining core must satisfy both load lower bounds at every eligible relevant variable, relative to its type. In particular, if all outside readers of an ordinary axis read depth \(e_p\ge2\), the necessary inequality is
\[
 \sum_{p\ne r:\,\text{reads }x} r^{2-e_p}\ \ge\ r-1.
\]
A surviving ordinary prime must have a larger reader on one of its ordinary axes (otherwise one simply peels that axis). Along this strict chain of primes the finite core leads to a true common Wieferich target. This is a necessary capacity certificate, not a test that establishes actual covering; it does not show that there are no such cores. Known gcd bounds only govern true terminal order pairs, not the ordinary reader graph.

## True ordinary-prime replay

The five first targets have load one if one insists on working at 5. On the first axis at 3 their load is \(13609/19683<1\). A separate target 491 reads two digits at 7. Its one outside weight \(1/49\) is strictly below the \((7-1)/7^2\) repair capacity. In the same integer example one of the six valuation-two ordinary phases is removed by 491, leaving five choices and preserving all targets. All rows here are ordinary; no true common Wieferich obstruction is asserted.

~~~python
from fractions import Fraction as F
from math import isqrt

P = (31,271,811,21871,196831)
O = ((30,3),(30,27),(810,405),(810,10935),(196830,98415))
n = 171254614781202647272066113924211428945
C, L = 98415, 196830

def s(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

for p, pair in zip(P,O):
    for a,o in zip((3,5),pair):
        assert pow(a,o,p)==1
        assert all(pow(a,o//r,p)!=1 for r in (2,3,5) if o%r==0)
    assert any(o%5==0 for o in pair) and all(o%25 for o in pair)
assert sum(F(1,d) for d in (3,3,81,81,19683)) == F(13609,19683) < 1

for p in P+(7,491):
    assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
    assert any(pow(a,p-1,p*p)!=1 for a in (3,5))
assert all(pow(a,490,491)==1 and pow(a,70,491)!=1 for a in (3,5))

c = C+10
u = lambda j,m: (n-s(c,C+L*j,m)) % m
assert u(0,49)==7
assert len({u(j,491) for j in range(49)})==49
J = [j for j in range(49) if u(j,343) in range(49,343,49)]
assert J == [5,12,26,33,40,47]
assert [j for j in J if u(j,491)==0] == [5]
assert u(12,343)==147 and u(12,491)==489
assert all(u(12,p) for p in P)
assert u(12,4)==1 and u(12,3)!=0

~~~
