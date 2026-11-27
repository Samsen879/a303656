# Linked traces recover both integer norms, but the shared parameter has a height cost

For an odd modulus D supported on split primes, the linked positive-odd trace tests with τ=6,21 reduce to l r=1 modulo D, where r²=−3 and l is odd and positive. A suitable root therefore exists exactly when D divides 3l²+1. Given l, take gcd(D,1+l sqrt(−3)) in the Eisenstein ring. At any split p^e dividing D, the element and its conjugate cannot meet the same prime ideal because their sum is 2. Norm divisibility thus selects one orientation at full precision, and the gcd has norm D. By multiplying by a unit to put its reduction modulo 2 in the integer suborder, recover integer coordinates a,b with D=a²+3b². No rational factorization is required for this Euclidean recovery, given l and the stated norm support. Inert square factors, if any, have to be handled separately.

Because D is odd and l is odd, the positive quotient (3l²+1)/D is a multiple of 4. For two coprime halves, a shared l must carry the product of the two D. On the true (9,9) fixture the individual minima are 324923 and 127229, neither accepted by the other half. The exact minimum shared l is 57544709323. The replay reconstructs both norms from it and shows a two-step decrement on one fixed side fails both trace checks. The two scaled mathematical parameters also cannot in general be replaced by a single common physical weight k: modulo 7 the two possible k r sets are disjoint, even allowing either side.

## Asymptotic obstruction on an existing genuine ray

Take (U,V)=3^j(133,23), A=5^U and S=3^V. The two odd halves are D_-=(A−S)/2, D_+=(A+S)/128. The base identities are checked in the replay. Cubic quotients A²±AS+S² are primitive Eisenstein norms (A and S are coprime); they are odd, and each is coprime to the matching previous half because any common factor would divide 3, which divides neither half. Hence both halves remain genuine with split-only support by induction. The halves are coprime to each other since any odd common prime would divide 2A and 2S. The split-only condition implies that each l exists by CRT.

If shared l=O(A) along infinitely many layers, a fixed m=(3l²+1)/(D_-D_+) occurs infinitely often. Then (l/A)²=m/(3·256)−(m S²/256+1)/(3A²). Since 3 does not divide m, the positive limiting square root is irrational. S=A^θ with θ<1/2; thus the approximants l/A have error O(A^(−2+2θ)) and reduced denominators powers of 5. This contradicts the finite-prime-denominator consequence of [Ridout's theorem](https://www.cambridge.org/core/journals/mathematika/article/abs/rational-approximations-to-algebraic-numbers/9B22B10EFDE4FFC405FCAAFB12C67D3C): an irrational algebraic number has only finitely many such approximations at exponent >1. Reduction of the denominator only weakens the required error bound, and convergence to an irrational number ensures infinitely many distinct rationals if there were infinitely many layers. For one half separately, suppose l=O(sqrt(A)) and set q=5^((U−1)/2). The same fixed-m argument gives irrational limit sqrt(5m/(3·2^a)), with a=1 or 7, and error O(q^(−2+2θ)). Thus even each separate minimum divided by sqrt(A) tends to infinity, and the common minimum divided by A tends to infinity.

The result supplies no effective threshold, no new phase, and no better power-law exponent. Separate finite inequalities in the replay apply to the full odd moduli of the 19 still-undecided labels, not to arbitrary peeled split support.

```python
from itertools import product
from math import gcd, prod

def F(q,z):
    t,s=2*q*q-1,2*q**3-1
    return 2*(1+s*z)**2-(1+t*z)**3

def minimum(parts):
    D=prod(parts)
    roots=[[x for x in range(p) if (3*x*x+1)%p==0] for p in parts]
    def odd_lift(rs):
        x=sum(r*(D//p)*pow(D//p,-1,p) for p,r in zip(parts,rs))%D
        return x if x%2 else x+D
    return min(map(odd_lift,product(*roots)))

def mul(z,w):  # Eisenstein coordinates in the basis 1, omega.
    a,b=z
    c,d=w
    return a*c-b*d,a*d+b*c-b*d

def recover(D,L):
    assert (3*L*L+1)%D==0
    x,y=(D,0),(1+L,2*L)
    while y!=(0,0):
        c,d=y
        h=c*c-c*d+d*d
        a,b=mul(x,(c-d,-d))
        u,v=mul(y,((2*a+h)//(2*h),(2*b+h)//(2*h)))
        x,y=y,(x[0]-u,x[1]-v)
    a,b=x
    while b%2:
        a,b=mul((a,b),(0,1))
    a,b=a-b//2,b//2
    assert a*a+3*b*b==D and gcd(a,b)==1
    return a,b

M,P=(5**9-3**9)//2,(5**9+3**9)//8
m,p=[49,109,181],[19,12979]
assert (M,P)==(prod(m),prod(p))
l,k,L=map(minimum,(m,p,m+p))
assert (l,k,L)==(324923,127229,57544709323)
assert (3*l*l+1)%P and (3*k*k+1)%M
r=pow(l,-1,M)
assert [F(q,l*r)%M for q in (6,21)]==[0,0]
assert [F(q,(l-2)*r)%M for q in (6,21)]==[484041,888793]
assert (recover(M,L),recover(P,L))==((961,-120),(157,-272))
assert [{(2*q*q-1)*(2*q**3-1)*z%7 for z in range(7)
         if F(q,z)%7==0 or F(q,-z)%7==0} for q in (6,21)]==[{3,4},{1,6}]

A,S=5**133,3**23
m=(20545392562693284644384637886087735400246635261,
   3514935999169995489797558912862627624253200474)
p=(996465818327706923877110216328632044839102412//4,
   6159042838796558433682659260361950264266519400//4)
assert 2*(m[0]**2+3*m[1]**2)==A-S
assert 128*(p[0]**2+3*p[1]**2)==A+S
assert gcd(*m)==gcd(*p)==1 and S*S<A and (A-S)%7==0

left={227:[27,115,169,227,313],229:[5,21,93,109,149,165,223,229],
      233:[25,217,267,283,317,331]}
for u,vs in left.items():
    A=5**u
    for v in vs:
        S=3**v
        nu=((A+S)&-(A+S)).bit_length()-1
        D=(A*A-S*S)//2**(1+nu)
        assert A>1000*S and nu in (3,5) and D%6==1
        assert 49*(4*D-1)>3*A*A
print("PASS")
```
