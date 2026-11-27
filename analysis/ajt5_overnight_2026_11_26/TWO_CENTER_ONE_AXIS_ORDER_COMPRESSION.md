# Two centers force a one-axis order compression

There is a one-axis exclusion with **no bound on the order of \(3\)**. Two legal centers with the same \(3\)-exponent and a suitable gap on the \(5\)-axis cannot both be hit by the same common-Wieferich terminal. The exact arithmetic also identifies the only two ordinary inert primes that can hit both. One of them does so on a fixed-target control with a genuine inverse-class midpoint.

### The order test

Let \(31\nmid H\), \(3960\mid H\), and let \(q>5\), \(q\ne31\), satisfy \(\operatorname{ord}_q(5)\mid31H\). Compare the two centers
\[
(C,D),\qquad (C,D+\Delta)
\]
at the same integer \(n\). If \(q\) hits both, subtracting the two equations gives \(5^\Delta\equiv1\pmod q\). Hence
\[
\operatorname{ord}_q(5)\mid g=\gcd(\Delta,31H).
\]
If \(q\) is Wieferich to base \(5\), its order is unchanged modulo \(q^2\), so \(q^2\mid5^g-1\). The argument also applies at zero observations.

Take \(\Delta=3\cdot31^2j\) for any positive \(j\) coprime to \(31H\). Then \(g=93\), and the exact factorization is
\[
5^{93}-1
=4\cdot31^2\cdot1861\cdot148429\cdot878851
\cdot625552508473588471\cdot172974812463239310024750410929.
\]
The five factors after \(31^2\) are distinct primes. Thus **even a singly base-\(5\) Wieferich reader cannot hit both centers**. Among ordinary inert readers other than \(31\), only \(878851\) and \(625552508473588471\) can hit both. The parameter \(H\) can carry arbitrary additional prime-to-\(31\) factors. The observed equality at the two centers, rather than a cap on the full orders, forces the small exponent \(93\).

There is also a single-center version. If the actual target has \(n=3^C+5^{D+93j}\) with \(\gcd(j,31H)=1\), then a hit at \((C,D)\) gives the same order test and excludes every such base-\(5\) Wieferich reader there. The remainder is positive and has \(31\)-valuation exactly two, by \(5^3-1=4\cdot31\). This version requires the displayed target identity. The two-center test works for arbitrary \(n\) once both centers are available.

### Fixed-target control

Take \(p=242731\), \(q=878851\), \(H=7716924192027342600\), \(C=D=31H\), and \(\Delta=3\cdot31^2\). Set
\[
n_0=3^C+5^D+31^2q\cdot6331571.
\]
On each chart use \(c=C+Hx\), \(d=D+e+H(5x\bmod31)\), where \(e=0\) or \(\Delta\). The unique top repair adds \(31Hk\) to \(c\) to retain the source remainder modulo \(31^3\). The top digit at both centers is zero. Every cell passes the small rows \(3,7,11,19,23\) and has remainder \(1\bmod4\).

| Reader | Full orders of \(3,5\) | Relative character | Exact valuation-one hits, first chart | Second chart |
|---|---|---|---|---|
| \(242731\) | \(242730,\ 40455\) | Inverse | \(1,30\) | None |
| \(878851\) | \(878850,\ 93\) | Noninverse | \(0\) | \(0\) |

The inverse row leaves its midpoint \(0\) safe. The noninverse row vetoes both centers, and its base-\(5\) lift is ordinary. Both observations are nonzero. The coefficient \(6331571\) comes from the actual inverse trace at \(p\), with a lift that passes the displayed small rows.

For a positive-remainder realization of every cell, use \(n=n_0+M(3^{992H}+5^{D+\Delta+31H})\), where \(M=32\cdot3\cdot7\cdot11\cdot19\cdot23\cdot31^3(pq)^2\). This preserves all checked residues.

```python
from math import gcd, isqrt, lcm, prod

cert = {
    625552508473588471:
        {2:3, 3:2, 5:2, 31:2, 67:2, 25654001:2, 391337:2},
    172974812463239310024750410929:
        {2:7, 3:3, 13:2, 31:2, 103:3, 563:2, 7489:2,
         13393417:2, 118258507:2}
}
def prime(n):
    if n not in cert:
        return n > 1 and all(n%d for d in range(2,isqrt(n)+1))
    m = n-1
    for p,a in cert[n].items():
        assert prime(p) and m%p == 0 and pow(a,n-1,n) == 1
        assert gcd(pow(a,(n-1)//p,n)-1,n) == 1
        while m%p == 0:
            m //= p
    return m == 1

f = (1861,148429,878851,625552508473588471,172974812463239310024750410929)
assert len(set(f+(2,31))) == 7 and all(map(prime,f+(2,31)))
assert 5**93-1 == 4*31**2*prod(f)
assert [z for z in f if z%4 == 3] == [878851,625552508473588471]
assert all(pow(5,z-1,z*z) != 1 for z in f if z%4 == 3)

r,p,q = 31,242731,878851
H = lcm(3960,p*(p-1)//r,q*(q-1)//r)
C = D = r*H
gap = 3*r*r
assert H == 7716924192027342600 and gcd(gap,r*H) == 93

def order(b,z,k,fs):
    m = k
    for f in fs:
        assert prime(f) and m%f == 0 and pow(b,k//f,z) != 1
        while m%f == 0:
            m //= f
    assert m == 1 and pow(b,k,z) == 1

for z,u,v,fu,fv,j in [
    (p,242730,40455,(2,3,5,29,31),(3,5,29,31),30),
    (q,878850,93,(2,3,5,7,31),(3,31),17)
]:
    assert prime(z) and z%4 == 3
    order(3,z,u,fu)
    order(5,z,v,fv)
    assert all(pow(b,z-1,z*z)!=1 and pow(b,r*H,z*z)==1 for b in (3,5))
    X = pow(3,H,z)
    assert X != 1 and pow(X,j,z) == pow(5,5*H,z)

X = pow(3,H,p)
a0 = (X+pow(X,-1,p)-2)*pow(r*r*q,-1,p)%p
a = a0+26*p
delta = r*r*q*a
assert a0 == 20565 and a == 6331571
def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m
def N(m):
    return (S(C,D,m)+delta)%m

assert N(p) and N(q) and delta%r**3
for e,expected in [(0,{p:{1:168738,30:168738},q:{0:354258}}),
                   (gap,{p:{},q:{0:346773}})]:
    hits = {p:{},q:{}}
    for x in range(r):
        c,d = C+H*x,D+e+H*(5*x%r)
        k, = [k for k in range(r)
              if (N(r**3)-S(c+r*H*k,d,r**3))%r**3 == delta%r**3]
        if x == 0:
            assert k == 0
        c += r*H*k
        assert (N(4)-S(c,d,4))%4 == 1
        assert all((N(z)-S(c,d,z))%z for z in (3,7,11,19,23))
        for z in hits:
            R = (N(z*z)-S(c,d,z*z))%(z*z)
            if R%z == 0:
                assert R
                hits[z][x] = R//z
    assert hits == expected
```

The two charts use distinct \(d\bmod3960\) heads. The result gives a pointwise exclusion of **one reader covering both centers**. It leaves open whether an arbitrary retained prefix supplies such a pair, and distinct exceptional readers could still hit one center each.

Independent BigInt checked the exact factorization with complete Lucas certificates, both ordinary inert base-5 lifts, and every cell of both 31-digit charts. The exclusion is for the same reader hitting both centers, not for a collection of distinct readers or for arbitrary availability of those centers.
