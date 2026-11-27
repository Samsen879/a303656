# Parent norm compatibility and an endpoint false positive

At d=0,r=4 the intended parent residual is m−4=(x−24)/5 for x=5m+4. On the width-one order chain with first prime 271 of order 30 and subsequent primes having order twice the preceding prime, take F=C−29. At each nonfinal forcing prime p whose order divides C, the short-side constraint has x≡5+3^F mod p. Thus if the parent also vanished there, p would divide 19*3^29−1. Its inert prime divisors are only 71 and 17971, of orders 35 and 17970 respectively. Neither is a possible chain member: neither is 271, and the former order is odd while the latter is twice the composite number 8985. The parent residual is therefore a unit at these forcing primes. This is a local compatibility test, not by itself a simultaneous integer-square construction.

On the two-prime chain 271,1627, F=8101, compare three possible endpoint residues for x modulo q³, q=1627: 0, 24, and 24+q. The child residuals at f=F are units in all three cases. The parent residual is a unit in the first, can be a zero-class norm of exact valuation 4 in the second (use local coordinates (q²,0)), but is forced to have valuation 1 in the third. The last one is a false positive for inferring a true parent from the two-child parity test.

```python
from math import isqrt
def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))
assert 19*3**29-1 == 8*71*1481*17971*86257
assert all(prime(p) for p in (71,1481,17971,86257))
for p,n,fac in [(71,35,(5,7)),(17971,17970,(2,3,5,599))]:
    assert pow(3,n,p)==1 and all(pow(3,n//q,p)!=1 for q in fac)
q,F=1627,8101
for x in (0,24,24+q):
    assert all((x-a-pow(3,F,q))%q for a in (1,5))
assert (24+q-24)%q**3 == q
```
