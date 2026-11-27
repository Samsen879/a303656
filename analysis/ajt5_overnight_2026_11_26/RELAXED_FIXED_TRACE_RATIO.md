# A fixed trace ratio after relaxing the sign and parity model

For the local trace cubic, write A=2τ²−1, B=2τ³−1, and Q(X)=2X²+4X+3. Direct multiplication gives
```
A X³ − B X² + τ³ − τ² =
(X−τ) [(2τ²−1)X² + (1−τ)X + τ(1−τ)].
(1−X³)² − (1−X²)³ = X² (X−1)² Q(X).
```
A one-sided usable root requires the trace denominators to be units and the second expression to be nonzero modulo the split prime. The selected root τ therefore has at most nine bad values at each split prime, counting multiplicities by degrees of τ(τ−1)(2τ²−1)(2τ³−1)Q(τ). Its selection and uniqueness among usable roots are distinct requirements.

At τ=3/4 the bracket in the cubic is precisely Q(X)/16. The trace pair after primitive scaling is (4,−5). For every split prime p≡1 mod 3 other than 19 the denominators are units and E(3/4)=513/2048≠0 mod p. Thus τ is the unique one-sided branch: any other root reduces to a root of Q, hence is never one-sided. Because the two factors are coprime at τ modulo p, the unique branch stays τ modulo every p^e. At 19, Q(τ)=0 modulo p, and the actual half (5^133+3^37)/8 has valuation one there; the replay directly exhibits the two-sided failure. τ=3 is usable and unique at 19 modulo p in the same branch test. Importantly, (4,−5) violates the original positive odd trace model. This certificate does not construct positive global coordinates with the relaxed trace pair.

For the original model the exact finite height search over reduced τ=a/b>0 with b odd and jointly positive traces after sign normalization gives:
- Complete true half (5^9−3^9)/2, all three split primes: minimum height 3, reached by 3 and 2/3.
- Actual (5^229−3^149)/2, selected block 7·67²: minimum height 4, reached by 4/3, vs the previously known height-18 repair.
- Same half, enlarged selected block 7·67²·23827: minimum height 5, reached by 1/5 and 2/5. The supported full-precision witness for 1/5 is exact, but one norm-capped leaf still cannot carry all three primes at B=31000. The full half remains unresolved.

## Exact replay

```python
from math import gcd

def delta(x):
    return (x-1)*(8*x**3-3*x-1)

def branches(a,b,p):
    if b%p==0:
        return []
    t=a*pow(b,-1,p)%p
    A,B=2*t*t-1,2*t**3-1
    if A*B*(A-B)%p==0:
        return []
    return [x for x in range(1,p)
            if (A*x**3-B*x*x+t**3-t*t)%p==0
            and ((1-x**3)**2-(1-x*x)**3)%p!=0]

def good(a,b,p):
    return b%p!=0 and branches(a,b,p)==[a*pow(b,-1,p)%p]

def minimum(P):
    for h in range(2,7):
        out=[]
        for b in range(1,h+1,2):
            for a in range(1,h+1):
                t,s=b*(2*a*a-b*b),2*a**3-b**3
                if max(a,b)==h and gcd(a,b)==1 and t*s>0:
                    if all(good(a,b,p) for p in P):
                        out.append((a,b))
        if out:
            return h,out

assert minimum((7,109,181))==(3,[(3,1),(2,3)])
assert minimum((7,67))==(4,[(4,3)])
assert minimum((7,67,23827))==(5,[(1,5),(2,5)])
assert branches(3,4,19)==[] and branches(3,4,67)==[51]
assert branches(2,3,67)==[18,23,52] and not good(1,7,7)
for p,g in [(7,3),(13,3),(19,9),(67,39),(109,54),(181,81),(23827,11838)]:
    assert sum(pow(delta(x),(p-1)//2,p)==p-1 for x in range(p))==g

def check(D,r,t,s,k,other):
    assert (r*r+3)%D==0 and gcd(2*t*s,D)==1
    diff=[]
    for z in (r,-r):
        u=(t+k*z)*pow(2*t,-1,D)%D
        v=(s+k*z)*pow(2*s,-1,D)%D
        diff.append((u*u-v**3)%D)
    assert diff==[0,other]

H0=(5**9-3**9)//2
assert H0==863**2+3*272**2==7**2*109*181
r=863*pow(272,-1,H0)%H0
check(H0,r,3,11,690159,53044)
check(H0,r,4,-5,583617,754779)
assert gcd(53044,H0)==gcd(754779,H0)==1

H=(5**229-3**149)//2
D=7*67**2*23827
assert H%D==0 and gcd(D,H//D)==1
assert 13**2+3*10**2==469 and 8**2+3*89**2==23827
assert 469*23827==11174863>31000
check(31423,16557,69,101,6977,23839)
check(D,378852245,115,123,513935575,708608612)
assert gcd(708608612,D)==1

assert ((5**133+3**37)//8)%19**2==38
check(19,4,4,-5,4,0)
print("PASS")
assert good(3,1,19)
```
