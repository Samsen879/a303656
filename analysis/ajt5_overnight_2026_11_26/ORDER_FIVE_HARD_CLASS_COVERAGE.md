# The order-five digit raises hard-class coverage to 99.99526300044815%

Keep the [order-eleven construction](https://github.com/Samsen879/a303656/commit/5d27927fd33b16de1a27eef9c02d04e2edff69fd) and add \((uG,vG)\) to \((C,D)\), where \(G=7E/5=8798328\) and \(u,v\) range over \(0,\ldots,4\). The small head at 11 and 31 permits exactly \(u=0,4\) and all five \(v\). Since \(22\cdot23^2\mid G\), the exact \(23^3\) readings are preserved. Among the ten screen rows the new digits change only 71, 211, 271 and 631, leaving the order-eleven gate at 67 intact. All retained offset gaps and the non-reuse conclusion are unchanged.

At 271 the vertical digit is trivial and the two horizontal forbidden sets are disjoint and of size seven. Therefore every residue allows at least one horizontal choice. At 71 the repeated vertical values form an order-five subgroup, so its forbidden set for a fixed horizontal choice is unchanged by \(v\). At 211 and 631 the vertical digit has order five and there are two repeated values each; jointly they can exclude at most four vertical choices after fixing \(u\). Thus 211 and 631 need not be included in the remaining mask count.

Condition on whether 271 permits one choice (weight \(14/271\), with either singleton giving the same result) or both (\(257/271\)). For the former the conditional rates are \(2792050910/2792050931\) and \(32443405908313/32546701754701\) for nonzero and zero modulo 67 respectively. For the latter they are \(1\) and \(2303481841520119/2310815824583771\). CRT and the weights \(66/67,1/67\) give exact relative coverage \(41955495401189315847/41957482926967530047\).

The old 271 failure \(128182243\) is repaired: the replay gives only one hit at 271, which is lifted to exact remainder \(140\cdot271^2\bmod271^3\). The new negative control \(102719045695\) has residues \(0,17,4\) at 67, 19 and 199: 67 forces the order-eleven digit to zero, 19 permits only anchor 2, and 199 then excludes it. The analogous fixed triple rejects \(12/(67\cdot19\cdot199)\) of the hard class. All other failures of this menu have relative mass \(16372885868/41957482926967530047\). This is finite-phase coverage only.

~~~python
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations
from math import isqrt, lcm, prod

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
C = [66+t*4887960 for t in range(3)]
D, E, J, G = 135004545737, 6284520, 3999240, 8798328
L, M = 1569603835800, 658812
V, FULL = 23*L, (1<<49)-1
assert len(I) == 25 and 5*G == 11*J == 7*E
assert G % (22*23**2) == 0
assert pow(3,J,23**3) == pow(5,5*J,23**3)
assert pow(5,L,529) == 24 and pow(5,V,23**3) == 530
assert all(pow(5,L,q) == 1 for q in Q|{19})
assert all(G % (q-1) == 0 for q in (7,19))
assert all(E%(q-1) == J%(q-1) == L%(q-1) == 4887960%(q-1) == 0
           for q in (11,31))
assert all(pow(3,G,q) == pow(5,G,q) == 1 for q in Q-{71,211,271,631})
assert all(pow(3,J,q) == pow(5,5*J,q) == 1 for q in Q-{67,199,4159})
assert all(pow(3,E,q) == pow(5,E,q) == 1 for q in (67,199,271))
assert pow(5,E,4159) == pow(5,J,4159) == 1

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+4*j,q)) % q

B = {q:{v for v,k in Counter(pow(5,4*j,q) for j in I).items() if k>1}
     for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b) % q for b in B[q]}

def fixed(q,t):
    if q == 19:
        return {(pow(3,C[t],q)+pow(5,D+4*j,q)) % q for j in I}
    return bad(q,C[t],D)

assert [(u,v) for u in range(5) for v in range(5)
        if all(R(2,66+u*G,D+v*G,j,q) for q in (11,31) for j in I)
        ] == [(u,v) for u in (0,4) for v in range(5)]
for q in (211,631):
    assert len(B[q]) == 2 and pow(5,G,q) != 1 and pow(5,5*G,q) == 1
assert B[71] == {pow(5,k,71) for k in range(5)}
assert pow(3,4887960,71) == pow(5,E,71) == pow(5,5*G,71) == 1
assert pow(5,G,271) == pow(3,4887960,271) == 1
b0,b4 = [bad(271,66+u*G,D) for u in (0,4)]
assert b0 == {56,60,122,127,154,212,219}
assert b4 == {5,113,117,179,184,211,269}

def zcount(q,t,x=0):
    return Counter(a for z in range(11)
                   for a in bad(q,C[t]+x*E+z*J,D+5*z*J))

for t in range(3):
    assert [z for z in range(11)
            if 0 not in bad(67,C[t]+z*J,D+5*z*J)] == [0]
    assert max(k for a,k in zcount(67,t).items() if a) == 2
    assert max(zcount(199,t).values()) == 2
    assert all(max(zcount(4159,t,x).values()) <= 2 for x in range(7))

