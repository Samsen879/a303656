# Twenty-five finite-phase centers for all odd deficient heads

For positive \(C\), the old 37-offset head \(D+8i\) requires units at \(3,7,11,19,31\), an admissible odd part at 2, and units or one repair to exact valuation two at 23. Its head alone falls short of 25 exactly when \(n\equiv1\bmod3\), \(7\cdot23\mid n\), and \(n\equiv3\bmod4\) or \(n\equiv6\bmod8\). This classification is only about the old head, before the other ordinary primes.

For given parities, if \(n\ne0\bmod7\), some \(C\bmod6\) makes every offset a unit at 7: otherwise a nonzero additive translation would carry one three-element multiplicative coset onto the other, contrary to their zero sums. At a fixed \(C\bmod6\), its five lifts mod 30 give five possible horizontal values at 31, of which at most three hit. If both rows are units, the bad classes of indices modulo 5, 9, 11 can be placed independently to lose at most ten, counting the allowed 23 repair. If the row at 7 is forced, the small replay checks the mod-90 choices making row 31 a unit or deleting the same class, and clearing 11 and 19 on what remains. The independent \(C\bmod11\) choice clears 23 unless \(n\equiv0\bmod23\) and \(D\) is odd. In the forced-7 branch this exception means \(C\) is even. A mod-3 and mod-11 class then delete at least 14 indices and at most one 23-hit can return. The unit at 3 forces odd \(D\) only for \(n\equiv1\bmod3\); for odd \(D\) the 2-adic guard forces even \(C\) precisely in the two displayed cases. All other needed low powers of 2 can be chosen via \(C,D\bmod8\), compatible with the odd-prime phases.

For every **odd** deficient head, extend the [first full hard-class menu](https://github.com/Samsen879/a303656/commit/dd4ef000e53f88ab807b7a5c7a8110f34aa3e67a) to \(C=66+(3t+w)P,\ D=D_0+(5w+12s)P\), with \(0\le t,w<3,\ s=0,1,\ P=1629320\). The shifted fallback at 271 is now available for each of the three ternary types. Read actual \(n\bmod11,31\) into the permitted horizontal order-five digits, and then \(n\bmod271\). For each individual horizontal digit the unshifted and shifted sets at 271 are disjoint. A common rotation of these digit sets changes the remaining 71 screen only by a common multiplicative rescaling, because the repeated vertical values there form the order-five subgroup. This allows normalization before grouping all head profiles. The exact replay checks 477 profiles, reduced by inclusion to 43. Across both 67 branches their 1419 minimal eligibility sets have one or two charts which cannot be covered simultaneously by any tuple of actual variable-prime residues. The existing choices of the order-eleven and vertical order-five digits, tie-row restoration and ordinary repair then apply. Thus all 341 old deficient odd classes modulo 658812 have 25 finite-phase centers, including every 19 residue. No exponent-height claim is made.

For \(n\equiv6\bmod8,\ n\equiv1\bmod3,\ n\equiv0\bmod161\), the mixed-gap templates \(D+4j\) have an all-seed 2-adic obstruction. Odd \(D\) and the guard force even \(C\). If the constant remainder modulo 16 is 8, only one parity of \(j\) survives, and the 7-deletion leaves at most 14. Otherwise \(R_j/16=a+5j\bmod8\), using \(5^4=1+112\bmod128\) and odd \(D\). The 2-adic guard requires residue in \(\{0,1,2,4,5\}\); with the 7 deletion the count is at most 17. The doubled-gap template \(D+8j\) gives a genuine 25-center finite-panel control at \(1196230\) with all remainders \(8\bmod32\). Uniform doubled-gap coverage of this even stratum is not established here. The replay also certifies an odd target outside the prior hard class.

~~~python
from collections import Counter
from functools import cache
from itertools import combinations, product
from math import isqrt, lcm

X = range(37)
assert min(sum(i%3 == b or i%11 == a for i in X)
           for a,b in product(range(11),range(3))) == 14
assert min(sum(i%5 == b or i%9 == d or i%11 == a for i in X)
           - any(i%11 == a and i%5 != b and i%9 != d for i in X)
           for a,b,d in product(range(11),range(5),range(9))) == 10
H11 = {pow(5,k,11) for k in range(5)}
H19 = [{pow(5,e,19) for e in range(9) if e%3 != s} for s in range(3)]
r31 = {pow(5,k,31):k for k in range(3)}
for cp,dp in ((0,1),(1,0)):
    r7 = {pow(5,k,7):k%3 for k in range(dp,6,2)}
    for a,b,d in product(range(31),range(11),range(19)):
        assert any(
            r31.get((a-pow(3,c,31))%31) in (None,r7[-pow(3,c,7)%7])
            and (b-pow(3,c,11))%11 not in H11
            and any((d-pow(3,c+30*t,19))%19 not in H19[r7[-pow(3,c,7)%7]]
                    for t in range(3))
            for c in range(cp,30,2))

for s in (-3,-1):
    js = list(range(0,33,2))+list(range(s,s+40,2))
    assert max(sum(j%3 != b and j%2 == c for j in js)
               for b,c in product(range(3),range(2))) == 14
    assert max(sum(j%3 != b and (a+5*j)%8 in {0,1,2,4,5} for j in js)
               for a,b in product(range(8),range(3))) == 17

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j%3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
P,E,J,G = 1629320,6284520,3999240,8798328
D,L,V = 135004545737,1569603835800,36100888223400
A = [(66+(3*t+w)*P,D+(5*w+12*s)*P)
     for s,w,t in product(range(2),range(3),range(3))]
FULL = (1<<49)-1

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+4*j,q))%q for j in I}

