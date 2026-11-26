# Retained cube cancellation digits can split after an ordinary repair

On an aligned equal-depth cube chart use source factors A U^x and B V^y modulo p^4, with U,V in 1+pZ_p, and set W=V^mu for the actual terminal discrete-log slope mu. When the terminal coefficients are opposite, cancellation at lower coordinate x requires source reading F(x)=A U^x+B W^x modulo p^4. Fix a lower reading t=F(x) mod p³. For the same first-digit block, expanding U^(pz) and W^(pz) gives
(F(x+pz)-t)/p³ = (F(x)-t)/p³ + z D(x) mod p,
where D(x)=[A U^x (U^p-1)+B W^x (W^p-1)]/p³ mod p. Slope alignment makes the numerator divisible by p³; quadratic terms in the expansion vanish modulo p^4. If two distinct lower coordinates in the block are genuinely retained-compatible and have identical fixed factors, a nonzero D(x) therefore gives distinct cancellation digits and removes a common collapse. This is a same-conditioning local criterion.

A separate test controls whether that reading was charged at all. Starting from a retained-compatible phase matching t mod p³, a nonzero change to a free second source digit on an ordinary axis gives exact source valuation two. To legalize the change, process the affected older rows and their repair descendants in increasing order. A sufficient certificate assigns an available ordinary primary axis at each such reader; every later retained row that reads this edited coordinate must be included in the closure. All visited primes are greater than the source prime, so their primary repairs can preserve the source valuation. If this certificate exists for one source axis, the reading already has a robust phase and never enters the exceptional-intercept branch. This requires that repairs preserve all fixed boundary periods, not just the displayed rows.

At p=71 and q=715823, repairing reader 50411 from valuation one to two gives retained-compatible coordinates 0 and 71 at t=87609 mod p³. Both lines have exact source valuation four after final adjustment, and cancel at fourth digits 14 and 25, respectively. The same older observations and small-head residues are kept; only the source observation is varied between the two cancellation tests. The arithmetic replay checks the named observables, and all other older inert rows are ordinary, with usable primary coordinates not appearing in any named order support (the small head rows are held fixed). Thus unnamed rows can be completed in increasing order without changing these readings. For the same reason the source has a robust phase: perturb the second digit and repair all affected ordinary readers in increasing order. This ordinary-terminal example is outside the charged exceptional branch and supports no unconditional subtraction.

```python
from math import isqrt, lcm

p, r, s, q = 71, 50411, 100823, 715823
c, d, n0 = 10082, 45369, 2420068764704544
P, H = p**3, 3960
assert q == 2*P+1 and r == 10*p*p+1 and s == 2*r+1
for v in (p,r,s,q):
    assert v%4 == 3 and all(v%i for i in range(2,isqrt(v)+1))
    assert all(pow(b,v-1,v*v) != 1 for b in (3,5))
assert pow(5,10,121) == 78
assert 14*r+1 < q < 18*r+1
assert (6*r+1)%11 == (10*r+1)%3 == (14*r+1)%5 == 0

def S(z,m):
    a,b = z
    return (pow(3,a,m)+pow(5,b,m))%m

def crt(n,M,a,m):
    return n+M*((a-n)*pow(M,-1,m)%m)

L = lcm(H,p-1,10*r**3,2*s)
def point(x,n,h):
    J = p**h
    a,b = c+L*((x-c)*pow(L,-1,J)%J),d
    for i in range(h):
        step,m = L*p**i,p**(i+2)
        b += step*next(k for k in range(p) if S((a,b+step*k),m)==n%m)
    return a,b

low = [point(x,n0,2) for x in (0,p)]
T = lcm(32,3,7,11,19,23,p**5,q*q)
N = crt(n0,T,S(low[0],r*r)+r,r*r)
assert (N-S(low[0],r*r))%(r*r) == r and (N-S(low[1],r))%r
J = lcm(H,p**4*(p-1),q-1,r-1)
a,b = low[0]
k = next(j for j in range(r) if S((a,b+J*j),r*r)==N%(r*r))
if S((a,b+J*k),r**3)==N%r**3:
    k += r
new = (a,b+J*k)
assert (N-S(new,r**3))%r**3 in range(r*r,r**3,r*r)
N = crt(N,T*r**3,0,s)
for z in low+[new]:
    assert S(z,P)==N%P==87609 and (N-S(z,s))%s
    assert (N-S(z,32))%32==18 and (N-pow(5,z[1],3))%3
    assert all((N-S(z,v))%v for v in (7,11,19,23))

for digit in (14,25):
    source = N%P+P*digit
    for i,x in enumerate((0,p)):
        pts = [point(x+p*p*j,source,3) for j in range(p)]
        if i==0:
            pts = [(a,b+J*k) for a,b in pts]
        pts = [(a,b+L*p**3) if (source-S((a,b),p**5))%p**5==0 else (a,b) for a,b in pts]
        assert all((source-S(z,p**5))%p**5 in range(p**4,p**5,p**4) for z in pts)
        anchor = (new,low[1])[i]
        assert {S(z,r**3) for z in pts} == {S(anchor,r**3)}
        assert {S(z,s) for z in pts} == {S(anchor,s)}
        shifts = {S(z,q) for z in pts}
        assert shifts=={0} if digit==(14,25)[i] else len(shifts)==p
print("Same retained boundary, legal reader repair, cancellation digits 14 and 25")

# Narrow independent arithmetic status check up to the real control's terminal.
primes=bytearray(b'\x01')*(q+1)
primes[:2]=b'\x00\x00'
for v in range(2,isqrt(q)+1):
    if primes[v]:
        primes[v*v:q+1:v]=bytes((q-v*v)//v+1)
assert [v for v in range(7,q+1,4) if primes[v] and pow(3,v-1,v*v)==1]==[11]
assert (r-1,s-1,q-1)==(10*p**2,2*r,2*p**3)
print("Named supports and ordinary status below control terminal verified")
```
