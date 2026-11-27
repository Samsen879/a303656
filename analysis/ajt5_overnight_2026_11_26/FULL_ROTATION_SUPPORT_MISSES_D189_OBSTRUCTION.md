# Complete prescribed rotation moduli still miss a necessary first-chord test

At the genuine K=5684 target n with three exact second chords, try first displacement coordinate d=189 and slope a=12154207. For e=(a²+d²)/2, C=D−e, the first endpoints require
```
(2e u+aC)² = d² W,  W=2e(n−H)−C².
```
This follows from dx=au+C and the starting norm. At this n the slope lies in the required critical band, and W≡1024 mod 8192 gives the relevant two-adic square condition. But W≡10 mod 11 is nonsquare (and 11 does not divide d), excluding the chosen first direction.

The exact real comparison is a different target n' at the same ordinary height with a fully certified primitive first chord of exactly that d and a. The two integers agree modulo the **entire** least common multiple of the three second rotation norms, times 2^16·3^4·7². Thus every prime-power read contained in that product sees the same n and n', and none can distinguish this first-chord failure. Yet n' differs by 1 modulo 11 and has the actual coordinates. It does not itself satisfy the second construction's integer-square condition; this is a comparison, not a simultaneous first and second chord on n'. On the true original n all three second chords are still certified. No unrestricted same-target or growth conclusion is asserted here.

```python
from math import gcd, isqrt, lcm

L,K,b = 71,5684,64310
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
ms = (b-2,b,b+2)
ps = [m*m+1 for m in ms]
P = lcm(*ps)

r,M = 7,21
for m,p in zip(ms,ps):
    g = gcd(M,p)
    s = -m*(c+1)-r
    assert s%g==0
    r += M*(s//g*pow(M//g,-1,p//g)%(p//g))
    M = lcm(M,p)
X = isqrt(1<<K)
lo = (4*X+4)//5
t = lo+(r-lo)%M
n = 2*(t*t+c*c)+J
S = n-H

def check(n,U,V,H,D):
    S = n-H
    assert 25**(16*(L+1)) <= n <= 9**(32*L) and 2**K <= S < 2**(K+1)
    assert sum(z*z for z in U)==S and sum(z*z for z in V)==S+2*D
    d,w = V[0]-U[0],V[1]-U[1]
    q,h = (d*d+w*w)//2,d*U[1]-w*U[0]
    assert d%2 and w%2 and gcd(d,w)==1 and h%2==0
    assert 2*q*S==(D-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
    return q

qs = set()
for m,p in zip(ms,ps):
    v,rem = divmod(t+m*(c+1),p)
    assert rem==0
    f,g = (m*m-1)*v-m*(c+1),2*m*v-c-1
    qs.add(check(n,(t-c,t+c),(f-g,f+g),J,E))
assert len(qs)==3

d,a = 189,12154207
e = (a*a+d*d)//2
C = D-e
W = 2*e*S-C*C
assert 128*d*d*K*K < 2*e < 128*d*d*K*(K+1)
assert (S%8192,D%8192,W%8192,W%11)==(2426,4371,1024,10)
assert gcd(W*d,P)==1 and gcd(a,d)==1

M = P*2**16*3**4*7**2
z0 = 3279728225976070523987972216772348100
j = ((9*d*X//8-C)//a-135)//d
u = 135+d*(j+(z0-j)%M)
x,rem = divmod(a*u+C,d)
assert rem==0 and gcd(x,21)==1
n1 = x*x+u*u+H
assert (n1-n)%M==0 and (n1-n)%11==1
check(n1,(x,u),(x+d,a-u),H,D)
v,rem = divmod(n1-J,2)
assert rem==0 and (z:=v-c*c)>0 and isqrt(z)**2!=z
```