B = {q:{b for b,k in Counter(pow(5,4*j,q) for j in I).items() if k>1}
     for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b)%q for b in B[q]}

assert all(s%(22*23**2)==0 for s in (P,E,G))
assert pow(3,P,7)==pow(5,5*P,7)
assert pow(3,J,23**3)==pow(5,5*J,23**3)
assert pow(5,L,529)==24 and pow(5,V,23**3)==530
assert all(pow(5,L,q)==1 for q in Q|{7,11,19,31})
assert all(s%(q-1)==0 for s in (E,J) for q in (7,11,19,31))
assert all(3*P%(q-1)==0 for q in (7,11,31))
assert all(G%(q-1)==0 for q in (7,19))
assert all(pow(b,G,q)==1 for b in (3,5) for q in Q-{71,211,271,631})
assert all(pow(3,J,q)==pow(5,5*J,q)==1 for q in Q-{67,199,4159})
assert all(pow(b,E,q)==1 for b in (3,5) for q in (67,199,271))
assert all(pow(b,P,67)==1 for b in (3,5))
assert pow(5,E,4159)==pow(5,J,4159)==1
assert pow(5,E,71)==pow(5,5*G,71)==pow(5,G,271)==pow(3,5*G,71)==1
assert B[71]=={pow(5,k,71) for k in range(5)}
assert {j%5 for j in I}==set(range(5)) and pow(5,G,31)==1
for q in (211,631):
    assert len(B[q])==2 and pow(5,G,q)!=1 and pow(5,5*G,q)==1

B271 = [[bad(271,A[3*w][0]+u*G,A[3*w][1]) for u in range(5)]
        for w in range(6)]
for w,u in product(range(3),range(5)):
    assert not B271[w][u] & B271[w+3][u]
