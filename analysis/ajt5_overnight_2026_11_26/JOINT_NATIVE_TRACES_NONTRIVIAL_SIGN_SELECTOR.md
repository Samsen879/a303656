# A simultaneous trace match can isolate split sign if the common value is nontrivial

With z=x^172, put D=z²−1. The units U=z+sqrt(D) and V=(1+sqrt(−D))/z have norms one and traces 2z and 2/z. Their local orders divide p−(D/p) and p−(−D/p) respectively. At p=3 mod 4 the orders divide p−1 and p+1 in some order, so their gcd is at most 2. This holds without knowing the factorization of the source.

For actual inputs compare c=C_a(2z) and d=C_b(2/z), where C_m is the Lucas trace. At any matching p the roots of T²−cT+1 show U^a=V^(±b). If c²≠4, the common root has order bigger than two, hence the p has split sign. One may compute the full matching gcd and then remove the entire prime-power support of c²−4 by powering before taking its gcd. On the true (31,295) composite remainder one prescribed exponent pair detects split p=421761845597, but a second pair without the deletion detects the actual inert factor 402997726421332771 at −2. Exponents for these finite positive/negative controls were chosen from known factor data, not by a guaranteed discovery algorithm.

On the still-unfactored (17,188), all 1089 exact pairs 1≤a,b≤33 have aggregate gcd 1. This is a precise finite obstruction, not a factorization. The actual source relation z^33=1+z also gives public squares v²=z, r²=1+z. Then A=(U+1)/r, B=v(V+1)/r have A²=2U and B²=2V. The half-angle criterion therefore puts U and V on the same norm-one square character (2/p), but at inert p their ambient groups have coprime odd parts. This is local structure and does not identify which original prime is inert.

```python
from math import gcd

def C(t,n,M):
    a,b = 2,t%M
    for bit in bin(n)[2:]:
        c = (a*b-t)%M
        a,b = ((a*a-2)%M,c) if bit=='0' else (c,(b*b-2)%M)
    return a

def match(M,z,a,b):
    c = C(2*z,a,M)
    d = C(2*pow(z,-1,M),b,M)
    g = gcd(M,c-d)
    return g,g//gcd(g,pow(c*c-4,M.bit_length(),g))

p,q = 421761845597,402997726421332771
M = p*q
z = pow(68693850624006015651041237082,172,M)
assert match(M,z,438798,379680)==(p,p)
assert match(M,z,(q-1)//2,(q+1)//2)==(q,1)

R = 626751537547263614426465772417729978972491
x = 252568635021313874012910903862214825457075
z = pow(x,172,R)
assert pow(x,343,R)==1 and gcd(R,pow(x,49,R)-1)==1
assert pow(z,33,R)==(z+1)%R and gcd(R,2*(z*z-1))==1
A = [C(2*z,a,R) for a in range(1,34)]
B = [C(2*pow(z,-1,R),b,R) for b in range(1,34)]
d = 1
for a in A:
    for b in B:
        d = d*(a-b)%R
assert d==262727204336491956460805331640981067969319
assert gcd(d,R)==1
```
