# Cross-label slope bounds are local, not a whole-window lock

Use actual labels with A=9^(T+3), B=25^(T+3), H1=27A+5B, H2=3A+125B, D1=9A+2B, D2=A+50B. For fixed n set S_i=n−H_i and U_i=H_i−D_i. Then U2−U1=e=72B−16A and H2−H1=120B−24A. On their respective critical windows α_i(q)=sqrt(2(n−U_i)q−q²−D_i²)/q. Their endpoints differ by O(D2/K²) while the individual windows have width of order S_i/K³. At the same real q they satisfy α_2(q)²−α_1(q)²=−2e/q−(D2²−D1²)/q². That comparison is only at the same q.

Suppose the first proved chord supplies a reduced direction slope p/s and the second window provides α_2 in [a_−,a_+], 1≤k≤B_2, |l−kα_2|≤ε. Then m=sl−pk is integral with
```
s(B_2 min(0,a_−−p/s)−ε) ≤ m ≤ s(B_2 max(0,a_+−p/s)+ε),
k = −m p^(−1) mod s.
```
This follows from adding and subtracting kα_2. In the short q_1±64 window of the K=396 anchor, only m in {−1,0,1} require testing. One direction pair survives geometric constraints and none passes the even-H norm residue. The existing true second chord elsewhere and its disjoint negative subwindow are replayed too.

On the whole second window the phase range has constant-order width. In a fixed interior phase interval, reduced odd–odd slopes with denominator a sufficiently small fixed proportion of sqrt(Q_*/D2) contribute order Q_*/D2 distinct slopes. Each has a real q at exactly that phase and within the direction radius, with the first integer chord kept fixed. This lower bound concerns geometric candidates only and does not rule out an arithmetic reduction exploiting integrality.

At K=500, the replay constructs one actual first chord and **two actual primitive second chords at that same target**. The second q values differ by over three quarters of the full critical window and their α values differ by more than four. Thus locking the second search to a narrow interval around that first anchor can miss a true second chord. A rule that only needs to find one second chord is a separate question. No arbitrary-target bridge is asserted.

## Exact replay

```python
from fractions import Fraction as F
from math import gcd, isqrt

def N(p): return p[0]**2+p[1]**2
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def seed(P,Q,K,S,D):
    d,e=Q[0]-P[0],Q[1]-P[1]
    q=(d*d+e*e)//2; H=abs(det(P,Q))
    assert d%2 and e%2 and gcd(d,e)==1
    assert norm_ok(P,Q,S,D) and 2*q*S==(D-q)**2+H*H
    assert 2**K<=S<2**(K+1) and 64*K*K*q<S<64*K*(K+1)*q
    return q,H
def norm_ok(P,Q,S,D): return N(P)==S and N(Q)==S+2*D

def anchor(T,K,a,m,u):
    A,B=9**(T+3),25**(T+3)
    D,E=9*A+2*B,A+50*B
    x=a*u+D-(a*a+1)//2; p=m*m+1
    assert (m*x+u)%p==(m*u-x)%p==0
    P=(((m*m-1)*x+2*m*u)//p,((m*m-1)*u-2*m*x)//p)
    Q=(x+1,a-u)
    S=x*x+u*u; n=S+27*A+5*B
    assert 25**(16*(T+4))<=n<=9**(32*(T+3))
    assert 64*K*K*(1+(a-2*u)**2)>2*S
    assert 400*K*K*m>9*p and 400*K*K<11*m
    q,H=seed(P,Q,K,S,D)
    return P,Q,q,H,n-3*A-125*B,D,E,72*B-16*A

K=396
P,Q,q1,H1,S,D,E,_=anchor(1,K,4479,6272660,
    107631485777229402067141184459932727503114031274994405730)
V=(-402027876083264712643034407366633865588710892230259818918608,
    266037776584567469843013189860709784275576321292507200145802)
W=(-402146554373700147282217986704201478331699512354938718599599,
    265858346725171887405552333993217862639834692105443252076883)
q0,H0=seed(V,W,K,S,E)
cap=isqrt(4*E*E//3)
d,e=W[0]-V[0],W[1]-V[1]
h=914*d+627*e
b=det((914,627),(V[0]+W[0],V[1]+W[1]))
assert h%E==b%E==0 and (abs(h)//E).bit_length()==173
assert cap*(914**2+627**2)<E*E

def f(q): return 2*(S+E)*q-q*q-E*E
R=262144
assert 64*K*K*(q0+3*R)<S<64*K*(K+1)*(q0-R)
for a,b,want in [(q0-R,q0+R,[q0]),(q0+R+1,q0+3*R,[])]:
    assert [q for q in range(a|1,b+1,2) if (v:=f(q))==isqrt(v)**2]==want

g=(41,-339); d,e=Q[0]-P[0],Q[1]-P[1]
h=g[0]*d+g[1]*e
b=det(g,(P[0]+Q[0],P[1]+Q[1]))
assert h%D==b%D==0 and 3*N(g)**2<=4*D*D
r=F(b if det((d,e),P)>0 else -b,h)
a,b=q1-64,q1+64
assert 64*K*K*b<S<64*K*(K+1)*a
B=isqrt(2*cap*b//E**2)
lo,hi=F(isqrt(f(b)),b),F(isqrt(f(a))+1,a)
eps=F(isqrt(2*cap*a)+1,a)
p,s=r.numerator,r.denominator
L=s*(B*min(0,lo-r)-eps); U=s*(B*max(0,hi-r)+eps)
assert (-(-L.numerator//L.denominator),U.numerator//U.denominator)==(-1,1)
pairs=[]
for j in (-1,0,1):
    for k in range((-j*pow(p,-1,s))%s or s,B+1,s):
        l=(j+p*k)//s
        if (k-l)%2==0 and gcd((k+l)//2,l)==1 and k*lo-eps<=l<=k*hi+eps:
            pairs.append((j,k,l))
assert [j for j,k,l in pairs]==[-1]
_,k,l=pairs[0]
assert not any(1<=(k*k*(S+E)+(l*l-k*k)//2*q)%(2*k*l)<=cap
               for q in range(a,b+1,2))

K=500
_,_,q1,H1,S,_,E,e=anchor(2,K,5655,10000044,
    383926026185211066579832133483647870363756550889720823037289401350858274)
q2,H2=seed(
    (-555665752269218079463250868810112072466437126704976976051563694667035033416,
     -2098789702591625386933144891775165171678475697642987232074809988870967114790),
    (-554924397528368768078439618419470379730429580287588640477205764547695341095,
     -2098985840108821775405675712994120271255707649544548238849623031313911542723),
    K,S,E)
q3,H3=seed(
    (2132579438804802673961666795126772462633637449354975956636769958162707934584,
     -407170211504417729213745196662407972442695682833421606773145402692580706010),
    (2132723235494580271795586868439140799950913745689895290598246417011103047973,
     -406416344074753569627800801752922313316974900757148762535629554468743241745),
    K,S,E)
assert 4*(q3-q2)*64*K*K*(K+1)>3*S
assert F(H2,q2)-F(H3,q3)>4 and F(H2,q2)-F(H1,q1)>4
for q,H in ((q2,H2),(q3,H3)):
    d=(e+q-q1)**2+(H-H1)**2-e*e
    assert d%2==0 and (d//2)**5>2**(9*K)
print("PASS")
```
