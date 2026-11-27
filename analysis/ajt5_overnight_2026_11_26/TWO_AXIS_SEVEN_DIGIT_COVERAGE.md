# A two-axis order-seven chart covers 82.6140936170% of the hard class

Starting with the [three-anchor screen](https://github.com/Samsen879/a303656/commit/ccc5955c4309a3273a11afc9c2032d0e6747eb33), keep the same 25 offsets and the relative vertical block phase. At each anchor \(C_t=66+4887960t\), release two digits by adding \((xE,yE)\) to the horizontal and vertical exponents, where \(E=6284520\) and \(0\le x,y<7\). These digits protect the reading at 19, the small head, and the complete \(23^3\) reading. In each chart the repeated values at \(67,199,271\) also stay fixed; the seven other screen rows \(43,71,127,211,379,631,4159\) are tested jointly. Any passing cell extends by the previous restoration and finite ordinary repair. The retained differences are unchanged, so the same common-Wieferich non-reuse proof applies.

There cannot be a private digit at 127 preserving every raw offset sum at the other rows. Subtracting the sums at indices 0 and 2 at 43 fixes the vertical power there, forcing \(42\mid\Delta D\). At 379 the same subtraction fixes the vertical power there, and then any one sum fixes the horizontal power there, forcing \(378\mid\Delta C\). The corresponding orders at 127 are 126 and 42, so its two powers stay fixed.

The prior failing target \(666510287684337524321867834203\) now passes. Only anchor \(t=2\) passes the fixed rows; on \(x=0\), \(y=6\) is the unique passing digit. The old double hit at 127 is reduced to one, and the ordinary repairs through 211 are at 107, 127 and 191. The reading at 43 changes without losing passage. At \(76123543771891597903165812612079\), by contrast, the six variable rows other than 127 kill 39 of the only eligible chart's 49 cells, and row 127 kills all ten that are left. This is a failure of this fixed menu, not of other exponent choices.

For the coverage calculation, a target first selects the set of anchors passing the fixed rows \(19,67,199,271\). For each variable prime and residue, assign a 49-bit mask on each eligible anchor, using the same residue at that prime for every anchor. The tuple fails exactly when unions of masks cover all cells in every eligible chart. The digit at 23 does not change these row counts because \(5^{V/23}=1\) in the screen rows. CRT and the standalone exact mask count give relative coverage \(242896793992697308048200/294013749177862311473033\) within the hard residue class. The ceiling from the fixed rows alone is \(2985048/3613243\); the variable rows cost only about \(1.26\cdot10^{-8}\) in relative density. Improvement from these digits is a finite-phase result, with no ordinary exponent-height bound.

~~~python
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations
from math import isqrt, lcm, prod

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
A, X = {67,199,271}, Q-{67,199,271}
C = [66+t*4887960 for t in range(3)]
D, L, E = 135004545737, 1569603835800, 6284520
V, M, FULL = 23*L, 658812, (1<<49)-1

def order(b,q):
    return next(k for k in range(1,q) if (q-1)%k==0 and pow(b,k,q)==1)

for b in (3,5):
    assert lcm(3960,23**2,*(order(b,q) for q in Q-{127})) == 7*E
    assert {q for q in Q if pow(b,E,q)==1} == (
        A if b==3 else A|{71,4159})
assert (order(5,43),order(3,379),order(3,127),order(5,127)) == (42,378,126,42)
assert E%(22*23**2)==0 and all(E%(p-1)==0 for p in (7,11,19,31))
assert all(pow(5,L,q)==1 for q in Q|{19})
assert pow(5,L,529)==24 and pow(5,V,23**3)==1+23**2

B = {q:{v for v,k in Counter(pow(5,4*j,q) for j in I).items() if k>1}
     for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*v)%q for v in B[q]}

def frozen(q,t):
    if q==19:
        return {(pow(3,C[t],q)+pow(5,D+4*j,q))%q for j in I}
    return bad(q,C[t],D)

def masks(t,q):
    d = {}
    for x in range(7):
        for y in range(7):
            for a in bad(q,C[t]+x*E,D+y*E):
                d[a] = d.get(a,0) | (1<<(7*x+y))
    return d

U = {(t,q):masks(t,q) for t in range(3) for q in X}

