# True endpoint norms do not guarantee a critical-band chord

For odd D, if S and R=S+2D are both Gaussian norms, their residues modulo 4 are 0 and 2 in some order. For any Gaussian P,Q with those norms, Q−P has odd coordinates. Thus q=N(Q−P)/2 is automatically an odd Gaussian norm and z=conj(P)Q gives the actual band equation. Conversely any numerical seed with 2qS=N(D−q+2iw) factors: allocate prime powers in the Gaussian integer D−q+2iw to obtain a factor δ of norm 2q, set conj(P)=(D−q+2iw)/δ and Q=P+δ. This proves that exhausting endpoint representations exhausts the seed possibilities. The band is an angular requirement; q=S+D−sqrt(SR)cos θ gives allowed width asymptotic to 1/(8√2 K²). In particular, if one actual endpoint's angles modulo π/2 have maximal gap smaller than the exact band width, it can hit that band with the other endpoint fixed. This does not ensure prescribed congruences on a hit.

## An exact same-target two-norm counterexample

In the actual (4,3),(3,4) labels, preserve the true chord anchor for the second label and shift its parameter by 41099101632 as in the replay. On the first label S=4p,R=2q, where p,q are positive primes ≡1 mod 4. Both exact norms are supplied. Independent recursion verifies the two primality assertions using exact Pocklington checks and a few affine elliptic-curve certificates: when a certified prime r exceeds (n^(1/4)+1)² and the reduced finite point has order r at every prime divisor of n, Hasse's bound excludes a divisor ≤√n. All inverse operations are checked over the residue ring. The replay requires Python's standard library only, not a probable-prime assumption.

Gaussian unique factorization gives one representation orbit up to independent sign changes and coordinate swaps for each endpoint. Sorting the absolute coordinates decreasingly maximizes their dot product, so the exact observed chord is globally minimal. Here 4810 q_min≤S<4811 q_min, while the window allows q<S/5760000. Thus no first-label integer band seed exists. This is a counterexample with both endpoint norms genuinely established, not merely locally permitted.

The same fixed anchor still allows a strict real-band completion with a verified rank-three mod panel. Aligning d modulo fixed prime powers with an actual out-of-band chord gives separately integral local completions at 7, 11, 19, 109 and 71089: for its known integer determinant h₀, impose d congruent modulo ℓ^m where m>2v_ℓ(h₀) and m−v_ℓ(h₀)>v_ℓ(N(z₂)). Hensel gives the appropriate numerator congruence for Gaussian division. The real completion and the local completions do not provide an integral point at the exact real angle.

A separate unbounded-height construction makes the endpoint norms pass any prescribed fixed finite panel but forces an odd inert valuation outside it. With the fixed anchor polynomial and base Δ=2445968927865, v₃(Δ)=1 and Δ≡1 mod4. Pick even x divisible by 3, congruent to 1 modulo Δ/3, and divisible by all panel inert primes coprime to Δ (and the other fixed primes to exclude). Then (x²+Δ)/3 is 3 mod4, so it has an odd-exponent inert prime ℓ outside the excluded set, not dividing x. Freeze true label residues modulo ℓ², set a=0 and 2u=x modulo ℓ, and avoid the single zero lift to enforce v_ℓ(S)=1. At inert panel primes ≥7 the two actual quadratic ends have at most four forbidden unit roots altogether. These are all fixed CRT choices, carried by the growing first-anchor parameters. This latter result is local compatibility only, not an unbounded series of the exact two-norm counterexample.

~~~python
from fractions import Fraction as F
from math import isqrt,gcd,prod
from functools import cache
import json

