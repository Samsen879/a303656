# One activated ancestor can serve two independent repair cuts

If one inert row q alone blocks a full repair line at lower prime t, it must read one variable digit on each axis, have equal nontrivial characters along the line, and have n=0 modulo q. Let the failing anchor be (c_t,d_t), with slope/intercept y=m x+b and b!=0 modulo t. Then its anchor ratio chi=-3^c_t/5^d_t modulo q equals beta^b for beta=5^L_5 of exact order t. It therefore has order t. If the same q serves distinct primes p,r, the two anchor ratios have quotient of exact order pr, and both order graphs at q are divisible by pr. Since each ratio has odd order, (3/q)^c_t (5/q)^d_t=-1 at an inert q.

In a common repaired block, assume the q-primary coordinate is frozen so that the moving characters have exact prime-to-q torsion at full precision q^E (not just modulo q). Their agreement modulo q then lifts by injectivity on that torsion. Independent p- and r-steps yield an ancestor residual n−S T modulo q^E, with S the sum of the center powers and T ranging over the roots of unity of order dividing pr. Unequal truncated valuations of n and S fix the residual at the smaller valuation. If both have the same odd valuation k<E, at most one T can make it rise: its reduction is forced by (n/q^k)/(S/q^k). Either separate line may miss that joint point, so independent line tests do not imply a blocked combined block.

At n=262347356419, the actual row 4523 blocks both native cuts at 7 and 19 on the displayed square-precision block, including all 133 simultaneous repairs. A shift at the same target preserves both lower grids and all ancestor collision positions modulo 4523, and keeps both displayed separate cuts blocked, yet opens a unique point in the combined block at full precision. The original unrestricted panel already passes at (1,0). The fixture is not a finite all-exponent obstruction; the small-c and ordinary-height issues remain separate.

```python
from itertools import product
from math import lcm

p,r,q = 7,19,4523
n,d = 262347356419,182219245
B = lcm(18,34*q)
L,K = B*r,B*p

def order(a,t):
    return next(j for j in range(1,t) if pow(a,j,t)==1)

assert [[order(a,t) for a in (3,5)] for t in (p,r,q)] == [
    [6,6], [18,9], [2261,4522]]
assert pow(3,L,q*q)==pow(5,5*L,q*q)
assert pow(3,K,q*q)==pow(5,11*K,q*q)

def residual(c,d,t):
    m=t*t
    return (n-pow(3,c,m)-pow(5,d,m))%m

for start,wanted in ((1,set()),(54576019,{(1,5,1,11)})):
    holes=set()
    for x,y,u,v in product(range(p),range(p),range(r),range(r)):
        c,e=start+L*x+K*u,d+L*y+K*v
        a,b,s=[residual(c,e,t) for t in (p,r,q)]
        P,R=y==5*x%p,v==11*u%r
        assert (a==0,b==0,s%q==0)==(P,R,P and R)
        assert a%p==b%r==0
        if P and R:
            if x==0 or u==0:
                assert s!=0
            if s==0:
                holes.add((x,y,u,v))
    assert holes==wanted
assert all(residual(1,0,t)%t for t in (p,r,q))
print("PASS")

# Independently verify full-precision torsion required for joint character transport.
for step,t in ((L,p),(K,r)):
    for a in (3,5):
        assert pow(a,step*t,q*q)==1 and pow(a,step,q)!=1
M=p*p*r*r*q*q
assert (n-pow(3,90561007,M)-pow(5,420273781,M))%M==0
print("Exact joint torsion and full-modulus escape independently checked")
```