def cover(ts):
    rows = [(q,Counter(tuple(U[t,q].get(a,0) for t in ts) for a in range(q)))
            for q in X]
    rows.sort(key=lambda row:-max(sum(v.bit_count() for v in m)
                                 for m in row[1]))
    limits = [[0]*len(ts) for _ in range(len(rows)+1)]
    suffix = [1]*(len(rows)+1)
    for k in reversed(range(len(rows))):
        q,h = rows[k]
        suffix[k] = suffix[k+1]*q
        limits[k] = [limits[k+1][i]+max(m[i].bit_count() for m in h)
                     for i in range(len(ts))]
    @cache
    def step(k,seen):
        if all(v==FULL for v in seen):
            return suffix[k]
        if any(v.bit_count()+r<49 for v,r in zip(seen,limits[k])):
            return 0
        total = 0
        for m,w in rows[k][1].items():
            z = tuple(v|a for v,a in zip(seen,m))
            if all(v.bit_count()+r>=49 for v,r in zip(z,limits[k+1])):
                total += w*step(k+1,z)
        return total
    out = step(0,(0,)*len(ts))
    step.cache_clear()
    return out

def overlap(ts):
    return prod(1-F(len(set.union(*(frozen(q,t) for t in ts))),q)
                for q in A|{19})

expected = [17658022886,88043024,2785075142,0,997821,56,0]
rho, ceiling = F(0), F(0)
for i,ts in enumerate(t for k in (1,2,3) for t in combinations(range(3),k)):
    other = [t for t in range(3) if t not in ts]
    p = sum((-1)**k*overlap(ts+s) for k in range(len(other)+1)
            for s in combinations(other,k))
    a = cover(ts)
    assert a==expected[i]
    rho += p*(1-F(a,prod(X)))
    ceiling += p
assert rho==F(242896793992697308048200,294013749177862311473033)
assert ceiling==F(2985048,3613243)

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+4*j,q))%q

def eligible(n):
    return [t for t in range(3) if
            all(n%q not in frozen(q,t) for q in A|{19})]

def lift(n):
    a, = [a for a in range(23) if R(n,66,D+a*L,15,529)==0]
    return a

N = 666510287684337524321867834203
N2 = 76123543771891597903165812612079
for n in (N,N2):
    assert n%M==372715 and eligible(n)==[2] and lift(n)==14

d = D+14*L
assert [j for j in I if R(N,C[2],d,j,127)==0]==[0,21]
assert [y for y in range(7)
        if all(N%q not in bad(q,C[2],d+y*E) for q in Q)]==[6]
assert [R(N,C[2],d+y*E,0,43) for y in (0,6)]==[41,40]
d += 6*E
assert (C[2],d)==(9775986,22109495954057)
assert R(N,C[2],d,15,23**3)==20*23**2

m = {q:U[2,q].get(N2%q,0) for q in X}
assert m[127].bit_count()==35
w = 0
for q in X-{127}:
    w |= m[q]
assert w.bit_count()==39 and (w|m[127])==FULL

T = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
     4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
     595123,3981071,5096867,9384251,12207031,16018507,190771747,
     28086211607,386478495679,6090817323763,42272797713043,
     625552508473588471)
assert all(sum(R(N,C[2],d,j,q)==0 for j in I)<=1 for q in T)
assert all(R(N,C[2],d,j,4)==1 and all(R(N,C[2],d,j,q) for q in (3,7,11,19,31))
           for j in I)

old, trace = 23**2, []
P = [q for q in range(27,212,4) if all(q%a for a in range(2,isqrt(q)+1))]
for q in P:
    roots = [j for j in I if R(N,C[2],d,j,q)==0]
    if roots:
        j, = roots
        e = lcm(V,old,q-1)
        assert e%q and pow(5,e,q*q)!=1
        x = next(x for x in range(2*q)
                 if R(N,C[2],d+x*e,j,q*q)==0 < R(N,C[2],d+x*e,j,q**3))
        d += x*e
        trace.append((q,j,x,R(N,C[2],d,j,q**3)//q**2))
    old = lcm(old,q*q*(q-1))
assert trace==[(107,5,73,96),(127,15,64,27),(191,9,110,11)]
assert all(R(N,C[2],d,j,q) or R(N,C[2],d,j,q*q)==0 < R(N,C[2],d,j,q**3)
           for j in I for q in P+[23])
print(rho, trace)
~~~
