# A uniform nineteen-center certificate on one 37-offset menu

**The 37-offset menu now gives nineteen non-reusable centers for every target \(n\).** Choose one seed \((C,D)\) and retain nineteen of the centers \((C,D+8i)\), \(0\le i\le36\). They pass the small-head tests and any finite panel of ordinary inert rows. Each genuine common-Wieferich reader can hit at most one retained center, so a finite blocker requires at least nineteen such readers.

The seed is selected before the ordinary repairs. The construction keeps the previous separate-axis locks and the squarefree certificate for all 40 possible tie primes. It uses a single menu throughout.

### How the seed is chosen

Choose parities for the tests at \(2,3\). With \(D\) of admissible parity at \(3\), toggling the parity of \(C\) shifts the sum by \(2\bmod8\). The allowed residual classes \(0,1,2,4,5\bmod8\) and their translate by \(2\) cover all eight classes. The final \(C\)-period has \(2\)-valuation one, so the required lift modulo \(32\) can be chosen after the odd rows are settled.

**First retain 22 candidates.** The exact small table in the replay shows that \(7,19,11,31\) can all be made units outside one index class modulo \(3\). There is one exceptional table entry, with both parities odd and readings \((2,0,8,27)\) at those four primes. There \(C=D=89\) leaves 27 candidates. Otherwise, shifting \(D\) by a multiple of \(8\) places the omitted class on a class of size 12, leaving 25.

Handle \(23,67\) together using the two free exponent residues modulo \(11\). If either observation is nonzero, some \(C\)-phase makes that row a unit on the whole menu: a nonzero translate cannot identify two cosets of the order-eleven subgroup, since both cosets sum to zero. If both rows force hits, their slopes are distinct, since \(3=5^{16}\bmod23\) and \(3=5^7\bmod67\). Thus their forbidden index classes can be aligned in the least occupied class modulo \(11\). This costs at most two candidates. Row \(199\), whose index period is \(33\), costs at most one. Keep 22.

**Spend at most three further deletions.**

- The free \(7\)-coordinates on the two axes give a choice making \(71\) a unit everywhere. At least four of the seven \(C\)-choices do so. Over those choices and the seven \(D\)-choices, the expected total deletion cost at \(43,127,211,631\) is at most \(65/28<3\). For nonzero observations this uses the exact coset-intersection caps \(3,2,2,2\). For zero observations, only one index class modulo \(3\) can contribute at \(43,127\), and only one modulo \(5\) at \(211,631\). Thus some choice costs at most two.
- A new ternary digit of \(D\) clears the ties at \(271\). The three possible hit classes are spaced by \(9\) modulo \(27\), and the repeated representatives lie in \(0,\ldots,9\). Successive ternary digits of \(C\) clear \(4159,163,487\). The replay checks that no three of the ten repeated \(5^{8i}\) values form a translate of a coset of the order-three subgroup. Row \(379\), which reads the first of those digits, can cost one deletion.
- The free \(19\)-coordinates clear \(191,6271\) jointly. Each row has at most eleven repeated classes on 22 indices. For nonzero observations the coset caps are \(6,2\). A zero observation excludes at most eleven parallel lines in the \(19\times19\) phase grid, leaving at least \(19\cdot8>6\cdot11\) choices for a nonzero companion row. With two zero observations the slopes \(16,3\bmod19\) differ, so both forbidden families can be avoided.

Every remaining tie is steered to a unit by the fresh \(C\)-directions in the replay. Each group offers more distinct choices than its total repeated classes. The ordinary repairs then use the separate-axis locks. All \(31\)-hits have already been removed. At other inert divisors of the \(3\)-lock, base \(5\) is fast and its lock leaves the repair coordinate free.

### Explicit phase increments and deletion accounting

Start the 23/67 step by independently varying \(C,D\) by multiples of 90, which preserves 7, 19, 11 and 31. The 11-compatible subgroup does not depend on \(D\). In the nonzero case where one row is cleared by choosing \(C\), varying \(D\) then places the other row's hit class, if present, at a least occupied residue modulo 11. In the two zero-hit families the distinct slopes give an invertible map from the two free phases to the two hit residues. Their common position costs at most two among at most 27 candidates. The index period 33 at 199 permits at most two hits within 37 offsets, so one deletion suffices there.

