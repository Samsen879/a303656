# A new actual common-target double chord at K=600

There is a new finite true same-target witness for labels (7,6) and (6,7), at one 601-bit n in the ordinary height window 25^112≤n≤9^192. Both chords have positive endpoint norms at their actual label offsets, primitive odd-odd differences, and strict critical inequalities 64K² q<S<64K(K+1)q. The first chord uses a short conjugation at its upper endpoint instead of the lower endpoint. Reorienting one Gaussian factor of the second upper endpoint keeps that endpoint's exact norm and the actual n, but takes the chord out of the strict window.

For first lower endpoint P=(au+C,u) set N=a²+1, C=D1−N/2, X=Nu+aC. Then N N(P)=X²+C², where N(P) denotes the squared Gaussian norm. Fix auxiliary factors F_j and imaginary coordinates y_j for the second two endpoints; if H1 and H_j are the appropriate true offsets, a common n requires simultaneous equations
```
X² − N F_j x_j² = N(F_j y_j² + H_j − H1) − C²
X = N u0+aC (mod N M).
```
The exact replay searches the one specified progression t=0,…,80000 and reconstructs both real parts at its unique hit t=75368. A true local divisibility member at t=0 does not have the requested real parts. The y_j were selected from finite prior angle-network data; the replay does not show how to choose them prospectively for arbitrary K or n. This finite double-label certificate is actual progress beyond the previous CRT-only K48000 target, not unbounded double-label growth and not an arbitrary-n result.

```python
from math import gcd, isqrt, prod

K, a, m = 600, 6787, 14400046
A, B = 9**6, 25**6
H, D = 27*A + 5*B, 9*A + 2*B
J, E = 3*A + 125*B, A + 50*B
N = a*a + 1
C = D - N//2
u0 = 360165488669719066380158365418059146498446585474721863599984289580194572185775984692960
M = 368862822831548233763975618941968980185300159619158867680
ps = ([5,13,37,41,53,61,89,101,113,149],
      [97,137,197,241,269,277,281,293,313,317])
ys = (3796713935821576759584338023569888051395527146283849097710947607804382838907629958,
      702724280090385625802700197716694807905480521468684616634436264984530151775528)
F, shifts = (4*prod(ps[0]), 2*prod(ps[1])), (J, J-2*E)

def real_part(X, i):
    z, rem = divmod(X*X+C*C+N*(H-shifts[i]), N*F[i])
    z -= ys[i]**2
    if rem or z < 0:
        return None
    x = isqrt(z)
    return x if x*x == z else None

p = m*m+1
assert M % p == 0 and all(M % f == 0 for f in F)
s0 = (a*u0+C)**2 + u0*u0
assert all((s0+H-h) % f == 0 for f,h in zip(F,shifts))
assert (m*(a*u0+C+1)-(a-u0)) % p == 0
assert ((a*u0+C+1)+m*(a-u0)) % p == 0
assert real_part(N*u0+a*C, 0) is None

hits = []
for t in range(80001):
    u = u0 + M*t
    X = N*u + a*C
    x = real_part(X, 0)
    if x is not None:
        y = real_part(X, 1)
        if y is not None:
            hits.append((t,u,x,y))
assert [row[0] for row in hits] == [75368]
_, u, x, y = hits[0]

def mul(z, w):
    a,b = z
    c,d = w
    return a*c-b*d, a*d+b*c

def norm(z):
    return sum(v*v for v in z)

def split(p):
    for x in range(1, isqrt(p)+1):
        y = isqrt(p-x*x)
        if x*x+y*y == p:
            return x,y
    raise AssertionError(p)

def endpoint(i, x, mask):
    z = ((2,0),(1,1))[i]
    factors = [*map(split, ps[i]), (x,ys[i])]
    for j,(v,w) in enumerate(factors):
        z = mul(z, (v, -w if (mask >> j) & 1 else w))
    return z

P = (a*u+C,u)
Q0 = (P[0]+1,a-u)
l,j = mul(Q0,(m,1))
assert l % p == j % p == 0
Q = mul((l//p,j//p),(m,1))
V,W = endpoint(0,x,1798), endpoint(1,y,1282)
n = norm(P)+H
assert n.bit_length() == 601 and 25**112 <= n <= 9**192

def check(U,Z,h0,d0):
    S = n-h0
    x,y = Z[0]-U[0], Z[1]-U[1]
    assert norm(U) == S and norm(Z) == S+2*d0
    assert x%2 and y%2 and gcd(x,y) == 1
    q = (x*x+y*y)//2
    h = x*U[1]-y*U[0]
    assert h%2 == 0 and 2*q*S == (d0-q)**2+h*h
    assert 2**K <= S < 2**(K+1)
    return S,q

for U,Z,h,d in ((P,Q,H,D),(V,W,J,E)):
    S,q = check(U,Z,h,d)
    assert 64*K*K*q < S < 64*K*(K+1)*q

for U,Z,h,d in ((P,Q0,H,D),(V,endpoint(1,y,1280),J,E)):
    S,q = check(U,Z,h,d)
    assert S < 64*K*K*q

print("verified", K, n.bit_length(), hits[0][0])
```