for i,(c,d) in enumerate(A):
    assert 0 not in small(c,d,7)
    assert [j for j in I if (pow(3,c,23)+pow(5,d+4*j,23))%23==0]==[15]
    assert B271[i//3]==[bad(271,c+u*G,d) for u in range(5)]
    for q,cap in [(67,2),(199,3),(4159,2)]:
        for x in range(7 if q==4159 else 1):
            sets = [bad(q,c+x*E+z*J,d+5*z*J) for z in range(11)]
            h = Counter(a for s in sets for a in s)
            assert max(k for a,k in h.items() if a or q!=67)<=cap
            if q==67:
                assert [z for z,s in enumerate(sets) if 0 not in s]==[0]

def profile(a,b,r):
    out = []
    for w in range(6):
        c,d = A[3*w]
        out.append(tuple(u for u in range(5)
                         if a not in small(c+u*G,d,11)
                         and b not in small(c+u*G,d,31)
                         and r not in B271[w][u]))
    return tuple(s if w<3 or not out[w-3] else () for w,s in enumerate(out))

def norm(us):
    return min(tuple(tuple(sorted((u+k)%5 for u in s)) for s in us)
               for k in range(5))

profiles = {norm(profile(a,b,r))
            for a,b,r in product(range(11),range(31),range(271))}
minimal = []
for us in sorted(profiles,key=lambda s:(sum(map(len,s)),s)):
    if not any(all(set(a)>=set(b) for a,b in zip(us,v)) for v in minimal):
        minimal.append(us)
assert (len(profiles),len(minimal)) == (477,43)

fixed = {q:[small(c,d,q) if q==19 else bad(q,c,d) for c,d in A]
         for q in (19,199)}

@cache
def mask(i,q,us):
    c,d = A[i]
    out = {}
    for x,y in product(range(7),repeat=2):
        s = (set.intersection(*(bad(71,c+x*E+u*G,d) for u in us))
             if q==71 else bad(q,c+x*E,d+y*E))
        for a in s:
            out[a] = out.get(a,0) | (1<<(7*x+y))
    return out

@cache
def cover(ss,us,zero):
    live = {43,71,127,379} | ({4159} if zero else set())
    rows = []
    for q in live:
        ms = [mask(i,q,u if q==71 else ()) for i,u in zip(ss,us)]
        rows.append(set(tuple(m.get(a,0) for m in ms) for a in range(q)))
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

for zero in (False,True):
    for us in minimal:
        states = {frozenset(i for i in range(18) if us[i//3]
                            and a not in fixed[19][i]
                            and (not zero or b not in fixed[199][i]))
                  for a in range(19) for b in range(199 if zero else 1)}
        least = [s for s in states if not any(r<s for r in states)]
        assert len(least)==(21 if zero else 12)
        for s in least:
            assert any(not cover(z,tuple(us[i//3] for i in z),zero)
                       for k in (1,2) for z in combinations(sorted(s),k))

tie = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
       4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
       595123,3981071,5096867,9384251,12207031,16018507,190771747,
       28086211607,386478495679,6090817323763,42272797713043,
       625552508473588471)
panel = [q for q in range(27,272,4) if all(q%k for k in range(2,isqrt(q)+1))]
for n,c,d,gap,m2,r2,last in [
    (20393864844619,66,168082672235297,4,4,1,(271,15,53,9)),
    (1196230,4888026,1100034892482637,8,32,8,(239,32,40,120)),
]:
    def R(j,q):
        return (n-pow(3,c,q)-pow(5,d+gap*j,q))%q

    assert all(R(j,m2)==r2 and all(R(j,q) for q in (3,7,11,19,31)) for j in I)
    assert all(sum(R(j,q)==0 for j in I)<=1 for q in tie)
    lock,trace = 23**2,[]
    for q in panel:
        hits = [j for j in I if R(j,q)==0]
        if hits:
            j, = hits
            e = lcm(V,lock,q-1)
            assert e%q and pow(5,e,q*q)!=1
            def trial(x):
                return (n-pow(3,c,q**3)-pow(5,d+x*e+gap*j,q**3))%q**3
            x = next(x for x in range(2*q) if trial(x) and trial(x)%q**2==0)
            d += x*e
            trace.append((q,j,x,R(j,q**3)//q**2))
        lock = lcm(lock,q*q*(q-1))
    assert trace[-1]==last and R(15,23**3)==529
    assert all(R(j,m2)==r2 for j in I)
    assert all(R(j,q) or R(j,q*q)==0<R(j,q**3) for j in I for q in panel+[23])
print("Verified every odd deficient head and both finite controls.")
~~~
