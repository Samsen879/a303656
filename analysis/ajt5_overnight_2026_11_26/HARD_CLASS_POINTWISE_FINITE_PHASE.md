# All targets in the original hard class have 25 finite-phase centers

Every \(n\equiv372715\bmod658812\) has a 25-center finite-phase menu using the same retained two-block offsets as the [order-five construction](https://github.com/Samsen879/a303656/commit/41c2aea4f8291c94b52c039a755e0ff0f9e9a406). The theorem is for this residue class, not all targets; it does not bound the exponent sizes within the ordinary height of \(n\).

Keep \(E,J,G\) from the earlier steps and set \(P=7E/27=1629320\). For \(t=0,1,2\) use three types \((C,D)=(66+(3t+w)P,D_0+5wP)\), \(w=0,1,2\), and an auxiliary type obtained from type 2 by adding \(12P\) to \(D\). The step \(P\) is a multiple of \(22\cdot23^2\), and \(3^P=5^{5P}\bmod7\), so the raw 23 readings and passage at 7 are preserved. The first two types allow both \(u=0,4\); the latter two allow \(u=4\). The small head allows all five vertical order-five digits. The auxiliary type and type 2 have disjoint repeated-value sets at 271; use the auxiliary only when type 2 does not pass.

At nonzero residues modulo 67, rows 67, 199 and 4159 forbid at most 2, 3 and 2 of the eleven order-eleven digits. If the residue is zero at 67, only digit zero works, and both 199 and 4159 are explicitly screened. As before, 211 and 631 together forbid at most four of the five vertical order-five choices after the horizontal choice is fixed. At 71 the repeated vertical orbit is invariant under that fifth-order shift, so an order-seven cell is excluded only if every available horizontal digit is excluded there.

The exact test below enumerates the seven profiles at 271, and every eligibility set at 19 and, in the zero branch, 199. It suffices to test the 231 inclusion-minimal sets. For each, one or two charts cannot all be covered by masks coming from actual residues at the remaining primes. In each mask choice the residue at a prime is shared across the charts. Consequently at least one chart contains a passing cell for every target in the class. Select its order-eleven and order-five digits as above and prescribe the nonzero \(23^2\) remainder with the original \(L,V\) digits. The earlier tie-row restoration and ordinary-prime lift then handle an arbitrary finite ordinary panel. All retained exponent gaps are unchanged, so a common-Wieferich reader cannot kill two centers; with at most 24 such readers in a given finite panel, some center survives.

The test includes both the earlier fixed-gate failure \(102719045695\), now passing with type 1, and \(14715324182281803579383227\), whose only eligible nonauxiliary chart is fully covered and which passes via the auxiliary type. It is possible to repair ordinary primes through 271 at both displayed targets, but these are congruence certificates, not positive remainder certificates within the ordinary exponent bound.

~~~python
from collections import Counter
from functools import cache
from itertools import combinations

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
P,E,J,G = 1629320,6284520,3999240,8798328
D,L,V = 135004545737,1569603835800,36100888223400
FULL = (1<<49)-1
assert len(I) == 25 and V == 23*L
A = [(66+(3*t+min(w,2))*P,
      D+(5*min(w,2)+12*(w==3))*P)
     for w in range(4) for t in range(3)]
allowed = [(0,4),(0,4),(4,),(4,)]

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+4*j,q)) % q for j in I}

B = {q:{b for b,k in Counter(pow(5,4*j,q) for j in I).items() if k>1}
     for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b) % q for b in B[q]}

assert all(s % (22*23**2) == 0 for s in (P,E,G))
assert pow(3,P,7) == pow(5,5*P,7)
assert pow(3,J,23**3) == pow(5,5*J,23**3)
assert pow(5,L,529) == 24 and pow(5,V,23**3) == 530
assert all(pow(5,L,q) == 1 for q in Q|{7,11,19,31})
assert all(s % (q-1) == 0 for s in (E,J) for q in (7,11,19,31))
assert all(G % (q-1) == 0 for q in (7,19))
assert all(pow(b,G,q) == 1 for b in (3,5) for q in Q-{71,211,271,631})
assert all(pow(3,J,q) == pow(5,5*J,q) == 1 for q in Q-{67,199,4159})
assert all(pow(b,E,q) == 1 for b in (3,5) for q in (67,199,271))
assert all(pow(b,P,67) == 1 for b in (3,5))
assert pow(5,E,4159) == pow(5,J,4159) == 1
assert pow(5,E,71) == pow(5,5*G,71) == pow(5,G,271) == 1
assert B[71] == {pow(5,k,71) for k in range(5)}
for q in (211,631):
    assert len(B[q]) == 2 and pow(5,G,q) != 1 and pow(5,5*G,q) == 1

B271 = [{u:bad(271,A[3*w][0]+u*G,A[3*w][1]) for u in allowed[w]}
        for w in range(4)]
