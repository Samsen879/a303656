# Three-hit monomial orbits: bounded components and a charged exceptional part

Fix actual n and p=3 mod 4 where both normalized terms z,1−z are nonsquares. Allow the bounded Laurent monomial transforms with exponent rows in {−1,0,1}² and nonzero determinant, and paths of such transforms between unordered triples. In the relaxed orbit graph there are at most 36 triples in an ordinary component; exceptional components account for at most 1596 triples per p.

Clearing Laurent denominators gives degree at most three. For a nonidentity relation with three distinct roots, the degree-three exponent pairs, up to swapping source or output axes, are (1/[z(1−z)],z), (1/z,z(1−z)), and ((1−z)/z,z(1−z)). This list follows by the finite row-pair degree test. The first forces the product of (1−z_i) to equal the negative product of z_i, impossible for three nonsquare pairs; the third forces the ratio of its two nonsquare output coefficients to equal the nonsquare product v. The middle gives an additional map only on triples of sum one: R(z_i)=(v/u)/z_i with u,v the second and third symmetric functions. It maps (u,v) to (v/u²,v²/u³) and is an involution preserving u/v. The identically vanishing relations are the previous six Möbius transforms.

The Möbius moves between sum-one triples occur only on A:u=2v, B:v=−1, C:u=1+2v, computed by summing the respective inverses. They join A to B, or act within C by involution. R preserves A. There are at most two line-intersection states and at most 12 further states where R takes B or C back into B or C; the latter solve respectively u³=−1, u³+u+2=0, v²+(1+2v)³=0, or (1+2v)³=v. Deleting these ≤14 states leaves ordinary components with at most six sum-one states; an exceptional state has at most three adjacent sum-one moves. Hence the total number of attached sum-one states is ≤14+3·14·6=266. Multiply by the at most six Möbius images per state for the displayed bounds. Genuine chart and denominator constraints only delete moves and states.

For the balanced long-step domain the exceptional part has log-prime weight O_ε(R^(2+ε)). Indeed the exceptional state equations and T³−T²+uT−v give a finite characteristic-zero set of seeds. Their bounded-length admissible orbit words give a fixed nonzero integer polynomial F containing all occurring pairwise phase ratios, outside finitely many bad primes. This follows by adjoining the algebraic roots, clearing denominators, and reducing the finite list. Each exceptional genuine triple has a horizontal span d between constants times sqrt(R) and R, because normalized determinant is a nonzero multiple of r≈R and normalized coefficients are O(sqrt(r)). Its prime divides F((3^720)^d). The sum of log heights over those d is O(R²); per prime there are at most 1596 exceptional triples, and the actual step parametrization introduces only O_ε(R^ε) divisor choices. The finitely many fixed bad primes do not have the required growing order. This does not bound the ordinary orbit count and gives no global pointwise middle.

The exact same-target replay gives 23 disjoint genuine four-hit packing seeds in distinct ordinary orbits, and a separate true three-hit pair connected by R but not by any of the six Möbius maps. The latter is not claimed to be a four-hit pair.

```python
from math import gcd

p,q,t,J,r,H = 1259,8807,155521,310,17,3720000
P,Q = p*p,q*q
M,L = 146651884329720,H//2-4
C,E = 3*t+80,t+144

def coord(a,b):
    c = a+M*((b-a)*pow(M,-1,Q)%Q)
    return (pow(2,L,P)+(c-pow(2,L,M*Q))%(M*Q))%P

U,V = coord(61827877807697,0),coord(135417323161960,39021647)
N = (pow(3,C,P)+pow(5,E,P)+85*(U*U+V*V))%P
assert N == 1223507 and M*Q < 1<<(L-4)
assert max(2*(C+720*(J-1)),3*(E+720*(J-1))) < H-5

def phase(a):
    i,j = a
    assert 0 <= i < J and 0 <= j < J
    X,Y = pow(3,C+720*i,P),pow(5,E+720*j,P)
    assert (N-X-Y)%P in range(p,P,p)
    z = X*pow(N,-1,p)%p
    assert pow(z,(p-1)//2,p) == pow(1-z,(p-1)//2,p) == p-1
    return z

def orbit(zs):
    def f(z):
        a,b = pow(z,-1,p),pow(1-z,-1,p)
        return z,1-z,a,1-a,b,1-b
    return {tuple(sorted(z%p for z in T)) for T in zip(*map(f,zs))}

def check(row):
    o,u,v,f = row
    def sub(z): return z[0]-o[0],z[1]-o[1]
    def det(a,b): return a[0]*b[1]-a[1]*b[0]
    A,B,F = map(sub,(u,v,f))
    e,m,l = det(A,B),det(F,B),det(A,F)
    assert e and e%r == 0
    assert all(any(A[j]%h == B[j]%h == 0 and
                   max(0,A[j],B[j])-min(0,A[j],B[j]) <= 90*h
                   for h in range(2,15)) for j in (0,1))
    if e < 0:
        e,m,l = -e,-m,-l
    d = gcd(e,gcd(m,l))
    assert 0 < m and 0 < l and m+l < e and (e//d)%r == 0 and e//d <= 408

rows = [
 (578,23283,34563,14713),(2057,9437,91229,11961),(90782,2394,89186,68134),
 (3257,11961,47899,15056),(5034,19041,73405,8143),(88473,5519,84885,85998),
 (5776,62746,75116,31782),(7812,46404,56808,37035),(50093,8143,23017,34235),
 (10113,37035,60219,26821),(90981,13891,87367,73405),(64963,14713,22148,34563),
 (86710,15056,31782,47624),(15784,92954,93792,89186),(22856,40112,47624,41417),
 (26377,48217,68134,47899),(26821,55261,76909,56808),(30190,40628,41880,38800),
 (33520,80782,88180,55261),(38800,56163,76836,62746),(95824,45019,81732,68949),
 (45896,49601,71933,53019),(53358,70775,95773,80782)]
assert len({i for row in rows for i in row[:3]}) == 69
keys = set()
for row in rows:
    a = tuple(divmod(z,J) for z in row)
    check(a)
    roots = tuple(map(phase,a))
    S = orbit(roots[:3])
    assert all(sum(T)%p != 1 for T in S)
    keys.add(min(S))
assert len(keys) == 23

a = tuple(map(phase,((17,249),(21,7),(97,120))))
b = tuple(map(phase,((155,167),(151,82),(75,33))))
assert a == (233,136,891) and b == (366,1201,952)
assert sum(a)%p == sum(b)%p == 1 and tuple(sorted(b)) not in orbit(a)
u = (a[0]*a[1]+a[0]*a[2]+a[1]*a[2])%p
v = a[0]*a[1]*a[2]%p
assert (u,v) == (393,933)
assert all(y == v*pow(u*x,-1,p)%p and
           (1-y)%p == x*(1-x)*pow(u,-1,p)%p for x,y in zip(a,b))
print("OK")
```
