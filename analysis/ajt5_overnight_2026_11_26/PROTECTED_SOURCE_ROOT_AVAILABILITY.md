# Protected retained repairs can supply distinct source roots

On the fixed-head D=r prime-source branch retain the original small-head observations and remove the source and older r-readers from both axes. Choose a retained anchor without looking at the removed observations or the terminal. Mark the remaining inert rows in decreasing order: p is marked if one ordinary axis has p not dividing its source order at r, and every larger retained reader of that axis's p-primary coordinate is already marked. If the phase domain has additional fixed periods, the chosen repair axes must also preserve those periods.

On an axis where a source-order digit ell^a is not fixed by the head, suppose ell is split or its own test is already protected, and all retained readers of that level are marked. Changing just that digit changes the source root modulo r. Repair the affected rows in increasing order on their marked axes. The two ordinary primary digits make a rooted residual have exact valuation two, while each axis preserves its contribution at r, preserves earlier rows, and only reaches marked rows later. Raising the local precision at a distinct prime adds only factors of that prime to its order. Thus the two roots can be retained without consulting n_r or the dropped observations. If a largest prime power in the source orders is free and its own test is protected, all its reached rows are larger than it; source-order preservation is automatic for those repairs. The earlier factorial comparison applies to the subfamily with both roots available. Quantifying the actual weight of this subfamily is a separate task.

The replay checks a real 59-to-2243 prefix where changing the split 29-digit requires exactly one retained repair at 523, giving different roots 50 and 22. It also checks the countercontrol at 683-to-1367: the free 31-digit is read by retained row 31, and both its repair axes read back into the source. The fixed head (8,55) is forced to the single root zero, while the alternate legal head (16,55) at the same n gives two roots. Both terminals are ordinary controls. This does not remove a finite charge or change the density bound.

```python
from math import isqrt, lcm

H = 3960
def prime(p): return p > 1 and all(p%j for j in range(2,isqrt(p)+1))
def order(b,p): return next(k for k in range(1,p) if pow(b,k,p)==1)
def fast(b,p): return pow(b,p-1,p*p)!=1
def S(c,d,m): return (pow(3,c,m)+pow(5,d,m))%m

def strip(M,p):
    while M%p==0:
        M //= p
    return M

def panel(r,q,orders):
    assert all(prime(p) and p%4==3 and all(fast(b,p) for b in (3,5))
               for p in (r,q))
    assert [order(b,p) for p in (r,q) for b in (3,5)]==orders
    old = [p for p in range(31,q,4) if p!=r and prime(p)]
    P = [p for p in old if (p-1)%r or
         all(pow(b,(p-1)//r,p)==1 for b in (3,5))]
    assert all(fast(3,p) for p in P)
    return P,set(old)-set(P),lcm(H,r-1,*(p*p*(p-1) for p in P))

def complete(n,c,d,M,P):
    assert (n-S(c,d,32))%4==1 and (n-pow(5,d,3))%3
    assert all((n-S(c,d,p))%p for p in (7,11,19,23))
    moved = []
    for p in P:
        m,T = p**3,strip(M,p)
        z = (n-S(c,d,m))%m
        if z%p==0:
            old = c
            f = ((pow(3,T,p*p)-1)//p)*pow(3,c,p)%p
            c += T*(z//p*pow(f,-1,p)%p)
            if (n-S(c,d,m))%m==0:
                c += T*p
            if c!=old:
                moved.append(p)
    for p in P:
        z = (n-S(c,d,p**3))%p**3
        assert z%p or (z and z%(p*p)==0)
    return c,moved

r,q,c,d,n0 = 59,2243,23,8817,1772213347634616708129
P,drop,M = panel(r,q,[29,29,19*r,38*r])
assert drop=={827,1063} and 523 in P and order(3,523)==58
assert prime(29) and 29%4==1 and H%29
L = strip(M,29)
L *= pow(L,-1,29)
F = lcm(32,3,7,11,19,23,r**3,q*q,*(p**3 for p in drop))
n = n0+F*((S(c+L,d,523**2)+523-n0)*pow(F,-1,523**2)%523**2)
a,x = complete(n,c,d,M,P)
b,y = complete(n,c+L,d,M,P)
assert a%H==b%H==c%H and x==[] and y==[523]
assert (S(a,d,r),S(b,d,r))==(50,22)

r,q,n,c,d = 683,1367,3060176961871,8,55
P,drop,M = panel(r,q,[31,22*31,r,2*r])
assert not drop and 31 in P and H%31 and H%22==H%30==0
assert (n%3,n%32,n%31**2)==(1,15,25)
assert len({S(c+H*i,d,r) for i in range(31)})==31
for i in range(31):
    a = c+H*i
    hits = [j for j in range(31) if (n-S(a,d+H*j,31**2))%31**2==0]
    assert (n-S(a,d,31))%31==0 and hits==[(14+20*i)%31]
    assert S(a,d+H*hits[0],r)==0
assert S(complete(n,c,d,M,P)[0],d,r)==0
a = complete(n,16,d,M,P)[0]
b = complete(n,16+strip(M,31),d,M,P)[0]
assert (S(a,d,r),S(b,d,r))==(542,287)
print("Active repair verified, singleton forced, alternate head split")

# Verify exactly why the two fixtures permit or prevent protected repairs.
assert order(3,59)==order(5,59)==29
assert order(3,523)==58 and 523%29!=0
assert all(order(a,683)%31==0 for a in (3,5))
print("Reader/source-order dependencies independently checked")
```
