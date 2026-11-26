# Exact fixed-divisor gcd and a compatible translation

Suppose an anchored exponent rectangle contains the starting cell and both first axis neighbors, with steps S,T. The gcd of all remainders is exactly
G=gcd(n-3^c0-5^d0, 3^c0(3^S−1), 5^d0(5^T−1)).
The three first cells show that every common divisor divides these quantities, and geometric series show the converse.

If a second rectangle has the same steps and starting d displaced by E, the gcd across the two is exactly gcd(G,5^d0(5^E−1)). Conversely, if E itself is used, additional displacements by multiples of E cannot reduce that gcd. One compatible translate removes every common prime q other than 5 for which ord_q(5) does not divide E. The gcd formula needs no factorization.

At the unchanged target of OMITTED_PRIME_PREFIX_OBSTRUCTION.md, G=463. The original restrictions forcing step orders to be powers of three at the five nonzero readers give minimum steps 2310 and 462, so a same-origin sublattice obeying them still has 463 as a common divisor. Relax the factor 7 of the 5-axis phase at reader 127, while retaining the stated lower anchors and raw phases at the other checked readers. The required d displacement is 1782, preserving the absolute ternary slope modulo 81. The displaced 3-by-6 prefix has 12 panel survivors, and every remainder is 137 modulo 463. The old prefix has nine survivors. The remainders at (31,1240) and (2341,2560) are positive and coprime, and pass the original panel. That eliminates a shared fixed-divisor obstruction, not the possibility of different odd-valuation divisors at the two cells. No two-square representation or change to global conclusions follows.

```python
from itertools import product
from math import gcd, lcm, prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j)+5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,p) for p in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M

def order(g,p):
    return next(k for k in range(1,p) if (p-1)%k==0 and pow(g,k,p)==1)

def away3(k):
    while k%3 == 0:
        k //= 3
    return k

assert [lcm(6,*(away3(order(g,p)) for p in P))
        for g in (3,5)] == [2310,462]
G = gcd(n-3**31-5**778,3**31*(3**2310-1),5**778*(5**462-1))
assert G == 463 and order(5,G) == 462
E = lcm(2,81,*(order(5,p) for p in (19,199,271,4159,1783,5023,163)))
assert E == 1782 and lcm(E,order(5,127)) == 12474
assert gcd(G,5**778*(5**E-1)) == 1
assert pow((n-pow(5,778+E,127))*pow(3,-31,127),3,127) == 16

def R(c,d):
    return n-3**c-5**d

def prefix(b):
    return [R(31+2310*x,b+462*y) for x,y in product(range(3),range(6))]

old,new = prefix(778),prefix(778+E)
assert 3**4651+5**4870 < n
assert [sum(all(r%p for p in Z+P) for r in L) for L in (old,new)] == [9,12]
assert all(r%463 == 137 for r in new)
a,b = R(31,1240),R(2341,2560)
assert all(a%p and b%p for p in Z+P) and gcd(a,b) == 1
assert a%463 == 0 and a%463**2 != 0
print("Two active prefixes with coprime panel survivors")

assert gcd(*old)==G and gcd(*(old+new))==1 and gcd(*new)==1
assert all((778+E+462*y)%81==(778+462*y)%81 for y in range(6))
print("Both rectangle gcds and anchor preservation independently checked")
```
