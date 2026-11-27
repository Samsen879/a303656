# Exact minimum of ten higher readers in the unequal-step chart

The [previous incidence bound](https://github.com/Samsen879/a303656/commit/98017adc8f185f6dd7278b5fc71a14ac5acd68f0) excludes nine higher readers in the tracked unequal-step adjacent \(Q\)-unit columns, where shallow readers have neutral anchor and order 49 and a deep reader may have order 343. The construction below attains ten: nine shallow readers and the deep reader \(q=262739\). The latter has a nonneutral anchor \(3^C\equiv235492\bmod q\). The case requiring that anchor to be neutral is not settled by this construction.

At the same target, columns \(17,18\) share shallow readers \(491,68699,135731\). Each has three further shallow readers. Write \(R(u,v)=n-3^{C+Au}-5^{Bv}\). On each native line modulo 7, the six shallow readers obstruct six distinct vertical classes modulo 49 at exact valuation one. Away from the native line, the valuation at 7 is one. In the uncovered class, the points away from the root modulo 343 have valuation three at 7. The remaining native roots are \(v=68,53\bmod343\) in columns 17 and 18. Their offset sums agree modulo \(7^4\) and modulo the deep prime, and the target makes both deep readings have exact valuation one. The lift orders in the replay make these conclusions periodic, so the entire two vertical fibres fail this panel.

On the same target, removing the deep reader leaves \((17,1440)\) and \((18,3483)\) with native valuations \(4,4\) at \(3,7\) and units at all other tested odd primes. The point \((19,45)\) passes the full panel with native valuations \(4,2\). All three have \(R\equiv1\bmod4\). These are local tests, not complete two-square certificates. The target is \(n=4\cdot3^{C+19A}+\delta\), with \(0\le\delta<M\) as reconstructed below. Its quarter-height box has horizontal maximum 19 and vertical maximum at least 6173, by \(5<3^2\) and \(2B\cdot6173\le19A\). Positivity holds throughout that box.

### Exact standalone replay

~~~python
from math import isqrt, lcm, prod

Q, d = 3571, 262739
shared = ((491,33,39), (68699,12,11), (135731,47,46))
left = ((6763,5), (119659,26), (190807,40))
right = ((430907,18), (434827,25), (472067,32))
base = (Q, *(q for q,v,w in shared), *(q for q,v in left+right))
primes = (*base, d)

def order(q):
    return 7 if q==Q else 343 if q==d else 49

D = lcm(18, *(q*((q-1)//order(q)) for q in primes))
j = 232*pow(D,-1,343)%343
B = D*(j if j%3 else j+343)
A = 4117*B
L = lcm(6*343, *(q*(q-1) for q in base))
C = 94*d*L

def S(u,v,m):
    return (pow(3,C+A*u,m) + pow(5,B*v,m)) % m

for q in primes:
    m = order(q)
    assert q%4 == 3 and all(q%i for i in range(2,isqrt(q)+1))
    for b,e in ((3,A),(5,B)):
        assert pow(b,e*m,q*q) == 1 != pow(b,e*(m//7),q)
    if q != d:
        assert pow(3,C,q*q) == 1

assert A%343 == B%343 == 232 and pow(3,C,2401) == 1
assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(5,B,27) == 1 != pow(5,B,81)
assert pow(5,9*B,243) == 1
assert pow(3,C,d) == 235492
assert S(17,68,2401) == S(18,53,2401) == 1479
assert S(17,68,d) == S(18,53,d) == 230525

eq = [(4,3),(243,82),(7**5,S(17,1440,7**5)+7**4),
      (Q*Q,S(0,1,Q*Q)+Q)]
for q,v,w in (*shared,(d,68,53)):
    m = q*q
    x,y = S(17,v,m),S(18,w,m)
    assert (x-y)%q == 0
    eq.append((m,next(x+j*q for j in (1,2) if (x+j*q-y)%m)))
eq += [(q*q,S(u,v,q*q)+q)
       for u,T in ((17,left),(18,right)) for q,v in T]
M = prod(m for m,_ in eq)
n0 = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M

def R(u,v,m):
    return (n0-S(u,v,m)) % m

def exact(u,v,q,k):
    z = R(u,v,q**(k+1))
    return z != 0 and z%q**k == 0

for u,r,T in ((17,68,left+tuple((q,v) for q,v,w in shared)),
              (18,53,right+tuple((q,w) for q,v,w in shared))):
    assert sorted(v for q,v in T) == [
        v for v in range((1-u)%7,49,7) if v != r%49
    ]
    assert R(u,r,2401) == 0 and exact(u,r,d,1)
    assert all(exact(u,v,q,1) for q,v in T)
    for v in range(343):
        if R(u,v,49):
            assert exact(u,v,7,1)
        elif v%49 != r%49:
            assert any(v%49 == t and exact(u,v,q,1) for q,t in T)
        elif v != r:
            assert exact(u,v,7,3)
        else:
            assert exact(u,v,d,1)
assert pow(5,343*B,2401) == pow(5,343*B,d*d) == 1

for u,v in ((17,1440),(18,3483)):
    assert exact(u,v,3,4) and exact(u,v,7,4) and exact(u,v,d,1)
    assert all(R(u,v,q) for q in base)
assert exact(19,45,3,4) and exact(19,45,7,2)
assert all(R(19,45,q) for q in primes)

E = C+19*A
delta = (n0-4*pow(3,E,M)) % M
assert E > M.bit_length() and 19*4117 >= 2*6173
print(E, delta)  # Common target n = 4*3**E + delta.
~~~