caps=json.loads(r'''{"22734859758697467720028644778423": ["P", [[96590279, 1, 2], [11176493, 1, 2], [5660243, 1, 2]]], "178551476837787447251412340749391879787293": ["P", [[22734859758697467720028644778423, 1, 2]]], "114478040022262436923924511949652755228306040315080566241882053": ["E", [98575461475456095600807551264210534289561704246655328413464481, 16955908611679023877152223069294623824442898680459871642737255, 641148659477427888592, 178551476837787447251412340749391879787293, 2, 16770005912939087145461240321247471487372344466958370717382980]], "13279452642582442683175243386159939726728789105965906468151650153": ["E", [7, 0, 116, 114478040022262436923924511949652755228306040315080566241882053, 1, 1458144983886330400913503475947008411233006926812360351902840313]], "132794526425824426831752433861599382047002730549598210502512318453": ["E", [5, 0, 10, 13279452642582442683175243386159939726728789105965906468151650153, 4, 26105396377839715542180155082117346181856599755295112053876828878]], "644633485095067621780415015950675933806533670854900610613060280646102633129857734409117281": ["P", [[132794526425824426831752433861599382047002730549598210502512318453, 1, 2]]]}''')
caps.update(json.loads(r'''{"824048677366887694854487": ["P", [[8443996186589, 1, 2]]], "743965978803018814893138244367": ["P", [[824048677366887694854487, 1, 2]]], "944922640450907990866699191046731435484879": ["E", [809933691815063992171456449468626944701307, 674944743179219993476213707890522453917735, 1270115391528, 743965978803018814893138244367, 2, 398360483645520745265144658010139659392613]], "220828421073377197465547600947621136472816222301": ["P", [[944922640450907990866699191046731435484879, 1, 2]]], "189470785280957635425439841613058935093676318734259": ["P", [[220828421073377197465547600947621136472816222301, 1, 2]]], "535986382053447886837888240144704348920611579051099238741561711": ["P", [[189470785280957635425439841613058935093676318734259, 1, 2]]], "2669057222229473132170365936328309614831362042200678101212448225905374893337067": ["E", [409365851916765916713198795017957967725604439151358786275829801668155491149376, 272910567944510611142132530011971978483736292767572524183886534445436994099584, 4979710887436909, 535986382053447886837888240144704348920611579051099238741561711, 1, 728284527902886048719204830384595174200796039782664644384240326293587079669908]], "1289266970190135243560830031901351867613067341709801221226120561292205266259715468818272373": ["E", [823309845725541687788999235507434454234885924264057112297003537434175097858695816856046504, 548873230483694458525999490338289636156590616176038074864669024956116731905797211237364336, 483042086716, 2669057222229473132170365936328309614831362042200678101212448225905374893337067, 1, 168279359833110038007420085022988227795425155866376059146366684799155996292551880351800975]]}'''))

def add(P,Q,a,n):
    if P is None: return Q
    if Q is None: return P
    x,y=P; u,v=Q
    if x==u and (y+v)%n==0: return None
    if x==u:
        # On the same prime-power ring, a nonzero y+v and inverse 2y imply equal points here.
        assert y==v
        r=(3*x*x+a)*pow(2*y,-1,n)%n
    else: r=(v-y)*pow(u-x,-1,n)%n
    w=(r*r-x-u)%n
    return w,(r*(x-w)-y)%n

def mul(m,P,a,n):
    Q=None
    for bit in bin(m)[2:]:
        Q=add(Q,Q,a,n)
        if bit=='1': Q=add(Q,P,a,n)
    return Q