assert not B271[2][4] & B271[3][4]
for i,(c,d) in enumerate(A):
    w = i//3
    assert [(u,v) for u in range(5) for v in range(5)
            if all(2 not in small(c+u*G,d+v*G,q) for q in (11,31))
            ] == [(u,v) for u in allowed[w] for v in range(5)]
    assert 0 not in small(c,d,7)
    assert [j for j in I if (pow(3,c,23)+pow(5,d+4*j,23))%23 == 0] == [15]
    assert B271[w] == {u:bad(271,c+u*G,d) for u in allowed[w]}
    for q,cap in [(67,2),(199,3),(4159,2)]:
        for x in range(7 if q == 4159 else 1):
            sets = [bad(q,c+x*E+z*J,d+5*z*J) for z in range(11)]
            h = Counter(a for s in sets for a in s)
            assert max(k for a,k in h.items() if q != 67 or a) <= cap
            if q == 67:
                assert [z for z,s in enumerate(sets) if 0 not in s] == [0]

def choices(a):
    us = tuple(tuple(u for u in allowed[w] if a not in B271[w][u])
               for w in range(4))
    return us[:3]+((),) if us[2] else us

def eligible(us,a,b=None):
    return frozenset(i for i,(c,d) in enumerate(A)
                     if us[i//3] and a not in small(c,d,19)
                     and (b is None or b not in bad(199,c,d)))

def masks(us,live):
    out = {}
    for q in live:
        for i,(c,d) in enumerate(A):
            if not us[i//3]:
                continue
            h = {}
            for x in range(7):
                for y in range(7):
                    s = (set.intersection(*(bad(71,c+x*E+u*G,d)
                                             for u in us[i//3]))
                         if q == 71 else bad(q,c+x*E,d+y*E))
                    for a in s:
                        h[a] = h.get(a,0) | (1<<(7*x+y))
            out[q,i] = h
    return out

def can_cover(ss,live,h):
    rows = [Counter(tuple(h[q,i].get(a,0) for i in ss) for a in range(q))
            for q in live]
    rows.sort(key=lambda row:-max(sum(m.bit_count() for m in z) for z in row))
    lim = [[0]*len(ss) for _ in range(len(rows)+1)]
    for k in reversed(range(len(rows))):
        lim[k] = [lim[k+1][i]+max(z[i].bit_count() for z in rows[k])
                  for i in range(len(ss))]

    @cache
    def visit(k,seen):
        if all(m == FULL for m in seen):
            return True
        if any(m.bit_count()+r < 49 for m,r in zip(seen,lim[k])):
            return False
        for z in rows[k]:
            new = tuple(a|b for a,b in zip(seen,z))
            if all(m.bit_count()+r >= 49 for m,r in zip(new,lim[k+1])):
                if visit(k+1,new):
                    return True
        return False

    result = visit(0,(0,)*len(ss))
    visit.cache_clear()
    return result

profiles = {choices(a) for a in range(271)}
assert len(profiles) == 7
total = 0
for zero in (False,True):
    live = {43,71,127,379} | ({4159} if zero else set())
    for us in profiles:
        h = masks(us,live)
        states = {eligible(us,a,b) for a in range(19)
                  for b in (range(199) if zero else (None,))}
        minimal = [s for s in states if not any(r<s for r in states)]
        assert len(minimal) == (21 if zero else 12)

        @cache
        def covered(ss):
            return can_cover(ss,live,h)

        for s in minimal:
            assert any(not covered(ss)
                       for k in (1,2) for ss in combinations(sorted(s),k))
        total += len(minimal)
        covered.cache_clear()
assert total == 231

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+4*j,q)) % q

def lift(n,c,d):
    a, = [a for a in range(23) if R(n,c,d+a*L,15,529) == 0]
    b, = [b for b in range(23) if R(n,c,d+a*L+b*V,15,23**3) == 529]
    return a,b,d+a*L+b*V

n = 102719045695
assert (n%658812,n%67,n%19,n%199) == (372715,0,17,4)
assert [i for i in range(3) if 17 not in small(*A[i],19)] == [2]
assert 4 in bad(199,*A[2])
c,d = A[4]
assert c == 6517346 and lift(n,c,d) == (18,7,281094099300537)
assert all(n%q not in bad(q,c,lift(n,c,d)[2]) for q in Q)

n = 14715324182281803579383227
assert n%658812 == 372715 and n%67 == 0
us = choices(n%271)
assert eligible(us,n%19,n%199) == {0,9,11}
live = {43,71,127,379,4159}
h = masks(us,live)
covered = 0
for q in live:
    covered |= h[q,0].get(n%q,0)
assert covered == FULL
c,d = A[9]
c += 4*G
assert c == 38452018 and lift(n,c,d) == (17,14,532230740726977)
assert all(n%q not in bad(q,c,lift(n,c,d)[2]) for q in Q)
print("Verified all", total, "minimal eligibility sets and both controls.")
~~~
