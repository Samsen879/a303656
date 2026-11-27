# A Gaussian conjugate-factor angular net

For true endpoint norms S and R=S+2D, the half squared distance at relative angle θ is q(θ)=S+D−sqrt(SR) cos θ. In the ordinary-height regime D≪2^(K/16), S in [2^K,2^(K+1)), the positive angular interval corresponding to S/(64K(K+1))<q<S/(64K²) has width (1+o(1))/(8 sqrt(2) K²).

If the permitted independent conjugate switches have positive angle increments d_i with d_1≤ε, d_(i+1)≤ε+∑_(j≤i)d_j and ∑d_i≥2π, their subset sums have maximum gap ≤ε modulo 2π. Inductively the next increment glues the old subset sums and their translate with a gap at most ε; a segment of length 2π suffices to cover the circle to that gap. This is a sufficient geometric condition for reaching the strict width; a fixed n still has to supply the factors. If D is odd, two true endpoint norms differing by 2D must be 0 and 2 mod 4, giving exactly odd-odd chord increments. Any common odd factor of a chord divides D. So if switches retain the parity and the proven residue separating the endpoints at all primes dividing D, the chord remains primitive.

## A constructed single-label growing chart

Choose minimum J=1 mod 4 with 2^J≥256K². At j=J,J−4,…,1 take the four independent binary switches of factors (2^j+i)^(1,2,4,8), starting with all their conjugates. The angle steps are 2 arctan(2^(−j)) times (1,2,4,8). Within a layer steps double; the transition to the next layer is at most another doubling since arctan(16x)≤16 arctan(x). First step ≤1/(128K²), last four sum to 30 arctan(1/2)>2π. This uses J+3=2 log_2(K)+O(1) blocks of total norm bit size O(log²K). The Gaussian product in a single starting orientation is primitive: conjugate sides of any odd p appearing at two levels j,k would imply 2^(2j)=−1 and 2^(j−k)=−1 modulo p. The former forces v_2(ord_p 2)=2 (j odd), the latter forces v_2(j−k)=1, impossible when levels agree mod 4. Every subset factor γ of the starting product Γ therefore also has primitive coordinates.

Take K=96T, X=2^K, D=9^(T+3)+2·25^(T+4), the actual second-label gap. Select a switch subset close to the middle of the desired angle, let γ=r+is be its starting product, and set up P0=(a+i)u+C with Q=(a−i)u+C+1+ia, C=D−(a²+1)/2. By CRT choose odd a ≈ X^(1/5) so that a+i is invertible modulo Γ and gcd(r−as,D)=1. At an odd p|D the latter forbids at most one class (or none when p|s), since γ is primitive; at primes of Γ the former forbids at most two classes, and these are split primes at least 5. A combined modulus ≤2 D N(Γ)=X^(1/16+o(1)) fits the a-interval. Then Γ|P0 fixes one residue of u modulo N(Γ); the ordinary u-height interval ≈sqrt(X)/a contains it. The base relative angle O(1/a) is negligible compared to the angular window, so the selected switch still hits after replacing P0 by (P0/γ) conjugate(γ). Norms and parity are preserved. The identity Re(γ(Q−P))=r−as excludes every odd common factor, proving primitivity. This makes true growing single-label targets by construction, not hits for a preassigned n or a simultaneous growth theorem for both labels.

The exact replay builds an actual K=48000 positive with 44 available binary blocks. It independently finds the K=692 fixed-target second endpoint by testing a true 8192-element conjugate family without using the successful end coordinates; exactly one hits and is primitive.

