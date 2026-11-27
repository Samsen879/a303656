# Two linked positive odd traces give a universal local split-prime selector

Use t=2τ²−1, s=2τ³−1. For τ=6 and τ=21 these give the two positive odd trace pairs (71,431) and (881,18521). Fix the same root r of r²=−3 and the same odd positive integer l in both tests, and use k=t s l. Then ρ=l r and
```
8(u²−v³) = 2(1+sρ)²−(1+tρ)³
u=(t+k r)/(2t), v=(s+k r)/(2s).
```
For τ=6 and 21 the right-hand cubics are respectively
```
−(ρ−1)(357911ρ²+1512ρ+1)
−(ρ−1)(683797841ρ²+71442ρ+1).
```
The resultant of the two displayed quadratic factors is 2^11 3^6 5^4 · 233 · 1824041, all prime to every p≡1 mod 3; the four traces are also units at each such prime. Thus at each split prime and every power of it, at least one quadratic factor is a unit, and both congruences hold exactly when ρ=1. The Chinese remainder theorem gives the same equivalence for every modulus supported on these primes, with **the same side and the same l in the two tests**. If a preexisting leaf supplies r, take an odd positive representative of its inverse modulo the leaf modulus. No leaf-norm increase is needed in this test; the weight can still grow with the modulus. It is a local branch selector, not a new ray or a global representation construction.

The full true Eisenstein half (5^27+3^27)/8 is replayed with its integer norm coordinates and all prime factors. On its p=379 block, the separate root sets are {1,112,180} and {1,55,151}; intersection keeps only 1. The joint rule also passes 19, where the relaxed 3/4 rule cannot separate the two sides. The optional mixed-side check exhibits a different finite residue at 700597, which cannot divide 5^U±3^V for odd U,V because 5 has nonsquare character and 3,−1 have square character there. The same-side proof does not need this exception analysis.

## Exact replay

```python
from math import gcd, isqrt

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

def branches(t,s,p):
    if t*s*(t-s)%p == 0:
        return []
    return [x for x in range(1,p)
            if (2*t*x**3-2*s*x*x+s-t)%p == 0
            and x*x*(x-1)**2*(2*x*x+4*x+3)%p]

def err(t,s,k,r,D):
    assert gcd(2*t*s,D)==1 and (r*r+3)%D==0
    out=[]
    for z in (r,-r):
        u=(t+k*z)*pow(2*t,-1,D)%D
        v=(s+k*z)*pow(2*s,-1,D)%D
        out.append((u*u-v**3)%D)
    return out

old=[(21,29),(21,25),(3,11),(7,15),(35,3)]
assert next(p for p in range(7,632,6) if prime(p)
            and all(len(branches(t,s,p))!=1 for t,s in old))==631
for p in (631,919,122041):
    assert prime(p) and [len(branches(t,s,p)) for t,s in old]==[3]*5

H=(5**9-3**9)//2
assert H==966721==863**2+3*272**2==511**2+840**2
r=863*pow(272,-1,H)%H
assert 5*107417+4*107409==H
assert err(4,-5,583617,r,H)==err(107417,107409,841011,r,H)==[0,754779]
assert all((H-5*t)%8!=4 or (H-5*t)//4>107416
           for t in range(1,107417,2))

a,b,c,d=357911,1512,683797841,71442
assert (a-c)**2+(a*d-b*c)*(d-b)==2**11*3**6*5**4*233*1824041
assert (a-c)**2+(-a*d-b*c)*(-d-b)==2**8*3**6*700597*4163597
P=(71,431,881,18521,233,1824041,4163597)
assert all(prime(p) and p%3==2 for p in P)

def F(q,x):
    t,s=2*q*q-1,2*q**3-1
    return 2*(1+s*x)**2-(1+t*x)**3

assert [[x for x in range(379) if F(q,x)%379==0] for q in (6,21)] == [
    [1,112,180],[1,55,151]]

def joint(D,r,l,other):
    assert l%2 and l*r%D==1
    for q,e in zip((6,21),other):
        t,s=2*q*q-1,2*q**3-1
        assert err(t,s,t*s*l,r,D)==[0,e]
    assert gcd(D,gcd(*other))==1

joint(H,r,1192999,(89100,788704))
assert ((5**133+3**37)//8)%19**2==38
assert err(4,-5,4,4,19)==[0,0]
joint(19,4,5,(9,0))

H=(5**27+3**27)//8
assert H==(-633978908)**2+3*420077085**2
P=(19,379,919,12979,10843039)
assert H==19*379*919*12979*10843039
assert all(prime(p) and pow(24*(8*25**3-3*25-1),(p-1)//2,p)==p-1
           for p in P)
r=-633978908*pow(420077085,-1,H)%H
joint(H,r,950137886422656851,(89100,170931600))
assert err(1249,31249,47994265427518826,r,H)==[0,487080000]

H=(5**29+3**9)//8
assert H%631**2==270068 and H%17**2==17
p,L=122041,15255
assert p==8*L+1 and L%2 and pow(3,L,p)==pow(5,L,p)==1
p=700597
assert prime(p) and F(6,394927)%p==F(21,-394927)%p==0
assert [pow(u,(p-1)//2,p) for u in (3,5,-1)]==[1,p-1,1]
print("PASS")
```
