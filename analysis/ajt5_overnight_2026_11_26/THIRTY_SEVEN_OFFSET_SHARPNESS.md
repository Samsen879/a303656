# Sharp upper counts for the 37-offset template

This is a finite-phase obstruction for the template of [the uniform 24-center result](https://github.com/Samsen879/a303656/commit/7c9397dbc7aa804dab06753a80a5beb8fe1d7029). It concerns one shared \(C\) and \(5\)-exponents \(D+8i\) for \(0\le i\le36\), with the usual 2-adic test and units required at \(3,7,11\). It does not obstruct a changed menu, extensions in exponent height, or the sum-of-two-squares problem itself.

Take \(n\equiv372715\pmod{658812}\), equivalently \(n\equiv7\bmod84\), \(0\bmod23\), and \(2\bmod11,31\). Set \(R_i=n-3^C-5^{D+8i}\). To pass the test at 2, \(C\) must be even: for odd \(C\), \(R_i\equiv3\bmod4\). If \(C>0\), the unit test at 3 forces \(D\) odd.

For even \(C\) and odd \(D\), at 7 and 23 the number \(-3^C\) is a nonsquare. The powers of 5 in the progression run through exactly the nonsquare coset at each prime, with index periods 3 and 11, respectively. The zero indices thus form one residue class at each period. Each union of two such hit classes has at least 14 indices in this window. The 7-hits must all be removed. If units are required at 23, all 23-hits must also be removed, leaving at most 23. If positive even valuation is allowed there, at most one 23-hit can be retained: two would force \(23^2\mid5^{D+8i}-5^{D+8j}\), which requires \(253\mid i-j\) by the order 506 at \(23^2\).

The remaining case \(C=0\), \(D\) even gives zero-index classes at 11 and 31 with periods 5 and 3, because \(n-1\equiv1\) at both primes. Their union has at least 16 indices. The 11-hits must all be removed; at most one 31-hit can be retained even if positive even valuation is allowed there (order 93 at \(31^2\)). This case has at most 22 survivors.

Consequently the uniform upper bounds are 24 with even valuations allowed at 23 and 23 with units required there, matching the previous construction. The argument is simultaneous in all seeds; later phase steering cannot change the upper bounds. The following checks the small modular data used in the proof.

~~~python
from math import lcm

def order(b, m):
    return next(j for j in range(1, m + 1) if pow(b, j, m) == 1)

assert lcm(84, 23, 11, 31) == 658812
assert [372715 % m for m in (84, 23, 11, 31)] == [7, 0, 2, 2]
assert [order(b,m) for b,m in
        [(5,7), (5,23), (5,11), (5,31), (5,529), (5,961)]] == [6,22,5,3,506,93]
assert all(pow(p-1, (p-1)//2, p) == p-1 for p in (7,23))
for a,b,want in [(3,11,14),(3,5,16)]:
    assert min(sum(i%a == x or i%b == y for i in range(37))
               for x in range(a) for y in range(b)) == want
~~~