Use multiples of 990 to vary both axes at the seven-phase step; this locks the earlier rows, including the actual orders at 199. Conditional on the chosen \(C\) clearing 71, there are at least \(4\cdot7\) equally weighted pairs of choices: at a nonzero target the coset cap at 71 is three and at zero the intersection of the order-seven and order-five cosets has size at most one. For nonzero readings the per-row expected deletion bounds with denominator 28 are \(33,22,4,4\), respectively: at 43 and 127 there are at most eleven repeated residues each; at 211 and 631 there are only two possible repeated residues each. At zero, the repeated representatives at 43 and 127 are drawn from \(0,\ldots,15\), of which at most six lie in one class modulo 3, each with conditional probability \(1/7\). The corresponding bound is \(24/28\). At 211 and 631 the only possible repeated representatives are 0 and 1, at most one in a given class modulo 5, giving \(4/28\). Taking the larger of the zero/nonzero bounds gives total \(65/28\).

Write \(G=\operatorname{lcm}(990,7)=6930\). At 271 vary \(D\) by \(G\), in its three new phases; this leaves all earlier readings unchanged. Its exponent step in the order-27 index cycle moves a hit by \(9\). At 4159, 163 and 487 vary only \(C\), using increments \(G,3G,9G\) respectively, with three choices per digit. The first change preserves the \(3\)-order 30 at 271; the next two preserve all prior choices, including the 379 order 378 once the first digit has been set. In a coset of order three, the sum and sum of squares vanish; a translate therefore obeys \(3\sum x_i^2=(\sum x_i)^2\). The exact nonvanishing test in the replay excludes a triple of tie values at any of these three rows. The index period 21 at 379 permits only one additional deletion.

Use the joint increment \(\operatorname{lcm}(990,7,243)\) independently on each axis at 191 and 6271; it preserves all earlier rows and induces order nineteen on both axes. The zero-row slopes checked at increment 990 are unchanged by this common rescaling. At the remaining rows the listed groups use a common \(C\)-increment \(tK\), then enlarge \(K\) to protect the new orders. Try the first one plus the total repeat count many integer choices. On each row these choices give distinct residues, so each repeated value excludes at most one choice. The final \(K\) has 2-valuation one, allowing the lift modulo 32 without disturbing any odd unit or tie reading.

### Same-target control

The CRT target in the replay makes the old seed \(C=D=2\) leave **only twelve** offsets at \(7,31\). On that same target, \(C=6,D=2\) clears all 37 offsets at those rows and passes the remaining head and tie tests. The base-\(5\) repair at \(499\) uses first digit \(180\) and gives remainder \(104\cdot499^2\bmod499^3\), with the full earlier ordinary prefix protected.

This is a finite-phase theorem. A target lift can make the control remainders positive while preserving the recorded readings. The construction gives no bound putting the selected exponents inside the ordinary window for the original input \(n\).

