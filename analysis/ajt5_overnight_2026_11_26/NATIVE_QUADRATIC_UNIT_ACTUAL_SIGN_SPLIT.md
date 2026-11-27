# Native quadratic units can split a real mixed-sign remainder

At an actual order-343 root x put z=x^172, so z²=x, and U=z+sqrt(x−1), of norm one. At prime p outside the bad denominators the relevant cyclic norm-one group has order p−( (x−1)/p ). For the Lucas trace C_m(U+U^(-1))=U^m+U^(-m), reduction of C_m(2z)−2 detects exactly whether the local order divides m, since T+T^(-1)=2 in the residue field forces T=1. This is an additional native arithmetic read, not a whole-ideal conjugation or norm operation.

The exact finite two-stage window uses E=lcm of positive j≤1024 prime to 7 and uses E times one or an eligible prime 1024<l≤2^20. On the actual mixed-sign remainder (31,295), using only the composite M and x as inputs, this finds a nontrivial factor 421761845597; the exact full exponent m=140587281866 detects it and m/2 does not. On (17,188), for the two named native quadratic units, even multiplying the same window by 7^49 yields aggregate gcd 1. This is an order-window exclusion on that still unfactored source, not a closure.

There is also a separately tested split-only sign gate. A square root v of z is available in its odd-order cyclic subgroup. The unit W=(1+iv)/(1−iv) has trace t=2(1−z)/(1+z). The polynomial T³+T²−2T−1 vanishes on C_n(t) exactly when W^n has order 7. An inert p is 1 mod 343 and its norm-one group has order p+1, not divisible by 7; hence this gcd only captures split-sign factors. A known exponent on (31,295) recovers the same split factor; multiplying it by 7 gives gcd 1. This verification exponent is derived after the factor is known and is distinguished from the first discovery window. The source relation z^33=z+1 on (17,188) also makes 1+z a square there; the local norm-one square test for U then agrees with the quadratic character of 2 via (U+1)²=2(1+z)U. None of these statements closes that source.

```python
from math import gcd, isqrt, lcm

def C(t,n,M):
    a,b = 2,t%M
    for bit in bin(n)[2:]:
        c = (a*b-t)%M
        a,b = ((a*a-2)%M,c) if bit=='0' else (c,(b*b-2)%M)
    return a

B = 2**20
s = bytearray(b'\1')*(B+1)
for j in range(2,isqrt(B)+1):
    if s[j]:
        s[j*j::j] = bytes((B-j*j)//j+1)
L = [1]+[j for j in range(1025,B+1) if s[j]]
E = lcm(*(j for j in range(1,1025) if j%7))

def block(t,e,M):
    t,a = C(t,e,M),1
    for l in L:
        a = a*(C(t,l,M)-2)%M
    return gcd(M,a)

M,x = 169969064866856199529458159287,68693850624006015651041237082
z = pow(x,172,M)
p = block(2*z,E,M)
assert p == 421761845597
m = 140587281866
assert gcd(M,C(2*z,m,M)-2)==p and gcd(M,C(2*z,m//2,M)-2)==1
t = 2*(1-z)*pow(1+z,-1,M)%M
for n,want in [(30125846114,p),(7*30125846114,1)]:
    a = C(t,n,M)
    assert gcd(M,a**3+a*a-2*a-1)==want

R,x = 626751537547263614426465772417729978972491,252568635021313874012910903862214825457075
z = pow(x,172,R)
r = pow(z,33*172,R)
assert pow(z,33,R)==(z+1)%R and r*r%R==(z+1)%R
assert 7**49 <= R+1 < 7**50
for t in (2*z,2*pow(r,-1,R)):
    assert block(t,7**49*E,R)==1
```
