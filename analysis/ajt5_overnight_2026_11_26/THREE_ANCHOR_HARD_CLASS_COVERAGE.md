# Three anchors cover 55.1042% of the hard class with 25 centers

Use the same retained two-block offsets, axis locks, and \(23\)-digit recipe as [the 25.2563% construction](https://github.com/Samsen879/a303656/commit/613f33622f5a03b1ecca3242e60eee3669da553e). The hard class is \(n\equiv372715\bmod658812\). Choose one of the horizontal exponents \(66+4887960t\), \(t=0,1,2\); their differences preserve the \(23^3\) reading. At 19, the three respective forbidden sets are \(\{1,8,9,15,16,17\}\), \(\{5,6,7,10,17,18\}\), and \(\{4,5,11,12,13,16\}\), with empty triple intersection. For each anchor screen only the units at 19 and the repeated hits at
\[
Q=\{43,67,71,127,199,211,271,379,631,4159\}.
\]
Accept if at least one anchor passes. This rule contains the prior event. Conditional on the \(23\)-digit, CRT factors each joint anchor probability row by row. Indeed at each \(q\in Q\), either \(5^{V/23}=1\) or the three horizontal shifts are equal, so changing the digit preserves the union size of any selected anchors' forbidden sets. Inclusion-exclusion gives the exact relative density \(162014025558392184545280/294013749177862311473033\).

Here is why the other tie rows need not be screened. Write \(B_q\) for the repeated vertical values at \(q\), \(O_q=\operatorname{ord}_q(3)\), and \(H=\operatorname{lcm}(3960,23^2)\). The replay chooses and removes groups of current rows \(S=\{q:v_\ell(O_q)\ge k\}\) for which \(k>v_\ell(H)\) and
\[
\sum_{q\in S}|B_q|\,\ell^{-(v_\ell(O_q)-k+1)}<1.
\]
Restore these groups in reverse order after restoring the four special rows. At a given group the horizontal step locks \(H\) and all currently restored orders, hence has \(\ell\)-valuation below \(k\). On the period of this step at any \(q\), the fraction of forbidden digits is at most the corresponding summand. Their sum being below one leaves a simultaneous digit. This restores 25 rows.

The four special rows are first restored in this order: 163 and 487 each have a private horizontal order-three digit, and the exact nonsquare-ratio check loses at most two of its three choices. Then a shared digit changes \((C,D)\) by \((xE,(16x\bmod23)E)\), with \(E\) in the replay. The Fermat quotients at 23 are 17 and 14, and \(14\cdot16\equiv17\bmod23\), so the root at 23 still vanishes modulo \(23^2\). At 47 the values \(\lambda z+bz^{10}\) forbid at most six choices, and at 31051 the horizontal orbit forbids at most seven. This leaves a shared digit, and adding \(V\) if needed restores exact valuation two at 23. The earlier two-axis locks then permit all ordinary finite repairs, and the same cross-block difference bound permits at most one hit per genuine common-Wieferich row.

The replay restores 25 centers at \(1031527\), previously rejected, and processes the panel through 211. The target \(666510287684337524321867834203\) still defeats the selected anchors: the first two fail at 19 and the third hits indices \(0,21\) at 127 with difference of exact valuation one, so a later step preserving those readings cannot repair both. This is a control for the current screen, not a claim about other menus or positive remainders within ordinary height.

~~~python
from collections import Counter
from fractions import Fraction as Fq
from functools import cache
from itertools import combinations
from math import gcd, isqrt, lcm, prod

F = {
    1:(2,2,2,3), 3:(3,7,31), 5:(11,71,521), 7:(29,449,19531),
    9:(3,19,829,5167), 11:(23,67,5281,12207031),
    13:(5227,38923,305175781), 15:(61,181,1741,7621),
    17:(409,3061,41540861,466344409), 19:(191,761,6271,19609,3981071,213029),
    21:(7,43,127,379,7603,519499), 23:(47,8971,42272797713043,332207361361),
    25:(101,251,401,1901,9384251,50150933101),
    27:(3,109,163,271,487,4159,31051,16018507),
    29:(59,35671,5096867,22125996444329,6090817323763),
    31:(1303,1861,21207101,28086211607,625552508473588471),
    33:(199,595123,190771747,386478495679),
    35:(211,631,4201,15216601,85280581,4698932281),
}
W = {
    42272797713043:(13967,4523), 332207361361:(9781,293),
    50150933101:(201167,277), 22125996444329:(13624382047,),
    6090817323763:(2061161,37), 28086211607:(453003413,),
    625552508473588471:(391337,25654001), 386478495679:(5855734783,),
}
A = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,
     911,1367,3701,4523,13967,37537,87877,391337,2061161,25654001,
     453003413,5855734783)

