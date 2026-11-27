# Short native trace relations require overlap, and half-angle screening is not universal

At a split prime, let original norm-one units U,V have orders m,n and common subgroup order g=gcd(m,n)>2. Its two corresponding generators differ by a unit exponent modulo g. Write h=ceil(sqrt(g)); among the first h+1 multiples of that exponent two lie in the same one of h intervals of length at most h. Their nonzero difference has magnitude ≤h−1<g/2 and therefore cannot give order 1 or 2. Up to sign it gives a genuine trace match with a≤(m/g)(h−1), b≤(n/g)h. In particular when p≤P and the ambient group index relative to g is ≤J, one may search the square of side ceil(sqrt((P+1)J))+J. Those upper bounds are additional input; nontrivial overlap alone allows long matches, e.g. element orders 3,3L.

For the original 343-chart let z=x^172, v²=z. Half-angle traces t_±=(z+1±i(z−1))/v correspond to units P,Q with P²=UV, Q²=U/V. At p=3 mod 4, Frobenius exchanges P,Q with a common possible inversion (the two roots can be written using (1±i)sqrt(z²−1)/v). If P^a=Q^(±b), apply Frobenius and eliminate the other unit to get P^(a²−b²)=Q^(a²−b²)=1. Thus the Gaussian norm of the trace difference can first collect matching support, then deleting support with the corresponding trace 2 conditions leaves only split primes.

The genuine split prime 485689 at a true native address has original exact orders 5 and 48569, coprime and odd. It cannot be captured by the original nontrivial joint rule. The half-angle rule also fails there: from a match and its square, coprimality forces m|a∓b and n|a±b, hence both odd orders divide a²−b². The half-angle units have the same two-primary part of size at most two, and a nontrivial such part forces a,b to have the same parity, so the deletion removes that prime. The exact replay gives an actual match at (145706,1) and its deletion.

At the real mixed-sign (31,295) remainder the half-angle read does retain the true split factor in a calibrated comparison. At (17,188) all 1089 pairs with 1≤a,b≤33 of the named half-angle traces have aggregate matching gcd 1. This leaves the latter source unfactored and gives no guarantee outside the checked window. No pointwise A303656 implication is made.

```python
from math import gcd, isqrt

def C(t,n,M):
    def mul(u,v):
        a,b=u
        c,d=v
        return ((a*c-b*d)%M,(a*d+b*c)%M)
    a,b=(2,0),t
    def sub(u,v):
        return ((u[0]-v[0])%M,(u[1]-v[1])%M)
    for bit in bin(n)[2:]:
        c=sub(mul(a,b),t)
        a,b=(sub(mul(a,a),(2,0)),c) if bit=='0' else (c,sub(mul(b,b),(2,0)))
    return a

def half(z,M):
    iv=pow(pow(z,172,M),-1,M)
    return ((z+1)*iv%M,(z-1)*iv%M)

def keep(g,c,M):
    return g//gcd(g,pow(c,M.bit_length(),g))

def joint(t,a,b,M):
    u,v=C(t,a,M)
    w,x=C(t,b,M)
    g=gcd(M,(u-w)**2+(v+x)**2)
    e,f=C(t,abs(a*a-b*b),M)
    return g,keep(g,gcd(e-2,f),M)

p,x=485689,256108
for q in (5,17,2857,p):
    assert all(q%d for d in range(2,isqrt(q)+1))
assert p%1372==1 and pow(x,343,p)==1!=pow(x,49,p)
z=pow(x,172,p)
G,H=(pow(b,1416,p) for b in (3,5))
assert pow(G,337,p)==x
assert (1-x+pow(H,178,p)-pow(H,194,p))%p==0
for t,m,fs in [(2*z,5,[5]),(2*pow(z,-1,p),17*2857,[17,2857])]:
    assert C((t,0),m,p)==(2,0)
    assert all(C((t,0),m//d,p)!=(2,0) for d in fs)
assert joint(half(z,p),145706,1,p)==(p,1)

p,q=421761845597,402997726421332771
M=p*q
z=pow(68693850624006015651041237082,172,M)
c=C((2*z,0),(q-1)//2,M)[0]
d=C((2*pow(z,-1,M),0),(q+1)//2,M)[0]
assert gcd(M,c-d)==q and keep(q,c*c-4,M)==1
assert joint(half(z,M),59118,818478,M)==(p,p)

R=626751537547263614426465772417729978972491
z=pow(252568635021313874012910903862214825457075,172,R)
t=half(z,R)
assert pow(z,33,R)==(z+1)%R and t[0]==pow(z,-139,R)
A=[C(t,a,R) for a in range(1,34)]
s=1
for u,v in A:
    for w,x in A:
        s=s*((u-w)**2+(v+x)**2)%R
assert s==335176245621623052119282807294155621946354
assert gcd(R,s)==1
```
