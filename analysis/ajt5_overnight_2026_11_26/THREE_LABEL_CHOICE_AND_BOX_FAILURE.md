# Three-label choice and the active-box boundary

Use F_i=n−3^c−5^(d+i), i=0,1,2, and initial exponent classes c mod H3 and d mod H5. If the finite inert panel includes 3, assume these classes allow an initial choice with c≥3 and all three valuations at 3 equal to 0 or 2, fixing the needed d phase mod 18. With no seed this is possible: if n is a unit choose parity of d giving labels 0 and 2 units, and adjust via the order of 5 mod 27 to make the remaining label have exact valuation 2. If 3 divides n they are all units. At an inert p>3, call a first digit available if one of bases b=3,5 has p∤H_b and v_p(b^ord_p(b)−1)=1. If at most f primes lack this property, there are common exponents for which at least 3−f chosen labels pass that whole panel.

Process primes in increasing order. Earlier prime-power order data have no p factor. After setting the mod-p phase, the three powers of 5 are distinct at this p (an inert p>3 cannot divide either 5−1 or 5²−1). Thus at most one current label needs repair. A free ordinary first digit reaches depth two and the next digit makes its valuation exactly two, preserving the old data. If no first digit is available, discard at most that one label. The choices preserve the same exponent pair. This leaves an activation constraint at any fixed n and does not guarantee an actual norm.

The strict box 3^c,5^d<n/4 can fail even with no seed: n=3920 has all 35 box residues covered by the actual odd valuations below. Each of the 14 primes is mandatory for this box, as it is the sole inert odd prime for at least one row. Cutting off at floor(log2 n)=11 leaves 13 survivors, none an actual norm. Outside the box there is the true representation n=13²+25²+1+5^5. Thus neither the box failure nor the finite survivors decide the original problem.

```python
from math import isqrt

n = 3920
P = {3,7,11,19,23,31,67,823,919,967,1283,1583,1607,1907}
Q = [p for p in range(3,n,4)
     if all(p % k for k in range(2,isqrt(p)+1))]

def odd(r,p):
    v = 0
    while r % p == 0:
        r //= p
        v ^= 1
    return v

S = [{p for p in Q if odd(n-3**c-5**d,p)}
     for c in range(7) for d in range(5)]
assert all(s & P for s in S)
assert {next(iter(s)) for s in S if len(s)==1} == P
assert sum(not (s & {3,7,11}) for s in S) == 13
assert n == 13**2 + 25**2 + 3**0 + 5**5
```
