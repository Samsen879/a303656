# Uniform 25-center finite-phase coverage

This note closes the three explicitly identified target strata of [the previous odd-D certificate](https://github.com/Samsen879/a303656/commit/98cb1297bd194ff9b3920fd4017bf87131251586); the other two residues modulo 3 were handled by [the even-D certificate](https://github.com/Samsen879/a303656/commit/371f755a6d2e41615a12dd1c97769d8695c222db). The new retained set changes the genuinely shared head pattern; it does not enlarge an exponent search. The resulting theorem concerns an arbitrary prescribed **finite** panel and contains no logarithmic exponent-height bound.

Independent replay verified all six initial capacities, the three disjoint 271 readings, 110 exact order-eleven projected masks with minimum seven, all gap factors and restoring budgets, and four complete native ordinary-panel controls (including the exact stress lift at 251). The order-three repair capacity at 163 and 487 uses the fact that both built exponents remain odd: both 3 and 5 are nonsquares there, so the coefficient ratio of their powers is a square. At every ordinary repair on a prescribed finite panel, process primes in increasing order and preserve previous residues modulo their cubes. The prospective next prime cannot divide any earlier prime’s lock \(p^2(p-1)\). If the next prime divides the ordinary horizontal period, it must occur in the factored period list, where base 5 is certified non-Wieferich and can use the vertical period instead; the small guarded prime 31 is already a unit. For the final 2-adic repair use the listed \(K_2\) enlarged with the full panel locks. Its 2-adic valuation is one, since \(p-1\) has valuation one at each odd inert prime.

With the inherited non-reuse argument, a finite obstruction that kills all centers after repairing the ordinary rows must use at least 25 distinct common-Wieferich primes. This conclusion is about finite obstructions in the construction. It does not certify that any of the 25 actual remainders at a prescribed input is positive or a sum of two squares.

**The three residual classes are closed.** A new retained-label set gives 25 finite-phase centers for every \(n\equiv84037,628273,764332\pmod{1088472}\), using positive \(C\) and odd \(D\). Together with the previous strata, this completes the uniform 25-center finite-phase theorem for \(n>1\).

### A different head pattern

Use the exponents \(D+8j\), with
\[
I'=\{0\le j\le38:\ j\not\equiv1\bmod5,\quad
j\not\equiv1\bmod9,\quad j\bmod11\notin\{6,10\}\}.
\]
There are exactly 25 labels. The starting phase is \(C=11,\ D=V+33\), where \(V=36100888223400\).

The operation is to **place the \(11\)- and \(19\)-hits in discarded index classes before choosing the retained labels**. Here both are placed in class \(1\), modulo \(5\) and \(9\) respectively. The same seed clears \(7\) and \(31\). The two blank classes mod \(11\) leave room to clear \(23\), including when \(23\mid n\). The guard at \(3\) holds since \(C>0\) and \(D\) is odd.

The only odd gap above 35 in the span would be 37. Both potential pairs are absent because labels \(1\) and \(37\) are discarded. Thus all gap odd parts are at most 35, and the earlier squarefree factor certificate gives the same common-Wieferich non-reuse bound.

### Exact phase budgets and restoration

Use \(E=6284520,\ J=3999240,\ P=1629320\).

1. On the 49 cells \((C+xE,D+yE)\), the maximum forbidden counts at \(43,71,127,211,379,631\) are respectively **\(13,14,6,2,6,2\)**. Their sum is 43, so a cell survives.
2. Add \(9sP\) to \(D\), with \(s=0,1,2\). The three repeated-value sets at \(271\) are pairwise disjoint, so at most one choice fails. This preserves the six earlier rows.
3. Add \(zJ\) to \(C\) and \(hJ\) to \(D\) independently. The exact masks at \(23,67,199\) leave at least **seven horizontal digits \(z\)** with some usable \(h\). Row \(4159\) forbids at most five \(z\)-digits. Thus one pair survives with \(23\) a unit at every center.

