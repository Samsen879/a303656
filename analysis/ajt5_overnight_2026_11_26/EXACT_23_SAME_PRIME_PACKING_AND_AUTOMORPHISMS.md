# The exact finite same-prime packing is 23 in a real chart

At the same actual CRT target n, witness p=1259 has 83 exact-once chart hits. Using the precise short-step, noncollinearity, internal fourth-point and reduced denominator constraints in the replay, these hits form 111 distinct eligible start triples. The explicit 23 disjoint edges prove the attainable lower bound. The certificate gives 83 nonnegative integer weights with total 190, where each edge's sum is at least 8. A disjoint packing therefore has size ≤floor(190/8)=23. This is a complete finite optimum, sharper than the prior packing lower bound. It is not a uniform asymptotic packing result. In the central subchart the corresponding exact maxima are 3 and 4 (with and without the requirement that r divide reduced e), while the other actual witness 8807 provides no eligible central edge despite having four hits.

## Why the simplest same-target symmetries cannot replicate arbitrarily many seeds

Normalize each hit to (z,1−z) by dividing by actual nonzero n modulo p. A two-term Laurent-monomial transform with exponent rows (a,b),(c,d) in {−1,0,1}² and nonzero determinant has form (λ z^a(1−z)^b, μ z^c(1−z)^d). If it sends four distinct actual hit arguments back to the sum-one graph, clearing poles produces a polynomial of degree at most three. In detail choose u=max(0,−a,−c),v=max(0,−b,−d); the only way the degree could reach four requires rows (1,1),(−1,−1), excluded by the determinant. Thus the sum relation is an identity. The first rational component's fibers above 0,1,infinity are confined to those same three points, since it and one minus it are Laurent monomials. They are distinct and nonempty; after relabeling, the first component can only be a pure power. Its degree is at most two, prime to the chart characteristic, and the single preimage of 1 forces degree one. Hence the transform belongs to the six fractional linear permutations of 0,1,infinity. The independent quadratic-character check can reduce this to two in the mixed-sign graph. Original grid and exact denominator requirements may shrink it further.

The reduced affine denominator is not itself an invariant of returning to the sum graph. If the translated original spans are below D/e, the original bounded positive barycentric equation lifts uniquely from its congruence; beyond that threshold, the exact inversion controls below show a denominator cap failure (119→2108) and a loss of divisibility/internality (255→189). They preserve the same actual n and all four exact-once hits. This concerns the stated transform family and finite fixture, not unrestricted packing at growing height.

```python
from itertools import combinations, product
from math import gcd, isqrt

H,J,t,r,s,p,q = 3720000,310,155521,17,37,1259,8807
C,E = 3*t+80,t+144
assert all(all(a%d for d in range(2,isqrt(a)+1)) for a in (r,s,p,q))
M,P,L = 146651884329720,q*q,H//2-4
assert M%(p*p) == 0 and gcd(M,P) == 1 and M*P < 1<<(L-4)
assert max(2*(C+720*(J-1)),3*(E+720*(J-1))) < H-5

def coord(a,b,m):
    c = a+M*((b-a)*pow(M,-1,P)%P)
    return (pow(2,L,m)+(c-pow(2,L,M*P))%(M*P))%m

def target(m):
    u = coord(61827877807697,0,m)
    v = coord(135417323161960,39021647,m)
    return (pow(3,C,m)+pow(5,E,m)+85*(u*u+v*v))%m

def chart(a):
    D,Q = (a-1)//2,a*a
    assert a%4 == 3 and D%(r*s) == 0 and J < D
    for b in (3,5):
        assert pow(b,720*D,a) == 1
        assert all(pow(b,720*(D//d),a) != 1 for d in (7,r,s) if D%d == 0)
    X = [pow(3,C+720*i,Q) for i in range(J)]
    Y = [pow(5,E+720*j,Q) for j in range(J)]
    N = target(Q)
    hits = [(i,j) for i,j in product(range(J),repeat=2)
            if (N-X[i]-Y[j])%Q in range(a,Q,a)]
    return N,X,Y,hits

def sub(a,b): return a[0]-b[0],a[1]-b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]

def coeff(o,u,v,f):
    A,B,F = sub(u,o),sub(v,o),sub(f,o)
    e,m,l = det(A,B),det(F,B),det(A,F)
    if e < 0:
        e,m,l = -e,-m,-l
    g = gcd(e,gcd(m,l))
    return e//g,m//g,l//g

def edges(hits,central=False):
    I = [i for i,z in enumerate(hits)
         if not central or all(77 <= a < 233 for a in z)]
    strict,loose = set(),set()
    for T in combinations(I,3):
        o,u,v = (hits[i] for i in T)
        A,B = sub(u,o),sub(v,o)
        if not det(A,B) or det(A,B)%r:
            continue
        if not all(any(A[j]%h == B[j]%h == 0 and
                       max(0,A[j],B[j])-min(0,A[j],B[j]) <= 90*h
                       for h in range(2,15)) for j in (0,1)):
            continue
        for i in I:
            e,m,l = coeff(o,u,v,hits[i])
            if 0 < m and 0 < l and m+l < e <= 408:
                loose.add(T)
                if e%r == 0:
                    strict.add(T)
    return strict,loose

N,X,Y,hits = chart(p)
assert N == 1223507 and len(hits) == 83
G,_ = edges(hits)
assert len(G) == 111
w = list(map(int,"00130304601414404854440103500007041080012544414340433302010004040604400042050463043"))
assert len(w) == 83 and sum(w) == 190
assert all(sum(w[i] for i in T) >= 8 for T in G)
pack = [(0,23,31),(2,12,78),(3,75,76),(5,14,45),(6,19,61),(7,68,74),
        (8,55,62),(10,42,53),(11,22,48),(13,33,54),(15,72,77),
        (16,20,56),(17,28,71),(18,79,80),(21,35,44),(25,46,57),
        (26,51,64),(27,36,38),(29,65,73),(34,52,63),(39,67,82),
        (41,47,60),(50,59,81)]
assert set(pack) <= G and len({i for T in pack for i in T}) == 69
for S,k in zip(edges(hits,True),(3,4)):
    assert len(S) == k and len({i for T in S for i in T}) == 3*k
NN,XX,YY,other = chart(q)
assert NN == 54 and not edges(other,True)[1]
assert sum(all(77 <= a < 233 for a in z) for z in other) == 4
for a,n,xx,yy,signs in [(p,N,X,Y,(p-1,p-1)),(q,NN,XX,YY,(1,q-1))]:
    assert tuple(pow(n*b[0],(a-1)//2,a) for b in (xx,yy)) == signs

def inverse_image(z):
    i,j = z
    a = N*N*pow(X[i],-1,p)%p
    return (next(k for k,x in enumerate(X) if x%p == a),
            next(k for k,y in enumerate(Y) if y%p == (N-a)%p))

for row,before,after in [
    (((131,18),(97,120),(129,122),(125,50)),(119,20,17),(2108,349,391)),
    (((161,183),(97,120),(131,18),(155,167)),(255,15,19),(189,96,-167))]:
    out = tuple(map(inverse_image,row))
    assert set(row+out) <= set(hits)
    assert coeff(*row) == before and coeff(*out) == after
print("23 full, 3 central, 4 without the divisibility gate, 0 at 8807")
```
