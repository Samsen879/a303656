# The order-eleven digit raises hard-class coverage to 97.4123583778%

Keep the [147-phase order-seven chart](https://github.com/Samsen879/a303656/commit/220c01780bed7204871553beb26b6517bf6df467) and the two-block retained offsets. With \(E=6284520\), add \((zJ,5zJ)\) to \((C,D)\), \(J=7E/11\), \(0\le z<11\). Among the ten screen rows this changes only 67, 199 and 4159. The identity \(3^J=5^{5J}=12125\bmod23^3\) scales all raw offset sums at 23 by the same unit when choosing the digit. Since \(n\equiv0\bmod23\), the retained hit at \(j=15\) stays the only hit modulo 23. Choose the two base-5 digits afterwards by adding \(aL+bV\), where \(V=23L\) as in the prior chart. These digits preserve the screen and can prescribe the exact remainder \(23^2\bmod23^3\) at that one hit. The common-Wieferich non-reuse argument is unchanged because the offset differences are unchanged.

When \(n\not\equiv0\bmod67\), each of 67, 199 and 4159 forbids at most two order-eleven digits, uniformly for each surviving order-seven cell. Thus the exact screen for this branch tests only fixed rows 19 and 271 and variable rows 43, 71, 127, 211, 379 and 631. The CRT mask count below gives conditional relative coverage \(\rho_+=98138422400428872/100740578764157441\). When \(n\equiv0\bmod67\), only \(z=0\) passes the row, and zero was among the 57 old allowed residues common to all anchors at 67. With old relative coverage \(\rho_0\), the new exact relative coverage is \((66/67)\rho_++\rho_0/57=5441708813555847004712232/5586261234379383917987627\).

All prior restoration steps and the ordinary finite repair still apply after passing the screen, with the \(V\)-digit available to restore the \(23^3\) value if the paired step changes the top digit. At \(6960835\) the old chart always hits both \(j=14,3\) at 67; \(z=1\) has units at all 40 tie rows and the repair through 211 has one hit at 131. At \(128182243\) all current phases still hit \(j=32,5\) at 271. Their vertical gap, 108, gives exact valuation one for the difference, so a repair preserving the first readings cannot make both valuations even. This unchanged row rejects \(7/271\) of the hard class in this menu. No positive-height or general conjecture claim.

~~~python
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations
from math import isqrt, lcm, prod

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
X = Q-{67,199,271}
C = [66+t*4887960 for t in range(3)]
D, L, E, J = 135004545737, 1569603835800, 6284520, 3999240
V, FULL = 23*L, (1<<49)-1
assert 11*J == 7*E
assert pow(3,J,23**3) == pow(5,5*J,23**3) == 12125
assert E % (22*23**2) == 0
assert all(J % (q-1) == E % (q-1) == 0 for q in (7,11,19,31))
assert pow(5,L,529) == 24 and pow(5,V,23**3) == 1+529
assert all(pow(5,L,q) == 1 for q in Q|{19})
assert all(pow(3,J,q) == pow(5,5*J,q) == 1 for q in Q-{67,199,4159})
assert all(pow(3,E,q) == pow(5,E,q) == 1 for q in (67,199,271))
assert pow(5,J,4159) == pow(5,E,4159) == 1

B = {q:{v for v,k in Counter(pow(5,4*j,q) for j in I).items() if k>1}
     for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*v) % q for v in B[q]}

def fixed(q,t):
    if q == 19:
        return {(pow(3,C[t],q)+pow(5,D+4*j,q)) % q for j in I}
    return bad(q,C[t],D)

def counts(q,t,x=0):
    return Counter(v for z in range(11)
                   for v in bad(q,C[t]+x*E+z*J,D+5*z*J))

for t in range(3):
    assert [z for z in range(11)
            if 0 not in bad(67,C[t]+z*J,D+5*z*J)] == [0]
    assert max(k for v,k in counts(67,t).items() if v) == 2
    assert max(counts(199,t).values()) == 2
    assert all(max(counts(4159,t,x).values()) <= 2 for x in range(7))
    assert fixed(67,t) == fixed(67,0)
    assert fixed(271,t) == {56,60,122,127,154,212,219}
assert len(fixed(67,0)) == 10

def masks(t,q):
    out = {}
    for x in range(7):
        for y in range(7):
            for v in bad(q,C[t]+x*E,D+y*E):
                out[v] = out.get(v,0) | 1<<(7*x+y)
    return out

