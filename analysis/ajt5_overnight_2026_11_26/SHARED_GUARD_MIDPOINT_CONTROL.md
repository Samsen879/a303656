# Shared guards charge distinct incoming neighbors, not flow units

In a fixed descending order graph, choose one allowed descending successor for each used contacting vertex until reaching a free coordinate. A vertex emits its own forbidden residue set exactly once, no matter how many roots reached it. Thus the sufficient capacity condition at coordinate r is that its number of distinct immediate predecessors is at most floor((r^j−1)/2), where each may ban at most two residues mod r^j. After choosing remaining allowed coordinate values, the proof of DESCENDING_ORDER_SHARED_GUARDS.md completes the unused ordinary primes. The same argument applies with fixed coordinates by treating their already forbidden values separately, not as freely selectable.

For a fixed set S of vertices that must emit a constraint, permit successors only in S or among free terminals. A capacity-respecting successor assignment exists iff every X⊆S has successors whose total capacity is at least |X|, by Hall's theorem after replicating successor slots. Being strictly descending makes every assignment reach terminals. This tests the given sufficient certificate, not actual parity feasibility.

A real fixed-phase countercontrol is the graph 20771,40487→31→3, after freezing t≡0 mod L, L=5*67*653. Two flow units cannot pass the capacity-one coordinate at 3, but 31 emits only one guard there, and t=L works. Locking t≡0 mod 3L blocks that guard too, but then t=3L works, with a literal valuation 2 at 31 in the c=2 row. The freedom at the deep ordinary root is essential. Without fixing phase or depth, the alternative private factors are available and this example is not a separation.

```python
q,p,L = 20771,40487,5*67*653
a,M = 0,1
for mod,r in [(63,2), (31**3,9+pow(25,3*L,31**3)+31**2),
              (q*q,10+q), (p*p,10+p)]:
    a += M*((r-a)*pow(M,-1,mod) % mod)
    M *= mod
n = a + M*25**(3*L+1)
assert n%63 == 2 and 4*max(81,25**(3*L)) < n
assert L%3 == 1 and L%31 == 19 and (3*L)%31 == 26
assert all((n-10)%(s*s) == s for s in (q,p))

P = (3,7,31,q,p)
assert all((n-h-25**L)%s for h in (9,81) for s in P)
assert (n-9-25**(3*L)) % 31**3 == 31**2
assert all((n-h-25**(3*L))%s
           for h in (9,81) for s in P if s != 31 or h == 81)
assert {t%31 for t in range(0,93,3)
        if (n-9-pow(25,t,31**2))%31**2 == 0} == {26}
```

This proves neither an arbitrary finite zero nor the converse to the guard criterion. No novelty claim is made.
