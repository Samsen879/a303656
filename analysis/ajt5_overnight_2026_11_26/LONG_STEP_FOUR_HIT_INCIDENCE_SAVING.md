# An incidence saving for a restricted long-step four-hit chart

Retain the saturation-sector hypotheses: r|e≤Cr, r|ad−bc≠0, r not dividing hk, actual fixed n not divisible by p, chart widths <D, 2R0<D=rs, and no rational-zero three-hit determinant, as verified by the prior coefficient/LTE bound. Write A=max(a,c), B=max(b,d), and assume A≤B by switching axes. Fix p,h,k and a candidate d0=e/r≤C. Then the fourth offset is (h(P/r)/d0,k(Q/r)/d0), and integrality puts it in two arithmetic progressions with steps h/gcd(h,d0), k/gcd(k,d0), lengths O_C(A), O_C(B).

View the residue reads as two multiplicative progressions. Multiply every solution by the powers of all the step shifts in the rectangle. This generates ≍_C AB distinct lines of the form α^(-1)x+β^(-1)y=n in the doubled product of size O_C(A) by O_C(B). The nonzero right side makes the lines distinct, and the doubled exponent spans <D give injective powers. Apply [Stevens–de Zeeuw, Theorem 4](https://arxiv.org/pdf/1609.06284v4#page=3): the Cartesian size condition follows from the replicated line count (or trivial bounded-size cases), and the arithmetic condition follows when R0³≪p², as in r,s≈R. Dividing the incidence bound by the number of replicated lines gives O_C(A^(1/2) B^(1/4)+1) actual fourth points. Summing the bounded number of d0 preserves this estimate.

The previous prime-support count charges O(R0/log D) primes per nonzero determinant and O(R0²/(AB)) actual h,k per coefficient tuple. In a dyadic coefficient box the number of eligible tuples with A≤B is O(A²B²/r), by fixing coprime a,c and sweeping the possible nonzero multiples of r. Summing gives O_C(R0³ M^(11/4)/(r log D)). At full width in the specified balanced regime r≈R≈H^(3/4), M≈sqrt(r), this is O(H^(81/32)/log H), still above the desired H²/log H. The short-step threshold extends to r^(19/72). The remaining sufficient support goal W_n=O(r^(55/24)) in the balanced long-step sector is not proved.

The exact replay shows two distinct (h,k) values with the same actual n,p and normalized template. They both yield genuine exact-once four hits; crossed pairings fail with the displayed 2×2 off-diagonal values. This refutes simply treating the two axis supports as independent or counting at most one (h,k) per prime.

```python
from itertools import combinations
from math import gcd, isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D = r*s
def prime(q):
    return q>2 and q%2 and all(q%i for i in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p==2*D+1 and p%4==3
assert t%720==1 and 16*t<=H<=24*t and J==H//12000 and 2*J<D
for q in (3,5):
    assert pow(q,720*D,p)==1
    assert all(pow(q,720*(D//a),p)!=1 for a in (r,s))

M,z = 146651884329720,1<<(H//2-4)
x,y = (z+(a-z)%M for a in (61827877807697,135417323161960))
S0 = 3**(3*t+80)+5**(t+144)
n = S0+85*(x*x+y*y)
assert n.bit_length()==H and n>3**(3*t+80+720*(J-1))+5**(t+144+720*(J-1))
assert n-S0==(7*x-6*y)**2+(6*x+7*y)**2 and n%(p*p)==1223507

def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))
def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))
def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

X = [pow(3,3*t+80+720*u,p*p) for u in range(J)]
Y = [pow(5,t+144+720*v,p*p) for v in range(J)]
def read(z):
    u,v=z
    assert 0<=u<J and 0<=v<J
    return (n-X[u]-Y[v])%(p*p)
def exact(z):
    return read(z) in range(p,p*p,p)

o,v,w,T = (26,83),(193,161),(266,179),(27,20)
assert plus(v,w)==tuple(r*a for a in T) and det(v,T)==-487
hits = [(i,j) for i in range(J) for j in range(J)
        if det(sub((i,j),o),T)%487 == det(v,sub((i,j),o))%487 == 0
        and read((i,j))%p==0]
assert hits==[(26,83),(161,183),(219,244),(292,262)]
assert all(map(exact,hits))
assert sorted(abs(det(sub(b,a),sub(c,a)))//487
              for a,b,c in combinations(hits,3))==[5,5,7,17]
assert read((53,103))%p==559 and read((30,104))%p==60

a,b,c,d = 15,13,88,6
assert a*d-b*c==-62*r
for o,h,k,e,m,l in [((30,137),3,-8,408,120,233),
                    ((308,293),-3,-7,238,90,9)]:
    assert h%r and k%r and e%r==0 and gcd(e,gcd(m,l))==1 and m+l<e
    v,w = (a*h,b*k),(c*h,d*k)
    F = tuple(m*u+l*v for u,v in zip(v,w))
    assert all(z%e==0 for z in F)
    f = tuple(z//e for z in F)
    assert all(exact(plus(o,z)) for z in ((0,0),v,w,f))

def cross(h,k):
    A,C = pow(3,720*a*h,p)-1,pow(3,720*c*h,p)-1
    B,E = pow(5,720*b*k,p)-1,pow(5,720*d*k,p)-1
    return (A*E-C*B)%p
assert [[cross(h,k) for k in (-8,-7)] for h in (3,-3)]==[[0,1041],[176,0]]
```
