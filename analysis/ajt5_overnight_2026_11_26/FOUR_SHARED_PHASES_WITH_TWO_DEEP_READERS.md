# Four shared horizontal phases with two deep readers

**One extra deep reader raises the sharp sharing limit from two to four full-fibre erasures modulo \(343\).** The actual eight-reader panel below erases columns \(4,53,102,151\), attaining the minimum spacing of \(49\). In the two-deep configuration it preserves column \(200\) and the immediate neighbor of each erased column at the same quarter-height target. Adjacent erasures by the higher readers remain impossible on columns where the fixed \(3571\) row is a unit.

An extra shallow reader has a different effect. If it supplies the seventh shallow phase at exact valuation one, it erases the entire horizontal class modulo \(49\). If there are still only six shallow phases, a single deep reader still gives at most two erased classes modulo \(343\).

## Incidence bound

Keep the previous \(3,7\) native chart, the equal steps, and \(3^C\equiv1\bmod q\) at the higher readers. Assume \(7\nmid B\), \(A/B\equiv1\bmod49\), and at most eight higher readers of orders \(49,343\), with at most two of order \(343\).

Every fully erased column needs at least six distinct shallow collisions. Each of the six nonroot vertical classes modulo \(49\) contains seven classes modulo \(343\) with native valuation two. Two deep readers can cover at most two of those seven classes. The \(3\)-test can be met independently by \(v\equiv0\bmod9\).

If two erased columns differed modulo \(49\), their two selections of six shallow readers would share at least four readers. The checked order-\(49\) swap lemma allows at most one shared reader among six distinct vertical classes. Indeed, a shared reader must exchange the horizontal and vertical phases, so its vertical phase at the first column is fixed by the second column. Thus all erasures lie in one horizontal class modulo \(49\).

Within that class, the shallow collision phases are constant. With six distinct phases, the missing vertical class must contain the native root \(r(u)\bmod343\) defined by \(7^4\mid R(u,r(u))\). The matching first lifting coefficients at \(7\) give
\[
r(u+49j)\equiv r(u)-49j\pmod{343}.
\]
To cover the even lifts in the missing class, a deep reader must hit \((u,r(u))\). At that reader write \(g\) for the common order-\(343\) step and \(T=u+r(u)\bmod343\). Its collision equation is
\[
(g^u)^2-(n\bmod q)g^u+g^T=0\pmod q.
\]
Thus it supplies at most two horizontal phases, exchanged by \(u\mapsto T-u\). Two deep readers supply at most four. If \(r(u)\not\equiv u\bmod49\), the swapped phase leaves the allowable horizontal class, and the bound drops to one phase per deep reader. This step uses the quadratic at order \(343\). The resultant check is confined to order \(49\).

## Same-target control

The six shallow readers cover \(v\equiv11,18,25,32,39,46\bmod49\) on \(u\equiv4\bmod49\). The native root moves with \(T=155\bmod343\). The deep readers \(9145067\) and \(11802631\) supply the pairs \(\{4,151\}\) and \(\{53,102\}\). All four deep collisions have exact valuation one. Off the deep root class in the one remaining shallow phase, the native valuation at \(7\) is three. This proves full-fibre erasure, including lifts away from the fine diagonal.

The replay checks failed points \((4,837),(53,2160),(102,396),(151,1719)\), all with native valuations \(4,4\). It also checks the four neighboring escapes at \(v=45\) and the escape \((200,3042)\), which lies in the same horizontal class modulo \(49\). For the shallow alternative, replacing the last deep row by \((202567,49,4,4)\) in the same CRT recipe fills the missing shallow phase. I checked that configuration also preserves \((5,45)\).

The replay includes the finite order-\(49\) input, independently repeated by exact multiplication determinants and complete factorization. It verifies the factorization products and primality of their factors. [SymPy polynomial reference](https://docs.sympy.org/latest/modules/polys/reference.html)

```python
from functools import cache
from math import isqrt, lcm, prod
from sympy import symbols, resultant, factorint

def prime(p):
    return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))

X = symbols("X")
Phi = sum(X**(7*j) for j in range(7))

@cache
def factors(n):
    f = factorint(n)
    assert prod(int(p)**k for p,k in f.items()) == n
    assert all(prime(p) for p in f)
    return f

for e,size in ((1,25),(7,3)):
    zeros, candidates = [], set()
    for a in range(49):
        for b in range((a-e)%7,49,7):
            N = abs(int(resultant(Phi,1+X**a-X**e-X**b,X)))
            if N:
                candidates.update(int(p) for p in factors(N) if p%196==99)
            else:
                zeros.append((a,b))
    assert zeros == [(e,0)] and len(candidates) == size
    for p in candidates:
        s = p-1
        while s%7 == 0:
            s //= 7
        g,h = pow(3,s,p),pow(5,s,p)
        assert g != h or pow(g,49,p) != 1 or pow(g,7,p) == 1

Q,p,q = 3571,9145067,11802631
shallow = list(zip((6763,119659,190807,430907,434827,472067),
                   (11,18,25,32,39,46)))
panel = ([(Q,7,0,1)] + [(t,49,4,b) for t,b in shallow]
         + [(p,343,4,151),(q,343,53,102)])
B = lcm(18,*(t*((t-1)//m) for t,m,a,b in panel))
C = lcm(*(t*(t-1) for t,m,a,b in panel))
A = 4117*B

def S(u,v,m):
    return (pow(3,C+A*u,m)+pow(5,B*v,m)) % m

for t,m,a,b in panel:
    g = pow(3,A,t*t)
    assert prime(t) and t%4 == 3 and pow(3,C,t*t) == 1
    assert g == pow(5,B,t*t) and pow(g,m,t*t) == 1 != pow(g,m//7,t)
assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(5,B,27) == 1 != pow(5,B,81) and pow(5,9*B,243) == 1
eq = [(4,3),(243,82),(7**5,S(4,837,7**5)+7**4)]
eq += [(t*t,S(a,b,t*t)+t) for t,m,a,b in panel]
M = prod(m for m,_ in eq)
r = sum(a*(M//m)*pow(M//m,-1,m) for m,a in eq) % M

def R(u,v,m):
    return (r-S(u,v,m)) % m

def val(u,v,t):
    return next(i for i in range(6) if R(u,v,t**(i+1)))

for u in range(4,343,49):
    v = (155-u)%343
    assert R(u,v,7**4) == 0
    hits = [t for t in (p,q) if R(u,v,t*t) == t]
    assert hits == {4:[p],53:[q],102:[q],151:[p]}.get(u,[])
for u,v,t in ((4,837,p),(53,2160,q),(102,396,q),(151,1719,p)):
    assert [val(u,v,i) for i in (3,7,t)] == [4,4,1]
    assert all(R(u,b,i*i) == i for i,b in shallow)
for u,v,k in ((5,45,2),(54,45,2),(103,45,2),(152,45,2),(200,3042,4)):
    assert [val(u,v,i) for i in (3,7)] == [4,k]
    assert all(R(u,v,t) for t,_,_,_ in panel)

E = C+200*A
delta = (r-4*pow(3,E,M)) % M
assert E > M.bit_length() and 200*4117 >= 2*3042
print(E, delta)  # The common target is 4*3**E + delta.
```

The last inequalities give \(M<3^E\), horizontal maximum \(200\), and vertical maximum at least \(3042\). Every displayed remainder is positive. The escapes certify survival of the specified local tests. Their full two-square status remains undetermined.
