# First rank thirteen is excluded through seventeen sources

Use the same fixed target, c and parity of d, a passing two-adic class, and muted rows 3,31,71,5167,19531 of the previous first-pivot analysis. Higher exact linear contractions retain at most one cylinder per original rigid source. This note concerns first rank 13 only.

Rank 13 is split and has no native veto. With t sources reading it, a complete fiber needs t>=13, leaving at most four lower-only terms. A deeper frontier requires 25 sources, so any witness is flat and needs all 13 first positions. At least 26−t>=9 are singleton. Any chosen singleton guard G is necessary for every flat.

Use the 72/135 window W of two first ternary branches and four first quinary branches outside the native 7 and 11 guards. On this window no native 7 or 11 guard is active. Outside the terms in the overcover G plus the lower-only guards that are blind to both 7 and 11, at most five surviving terms remain. Their relative coverage of the free (7,11) fiber is at most 5/7, so they cannot close it. The four lower-only blind terms cost at most 24 units of 1/135: the fixed row-19 ninth of cost 12, plus at most four each for the other three.

A 7- and 11-blind singleton costs more than nine units on W only with lower depth pair (0,0), (1,0), (0,1) or (2,0). Its raw or least-helper order divides twice its retained odd support. Exact primitive norm factorizations below show that among the relevant orders divisible by 13 there are only eight inert heads. They are all ordinary, and each has one position at this target and parity. Among relevant orders not divisible by 13, only row 19 can supply a large guard: rows 7 and 11 are unprocessed and the other small heads are muted. A guard inherited through 19 has exactly the same ninth as the exceptional lower-only charge.

Nine distinct singleton positions therefore force a guard G of effective mass at most nine, or a guard from the row-19 ninth. The former case leaves at least 72−9−24=39 units; the latter charges row 19 once and leaves at least 72−12−4*4=44 units. Each surviving lower pair lifts through 7, 11 and 13 and then through the exact higher history. The replay proves the head inventory and an arithmetic lower-guard control with a synthetic top assignment. The aggregate budget-17 theorem still requires checking the other ranks and modulus bridge together.

```python
from functools import cache
from math import gcd, isqrt, prod

@cache
def phi(w):
    a, r = divmod(5**w-1, prod(phi(d) for d in range(1,w) if w%d==0))
    assert r == 0
    return a

cert = {1034150930241911:(472640197,), 472640197:(331,191),
        608459012088799:(95393,82021), 43236180703:(1877,157)}

def prime(q):
    if q not in cert:
        return q>1 and all(q%d for d in range(2,isqrt(q)+1))
    ps = cert[q]
    f = prod(ps)
    return ((q-1)%f==0 and f*f>q and all(map(prime,ps))
            and pow(2,q-1,q)==1
            and all(gcd(pow(2,(q-1)//p,q)-1,q)==1 for p in ps))

rows = [(13,(),17409,1450), (26,(5227,38923),1,0),
        (39,(79,608459012088799),1,0), (78,(),181873380,194627809),
        (65,(131,1034150930241911),109022890,95395059),
        (130,(),17019632986472559,63025587648511280),
        (117,(),14102652216932230673717400,3343572777768341194340999),
        (234,(40483,43236180703),344383557815701918,57875985484340415)]
for w,qs,a,b in rows:
    assert phi(w)==prod(qs)*(a*a+b*b) and gcd(a,b)==1
    for q in qs:
        assert prime(q) and q%4==3 and pow(5,w,q)==1 and pow(5,w,q*q)!=1
        assert all(pow(5,d,q)!=1 for d in range(1,w) if w%d==0)
assert sum(len(qs) for w,qs,a,b in rows)==8 < 26-17
assert min(72-9-(12+3*4), 72-12-4*4)==39

n = 4+124780301653257289028475**2+79104957347947814158856**2
for q,w in ((3,2),(31,3),(71,5),(5167,18),(19531,7)):
    assert all((n-3-pow(5,d,q))%q for d in range(0,2*w,2))
W = {d for d in range(0,270,2) if d%3!=2 and d%5!=4}
holes = set()
for d in W:
    assert all((n-3-pow(5,d,q))%q for q in (7,11))
    lower = any((n-3-pow(5,d,q))%q==0 for q in (19,163,271,487))
    assert lower == (d%9==4 or d%27 in (1,7,10))
    if not (lower or (d%3==0 and d%5==0)):  # Synthetic flat guard.
        holes.add(d)
assert len(W)==72 and len(holes)==39
print("PASS")

# Check the mass classification separately in normalized units.
from fractions import Fraction as Q
from itertools import product
above=[]
for a,b in product(range(4),repeat=2):
    bound=(Q(2,3) if a==0 else Q(1,3**a))*(Q(4,5) if b==0 else Q(1,5**b))
    if 135*bound>9: above.append((a,b))
assert above==[(0,0),(0,1),(1,0),(2,0)]
print("Blind-guard mass classification independently checked")
```
