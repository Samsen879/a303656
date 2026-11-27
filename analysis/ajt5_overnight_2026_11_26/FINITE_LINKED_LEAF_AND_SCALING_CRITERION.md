# Finite leaves and coordinate-scale linked traces are different models

Let X=5^U, B=floor(sqrt(X)), and let one actual half have full odd split-only modulus D<B². For q a prime power define lambda(q) as the minimum positive odd l satisfying q|3l²+1. In the **fixed actual trace** model, where every prime power of D must be carried at full precision by a leaf and each leaf has l≤B, a finite leaf cover exists iff lambda(q)≤B for each exact prime power q||D. When it exists, at most three leaves suffice.

Necessity is immediate from each carried power. If some q>B it is unique; take its good leaf and one more for D/q<B. Otherwise greedily merge pairs whose product is ≤B. Four remaining leaves would give two disjoint pairs with product >B, contradicting D<B². Each odd split-only product at most B has a positive odd root representative smaller than its modulus, using one of two opposite nonzero roots. This is an exact criterion once the prime-power factors are known; it says nothing about when the largest factor on an arbitrary ray meets it.

For a cubic step A,S to A³,S³ (A=5^u, S=3^v), the new factors are Λ=A²±AS+S² and (2A±S)²+3S²=4Λ. For every split power q|Λ, any valid l must have q|3Sl−(2A±S) or q|3Sl+(2A±S). The split factor is coprime to 3S, and the two opposite roots modulo q exhaust the possibilities by Hensel uniqueness. The first expression cannot be zero as an integer because S does not divide 2A; the second is positive. Hence l≤B forces q≤3SB+2A±S. On the existing 266/9 ray, an entire shell with its coherent original side must divide a **single** such expression and forces l≥A²/(6S) for large A. Since S≤A^(23/133), the ratio to next-layer sqrt(A³) grows at least as A^(87/266)/6. This does not exclude a split into mixed orientations and leaves.

The exact (3,1) cubic-ray controls hit true shell primes 15259 and 3814750000729, whose minimal fixed-trace l are respectively 13591 at (9,3) and 2637358073421 at (27,9); the latter exceeds 966 times that layer's coordinate scale. No count of additional fixed-trace leaves fixes these finite budget failures. At ten times the coordinate bound, the smaller fixture has the exact separate leaves given below.

## Allow the physical traces themselves to scale

If D=a²+3b² is primitive, odd and split-only, set u=|a−3b| and v=|a+b|. Both are positive odd numbers, since a,b have opposite parity; they satisfy u²+3v²=4D and are units modulo D. In each of the two linked tests scale its fixed odd trace pair (t_i,s_i) to (u t_i,u s_i) and set the physical weight to t_i s_i v. The input to the original linked cubics becomes ρ=v r/u, so r=u/v makes ρ=1. All physical traces and weights are O(sqrt(D)). This re-encodes a known primitive norm, not a way to find one for an arbitrary half. It gives one leaf per known genuine half on the existing 266/9 ray, with **variable actual traces**; it does not contradict the fixed-trace obstruction. The real shell control below checks both tests pass with (u,v)=(119,125), and both fail when only v is changed to 123.

```python
from math import gcd,isqrt,prod

def N(a,b):
    return a*a+3*b*b

def F(q,z):
    t,s=2*q*q-1,2*q**3-1
    return 2*(1+s*z)**2-(1+t*z)**3

def certify_prime(p,a,fs):
    assert prod(q**e for q,e in fs)==p-1
    assert all(all(q%d for d in range(2,isqrt(q)+1)) for q,e in fs)
    assert pow(a,p-1,p)==1
    assert all(gcd(pow(a,(p-1)//q,p)-1,p)==1 for q,e in fs)

def odd_min(A,S,sign,p):
    assert p==A*A+sign*A*S+S*S
    r=(2*A+sign*S)*pow(3*S,-1,p)%p
    return min(t if t%2 else t+p for t in (r,p-r))

p,q=15259,3814750000729
certify_prime(p,2,[(2,1),(3,1),(2543,1)])
certify_prime(q,7,[(2,3),(3,3),(43,1),(379,1),(1083689,1)])
assert N(7,2)==(5**3-3)//2 and (5**3+3)//8==16
assert odd_min(125,3,-1,p)==13591>isqrt(5**9)
assert odd_min(5**9,3**3,1,q)==2637358073421
assert 2637358073421**2>966**2*5**27
assert N(43,570)==(5**9-3**3)//2==427*2287
assert (5**9+3**3)//8==16*N(64,61)==16*p
assert ((5**27-3**9)//2)%q==0

for D,l in ((427,235),(2287,2061),(p,13591)):
    assert l%2 and l<=10*isqrt(5**9) and (3*l*l+1)%D==0

u,v=119,125
assert N(u,v)==4*p and gcd(u*v,p)==1
r=u*pow(v,-1,p)%p
assert [F(t,v*r*pow(u,-1,p))%p for t in (6,21)]==[0,0]
assert [F(t,(v-2)*r*pow(u,-1,p))%p for t in (6,21)]==[3082,2967]
print("PASS")
```
