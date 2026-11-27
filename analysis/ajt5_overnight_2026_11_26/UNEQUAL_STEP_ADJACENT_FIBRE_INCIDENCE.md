# Adjacent vertical fibres with unequal actual order-49 steps

**Unequal \(3,5\) step phases can erase adjacent columns, but nine readers still cannot.** In the native \(3,7\) chart below, at most three actual order-\(49\) readers can collide in both columns of an adjacent pair outside the fixed \(3571\) stripes. Three is attained. The bound rules out nine-reader erasure even with order-\(343\) rows allowed. For panels using only order-\(49\) readers, **eleven is the exact minimum**, and the replay realizes it at one quarter-height target.

## Certified incidence bound

Use \(R(u,v)=n-3^{C+Au}-5^{Bv}\) with native line \(v\equiv1-u\bmod7\), \(A\equiv B\not\equiv0\bmod7\), and \(3^C\equiv1\bmod q\) at each shallow reader. The two actual steps \(g=3^A\) and \(h=5^B\) each have order \(49\) modulo the reader prime \(q\). Their ratio in the exponent can be any unit: write \(h=g^k\). The fixed \(3571\) row erases \(u\equiv0,1\bmod7\), so the adjacent pairs of interest start at \(u\bmod7\in\{2,3,4,5\}\).