```python
from math import gcd, isqrt

def N(z): return z[0]**2+z[1]**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]
def bar(z): return z[0],-z[1]
def sub(z,w): return z[0]-w[0],z[1]-w[1]
def div(z,w):
    v=mul(z,bar(w)); m=N(w)
    assert all(x%m==0 for x in v)
    return tuple(x//m for x in v)
def pw(z,n):
    a=(1,0)
    for _ in range(n): a=mul(a,z)
    return a
def cop(n,x):
    while (g:=gcd(n,x))>1: n//=g
    return n
def crt(a,m,b,n): return a+m*((b-a)*pow(m,-1,n)%n)
def first(lo,r,m): return lo+(r-lo)%m
def seed(P,Q,S,D,K):
    x,y=sub(Q,P); q=(x*x+y*y)//2
    h=P[0]*Q[1]-P[1]*Q[0]
    assert N(P)==S and N(Q)==S+2*D and gcd(x,y)==1
    assert x%2 and y%2 and h%2==0 and 2*q*S==(D-q)**2+h*h
    assert 2**K<=S<2**(K+1) and 64*K*K*q<S<64*K*(K+1)*q

T=500; K=96*T; X=1<<K
A,B=9**(T+3),25**(T+3); D=A+50*B
J=1
while 2**J<256*K*K: J+=4
blocks=[(j,pw((1<<j,1),e)) for j in range(J,0,-4) for e in (1,2,4,8)]
G,Z=(1,0),(1,0)
den=128*K*K*(K+1); num=den-(2*K+1)
for j,g in reversed(blocks):
    G=mul(G,bar(g))
    if 2**j<=K: continue
    z=mul(Z,g)
    if den*(z[0]**2-z[1]**2)>=num*N(z): Z=z
gamma=bar(Z); r,s=gamma; M=N(G)
assert len(blocks)==44 and M.bit_length()==6935
assert gcd(*G)==gcd(r,s)==1
i=-G[0]*pow(G[1],-1,M)%M
assert (i*i+1)%M==0
M0=cop(M,r+s*i-s)
a0=crt(1-i,M0,2-i,M//M0)
D0=cop(D,M*s)
a1=crt(a0,M,(r-1)*pow(s,-1,D0)%D0,D0)
a=first(1<<(K//5),crt(a1,M*D0,1,2),2*M*D0)
assert gcd(a+i,M)==gcd(r-a*s,D)==1
C=D-(a*a+1)//2
u=first(6*isqrt(X)//(5*a),-C*pow(a+i,-1,M)%M,M)
P0=(a*u+C,u); Q=(P0[0]+1,a-u)
div(P0,G)
P=mul(div(P0,gamma),Z)
S=N(P0); n=S+3*A+125*B
assert 25**(16*(T+4))<=n<=9**(32*(T+3))
assert 64*K*(K+1)*N(sub(Q,P0))<=2*S
seed(P,Q,S,D,K)

K,a=692,7829
A,B=9**8,25**8
D,E=9*A+2*B,A+50*B
u=21971192886866971970018735123723528582244322574908256486687716817273768616531491076289938385186208385
x=a*u+D-(a*a+1)//2
g=(10464643495,548)
P1=mul(div((x,u),g),bar(g)); Q1=(x+1,a-u)
n=x*x+u*u+27*A+5*B
assert 25**144<=n<=9**256
seed(P1,Q1,n-27*A-5*B,D,K)
gs,gr=(19,21),(20,48)
div(P1,gs); div(Q1,gr)
S,R=n-3*A-125*B,n-A-25*B
p=(3912679469294950753411730218583498993597338909061349550737332549031640099920579113695453098199297633425,
   4645865803264816085481595569551027930441066410501978924539923428513836955285867786591042592917116594922)
P=mul(gs,p)
assert N(P)==S and 128*K*(K+1)*E*E<=S*S
def gsquare(p):
    return next((x,y) for x in range(1,isqrt(p))
                if (y:=isqrt(p-x*x))**2==p-x*x)
factors=[gsquare(p) for p in (5,29,37,53,89,113,157,293,313,337)]
factors.append((
    694163754322795908866012039864594108260579446681679034982999785784132726165355329057952536556,
    553839529941448795866389225517834213287473048140380498618244783830086697778977886984424957805))
Q=[gr]
for f in factors:
    Q=[mul(q,h) for q in Q for h in (f,bar(f))]
Q={mul(q,w) for q in Q for w in ((1,0),(0,1),(-1,0),(0,-1))}
assert len(Q)==8192 and all(N(q)==R for q in Q)
hits=[q for q in Q if 32*K*K*N(sub(q,P))<S<
                      32*K*(K+1)*N(sub(q,P))]
assert len(hits)==1
seed(P,hits[0],S,E,K)
print("PASS")
```
