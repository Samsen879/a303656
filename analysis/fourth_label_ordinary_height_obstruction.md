# A full ordinary-height obstruction for one fixed fourth label

For infinitely many pairs of growing exponents, an affine family from [#94](https://github.com/Samsen879/a303656/pull/94) has genuine three-label targets at ordinary height, but a specified fourth label fails at every target in the ordinary-height window on that family. The obstruction tests the full residual, not a sublattice of coordinate pairs.

## Strand and all possible parameters

For \(1\le V\le U\), set \(T=5^U,W=3^V\), \(Q=15625T^2\),
\[
p=(51T-19W)/6,\quad q=(51T+19W)/6,\quad G=p^2+q^2,\quad R=(T^2+W^2)/2.
\]
The positive integers \(p,q\) are coprime because \(p+q=17T\) and \(q-p=19W/3\) are coprime. Let \(z_0=(x_0,y_0)\) be the unique integer point with \(0\le x_0<q\) and \(px_0+qy_0=R\). Put \(z=z_0+\tau(q,-p)\), \(C=20821T^2+2903W^2\), \(n=C+|z|^2\). At \(j=-12,-6,12\), respectively, the rows \(z+j(p,q)\) give the actual labels
\[
(2V+3,2U+2),\quad (2V+7,2U+6),\quad (2V+1,2U).
\]
In fact the corresponding shifts \(s_j\) satisfy \(s_j+2jR+j^2G=C\). The fourth label tested here has shift \(s=5T^2+243W^2\), i.e. \((2V+5,2U+1)\).

Set \(L=qx_0-py_0\). Direct substitution gives \(L/G=x_0/q-pR/(qG)\), so \(-1/144<L/G<1\) since \(R\le T^2\) and \(G\ge(2601/18)T^2\). Also \(|z|^2=R^2/G+G(\tau+L/G)^2\). Thus \(n<5Q\) implies
\[
|\tau+L/G|^2<57304\cdot18/2601<(20-1/144)^2,
\]
so all candidates have \(-20\le\tau\le19\). The \(Q<n\) lower bound is automatic since \(C>Q\). For \(\tau=0\), the upper bound is automatic: \(G\le(2601+361)T^2/18\) and \(|L/G|<1\). All first-three norms are positive there: \(n>s_j\), since \(s_j\le17812T^2<C\). The same inequality applies anywhere on the strand.

## Exact certificate and infinite progression

Let \(F=n-s\). At the seed \((U,V)=(9,7)\), for every odd \(\tau\in[-20,19]\), \(F=6\bmod8\). For the even \(\tau=-20,-18,\ldots,18\), the replay verifies valuation one at the corresponding prime in this list:
\[
31,23,3,3,7,3,3,31,1867,324151,7,3,3,1447,3,3,19,7,7,23 .
\]
All these primes are \(3\bmod4\). Such a prime dividing \(a^2+b^2\) would divide both coordinates, hence divide the norm to at least the second power. The square residues modulo 8 also exclude 6. These tests rule out all fourth coordinates. In particular the table includes \(\tau=-20\), which is outside the height window at the seed but could not be discarded before taking the progression.

Let \(M=8\prod p^2\), over the distinct listed primes, \(B=6\cdot646M\), and \(D=453274310894536143915556514861113344000\). On \((U,V)=(9+iD,7+iD)\) for \(i\ge0\), the values \(T,W\) are fixed modulo \(B\): the replay checks \(5^D=1\bmod B\), and \(3^D=1\) modulo the part of \(B\) coprime to 3. On the 3-primary part \(W\) is identically zero.

In fact, on this progression, the canonical base point is given by
\[
646z_0=(19T-51W,19T+51W)+12(q,-p).
\]
It is integral by congruence to the seed, and its dot product with \((p,q)\) is \(R\) after division. Because \(W/T\le3^7/5^9\), its first coordinate is positive and at most \((114/51+12)q/646<q\). Therefore \(p,q,z_0\) and \(F\) for every fixed \(\tau\) are constant modulo \(M\). The entire certificate persists on the progression, and \(\tau=0\) gives unbounded genuine three-label targets.

## Controls and reproduction

The finite scan exhausts \(1\le V\le U\le10\) and every ordinary-height \(\tau\). It finds 2,186 candidates, of which 1,095 fail modulo 8, 745 fail at a small test prime, 125 fail at another verified prime, and 221 are distinct four-label targets with explicit fourth coordinates. The only layer with no such target in this scan is \((9,7)\). The known positive control \((3,2,-5)\) gives \(371992113-s=19164^2+2153^2\); the negative control \((1,1,-17)\) has \(F=7^2\cdot163\cdot199\), so being divisible by 7 alone is not an obstruction.

Run the following block with Python 3.9+ and SymPy. The factorizer is used only to find candidate factors; decisions are certified by exact prime and valuation checks or by recovering integer coordinates.

```python
from math import gcd, isqrt, prod
from sympy import factorint

PANEL = (3,7,11,19,23,31,43,47,59,67,71,79,83,103)
EVEN = (31,23,3,3,7,3,3,31,1867,324151,7,3,3,1447,3,3,19,7,7,23)

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

def oddval(n,p):
    parity = 0
    while n % p == 0:
        n //= p
        parity ^= 1
    return parity

def data(U,V,t):
    T,W = 5**U,3**V
    p,q = (51*T-19*W)//6,(51*T+19*W)//6
    R = (T*T+W*W)//2
    assert gcd(p,q) == 1
    x0 = R*pow(p,-1,q) % q
    y0 = (R-p*x0)//q
    x,y = x0+t*q,y0-t*p
    n = 20821*T*T+2903*W*W+x*x+y*y
    shifts = (25*T*T+27*W*W,15625*T*T+2187*W*W,T*T+3*W*W)
    assert all(n-s == (x+j*p)**2+(y+j*q)**2 > 0
               for s,j in zip(shifts,(-12,-6,12)))
    return n,n-5*T*T-243*W*W,15625*T*T,(x0,y0,p,q)

def coordinates(factors):
    x,y = 1,0
    for p,e in sorted(factors.items()):
        if p%4 == 3:
            assert e%2 == 0
            x,y = x*p**(e//2),y*p**(e//2)
            continue
        if p == 2:
            a,b = 1,1
        else:
            z = 2
            while pow(z,(p-1)//2,p) != p-1:
                z += 1
            r,a = p,pow(z,(p-1)//4,p)
            while a*a > p:
                r,a = a,r%a
            b = isqrt(p-a*a)
            assert a*a+b*b == p
        for _ in range(e):
            x,y = x*a-y*b,x*b+y*a
    return x,y

assert 57304*18*144**2 < 2601*(20*144-1)**2
assert all(prime(p) for p in set(PANEL+EVEN))
tot = [0]*5
targets,empty = set(),[]
for U in range(1,11):
    for V in range(1,U+1):
        hits = 0
        for t in range(-20,20):
            n,F,Q,_ = data(U,V,t)
            assert F > 0 and n > Q
            if n >= 5*Q:
                continue
            tot[0] += 1
            if F%8 == 6:
                tot[1] += 1
                continue
            if any(oddval(F,p) for p in PANEL):
                tot[2] += 1
                continue
            fac = factorint(F)
            bad = [p for p,e in fac.items() if p%4 == 3 and e%2]
            if bad:
                p = min(bad)
                assert prime(p) and oddval(F,p)
                tot[3] += 1
                continue
            x,y = coordinates(fac)
            assert x*x+y*y == F
            tot[4] += 1
            hits += 1
            targets.add(n)
        if not hits:
            empty.append((U,V))
assert tot == [2186,1095,745,125,221] and len(targets) == 221
assert empty == [(9,7)]
assert data(3,2,-5)[:2] == (371992113,19164**2+2153**2)
assert data(1,1,-17)[1] == 1589413 == 7**2*163*199

T,W = 5**9,3**7
for t in range(-20,20):
    n,F,Q,(x,y,p,q) = data(9,7,t)
    assert (646*x,646*y) == (19*T-51*W+12*q,19*T+51*W-12*p)
    if t%2:
        assert F%8 == 6
    else:
        a = EVEN[(t+20)//2]
        assert a%4 == 3 and F%a == 0 and F%(a*a) != 0

M = 8*prod(p*p for p in set(EVEN))
B = 6*646*M
D = 453274310894536143915556514861113344000
B0 = B
while B0%3 == 0:
    B0 //= 3
assert pow(5,D,B) == 1 and pow(3,D,B0) == 1 and 3**7%(B//B0) == 0
print(tot, empty, D)

```

The argument concerns only this fourth shift and this strand, and says nothing about other labels or whether the conjecture holds at every target.
