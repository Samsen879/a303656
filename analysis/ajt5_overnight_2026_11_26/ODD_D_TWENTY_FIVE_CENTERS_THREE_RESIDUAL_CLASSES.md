# Odd-D finite-phase coverage outside three residual target classes

This continues [the even-D finite-phase certificate](https://github.com/Samsen879/a303656/commit/371f755a6d2e41615a12dd1c97769d8695c222db). The odd-D construction, except for the three exact target residues below, adds the \(n\equiv1\bmod3\) strata. The exceptions are failures of this small-head/unit strategy with these retained gaps; they are not exceptions to the original sum-of-powers conjecture. The two positive controls have genuinely repaired modular phases, not claimed height-bounded positive norms.

An independent bit-mask implementation reran all ordinary and locked head profile families, the combined maximum masks, and the negative locked example. An independent integer replay also checked the 40-prime tie catalogue, its primality/product certificates, both order-three repair caps, all 15 reverse tie budgets, the mixed 47/31051 cap, and the three controls including their exact 23-adic readings. The 23-locked horizontal step preserves divisibility by \(23^2\) at the unique retained center: on the root modulo 23 the two powers are negatives, and \(14\cdot16\equiv17\bmod23\) matches their first-order multipliers modulo \(23^2\). The later vertical step \(V\) then changes the residue modulo \(23^3\) by a unit multiple of \(23^2\), preserving the already repaired smaller reading.

**The 25-center finite-phase theorem now covers every \(n>1\) outside**
\[
\boxed{n\equiv 84037,\ 628273,\ \text{or }764332\pmod{1088472}.}
\]
This combines the previous \(n\bmod3\in\{0,2\}\) theorem with the new \(n\equiv1\bmod3\) certificate. The three remaining classes have a common small-head obstruction for the retained set \(I\) with positive \(C\). The obstruction occurs before any tie restoration.

### Exact residual and parity audit

The three classes are precisely
\[
 n_3=1,\quad n_8\in\{1,4,5\},\quad
 (n_7,n_{19},n_{11},n_{31})=(2,0,8,27),
\]
where \(n_p=n\bmod p\). There is no condition at \(23\) or \(67\).

For \(C>0\), the unit at \(3\) forces odd \(D\). For these three \(n_8\) values the guard at \(2\) then forces odd \(C\). On the fixed retained set, units at \(7,19\) force \((C,D)\equiv(5,3)\bmod6\). Among the five resulting \(C\)-classes mod \(30\), only \(5,17\) clear \(11\), and both hit \(31\). This exhausts all positive-\(C\) seeds under these head guards.

With \(C=0\), the unit at \(3\) instead forces even \(D\). At \(n_8=1,5\), that choice fails at \(2\). At \(n_8=4\), it can give a legal small head. For example, \(n=764332,\ C=0,\ D=125182\) gives the required small readings, including exact valuation two at \(23\). The all-panel restoration below uses positive \(C\) and leaves this zero-exponent option open.

### Coverage of the other \(n\equiv1\bmod3\) targets

Keep the 25 labels \(I\) and doubled offsets \(D+8j\). For \(e=C\bmod2\), use anchors
\[
(C,D)=\bigl(66+eH+(3t+w)P,\ D_0+(5w+d+3s)P\bigr),
\]
with the constants in the replay. Here \(t,w,d\in\{0,1,2\}\) and \(s\in\{0,1\}\). Read \(7\) against the actual target and choose the least legal \(d\) for each \(w\), with two exceptions:

- For **odd \(C\)** at \((n_7,n_{19})=(2,0)\), use only \((w,d)=(1,2)\). At \((4,0)\), use only \((2,1)\). The first case omits the exact residual head \((n_{11},n_{31})=(8,27)\).
- For **even \(C\)** with \(n_{23}=n_{67}=0\), the diagonal order-eleven digit is forced to zero. At \(n_7=3,5,6\), keep every legal \((w,d)\) so that the locked \(199,4159\) readings can be screened jointly. Elsewhere the least legal digit suffices.

The replay checks the actual \(11,31,271\) profiles and all inclusion-minimal eligibility sets at \(19\), adding \(199\) in the locked branch. Each eligible set contains one or two charts that cannot be jointly covered by the remaining prime residues.

For \(n_{23}\ne0\), independent order-eleven digits leave a strict unit at \(23\) and clear repeated hits at \(67,199,4159\). The exact combined horizontal mask has at most ten of eleven bits set. For \(n_{23}=0\), use the diagonal slope \(5\) to keep \(j=15\) the unique root. Outside the locked branch, the exact maximum forbidden count is seven for even \(C\) and nine for odd \(C\). The \(23\)-adic lift makes the retained root exactly \(23^2\bmod23^3\).

The replay also checks the generic reverse tie-restoration budgets, both order-three repairs, and the two \(47,31051\) branches. Since the exponent gaps have odd parts at most 35, the factored \(5^{2m}-1\) catalogue certifies non-reuse by common Wieferich primes. Ordinary repairs use an available axis with nonzero first-order coefficient, preserving previous readings mod prime cubes. A final vertical period of \(2\)-adic valuation one gives the required common residue mod \(32\), while preserving the repaired odd-prime readings.

### Matched controls

- **\(39321697\)** and **\(1446119089\)** agree at \(8,3,7,11,19,23,67\). Their residues at \(31\) are 26 and 27. The first passes the new odd-\(C\) special menu and the ordinary panel through \(271\). The second is in the residual class and fails the exact small-head test above.
- **\(9216906648208602209939278\)** has \(n_{23}=n_{67}=0\). The least-digit, unshifted-first menu leaves one eligible chart, and its actual residue masks cover all 49 cells. Keeping the other legal low digits repairs the same target. The resulting phase passes the ordinary panel through \(271\).

These are finite-phase statements.

### Standalone replay

```python
from collections import Counter
from functools import cache
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, isqrt, lcm, prod

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j%3 != 1 and j != 26]
P,E,J,G,H = 1629320,6284520,3999240,8798328,5498955
D,V = 135004545787,36100888223400
L = V//23
Q = {43,67,71,127,199,211,271,379,631,4159}
FULL = (1<<49)-1

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+8*j,q))%q for j in I}

def rep(q):
    return {b for b,k in Counter(pow(5,8*j,q) for j in I).items() if k>1}

B = {q:rep(q) for q in Q}
def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b)%q for b in B[q]}

def anchor(e,w,d,t=0,s=0):
    return 66+e*H+(3*t+w)*P, D+(5*w+d+3*s)*P

assert len(I)==25 and {j%5 for j in I}==set(range(5))
assert {j%11 for j in I}==set(range(11))
assert all(k%(q-1)==0 for q in (7,11,19,31) for k in (E,J))
assert all(G%(q-1)==0 for q in (7,19,23))
assert all(3*P%(q-1)==0 for q in (7,11,31))
assert all(pow(b,G,q)==1 for q in Q-{71,211,271,631} for b in (3,5))
assert all(pow(b,J,q)==1 for q in Q-{67,199,4159} for b in (3,5))
assert all(pow(b,E,q)==1 for q in (67,199,271) for b in (3,5))
assert pow(5,G,31)==pow(5,E,71)==pow(5,E,4159)==pow(5,J,4159)==1
assert pow(5,5*G,71)==pow(3,5*G,71)==pow(5,G,271)==1
assert B[71]=={pow(5,k,71) for k in range(5)}
assert not B[271]&{b*pow(5,3*P,271)%271 for b in B[271]}
assert pow(3,J,23)==pow(5,5*J,23)!=1
assert pow(3,11*J,23)==pow(5,11*J,23)==1
assert pow(5,L,529)==24 and pow(5,V,23**3)==530
assert all(pow(5,L,q)==1 for q in Q|{7,11,19,31})
for q in (211,631):
    assert len(B[q])==2 and pow(5,G,q)!=1 and pow(5,5*G,q)==1

@cache
def mask(c,d,q,us):
    out = {}
    for x,y in product(range(7),repeat=2):
        vals = (set.intersection(*(bad(71,c+x*E+u*G,d) for u in us))
                if q==71 else bad(q,c+x*E,d+y*E))
        for a in vals:
            out[a] = out.get(a,0) | (1<<(7*x+y))
    return out

@cache
def cover(charts,locked):
    rows = []
    for q in (43,71,127,379,4159) if locked else (43,71,127,379):
        ms = [mask(c,d,q,u if q==71 else ()) for c,d,u in charts]
        rows.append({tuple(m.get(a,0) for m in ms) for a in range(q)})
    rows.sort(key=lambda h:-max(sum(m.bit_count() for m in z) for z in h))
    n,k = len(rows),len(charts)
    lim = [[0]*k for _ in range(n+1)]
    for i in reversed(range(n)):
        lim[i] = [lim[i+1][j]+max(z[j].bit_count() for z in rows[i])
                  for j in range(k)]
    @cache
    def visit(i,seen):
        if all(m==FULL for m in seen):
            return True
        if any(m.bit_count()+r<49 for m,r in zip(seen,lim[i])):
            return False
        for z in rows[i]:
            new = tuple(a|b for a,b in zip(seen,z))
            if all(m.bit_count()+r>=49 for m,r in zip(new,lim[i+1])):
                if visit(i+1,new):
                    return True
        return False
    ans = visit(0,(0,)*k)
    visit.cache_clear()
    return ans

def minimal(bits):
    out = []
    for z in sorted(bits,key=int.bit_count):
        if not any(z&k==k for k in out):
            out.append(z)
    return out

def norm(us):
    return min(tuple(tuple(sorted((u+k)%5 for u in s)) for s in us)
               for k in range(5))

@cache
def certify(e,groups,locked,targets,skip=()):
    A = [anchor(e,w,d,t,s)
         for s in range(2) for w,d in groups for t in range(3)]
    g = len(groups)
    b271 = [[bad(271,c+u*G,d) for u in range(5)] for c,d in A[::3]]
    for i,(c,d) in enumerate(A):
        assert b271[i//3]==[bad(271,c+u*G,d) for u in range(5)]

    @cache
    def head(a,b):
        return [tuple(u for u in range(5) if a not in small(c+u*G,d,11)
                     and b not in small(c+u*G,d,31)) for c,d in A[::3]]

    def profile(a,b,r):
        us = [tuple(u for u in s if r not in b271[i][u])
              for i,s in enumerate(head(a,b))]
        return norm(tuple(s if i<g or not us[i-g] else ()
                          for i,s in enumerate(us)))

    def score(us):
        return sum(1<<(5*i+u) for i,s in enumerate(us) for u in s)

    profiles = {score(us):us for us in
                {profile(a,b,r) for a,b in product(range(11),range(31))
                 if (a,b) not in skip for r in range(271)}}
    f19 = [small(c,d,19) for c,d in A]
    f199 = [bad(199,c,d) for c,d in A]
    elig = minimal({sum(1<<i for i in range(len(A)) if a not in f19[i]
                        and (not locked or b not in f199[i]))
                    for a,b in product(targets,range(199 if locked else 1))})
    for m in minimal(profiles):
        us = profiles[m]
        active = sum(1<<i for i in range(len(A)) if us[i//3])
        for k in minimal({z&active for z in elig}):
            ids = [i for i in range(len(A)) if k>>i&1]
            assert any(not cover(tuple((*A[i],us[i//3]) for i in s),locked)
                       for r in (1,2) for s in combinations(ids,r))
    return A

def groups(e,a7):
    return tuple((w,d) for w,d in product(range(3),range(3))
                 if a7 not in small(*anchor(e,w,d),7))

A = [set(),set()]
all19 = tuple(range(19))
for a7 in range(7):
    for e in (0,1):
        gs = groups(e,a7)
        first = tuple((w,next(d for v,d in gs if v==w)) for w in range(3))
        targets = tuple(range(1,19)) if e and a7 in (2,4) else all19
        A[e].update(certify(e,first,False,targets))
        if not e:
            wide = gs if a7 in (3,5,6) else first
            certify(e,wide,True,all19)
for a7,w,d,skip in [(2,1,2,((8,27),)),(4,2,1,())]:
    assert all(a7 not in small(*anchor(1,w,d,t,s),7)
               for t,s in product(range(3),range(2)))
    A[1].update(certify(1,((w,d),),False,(0,),skip))
assert list(map(len,A))==[54,54]

def reads(q,c,d):
    out = [[0]*11 for _ in range(q)]
    for z,h in product(range(11),repeat=2):
        for a in bad(q,c+z*J,d+h*J):
            out[a][z] |= 1<<h
    return out

def line(q,c,d,s):
    out = [0]*q
    for z in range(11):
        for a in bad(q,c+z*J,d+s*z*J):
            out[a] |= 1<<z
    return out

assert all(pow(5,L,q)==1 for q in Q|{7,11,19,31})
assert pow(5,L,529)==24 and pow(5,V,23**3)==530
assert pow(3,J,23)==pow(5,5*J,23)!=1
N23 = {pow(5,2*k+1,23) for k in range(11)}
for e,anchors in enumerate(A):
    caps = [0,0]
    for c,d in anchors:
        assert [j for j in I if (pow(3,c,23)+pow(5,d+8*j,23))%23==0]==[15]
        p,q = reads(67,c,d),reads(199,c,d)
        dead = {sum(1<<z for z in range(11) if a[z]|b[z]==2047)
                for a in p for b in q}
        h23 = {sum(1<<z for z in range(11)
                   if (n-pow(3,c+z*J,23))%23 in N23) for n in range(1,23)}
        p = line(67,c,d,5)
        if not e:
            assert p[0]==2046
        diag = {a|b for a in p[0 if e else 1:] for b in line(199,c,d,5)}
        for x in range(7):
            h = set(line(4159,c+x*E,d,0))
            caps[0] = max(caps[0],max((a|b|k).bit_count()
                                      for a in dead for b in h23 for k in h))
            caps[1] = max(caps[1],max((a|b).bit_count() for a in diag for b in h))
    assert caps==([10,7] if e==0 else [10,9])

# Exact tie catalogue and reverse restoration budgets.
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
assert len(T)==40 and all(pow(5,V,q)==1 for q in T)
Adiv = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,
        911,1367,3701,4523,13967,37537,87877,391337,2061161,25654001,
        453003413,5855734783)
assert all(map(prime,Adiv))
def order(b,q):
    r,u = q-1,q-1
    for p in Adiv:
        while r%p==0:r//=p
        while u%p==0 and pow(b,u//p,q)==1:u//=p
    assert r==1
    return u

O = {q:order(3,q) for q in T}
assert all(pow(5,q-1,q*q)!=1 for q in Adiv if q>31 and q%4==3)
assert V==lcm(3960,*(2*m for m in Fct))
assert [q for q in Adiv if q>23 and q%4==3 and V%q==0]==[31]
for q in T:
    B[q] = rep(q)
hold = set(Q)
for q in (163,487):
    e = lcm(3960,529,*(O[p] for p in hold))
    Z = {pow(3,e*x,q) for x in range(3)}
    assert len(Z)==3 and max(max(Counter((a*z+b)%q for z in Z
                                     for b in B[q]).values())
                             for a in range(1,q))==2
    hold.add(q)
e = lcm(3960,O[31051]//23,*(order(b,q) for b in (3,5) for q in hold))
assert e==3742200 and e%22==0 and e%23!=0
assert pow(5,e,31051)==1 and pow(5,16*e,47)==pow(3,10*e,47)
assert [(pow(b,22,529)-1)//23 for b in (3,5)]==[17,14]
assert all(O[q]//gcd(O[q],e)==23 for q in (47,31051))
Z = {pow(3,e*x,47) for x in range(23)}
assert (len(B[47]),len(B[31051]))==(5,7)
assert max(max(Counter(y for z in Z for y in
                       {(a*z+b*pow(z,10,47))%47 for b in B[47]}).values())
           for a in range(1,47))==6
hold.update((47,31051))
logs = [(595123,12207031,190771747),(59,35671,6090817323763),
        (5227,625552508473588471),(1303,19531,519499,16018507,28086211607),
        (386478495679,),(5096867,),(9384251,),(42272797713043,),
        (3981071,),(191,6271),(38923,),(7603,),(5167,),(8971,),(251,)]
for S in reversed(logs):
    e = lcm(3960,529,*(O[q] for q in hold))
    assert sum(F(len(B[q]),O[q]//gcd(O[q],e)) for q in S)<1
    hold.update(S)
assert hold==T-{31}

# Native controls.
def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+8*j,q))%q

assert {(c%6,d%6) for c,d in product(range(1,18,2),repeat=2)
        if 2 not in small(c,d,7) and 0 not in small(c,d,19)}=={(5,3)}
assert [c for c in range(5,30,6) if 8 not in small(c,3,11)]==[5,17]
assert all(27 in small(c,3,31) for c in (5,17))
assert 1446119089%1088472==628273
assert all(39321697%q==1446119089%q for q in (8,3,7,11,19,23,67))
assert (39321697%31,1446119089%31)==(26,27)

n = 9216906648208602209939278
A0 = [anchor(0,w,(0,0,2)[w],t,s)
      for s,w,t in product(range(2),range(3),range(3))]
us = [tuple(u for u in range(5) if all(n%q not in small(c+u*G,d,q)
             for q in (11,31)) and n%271 not in bad(271,c+u*G,d))
      for c,d in A0[::3]]
us = [s if w<3 or not us[w-3] else () for w,s in enumerate(us)]
assert [i for i,(c,d) in enumerate(A0) if us[i//3]
        and n%19 not in small(c,d,19) and n%199 not in bad(199,c,d)]==[2]
c,d = A0[2]
m = 0
for q in (43,71,127,379,4159):
    m |= mask(c,d,q,us[0] if q==71 else ()).get(n%q,0)
assert m==FULL

panel = [q for q in range(27,272,4) if prime(q)]
for n,c,d,r in [
    (39321697,31009517,2679369295469049676786210157263305837775610448446849513211799047,1),
    (9216906648208602209939278,27623442,2200018157974367732864782107,8),
]:
    assert all(R(n,c,d,j,32)==r and
               all(R(n,c,d,j,q) for q in (3,7,11,19,31)) for j in I)
    assert [j for j in I if not R(n,c,d,j,23)]==[15]
    assert R(n,c,d,15,23**3)==529
    assert all(sum(not R(n,c,d,j,q) for j in I)<=1 for q in T)
    assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q)==0<R(n,c,d,j,q**3)
               for j in I for q in panel)

n,c,d = 764332,0,125182
assert all(R(n,c,d,j,32)==2 and
           all(R(n,c,d,j,q) for q in (3,7,11,19,31)) for j in I)
assert [j for j in I if not R(n,c,d,j,23)]==[15]
assert R(n,c,d,15,23**3)==529
print("Verified the n=1 mod 3 coverage certificate and native controls.")
```