def mask(t,q,us):
    out = {}
    for x in range(7):
        for y in range(7):
            values = (set.intersection(*(bad(q,C[t]+x*E+u*G,D) for u in us))
                      if q == 71 else bad(q,C[t]+x*E,D+y*E))
            for a in values:
                out[a] = out.get(a,0) | (1<<(7*x+y))
    return out

def measure(us,zero):
    live = {43,71,127,379} | ({4159} if zero else set())
    frozen = {19,199} if zero else {19}
    U = {(t,q):mask(t,q,us) for t in range(3) for q in live}

    def cover(ts):
        rows = [(q,Counter(tuple(U[t,q].get(a,0) for t in ts)
                           for a in range(q))) for q in live]
        rows.sort(key=lambda p:-max(sum(m.bit_count() for m in z)
                                    for z in p[1]))
        lim = [[0]*len(ts) for _ in range(len(rows)+1)]
        rest = [1]*(len(rows)+1)
        for k in reversed(range(len(rows))):
            q,h = rows[k]
            rest[k] = rest[k+1]*q
            lim[k] = [lim[k+1][i]+max(m[i].bit_count() for m in h)
                      for i in range(len(ts))]

        @cache
        def step(k,seen):
            if all(m == FULL for m in seen):
                return rest[k]
            if any(m.bit_count()+b < 49 for m,b in zip(seen,lim[k])):
                return 0
            total = 0
            for m,w in rows[k][1].items():
                new = tuple(a|b for a,b in zip(seen,m))
                if all(a.bit_count()+b >= 49 for a,b in zip(new,lim[k+1])):
                    total += w*step(k+1,new)
            return total

        ans = step(0,(0,)*len(ts))
        step.cache_clear()
        return ans

    def overlap(ts):
        return prod(1-F(len(set.union(*(fixed(q,t) for t in ts))),q)
                    for q in frozen)

    ans = F(0)
    for size in (1,2,3):
        for ts in combinations(range(3),size):
            other = [t for t in range(3) if t not in ts]
            p = sum((-1)**k*overlap(ts+s) for k in range(len(other)+1)
                    for s in combinations(other,k))
            ans += p*(1-F(cover(ts),prod(live)))
    return ans

single = (F(2792050910,2792050931),F(32443405908313,32546701754701))
both = (F(1),F(2303481841520119,2310815824583771))
rho = F(0)
for us,mass,want in [((0,),7,single),((4,),7,single),((0,4),257,both)]:
    a,b = measure(us,False),measure(us,True)
    assert (a,b) == want
    rho += F(mass,271)*(66*a+b)/67
assert rho == F(41955495401189315847,41957482926967530047)
assert 1-rho-F(12,67*19*199) == F(16372885868,41957482926967530047)

n = 128182243
assert n%M == 372715 and n%67 == 54 and n%271 in b0-b4
assert [j for j in I if not R(n,66,D,j,271)] == [32,5]
c,d = C[1]+4*G+J,D+5*J
a, = [a for a in range(23) if R(n,c,d+a*L,15,529) == 0]
b, = [b for b in range(23) if R(n,c,d+a*L+b*V,15,23**3) == 529]
d += a*L+b*V
assert (a,b,c,d) == (16,6,44080578,241854015255137)
assert [j for j in I if not R(n,c,d,j,271)] == [17]
assert [j for j in I if not R(n,c,d,j,23)] == [15]
assert all(R(n,c,d,j,4) == 1 and all(R(n,c,d,j,q) for q in (3,7,11,19,31))
           for j in I)

n2 = 102719045695
assert (n2%M,n2%67,n2%19,n2%199) == (372715,0,17,4)
assert [t for t in range(3) if n2%19 not in fixed(19,t)] == [2]
assert n2%199 in fixed(199,2)

T = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
     4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
     595123,3981071,5096867,9384251,12207031,16018507,190771747,
     28086211607,386478495679,6090817323763,42272797713043,
     625552508473588471)
assert all(sum(R(n,c,d,j,q)==0 for j in I) <= 1 for q in T)
panel = [q for q in range(27,272,4) if all(q%k for k in range(2,isqrt(q)+1))]
lock, trace = 23**2, []
for q in panel:
    hits = [j for j in I if R(n,c,d,j,q) == 0]
    if hits:
        j, = hits
        e = lcm(V,lock,q-1)
        assert e%q and pow(5,e,q*q) != 1
        x = next(x for x in range(2*q)
                 if R(n,c,d+x*e,j,q*q) == 0 < R(n,c,d+x*e,j,q**3))
        d += x*e
        trace.append((q,j,x,R(n,c,d,j,q**3)//q**2))
    lock = lcm(lock,q*q*(q-1))
assert trace[-1] == (271,17,110,140)
assert R(n,c,d,15,23**3) == 529
assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q) == 0 < R(n,c,d,j,q**3)
           for j in I for q in panel+[23])
print(rho, trace)
~~~
