# A phase test can distinguish genuine sources after ordinary order gates pass

In the neutral chart, if every menu tag has e(1−k)=d mod 7, and F is a verified 7-unit annihilator of the non-7 part of 3/5, each admissible prime must have ((3/5)x^(−d))^(49F)=1. On the actual (40,86) remainder, both certified factors pass the sign gate and all three original reads 3,5,3/5 have exact order 343 after the mask. Nevertheless the menu-phase gcd is 1, so it excludes both factors. The mask here comes from the known factorization; verification of the gcd is short.

## The whole-source seventh symbol is informative but not sign-selective

For the genuine unresolved (17,188) source R let y=x^49. Independently verified exact arithmetic gives a principal generator α of the ideal (R,ζ_7−y): evaluating α at y vanishes modulo R, and the determinant norm equals R, proving equality of ideals by index. The sum of coefficient indices weighted by coefficients is 0 mod 7, so α is congruent to a rational integer modulo (1−ζ_7)^2, and the coefficient sum is nonzero mod 7. Thus α is primary for [Eisenstein reciprocity](https://www.degruyterbrill.com/document/doi/10.1515/jmc-2020-0013/html). The reduced computations of α^((b^6−1)/7) modulo b=3,5 give exponents 5,6 respectively relative to ζ_7. These rational primes have order 6 modulo 7 and are inert in this cyclotomic ring, so the exponents are the two whole-source symbol logs. At any admissible p the menu requirement would be local log difference d(p−1)/343. Because p≡1 mod 343, summation with multiplicities would force d(R−1)/343 mod 7. Here d=4 and the resulting discrepancy is 6 mod 7; some supported factor does not match the phase requirement. This does not certify that such a factor is on the required sign side.

The actual (31,295) countercontrol is why one cannot conclude that. Its whole-source discrepancy is nonzero, but the sign-gate factor has a genuine matching coarse phase; the excluded-sign factor accounts for the discrepancy. No full closure of (17,188), no claim of full precision on the matching (31,295) factor, and no arbitrary-n conclusion are made.

```python
from itertools import permutations
from math import gcd, isqrt, prod

def chart(M, x, u, v, tags, d):
    assert pow(x, 343, M) == 1 and gcd(pow(x, 49, M)-1, M) == 1
    assert (1-x+pow(x, u, M)-pow(x, v, M)) % M == 0
    assert {e*(1-k) % 7 for e,k in tags} == {d}

def prime(p, *ls):
    a = prod(ls)
    assert a*a > p and (p-1) % a == 0 and pow(2,p-1,p) == 1
    for l in ls:
        assert all(l % j for j in range(2,isqrt(l)+1))
        assert gcd(p,pow(2,(p-1)//l,p)-1) == 1

def phase(p,x,a,b):
    s,r = divmod(p-1,343)
    assert r == 0 and s % 7
    assert (pow(3,s,p),pow(5,s,p)) == (pow(x,a*s,p),pow(x,b*s,p))
    return s

p,q = 45574318763,337621934255663
prime(p,66434867)
prime(q,55529759)
Q,x = p*q,13129993496012691450693331
chart(Q,x,40,86,[(3,200),(15,255)],5)
assert p%1372 == q%1372 == 687
phase(p,x,60,120)
phase(q,x,101,165)
F = (p-1)*(q-1)//7**6
b = 3*pow(5,-1,Q)%Q
for z in (3,5,b):
    assert pow(z,343*F,Q) == 1 and gcd(Q,pow(z,49*F,Q)-1) == 1
assert gcd(Q,pow(b*pow(x,-5,Q),49*F,Q)-1) == 1

p,q = 421761845597,402997726421332771
prime(p,23646661)
prime(q,5987,16232033)
M,x = p*q,68693850624006015651041237082
tags = [(34,100),(34,149)]
chart(M,x,31,295,tags,1)
assert (M%2401,p%1372,q%1372) == (1,1,687)
s,t = phase(p,x,141,107),phase(q,x,202,327)
assert {(e%7,e*k%7) for e,k in tags} == {(202%7,327%7)}
assert (s*(141-107-1)%7,t*(202-327-1)%7) == (3,0)

R,x = 626751537547263614426465772417729978972491,252568635021313874012910903862214825457075
chart(R,x,17,188,[(5,276),(15,165)],4)
assert gcd(R,105) == 1 and R%16807 == 4803
a = (-6479553,-6564780,-8918326,-9033544,-5733539,-12240864)
def unit(j):
    return tuple(int(i == j) for i in range(6))
def mul(u,v,m=0):
    w = [0]*7
    for i,c in enumerate(u):
        for j,d in enumerate(v):
            w[(i+j)%7] += c*d
    z = tuple(c-w[6] for c in w[:6])
    return tuple(c%m for c in z) if m else z

W = [mul(a,unit(i)) for i in range(6)]
N = sum((-1)**sum(v[i]>v[j] for i in range(6) for j in range(i+1,6))
        *prod(W[i][v[i]] for i in range(6)) for v in permutations(range(6)))
assert N == R and sum(c*pow(x,49*i,R) for i,c in enumerate(a))%R == 0
assert sum(a)%7 and sum(i*c for i,c in enumerate(a))%7 == 0
for p,L in [(3,5),(5,6)]:
    w = unit(0)
    for _ in range((p**6-1)//7):
        w = mul(w,a,p)
    assert w == (unit(L) if L<6 else (p-1,)*6)
assert (5-6-4*((R-1)//343))%7 == 6
```
