# A transported rank-three CRT class with no integral two-label completion

For the old (4,3),(3,4) labels the common window 25^64≤n≤9^96 restricts floor(log₂ n) to 297,…,304. Rigid proportional rescaling of both chord endpoint norms does not give an unbounded alternative: it requires preserving D₁:D₂=37811:781979. The resulting four terms in powers of 9 and 25 form a nondegenerate S-unit equation: same-base cancellations are ruled out by the coefficient ratio, and cross-base pairs are ruled out by parity. [Evertse–Schlickewei–Schmidt](https://annals.math.princeton.edu/2002/155-3/p04) gives finitely many projective solutions, and a common scale that is both a power of 9 and a power of 25 is trivial. Also a fixed rational-function family n(t),q(t) with n→∞ cannot keep n/q≈64(log₂ n)² asymptotically, since their ratio grows as a power of t or tends to a constant.

There is a different, unbounded **obstruction** construction. Add T to all four exponents along a fixed progression preserving the old label constants modulo 109M, where M fixes all rank rows, prime-column depths and the bad support at 2 and 5. Take K=96T and X=2^K. The label power bounds leave the entirety of [X,2X) at large T. The single genuine seed for the label (3+T,4+T) can be built from (x,u),(x+1,a−u) with x=au+D−(a²+1)/2 and odd a in the old congruence class. Irrational rotation along the fixed K progression gives infinitely many a with a−8√2 K in a fixed interior interval of (√2,3√2). For u on its old congruence class near sqrt(3X/2)/a, n is near 3X/2, and S/(64q)=(a²+1)/128+o(1) is strictly in (K²,K(K+1)). This supplies a genuine seed and preserves the relevant n residues.

Independently choose an integer difference Δ near the difference of two strict real-band points at that same n, with Δ≡Δ₀ mod M and Δ≡(16,8) mod 109. At new primes dividing W, choose residues so N(Δ)−e² is a unit, retaining only the anchored bad support. The CRT grid modulus is O(rad(W))=O(X^(3/16)) after absorbing fixed constants. It is much smaller than the O(X/K^4) transverse tolerance for the central construction (choose real angles separated by a fixed proportion of their angular window). Thus the rank-three modular data and two compatible real angles can coexist at arbitrarily large scales within this construction.

But the same n and chosen Δ force j=1, L=56 and M₁M₂=29 modulo 109. The oriented cross product would have to satisfy h²=M₁M₂−(L−j)²≡56 mod 109, a quadratic nonresidue. There is no integer completion for that Δ at the prescribed n. The single true seed at that n is an independent witness; the compatible real points for the moved Δ need not include that particular Gaussian point. No claim rules out a different Δ or a second true label at that n by some other construction.

The finite replay at the genuine 560-bit anchor verifies rank preservation under the exact prescribed grid displacement, the two strict real angular intervals and the explicit nonresidue obstruction.

~~~python
from math import gcd, isqrt, prod
from fractions import Fraction as F

K, X = 300, 1 << 300
a, u = 3395, 472984194841387909896403492694189266281840
x = a*u + 9**3 + 2*25**4 - (a*a+1)//2
n = x*x + u*u + 3*9**3 + 5*25**4

def N(z): return z[0]**2+z[1]**2
def cert(r,s,P,Q):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    x,y = P
    v,w = Q
    f,g,h = x-v,y-w,x*w-y*v
    assert f%2 and g%2 and h%2==0
    q = ((f+g)//2)**2+((f-g)//2)**2
    assert A<=B and B**16<=n<=A**32 and X<=S<2*X
    assert N(P)==S and N(Q)==S+2*D and q%2
    assert 2*q*S==(D-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
    return U,D,(n-U-q,abs(h)),q

P = (1238240656117444633368032107716581205155788446,
     1022396213763583296740059539842408420297582288)
Q = (1237638945231334085263186942097216682418805929,
     1023124519121177798984074135516404730073639771)
U,D,z,q = cert(4,3,P,Q)
V,E,w,qq = cert(3,4,(x,u),(x+1,a-u))
assert q!=qq and X<=n<2*X
e,b,g = V-U,D+E,E-D
W = e*b*g
L = (n-U)*(n-V)-(D*D+E*E)//2
delta = z[0]-w[0],z[1]-w[1]
d = N(delta)-e*e
assert (d//2).bit_length()==560
rows = (181,1229,1383784813,493076497,332378247127)
cols = (277,8377,268293089)
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)
assert all(p>1 and all(p%f for f in range(2,isqrt(p)+1))
           for p in rows+cols+(109,))
assert all(W%l for l in rows) and all(bad%p and p%4==1 for p in cols)
def code(t):
    return sum((pow(t,(l-1)//2,l)==l-1)<<i for i,l in enumerate(rows))
assert [code(t) for t in (2,5,*cols)]==[7,28,1,15,17]
assert not ({1,15,17,14,16,30,31}&{0,7,28,27})

M = 2**6*3**3*5**3*prod(rows)*prod(p*p for p in cols)
df = delta[0]+57*M,delta[1]+75*M
dd = N(df)-e*e
for v in (d,dd):
    assert gcd(v,W*W)==800 and all(v%l==0 for l in rows)
    assert all((v+t*t)%p==0 and (v+t*t)%p**2
               for p,t in zip(cols,(b,b,g)))
assert dd%2==0 and (dd//2)**5>X**9
M1,M2 = N(z),N(w)
h2 = M1*M2-(L-dd//2)**2
assert h2>0 and h2%109==56 and pow(56,54,109)==108

T = 1<<64
r = isqrt(h2*T*T)
C = N(df)
v = F(M1-M2+C,2)
sgn = 1 if z[0]*w[1]>z[1]*w[0] else -1
for hh in (sgn*F(r,T),sgn*F(r+1,T)):
    x1,y1 = (v*df[0]-hh*df[1])/C,(v*df[1]+hh*df[0])/C
    for U0,D0,x0,y0 in ((U,D,x1,y1),(V,E,x1-df[0],y1-df[1])):
        S,q0 = n-U0-D0,n-U0-x0
        assert y0>0 and 64*K*K*q0<S<64*K*(K+1)*q0
print("Native rank 3. Same rank and real band after CRT; h^2 = 56 mod 109.")
~~~
