# Charge cube case 3 to the reachable older exceptions

Use p for the ordinary source and q for the terminal. Keep exactly the rows retained by the original cube proof after both axes' depth-three readers are dropped. Let G be the original case-3 event: the observed source digit t modulo p³ matches an available phase, but no phase compatible with the retained tests gives even valuation zero or two. Its original uniform gate bound is p^(-2).

For a fixed source axis, a second-digit change can affect only retained reader rows r whose order on this axis is divisible by p². At each reached row fix in advance an axis of minimum lifting depth (choose either minimum in a tie). Add to the closure any later retained reader of the edited primary coordinate on that axis. These shifts fix all non-primary coordinates, and the dependence of an r-adic order on primary coordinates at an unrelated prime is unchanged by raising its r-adic precision. The small-head periods have no source or repair prime in their support.

Fix t and the observations outside the closure. If no phase matches t and the outside tests, G is empty. Otherwise choose such a phase before reading the closure. A nonzero second-digit adjustment on the source produces exact valuation two. Process the closure in increasing order, preserving the source and all earlier observations. A reader r can stop the trial only at an odd valuation below its minimum available lifting depth e_r, as ordinary lifting repairs any collision at or above that depth to a safe even shell. The shift is selected before n_r is read, so the charge per trial step is at most beta_r=(1-r^(-2 floor(e_r/2)))/(r+1). Ordinary rows have beta_r=0. If all repairs work, the candidate contradicts G. Since the bound holds conditional on t and outside observations, and after fixing the small head, the new gate is at most min(p^(-2), sum_(r in closure) beta_r). The minimum can be taken over fixed source-axis and repair policies. Two trials may reach the same reader, so there is no product of trial failure probabilities. Dropped observations remain unread; the original noncollapsed-line loss factor still applies. The phase and the matching events in the published case-3 parity branch still determine the fourth-digit factor.

Every row that actually contributes is a common Wieferich prime above the inherited cutoff B=9*10^14. It is at least 2p²+1, already true at the first affected inert reader, and the order path increases. Counting potentially contributing inert integers in (L,q), L=max(B,2p²), bounds the gate by (q-L)/(4L)+1/L when q>L. For the original eight finite sources, this is below half the original gate whenever B<q<=B+B/p². This comparison is per terminal only. No aggregate decimal is revised without repricing the matching reciprocal-prime envelope, and no new scan or assumption about common exceptions is used.

At the real ordinary comparison p=71 with readers 50411 and 100823, the two source-axis trials can hit the very same older observation after repairing 50411 on base 5. Repairing instead on base 3 leaves that observation a unit on both trials. The checked example gives ordinary comparison geometry, not a genuine common exception.

```python
from math import isqrt, lcm

p,r,s,q = 71,50411,100823,715823
H = 3960

def S(z,m):
    return (pow(3,z[0],m)+pow(5,z[1],m))%m

def edit(z,w,i):
    return (z[0]+w,z[1]) if i==0 else (z[0],z[1]+w)

def exact(n,z,v,k):
    m=v**(k+1)
    return (n-S(z,m))%m in range(v**k,m,v**k)

def repair(n,z,v,U,i):
    m=v*v
    a=(3,5)[i]
    f=(pow(a,U,m)-1)//v
    k=((n-S(z,m))//v)*pow(pow(a,z[i],v)*f,-1,v)%v
    z=edit(z,k*U,i)
    if (n-S(z,v**3))%v**3==0:
        z=edit(z,v*U,i)
    assert exact(n,z,v,2)
    return z

for v in (p,r,s,q):
    assert v%4==3 and all(v%i for i in range(2,isqrt(v)+1))
    assert all(pow(a,v-1,v*v)!=1 for a in (3,5))
assert (r,s,q)==(10*p*p+1,2*r+1,2*p**3+1)
assert all(pow(b,10*p,r)!=1 and pow(b,2,s)!=1 for b in (3,5))

U=lcm(H,p**4*(p-1),q-1,r-1,2*s)
d=r*(r-1)
f=(pow(3,r-1,r*r)-1)//r
c=(r-1)*(((pow(5,d+U,r*r)-1)//r)*pow(f,-1,r)%r)
z=(c,d)
L=p*lcm(H,p-1,10,r*r,2*s*s)
assert L%(p*p) and pow(3,L,r*r)==pow(5,63*L,r*r)!=1
starts=[edit(z,L,0),edit(z,63*L,1)]
ends=[edit(x,U,1) for x in starts]
assert len({S(x,r*r) for x in ends})==len({S(x,s*s) for x in ends})==1

a=S(ends[0],r*r)
a=next(a+j*r*r for j in range(3)
       if all(a+j*r*r!=S(x,r**3) for x in ends))
n,M=0,1
for m,b in [(32,S(z,32)+1),(3,0),*[(h,S(z,h)+1) for h in (7,11,19,23)],
            (p**5,S(z,p**5)),(r**3,a),(s*s,S(ends[0],s*s)+s)]:
    n+=M*((b-n)*pow(M,-1,m)%m)
    M*=m
assert n==3212675318122972340498536406298976587315

for x,y in zip(starts,ends):
    assert exact(n,x,p,2) and exact(n,x,r,1) and (n-S(x,s))%s
    assert exact(n,y,p,2) and exact(n,y,r,2) and exact(n,y,s,1)
    assert (n-S(repair(n,x,r,U,0),s))%s
    V=lcm(H,p**4*(p-1),q-1,r*r*(r-1),s-1)
    final=repair(n,y,s,V,1)
    assert all(exact(n,final,v,2) for v in (p,r,s))
    assert S(final,q)==S(y,q)
    assert (n-S(final,32))%32==1 and (n-S(final,3))%3
    assert all((n-S(final,h))%h for h in (7,11,19,23))
print("Shared reader observation and both ordinary repair choices verified")

# Exact arithmetic on the original eight finite cube sources.
from fractions import Fraction
B=9*10**14
roots=[v for v in range(31,101,4) if all(v%i for i in range(2,isqrt(v)+1))]
assert len(roots)==8
for v in roots:
    lo=max(B,2*v*v)
    hi=B+B//(v*v)
    assert Fraction(hi-lo,4*lo)+Fraction(1,lo)<Fraction(1,2*v*v)
print("All eight near-cutoff half-gate inequalities verified")
```
