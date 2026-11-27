# Fixing a genuine Gaussian anchor reveals stronger integer obstructions

Under the two actual labels (4+T,3+T),(3+T,4+T), fix the genuine z₂ of the second-written label. For the desired difference squared d+e², put c=(M₁+M₂−e²−d)/2 and F=M₁M₂−c² with M_i=(n−U_i−D_i)(n−U_i+D_i). The real point containing this exact anchor is z₁=(c−ih)/conj(z₂), h²=F. An integral seed needs integer h and conjugate(z₂) dividing the numerator in the Gaussian integers, plus parity, norm and height conditions. At a splitting prime p dividing both coordinates of z₂, any p∤c violates divisibility even when F≡−c² lifts to a square at every p-power.

Take K=96T, X=2^K, and odd a with a−8√2K in [√2,3√2]. Set N=a²+1, C=D₂−N/2 and take u between (6/5)√X/a and (5/4)√X/a. The Gaussian chord (au+C,u),(au+C+1,a−u) supplies a true seed in the strict t=8 band: its endpoint norm difference is 2D₂, q₂=((2u−a)²+1)/2, and S₂/(64q₂)=(a²+1)/128+o(1). The growing labels make both ordinary height windows valid.

Keep the old label residues by a fixed progression of T in the finite rank panel and modulo 49 and 71089. In mod 7 some u-class gives n≡3 or 4 and nonzero derivative: take u≡0 if a≠0, or u≡2 if a≡0. Exactly six of its seven lifts into mod 49 make v₇(M₁)=1. Since 7 is Gaussian inert, the entire circle for label (4+T,3+T) has no Gaussian integer point. Independently impose 2u≡a−20365 mod 71089, where 20365²≡−1 and D₂≡0. Both chord endpoints then vanish in one evaluation component, so 71089 divides both coordinates of z₂. CRT gives proportion 6/49+o(1) in that anchor progression.

For these same fixed anchors place d on the old rank-three congruence and d≡d₀ mod 71089. Extra primes of W receive unit d residues. The O(X^(3/16)) CRT spacing is much smaller than the order X²/(log X)^4 d tolerance from an interior real angle window. Thus these false candidates have exact real completion containing the genuine z₂ and the old rank panel. They also have c≡13347 mod 71089. The replay checks a same n and same z₂ nonresidue at 109 and an actual shifted-anchor control with v₇(M₁)=1 and locally square F at 71089. No arbitrary target or other labeling is excluded.

For fixed large T and the stated a, write A=9^(T+3), B=25^(T+3) and vary u. The discriminant of S₁(u) is −4F_S with F_S=C²+N(120B−24A). The positive square root lies strictly below C+6N/5 by less than 1/5, since the squared difference is (132/5)AN+(6/25)N² and A/B→0. The upper endpoint is on the 1/5 grid; F_S is not an integer square. Then S₁ is a conjugation-invariant irreducible in Q(i)[u], appears once in M₁, and cannot be contributed by a rational Gaussian function norm. This rules out fixed-chord rational formulas, not isolated integer u or other chords.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt, prod

K, X, a = 300, 1 << 300, 3395
A, B = 9**3, 25**3
U, V, D, E = 18*A+3*B, 2*A+75*B, 9*A+2*B, A+50*B
e, b, g = V-U, E+D, E-D
W = e*b*g
u0 = 472984194841387909896403492694189266281840
dx = 1185754957113613171463733785933264081457749154312089869861402491014581613938778660
dy = -2014154207221590115583785809874279455203009021599933435790807841958275179852930884836
d0 = dx*dx + dy*dy - e*e
rows = (181,1229,1383784813,493076497,332378247127)
marks = (277,8377,268293089)
M = 2**6*3**3*5**3*prod(rows)*prod(p*p for p in marks)
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)
assert all(all(p % j for j in range(2,isqrt(p)+1))
           for p in (*rows,*marks,109,71089))

def code(v):
    return sum((pow(v,(p-1)//2,p)==p-1)<<i
               for i,p in enumerate(rows))

codes = [code(v) for v in (2,5,*marks)]
assert codes == [7,28,1,15,17]
span = {0}
for v in codes:
    span |= {x ^ v for x in span}
assert len(span) == 32

def cert(n, U, D, z):
    S, q = n-U-D, n-U-z[0]
    assert z[1]>0 and X<=S<2*X
    assert 64*K*K*q<S<64*K*(K+1)*q
    assert 2*q*S==(D-q)**2+z[1]**2
    return q

def anchor(u):
    x = a*u+E-(a*a+1)//2
    n = x*x+u*u+V+E
    t = 2*u-a
    q = ((t+1)//2)**2+((t-1)//2)**2
    z = (n-V-q, abs(x*(a-u)-u*(x+1)))
    assert (x+1)**2+(a-u)**2==n-V+E
    assert q%2 and z[1]%2==0 and cert(n,V,E,z)==q
    assert X<=n<2*X and 25**64<=n<=9**96 and 9*A<=B
    return n,z

def completion(n,z,d):
    assert d%2==0 and (d//2)**5>X**9 and gcd(d,W*W)==800
    assert all(d%p==0 and W%p for p in rows)
    assert all(p%4==1 and bad%p and v%p==0 and v%(p*p)
               for p,v in zip(marks,(d+b*b,d+b*b,d+g*g)))
    M1, M2 = (n-U)**2-D*D, (n-V)**2-E*E
    c = (M1+M2-e*e-d)//2
    H = M1*M2-c*c
    den = 1<<64
    lo = isqrt(H*den*den)
    for h in (F(lo,den), F(lo+1,den)):
        x,y = (c*z[0]+h*z[1])/M2, (c*z[1]-h*z[0])/M2
        S,q = n-U-D,n-U-x
        assert y>0 and X<=S<2*X and 64*K*K*q<S<64*K*(K+1)*q
    return c,H

n,z = anchor(u0)
ok = z[0]+dx,z[1]+dy
q = cert(n,U,D,ok)
assert q%2 and ok[1]%2==0
assert q == (63297235741977069584715027315893519537483**2
             +665008121852525174429880646680416256520000**2)
c,H = completion(n,z,d0)
assert c==ok[0]*z[0]+ok[1]*z[1]
assert H==(ok[0]*z[1]-ok[1]*z[0])**2

_,H = completion(n,z,d0+6*M*W)
assert H%109==54 and pow(54,54,109)==108

n,z = anchor(u0+3119444)
c,H = completion(n,z,d0)
assert ((n-U-D)%49,(n-U+D)%49)==(41,7)
assert all(v%71089==0 for v in z)
assert (c%71089,H%71089)==(13347,6625)
assert 38408**2%71089==6625
~~~
