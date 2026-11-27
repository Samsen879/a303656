# A two-block character filter and one target per oriented allocation

Under the fixed oriented Δ, fixed sign of h, and fixed bad-prime allocation hypotheses of the [half-angle divisor](https://github.com/Samsen879/a303656/commit/0e27395890329884cfe6c1eb7d14791e58cf2adf), take a,b-independent notation e,b,g for the Gram parameters, d=2j and W=ebg. Let m=m_bm_g be the product of good-prime changes in the two remaining Gram factors and G=gcd(d,R). The half-angle coprime pair is (a,c) with c>0, and Λ=a²−dc² divides 4mG. Its entire good-prime part is m; those good primes are coprime to d.

At every odd prime ℓ dividing d but not W, the midpoint congruence av≡−W mod d makes a a unit. Hence Λ is a nonzero square modulo ℓ. Form a vector of Legendre characters at these ℓ; make it additive using values in F₂, and quotient by the vectors of prime divisors of 2G. Calling this reduced character σ, it follows that σ(m_b)=σ(m_g). In particular, counts A_σ and B_σ of directional candidate changes in the two blocks combine as a sum of matching character-class products, not as a full cross product. If r actually independent parity columns are present in an otherwise unrestricted binary choice, only a 2^(−r) portion of those choices can solve the character condition. No uniform lower bound on actual rank is claimed.

Now fix a genuine anchor and a specified oriented change at every prime of m. At each p^ν exactly dividing m, the chosen split direction forces a≡ρ_p c modulo p^ν, for the specified root ρ_p of d. Thus any two candidate coprime pairs obey m | ac′−a′c. At ordinary height X≤n,n′<2X and j≥X with j≪X²/(log X)^4, |c|√d<|a|/2 for large X, since the ratio is asymptotic to |n′−n|/(n+n′)≤1/3. Hence

~~~text
|ac′−a′c| ≪ sqrt(ΛΛ′)/sqrt(d) ≪ mG/sqrt(d) = o(m).
~~~

Here G≤W²=O(X^(3/8)) and sqrt(d)≫sqrt(X). The determinant is zero. Coprimality and c>0 force identical pairs, so k=(cx+ay)/Λ and s=ck are uniquely determined by the anchor. Thus there is at most one candidate ordinary-height integer partner per specified oriented allocation, without an extra sum over midpoints. This is an upper bound and does not produce a partner. The count of actual oriented allocations in the middle shells remains open.

## Exact character control at genuine labels

In the 560-bit native deficit fixture, G=800 and the product character at ℓ=181 and 1229 kills both bad support primes 2 and 5. Both entire good blocks pair with product character +1; omitting the exponent-one prime 277 from the first block gives −1, so this latter proposed combined allocation cannot connect two genuine integer targets. The +1 case merely passes this test.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt, prod

K, X = 300, 1 << 300
u, a = 472984194841387909896403492694189266281840, 3395
x = a*u + 9**3 + 2*25**4 - (a*a+1)//2
n = x*x + u*u + 3*9**3 + 5*25**4

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
    return U,D,(z[0],abs(z[1])),q

P = (1238240656117444633368032107716581205155788446,
     1022396213763583296740059539842408420297582288)
Q = (1237638945231334085263186942097216682418805929,
     1023124519121177798984074135516404730073639771)
U,D,z,q = cert(4,3,P,Q)
V,E,w,qq = cert(3,4,(x,u),(x+1,a-u))
assert q!=qq
e,b,g = V-U,D+E,E-D
W = e*b*g
dot,h = mul(bar(z),w)
j = (n-U)*(n-V)-(D*D+E*E)//2-dot
d,Delta = 2*j,sub(z,w)
C = N(Delta)
xx,yy = d*(2*n-U-V)-W,2*h
R = prod(d+l*l for l in (e,b,g))
assert j**5>X**9 and C==d+e*e and xx*xx-d*yy*yy==R
G = gcd(d,R)
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)

def strip(t,m):
    while (f:=gcd(t,m))>1: t//=f
    return t
def prime(p):
    return p>1 and all(p%k for k in range(2,isqrt(p)+1))
def chi(t):
    return prod(1 if pow(t,(p-1)//2,p)==1 else -1 for p in (181,1229))
def red(v,m):
    v=F(v)
    return v.numerator*pow(v.denominator,-1,m)%m

assert strip(G,10)==1 and chi(2)==chi(5)==1
assert all(prime(p) and d%p==0 and W%p for p in (181,1229))
B0,G0 = strip(d+b*b,bad),strip(d+g*g,bad)
assert gcd(B0,G0)==gcd(B0*G0,gcd(xx,yy))==1
assert prime(277) and B0%277==0 and B0%277**2
assert chi(B0)==chi(G0)==1 and chi(277)==-1

assert chi(B0*G0)==1 and chi(B0//277*G0)==-1

~~~
