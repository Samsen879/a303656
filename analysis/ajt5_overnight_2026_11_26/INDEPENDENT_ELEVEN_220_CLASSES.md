# Independent order-eleven digits give 25 centers in 220 more classes

For \(23\nmid n,\ n\bmod3\in\{0,1\}\), and \(n\bmod8\in\{0,2,3,6,7\}\), the doubled-gap template from the [even-stratum construction](https://github.com/Samsen879/a303656/commit/8e2bb2b8e6db422b9d0dcfa90e08d82b671fe21b) gives 25 finite-phase centers. These are 220 classes modulo 552, with no restriction at \(7,11,19,31\). The conclusion includes all ordinary rows of a prescribed finite panel and cross-block non-reuse, not a bound on exponent height.

Keep the doubled offsets and six types. The initial screen reads the 11/31/271 head, then 7 and 19, then the joint order-seven masks at 43, 71, 127, 379. The forbidden sets at 7 for the three ternary types are \(\{4,6\},\{1,5\},\{2,3\}\). The exact check ranges over all seven residues at 7. For each of the 53 minimal head profiles it checks 12 minimal eligibility sets, each with a single or paired chart that cannot be covered by shared prime residues. The order-five costs remain as in the previous construction.

Replace the diagonal order-eleven shifts by \((zJ,hJ)\), \(0\le z,h<11,\ J=3999240\). At 23 the horizontal orbit is exactly the squares, and for every \(h\) the vertical values range over all nonsquares because the retained indices meet every class modulo 11. Each nonzero target there forbids five \(z\)'s. At 4159 at most two horizontal digits are forbidden, and \(h\) is invisible. If the target at 67 is nonzero, at most two further horizontal digits can hit it for any \(h\); indeed the repeated values lie in the order-eleven vertical orbit there. For any surviving \(z\), the four repeated values at 199 forbid at most four \(h\)'s. If the target at 67 is zero, use \(h=7z\bmod11\); the two powers scale together at 67, preserving passage. The row at 199 then forbids at most three \(z\)'s. In either branch the total horizontal cost is below eleven and all 23 readings can be units.

The standard reverse tie restoration and the special order-three rows still apply. With 23 units, the final pair 47 and 31051 needs only the protected horizontal step 3742200: the orbits have size 23 and their respective costs are at most five and seven. The step preserves the first reading at 23. All ordinary repairs then proceed with the earlier axis locks. Finally use the even proof's vertical period with \(v_2=1\) to select common remainders modulo 32 equal to 2, 4, 5, 8 or 1 respectively for the five listed \(n\bmod8\) values. These each have odd part 1 modulo 4. Positive \(C\), odd \(D\) give the unit at 3 for the two covered \(n\bmod3\) values. The \(C=0\) case is not justified by periodicity at 3 and is not used.

At the same target \(201670\), the old diagonal at 67 forces digit zero and leaves three hits at 23. The independent digits \((1,7)\) with the displayed head leave none; the replay checks all 25 through 271. This is a finite-panel control.

~~~python
from collections import Counter
from functools import cache
from itertools import combinations, product
from math import isqrt, lcm

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
P,E,J,G = 1629320,6284520,3999240,8798328
D,V = 135004545787,36100888223400
A = [(66+(3*t+w)*P,D+(5*w+3*s)*P)
     for s,w,t in product(range(2),range(3),range(3))]
FULL = (1<<49)-1

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+8*j,q))%q for j in I}

def repeats(q):
    return {v for v,k in Counter(pow(5,8*j,q) for j in I).items() if k>1}

B = {q:repeats(q) for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b)%q for b in B[q]}

# The fixed head and the available order-five digits.
assert len(I)==25 and {j%5 for j in I}==set(range(5))
assert {j%11 for j in I}==set(range(11))
assert all(s%(q-1)==0 for s in (E,J) for q in (7,11,19,31))
assert all(G%(q-1)==0 for q in (7,19))
assert all(3*P%(q-1)==0 for q in (7,11,31))
assert pow(5,G,31)==1
assert all(pow(b,G,q)==1 for b in (3,5) for q in Q-{71,211,271,631})
assert all(pow(b,J,q)==1 for b in (3,5) for q in Q-{67,199,4159})
assert all(pow(b,E,q)==1 for b in (3,5) for q in (67,199,271))
assert pow(5,E,4159)==pow(5,J,4159)==1
assert pow(5,E,71)==pow(5,G,271)==pow(5,5*G,71)==pow(3,5*G,71)==1
assert B[71]=={pow(5,k,71) for k in range(5)}
for q in (211,631):
    assert len(B[q])==2 and pow(5,G,q)!=1 and pow(5,5*G,q)==1

B271 = [[bad(271,A[3*w][0]+u*G,A[3*w][1]) for u in range(5)]
        for w in range(6)]
for w,u in product(range(3),range(5)):
    assert not B271[w][u] & B271[w+3][u]
