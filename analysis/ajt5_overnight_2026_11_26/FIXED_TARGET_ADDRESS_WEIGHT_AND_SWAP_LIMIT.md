# A fixed-target weighted address bound for a balanced long-step sector

Fix n and the original chart S(i,j)=α 3^(720i)+β 5^(720j), with positive remainders, widths <D=rs, r,s≈R≈H^(3/4). Let Q_D be the squarefree product of counted primes not dividing 15n, each original step of order a multiple of D. In the balanced long-step sector assume a,b,c,d≤C sqrt(r), r|ad−bc≠0, r not dividing hk, and physical step sizes O_C(R). For a common actual address set A put B_n(A)=∑_(o∈A) log gcd(Q_D,n−S(o)).

The total log-prime weight W_n(A) of triples with at least one vertex in A is O_(C,ε)(R^(3/4+ε) B_n(A)). For fixed counted p and anchor, the nearby residue graph has O(R^(3/4)) hits by the same Cartesian incidence theorem and replicated distinct-line construction, with doubled span <D and characteristic condition R³≪p². A fixed actual displacement v has O_ε(R^ε) decompositions into (a,h),(b,k), by the divisor bound. For each decomposition, ad−bc=rj has O_C(1) nonzero j; gcd(a,b) divides j since it is <r, and max(a,b) is ≫_C sqrt(r) because the determinant magnitude is at least r. Thus the solutions (c,d) lie on a lattice line with at most O_C(1) members in the bounded box. If the anchor is either translated vertex, choose the nearby start first and use the same argument (swap v,w when needed). Charge each prime at a fixed actual anchor to that anchor's true remainder. This gives the bound and also B_n(A)≤O(|A|H).

A natural sufficient but not verified full-sector condition is a common address set intersecting every relevant triple and B_n(A)≪R^(37/24−δ). Since the prior fourth-point capacity is O(R^(3/8)) here, this condition would reach O(H²/log H) total four hits. In particular |A|≪R^(5/24−δ) suffices if such a set exists. This does not average over n or assert any such full-sector address set.

A separate exact bound: at fixed n,p, an observed phase product XY determines X,Y up to switching as roots of T²−nT+XY. Since both axes are injective on the original short chart, this gives at most two addresses; it is unique when the axis characters are fixed and unequal. Each fixed nonzero offset (i,j) causing a swap has x^i y^j=1 mod p and X(1+x^i)=n. The latter with n nonzero permits one start for that p, and the former has a nonzero integer numerator of log height O(R) by independence of 3 and 5. This controls repeated products, not recurring primes at different products.

The replay verifies a true exact-once swapped pair at (1,268),(277,128) with product 405 modulo 1259, reaching multiplicity two. It also retains the genuine diagonal-vs-crossed supports and the saturated-lattice rank obstruction.

```python
from itertools import combinations
from math import gcd, isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D,P = r*s,p*p
assert all(q%2 and all(q%i for i in range(3,isqrt(q)+1,2))
           for q in (t,r,s,p))
assert p == 2*D+1 and p%4 == 3 and 2*J < D
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000
for b in (3,5):
    assert pow(b,720*D,p) == 1 and pow(b,p-1,P) != 1
    assert all(pow(b,720*(D//a),p) != 1 for a in (r,s))

M,L = 146651884329720,H//2-4
C,E = 3*t+80,t+144
u,v = [(pow(2,L,P)+(a-pow(2,L,M))%M)%P
       for a in (61827877807697,135417323161960)]
N = (pow(3,C,P)+pow(5,E,P)+85*(u*u+v*v))%P
assert N == 1223507 and N%p == 1018
assert M < 1<<(L-4)
assert max(2*(C+720*(J-1)),3*(E+720*(J-1))) < H-5
X = [pow(3,C+720*i,P) for i in range(J)]
Y = [pow(5,E+720*j,P) for j in range(J)]

def read(z):
    i,j = z
    assert 0 <= i < J and 0 <= j < J
    return (N-X[i]-Y[j])%P

def exact(z):
    return read(z) in range(p,P,p)

def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

def sub(a,b):
    return a[0]-b[0],a[1]-b[1]

for i,j,h,k,e,m,l in [(30,137,3,-8,408,120,233),
                       (308,293,-3,-7,238,90,9)]:
    v,w = (15*h,13*k),(88*h,6*k)
    F,G = m*v[0]+l*w[0],m*v[1]+l*w[1]
    assert h%r and k%r and e%r == 0 and gcd(e,gcd(m,l)) == 1
    assert F%e == G%e == 0 and m+l < e
    assert all(exact((i+a,j+b)) for a,b in ((0,0),v,w,(F//e,G//e)))

def cross(h,k):
    return det((pow(3,720*15*h,p)-1,pow(5,720*13*k,p)-1),
               (pow(3,720*88*h,p)-1,pow(5,720*6*k,p)-1))%p

assert [[cross(h,k) for k in (-8,-7)] for h in (3,-3)] == [[0,1041],[176,0]]

o,v,T = (26,83),(193,161),(27,20)
assert det(v,T) == -487
hits = [(i,j) for i in range(J) for j in range(J)
        if det(sub((i,j),o),T)%487 == det(v,sub((i,j),o))%487 == 0
        and read((i,j))%p == 0]
assert hits == [(26,83),(161,183),(219,244),(292,262)]
assert all(map(exact,hits))
assert sorted(abs(det(sub(b,a),sub(c,a)))//487
              for a,b,c in combinations(hits,3)) == [5,5,7,17]
assert (read((53,103))%p,read((30,104))%p) == (559,60)

pair = ((1,268),(277,128))
assert [(X[i]%p,Y[j]%p) for i,j in pair] == [(252,766),(766,252)]
assert all(map(exact,pair)) and 252*766%p == 405
i,j = sub(*pair)
assert pow(3,720*i,p)*pow(5,720*j,p)%p == 1
print("OK")
```
