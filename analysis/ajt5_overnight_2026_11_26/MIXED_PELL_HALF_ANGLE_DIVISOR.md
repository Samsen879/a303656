# An integral half-angle divisor for mixed Pell allocation changes

Use two distinct actual labels in the t=8 band, ordered by U_i=2A_i+3B_i, with A_i=9^r_i≤B_i=25^s_i and D_i=A_i+2B_i. Write e=U₂−U₁, b=D₁+D₂, g=D₂−D₁, W=ebg. Ordering by U also orders D and U−D, since distinct B have a factor 25 gap and A≤B, and when B is the same all three increase with A. Thus e>g>0, b>g, and e≠b: equality e=b would give (A₂+B₂)=(3A₁+5B₁), which is impossible using [B,2B], [5B,8B], and the same gap. This nondegeneracy is separate from the same-label case.

Fix an oriented difference Δ and one sign of h. Two integral target points satisfy x²−dy²=R, where d=2j>0, R=(d+e²)(d+b²)(d+g²), x=d(2n−U₁−U₂)−W, y=2h. Let s=n′−n, h_+=h+h′, h_−=h′−h, and x_+=(x+x′)/2. Subtract the two Pell equations to get s x_+=h_+ h_−. Put k=gcd(|s|,|h_+|), a=h_+/k, c=s/k. Since coprime a,c, one has x_+=av and h_−=cv for an integer v. The equations factor exactly:

~~~text
x′+y′√d = (a+c√d)(v+k√d)
x +y √d = (a−c√d)(v+k√d)
Λ = a²−dc²,  R = Λ(v²−dk²),  av ≡ −W (mod d).
~~~

In the large shells X≤j≪X²/(log X)^4, same-sign h and x≈2dn give Λk²=h_+²−ds²≈dX², so Λ is a positive divisor of R. It need not be claimed a proper divisor. A fixed a with |a|/gcd(a,d)>2X gives at most one integer n+n′ at ordinary height, since the v congruence has period d/gcd(a,d).

At a good odd split p outside d, coprimality of a,c means the two components of a+c√d cannot both be divisible by p. Thus v_p(Λ) is exactly the absolute allocation change. Unramified inert good primes give no allocation change. Fixing bad allocations and the first-factor pins, the good part of Λ is m=m_b m_g from the remaining two factors. Write G_m=gcd(d,R/m). The half-trace of the ratio has V−1=2dc²/Λ. The earlier relation d/G_m | 2m(V−1) and gcd(Λ,c)=1 imply Λ | 4mG_m. In particular m_b m_g G_m k²≫dX². Since m_b m_g≪d², if gcd(d,R) is bounded this rules out mixed changes with k≪X/√d, even for target pairs far apart. It does not bound how often large k can occur; it also does not assert the full joint shell count.

The exact replay constructs a genuine pair of numerical seeds at one integer (the 563-bit deficit control), and a second rational Pell point that passes the real window and flips allocations at 509 and 281 in distinct Gram factors. The rational target moves by between one and two, but its reduced half-angle Λ exceeds R and therefore cannot be an integer divisor as required. This checks the distinction between local/real feasibility and an actual second integer target.

~~~python
from fractions import Fraction as F
from math import isqrt, prod

K, X = 301, 1 << 301
a, u = 3411, 828928256542149812983540043167074401999330
x = a*u + 9**3+2*25**4-(a*a+1)//2
n = x*x+u*u+3*9**3+5*25**4

def N(z): return z[0]**2+z[1]**2
def bar(z): return z[0],-z[1]
def sub(z,w): return z[0]-w[0],z[1]-w[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]

