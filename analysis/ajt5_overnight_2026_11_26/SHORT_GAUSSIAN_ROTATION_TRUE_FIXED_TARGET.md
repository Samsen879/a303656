# A genuinely short Gaussian rotation enters the band while preserving the anchor

Fix n, the second label's true seed z₂, and the first label's endpoint Q. Factor its other endpoint as P₀=C∏conj(γ_i)^(m_i). Replacing some of these factors by unit multiples of γ_i preserves N(P₀) and hence the same n and all the fixed data. In the chosen directed coordinate, let δ_i be the positive rotation steps, b the distance from the initial angle to the window entrance, and w the window width. If g<w, b<∑m_iδ_i, and δ_i≤g+∑_(j<i)m_jδ_j, then the attainable partial sums have maximal gap at most g. The induction uses successive translates of the previous interval's endpoints; the next translation leaves a gap at most δ_i minus the previous span. Thus one rotation enters the strict window. For one step it is enough that b<δ<w. A fixed difference congruence is an extra check; equal factor residues modulo the selected modulus preserve endpoint and cross-term residues.

## Exact new two-label example

At (5,4),(4,5), K=396, the original first-label chord is outside the window, while replacing its factor π=6272660+i by conj(π) enters the strict q band. The target n, other endpoint Q, and second label's genuine seed remain identical. The short angle is between 1/(25K²) and 3/(50K²). Both labels satisfy their ordinary height bounds and the high-deficit check; the executable control below checks the coordinates and factor identity, not a proxy density. It also contains an independent Pocklington replay for the earlier finite true-endpoint angle gap.

## One-label growth and why representation counts alone cannot help

For one growing actual label (4+T,3+T), put K=96T and let a be the largest odd integer with a²+1<128K². The original chord just overshoots the upper q edge, with excess angle at most (1/32+o(1))/K² via 2 arctan(1/a) and the at-most-two miss in the odd grid. [Stucky's Gaussian-prime sector theorem](https://arxiv.org/pdf/2008.11325) supplies a Gaussian prime of norm in [K^8/2,K^8] and positive angle in [9,11]/(400K²): with x=K^8 the sector mass is of order x^(3/4), above the x^(7/10+ε) hypothesis for small fixed ε, and prime-power contributions are smaller. Its norm exceeds a²+1, so divisibility of the actual chord endpoint by that prime is one soluble congruence in u and the ordinary-height u interval accommodates it. Conjugation moves it by (0.045 to 0.055)/K², crossing the deficit while staying in the angular window of width (1+o(1))/(8√2 K²). This proves unbounded growth for one label; it does not simultaneously provide the second label's same-target genuine seed.

Conversely choose m distinct split rational primes ≤m^8 with individually selected Gaussian factor angles in (0,m^(−2)], by the same sector result. For their product L, Gaussian unique factorization gives r₂(L)=4·2^m, while log L=O(m log m); yet all angle sums lie within distance 1/m of zero modulo π/2. There is a gap at least π/2−2/m. Thus even more than every fixed polylog power of representations does not imply small maximal angle gap for a single true norm. This does not assert such a family for two simultaneous 3,5 labels.

~~~python
from math import gcd, isqrt, prod

def N(z): return z[0]**2 + z[1]**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]
def chord(a,u,D):
    x = a*u + D - (a*a+1)//2
    return (x,u), (x+1,a-u)
def seed(P,Q,D):
    S = N(P)
    f,g = P[0]-Q[0], P[1]-Q[1]
    assert f%2 and g%2 and N(Q)==S+2*D
    q = ((f+g)//2)**2 + ((f-g)//2)**2
    h = abs(P[0]*Q[1]-P[1]*Q[0])
    assert q%2 and h%2==0 and 2*q*S==(D-q)**2+h*h
    return q, (S+D-q,h)
def band(S,q,K): return 64*K*K*q < S < 64*K*(K+1)*q

A,B = 9**3,25**3
H1,D1,H2,D2 = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
u = 472984194841387909896403492694189266281840 + 41099101632
V,W = chord(3395,u,D2)
n = N(V)+H2
S,R = n-H1,n-H1+2*D1
p,q = S//4,R//2
assert (S,R)==(4*p,2*q) and p%4==q%4==1

proved = set()
def pock(n,fs,a=2):
    F = prod(fs)
    assert (n-1)%F==0 and F*F>n and pow(a,n-1,n)==1
    for l in set(fs):
        if l not in proved:
            assert 1<l<10**8 and all(l%d for d in range(2,isqrt(l)+1))
        assert gcd(pow(a,(n-1)//l,n)-1,n)==1
    proved.add(n)

p1,p2 = 123970123699223,1233683639
p3 = 11188520895438746414943207682170016053103859
p4 = 132794526425824426831752433861599382047002730549598210502512318453
q1,q2 = 17631688827529032222554869,158881933831698858944533088228303
q3,q4 = 26827662066031,418994426147272159
for v,fs in (
    (p1,[619061]+[31]*3),(p2,[56076529]),(p3,[p1,p2]),(p4,[p3]),(p,[p4]),
    (q1,[95902879,28711381]),(q2,[q1]),(q3,[23017,2221]),(q4,[q3]),(q,[q2,q4])
):
    pock(v,fs)

assert 25**64<=n<=9**96 and 2**300<=min(S,N(V))<=max(S,N(V))<2**301
assert band(N(V),seed(V,W,D2)[0],300) and (S%7,R%7)==(4,5)
s,t = 795427079358195677328522559435812965515974020,109221090082265238287023401744804745259577609
v,w = 918451307774422669862501814152767425055669367,667618278238087162806172796406221732126885178
assert s*s+t*t==p and v*v+w*w==q and s>t and v>w>0
P,Q = (2*s,2*t),(v+w,v-w)
least = seed(P,Q,D1)[0]
assert N(P)==S and N(Q)==R and 4810*least<=S<4811*least

K,a,m = 396,4479,6272660
A,B = 9**4,25**4
H1,D1,H2,D2 = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
u = 107631485316749505966915001550914801154368133026062392450
P,Q = chord(a,u,D1)
n = N(P)+H1
pock(m*m+1,[971,971,19,19],3)
v = mul(P,(m,-1))
assert all(x%(m*m+1)==0 for x in v)
J = mul(tuple(x//(m*m+1) for x in v),(m,-1))
assert N(J)==N(P) and D1<N(P)
assert 50*K*K*m>m*m+1 and 100*K*K<3*m
assert 64*K*K*seed(P,Q,D1)[0]>N(P)
q,z1 = seed(J,Q,D1)
assert band(N(P),q,K)

V = (39291590784097337611247250162511840943599363386177292437728,
    -480477554754808827738402215681093878519857497990500323681558)
W = (39077203952492360055572050915095205482030172452458985200149,
    -480495038331053522082116298363812621569685932789593250143863)
q,z2 = seed(V,W,D2)
assert N(V)+H2==n and band(N(V),q,K)
assert 25**80<=n<=9**128 and 2**K<=min(N(P),N(V))<=max(N(P),N(V))<2**(K+1)
d = N(tuple(x-y for x,y in zip(z1,z2)))-((H2-D2)-(H1-D1))**2
assert d%2==0 and (d//2)**5>2**(9*K)
~~~
