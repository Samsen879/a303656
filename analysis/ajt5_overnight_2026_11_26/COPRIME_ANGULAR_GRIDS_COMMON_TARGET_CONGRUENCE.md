# Two coprime Gaussian angular grids can share a local target

Put A=9^(T+3), B=25^(T+3) and consider the actual four offsets 27A+5B, 9A+B, 3A+125B, A+25B. They are all distinct modulo 5. Thus the earlier grid with all factors sharing odd exponent j in 2^j+i, whose norms are divisible by 5, can be placed at only one endpoint of any fixed n.

Two grids with coprime integer norms are available. For f=0,1 choose levels j=2^f(2t+1) and factors 2^j+(-1)^t i. Any odd prime in their norms has v_2(ord_p 2)=2+f, making the two grids coprime. Within a grid the alternating sign keeps repeated split factors on the same Gaussian side, since 2^(j-k) is −1 exactly when the difference of t's is odd. Repeating each level in binary blocks fills the angle gaps as in the earlier angular-net construction. This supplies local angle flexibility, without transferring it to actual unknown endpoint coordinates.

For a horizontal chord write a=v+2u. Modulo a grid norm M where v²=−1, the first coordinate is D−vu and the squared norm becomes D²−2Dvu modulo M. If z represents i modulo the primitive grid product, use v=−z and solve for the affiliated chord's u so the actual Gaussian residue is zero. For the other chord, use v=z and solve the linear norm residue for a common target, when gcd(D,M)=1. At K=48000 the replay checks grids with 2675 and 7262-bit coprime norms, full CRT modulo 16M1M2 and an ordinary-height common **residue target**. This is not a common integer norm construction.

The remaining exact condition can be isolated. For fixed odd slopes a_i define e_i=(a_i²+1)/2, c_i=(D_i−e_i)/2, v_i=e_i u_i+a_i c_i, and ℰ=e_1 e_2. Then e_i(n−H_i)=2(v_i²+c_i²) for the integer horizontal model. Taking x=e_2v_1,y=v_2 gives
```
x²−ℰ y²=e_2[ℰ(H_2−H_1)/2+e_1 c_2²−e_2 c_1²].
```
If the grids require u_i=t_i modulo M_i, the exact side conditions are x=e_2(a_1c_1+e_1t_1) modulo ℰ M1 and y=a_2c_2+e_2t_2 modulo e_2 M2. With these congruences the equation is equivalent to reconstructing integer horizontal endpoints at one n, before checking heights and switches. Neither CRT solvability nor this rearrangement solves the integer equation. The replay also contains the previously certified genuine K692 double chord for comparison.

```python
from math import gcd

def N(z): return z[0]**2+z[1]**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def bar(z): return z[0],-z[1]
def div(z,w):
    t=mul(z,bar(w)); m=N(w)
    assert all(x%m==0 for x in t)
    return tuple(x//m for x in t)
def pw(z,k):
    x=(1,0)
    while k:
        if k%2: x=mul(x,z)
        z=mul(z,z); k//=2
    return x
def crt(a,m,b,n): return a+m*((b-a)*pow(m,-1,n)%n)
def native(T):
    A,B=9**(T+3),25**(T+3)
    return (9*A+2*B,A+50*B),(27*A+5*B,3*A+125*B)
def target(a,u,d,h):
    return (a*u+d-(a*a+1)//2)**2+u*u+h
def grid(K,f):
    j0=1<<f; step=2*j0; j=j0
    while 2**j<256*K*K: j+=step
    G=(1,0)
    for k in range(j,0,-step):
        sign=(-1)**((k//j0-1)//2)
        e=15 if k==1 else (1<<step)-1
        G=mul(G,pw((1<<k,sign),e))
    assert gcd(*G)==1
    return G

T=500; K=96*T
D,H=native(T); G=[grid(K,f) for f in (0,1)]
M=list(map(N,G))
assert [m.bit_length() for m in M]==[2675,7262]
assert gcd(*M)==1 and all(gcd(m,d)==1 for m in M for d in D)
assert M[0]%5==0 and M[1]%5!=0

local=[]
for i,((r,s),m) in enumerate(zip(G,M)):
    z=-r*pow(s,-1,m)%m
    assert (z*z+1)%m==0
    u=[0,0]; a=[0,0]
    u[i]=-D[i]*pow(2*z,-1,m)%m
    u[1-i]=(D[1-i]**2-H[i]+H[1-i])*pow(2*D[1-i]*z,-1,m)%m
    a[i]=2*u[i]-z; a[1-i]=2*u[1-i]+z
    local.append((a,u))

W=M[0]*M[1]
def merge(j,i,v):
    return crt(crt(local[0][j][i],M[0],local[1][j][i],M[1]),W,v,16)
a=[merge(0,i,3) for i in (0,1)]
u=[merge(1,i,1) for i in (0,1)]
lo=3*2**(K-1)
n=lo+(target(a[0],u[0],D[0],H[0])-lo)%(16*W)
assert 25**(16*(T+4))<=n<=9**(32*(T+3))
for i in (0,1):
    assert 2**K<=n-H[i]<2**(K+1)
    assert (target(a[i],u[i],D[i],H[i])-n)%(16*W)==0
    div((a[i]*u[i]+D[i]-(a[i]**2+1)//2,u[i]),G[i])

for T in (0,1):
    D,H=native(T)
    A=9**(T+3)
    assert len({2*A%5,4*A%5,3*A%5,A%5})==4
    d=H[1]-H[0]
    assert (-2*d-(D[1]-1)**2)%5==(2*d-(D[0]-1)**2)%5==3
    assert (2*(4*A-H[1])-(D[1]-1)**2)%5==(4 if T==0 else 2)

K=692; D,H=native(5); a=7829
u=21971192886866971970018735123723528582244322574908256486687716817273768616531491076289938385186208385
x=a*u+D[0]-(a*a+1)//2
g=(10464643495,548); V=(x,u); Q=(x+1,a-u)
P=mul(div(V,g),bar(g)); n=N(V)+H[0]
def seed(P,Q,H,D):
    d,e=Q[0]-P[0],Q[1]-P[1]
    S=N(P); q=(d*d+e*e)//2
    assert d%2 and e%2 and gcd(d,e)==1
    assert (P[0]*Q[1]-P[1]*Q[0])%2==0
    assert S+H==n and N(Q)==S+2*D
    assert 2**K<=S<2**(K+1) and 64*K*K*q<S<64*K*(K+1)*q
assert 25**144<=n<=9**256 and N(P)==N(V)
seed(P,Q,H[0],D[0])
r=(3912679469294950753411730218583498993597338909061349550737332549031640099920579113695453098199297633425,
   4645865803264816085481595569551027930441066410501978924539923428513836955285867786591042592917116594922)
s=(2854186525561869658626979365433357281388535358342838614713375126251636208255746967547984862778133530992,
   1672134630569446518371818448424744811960147784067280159655062908073992262506249946321344576078243929351)
div(P,(19,21)); div(Q,(20,48))
seed(mul((19,21),r),mul((20,48),s),H[1],D[1])
```
