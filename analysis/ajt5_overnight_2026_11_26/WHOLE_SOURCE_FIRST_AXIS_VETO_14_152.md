# Whole-source first-axis exclusion for (14,152)

For a native root x of order 343, suppose a coarse menu's every permitted exponent E is r modulo 7. Then after a certified 7-free annihilator F of the axes' non-7 components, a first-axis necessary condition at each prime is 3^(49F)=x^(49rF). One verifies coverage before applying the phase test: 3^(2401F)=5^(2401F)=1 on the composite block suffices here. A composite gcd of 1 in the phase test witnesses exclusion on every covered prime; without coverage, the same gcd might exclude nothing on the uncovered factors.

For (14,152) the full reconstructed coarse menu is {(1,191),(1,240),(15,79),(15,128)} and the lifts are E=e+49j, so r=1. On the previously unresolved Q=1707542200628666649958800561642353, F=1036704944750048943625024830 gives complete coverage. The exact gcd ladder for 3 at 7,49,343,2401 is (1,19506836031383,19506836031383,Q). No factor can have exact first-axis order 343. On the full reduced source R, G=2621·846217·F verifies coverage and gives gcd(R,3^(49G)−x^(49G))=1. Thus the whole specified neutral chart source is vetoed; this is not a pointwise result for A303656.

The discovery used factorization to find the exponent, while the rejection verifier below does not need factor search for R or Q. Deleting either indicated large factor of F preserves the phase gcd 1 but destroys one side of coverage, a real warning against trusting the phase gcd alone. The replay also reconstructs the original resultant and menu and checks uniqueness of the native root prime by prime.

```python
from math import gcd, isqrt, prod
from sympy import symbols, resultant

def menu(target):
    out = set()
    for a in range(36,343,49):
        g,h = (pow(b,a+343*(-a%6),2401) for b in (3,5))
        inv = {pow(h,j,2401):j for j in range(343)}
        for u0,I,J in ((17,(33,12,47),(39,11,46)),
                       (24,(40,5,26),(46,4,25)),(38,(5,40,33),(11,39,32))):
            for u in range(u0,343,49):
                for v in range((1-u)%7,343,7):
                    w = inv[(pow(h,v,2401)+pow(g,u,2401)-pow(g,u+1,2401))%2401]
                    if v%49 in I or w%49 in J:
                        continue
                    for k in range(1,343):
                        if not k%7:
                            continue
                        P,Q = (0,k*v-u),(1,k*w-u)
                        b,c,d = min(((S[1-i]-S[i])*t%343,(T[1-j]-S[i])*t%343,d)
                            for S,T in ((P,Q),(Q,P)) for i in (0,1) for j in (0,1)
                            if (d:=(T[j]-S[i])%343)%7 for t in [pow(d,-1,343)])
                        if (b,c)==target:
                            out.add((pow(a*d,-1,343)%49,k))
    return out

from math import gcd, isqrt, prod

R=7794092988996359616004983264299816596361951171
Q=1707542200628666649958800561642353
x=13637500586108896670367803493377664812606052
fs=[2,3,3,5,132263,3062750177,28435621037]
F=prod(fs)
G=F*2621*846217
p=19506836031383

assert R%Q==0 and gcd(F*G,7)==1
assert pow(x,343,R)==1 and gcd(R,pow(x,49,R)-1)==1
assert (1-x+pow(x,14,R)-pow(x,152,R))%R==0
assert tuple(gcd(Q,pow(3,F*7**j,Q)-1) for j in (1,2,3,4))==(1,p,p,Q)

def phase(n,f):
    return gcd(n,pow(3,49*f,n)-pow(x,49*f,n))

for n,f in ((Q,F),(R,G)):
    assert pow(3,2401*f,n)==pow(5,2401*f,n)==1
    assert phase(n,f)==1

for ell in set(fs):
    assert all(ell%d for d in range(2,isqrt(ell)+1))
    assert pow(3,2401*(F//ell),Q)!=1

q=Q//p
assert p*q==Q and q==87535579726078465591
for ell,covered in ((28435621037,q),(3062750177,p)):
    f=F//ell
    assert gcd(Q,pow(3,2401*f,Q)-1)==covered
    assert phase(Q,f)==1

assert menu((14,152))=={(1,191),(1,240),(15,79),(15,128)}
t=symbols("t")
assert resultant(sum(t**i for i in range(0,343,49)),1-t+t**14-t**152,t)==7*R
for j in range(1,343):
    if j%7:
        y=pow(x,j,R)
        assert gcd(1-y+pow(y,14,R)-pow(y,152,R),R)==(R if j==1 else 1)
print("PASS")
```
