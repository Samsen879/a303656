# One selectable 37-offset menu with nineteen centers on a large target class

**One 37-offset menu gives at least nineteen non-reusable centers on a periodic class of density \(79.492157\ldots\%\).** For each target the construction uses one common \(3\)-exponent and selects from the offsets \(0,\ldots,36\) on the \(5\)-axis. It works for any finite ordinary inert panel. For the same seeded phases with the unit condition at \(31\), a panel containing all the tie primes gives a ceiling on the eligible target fraction for these seeded phases of \(80.467767\ldots\%\).

### The periodic screen

Use \(h=8\) and centers \((C,D+8i)\). Choose \(D=2\) if \(n\not\equiv1\bmod3\), and \(D=1\) otherwise. For the test at \(2\), the allowed residual classes modulo \(8\) are \(0,1,2,4,5\). Switching the seed \(C\) between \(2\) and \(1\) shifts the \(3\)-power by \(2\bmod8\), so one choice works. Then vary \(C\) by multiples of the lcm of the odd-row periods to realize the required residue modulo \(32\). That lcm has \(2\)-valuation one, so these variations preserve all odd readings and traverse all four lifts of the chosen \(3\)-power modulo \(8\).

Let \(T\) be the 40 inert primes above \(23\) in the factor certificate below. They include every possible tie prime: if two offsets tie at \(q\), then \(\operatorname{ord}_q(5)\mid8(i-j)\), and \(v_2(q-1)=1\) forces \(q\mid5^{2m}-1\) for some odd \(m\le35\). All these factors above \(23\) occur to exponent one. A base-\(5\) Wieferich reader that hit twice would force a square factor in the same integer, so **no genuine common-Wieferich reader can hit twice in the selected menu**.

Delete all hits at \(7,11,19,23,31\), leaving a set \(A\). For each \(q\in T\setminus\{31\}\), let \(H_q\) be its hit set in \(A\) and put \(\ell_q=\max(0,|H_q|-1)\). The sufficient screen is
\[
 |A|-\sum_q\ell_q\ \ge19.
\]
For each row, keep one of its hits and mark the others for deletion. The union of the deletions has size at most the sum. Membership is periodic modulo \(24\prod_{q\in\{7,11,19,23\}\cup T}q\). Changing the parity seed permutes the target residues at each odd prime, since the shifts have the form \(3^C+5^D5^{8i}\). The replay therefore counts one distribution by exact CRT weights, without adding menus.

Protect the axes separately in the ordinary repairs. The \(3\)-lock uses the \(q-1\) for \(q\in T\), and the \(5\)-lock uses the \(2m\) above. Both include the coordinate \(31\), which is why the screen drops **all** its hits. At the other inert prime divisors above \(23\) of the \(3\)-lock, base \(5\) is fast and its lock leaves that coordinate free. Each retained ordinary row has at most one hit. The common first digit and a top digit then give exact valuation two while preserving the earlier readings.

For that seeded-template ceiling, replace the sum in the screen by \(\max_q\ell_q\). This is necessary for the same protected phases when all tie rows are enforced: every \(q\in T\setminus\{31\}\) exceeds \(36\), and its base-\(5\) order grows by \(q\) modulo \(q^2\). Two tied offsets therefore have distinct lifts, and at most one can pass the valuation test.

### Same-target replay

The CRT target below leaves 25 offsets after the mandatory deletions. At \(43\), indices \(2,23\) have first readings \(1,2\). Keeping both fails. Dropping \(23\) leaves **24** centers that pass the full ordinary prefix through \(499\), with exact remainders \(32\cdot43^2\bmod43^3\) and \(125\cdot499^2\bmod499^3\) at the two repaired centers. On the same target, taking the base-\(3\) repair at \(499\) with the \(38923\) lock released succeeds at \(499\), but creates an incompatible tie at \(38923\) on retained indices \(0,26\).

This is a finite-phase result. A sufficiently large target lift preserves the control readings and makes its remainders positive. No ordinary exponent-height bound for the original input \(n\) follows.

