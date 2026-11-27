# Two retained heads with distinct source roots

In a doubly ordinary prime-source case r>23, suppose the terminal q sees exactly one r-digit on each axis, and two anchors pass the same retained observations before n_r, the dropped older r-readers, or n_q are observed. The anchors must belong to the phase domain being charged. If their source shifts 3^c+5^d modulo r are different, every n_r has at least one unit anchor. On that anchor the full r-by-r digit grid preserves the source unit. Each dropped reader can reject at most r cells, because it is injective along a read axis with the other fixed; the terminal has fibers of size at most r for the same reason. To first block it must leave at most r cells. Dividing the rejection counts by r gives counts at most one and expected sum at most rS, where S sums the dropped reader weights. The distinct-reader argument bounds this by min(1,(rS)^(r−1)/(r−1)!), before the terminal factor. No independence between the two anchors is used.

For a rooted anchor, put A=3^c and B=5^d modulo r and use absolute r-digits. Writing the two terminal characters as g=h^mu with prime-to-r coefficients C,D, a constant terminal line requires C=-D and A/B=-mu alpha_5/alpha_3, with alpha_a the ordinary source lift coefficients. Then the repair slope matches mu and the intercept is forced to zero, so its alignment is the single reading [A]+[B] modulo r², with Teichmuller lifts. For nonempty alignments their readings differ exactly when their roots differ: the required ratio is the same, and if it is -1 the lifts sum to zero. At a given source reading one chooses the smaller applicable charge: unit-grid factorial, rooted nonconstant distinct-reader charge plus constant older alignments, or one for a rooted constant line. The terminal factor comes after the older-reader tests. Distinct head labels alone do not imply distinct roots.

At the fixed actual 59-to-2243 target, two legal heads have the same root 50 and alignment reading 1407. Another retained extension of the second head has root 33 and alignment reading 1272. Replaying the full retained prefix and both dropped readers gives the same-alignment and root-split controls; 58 unit choices in the third displayed row survive the old reads and terminal. The terminal is ordinary in this example. General access to two such anchors in the original charged domain is not proved, so no finite ledger charge is removed.

```python
from math import isqrt, lcm

r,q,n,H = 59,2243,1772213347634616708129,3960

def prime(p):
    return p > 1 and all(p%j for j in range(2,isqrt(p)+1))

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

assert all(prime(p) and p%4==3 for p in (r,q))
assert [next(k for k in range(1,p) if pow(b,k,p)==1)
        for p in (r,q) for b in (3,5)] == [29,29,19*r,38*r]
assert all(pow(b,p-1,p*p)!=1 for p in (r,q) for b in (3,5))
assert (n%3,n%32,n%(r*r),n%(q*q)) == (0,1,1407,q)

old = [p for p in range(31,q,4) if p!=r and prime(p)]
drop = {p for p in old if (p-1)%r==0
        and any(pow(b,(p-1)//r,p)!=1 for b in (3,5))}
assert drop == {827,1063}
keep = [p for p in old if p not in drop]

def complete(c,d):
    assert c%2 == d%2 == 1 and (n-S(c,d,32))%32 == 17
    assert (n-pow(5,d,3))%3
    assert all((n-S(c,d,p))%p for p in (7,11,19,23))
    V = lcm(H,29,38)
    c += V*(-c*pow(V,-1,q)%q)
    d += V*(-d*pow(V,-1,q)%q)
    T = V*q
    for p in keep:
        L = lcm(T,p-1)
        z = (n-S(c,d,p*p))%(p*p)
        if z%p==0:
            slope = ((pow(3,L,p*p)-1)//p)*pow(3,c,p)%p
            c += L*(z//p*pow(slope,-1,p)%p)
            if (n-S(c,d,p**3))%p**3==0:
                c += L*p
        z = (n-S(c,d,p**3))%p**3
        assert z%p or (z and z%(p*p)==0)
        T = lcm(T,(p-1)*p*p)
        while T%r==0:
            T //= r
    assert all(pow(b,T,p**3)==1 for p in keep for b in (3,5))
    return c,d,T

seeds = [(23,8817),(8839,8817),(8839+75240,8817+18*75240)]
for seed,loc,root in zip(seeds,(1407,1407,1272),(50,50,33)):
    c,d,T = complete(*seed)
    assert (c%H,d%H)==tuple(e%H for e in seed)
    assert c%q==d%q==0 and T%r and S(c,d,r)==root
    for i in range(r):
        a = c+T*i
        j, = [j for j in range(r) if S(a,d+T*j,r*r)==loc]
        b = d+T*j
        assert S(a,b,q*q)==0
        if loc==1407:
            if (n-S(a,b,r**3))%r**3==0:
                b += T*r
            z = (n-S(a,b,r**3))%r**3
            assert z and z%(r*r)==0
            assert (n-S(a,b,q*q))%(q*q)==q
            assert all((n-S(a,b,p))%p for p in drop)

assert (n-S(c,d,r))%r==17
assert sum(all((n-S(c+T*i,d,p))%p for p in drop|{q})
           for i in range(r))==58
print("shared 1407, split 1272, and 58 surviving unit choices")
```
