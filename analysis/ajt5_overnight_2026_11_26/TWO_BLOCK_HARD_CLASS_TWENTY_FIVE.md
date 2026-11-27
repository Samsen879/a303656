# Two blocks supply 25 centers on part of the hard class

The [contiguous-template cap](https://github.com/Samsen879/a303656/commit/2f6837d5552626a9973825edd41179943cc432a6) does not extend to all templates with one horizontal exponent. On the hard class \(n\equiv372715\bmod658812\), two vertical blocks give 25 centers on an explicit periodic subset of relative density \(0.2525632297\ldots\). This is a density within the hard residue class of an admissible menu, not a density of actual positive norm representations.

Use a positive even \(C\), odd \(D\), and vertical exponents \(D+4j\) for
\[
J_s=\{0,2,\ldots,32\}\cup\{s,s+2,\ldots,s+38\},\qquad s=-3,-1.
\]
At \(n=372715,C=66,D=135004545737\), the phases \(-3,-1\) give 26 and 25 candidates respectively before the check at 23, after requiring units at \(3,7,11,19,31\). Both hit at \(j=15,26\) at 23; those remainders are \(22\cdot23^2\) and \(189\cdot23\bmod23^3\). Thus with \(s=-3\), the retained menu \(I=\{j\in J_{-3}:j\not\equiv1\bmod3,\ j\ne26\}\) has 25. The ordinary repairs through 211 are checked below. For arbitrary allowed seeds in the hard class, the strict count is at most 24 for \(s=-3\) and 23 for \(s=-1\), by dropping the hit classes modulo 3 and 11. The count with even-valuation repair at 23 adds at most one, by the order 506 of 5 modulo \(23^2\).

For every cross-block difference, its odd part is at most 35; within one block it is at most 19. If an inert \(q>23\) ties two centers, its base-5 order divides \(2m\) for some odd \(m\le35\). The 40-prime tie list \(T\) in the replay is exhaustive, and all its primes occur to exponent one in each relevant \(5^{2m}-1\). Therefore a base-5 Wieferich prime cannot tie two centers, even across the blocks. In particular each genuine common-Wieferich prime can kill at most one center.

To repair any finite ordinary panel, lock \(C,D\) modulo \(U=\operatorname{lcm}(3960,q-1:q\in T)\) and \(V=\operatorname{lcm}(3960,2m:m\le35\ \text{odd})\). Outside \(T\) there cannot be two hits, and at \(T\) the seed is checked to have no repeated hit. At each inert ordinary \(p>23\), repair in increasing order with a step that includes \(p-1\), \(23^2\), and all earlier \(r^2(r-1)\). Lower primes cannot put \(p\) into this step. The only inert divisor of \(V\) above 23 is the unit row 31; every inert divisor of \(U\) above 31 is base-5 ordinary. So for each nonunit ordinary row some ordinary axis can be changed with a step prime to \(p\). The first digit makes the remainder zero modulo \(p^2\); the second avoids zero modulo \(p^3\). The previously imposed readings and tie locks remain intact. Blocking all 25 centers then requires at least 25 distinct common-Wieferich rows.

For the periodic subset, use the same \(C,I\) and shift \(D\) by \(yV/23\), choosing the unique digit \(0\le y<23\) which makes the \(j=15\) remainder zero modulo \(23^2\). Adding \(V\) once if needed gives exact valuation two. The six forbidden residues at 19 and the \(b_q\) repeated offset values at each \(q\in T\setminus\{31\}\) are transported by invertible affine changes, leaving their counts fixed. The 31 reading is already locked. CRT after fixing the digit gives relative density \((13/19)\prod_{q\in T\setminus\{31\}}(1-b_q/q)\). The next target \(1031527\) fails this fixed menu at 19; other menus remain possible. All conclusions are finite-phase, with no height guarantee at either displayed target.

~~~python
from collections import Counter
from fractions import Fraction
from functools import cache
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

@cache
def prime(n):
    if n not in W:
        return n > 1 and all(n % d for d in range(2, isqrt(n)+1))
    u = prod(W[n])
    return (u*u > n and (n-1) % u == 0 and pow(2,n-1,n) == 1
            and all(prime(d) and gcd(pow(2,(n-1)//d,n)-1,n) == 1
                    for d in W[n]))

T = set()
for m in range(1,36,2):
    f = Counter(p for d, fs in F.items() if m % d == 0 for p in fs)
    assert all(map(prime,f)) and prod(p**v for p,v in f.items()) == 5**(2*m)-1
    assert all(v == 1 for p,v in f.items() if p > 23)
    T.update(p for p in f if p > 23 and p % 4 == 3)
assert len(T) == 40 and 31 in T

A = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,
     911,1367,3701,4523,13967,37537,87877,391337,2061161,25654001,
     453003413,5855734783)
assert all(map(prime,A))
U = lcm(3960, *(p-1 for p in T))
V = lcm(3960, *(2*m for m in F))
for p in T:
    k = p-1
    for a in A:
        while k % a == 0:
            k //= a
    assert k == 1 and pow(5,V,p) == 1
assert [p for p in range(27,36,4) if prime(p) and V % p == 0] == [31]
assert all(pow(5,p-1,p*p) != 1 for p in A if p > 31 and p % 4 == 3)
assert pow(5,3,7) == 6 and pow(5,2,7) != 1
assert pow(5,11,23) == 22 and pow(5,2,23) != 1 and pow(5,22,529) != 1

n, C, D = 372715, 66, 135004545737
def J(s):
    return list(range(0,33,2)) + list(range(s,s+40,2))

for js, upper in ((range(37),23),(J(-3),24),(J(-1),23)):
    assert max(sum(j % 3 != a and j % 11 != b for j in js)
               for a in range(3) for b in range(11)) == upper

def R(j, m, d=D, target=n):
    return (target-pow(3,C,m)-pow(5,d+4*j,m)) % m

for s, count in ((-3,26),(-1,25)):
    H = [j for j in J(s) if all(R(j,p) for p in (3,7,11,19,31))]
    assert len(H) == count and [j for j in H if not R(j,23)] == [26,15]

I = [j for j in J(-3) if j % 3 != 1 and j != 26]
assert len(I) == 25 and all(R(j,4) == 1 for j in I)
assert all(R(j,p) for j in I for p in (3,7,11,19,31))
assert [R(j,23**3) for j in (15,26)] == [22*23**2,189*23]

def classes(p):
    return Counter(R(j,p) for j in I)

assert [(p,classes(p)[0]) for p in sorted(T) if classes(p)[0]] == [(43,1),(47,1)]
L = V//23
assert V == 23*L and all(L % (p-1) == 0 for p in (7,11,19,23,31))
assert pow(5,L,529) == 24 and pow(5,V,23**3) == 1+23**2
assert len(classes(19)) == 6
rho = Fraction(13,19)*prod(
    1-Fraction(sum(v > 1 for v in classes(p).values()),p) for p in T-{31}
)
assert Fraction(25256,100000) < rho < Fraction(25257,100000)

n1 = n+658812
assert [y for y in range(23) if R(15,529,D+y*L,n1) == 0] == [14]
assert [R(j,19**2,D+14*L,n1) for j in (12,30,3,21)] == [152,95,0,304]
assert pow(5,9,19**2) == 115 and pow(5,3,19) != 1

P = [p for p in range(27,212,4) if prime(p)]
M, d, trace = 23**2, D, []
for p in P:
    roots = [j for j in I if R(j,p,d) == 0]
    assert len(roots) <= 1
    if roots:
        j, = roots
        B = lcm(M,V,p-1)
        assert B % p and pow(5,B,p*p) != 1
        t = next(t for t in range(2*p)
                 if 0 < R(j,p**3,d+t*B) and R(j,p*p,d+t*B) == 0)
        d += t*B
        trace.append((p,j,t,R(j,p**3,d)//(p*p)))
    M = lcm(M,p*p*(p-1))

assert trace == [(43,15,4,34),(47,21,12,11),(83,32,20,31),(139,9,1,127)]
assert all(R(j,p,d) or (0 < R(j,p**3,d) and R(j,p*p,d) == 0)
           for j in I for p in P+[23])
print(len(I), trace)
~~~
