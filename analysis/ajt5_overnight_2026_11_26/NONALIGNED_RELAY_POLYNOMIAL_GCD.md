# Polynomial gcd certificate for nonaligned relay digits

**The original nonaligned \(7,79\to3319\) control has no hits by a degree-29 polynomial gcd certificate.** The certificate allows the two relay digits and the spare phase to vary independently, so it covers the actual shared-label orbit in one calculation. A second target shows exactly where that relaxation loses information. [Pinned double-relay control](https://github.com/Samsen879/a303656/blob/f0c2bac68b965850151c8a12a314f980930c72e4/analysis/ajt5_overnight_2026_11_26/DOUBLE_RELAY_CANCELLATION_CRITERION.md)

### Project through the exact relay orders

At \(r=3319\), the first-axis relay generators are \(441,1445\), of orders \(7,79\). On the nonaligned rays \((3,71)\), the second-axis generators are their respective fifth and 36th powers. Thus with \(L=7\cdot79=553\), the CRT exponent \(k=194\) combines both reads.

The two terms at the reader are \(AX\) and \(BX^kY\), where \(X\in\mu_L\) is the product of the first-axis relay factors and \(Y\in\mu_3\) is the spare phase. Here \(A=-1,\ B=1,\ N=n\bmod3319=1136\). The relaxed hit equation is equivalent to
\[
X^{553}=1,\qquad F_N(X)=(N+X)^3-X^{29}=0,
\]
since \(3k\equiv29\pmod{553}\). Conversely, each common root gives exactly one relaxed phase \(Y=(N+X)/X^k\). The polynomial \(X^{553}-1\) splits into distinct linear factors in the reader field, so the gcd degree counts the relaxed hits exactly.

For the pinned target,
\[
\gcd(X^{553}-1,F_{1136})=1
\quad\text{over }\mathbb F_{3319}.
\]
The standard-library replay below checks the two exact gcds by polynomial Euclid after binary powering modulo the degree-29 polynomial. It does not evaluate the hit equation label by label. More generally, for a spare factor of order \(M\), this test uses \((N-AX)^M-B^MX^{kM\bmod L}\). If its degree is \(D\), reducing \(X^L\) modulo it by repeated squaring keeps the polynomial arithmetic at degree \(O(D)\).

### Same graph, where coupling matters

At \(n'=16625594332193\), the relay conditions are preserved and \(N'=2609\). The relaxed gcd is \((X-1381)(X-2422)\). Both roots have exact order 553. Their projected relay digits explain why neither is a true hit.

| Root | Digits at \(7,79\) | Shared-label test |
|---:|---:|---|
| \(1381\) | \((4,15)\) | The first digit requires \(j=0\) and the second requires \(j=1\) |
| \(2422\) | \((5,38)\) | The first digit is outside its order-3 orbit |

The same projection also gives a sparse simultaneous-translate test. In this graph \(X(j+1)=X(j)^{23}\) and \(Y(j+1)=1791Y(j)\). Eliminating \(Y\) between two consecutive hits adds the polynomial
\[
N+X^{23}-1791X^{397}(N+X).
\]
At the two relaxed roots for \(N'=2609\) its values are \(3148,972\). Thus even before checking the individual digit orbits, the coupled translate test excludes consecutive hits.

### Runnable replay

```python
from math import isqrt, lcm, prod


h, r, n = 3, 3319, 16548479088281
P, C, D = (7, 79), 214742619, 79168445538
L = prod(P)
H = lcm(*(p*p*(p-1) for p in P), r*(r-1))

def step(m):
    b = H//m
    return b*pow(b, -1, m)

J = step(h)
A, B, alpha, beta = pow(3,C,r), pow(5,D,r), pow(3,J,r), pow(5,2*J,r)
assert (A,B,alpha,beta,n%r) == (3318,1,1,1791,1136)
assert pow(beta,h,r) == 1 and beta != 1
assert all(all(z%d for d in range(2,isqrt(z)+1)) for z in (r,*P))

g, f0, w = [], [], []
for p, ray, k0 in zip(P, (3,71), (5,36)):
    u = step(p*p)
    assert p*u%(r*(r-1)) == 0
    assert all(u%(q*q*(q-1)) == 0 for q in P if q != p)
    assert n%(p*p) == p
    assert (pow(3,C,p*p)+pow(5,D,p*p))%(p*p) == 0
    assert pow(3,J,p*p) == pow(5,2*J,p*p)
    a,b = ((pow(base,u,p*p)-1)//p for base in (3,5))
    assert pow(3,u,p) == pow(5,u,p) == 1 and a
    f0.append(pow((a*pow(3,C,p)+ray*b*pow(5,D,p))%p, -1, p))
    w.append(pow(3,-J,p))
    g.append(pow(3,u,r))
    assert g[-1] != 1 and pow(g[-1],p,r) == 1
    assert pow(5,ray*u,r) == pow(g[-1],k0,r)

assert (g,f0,w) == ([441,1445],[4,35],[2,23])
assert all(v != 1 and pow(v,h,p) == 1 for v,p in zip(w,P))
k = 194
assert tuple(k%p for p in P) == (5,36)

def trim(f):
    while f and f[-1] % r == 0: f.pop()
    return f
def rem(a,b):
    a = trim(a[:])
    inv = pow(b[-1],-1,r)
    while a and len(a) >= len(b):
        j = len(a)-len(b)
        u = a[-1]*inv%r
        for t,v in enumerate(b): a[j+t]=(a[j+t]-u*v)%r
        trim(a)
    return a
def mul(a,b,f):
    if not a or not b: return []
    c = [0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b): c[i+j]=(c[i+j]+u*v)%r
    return rem(c,f)
def Xpower(e,f):
    a,b=[1],[0,1]
    while e:
        if e&1: a=mul(a,b,f)
        b=mul(b,b,f)
        e//=2
    return a
def witness_gcd(N):
    f=[N**3%r,3*N*N%r,3*N%r,1]+[0]*25+[-1]
    z=Xpower(L,f)
    if z: z[0]=(z[0]-1)%r
    else: z=[-1%r]
    g=trim(z)
    while g: f,g=g,rem(f,g)
    return [x*pow(f[-1],-1,r)%r for x in f]
assert witness_gcd(n%r)==[1]
n2 = 16625594332193
assert (n2-n)%(12*prod(p**3 for p in P)) == 0 and n2%r == 2609
assert witness_gcd(n2%r)==[1381*2422%r,-(1381+2422)%r,1]
assert tuple(23%p for p in P)==tuple(w) and k*(23-1)%L==397
for X, digits in ((1381,(4,15)), (2422,(5,38))):
    assert prod(pow(v,d,r) for v,d in zip(g,digits))%r == X
assert 4 == f0[0] and 15 == f0[1]*w[1]%79
assert pow(5*pow(f0[0],-1,7),h,7) != 1
assert [(2609+pow(X,23,r)-beta*pow(X,397,r)*(2609+X))%r
        for X in (1381,2422)] == [3148,972]
print('OK')
```

The first digits are \(f_0w^j\bmod p\) because the two coefficients in each relay repair equation scale together along the spare line. Adding \(pu\) to the \(3\)-exponent when needed gives exact relay valuation two. The step checks make this lift invisible at the reader and at the other relay. These are certificates for the specified finite panel. A full square-sum witness still requires the remaining inert primes.

The univariate projection presumes the first reader term has no moving spare-phase factor and the second has one of exact order M. If both direct factors move, the simple elimination does not by itself apply. In the case that the projected polynomial is identically zero, the relaxed gcd is simply the whole order polynomial and supplies no absence certificate.
