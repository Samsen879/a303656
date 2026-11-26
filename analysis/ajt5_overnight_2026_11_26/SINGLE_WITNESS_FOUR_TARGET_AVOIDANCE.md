# Four simultaneous inert-root targets for the single-witness problem

Let \(P,T\) be disjoint finite sets of odd inert primes. At each member of \(P\) at least one unit base has an ordinary lift, i.e. valuation one in \(a^{p-1}-1\). Suppose \(|T|\le4\). For arbitrary observations of the same profinite integer \(n\), there is a positive-measure phase cylinder giving a local norm at 2 and all \(P\), and a unit residual at every \(T\). At 3 use the growing-axis convention \(3^c=0\), so the only unit base there is 5. At members of \(T\) no ordinary-lift assumption is made.

**Proof.** Induct on the largest prime \(r\) dividing any unit-base order modulo a target. If there are no targets, repair ordinary primes in ascending order after the test at 2, using an unread own primary digit whenever a residual needs an even valuation. If the largest order factor is 2, the only possible inert target is 3: an inert \(t>3\) would have \(\operatorname{ord}_t(3)\mid2\), which would give \(t\mid8\). Choose the parity of \(d\) to avoid the root at 3. At 2, when \(n\) is odd one can choose \(c\)'s parity to give residual \(1\bmod4\). When \(n\) is even, the two parities of \(c\) give residuals differing by 2 modulo 8, so not both are the failing \(6\bmod8\) class. A residual congruent to 0 or 4 modulo 8 is made a norm by altering higher bits of \(d\), since \(5^2\) generates the principal unit group starting at depth 3. These higher bits do not change the 3-test. Repair the remaining ordinary primes in increasing order.

For \(r\ge3\) temporarily withdraw all targets \(T_1\) that read an \(r\)-primary digit. Add \(r\) as a substitute target if it is inert and not already a target. It replaces at least one test, and all substitute order factors are strictly smaller than \(r\). Apply the induction hypothesis, retaining only ordinary tests below \(r\) in this step (and removing any promoted test from \(P\)). This supplies fixed other primary coordinates, with a unit value at \(r\) if inert. Vary both \(r\)-primary coordinates independently across all the digits the withdrawn targets read. These changes do not disturb smaller primes, any target in \(T\setminus T_1\), or the unit residual at \(r\). For \(t\in T_1\), put \(e_t=\max_a v_r(\operatorname{ord}_t(a))\). With the other axis fixed, the most deeply read axis uniformly takes \(r^{e_t}\) distinct residues modulo \(t\). Thus one bad root removes a fraction at most \(r^{-e_t}\) of the shared grid. For \(r\ge5\) the sum over withdrawn targets is at most \(4/r<1\). For \(r=3\), an inert target with \(e_t=1\) must be the lone possibility \(t=7\), since an inert \(t>3\) with this order restriction divides \(3^6-1=2^3\cdot7\cdot13\). The sum is at most \(1/3+3/9<1\). Choose a grid point left over. Now repair all ordinary primes above \(r\) in increasing order, varying their own primary coordinates to obtain valuation two when necessary. They do not change any target modulo its prime, since the target orders have no prime factor above \(r\). All tests just imposed can be witnessed at finite depths, so the resulting good phases contain a cylinder.

**Consequence.** If \(q\) is among the first four common Wieferich inert primes, let \(T\) consist of \(q\) and all earlier common Wieferich inert primes, and \(P\) of all other earlier odd inert primes. For every \(n_q\bmod q\), the lemma supplies a phase that passes the full earlier head and avoids that terminal root. Thus \(U_q\) in the [terminal projection test](SINGLE_WITNESS_TERMINAL_PROJECTION.md) is not a singleton. Any actual first blocker must occur at the fifth or a later common Wieferich inert prime. This is not the assertion that any such primes exist. The elementary budget reaches equality for five targets of depth one at \(r=5\), and does not conclude that case.

## Replay of the shared-root and ordinary-repair steps

The actual control uses two ordinary target primes, 19 and 163, to check the two deleted grid points and an earlier 7-condition repaired without changing either target. It checks a finite same-\(n\) construction, not a blocker or an integer witness.

~~~python
from itertools import product
from math import isqrt

n = 743269
def s(c, d, m):
    return (pow(3,c,m) + pow(5,d,m)) % m

def order(a, p):
    return next(k for k in range(1,p) if pow(a,k,p) == 1)

assert [(order(3,p),order(5,p)) for p in (19,163)] == [(18,9),(162,54)]
assert all(pow(a,p-1,p*p) != 1 for p in (19,163) for a in (3,5))
assert (n%4,n%3,n%19,n%163) == (1,1,8,152)
bad = {(c,d) for c,d in product((1,3,5),repeat=2)
       if s(c,d,19)==n%19 or s(c,d,163)==n%163}
assert bad == {(1,1),(3,3)}

assert (n-s(1,3,49))%49 == 7
c,d = 1945,3
assert (n-s(c,d,343))%343 in range(49,343,49)
assert (s(c,d,19),s(c,d,163)) == (14,128)
assert (n-s(c,d,4))%4 == 1
for p in range(3,163,4):
    if all(p%j for j in range(2,isqrt(p)+1)):
        u = (n-s(c,d,p**3))%p**3
        assert u%p != 0 or u in range(p*p,p**3,p*p)

~~~
