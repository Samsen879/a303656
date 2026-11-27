# Cross-digit budget for a deeper reader

Fix an ordinary source p, a rooted two-axis chart with both source bases ordinary, the old head, and the prime-to-p exponent coordinates. At an older reader r let the greatest p-order depth be d>=2. Fix two distinct prefixes a,b modulo p^(d-1) of the free source coordinate. Let T_a,T_b be the actual surviving sets of next digits; the argument does not restore a blocked digit.

Subtracting source equations and applying LTE to both bases shows that the compensated digit difference has the same valuation as the free digit difference. Within either block varying digit d produces the same nonzero affine response slope on the other axis, from the linearized source congruence modulo p^(d+1) with the head fixed. Thus the reader shifts have form f_i(u)=A_i xi^u+B_i eta^u with shared p-th roots xi,eta. At least one root is nontrivial, by depth d. For v=u+j and xi!=eta, equality is equivalent to (A_a-A_b xi^j)(xi/eta)^u=-(B_a-B_b eta^j). Both coefficients cannot vanish: on an axis of depth d the coefficient ratio between these prefixes has order exceeding p. Hence at most one pair lies on each of the p diagonals. If xi=eta, put C_i=A_i+B_i. For both C_i nonzero, at most one diagonal occurs, and its count is |T_a intersection (T_b-j)|. One zero coefficient gives no pairs; both zero gives |T_a||T_b| pairs. Summing the exact counts of multiple readers yields a sufficient pair-separation criterion if the sum is strictly below |T_a||T_b|. A shallow collision cannot be undone at this depth.

For q=2p^3+1 inert, no older inert reader has depth three and at most (p-1)/2 can have depth two: they are 2kp²+1 for odd k<p. On first-digit pairs with full second-digit freedom, avoid double-zero pairs and then the remaining depth-two readers together cost at most p(p-1)/2<p². This is only a conditional separation criterion for that cube subfamily. Access to full blocks, whole-chart collapse, and shared shallow failures still require separate treatment before changing any unconditional bound.

At p=71 and q=715823, the two collapsed lower coordinates are 0 and 1041. At first digits 0 and 17, the allowed second-digit sets have 70 and 71 entries, respectively. Reader 50411 identifies exactly one allowed pair (19,70), and the replay gives a CRT target rejecting both. The alternative second digits (1,0) give two reader units on the same target and preserve both noncollapsed terminal lines. The separate pair of first digits (6,21) collides at shallow reader 1279 regardless of second digits. All conclusions are local; no density claim changes.

```python
from math import isqrt, lcm, prod

p, q, s, r = 71, 715823, 1279, 50411
n, c, d = 2420068764704544, 10082, 45369
H = 3960
L = lcm(H, p-1, 18, 10, r, s)

def S(pt, m):
    a, b = pt
    return (pow(3, a, m) + pow(5, b, m)) % m

def point(x, h, even=False):
    P = p**h
    a, b = c+L*((x-c)*pow(L, -1, P) % P), d
    for i in range(h):
        u, m = L*p**i, p**(i+2)
        b += u*next(j for j in range(p) if S((a,b+u*j),m) == n%m)
    if even:
        m = p**(h+2)
        if n%m == S((a,b),m):
            b += L*P
        assert (n-S((a,b),m))%m in range(p**(h+1),m,p**(h+1))
    assert (a-c)%H == (b-d)%H == 0
    return a,b

for v in (p,q,s,r):
    assert v%4 == 3 and all(v%i for i in range(2,isqrt(v)+1))
    assert all(pow(b,v-1,v*v) != 1 for b in (3,5))
assert q == 2*p**3+1 and r == 10*p*p+1 and s == 18*p+1
for v in (q,r):
    assert all(pow(b,(v-1)//p,v) != 1 for b in (3,5))
assert pow(3,L*p,r) == pow(5,63*L*p,r) != 1
f,g = [(pow(b,p-1,p*p)-1)//p for b in (3,5)]
assert -pow(3,c,p)*f*pow(pow(5,d,p)*g,-1,p)%p == 41
assert (n-pow(5,d,3))%3

P, M = p**3, p**4
assert pow(pow(5,2*pow(2,-1,P),q),321174,q) == 3
U,V = [pow(b,(p-1)*pow(p-1,-1,P),M) for b in (3,5)]
W = pow(V,321174,M)
A,B = [pow(b,e*P*pow(P,-1,p-1),M) for b,e in ((3,c),(5,d))]
assert [x for x in range(p*p)
        if (A*pow(U,x,M)+B*pow(W,x,M))%M == n%M] == [0,1041]

def block(a,m):
    return [S(point(a+p*u,2),m) for u in range(p)]

A,B = block(0,r),block(17,r)
assert [(u,v,A[u]) for u in range(1,p) for v in range(p)
        if A[u] == B[v]] == [(19,70,13184)]
assert set(block(6,s)+block(21,s)) == {96}
assert (block(0,s)[0],block(17,s)[0]) == (603,144)

M = 32*3*prod((7,11,19,23))*p**5*q*q*s*s
N = n+M*((13184-n)*pow(M,-1,r*r) % (r*r))
for a,u,size in ((0,0,1),(0,19,p),(17,70,p),(0,1,p),(17,0,p)):
    pts = [point(a+p*u+p*p*j,3,True) for j in range(p)]
    assert len({S(z,q) for z in pts}) == size
    assert len({S(z,r*r) for z in pts}) == 1
    assert all((N-S(z,32))%32 == 18 and (N-S(z,s))%s
               and all((N-S(z,t))%t for t in (7,11,19,23)) for z in pts)
    if (a,u) in ((0,19),(17,70)):
        assert all((N-S(z,r*r))%(r*r) in range(r,r*r,r) for z in pts)
    if (a,u) in ((0,1),(17,0)):
        assert all((N-S(z,r))%r for z in pts)
assert (A[1],B[0]) == (4533,44461)
print("depth-two collision, blocked digit, and same-target replacement verified")

# Independent cross-pair count by intersection of observed reader fibers.
from collections import Counter
U,V=Counter(A[1:]),Counter(B)
assert sum(m*V[y] for y,m in U.items())==1
W=Counter(A)
assert sum(m*V[y] for y,m in W.items()) in (1,2)
print("Filtered reader-fiber intersection independently verified")
```