```python
from collections import Counter
from itertools import combinations, product
from math import gcd, isqrt, lcm, prod

# Multiply the rows indexed by divisors of m to obtain 5^(2m)-1.
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
 35:(211,631,4201,15216601,85280581,4698932281)
}
W = {42272797713043:(13967,4523),332207361361:(9781,293),
     50150933101:(201167,277),22125996444329:(13624382047,),
     6090817323763:(2061161,37),28086211607:(453003413,),
     625552508473588471:(391337,25654001),386478495679:(5855734783,)}

def prime(n):
    if n not in W:
        return n>1 and all(n%d for d in range(2,isqrt(n)+1))
    u = prod(W[n])
    return (u*u>n and (n-1)%u==0 and pow(2,n-1,n)==1
            and all(prime(p) and gcd(pow(2,(n-1)//p,n)-1,n)==1 for p in W[n]))

T = set()
for m in F:
    f = Counter(q for d,fs in F.items() if m%d==0 for q in fs)
    assert all(map(prime,f)) and prod(q**v for q,v in f.items())==5**(2*m)-1
    assert all(v==1 for q,v in f.items() if q>23)
    T.update(q for q in f if q>23 and q%4==3)

A = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,911,
     1367,3701,4523,13967,37537,87877,391337,2061161,25654001,453003413,5855734783)
def order(b,q):
    r = u = q-1
    for p in A:
        while r%p==0: r//=p
        while u%p==0 and pow(b,u//p,q)==1: u//=p
    assert r==1
    return u

assert len(T)==40 and all(map(prime,A))
O = {q:(order(3,q),order(5,q)) for q in T}
K5 = lcm(3960,*(2*m for m in F))
assert K5%31==0
assert all(K5%p and pow(5,p-1,p*p)!=1 for p in A if p>23 and p%4==3 and p!=31)

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

full = (1<<341)-1
bad = []
for a,b in product(range(2),repeat=2):
    rows = []
    for c,d,k in product(range(a,90,2),range(b,18,2),range(3)):
        X,Y,Z = [{S(c,d+8*i,q) for i in range(9) if i%3!=k} for q in (7,19,31)]
        M = sum(1<<(31*u+v) for u,v in product(range(11),range(31))
                if v not in Z and (u-pow(3,c,11))%11 not in (1,3,4,5,9))
        rows.append((X,Y,M))
    for u,v in product(range(7),range(19)):
        M = 0
        for X,Y,Z in rows:
            if u not in X and v not in Y: M |= Z
        if M!=full:
            bad += [(a,b,u,v,j//31,j%31) for j in range(341) if not (M>>j)&1]
assert bad==[(1,1,2,0,8,27)]
assert sum(all(S(89,89+8*i,q)!=n for q,n in ((7,2),(19,0),(11,8),(31,27)))
           for i in range(37))==27
assert pow(5,16,23)==3 and pow(5,7,67)==3

def cap(q,a,b):
    X = {pow(i,(q-1)//a,q) for i in range(1,q)}
    Y = {pow(i,(q-1)//b,q) for i in range(1,q)}
    seen, best = set(), 0
    for r in range(1,q):
        if r in seen: continue
        Z = {r*y%q for y in Y}
        seen |= Z
        v = Counter((x+z)%q for x in X for z in Z)
        best = max(best,max((k for n,k in v.items() if n),default=0))
    return best

assert [cap(q,7,7) for q in (43,127,211,631)]==[3,2,2,2]
assert cap(71,7,5)==3 and [cap(q,19,19) for q in (191,6271)]==[6,2]
for q,k in ((191,16),(6271,3)):
    assert pow(3,990,q)==pow(5,990*k,q) and pow(5,990,q)!=1
for q in (4159,163,487):
    for X in combinations([pow(5,8*i,q) for i in range(10)],3):
        assert (3*sum(x*x for x in X)-sum(X)**2)%q

G = [(7,(19531,1303,519499)),(1,(251,)),(1,(47,31051)),
     (1,(8971,)),(1,(59,)),(1,(5167,35671))]
G += [(1,(q,)) for q in (12207031,5227,38923,3981071,7603,42272797713043,
       9384251,16018507,5096867,6090817323763,28086211607,625552508473588471,
       595123,190771747,386478495679)]
K = lcm(990,7,243,19)
used = {31,67,199,43,127,71,211,631,163,271,487,4159,379,191,6271}
for t,Q in G:
    assert not used.intersection(Q)
    used.update(Q)
    m = [O[q][1]//gcd(8,O[q][1]) for q in Q]
    r = sum(min(11,h,37-h) for h in m)
    assert all(O[q][0]//gcd(O[q][0],t*K)>r for q in Q)
    K = lcm(K,*(O[q][0] for q in Q))
assert used==T and K%4==2

p = 499
P = tuple(q for q in range(27,p,4) if prime(q))
assert all(any(pow(b,q-1,q*q)!=1 for b in (3,5)) for q in P)
X = [(32,3),(7,6),(31,14),(p**3,1253)]
X += [(q,0) for q in (T|set(P)|{3,7,11,19,23})-{7,31}]
M = prod(q for q,r in X)
n = sum(r*(M//q)*pow(M//q,-1,q) for q,r in X)%M
assert sum(all((n-S(2,2+8*i,q))%q for q in (7,31)) for i in range(37))==12
B = lcm(3960,p-1,K5,*(q*q*(q-1) for q in P))
j = pow(25*((pow(5,B,p*p)-1)//p),-1,p)
D = 2+B*j
assert j==180 and (n-S(6,D,32))%32==17
assert (n-S(6,D,p**3))%p**3==104*p*p
for i in range(37):
    assert all((n-S(6,D+8*i,q))%q for q in T|set(P)|{3,7,11,19,23})
    assert i==0 or (n-S(6,D+8*i,p))%p
```