A collision shared by \((u,v)\) and \((u+1,v')\) requires
\[
1+g^a-g-g^b=0,\qquad a=kv-u,\quad b=kv'-u.
\]
The native line gives \(a-b\equiv k\bmod7\), which is nonzero. Taking resultants with \(\Phi_{49}\) leaves 35 possible inert primes after the actual-base order and ratio tests. The only zero resultant is \((a,b)=(1,0)\). It forces \(k\equiv1\bmod7\) and \(u\equiv0\bmod7\), so it gives no additional prime for the pairs in scope. An independent exact multiplication-determinant implementation reproduced all 2,058 resultants, the resulting 35 admissible prime candidates, and the incidence histogram. [SymPy polynomial reference](https://docs.sympy.org/latest/modules/polys/reference.html)

The finite incidence check retains the **common** stride residue. If \(s\) is the prime-to-\(7\) part of \(q-1\), put \(G=(3^s)^{s^{-1}\bmod49}\) and \(H=(5^s)^{s^{-1}\bmod49}\) modulo \(q\). Then the actual steps are \(G^A,H^B\). On a complete vertical phase class modulo \(7\), the set of \(H^{Bv}\) depends only on \(B\bmod7\), so the check can replace \(B\) with \(A\) when counting shared primes. Over all 1,176 common stride and horizontal phase choices, the counts of shared primes are \(0,1,2,3\) in 672, 364, 126, and 14 cases, respectively.

Each fully erased fibre needs seven distinct readers. It also needs six shallow readers if the total budget is at most ten. A nonroot class modulo \(49\) missing a shallow row costs seven order-\(343\) rows, since all seven children have native-even lifts. If the total budget is \(H_0\) with \(d\) deep rows, two erased adjacent columns therefore require
\[
14-H_0\le3+d,\qquad 12-(H_0-d)\le3.
\]
These inequalities exclude \(H_0\le9\). At \(H_0=10\) they force nine shallow rows and one deep row. That case remains undecided here. With no deep rows they give \(H_0\ge11\).

The same counting applies inside an active box with vertical maximum at least \(6173\). Each required phase modulo \(343\) has a representative below \(3087\) with \(v\equiv0\bmod9\). In the native root phase, trying that representative and its translate by \(3087\) gives an exact valuation-four lift at \(7\). The nonroot required phases already have valuation two.

## Same-target arithmetic control

At \(A\equiv B\equiv36\bmod49\), the three shared readers are \(491,68699,135731\), with exponent ratios \(22,13,37\). They use vertical phases \(33,12,47\) at \(u=17\) and \(39,11,46\) at \(u=18\). Eight one-sided rows fill the other phases. The shared offsets agree modulo their primes and have distinct lifts modulo the squares. The CRT prescription avoids both lifts, giving exact valuation one at each endpoint.

The eleven-row panel erases both full fibres. Deleting rows \(472067,545959\) leaves a nine-row panel that still erases column \(17\) and admits \((18,81)\). At the same target the eleven-row panel kills that point at exact valuation one at \(545959\). Both panels admit \((19,45)\).

```python
from collections import Counter
from functools import cache
from math import isqrt, lcm, prod
from sympy import symbols, resultant, factorint

@cache
def prime(p):
    return p == 2 or (p > 2 and p%2
                      and all(p%d for d in range(3,isqrt(p)+1,2)))

@cache
def factors(n):
    f = factorint(n)
    assert prod(int(p)**k for p,k in f.items()) == n
    assert all(prime(p) for p in f)
    return f

X = symbols("X")
Phi = sum(X**(7*j) for j in range(7))
roots, zero = {}, []
for a in range(49):
    for b in range(49):
        c = (a-b)%7
        if not c:
            continue
        N = abs(int(resultant(Phi,1+X**a-X-X**b,X)))
        if not N:
            zero.append((a,b))
            continue
        for p in factors(N):
            p = int(p)
            if p%196 != 99:
                continue
            s = p-1
            while s%7 == 0:
                s //= 7
            x,y = pow(3,s,p),pow(5,s,p)
            if (all(pow(z,49,p) == 1 != pow(z,7,p) for z in (x,y))
                    and pow(x,7*c,p) == pow(y,7,p)):
                k = pow(s,-1,49)
                roots[p] = pow(x,k,p),pow(y,k,p)

counts = Counter()
for t in range(1,49):
    if t%7 == 0:
        continue
    for u in range(49):
        if u%7 not in (2,3,4,5):
            continue
        hits = 0
        for p,(G,H) in roots.items():
            g,h = pow(G,t,p),pow(H,t,p)
            left = {(pow(g,u,p)+pow(h,v,p))%p
                    for v in range((1-u)%7,49,7)}
            right = {(pow(g,u+1,p)+pow(h,v,p))%p
                     for v in range((-u)%7,49,7)}
            hits += bool(left & right)
        counts[hits] += 1
assert zero == [(1,0)] and len(roots) == 35
assert counts == {0:672,1:364,2:126,3:14}

Q = 3571
shared = ((491,33,39),(68699,12,11),(135731,47,46))
L = tuple(zip((6763,119659,190807,202567),(5,19,26,40)))
U = tuple(zip((430907,434827,472067,545959),(4,18,25,32)))
qs = [Q]+[q for q,_,_ in shared]+[q for q,_ in L+U]
D = lcm(18,*(q*((q-1)//(7 if q==Q else 49)) for q in qs))
j = 36*pow(D,-1,49)%49
B = D*(j if j%3 else j+49)
A = 4117*B
C = lcm(*(q*(q-1) for q in qs))

def S(u,v,m):
    return (pow(3,C+A*u,m)+pow(5,B*v,m))%m

assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(5,B,27) == 1 != pow(5,B,81)
for q in qs:
    m = 7 if q==Q else 49
    assert prime(q) and q%4 == 3 and pow(3,C,q*q) == 1
    for a,e in ((3,A),(5,B)):
        assert pow(a,e*m,q*q) == 1 != pow(a,e*(m//7),q)
for (q,_,_),k in zip(shared,(22,13,37)):
    assert pow(3,A*k,q) == pow(5,B,q)

eq = [(4,3),(243,82),(343,S(18,81,343)+49),(Q*Q,S(0,1,Q*Q)+Q)]
for q,v,w in shared:
    m = q*q
    x,y = S(17,v,m),S(18,w,m)
    assert (x-y)%q == 0 and x != y
    eq.append((m,next(x+j*q for j in (1,2) if (x+j*q-y)%m)))
eq += [(q*q,S(u,v,q*q)+q) for u,T in ((17,L),(18,U)) for q,v in T]
M = prod(m for m,_ in eq)
n0 = sum(r*(M//m)*pow(M//m,-1,m) for m,r in eq)%M

def R(u,v,m):
    return (n0-S(u,v,m))%m

def exact(u,v,q,k):
    z = R(u,v,q**(k+1))
    return z != 0 and z%q**k == 0

for u,T in ((17,L+tuple((q,v) for q,v,w in shared)),
            (18,U+tuple((q,w) for q,v,w in shared))):
    assert sorted(v for q,v in T) == list(range((1-u)%7,49,7))
    assert all(exact(u,v,q,1) for q,v in T)

keep = set(qs)-{472067,545959}
for u,v in ((17,180),(18,81),(19,45)):
    assert exact(u,v,3,4) and exact(u,v,7,2)
assert exact(17,180,491,1)
assert all(R(18,81,q) for q in keep) and exact(18,81,545959,1)
assert all(R(19,45,q) for q in qs)

E = C+19*A
delta = (n0-4*pow(3,E,M))%M
assert E > M.bit_length() and 19*4117 >= 2*6173
print(E, delta)  # The common target is 4*3**E + delta.
```

The target has quarter-height horizontal maximum \(19\) and vertical maximum at least \(6173\). All displayed remainders are positive. The escapes certify survival of the specified local tests, with full two-square status undetermined.
