# Verified modular order chains extract Gaussian factors

Let R be a positive odd remainder. Verify a^(2^s K)=1 mod R with K odd and s>=2. Define C=gcd(R,a^(2K)−1) and D_j=gcd(R,a^(2^j K)+1) for 1<=j<s. These factors are pairwise coprime and multiply to R: on each prime power in R the order's odd part divides K, and its two-part determines precisely one bucket. If the two-part is 1 or 2 it belongs to C; if it is 2^(j+1), uniqueness of the order-two element in an odd prime-power unit group puts the entire power in D_j.

Each D_j has a modular root of minus one, namely a^(2^(j−1)K). More generally, the Gaussian gcd of R and t+i has norm exactly gcd(R,t²+1): imposing t+i=0 reduces the Gaussian ring to the integer quotient at t²+1, and then imposing R gives that quotient index. Thus Euclidean descent can produce square coordinates of each extracted divisor without factoring R. If R=1 mod 4 and all tested inert valuations are even, C below the product of the two smallest untested inert primes guarantees R is a norm. The extracted factors are odd norms; failure in C would require two distinct remaining inert primes.

At n=5277, the same modular exponent 900 at base 3 yields a true norm at (c,d)=(3,4) and a sharp failure at (3,2), with cofactors 37 and 209 respectively. Another real control R=341 passes the base-two Fermat test but yields no extracted factor. The method requires a verified order bound and a small or otherwise certified cofactor; it does not find them uniformly for prescribed n or change the global conclusions.

```python
from math import gcd, prod

def gg(a, b):
    while b != (0,0):
        x,y = a
        u,v = b
        D = u*u+v*v
        p = (2*(x*u+y*v)+D)//(2*D)
        q = (2*(y*u-x*v)+D)//(2*D)
        a,b = b,(x-p*u+q*v, y-p*v-q*u)
    return a

def parts(R, a, K, s):
    assert R%2 and K%2 and pow(a,2**s*K,R)==1
    C = gcd(R,pow(a,2*K,R)-1)
    out = []
    for j in range(1,s):
        t = pow(a,2**(j-1)*K,R)
        u,v = gg((R,0),(t,1))
        D = gcd(R,t*t+1)
        assert u*u+v*v == D
        out.append(D)
    assert C*prod(out) == R
    return C,out

n = 5277
for d,want in ((4,(37,[125])), (2,(209,[25]))):
    R = n-3**3-5**d
    assert R%4==1 and R%3 and R%7 and 4*max(3**3,5**d)<n
    C,D = parts(R,3,225,2)
    assert (C,D) == want
    if C == 37:
        u,v = gg((R,0),(pow(3,225,R),1))
        assert (6*u-v)**2+(u+6*v)**2 == R
    else:
        assert C==11*19 and R%11==R%19==0 and R%121 and R%361

R = 393-3**3-5**2
assert R==341 and R%8==5 and parts(R,2,85,2)==(341,[1])
assert R%11==R%31==0 and R%121 and R%961
print("Same-target norm, exact threshold failure, and Fermat countercontrol")

from math import isqrt
N=5277-3**3-5**4
assert any(isqrt(N-x*x)**2==N-x*x for x in range(isqrt(N)+1))
for m in (5225,341):
    assert not any(isqrt(m-x*x)**2==m-x*x for x in range(isqrt(m)+1))
print("Independent two-square tests passed")
```
