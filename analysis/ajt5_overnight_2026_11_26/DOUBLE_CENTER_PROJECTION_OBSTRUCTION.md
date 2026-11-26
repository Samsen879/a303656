# A joint center cannot replace two independent center supports

Set t=d mod 19 and s=d mod 43 in the fixed chart of JOINT_NATIVE_PREFIX_CERTIFICATE.md. In the ternary phase x=0 mod 9, the native modulo-19² veto leaves the entire strip t=0 with s free. In x=1 mod 3, the native modulo-43² veto leaves s=22 with t free. The two phase guards are disjoint. A single simultaneous center restriction (t,s)=(0,22) removes only one cell of either strip. Fixing s=22 makes it appear to close the first strip, and fixing t=0 makes it appear to close the second, but the two conditional projections cannot both be used when both axes are free. This statement concerns a single source supported on the one center pair; sources with separately justified releases or multiple pieces require a different analysis.

A direct inert reader Q of both centers needs 817 dividing ord_Q(5) and hence Q=1635 mod 3268. Its log residue must be 323 mod 817, consistent with all other locks; a first-prefix support on both coordinates has depth one on both. Those congruences alone provide no rigid source. A genuinely rigid row must also meet its valuation and target requirements; joint rigidity in both bases requires the corresponding conditions for base 3.

The replay adds three ordinary readers by CRT at one represented target. With their own digits frozen off center, 191 and 9547 induce the two separate center strips; 8171 instead reads the joint center with order 4085. The two separate readers close their claimed phases, whereas the joint reader alone leaves a survivor in every ternary phase with both native digits free. With private digits released, each new reader is ordinary and can take its own center. No common Wieferich source, global exclusion, or change in density is claimed.

```python
from itertools import product
from math import isqrt, prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

U = 1749240030127890765912351734436595992951490159
V = 1808434766219862061671534508108331483094094788
M = 12*7*31*71*5167*19531*prod(p*p for p in
                            (19,43,11,1171,251,211,20771))
R = [(191,19,(19,),0,2,34649), (9547,86,(2,43),22,0,19999341),
     (8171,4085,(5,19,43),6042,0,21270034)]
u = crt([(U%M,M)]+[(a,q*q) for q,_,_,_,a,_ in R])
v = crt([(V%M,M)]+[(b,q*q) for q,_,_,_,_,b in R])
n = 28+u*u+v*v
for q,w,fs,e in [(19,9,(3,),0),(43,42,(2,3,7),22)]+[r[:4] for r in R]:
    assert q%4==3 and all(q%j for j in range(2,isqrt(q)+1))
    assert pow(5,w,q)==1 and all(pow(5,w//p,q)!=1 for p in fs)
    assert pow(5,w,q*q)!=1 and (n-3-pow(5,e,q*q))%(q*q)==0

def veto(q,d):
    r = (n-3-pow(5,d,q*q))%(q*q)
    return r!=0 and r%q==0

def safe(off):
    lock = [(0,2),(2,5),(1,7)]+[((e+b)%q,q)
                                for (q,_,_,e,_,_),b in zip(R,off)]
    out = [set() for _ in range(9)]
    for x,t,s in product(range(9),range(19),range(43)):
        d = crt(lock+[(x,9),(t,19),(s,43)])
        if not any(veto(q,d) for q in (19,43,191,9547,8171)):
            out[x].add((t,s))
    return out

A,B = safe((1,1,0)),safe((0,0,1))
assert {x for x,S in enumerate(A) if not S}=={0,1,4,7}
assert all(B)
assert {x for x,S in enumerate(B) if all(s!=22 for t,s in S)}=={0}
assert {x for x,S in enumerate(B) if all(t!=0 for t,s in S)}=={1,4,7}
print("PASS")

# Check individual induced sets and concrete escapes with both digits free.
assert {i for i,F in enumerate(safe((1,0,0))) if not F}=={0}
assert {i for i,F in enumerate(safe((0,1,0))) if not F}=={1,4,7}
assert (0,23) in B[0]
assert all((1,22) in B[i] for i in (1,4,7))
assert crt([(0,19),(22,43)])==323
print("Individual arrows and simultaneous-free escapes independently checked")
```
