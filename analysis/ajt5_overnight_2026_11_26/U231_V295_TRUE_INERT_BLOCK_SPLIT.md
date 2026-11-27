# Two individually decisive inert factors can hide in a 1-mod-3 block

The actual positive half J=(5^231+3^295)/8 contains two odd, exact unitary divisors p=72197823963870893 and q=778603984326529553, each 2 mod 3. Either alone certifies some inert prime of odd valuation, with no primality assumption needed for the rejection verifier. The negative half need not be decided to veto this label. The veto persists under simultaneous cubing because the corresponding odd cubic quotient is itself an Eisenstein norm and is coprime to the old odd half outside 3.

Their product pq is 1 mod 3, so the coarse residue test at a combined block can fail to identify the obstruction. On the complete J, a scalar cube-root gcd gives 1 when using the tested base and exponent. With the same derived exponent in the quadratic trace recurrence, offsets g,g+1,g+6 give gcds pq,p,q respectively. This verifies the splitting of a true lump on the original integer, rather than treating residue 1 as a positive norm certificate. The exponent is chosen from discovered blocks, not a generic factor-discovery guarantee.

The remaining unresolved U231 labels are V=13 and 31. No new phase is established.

```python
from math import gcd, lcm

A, S = 5**231, 3**295
J = (A+S)//8
p, q = 72197823963870893, 778603984326529553
assert 8*J == A+S and J%2 == 1 and (p*q)%3 == 1
for d in (p, q):
    assert J%d == 0 and gcd(d, J//d) == 1 and d%3 == 2 and d%2 == 1

g = pow(5, 148, J)*pow(-3, -189, J)%J
E = lcm((p+1)//3, (q+1)//3)
z = pow(g, E, J)
assert gcd(z*z+z+1, J) == 1

def trace_block(k):
    T = 2*(k*k-3)*pow(k*k+3, -1, J)%J
    a, b = 2, T
    for bit in bin(E)[2:]:
        c, d, f = (a*a-2)%J, (a*b-T)%J, (b*b-2)%J
        a, b = (c, d) if bit == "0" else (d, f)
    return gcd(a+1, J)

assert [trace_block(g+j) for j in (0, 1, 6)] == [p*q, p, q]
```
