# A capacity criterion for descending shared-order guards

Use the same seeded rows and contacts as DESCENDING_ORDER_SHARED_GUARDS.md. Choose a depth j_r at each prime coordinate r. Admit an edge p→r when r^(j_r) divides ord_p(25), and give r incoming capacity floor((r^(j_r)−1)/2). A coordinate is a terminal if it is outside the panel or has no contact. Add one source unit at the outgoing side of each contacting nonregular panel prime. If all units can reach terminals by integral flow through vertex capacities, the two rows have a common local survivor.

Every edge goes strictly down. At each used nonterminal retain just one positive-flow outgoing edge; every source still follows a descending path ending at a terminal. An incoming predecessor bans at most two residues at the coordinate it points to. The number of distinct remaining predecessors is at most the original incoming flow, so the capacity bounds their total bans strictly below the number of coordinate residues. Keep one available residue at each used coordinate and finish ordinary primes in increasing order as in the earlier proof. This is sufficient, not necessary; a unit-flow model may overcount paths that could merge.

There are grows-with-panel examples using real orders. For inert prime ell≥313, Phi_ell(25) is 3 mod 4 and has an inert divisor. Its divisors here have exact order ell (the exceptional divisor ell would require 25≡1 mod ell). An inert prime of order ell is at least 2ell+1>625. Fewer than ell/2 distinct inert primes can therefore have this order, since their product divides Phi_ell(25)<25^ell. All may use the coordinate ell as a terminal. Select successive ell larger than the preceding 25^ell to separate the groups and their terminals. This does not assert infinitely many nonregular primes.

A greedy first-factor projection can fill a coordinate even when no true local obstruction exists, as the following exact replay shows. Raising precision to 27 (or changing the chosen factors) avoids the failure.

```python
p,q = 40487,1645333507
a,b = 116963,119314
r = (9 + pow(25,a,q*q) + q) % (q*q)
N,M = 0,1
for d,z in [(63,2),(31**3,10+31**2),(p*p,10+p),(q*q,r)]:
    N += M*((z-N)*pow(M,-1,d) % d)
    M *= d
n = N + M*25**(b+1)
assert n%63 == 2 and 4*max(81,25**b) < n

def odd_one(x,p):
    return x%p == 0 and x%(p*p) != 0

assert odd_one(n-10,p)
assert odd_one(n-9-25**a,q) and odd_one(n-81-25**b,q)
assert {0,a%3,b%3} == {0,1,2} and {a%27,b%27} == {1,26}
assert {(9+25**j)%31 for j in range(3)} == {3,10,14}
assert {(81+25**j)%31 for j in range(3)} == {13,20,24}
assert n%31 == 10
assert all((n-h-625)%s for h in (9,81) for s in (3,7,31,p,q))
```

This concerns finite local parity, not activated witnesses for all integers or a full norm theorem.