U = {(t,q):masks(t,q) for t in range(3) for q in X}

def covers(ts,live):
    rows = [(q,Counter(tuple(U[t,q].get(v,0) for t in ts)
                      for v in range(q))) for q in live]
    rows.sort(key=lambda item:-max(sum(m.bit_count() for m in z)
                                  for z in item[1]))
    lim = [[0]*len(ts) for _ in range(len(rows)+1)]
    suffix = [1]*(len(rows)+1)
    for k in reversed(range(len(rows))):
        q,h = rows[k]
        suffix[k] = suffix[k+1]*q
        lim[k] = [lim[k+1][i]+max(z[i].bit_count() for z in h)
                  for i in range(len(ts))]

    @cache
    def step(k,seen):
        if all(m == FULL for m in seen):
            return suffix[k]
        if any(m.bit_count()+b < 49 for m,b in zip(seen,lim[k])):
            return 0
        total = 0
        for z,w in rows[k][1].items():
            new = tuple(a|b for a,b in zip(seen,z))
            if all(m.bit_count()+b >= 49 for m,b in zip(new,lim[k+1])):
                total += w*step(k+1,new)
        return total

    n = step(0,(0,)*len(ts))
    step.cache_clear()
    return n

def measure(frozen,live,expected):
    def overlap(ts):
        return prod(1-F(len(set.union(*(fixed(q,t) for t in ts))),q)
                    for q in frozen|{19})
    r = F(0)
    subsets = (s for k in (1,2,3) for s in combinations(range(3),k))
    for i,ts in enumerate(subsets):
        other = [t for t in range(3) if t not in ts]
        p = sum((-1)**k*overlap(ts+s) for k in range(len(other)+1)
                for s in combinations(other,k))
        a = covers(ts,live)
        assert a == expected[i]
        r += p*(1-F(a,prod(live)))
    return r

old = measure({67,199,271},X,[17658022886,88043024,2785075142,0,997821,56,0])
plus = measure({271},X-{4159},[3938865,622,577927,0,96,0,0])
assert old == F(242896793992697308048200,294013749177862311473033)
assert plus == F(98138422400428872,100740578764157441)
rho = F(66,67)*plus+old/57
assert rho == F(5441708813555847004712232,5586261234379383917987627)

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+4*j,q)) % q

n = 6960835
assert n%658812 == 372715 and n%67 == 4
assert all(n%67 in fixed(67,t) for t in range(3))
assert [j for j in I if not R(n,66,D,j,67)] == [14,3]
c,d = 66+J,D+5*J
a, = [a for a in range(23) if R(n,c,d+a*L,15,529) == 0]
b, = [b for b in range(23) if R(n,c,d+a*L+b*V,15,23**3) == 529]
d += a*L+b*V
assert (a,b,c,d) == (16,1,3999306,61349574138137)
assert [j for j in I if not R(n,c,d,j,23)] == [15]
assert all(R(n,c,d,j,4) == 1 and all(R(n,c,d,j,q) for q in (3,7,11,19,31))
           for j in I)

n2 = 128182243
assert n2%658812 == 372715 and n2%271 == 56
assert [j for j in I if not R(n2,66,D,j,271)] == [32,5]
assert pow(5,108,271**2) == 33063

T = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
     4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
     595123,3981071,5096867,9384251,12207031,16018507,190771747,
     28086211607,386478495679,6090817323763,42272797713043,
     625552508473588471)
assert all(R(n,c,d,j,q) for j in I for q in T)

P = [q for q in range(27,212,4) if all(q%k for k in range(2,isqrt(q)+1))]
lock, trace = 23**2,[]
for q in P:
    roots = [j for j in I if R(n,c,d,j,q) == 0]
    if roots:
        j, = roots
        e = lcm(V,lock,q-1)
        assert e%q and pow(5,e,q*q) != 1
        x = next(x for x in range(2*q)
                 if R(n,c,d+x*e,j,q*q) == 0 < R(n,c,d+x*e,j,q**3))
        d += x*e
        trace.append((q,j,x,R(n,c,d,j,q**3)//q**2))
    lock = lcm(lock,q*q*(q-1))
assert trace == [(131,9,68,40)]
assert R(n,c,d,15,23**3) == 529
assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q) == 0 < R(n,c,d,j,q**3)
           for j in I for q in P+[23])
print(rho, trace)
~~~
