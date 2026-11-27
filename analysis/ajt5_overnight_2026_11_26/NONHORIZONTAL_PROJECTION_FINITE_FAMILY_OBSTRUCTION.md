# Nonhorizontal primitive projection survives an old panel but a fixed direction family can be excluded

For primitive Gaussian direction g=r+is with L=r²+s², write the two transformed endpoints as conj(g)P=x+iy and conj(g)Q=x+h+i(b−y). Here h is a fixed integral projection, not the full chord length. Put N=h²+b² and C=LD−N/2. The actual norm difference implies hx−by=C and the complete-square condition LN(n−H)−C²=(bx+hy)². Integral endpoints require reconstructing both with g/L, not merely passing this square test. When h=0, the resulting chord q=2LD²/b² is too small for the stated growing band even with the small allowed rotation. For any fixed h>0, the exact identity for S and the critical window reduce possible slopes to |b|=ha+j, −4h≤j≤10h; for h=1 the six differences are −2,0,2,4,6,8 on the same anchored phase.

At both directions (1,2),(2,1), L=5, h=1, b=a+4, explicit shared CRT anchor classes give genuine reconstructed local endpoints at 5,7,17,19,29. Varying y by 5z gives derivative 2(bx+y), a unit at each, so each label separately lifts for the same fixed target n through all depths of this old panel. In that same anchor family adding six new primes (11,13,23,31,37,41) independently obstructs all six slopes by exact nonsquare reads of the transformed equation. This is a real failure beyond the old finite panel, not a failure of every nonhorizontal representation.

For any fixed finite list of primitive directions and projection heights, each possible slope difference is finite as just noted. Along the first actual anchor, substituting n=H₁+N₁u²+2aC₁u+C₁² into the second square test gives a quadratic in u. The difference of its completed-square centers is G₁−G₂, with G_i=H_i−D_i+N_i/(4L_i)+L_iD_i²/N_i. At the base labels this is a nonzero rational function of a: different quadratic leading terms unless L₂=h²; a distinct linear coefficient if j≠0; and when both vanish the actual base inequalities H₁−D₁<H₂−D₂, D₁<D₂ make it strictly negative. Choose a calibration avoiding the finite degeneracies. For each pattern choose a new prime avoiding that quadratic's discriminant and leading-coefficient support. A nondegenerate quadratic takes a nonsquare somewhere modulo each such odd prime, via its exact quadratic-character sum. Freeze the true labels and a in these congruences; combine the forbidden u reads by CRT. The growing first chord retains its actual target and admits the independent narrow-Gaussian-sector congruence for its short rotation into the window. This excludes each specified finite family on an unbounded set of generated anchors, not every integral second seed. No uniform growing direction radius is claimed here.

The actual K396 replay ends with a genuine second primitive displacement at the same true n and first short rotation, while the stated short L=5 and horizontal directions fail. A direction projecting this particular genuine displacement to 1 has length >2^184. That last observation is about the chosen actual chord, not all representations at this n.

~~~python
from math import gcd, isqrt

def data(T):
    A,B = 9**(T+3),25**(T+3)
    return 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
def C(b,D,L=1): return L*D-(b*b+1)//2
def f(a,H,D,u): return (a*u+C(a,D))**2+u*u+H
def F(L,b,H,D,n): return L*(b*b+1)*(n-H)-C(b,D,L)**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def N(z): return z[0]**2+z[1]**2
def sub(z,w): return tuple(a-b for a,b in zip(z,w))
def prime(p): return p>1 and all(p%d for d in range(2,isqrt(p)+1))

a,T0 = 72170223301,5*23604840
H,D,J,E = data(0)
b = a+4
for p,u,z1,z2 in [(5,1,7,13),(7,1,16,15),(17,1,254,80),
                  (19,3,15,231),(29,0,671,334)]:
    assert pow(9,T0,125 if p==5 else p*p)==1
    assert p==5 or pow(25,T0,p*p)==1
    j0 = {5:4,7:2,17:6,19:-2,29:8}[p]
    assert not ({f(a,H,D,v)%(p*p) for v in range(p*p)}
                & {f(a+j0,J,E,v)%(p*p) for v in range(p*p)})
    for g,y in [((1,2),1+5*z1),((2,1),4+5*z2)]:
        x = b*y+C(b,E,5)
        assert all(c%5==0 for c in (*mul(g,(x,y)),*mul(g,(x+1,b-y))))
        assert (J+(x*x+y*y)//5-f(a,H,D,u))%(p*p)==0
        assert 2*(b*x+y)%p

for j,p,u,r in [(-2,11,1,6),(0,13,2,2),(2,23,0,19),
                (4,31,2,21),(6,37,1,32),(8,41,2,27)]:
    assert prime(p) and F(5,a+j,J,E,f(a,H,D,u))%p==r
    assert pow(r,(p-1)//2,p)==p-1

def seed(P,Q,D):
    x,y = sub(P,Q)
    assert x%2 and y%2 and N(Q)==N(P)+2*D
    q = ((x+y)//2)**2+((x-y)//2)**2
    w = P[0]*Q[1]-P[1]*Q[0]
    assert q%2 and w%2==0 and 2*q*N(P)==(D-q)**2+w*w
    return q

H,D,J,E = data(1)
K,a,m = 396,4479,6272660
u = 107631485777229402067141184459932727503114031274994405730
P = (a*u+C(a,D),u)
Q = (P[0]+1,a-u)
n = N(P)+H
p,G = m*m+1,(19*971)**2
assert G*G>p and (p-1)%G==0 and pow(3,p-1,p)==1
assert all(prime(l) and gcd(pow(3,(p-1)//l,p)-1,p)==1 for l in (19,971))
z = mul(P,(m,-1))
assert all(x%p==0 for x in z)
P1 = mul(tuple(x//p for x in z),(m,-1))
assert 400*K*K*m>9*p and 400*K*K<11*m
assert N(P1)==N(P) and 64*K*K*seed(P,Q,D)>N(P)

V = (-402027876083264712643034407366633865588710892230259818918608,
      266037776584567469843013189860709784275576321292507200145802)
W = (-402146554373700147282217986704201478331699512354938718599599,
      265858346725171887405552333993217862639834692105443252076883)
S = N(V)
assert S+J==n and 25**80<=n<=9**128
for X,Y,d in [(P1,Q,D),(V,W,E)]:
    q = seed(X,Y,d)
    assert 2**K<=N(X)<2**(K+1) and 64*K*K*q<N(X)<64*K*(K+1)*q

bs = [b for b in range(1,isqrt(128*K*(K+1))+1,2)
      if 128*K*K<b*b+1<128*K*(K+1)]
assert bs==[4481,4483,4485]
for L,ps in [(1,[7,17,11]),(5,[11,7,11])]:
    assert 128*E*(2*isqrt(L*S)+3*L*E+4)*K*(K+1)<S
    for b,p in zip(bs,ps):
        assert pow(F(L,b,J,E,n)%p,(p-1)//2,p)==p-1

d,e = sub(W,V)
assert gcd(d,e)==1
r = pow(d,-1,abs(e))
s = (1-r*d)//e
j = -(r*e-s*d)//(d*d+e*e)
assert min((r+i*e)**2+(s-i*d)**2 for i in (j,j+1))>2**368
~~~
