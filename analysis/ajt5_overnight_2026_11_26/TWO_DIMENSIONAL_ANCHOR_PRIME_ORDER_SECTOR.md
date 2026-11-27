# A genuinely two-dimensional anchor perturbation defeats one growing order sector

At bit-height H keep the fixed j=1 lane c≡3 mod 80,d≡1 mod 144 and the same prescribed target n. For prime t≡1 mod 720 in [H/24,H/16], use c=3t+80i,d=t+144k. In the actual chart the inert primes p≥7 with lcm(ord_p 27,ord_p 5) dividing 720 are exactly 7,11,19,31. At i=0,…,5 the three prime reads 7,19,31 ignore k and respectively hit at most 2,1,2 cells, leaving i₀; at k=0,1 the p=11 read ignores i and hits at most one, leaving k₀. These choices depend only on the same n. Expanding i=i₀+9u,k=k₀+5v gives both step sizes 720, retains all four unit readings, and fits the true exponent box for 0≤u,v<J with 720J+400≤H/16. After a 17 peel, one extra class v mod 17 per fixed u can be lost because 5^144≡103 mod 17².

For an actual inert p in a sector r|ℓ_p|720r, ℓ_p=lcm(ord_p 27,ord_p 5), a prime r>5 divides at least one effective order of the new chart coordinates, and that order is exactly r after the stride 720. Thus one p removes at most J ceil(J/r) cells. Every such p divides gcd(27^(720r)−1,5^(720r)−1) and is at least 2r+1. The number is O(r/log r). Taking J=r→∞ with r=o(H), even the entire actual prime sector removes only o(1) of the square, while the 17 factor removes ≤1/17+o(1). A finite sum of these period-sector capacities gives a sufficient condition for a survivor. If a fixed fraction survives for infinitely many prime t, a finite double count for each H selects one single translation (u,v) working at ≫H/log H prime t in that window. This is sector-level survival, not a two-square witness at each surviving label.

The actual 320,000-bit n in the replay singles out the failure of one-axis methods: the original prime-ray labels are marked by 7, and the entire fixed k=0 horizontal lane is marked by 11 at all large prime parameters. Both one-step attempts at the chosen label have valuation one somewhere, but the double move recovers a literal two-square certificate on the same n. Its lifted 23×23 square has 484 verified survivors of the specified full inert panel and the extra 17 test. The congruence fixture can also be repeated on a fixed prime arithmetic progression. This does not cover arbitrary mixtures of order sectors or all labels.

~~~python
from itertools import product
from math import gcd, isqrt, prod

def inert(n):
    out, d = [], 2
    while d*d <= n:
        if n%d == 0:
            if d > 5 and d%4 == 3:
                out.append(d)
            while n%d == 0:
                n //= d
        d += 1
    return out + ([n] if n > 5 and n%4 == 3 else [])

def crt(rows):
    M = prod(rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for m,a in rows.items())%M, M

def norm_mod_p2(R,p):
    x,y = next((x,y) for x in range(1,p) for y in range(p)
               if (x*x+y*y-R)%p == 0)
    x += p*((R-x*x-y*y)//p*pow(2*x,-1,p)%p)
    assert (x*x+y*y-R)%p**2 == 0
    return x,y

def panel(r):
    return inert(gcd(27**(720*r)-1,5**(720*r)-1))

P0,P = panel(1),panel(23)
assert P0 == [7,11,19,31]
assert P == [7,11,19,31,47,139,691,6211]
assert [next(e for e in range(1,p) if pow(3,80*e,p)==1) for p in P0] == [3,1,9,3]
assert [next(e for e in range(1,p) if pow(5,144*e,p)==1) for p in P0] == [1,5,1,1]
assert pow(5,144,289)==103 and pow(3,80,121)==1
assert all(pow(g,720,47)!=1 and pow(g,720*23,47)==1 for g in (3,5))

H,t,J = 320000,16561,23
assert t%720==1 and H<=24*t and 16*t<=H
assert all(t%d for d in range(2,isqrt(t)+1))

def S(i,k,m=None):
    c,d = 3*t+80*i,t+144*k
    return 3**c+5**d if m is None else (pow(3,c,m)+pow(5,d,m))%m

s = S(1,1)
X,Y = {120:17},{120:40}
for p in (17,19,31,139,691,6211):
    X[p],Y[p] = 1,0
for p,v in ((7,18),(11,54),(47,32)):
    m = p*p
    X[m],Y[m] = norm_mod_p2((v-s)*pow(85,-1,m)%m,p)
x,M = crt(X)
y,_ = crt(Y)
z = 2**(H//2-4)
x,y = z+(x-z)%M,z+(y-z)%M
n = s+85*(x*x+y*y)
assert n.bit_length()==H and (n%8,n%3,n%25,n%17)==(5,1,17,15)
assert (n%49,n%121,n%2209)==(18,54,32)
assert n-s==(7*x-6*y)**2+(6*x+7*y)**2
for (i,k),p in [((0,0),7),((0,1),7),((1,0),11)]:
    assert (n-S(i,k,p*p))%(p*p) in range(p,p*p,p)
for p,v,j0 in ((7,18,1),(11,54,2)):
    m = p*p
    assert [j for j in range(p) if
            (pow(27,1+720*j,m)+pow(5,1+720*j,m))%m==v] == [j0]
    assert (1+720*j0)%p==0

i0 = next(i for i in range(6) if all((n-S(i,0,p))%p for p in (7,19,31)))
k0 = next(k for k in range(2) if (n-S(i0,k,11))%11)
assert (i0,k0)==(1,1) and 720*J+400<=H//16
ok = [(u,v) for u,v in product(range(J),repeat=2)
      if all((n-S(i0+9*u,k0+5*v,p))%p for p in P)
      and (n-S(i0+9*u,k0+5*v,289))%289]
assert ok[0]==(0,0) and len(ok)==484
~~~