The reverse restoration costs two of three digits at each of \(163,487\), at most eleven of 23 at the pair \(47,31051\), and **three of five at \(251\)**. The \(251\) estimate uses its actual order-five orbit. Counting its seven repeated values alone would give no guarantee. The other fourteen groups pass the exact reverse union bounds.

After ordinary repair, a vertical period of \(2\)-adic valuation one preserves all prescribed odd readings and sets every remainder to \(n\bmod8\pmod{32}\). Both exponents remain odd. This gives exact \(v_2=0\) for residues \(1,5\bmod8\), and exact \(v_2=2\) for residue \(4\bmod8\), with odd part \(1\bmod4\) in all three cases.

### Matched controls

The old retained set fails its small head at each target below. The new set passes all 25 centers through the ordinary panel at \(271\).

| Target | New seed before restoration | Final \(R_j\bmod32\) |
|---:|---:|---:|
| \(1446119089\) | \((11,36100918503393)\) | 1 |
| \(764332\) | \((11,36100888223433)\) | 4 |
| \(84037\) | \((11,36100906886553)\) | 5 |

A separate stress control, \(158604569988085249738760629807450735483399228\), starts with two hits at \(251\), at \(j=0,25\). Their difference has valuation one at \(251\). The specialized restoration shifts \(C\) from \(11\) to \(1979623811\), clears both hits, and the ordinary panel through \(271\) passes.

These are finite-phase certificates. They give no ordinary exponent-height bound or claim of positive two-square remainders.

### Standalone replay