for i,(c,d) in enumerate(A):
    assert small(c,d,7)==[{4,6},{1,5},{2,3}][i//3%3]
    assert B271[i//3]==[bad(271,c+u*G,d) for u in range(5)]

@cache
def head(a,b):
    out = []
    for w in range(6):
        c,d = A[3*w]
        out.append(tuple(u for u in range(5)
                         if a not in small(c+u*G,d,11)
                         and b not in small(c+u*G,d,31)))
    assert all(out)
    return out

def profile(a,b,r):
    out = [tuple(u for u in us if r not in B271[w][u])
           for w,us in enumerate(head(a,b))]
    return tuple(us if w<3 or not out[w-3] else () for w,us in enumerate(out))

def norm(us):
    return min(tuple(tuple(sorted((u+k)%5 for u in s)) for s in us)
               for k in range(5))

profiles = {norm(profile(a,b,r))
            for a,b,r in product(range(11),range(31),range(271))}
minimal = []
for us in sorted(profiles,key=lambda s:(sum(map(len,s)),s)):
    if not any(all(set(a)>=set(b) for a,b in zip(us,v)) for v in minimal):
        minimal.append(us)
assert (len(profiles),len(minimal))==(458,53)

@cache
def mask(i,q,us):
    c,d = A[i]
    out = {}
    for x,y in product(range(7),repeat=2):
        vals = (set.intersection(*(bad(71,c+x*E+u*G,d) for u in us))
                if q==71 else bad(q,c+x*E,d+y*E))
        for a in vals:
            out[a] = out.get(a,0) | (1<<(7*x+y))
    return out

@cache
def cover(ss,us):
    rows = []
    for q in (43,71,127,379):
        ms = [mask(i,q,u if q==71 else ()) for i,u in zip(ss,us)]
        rows.append({tuple(m.get(a,0) for m in ms) for a in range(q)})
    rows.sort(key=lambda h:-max(sum(m.bit_count() for m in z) for z in h))
    lim = [[0]*len(ss) for _ in range(len(rows)+1)]
    for k in reversed(range(len(rows))):
        lim[k] = [lim[k+1][i]+max(z[i].bit_count() for z in rows[k])
                  for i in range(len(ss))]

    @cache
    def visit(k,seen):
        if all(m==FULL for m in seen):
            return True
        if any(m.bit_count()+r<49 for m,r in zip(seen,lim[k])):
            return False
        for z in rows[k]:
            new = tuple(a|b for a,b in zip(seen,z))
            if all(m.bit_count()+r>=49 for m,r in zip(new,lim[k+1])):
                if visit(k+1,new):
                    return True
        return False

    ans = visit(0,(0,)*len(ss))
    visit.cache_clear()
    return ans

fixed = {q:[small(c,d,q) for c,d in A] for q in (7,19)}
total = 0
for us in minimal:
    states = {frozenset(i for i in range(18) if us[i//3]
                        and a not in fixed[7][i] and b not in fixed[19][i])
              for a,b in product(range(7),range(19))}
    least = [s for s in states if not any(r<s for r in states)]
    assert len(least)==12
    for s in least:
        assert any(not cover(z,tuple(us[i//3] for i in z))
                   for k in (1,2) for z in combinations(sorted(s),k))
    total += len(least)
assert total==636

# Independent order-eleven digits and the later horizontal restoration.
S23 = {pow(3,k,23) for k in range(11)}
N23 = {pow(5,2*k+1,23) for k in range(11)}
assert len({pow(3,k*J,23) for k in range(11)})==11
assert {sum((a-b)%23 in N23 for b in S23) for a in range(1,23)}=={5}
assert pow(3,J,67)==pow(5,7*J,67)
assert pow(5,J,199)!=1 and pow(5,11*J,199)==1 and len(B[199])==4
for c,d in A:
    risk = Counter(a for z in range(11) for a in
                   {(pow(3,c+z*J,67)+pow(5,d+h*J,67))%67 for h in range(11)})
    assert max(k for a,k in risk.items() if a)<=2
    assert [z for z in range(11) if 0 not in bad(67,c+z*J,d+5*z*J)]==[0]
    line = Counter(a for z in range(11) for a in bad(199,c+z*J,d+7*z*J))
    assert max(line.values())<=3
    for x in range(7):
        h = Counter(a for z in range(11) for a in bad(4159,c+x*E+z*J,d))
        assert max(h.values())<=2
for q,k in ((47,5),(31051,7)):
    assert 3742200%22==0
    assert len(repeats(q))==k
    assert len({pow(3,3742200*z,q) for z in range(23)})==23

n = 201670
def R(c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+8*j,q))%q

assert (n%8,n%3,n%7,n%23,n%67)==(6,1,0,6,0)
assert [j for j in I if not R(66,D,j,23)]==[0,11,33]
K = lcm(V//4,529)
c,d = 66+3*G+J,D+7*J+3*K
assert (c,d)==(30394290,622875354394117)
assert all(R(c,d,j,32)==8 and
           all(R(c,d,j,q) for q in (3,7,11,19,23,31)) for j in I)

tie = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
       4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
       595123,3981071,5096867,9384251,12207031,16018507,190771747,
       28086211607,386478495679,6090817323763,42272797713043,
       625552508473588471)
assert all(sum(not R(c,d,j,q) for j in I)<=1 for q in tie)
panel = [q for q in range(27,272,4) if all(q%k for k in range(2,isqrt(q)+1))]
lock,trace = 529,[]
for q in panel:
    hits = [j for j in I if not R(c,d,j,q)]
    if hits:
        j, = hits
        e = lcm(V,lock,q-1)
        assert e%q and pow(5,e,q*q)!=1
        x = next(x for x in range(2*q) if R(c,d+x*e,j,q*q)==0<R(c,d+x*e,j,q**3))
        d += x*e
        trace.append((q,j,x,R(c,d,j,q**3)//q**2))
    lock = lcm(lock,q*q*(q-1))
assert trace[-1]==(251,3,63,16)
assert all(R(c,d,j,32)==8 and R(c,d,j,23) for j in I)
assert all(R(c,d,j,q) or R(c,d,j,q*q)==0<R(c,d,j,q**3)
           for j in I for q in panel)
assert (7-3**0-5**0)%3==2 and (7-3**2-5**0)%3==0
print(total, trace)
~~~