def cert(r,s,P,Q):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    f,g = sub(P,Q)
    z = mul(bar(P),Q)
    if z[1]<0: P,Q,z = bar(P),bar(Q),bar(z)
    assert f%2 and g%2 and z[1]%2==0
    q = ((f+g)//2)**2+((f-g)//2)**2
    assert X<=n<2*X and A<=B and B**16<=n<=A**32
    assert N(P)==S and N(Q)==S+2*D and q%2 and z[0]==n-U-q
    assert 2*q*S==(D-q)**2+z[1]**2 and X<=S<2*X
    assert 64*K*K*q<S<64*K*(K+1)*q
    return U,D,P,Q,z,q

P = (2698115859994096559547095681235316801185026742,
     845447996369883676206443633193679268818732588)
Q = (2698611898993095184751390925053140197778235579,
     843863334391543961275303183778626961636017633)
U,D,a1,c1,z,q1 = cert(4,3,P,Q)
V,E,a2,c2,w,q2 = cert(3,4,(x,u),(x+1,a-u))
assert q1!=q2
e,b,g = V-U,D+E,E-D
W = e*b*g
L = (n-U)*(n-V)-(D*D+E*E)//2
dot,h = mul(bar(z),w)
j,delta = L-dot,sub(z,w)
d,C = 2*j,N(delta)
xx,yy = d*(2*n-U-V)-W,2*h
R = prod(d+l*l for l in (e,b,g))
Cb = N(sub(mul(a1,bar(a2)),mul(c1,bar(c2))))
Cg = N(sub(mul(a1,c2),mul(a2,c1)))
assert j**10>X**18 and 0<h*h*K**4<N(z)*N(w)
assert [C,Cb,Cg]==[d+l*l for l in (e,b,g)]
assert xx*xx-d*yy*yy==R

p,q = 509,281
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)
for l,F0 in ((p,Cb),(q,Cg)):
    assert all(l%v for v in range(2,isqrt(l)+1))
    assert l%4==1 and F0%l==0 and R%l**2 and (bad*xx*yy)%l

M,T = (30*d*C*(R//(p*q)))**3,(p*q)**3
k0 = 2*xx*yy**2//(3*R)
k = k0+(-1-pow(M,-1,T)-k0)%T
t = 1+F(M,1+M*k)
Y = yy+2*yy*(1-t)*xx**2/(t*t*d*yy**2-xx**2)
Z = xx+t*F(d*yy,xx)*(Y-yy)
H = (Z+W)/d
nn = (H+U+V)/2
s = nn-n
assert Z*Z-d*Y*Y==R and 1<s<2 and nn.denominator>1 and X<=nn<2*X
zz = tuple(v/C for v in mul(delta,((e*H+b*g+C)/2,Y/2)))
ww = sub(zz,delta)
for r,k,U0,D0,z0 in ((4,3,U,D,zz),(3,4,V,E,ww)):
    S,Q0 = nn-U0-D0,nn-U0-z0[0]
    assert 25**(16*k)<=nn<=9**(32*r) and X<=S<2*X
    assert z0[1]>0 and N(z0)==S*(S+2*D0)
    assert 2*Q0*S==(D0-Q0)**2+z0[1]**2 and 64*K*K*Q0<S<64*K*(K+1)*Q0

def red(v,m):
    v=F(v)
    return v.numerator*pow(v.denominator,-1,m)%m

assert red(Z-xx,T)==red(Y+yy,T)==0
for l in (p,q):
    i=next(i for i in range(l) if (i*i-d)%l==0)
    assert [red(Z+i*Y,l)==0,red(Z-i*Y,l)==0]==[
        (xx-i*yy)%l==0,(xx+i*yy)%l==0]
assert all(red(v,30*C)==0 for v in (nn-n,*sub(zz,z),*sub(ww,w)))

f = F(s,(Y+yy)/2)
assert f==F(Y-yy,Z+xx)
a,c = f.denominator,f.numerator
Lam = a*a-d*c*c
assert Lam*(((Z+xx)/(2*a))**2-d*(s/c)**2)==R
assert Lam>R and 0<N(sub(zz,z))-s*s<1
print("Native 563-bit shell and rational mixed switches verified")
~~~
