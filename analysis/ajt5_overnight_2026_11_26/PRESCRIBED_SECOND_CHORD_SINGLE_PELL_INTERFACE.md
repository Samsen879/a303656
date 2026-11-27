# Prescribe the second chord's imaginary coordinates before a single common-target equation

Let A=9^(T+3), B=25^(T+3), with true offsets H=27A+5B, J=3A+125B and half-gaps D=9A+2B, E=A+50B. Set c=(E−1)/2. The second-label endpoints P=(1+i)(t+ic), Q0=(1+i)(t+i(c+1)) have the correct norm gap 2E for any integer t. If m is even, p=m²+1 and t=pv−m(c+1), then replacing Q0 by Q=(1+i)(m+i)(mv−c−1+iv) preserves that norm. Direct subtraction yields (Q−P)/(1+i)=−2v+i(2mv−E). Hence the true displacement is odd-odd and primitive iff gcd(v,E)=1. Exact arithmetic gives q=4v²+(2mv−E)² and 2S−p q=−4pmv+2E(m²−1)+p. This allows a critical second chord without fixing arbitrary Gaussian imaginary coordinates retrospectively.

A horizontal first chord with odd slope a and e=(a²+1)/2, c1=(D−e)/2 has lower norm 2(x²+c1²)/e with x=e u+a c1. Thus common n reduces to the single prescribed equation
```
x² − e t² = e(c²+(J−H)/2) − c1²,
x = a c1 mod e,  t = −m(c+1) mod p.
```
Reconstruct u,v from it, then separately check both strict angular windows and ordinary heights. This is a smaller arithmetic interface; no simultaneous solution within this new prospective subfamily was verified here.

The replay constructs true second-label primitive critical chords at K=450,720,3150, always with v_7(n−H)=1 and thus no first-label norm at the same n. The first-label obstruction happens before checking angles. The separately certified old K600 double positive is outside this subfamily, as proved by the modulo 11 read in the replay. These are ordinary-height same-target tests and not a source of arbitrary-n representations.

```python
from math import gcd, isqrt

def replay(T):
    L = T+3
    A, B = 9**L, 25**L
    H, D = 27*A+5*B, 9*A+2*B
    J, E = 3*A+125*B, A+50*B
    K, X = 90*L, 1 << (45*L)
    c = (E-1)//2
    m = 2*(isqrt(128*K*K)//2+1)
    p = m*m+1
    assert 128*K*K < p-1 < p+1 < 128*K*(K+1)
    t49 = 2 if (2*(4+c*c)+J-H)%49 else 9
    v49 = (t49+m*(c+1))*pow(p,-1,49)%49
    v0 = 1+E*((v49-1)*pow(E,-1,49)%49)
    lo = (4*X+5*m*(c+1)+5*p-1)//(5*p)
    v = lo+(v0-lo)%(49*E)
    t = p*v-m*(c+1)
    assert 4*X <= 5*t and 6*t <= 5*X and v > 16*m+4*E

    P = (t-c,t+c)
    a,b = (m*m-1)*v-m*(c+1), 2*m*v-c-1
    Q = (a-b,a+b)
    S = sum(z*z for z in P)
    n = S+J
    assert 25**(16*(L+1)) <= n <= 9**(32*L)
    assert all(2**K <= z < 2**(K+1) for z in (S,n-H,n-H+2*D))
    assert sum(z*z for z in Q) == S+2*E
    x,y = Q[0]-P[0], Q[1]-P[1]
    assert x%2 and y%2 and gcd(x,y)==1
    q,h = (x*x+y*y)//2, x*P[1]-y*P[0]
    assert h%2==0 and 2*q*S == (E-q)**2+h*h
    assert 64*K*K*q < S < 64*K*(K+1)*q
    assert (n-H)%7==0 and (n-H)%49!=0
    return K, n.bit_length(), (n-H)%49

assert [replay(T) for T in (2,5,32)] == [
    (450,451,21), (720,721,28), (3150,3151,42)]

# 旧 K600 的已证 u ≡ 14 (mod 22)
A,B = 9**6,25**6
a,u = 6787,14
C = 9*A+2*B-(a*a+1)//2
s = (a*u+C)**2+u*u+24*A-120*B
assert s%2==0 and (s//2-((A+50*B-1)//2)**2)%11==8
assert 8 not in {x*x%11 for x in range(11)}
```
