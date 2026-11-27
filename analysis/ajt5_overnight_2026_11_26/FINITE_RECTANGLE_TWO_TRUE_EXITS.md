# Blocking an arbitrary finite exponent rectangle while retaining two true exits

Fix finite C,D. Choose unequal H1=3^C'+1 and H2=1+5^D' larger than every root h=3^c+5^d with c≤C,d≤D. For each distinct h choose a new inert prime p>5 not dividing (h−H1)(h−H2)(H1−H2), and require n≡h+p mod p². With M the product of p², CRT gives the class. Every low root is blocked at its assigned prime when active.

To preserve both exits in that same class, at each p² represent n−H1 and n−H2 by two squares locally. Both are units; their mod-p solutions exist by the pigeonhole intersection of two sets of squares of size (p+1)/2, and a unit coordinate permits lifting. Take the difference of the two local coordinate vectors, and choose common integer representatives a,b for that difference by CRT. They are not both zero mod any p|M because the two norms differ by a unit. Choose a nonzero odd representative a, then take b odd and congruent to 1 at prime factors of a not dividing M to arrange gcd(a,b)=1. If (u,v) is the second local coordinate vector combined by CRT, then
```
a*u+b*v = (H2−H1−a²−b²)/2 mod M .
```
The right-hand side is an integer (both H values and both a,b have the required parity). Bézout corrects u,v by multiples of M to make this exact. Replace (u,v) by (u+bMt,v−aMt) to get unbounded true representations n=H2+u²+v²=H1+(u+a)²+(v+b)² in the same class, with every low candidate strictly active for large t.

When C=D=K and the high powers are the first beyond the low root bound, each excluded prime product has O(K+1) prime factors. The prime number theorem in progressions provides enough distinct odd inert primes of polynomial size in K; hence log M=O(K² log(K+2)). The bounded CRT and Bézout representatives for a,b,u,v can all be chosen polynomial in M and H1,H2, and t can be chosen polynomially bounded to activate the low roots. This yields examples with log n=O(K² log(K+2)). In particular a common cap o(sqrt(log n/log log n)) cannot guarantee representations at every integer. This does not rule out any proportional power box on unbounded n.

Concrete two-norm family extending the strict-box countercontrol at 3920:

```python
from math import prod
P=(3,7,11,19,23,31,67,823,919,967,1283,1583,1607,1907)
M=3**6*prod(p*p for p in P if p!=3)
def v(n,p):
    j=0
    while n%p==0: n//=p; j+=1
    return j
for c in range(7):
    for d in range(5):
        R=3920-3**c-5**d
        assert any(v(R,p)%2 and v(R,p)<v(M,p) for p in P)
for t in (0,1,3,999):
    s,w=9*M*t,-11*M*t
    n=3126+(13+s)**2+(25+w)**2
    assert n==2188+(24+s)**2+(34+w)**2
    assert n%M==3920%M
```

No assertion about the original conjecture's possible exceptions follows from these fixed-rectangle constructions.
