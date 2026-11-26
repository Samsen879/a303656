# An exact terminal projection test for finite single-witness blocking

This refines the [finite-obstruction characterization](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md) for the growing exponent box. At an inert prime \(q>5\), fix all earlier local observations, and assume the old head has a surviving phase. Let \(U_q\subset\mathbb F_q\) be all values of \(3^c+5^d\bmod q\) on the old survivors, not its image on any one selected branch. Only a common Wieferich \(q\) can first block. For such a prime, the conditional probability of first blocking at \(q\) is positive **if and only if \(U_q\) is a singleton**. This states a test for each terminal prime and compatible head, not that one exists.

## Terminal lifts

With at least two distinct shift values, one is different from \(n_q\bmod q\) and passes at \(q\). Now suppose \(U_q=\{s\}\) and write \(\lambda=\min(v_q(3^{q-1}-1),v_q(5^{q-1}-1))\ge2\). Any unit power of either base agrees modulo \(q^\lambda\) with its unique torsion lift \([u]\) of the first digit \(u\in\mathbb F_q^\times\). For an integer representative \(u\) it is \(u^{q^{\lambda-1}}\bmod q^\lambda\): its residue is \(u\) and its \((q-1)\)-st power is 1. The \(q\)-primary indices are unread by all earlier tests. At a given phase they can change the shift throughout its ball modulo \(q^\lambda\), by the fastest unit axis. Thus this phase is killed exactly if its locked residue difference has odd valuation below \(\lambda\).

For \(s\ne0\), let \(D\) be the number of distinct old-survivor shift lifts modulo \(q^2\). The \(q-2\) ordered nonzero representations \(u+v=s\) have one diagonal, so \(D\le(q-1)/2\) by symmetry of \([u]+[v]\). If \(n_q\bmod q^2\) lies above \(s\) but misses the \(D\) lifts, every candidate is killed at valuation one. Hence
\[
 (q-D)/q^2\ \le\ \Pr(q\text{ first blocks}\mid\text{old head})\ \le\ 1/q,
\]
and the lower bound is the exact probability for \(\lambda=2\). If \(s=0\), all lifts to depth \(\lambda\) agree with zero since \([u]+[-u]=0\). The conditional blocker then consists exactly of \(n_q\) with odd valuation below \(\lambda\). The next digit cannot automatically break a genuine zero-sum cancellation.

## A reduced exact enumeration of the old phases

For each axis \(a\in\{3,5\}\), initialize the count \(d_{r,a}\) of retained \(r\)-primary digits to the \(r\)-valuation of \(\operatorname{ord}_q(a)\). Work downwards through the earlier odd inert primes \(p<q\), including 3 (where only the 5-axis is a unit). At \(p\) set
\[
 k_p=\min_{a:\,p\nmid a}\bigl(d_{p,a}+v_p(a^{p-1}-1)\bigr).
\]
If \(k_p=1\), no test at \(p\) need be stored: an ordinary axis with no retained \(p\)-digit fills a residue ball at depth one and can make any collision good without changing higher-prime tests. If \(k_p\ge2\), store the test and enlarge the retained low digits of each unit axis to include the factors of \(\operatorname{ord}_p(a)\). Those factors are at smaller primes, so a single descending pass suffices. Earlier common Wieferich tests are always retained. Split primes have no restriction.

Now enumerate the retained digits. At each stored odd test, the old observation must give even valuation below \(k_p\), or the difference must vanish at depth \(k_p\). At 2 only parities need be reserved: every odd inert order has at most one factor of 2. For odd \(n_2\), the first-axis parity must make the residual \(1\bmod4\); for even \(n_2\), among the four parity pairs just the one yielding \(6\bmod8\) cannot be repaired. With fixed parities \(5^d\) can move through its residue ball modulo 8, giving a good higher lift whenever the residual is \(0\bmod8\) or \(4\bmod8\). Complete any parity not already retained. Then each passing enumeration extends to a positive-measure old survivor set: remaining primary digits fix the odd valuations using one fastest free axis at each retained prime, and repair skipped tests in ascending prime order without changing retained digits. The resulting output at \(q\) is precisely \(U_q\).

One simple sufficient check is any terminal digit not read by the retained old tests; varying that digit alone changes the output. For the zero-sum branch, a surviving phase with the same quadratic character on the two base powers excludes cancellation, since \(-1\) is a nonsquare at inert \(q\). These criteria still need a proof covering all possible heads and primes.

## Restricted-branch countercontrols

At terminal \(103951\), a selected old 11-variant family leaves one survivor, but a different legal phase has a second terminal value. At terminal \(139\), a whole selected line of 23 old survivors cancels identically, but a different legal phase gives a nonzero terminal value. These are actual 3,5 order and valuation computations; the two terminal primes used here are ordinary, not common Wieferich examples.

~~~python
from itertools import product
from math import isqrt

def s(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

def order_is(a,p,d,factors):
    return pow(a,d,p)==1 and all(pow(a,d//r,p)!=1 for r in factors)

q,n = 103951,129
assert all(q%r for r in range(2,isqrt(q)+1))
assert order_is(3,q,9450,(2,3,5,7))
assert order_is(5,q,51975,(3,5,7,11))
assert (pow(3,10,121),pow(5,10,121)) == (1,78)
assert n%12==9 and n-s(1,1,1331)==121
assert [y for y in range(11) if (n-s(1,1+9450*y,121))%121==0] == [0]
assert (n-s(1,2,11))%11 and s(1,2,q)==28
assert pow(3,q-1,q*q)!=1 and pow(5,q-1,q*q)!=1

r,q,n = 23,139,121965
assert n%12==9
line = [(x,y) for x,y in product(range(r),repeat=2)
        if (n-s(1+66*x,250+66*y,r*r))%(r*r)==0]
assert line == [(x,y) for x,y in product(range(r),repeat=2) if x==15*y%r]
assert {s(1+66*x,250+66*y,q) for x,y in line} == {0}
assert pow(5,66*r,q)==1
for x,y in line:
    assert any((n-s(1+66*x,250+66*(y+r*j),r**3))%r**3
               in range(r*r,r**3,r*r) for j in (0,1))
assert (n-s(1,1,r))%r and s(1,1,q)==8
assert (pow(3,q-1,q*q),pow(5,q-1,q*q)) == (6256,13762)

~~~