```python
from collections import Counter
from functools import cache
from fractions import Fraction
from itertools import combinations, product
from math import gcd, isqrt, lcm, prod

I = tuple(j for j in range(39)
          if j%5 != 1 and j%9 != 1 and j%11 not in (6,10))
P,E,J,V = 1629320,6284520,3999240,36100888223400
C,D = 11,V+33
S = (43,71,127,211,379,631)
Q = set(S)|{67,199,271,4159}

def vals(q,c,d):
    return {(pow(3,c,q)+pow(5,d+8*j,q))%q for j in I}

def rep(q):
    return {b for b,k in Counter(pow(5,8*j,q) for j in I).items() if k>1}

B = {q:rep(q) for q in Q}
B[23] = {pow(5,8*j,23) for j in I}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b)%q for b in B[q]}

assert len(I)==25 and max(
    (b-a)//((b-a)&-(b-a)) for a,b in combinations(I,2))==35
assert all(a not in vals(q,C,D) for q,a in [(7,2),(11,8),(19,0),(31,27)])
assert all(e%(q-1)==0 for e in (E,J) for q in (7,11,19,31))
assert 9*P%lcm(6,5,9,3)==0
assert all(pow(b,J,q)==1 for q in set(S)|{271} for b in (3,5))
assert all(pow(5,9*P,q)==1 for q in set(S)|{23,67,199})
assert all(pow(b,E,q)==1 for q in (23,67,199,271) for b in (3,5))
assert pow(5,E,4159)==pow(5,J,4159)==1
assert pow(3,J,4159)!=1 and pow(3,11*J,4159)==1

assert [max(Counter(a for x,y in product(range(7),repeat=2)
                    for a in bad(q,C+x*E,D+y*E)).values())
        for q in S]==[13,14,6,2,6,2]
q271 = [bad(271,C,D+9*s*P) for s in range(3)]
assert all(not a&b for a,b in combinations(q271,2))

def masks(q):
    out = [0]*q
    for z,h in product(range(11),repeat=2):
        for a in bad(q,C+z*J,D+h*J):
            out[a] |= 1<<(11*z+h)
    return set(out)

def project(mask):
    return sum(1<<z for z in range(11) if (mask>>(11*z))&2047)

full = (1<<121)-1
p,q,r = [{full^b for b in masks(q)} for q in (23,67,199)]
pairs = {a&b for a in p for b in q}
projections = {project(a&b) for a in pairs for b in r}
assert (len(projections),min(m.bit_count() for m in projections))==(110,7)
assert len(B[4159])==5

# Factor certificate for all possible repeated-hit primes above 23.
Fct = {1:(2,2,2,3),3:(3,7,31),5:(11,71,521),7:(29,449,19531),
9:(3,19,829,5167),11:(23,67,5281,12207031),13:(5227,38923,305175781),
15:(61,181,1741,7621),17:(409,3061,41540861,466344409),
19:(191,761,6271,19609,3981071,213029),21:(7,43,127,379,7603,519499),
23:(47,8971,42272797713043,332207361361),25:(101,251,401,1901,9384251,50150933101),
27:(3,109,163,271,487,4159,31051,16018507),29:(59,35671,5096867,22125996444329,6090817323763),
31:(1303,1861,21207101,28086211607,625552508473588471),33:(199,595123,190771747,386478495679),
35:(211,631,4201,15216601,85280581,4698932281)}
W = {42272797713043:(13967,4523),332207361361:(9781,293),
50150933101:(201167,277),22125996444329:(13624382047,),
6090817323763:(2061161,37),28086211607:(453003413,),
625552508473588471:(391337,25654001),386478495679:(5855734783,)}

@cache
def prime(n):
    if n not in W:
        return n>1 and all(n%d for d in range(2,isqrt(n)+1))
    f = prod(W[n])
    return (f*f>n and (n-1)%f==0 and pow(2,n-1,n)==1 and
            all(prime(p) and gcd(pow(2,(n-1)//p,n)-1,n)==1 for p in W[n]))

T = set()
for m in Fct:
    f = Counter(q for d,ps in Fct.items() if m%d==0 for q in ps)
    assert all(map(prime,f)) and prod(q**v for q,v in f.items())==5**(2*m)-1
    assert all(v==1 for q,v in f.items() if q>23)
    T.update(q for q in f if q>23 and q%4==3)
assert len(T)==40 and V==lcm(3960,*(2*m for m in Fct))
assert all(pow(5,V,q)==1 for q in T)
assert [q for q in range(27,36,4) if prime(q) and V%q==0]==[31]

Adiv = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,
        911,1367,3701,4523,13967,37537,87877,391337,2061161,25654001,
        453003413,5855734783)
assert all(map(prime,Adiv))
assert all(pow(5,q-1,q*q)!=1 for q in Adiv if q>31 and q%4==3)

def order(b,q):
    r,u = q-1,q-1
    for p in Adiv:
        while r%p==0:
            r //= p
        while u%p==0 and pow(b,u//p,q)==1:
            u //= p
    assert r==1
    return u

O = {q:order(3,q) for q in T}
U = lcm(3960,*(q-1 for q in T))
B.update({q:rep(q) for q in T})
hold = set(Q)
steps = []

def private(q,k,cap,square=False):
    e = lcm(3960,529,*(O[p] for p in hold))
    assert O[q]//gcd(O[q],e)==k
    Z = {pow(3,e*x,q) for x in range(k)}
    assert max(max(Counter((a*z+b)%q for z in Z for b in B[q]).values())
               for a in range(1,q) if not square or pow(a,(q-1)//2,q)==1)==cap
    if square:
        assert pow(3,(q-1)//2,q)==pow(5,(q-1)//2,q)==q-1
    steps.append(((q,),e,k))
    hold.add(q)
    return e

private(163,3,2,True)
private(487,3,2,True)
e = lcm(3960,O[31051]//23,*(order(b,q) for q in hold for b in (3,5)))
assert e==3742200 and all(O[q]//gcd(O[q],e)==23 for q in (47,31051))
assert (len(B[47]),len(B[31051]))==(6,5)
steps.append(((47,31051),e,23))
hold.update((47,31051))
assert private(251,5,3)==1979623800

groups = [(595123,12207031,190771747),(59,35671,6090817323763),
          (5227,625552508473588471),(1303,19531,519499,16018507,28086211607),
          (386478495679,),(5096867,),(9384251,),(42272797713043,),
          (3981071,),(191,6271),(38923,),(7603,),(5167,),(8971,)]
for S0 in reversed(groups):
    e = lcm(3960,529,*(O[q] for q in hold))
    periods = [O[q]//gcd(O[q],e) for q in S0]
    assert sum(Fraction(len(B[q]),k) for q,k in zip(S0,periods))<1
    steps.append((S0,e,lcm(*periods)))
    hold.update(S0)
assert hold==T-{31}

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+8*j,q))%q

def select(n):
    x,y = next((x,y) for x,y in product(range(7),repeat=2)
               if all(n%q not in bad(q,C+x*E,D+y*E) for q in S))
    c,d = C+x*E,D+y*E
    s = next(s for s in range(3) if n%271 not in bad(271,c,d+9*s*P))
    d += 9*s*P
    z,h = next((z,h) for z,h in product(range(11),repeat=2)
               if all(n%q not in bad(q,c+z*J,d+h*J) for q in (23,67,199,4159)))
    return c+z*J,d+h*J

old = [j for j in list(range(0,33,2))+list(range(-3,36,2))
       if j%3!=1 and j!=26]
def oldsmall(c,d,q):
    return {(pow(3,c,q)+pow(5,d+8*j,q))%q for j in old}

assert {(c%6,d%6) for c,d in product(range(1,18,2),repeat=2)
        if 2 not in oldsmall(c,d,7) and 0 not in oldsmall(c,d,19)}=={(5,3)}
assert [c for c in range(5,30,6) if 8 not in oldsmall(c,3,11)]==[5,17]
assert all(27 in oldsmall(c,3,31) for c in (5,17))

stress = 158604569988085249738760629807450735483399228
panel = [q for q in range(35,272,4) if prime(q)]
K2 = lcm(V//4,*(p*p*(p-1) for p in panel))
assert K2%4==2 and all(pow(5,K2,q)==1 for q in T|{7,11,19,23,31})

for n in (1446119089,764332,84037,stress):
    assert (n%3,n%7,n%11,n%19,n%31)==(1,2,8,0,27) and n%8 in (1,4,5)
    c,d = select(n)
    if n==stress:
        assert (c,d)==(11,D)
        assert [j for j in I if not R(n,c,d,j,251)]==[0,25]
        assert pow(5,200,251**2)!=1
    for group,e,k in steps:
        c += e*next(a for a in range(k)
                      if all(n%q not in bad(q,c+a*e,d) for q in group))
    if n==stress:
        assert c==1979623811 and n%251 not in vals(251,c,d)
    assert all(sum(not R(n,c,d,j,q) for j in I)<=1 for q in T)

    lock = 1
    for q in panel:
        hits = [j for j in I if not R(n,c,d,j,q)]
        if hits:
            j, = hits
            b = 5 if pow(5,q-1,q*q)!=1 else 3
            assert pow(b,q-1,q*q)!=1
            e = lcm(V if b==5 else U,q-1,lock)
            assert e%q
            dc,dd = (e,0) if b==3 else (0,e)
            a = next(a for a in range(2*q)
                     if R(n,c+a*dc,d+a*dd,j,q*q)==0<
                        R(n,c+a*dc,d+a*dd,j,q**3))
            c,d = c+a*dc,d+a*dd
        lock = lcm(lock,q*q*(q-1))

    k, = [k for k in range(4) if R(n,c,d+k*K2,0,32)==n%8]
    d += k*K2
    assert all(R(n,c,d,j,32)==n%8 and
               all(R(n,c,d,j,q) for q in (3,7,11,19,23,31)) for j in I)
    assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q)==0<R(n,c,d,j,q**3)
               for q in panel for j in I)

print("Verified the residual-class certificate and all four finite controls.")
```
