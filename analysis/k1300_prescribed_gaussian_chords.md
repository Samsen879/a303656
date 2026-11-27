# K1300 exact double-label witness with prescribed Gaussian factors

For A303656, two pairs of actual power labels have simultaneous primitive Gaussian chords at one 1301-bit target. This is a finite exact construction, and does not imply an unbounded family, arbitrary-target coverage, or a solution to the conjecture.

Use \(A=9^L,\ B=25^L,\ L=13\), and the two lower offsets \(H=27A+5B,\ J=3A+125B\). These are the sums of the power labels \((2L+3,2L+1),(2L+1,2L+3)\). The upper endpoints in norm are given by subtracting the offsets \(H-2D=9A+B\) and \(J-2E=A+25B\), with \(D=9A+2B,\ E=A+50B\). The common target \(n=J+2(t^2+c^2)\) has \(c=(E-1)/2\). The two first endpoints have half-norms \(t^2+U\) and \(t^2+V\), with \(U=c^2+(J-H)/2,\ V=U+D\).

For either \(W=U,V\), let \(s=c-64\), \(u=x^2+W-s^2,\ v=2xs,\ G=v-iu,\ Q=u^2+v^2\). If \(2x\) is invertible modulo \(Q\), the congruence
\[
t\equiv(x^2+s^2-W)(2x)^{-1}\pmod Q
\]
implies \(Q\mid t^2+W\). In fact \(r=(x^2+s^2-W)/(2x)\) has \((2x)^2(r^2+W)=(x^2+W-s^2)^2+(2xs)^2\) modulo \(Q\), by direct expansion. Conjugating \(G\) preserves its norm and changes the phase by a switch with \(1-\Re(\overline G/G)=2u^2/Q\). The choices \(x=959077,959662\) respectively give coprime odd 172-bit factor norms, each with its switch strictly in the middle third of the stated \(K=1300\) window. This only forces divisibility. The residual factors' actual Gaussian coordinates from a finite search are included below; their uniform availability is unproved.

The replay verifies all four primitive chords at the exact same target, using integer coordinates. At the first label, conjugating only the prescribed factor in one endpoint maintains both norms and primitivity but makes the displacement fall below the strict window: the original \(q\) is 1274 bits, the switched \(q\) is 1246 bits. The three second chords remain unchanged. This is a same-target control on angle sensitivity.

~~~python
from math import gcd, lcm
from fractions import Fraction as F

L,K = 13,1300
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
U,V = c*c+(J-H)//2,c*c+(J-H)//2+D
t = 3737551353956189175543762561365416039955591893521954070314613719117791102306249655974540759565611052025910215237980395321529641676130457850522529142604796595228741230714566098761395081817276132465
p = (38701248827848540897834612935501853433397093145398215666224966916420852814459227105642836018315983534724989658145210829293750240217162675626589629049033307229481366375440,
     63038466725711821245582302594878773486305924582361002729884072165540511307782222171950003946019509498893851270421470025995194909820388347398248932782419037483550338747618)
r = (38677657419102337938902263929494885618081010290396566272917465929525509028979888859197832588332449224948072388068741589611416375274416355143489376981173837291754984366331,
     63000038841131707201624693022817034591492937755110564361533456255342810331898717140650400478605982534043355077824093376552171742650892296255731958573096569144706734399329)
ms = (14708,14710,14712)

def norm(z): return z[0]**2+z[1]**2
def bar(z): return z[0],-z[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]

n = J+2*(t*t+c*c)
assert n.bit_length()==1301 and 25**224<=n<=9**416
lo,hi = F(1,64*K*(K+1)),F(1,64*K*K)
base = lcm(*(m*m+1 for m in ms))*D*E*U*V
G = []
s = c-64
for W,x in ((U,959077),(V,959662)):
    u,v = x*x+W-s*s,2*x*s
    g = (v,-u)
    Q = norm(g)
    assert Q.bit_length()==172 and Q%2 and gcd(u,v)==gcd(Q,base)==1
    assert (2*lo+hi)/3 < F(2*u*u,Q) < (lo+2*hi)/3
    assert (2*x*t-x*x-s*s+W)%Q==0
    z,rem = divmod(t*t+W,Q)
    assert rem==0 and gcd(z,Q)==1
    base *= Q
    G.append(g)

def seed(P,Q,H,D):
    S = n-H
    assert 2**K<=S<2**(K+1) and norm(P)==S and norm(Q)==S+2*D
    x,y = Q[0]-P[0],Q[1]-P[1]
    q,h = (x*x+y*y)//2,x*P[1]-y*P[0]
    assert x%2 and y%2 and h%2==0 and gcd(x,y)==1
    assert 2*q*S==(D-q)**2+h*h
    return q

def band(S,q): return 64*K*K*q<S<64*K*(K+1)*q

qs = set()
for m in ms:
    v,rem = divmod(t+m*(c+1),m*m+1)
    assert rem==0
    x,y = (m*m-1)*v-m*(c+1),2*m*v-c-1
    q = seed((t-c,t+c),(x-y,x+y),J,E)
    assert band(n-J,q)
    qs.add(q)
assert len(qs)==3

P,Q = mul(G[0],p),mul(bar(G[1]),r)
q = seed(P,Q,H,D)
assert gcd(n-H,D)==gcd(q,D)==1 and band(n-H,q)
Z = mul(bar(P),Q)
assert norm(Z)==(n-H)*(n-H+2*D) and q==n-H+D-Z[0]
qbad = seed(mul(bar(G[0]),p),Q,H,D)
assert 64*K*(K+1)*qbad < n-H
print("verified",K,len(qs),q.bit_length(),qbad.bit_length())
~~~
