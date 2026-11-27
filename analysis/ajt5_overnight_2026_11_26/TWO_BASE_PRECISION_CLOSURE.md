# Exact two-base precision closure for an all-exponent modulus

Fix M and work in the exponent range c>=v_3(M), d>=0. Keep the binary and ternary parts and discard split factors. For every inert prime p>3 with original precision e_p, write w_a(p)=ord_p(a) and s_a(p)=v_p(a^w_a(p)−1) for a=3,5. Process these primes in decreasing order. Set the new precision e'_p to the minimum of e_p and the two numbers
s_a(p) + max_{q>p, e'_q>=2} v_p(w_a(q)).
The empty maximum is zero. Drop rows of precision at most one. The resulting divisor of M has exactly the same feasible target integers in the stated exponent range.

To lower a row at p, adjust the chosen exponent by nonnegative multiples of the lcm L of its own order modulo p and the full orders at every other retained row. The other residues remain fixed (the nonunit power of 3 modulo the ternary factor is already zero). Only larger inert readers can contribute p to L, because orders at their prime powers add powers of their own prime only, and the binary and ternary rows cannot contribute this p. The adjusted power runs through exactly its lift ball modulo p^e, with precision K=min(e,s_a(p)+v_p(L)), by LTE. A residue with even valuation below K passes in all lifts; zero modulo p^K can be lifted to zero modulo p^e; an odd valuation below K persists in all lifts. This proves equivalence for each elimination on the same target, and reversing the process recovers simultaneous full-precision feasibility. Base-5-only changes keep small-c slices too; using base 3 requires a separate small-c check.

Thus any retained precision deficit above s_a(p) needs a larger retained reader in that base's order graph. Following needed edges eventually ends at an inert row exceptional to both bases, and paths may switch bases. At square precision 7 and 19 need readers in each graph; 11 already has intrinsic base-3 depth two but still needs a base-5 reader. This is independent of a small-source budget. It does not force two paths to meet or exclude all possible obstructions.

The arithmetic control shows a panel where reader 71 freezes the needed base-3 digit at 7 but not the corresponding base-5 digit, and gives an actual mixed-axis full-precision modular square witness at the same target. The replay is local; no new density or pointwise theorem follows.

```python
from math import lcm, prod

def order(a,m):
    return next(k for k in range(1,m+1) if pow(a,k,m)==1)

n = 6714892523756
E = {2:4, 3:2, 7:3, 11:2, 19:2, 71:2}
def r(p,c,d):
    m = p**E[p]
    return (n-pow(3,c,m)-pow(5,d,m)) % m

assert [r(p,7,0) for p in (7,11,19,71)] == [7,11,19,0]
assert [order(a,71**2) for a in (3,5)] == [2485,355]
assert pow(3,5,121)==1 and pow(3,5,1331)!=1
assert pow(5,5,121)!=1
L = lcm(order(3,16),order(3,7),order(3,19),order(3,71**2))
assert L==89460 and pow(3,L,49)==1
assert (n-pow(3,7,49)-1)%49==7

assert (10771-7)%36==0 and r(7,10771,0)==245 and r(19,10771,0)==0
c,d,x = 5635987,54877320,1208435214448
M = prod(p**e for p,e in E.items())
assert (n-pow(3,c,M)-pow(5,d,M)-x*x)%M==0
print("PASS")

# Verify exact lift balls by enumerating two independent actual source steps.
for a,p,e,L0,K in ((3,7,3,36,1),(5,11,2,5,1),(3,7,3,89460,2)):
    m=p**e
    assert {pow(a,L0*j,m) for j in range(p**e)}==set(range(1,m,p**K))
print("Exact lift balls independently checked")
```