@cache
def prime(n):
    if n not in W:
        return n > 1 and all(n % d for d in range(2,isqrt(n)+1))
    u = prod(W[n])
    return (u*u > n and (n-1) % u == 0 and pow(2,n-1,n) == 1
            and all(prime(d) and gcd(pow(2,(n-1)//d,n)-1,n) == 1
                    for d in W[n]))

T = set()
for m in range(1,36,2):
    f = Counter(q for d,fs in F.items() if m % d == 0 for q in fs)
    assert all(map(prime,f)) and prod(q**v for q,v in f.items()) == 5**(2*m)-1
    assert all(v == 1 for q,v in f.items() if q > 23)
    T.update(q for q in f if q > 23 and q % 4 == 3)
assert len(T) == 40 and 31 in T and all(map(prime,A))

@cache
def order(b,q):
    o, u = q-1, q-1
    for a in A:
        while u % a == 0:
            u //= a
        while o % a == 0 and pow(b,o//a,q) == 1:
            o //= a
    assert u == 1
    return o

V = lcm(3960,*(2*m for m in F))
L, H = V//23, lcm(3960,23**2)
assert V == 23*L and all(L % (p-1) == 0 for p in (7,11,19,23,31))
assert pow(5,L,529) == 24 and pow(5,V,23**3) == 1+23**2
assert all(pow(5,V,q) == 1 for q in T)
assert [p for p in range(27,36,4) if prime(p) and V % p == 0] == [31]
assert all(pow(5,p-1,p*p) != 1 for p in A if p > 31 and p % 4 == 3)

J = list(range(0,33,2)) + list(range(-3,36,2))
I = [j for j in J if j % 3 != 1 and j != 26]
assert len(I) == 25
D0, K = 135004545737, 4887960
Cs = [66+t*K for t in range(3)]
assert K % 18 == 6 and K % (22*23**2) == 0
assert all(K % (p-1) == 0 for p in (7,11,31))

def R(n,c,d,j,m):
    return (n-pow(3,c,m)-pow(5,d+4*j,m)) % m

def repeated(q):
    return {b for b,v in Counter(pow(5,4*j % order(5,q),q)
                                 for j in I).items() if v > 1}

O = {q:order(3,q) for q in T-{31}}
B = {q:repeated(q) for q in O}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b) % q for b in B[q]}

def row19(c,d):
    return {(pow(3,c,19)+pow(5,d+4*j,19)) % 19 for j in I}

def val(n,p):
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e

# Remove groups using the exact order budget.
Q14, log = set(O), []
while True:
    opts = []
    for ell in A:
        for k in {val(O[q],ell) for q in Q14}:
            if k <= val(H,ell):
                continue
            S = tuple(sorted(q for q in Q14 if val(O[q],ell) >= k))
            w = sum(Fq(len(B[q]),ell**(val(O[q],ell)-k+1)) for q in S)
            if w < 1:
                opts.append((len(S),-w,-ell,k,S))
    if not opts:
        break
    _, _, negell, k, S = max(opts)
    log.append((-negell,k,S))
    Q14 -= set(S)
assert len(log) == 15 and len(Q14) == 14
Q12 = Q14-{47,31051}
Q = Q12-{163,487}
assert Q == {43,67,71,127,199,211,271,379,631,4159}

assert not set.intersection(*(row19(c,D0) for c in Cs))
assert all(pow(5,L,q) == 1 or pow(3,K,q) == 1 for q in Q)
rho = Fq(0)
for size in (1,2,3):
    for cs in combinations(Cs,size):
        a = 1-Fq(len(set.union(*(row19(c,D0) for c in cs))),19)
        a *= prod(1-Fq(len(set.union(*(bad(q,c,D0) for c in cs))),q) for q in Q)
        rho += (-1)**(size+1)*a
assert rho == Fq(162014025558392184545280,294013749177862311473033)

for q in (163,487):
    G = {pow(3,k*(O[q]//3),q) for k in range(3)}
    assert len(G) == 3 and pow(5,(q-1)//2,q) == q-1
    assert max(max(Counter((a*z+b) % q for z in G for b in B[q]).values())
               for a in range(1,q) if pow(a,(q-1)//2,q) == q-1) == 2

E = lcm(3960,O[31051]//23,*(order(b,q) for q in Q12 for b in (3,5)))
assert E % 23 and E % 22 == 0
assert [(pow(b,22,529)-1)//23 for b in (3,5)] == [17,14]
assert 14*16 % 23 == 17
assert O[47]//gcd(O[47],E) == O[31051]//gcd(O[31051],E) == 23
assert pow(5,E,31051) == 1 and pow(5,16*E,47) == pow(3,10*E,47)
G = {pow(3,E*x,47) for x in range(23)}
assert len(G) == 23 and len(B[31051]) == 7
assert max(max(Counter(s for z in G for s in
                       {(a*z+b*pow(z,10,47)) % 47 for b in B[47]}).values())
           for a in range(1,47)) == 6

def heads(n):
    assert n % 658812 == 372715
    y, = [y for y in range(23) if not R(n,66,D0+y*L,15,529)]
    d = D0+y*L
    return y,d,[t for t,c in enumerate(Cs)
                if n % 19 not in row19(c,d)
                and all(n % q not in bad(q,c,d) for q in Q)]

def restore(n):
    y,d,ts = heads(n)
    c = Cs[ts[0]]
    if not R(n,c,d,15,23**3):
        d += V
    have = set(Q)
    for q in (163,487):
        e = lcm(H,*(O[p] for p in have))
        assert O[q]//gcd(O[q],e) == 3
        c += e*next(x for x in range(3) if n % q not in bad(q,c+x*e,d))
        have.add(q)
    x = next(x for x in range(23) if all(
        n % q not in bad(q,c+x*E,d+(16*x % 23)*E) for q in (47,31051)))
    c += x*E
    d += (16*x % 23)*E
    if not R(n,c,d,15,23**3):
        d += V
    have.update((47,31051))
    for ell,k,S in reversed(log):
        e = lcm(H,*(O[p] for p in have))
        assert val(e,ell) < k
        periods = [O[q]//gcd(O[q],e) for q in S]
        assert sum(Fq(len(B[q]),p) for q,p in zip(S,periods)) < 1
        c += e*next(x for x in range(lcm(*periods))
                    if all(n % q not in bad(q,c+x*e,d) for q in S))
        have.update(S)
    assert all(n % q not in bad(q,c,d) for q in O)
    assert all(R(n,c,d,j,p) for j in I for p in (3,4,7,11,19,31))
    assert R(n,c,d,15,529) == 0 < R(n,c,d,15,23**3)
    return c,d

def panel(n,c,d):
    P = [p for p in range(27,212,4) if prime(p)]
    old,trace = 23**2,[]
    for p in P:
        roots = [j for j in I if not R(n,c,d,j,p)]
        assert len(roots) <= 1
        if roots:
            j, = roots
            e = lcm(V,old,p-1)
            assert e % p and pow(5,e,p*p) != 1
            t = next(t for t in range(2*p)
                     if not R(n,c,d+t*e,j,p*p) and R(n,c,d+t*e,j,p**3))
            d += t*e
            trace.append(p)
        old = lcm(old,p*p*(p-1))
    assert all(R(n,c,d,j,p) or
               (not R(n,c,d,j,p*p) and R(n,c,d,j,p**3))
               for j in I for p in P+[23])
    return trace

n = 1031527
assert heads(n)[0::2] == (14,[2])
assert [R(n,66,D0+14*L,j,361) for j in (12,30,3,21)] == [152,95,0,304]
assert restore(n) == (9775986,22109458246937)
assert panel(n,*restore(n)) == [47,79,103]
assert panel(372715,*restore(372715)) == [43,47,83,139]

n = 666510287684337524321867834203
y,d,ts = heads(n)
assert y == 14 and ts == [] and n % 19 == 17 and n % 127 == 72
assert [j for j in I if not R(n,Cs[2],d,j,127)] == [0,21]
assert pow(5,84,127**2) == 14860
print(rho)
~~~
