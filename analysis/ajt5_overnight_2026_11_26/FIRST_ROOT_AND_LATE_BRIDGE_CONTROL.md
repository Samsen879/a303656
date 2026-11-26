# A first-root certificate can coexist with real late bridges

For m=5150158917, x=5m+4, the parent d=0,c=1 is genuine: m−4=43487²+57088². Order all active child rows by their numerical root 5^e+3^f. The least root of a true bridge is 248=5+3^5, with x−248=11665²+160046². Of the 20 strictly smaller distinct roots, 34 and 152 are both blocked by the same prime 59 at valuation exactly one. But the same x has a further true bridge at R=5^14+3^21>x/2 with x−R=21660²+93369².

```python
from math import isqrt
m=5150158917
x=5*m+4
T,R=248,5**14+3**21
def norm(n):
    for a in range(isqrt(n//2)+1):
        b=isqrt(n-a*a)
        if a*a+b*b==n:
            return True
    return False
small={5**e+3**f for e in range(5) for f in range(6) if 5**e+3**f<T}
assert len(small)==20 and all(not norm(x-z) for z in small)
assert m-4==43487**2+57088**2 and x-T==11665**2+160046**2
assert x/2<R<x and x-R==21660**2+93369**2
assert all((x-z)%59**2 in range(59,59**2,59) for z in (34,152))
```

More generally, if a fixed completed congruence modulus M coprime to 3 preserves the target's finite even valuations, roots 5+3^(F+j*ord_M(3)) repeat the target residue. As m grows in the class, unboundedly many of those roots eventually activate and survive the same finite local tests. This counting observation makes no claim they are real norms; the late bridge above is a separate actual check. No claim is made about a full-menu obstruction or a bound for all true late bridges.
