# Bounded chart-order diversity costs Ω(H log H) bits; a 16-marker finite replay

This applies to the selected actual chart c=C+16i, d=D+144k inside [ceil(H/32),floor(H/4)]², with N_c,N_d both comparable to H. It is a cover problem for this chart only. A marker is an inert prime p≥7 and its chosen residue modulo p², excluding labels whose residual has exact valuation one there. Call the prime ordinary if at least one of 3 or 5 fails the base-p Wieferich congruence modulo p².

For a_p=ord_p(3^16) and b_p=ord_p(5^144), at fixed k a marker can meet at most one i progression modulo a_p; at fixed i the other axis gives the symmetric bound. The marked fraction is at most min(1/a_p+1/N_c,1/b_p+1/N_d). Assign each marker to one of its axes and group by the chosen effective order r. If a group has m_r distinct primes, they all divide 3^(16r)−1 or 5^(144r)−1 and each is ≥r+1, whence m_r log(r+1)≤C r. The union of that group marks O(1/log r+m_r/H).

Any fixed panel of ordinary primes leaves a positive periodic survivor fraction. Process the primes in increasing order. If p divides the current positive remainder, choose an ordinary axis. Change its exponent by a multiple of a step divisible by the chart stride, the order of the active base modulo p, and the orders modulo q³ for all earlier q<p. That step is prime to p: neither stride is divisible by p≥7, and all prime divisors of the earlier group orders are ≤q<p. The base power of this step generates the principal units modulo p³, so one adjustment makes the remainder p² modulo p³ and preserves every earlier reading. The resulting index class repeats periodically with a panel-dependent period. If chart residues or target residues vary, they have finitely many relevant values for a fixed panel, so one can pass to a constant subsequence.

If a sequence of full covers uses a bounded number of axis/order groups and o(H) distinct markers, pass to a subsequence on which each group order is fixed or tends to infinity. The fixed groups leave a positive periodic fraction, while the drifting groups mark o(1). Contradiction. Thus full ordinary covers with bounded order diversity require Ω(H) distinct markers and Ω(H log H) CRT bits, the latter by the distinct prime product lower bound. This does not yet exclude sublinear bit cost with unbounded order diversity. In such a putative cover o(H/log H) primes are available and, for any fixed η>0, primes with max(a_p,b_p)≥ηH/log H can cover only o(1) of the chart.

## Finite matched control

The code constructs two 1,200-bit targets with the same selected head, mod-25 reading and all specified old inert readings through 137. The positive residual has the form 85q, with q odd and a root of −1 modulo q. Any odd prime dividing q is therefore 1 modulo 4, so 85q is a two-square norm without needing a primality assumption on q. For the other target, 16 ordinary primes cover the entire 32-label selected chart exactly at valuation one. The marker product costs 290 bits and the full matching CRT modulus costs 577 bits (previous 32-marker control: 812 bits). The prime 547 covers three distinct rows of the same column by exact horizontal order seven. No claim is made about labels outside the selected chart.

~~~python
from itertools import product
from math import isqrt, prod

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

grid = list(product(range(51,301,16),(145,289)))
S = [3**c+5**d for c,d in grid]
marks = {
    139:(12,15), 151:(27,), 163:(14,21), 199:(25,28),
    263:(7,24), 271:(0,30), 283:(6,11), 331:(5,8),
    367:(9,20), 547:(3,17,31), 643:(2,19), 827:(1,18),
    1399:(16,23), 3851:(4,26), 4003:(22,29), 4079:(10,13),
}
assert sorted(i for group in marks.values() for i in group) == list(range(32))
assert all(prime(p) and p % 4 == 3 and
           any(pow(a,p-1,p*p) != 1 for a in (3,5)) for p in marks)
assert pow(3,16*7,547) == 1 and pow(3,16,547) != 1
assert [grid[i] for i in marks[547]] == [(67,289),(179,289),(291,289)]

P = [p for p in range(7,138,4) if prime(p)]
W = 1728*17*prod(p**3 for p in P if p <= 75)
u = 2**1195+1109
q0 = 2**1193
q = q0+(u*pow(5,-1,W)-q0)%W+413*W
good = S[0]+85*q
r = pow(3,(q-1)//4,q)
assert r*r%q == q-1 and all((good-S[0])%p for p in P)
assert good%8 == 5 and good%3 != 2 and good%17 == S[0]%17

Q = 25*1728*17*prod(p**3 for p in P)
B = prod(p*p for p in marks)
t = 0
for p,group in marks.items():
    s = S[group[0]]%p
    assert all(S[i]%p == s for i in group)
    m = p*p
    a = next(s+k*p for k in range(p)
             if all((s+k*p-S[i])%m for i in group))
    u = (a-good)*pow(Q,-1,m)%m
    t += u*(B//m)*pow(B//m,-1,m)
bad = good+Q*(t%B)
assert bad > good and bad.bit_length() == good.bit_length() == 1200
assert (bad-good)%Q == 0
assert B.bit_length() == 290 and (Q*B).bit_length() == 577
for p,group in marks.items():
    for i in group:
        R = bad-S[i]
        assert R > 0 and R%p == 0 and R%p**2 != 0
~~~
