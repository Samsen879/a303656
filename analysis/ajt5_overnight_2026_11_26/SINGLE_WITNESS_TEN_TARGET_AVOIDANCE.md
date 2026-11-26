# The first ten common-Wieferich inert primes cannot first block

The [weighted root-avoidance lemma](SINGLE_WITNESS_SIX_TARGET_AVOIDANCE.md) extends to ten simultaneous inert root targets for the actual bases 3,5, while retaining all earlier ordinary local norm conditions. Consequently no first finite blocker for the studied growth box can occur at any of its first ten common Wieferich inert primes, if those primes exist. No conclusion for all such primes is claimed.

When the current largest source prime is at least 11, descend one source as in the earlier proof, giving a unit at the source itself if inert by using it as a lower target. The number of targets does not increase and the loss is at most \(10/11<1\). When the largest source reaches 7 or below, use the joint block of free digits at \(3,5,7\). As before choose the two parities first to pass 2 and leave a unit at 3, while 5 imposes no norm condition. Add a unit target at 7 if it is among the ordinary conditions and not yet a target. It reads only smaller digits. This gives at most eleven targets \(p>3\) at that stage. Larger ordinary conditions can subsequently be repaired with their own primary digits without changing the simultaneous terminal units.

At inert \(p>5\) the block orders, when all its source primes are in this block, are \(u=\operatorname{ord}_p(9)\), \(v=\operatorname{ord}_p(25)\), the odd parts of the full orders. The loss weight is at most \(1/D,\ D=\max(u,v)\). When \(u,v\) are \(3,5,7\)-smooth and \(D\le81\), the complete list \((p,D)\) is
\[
 (7,3),(11,5),(19,9),(31,15),(43,21),(271,27),
 (71,35),(127,63),(883,63),(151,75),(163,81).
\]
For completeness, for each possible \(u,v\) every candidate divides \(\gcd(9^u-1,25^v-1)\); the replay strips all its prime factors exactly and checks the orders. The first possible \(3,5,7\)-smooth odd integer beyond 81 is 105. Thus any eleven target weights sum to at most the sum of the eleven listed weights, \(12499/14175<1\), by replacing omitted low-order weights with no larger ones. This proves simultaneous avoidance. In particular a proposed first blocker at one of the first ten common Wieferich inert primes can be avoided by treating it and all earlier such primes as the targets and separately meeting the ordinary earlier conditions.

## Reusable block and intersection checks

For a more general group of released primary primes, keep the affected ordinary primes within the released block as unit targets. Recursively solve unaffected lower tests, release the block, then repair larger ordinary primes in order. At a fixed lower phase, if the two axis cosets at a target are \(A,H\) of sizes \(u,v\), its true forbidden proportion is
\[
 \frac{|A\cap(n_p-H)|}{uv}.
\]
For \(n_p=0\bmod p\), this is zero or \(1/\operatorname{lcm}(u,v)\) by intersecting cosets. For \(u=v>1\) and nonzero \(n_p\), a full matching is impossible: summing its paired residues would give \(u n_p=0\). So the loss is at most \((u-1)/u^2\). One can explicitly compute the joint survival fraction for a finite core and charge the remaining targets only against that fraction, without assuming their losses are independent.

The exact gcd filter has a stronger version on genuinely exceptional targets: for actual odd orders \(u,v\), simultaneous Wieferich is equivalent to \(p^2\) dividing that gcd, since \(2u,2v\mid p-1\) and the remaining multiplier is a \(p\)-unit. None of the low-order candidates in the table is simultaneous Wieferich. This is a finite table, not a bound on the entire high-order tail.

The second replay panel exceeds one by crude weights but falls below one using an exact finite coset count at 11. It also verifies the effect of one earlier valuation failure at the same actual \(n=1421\), with a different exponent pair producing a true integer witness. The panels use ordinary primes and do not simulate a proved common Wieferich obstruction.

~~~python
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt

D = sorted({3**i*5**j*7**k for i,j,k in product(range(5),range(3),range(3))
            if 3**i*5**j*7**k <= 81})
L = (2,7,11,19,31,43,61,71,109,127,151,163,181,271,883)
assert all(all(p%j for j in range(2,isqrt(p)+1)) for p in L)
seen = set()
for u,v in product(D,repeat=2):
    g = gcd(9**u-1,25**v-1)
    for p in L:
        if g%p == 0:
            seen.add(p)
        while g%p == 0:
            g //= p
    assert g == 1
assert seen == set(L)
S = sorted(p for p in seen if p%4 == 3)

def order(a,p):
    return next(j for j in range(1,p) if pow(a,j,p)==1)

def budget(P):
    return sum(F(1,max(order(9,p),order(25,p))) for p in P)

assert budget(S) == F(12499,14175)
assert all(any(pow(a,p-1,p*p)!=1 for a in (3,5)) for p in S)

T = (43,71,127,883,211,379,631)
assert all(any(order(a,p)%7==0 for a in (9,25))
           and all(order(a,p)%49 for a in (9,25)) for p in T)
assert budget(T+(7,)) == F(62,135)

P = (7,11,19,23,31,43,67,71,127,151,163)
assert all(any(pow(a,p-1,p*p)!=1 for a in (3,5)) for p in P+T)
assert budget(P) == F(157589,155925) > 1
H = {pow(3,j,11) for j in range(5)}
assert H == {pow(5,j,11) for j in range(5)}
assert max(sum((a+b-n)%11==0 for a,b in product(H,repeat=2))
           for n in range(11)) == 3
assert budget(P)-F(2,25) == F(29023,31185) < 1

n = 1421
assert (n-28)%49 == 21
assert n-3**3-5**2 == 37**2 and all((n-52)%p for p in P)

~~~