```python
from collections import Counter
from fractions import Fraction
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

def prime(q):
    if q not in W:
        return q>1 and all(q%d for d in range(2,isqrt(q)+1))
    u = prod(W[q])
    return (u*u>q and (q-1)%u==0 and pow(2,q-1,q)==1
            and all(prime(p) and gcd(pow(2,(q-1)//p,q)-1,q)==1 for p in W[q]))

T = set()
for m in F:
    f = Counter(q for d,fs in F.items() if m%d==0 for q in fs)
    assert all(map(prime,f)) and prod(q**j for q,j in f.items())==5**(2*m)-1
    assert all(j==1 for q,j in f.items() if q>23)
    T.update(q for q in f if q>23 and q%4==3)
assert len(T)==40 and min(T-{31})>36
A = (2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,911,
     1367,3701,4523,13967,37537,87877,391337,2061161,25654001,453003413,5855734783)
assert all(map(prime,A))
for q in T:
    r = q-1
    for p in A:
        while r%p==0: r//=p
    assert r==1
K5 = lcm(3960,*(2*m for m in F))
assert [p for p in range(27,71,4) if prime(p) and K5%p==0]==[31]
assert all(K5%p and pow(5,p-1,p*p)!=1 for p in A if p>23 and p%4==3 and p!=31)

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m
def good2(x):
    t = x & -x
    return bool(t and t<=8 and x//t%4==1)

small = (7,11,19,23)
L3 = lcm(*(q-1 for q in T|set(small)))
assert L3%4==2
for n in range(96):
    d = 2 if n%3!=1 else 1
    c = next(c for c in (2,1) if (n-S(c,d,8))%8 in (0,1,2,4,5))
    assert (n-S(c,d,3))%3
    assert any(good2((n-S(c+j*L3,d,32))%32) for j in range(4))

head, Q = small+(31,), sorted(T-{31})
def row(q):
    d = {}
    for i in range(37):
        x = S(2,2+8*i,q)
        d[x] = d.get(x,0)|(1<<i)
    f = Counter(d.values())
    f[0] += q-len(d)
    return f

P = {q:row(q) for q in head+tuple(Q)}
H = {0:1}
for q in head:
    D = Counter()
    for M,w in H.items():
        for R,v in P[q].items():
            if (M|R).bit_count()<=18:
                D[M|R] += w*v
    H = D
lo = hi = 0
for M,w in H.items():
    k = 18-M.bit_count()
    a,b = [1]+[0]*k,1
    for q in Q:
        f = Counter()
        for R,v in P[q].items():
            f[max(0,(R&~M).bit_count()-1)] += v
        b *= sum(v for j,v in f.items() if j<=k)
        a = [sum(v*a[i-j] for j,v in f.items() if j<=i) for i in range(k+1)]
    lo += w*sum(a)
    hi += w*b
den = prod(head)*prod(Q)
assert Fraction(79492,100000)<Fraction(lo,den)<Fraction(79493,100000)
assert Fraction(80467,100000)<Fraction(hi,den)<Fraction(80468,100000)

def earlier(p):
    return tuple(q for q in range(27,p,4) if prime(q))
def prev(p):
    return lcm(3960,*(q*q*(q-1) for q in earlier(p)))
def digit(b,e,B,p):
    return pow(pow(b,e,p)*((pow(b,B,p*p)-1)//p),-1,p)

s,p,q = 43,499,38923
B = lcm(K5,prev(s),s-1)
j = digit(5,18,B,s)
D = 2+B*j
B5 = lcm(K5,prev(p),p-1)
B3 = lcm(prev(p),p-1,*(z-1 for z in T if z!=q))
u,v = digit(5,D,B5,p),digit(3,2,B3,p)
D2,C = D+B5*u,2+B3*v
R = [(32,3),(7,4),(s**3,(S(2,18,s**3)+s)%s**3),
     (p**3,(S(2,D,p**3)+p)%p**3),(q,S(C,D,q))]
R += [(z,0) for z in (T|set(earlier(p))|set(small)|{3})-{7,s,q}]
M = prod(m for m,r in R)
n = sum(r*(M//m)*pow(M//m,-1,m) for m,r in R)%M
J = [i for i in range(37) if all((n-S(2,2+8*i,z))%z for z in head)]
g = {z:[i for i in J if (n-S(2,2+8*i,z))%z==0] for z in Q}
assert len(J)==25 and g[s]==[2,23]
assert all(len(g[z])<=1 for z in Q if z!=s)
assert [(n-S(2,2+8*i,s*s))%(s*s)//s for i in (2,23)]==[1,2]
I = [i for i in J if i!=23]
assert len(I)==24 and good2((n-S(2,D2,32))%32)
assert (n-S(2,D2+16,s**3))%s**3==32*s*s
assert (n-S(2,D2,p**3))%p**3==125*p*p
assert (n-S(C,D,p**3))%p**3==210*p*p
for i in I:
    assert all((n-S(2,D2+8*i,z))%z for z in head+(3,))
    for z in earlier(p)+(p,):
        r = (n-S(2,D2+8*i,z**3))%z**3
        assert r%z or (r and r%(z*z)==0)
assert [(n-S(C,D+8*i,q*q))%(q*q) for i in (0,26)]==[37936*q,10607*q]
```
