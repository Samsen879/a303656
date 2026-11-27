# Twenty-seven centers on an explicit periodic target class

**Twenty-seven centers are available on an explicit class of targets of density \(1.30715\ldots\%\).** They share one \(3\)-exponent and survive any finite ordinary inert panel. Each genuine common-Wieferich reader can hit at most one center, so a blocker on this class needs at least 27 such readers.

The result is conditional on the target class. There is also a uniform limitation on the compact construction: for \(n\equiv372715\bmod658812\), **any window of 28 consecutive offsets on the power-of-two-gap, common-\(C\) chart contains at most 18 legal centers**, even allowing \(C=0\). Thus 19 centers for every target requires a wider window or a different construction.

### The 27-center construction

Take offsets \(i=0,\ldots,26\), gap \(8\), and initial exponents \(C=D=2\). The target class requires all 27 small-head tests to pass. At each ordinary tie prime, it requires just the repeated values of \(3^2+5^{2+8i}\) to be avoided by \(n\). The exact density is the product of these allowed residue fractions, including \(15/32\) at \(2\). The replay certifies it is strictly between \(1.30\%\) and \(1.31\%\).

If two centers tie at an inert prime \(q>23\), then \(\operatorname{ord}_q(5)\mid8(i-j)\). Since \(v_2(q-1)=1\), this forces \(q\mid5^{2m}-1\) for some odd \(m\le25\). The factor certificate below gives exactly 21 possible tie primes, each occurring to exponent one in every relevant integer. A common-Wieferich reader that hits twice would require \(q^2\mid5^{2m}-1\), by lifting its exact order to \(q^2\). This excludes reuse across **the single 27-center menu**. [Project exact-order charging note](https://github.com/Samsen879/a303656/blob/9826d9cfa8038c80f460fafe27f24dc2ce99acd6/analysis/ajt5_overnight_2026_11_26/EXACT_ORDER_LOW_DENSITY_BOUND.md)

Protect the two axes separately. On the \(3\)-axis use the lcm of \(3960\) and the 21 values \(q-1\). On the \(5\)-axis use the lcm of \(3960\) and the \(2m\) above. The only inert primes above \(23\) dividing the first lock are \(31,67,71,499,911,4523,13967\). None divides the second, and base \(5\) is fast at all seven. At those rows use base \(5\). At other ordinary rows either fast axis is available. Because repeated classes are units, at most one center needs repair at each row. The usual common first digit and a top digit give exact valuation two, with the earlier readings preserved.

### Compact-window obstruction and actual repair control

For \(n\equiv372715\bmod658812\), the tests at \(2,3\) force \(C\) even and, if \(C>0\), \(D\) odd. With \(D\) odd, rows \(7\) and \(23\) each forbid an entire index class, modulo \(3\) and \(11\) respectively. In a 28-index window these classes remove at least \(9+2-1=10\) centers. If \(C=0\) and \(D\) is even, the chosen residues \(n\equiv2\bmod11,31\) instead give a forbidden class modulo \(5\) and a tied class modulo \(3\). In the latter class at most one center can pass \(31\): the \(5\)-order grows from \(3\) to \(93\) modulo \(31^2\), so the tied centers have distinct lifts in this window. This branch leaves at most \(28-(9-1)-(5-2)=17\).

The repair control uses one exact target, given by CRT in the replay. After the full ordinary prefix below \(499\), the protected base-\(5\) repair at \(499\) uses first digit \(180\) and gives remainder \(104\cdot499^2\bmod499^3\). The alternative base-\(3\) repair, with the \(38923\) lock released, also gives exact valuation two at \(499\). It turns indices \(0,13,26\) into a tie at \(38923\) with distinct first readings \(33369,243,6040\). No common first digit can repair that frozen tie.

These statements concern finite phases. The control can be lifted to positive remainders while preserving all specified readings. The construction gives no ordinary exponent-height bound for the original input \(n\).

```python
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt, lcm, prod

# For odd m, multiply the rows indexed by divisors of m.
F = {
 1:(2,2,2,3), 3:(3,7,31), 5:(11,71,521), 7:(29,449,19531),
 9:(3,19,829,5167), 11:(23,67,5281,12207031),
 13:(5227,38923,305175781), 15:(61,181,1741,7621),
 17:(409,3061,41540861,466344409),
 19:(191,761,6271,19609,3981071,213029),
 21:(7,43,127,379,7603,519499),
 23:(47,8971,42272797713043,332207361361),
 25:(101,251,401,1901,9384251,50150933101)
}
W = {42272797713043:(13967,4523), 332207361361:(9781,293),
     50150933101:(201167,277)}

def prime(q):
    if q not in W:
        return q>1 and all(q%d for d in range(2,isqrt(q)+1))
    U = prod(W[q])
    return (U*U>q and (q-1)%U==0 and pow(2,q-1,q)==1
            and all(prime(s) and gcd(pow(2,(q-1)//s,q)-1,q)==1
                    for s in W[q]))

assert all(prime(q) for fs in F.values() for q in fs)
T = set()
for m in F:
    v = Counter(q for d,fs in F.items() if m%d==0 for q in fs)
    assert prod(q**j for q,j in v.items()) == 5**(2*m)-1
    assert all(j==1 for q,j in v.items() if q>23)
    T.update(q for q in v if q>23 and q%4==3)
assert len(T)==21

A = (2,3,5,7,11,13,19,23,31,41,67,71,181,373,499,521,911,4523,13967,37537)
assert all(map(prime,A))
for q in T:
    r = q-1
    for s in A:
        while r%s==0:
            r //= s
    assert r==1
assert all(pow(5,s-1,s*s)!=1 for s in A if s>23 and s%4==3)

small = (3,7,11,19,23)
K5 = lcm(3960,*(2*m for m in F))
def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m
def good2(r):
    t = r & -r
    return bool(t and t<=8 and r//t%4==1)
def forbidden(q):
    v = Counter(S(2,2+8*i,q) for i in range(27))
    return {x for x,k in v.items() if k>1 or q in small}

rho = Fraction(15,32)*prod(Fraction(q-len(forbidden(q)),q) for q in set(small)|T)
assert Fraction(13,1000)<rho<Fraction(131,10000)

p,q = 499,38923
P = tuple(s for s in range(27,p,4) if prime(s))
assert all(any(pow(b,s-1,s*s)!=1 for b in (3,5)) for s in P)
K = lcm(3960,*(s*s*(s-1) for s in P))
B3 = lcm(K,p-1,*(s-1 for s in T if s!=q))
B5 = lcm(K,p-1,K5)
def digit(b,B):
    return pow(b*b*((pow(b,B,p*p)-1)//p),-1,p)
j,k = digit(3,B3),digit(5,B5)
C,D = 2+B3*j,2+B5*k
assert (j,k)==(19,180) and S(C,2,q)==4752

R = [(32,3),(p**3,533),(q,4752)]+[(s,0) for s in (set(small+P)|T)-{q}]
M = prod(m for m,x in R)
n = sum(x*(M//m)*pow(M//m,-1,m) for m,x in R)%M
assert good2((n-S(2,2,32))%32)
assert all(n%s not in forbidden(s) for s in set(small)|T)
assert (n-S(2,D,p**3))%p**3==104*p*p
assert all((n-S(2,D+8*i,p))%p for i in range(1,27))
assert all((n-S(2,D+8*i,s))%s for s in set(small+P)|T for i in range(27))
assert (n-S(C,2,p**3))%p**3==486*p*p
assert [(n-S(C,2+8*i,q*q))%(q*q) for i in (0,13,26)]==[33369*q,243*q,6040*q]

n0 = 372715
assert (n0%84,n0%23,n0%11,n0%31)==(7,0,2,2)
assert pow(5,3,31)==1 and pow(5,3,31**2)!=1
assert min(sum(i%3==a or i%11==b for i in range(28))
           for a in range(3) for b in range(11))==10
```
