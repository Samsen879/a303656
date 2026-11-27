# Rank three of the mixed Pell character filter on a genuine anchor

The existing [mixed allocation filter](https://github.com/Samsen879/a303656/commit/caadf573d8b47d1b49d5475e2c14ad5328f8fac2) assigns odd-prime rows ℓ|d, ℓ∤W, encoding Legendre symbols (p/ℓ) as bits and quotienting by the columns of primes dividing 2G, G=gcd(d,R). An integral two-block change must have zero combined signature.

Two algebraic relations explain which restrictions are automatic. First, a good split prime in either remaining Gram factor has p≡1 mod 4 and (d/p)=1. For d's squarefree part 2^ε times the product of a set F of odd primes, quadratic reciprocity gives (2/p)^ε times the product over ℓ in F of (p/ℓ) equal to one. With only these splitting conditions, the CRT model for allowed residue classes imposes no nontrivial relation on selected rows unless ε=0 and a nonempty F is contained in them. In that case the single relation descends to the quotient only when it kills the bad support columns. This description of permissible residue classes does not assert that actual Gram prime factors occupy them independently.

Second, the full Gram factor C_λ=d+λ² reduces to a nonzero square at each selected row. Hence the sum of its good-prime columns with odd exponent equals the corresponding sum over its bad part, both before and after quotienting. This is a dependence for a full block, not an identity forcing each column to vanish.

## Exact 560-bit control

The shared genuine integer anchor is on the actual (4,3),(3,4) labels in the strict t=8 band; its deficit j has 560 bits. The five exact prime rows are 181, 1229, 1383784813, 493076497, 332378247127. In this row order (lowest bit first), the bad columns 2 and 5 have codes 7 and 28. The independent good columns 277, 8377, 268293089 have codes 1, 15, 17 in the same coordinates, each with actual depth one in its respective Gram factor. They span rank three modulo the bad support. Among the eight masks obtained by toggling these three whole-factor selections, exactly the one omitting 8377 passes. The two whole good parts have codes 19 and 7. Up to 8192, the only good prime in the two blocks is 277; quotienting by its column too leaves rank two on 8377 and 268293089. None of these finite statements provides a second integer target or a uniform growing rank lower bound.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt, prod

K, X = 300, 1 << 300
a, u = 3395, 472984194841387909896403492694189266281840
x = a*u + 9**3+2*25**4-(a*a+1)//2
n = x*x+u*u+3*9**3+5*25**4

def N(z): return z[0]**2+z[1]**2
def sub(z,w): return z[0]-w[0],z[1]-w[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def bar(z): return z[0],-z[1]

def cert(r,s,P,Q):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    f,g = sub(P,Q)
    z = mul(bar(P),Q)
    q = ((f+g)//2)**2+((f-g)//2)**2
    assert X<=n<2*X and A<=B and B**16<=n<=A**32
    assert N(P)==S and N(Q)==S+2*D and f%2 and g%2 and q%2
    assert z[1]%2==0 and z[0]==n-U-q
    assert 2*q*S==(D-q)**2+z[1]**2 and X<=S<2*X
    assert 64*K*K*q<S<64*K*(K+1)*q
    if z[1]<0: P,Q,z=bar(P),bar(Q),bar(z)
    return U,D,P,Q,z,q

P = (1238240656117444633368032107716581205155788446,
     1022396213763583296740059539842408420297582288)
Q = (1237638945231334085263186942097216682418805929,
     1023124519121177798984074135516404730073639771)
U,D,a1,c1,z,q = cert(4,3,P,Q)
V,E,a2,c2,w,qq = cert(3,4,(x,u),(x+1,a-u))
assert q!=qq
e,b,g = V-U,D+E,E-D
W = e*b*g
dot,h = mul(bar(z),w)
j = (n-U)*(n-V)-(D*D+E*E)//2-dot
d,Delta = 2*j,sub(z,w)
C = N(Delta)
Cb = N(sub(mul(a1,bar(a2)),mul(c1,bar(c2))))
Cg = N(sub(mul(a1,c2),mul(a2,c1)))
assert [C,Cb,Cg]==[d+l*l for l in (e,b,g)]
xx,yy = d*(2*n-U-V)-W,2*h
R,G = C*Cb*Cg,gcd(d,C*Cb*Cg)
assert j.bit_length()==560 and j**5>X**9 and xx*xx-d*yy*yy==R
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)

def strip(t,m):
    while (f:=gcd(t,m))>1: t//=f
    return t
def prime(p):
    return p>1 and all(p%k for k in range(2,isqrt(p)+1))
def red(v,m):
    v=F(v)
    return v.numerator*pow(v.denominator,-1,m)%m

rows = (181,1229,1383784813,493076497,332378247127)
marks = (277,8377,268293089)
assert strip(G,10)==1 and G%2==G%5==0
assert all(prime(p) and d%p==0 and W%p for p in rows)
def code(t):
    assert all(t%p for p in rows)
    return sum((pow(t,(p-1)//2,p)==p-1)<<i for i,p in enumerate(rows))
B0,G0 = strip(Cb,bad),strip(Cg,bad)
assert gcd(B0,G0)==gcd(B0*G0,gcd(xx,yy))==1
for p,Q0 in zip(marks,(B0,B0,G0)):
    assert prime(p) and p%4==1 and Q0%p==0 and Q0%p**2
assert [code(t) for t in (2,5,*marks,B0,G0)]==[7,28,1,15,17,19,7]
N0 = {0,7,28,27}
masks = [B0*G0//prod(p for i,p in enumerate(marks) if z0>>i&1)
         for z0 in range(8)]
assert [i for i,m in enumerate(masks) if code(m) in N0]==[2]
assert [p for p in range(2,8193) if prime(p) and B0*G0%p==0]==[277]
assert not ({15,17,15^17} & (N0|{v^1 for v in N0}))

~~~