@cache
def prime(n):
    if str(n) not in caps:
        assert 1<n<10**14
        assert n==2 or n%2 and all(n%d for d in range(3,isqrt(n)+1,2))
        return
    tag,v=caps[str(n)]
    if tag=='P':
        d=prod(p**e for p,e,a in v)
        assert d>isqrt(n) and (n-1)%d==0
        for p,e,a in v:
            prime(p)
            assert pow(a,n-1,n)==1 and gcd(pow(a,(n-1)//p,n)-1,n)==1
    else:
        a,b,t,p,x,y=v
        prime(p)
        assert p>(isqrt(isqrt(n))+2)**2 and gcd(4*a**3+27*b*b,n)==1
        assert (y*y-x*x*x-a*x-b)%n==0
        Q=mul(t,(x,y),a,n)
        assert Q is not None and mul(p,Q,a,n) is None

K=300; X=1<<K; a=3395; A=9**3; B=25**3
U,V,D,E=18*A+3*B,2*A+75*B,9*A+2*B,A+50*B
e,b,g=V-U,E+D,E-D
W=e*b*g
u0=472984194841387909896403492694189266281840
def nm(z): return z[0]**2+z[1]**2
def diff(x,y): return x[0]-y[0],x[1]-y[1]
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def band(S,q):return 64*K*K*q<S<64*K*(K+1)*q
def seed(P,Q,S,D):
    q=nm(diff(P,Q))//2; z=(dot(P,Q),abs(cross(P,Q)))
    assert nm(P)==S and nm(Q)==S+2*D and q%2 and z[1]%2==0
    assert 2*q*S==(D-q)**2+z[1]**2
    return q,z
def anchor(u):
    x=a*u+E-(a*a+1)//2
    S=x*x+u*u; n=S+V+E
    q,z=seed((x,u),(x+1,a-u),S,E)
    assert 25**64<=n<=9**96 and X<=S<2*X and X<=n<2*X and band(S,q)
    return n,z
n,z=anchor(u0)
P=(1238240656117444633368032107716581205155788446,1022396213763583296740059539842408420297582288)
Q=(1237638945231334085263186942097216682418805929,1023124519121177798984074135516404730073639771)
q,z1=seed(P,Q,n-U-D,D)
assert band(n-U-D,q)
d0=nm(diff(z1,z))-e*e

n,z=anchor(u0+41099101632); S=n-U-D; R=S+2*D
p,q=S//4,R//2
assert S==4*p and R==2*q and p%4==q%4==1 and (S%7,R%7)==(4,5)
prime(p); prime(q)
P0=(795427079358195677328522559435812965515974020,109221090082265238287023401744804745259577609)
Q0=(918451307774422669862501814152767425055669367,667618278238087162806172796406221732126885178)
assert nm(P0)==p and nm(Q0)==q
P=tuple(sorted((2*P0[0],2*P0[1]),reverse=True))
Q=tuple(sorted((abs(Q0[0]+Q0[1]),abs(Q0[0]-Q0[1])),reverse=True))
qm,z1=seed(P,Q,S,D)
assert 4810*qm<=S<4811*qm and not band(S,qm)

pp=71089
prime(pp)
def v(y,p):
    assert y
    t=0
    while y%p==0:y//=p;t+=1
    return t
assert all(x%pp==0 for x in z) and v(nm(z),pp)==2
rows=(181,1229,1383784813,493076497,332378247127)
marks=(277,8377,268293089)
M=2**6*3**3*5**3*prod(rows)*prod(p*p for p in marks)
dout=nm(diff(z1,z))-e*e
m=7**2*11**4*19**2*109**2*pp**4; s=M*W//7
assert M*W%7==0
d=d0+s*((dout-d0)*pow(s,-1,m)%m)
assert d%2==0 and (d//2)**5>X**9 and gcd(d,W*W)==800
assert all(d%l==0 and W%l for l in rows)
assert [v(d+t*t,p) for t,p in zip((b,b,g),marks)]==[1,1,1]
bad=2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)
for p in rows+marks:prime(p)
assert all(p%4==1 and bad%p for p in marks)
def cd(t):return sum((pow(t,(p-1)//2,p)==p-1)<<i for i,p in enumerate(rows))
assert list(map(cd,(2,5,*marks)))==[7,28,1,15,17]

c=(S*R+nm(z)-e*e-d)//2; F0=S*R*nm(z)-c*c
h0=cross(z1,z)
assert (F0-h0*h0)%m==0
for p in (7,11,19,109,pp):
    assert v(m,p)>2*v(h0,p) and v(m,p)-v(h0,p)>v(nm(z),p)
T=1<<64
h=isqrt(F0*T*T)
for hh in (F(h,T),F(h+1,T)):
    x,y=(c*z[0]+hh*z[1])/nm(z),(c*z[1]-hh*z[0])/nm(z)
    assert y>0 and band(S,n-U-x)
print("Exact endpoint prime certificates, minimal chord and strict real/local contrast passed.")

~~~
