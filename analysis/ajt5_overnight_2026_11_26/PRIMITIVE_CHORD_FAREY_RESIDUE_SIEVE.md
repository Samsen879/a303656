# A Farey and norm-residue sieve for the primitive second chord

Fix a genuine target and second label, with lower squared radius S in [2^K,2^(K+1)) and a positive endpoint norm gap 2D. In the critical window 64K²q<S<64K(K+1)q write Q_*≈S/K² for the common scale of q. Assume D is at least a fixed positive multiple of K and D≪2^(K/16). Write A=S+D, F(q)=2Aq−q²−D², α(q)=sqrt(F(q))/q, and L*=floor(2D/sqrt(3)). The prior complete direction lattice for primitive odd chords supplies a shortest nonzero direction g, primitive in that lattice, with L=N(g)≤L*. Its projection and cross-read are kD and lD. Reflect or reverse direction signs as needed to use H=sqrt(F(q))≥0 and k>0. The primitive basis coordinates imply k≡l mod 2 and gcd((k+l)/2,l)=1.

On a subwindow [a,b], we have k≤sqrt(2L*b)/D and |l−kα(q)|≤sqrt(2L*/a) by the direction identities. Since α decreases there, fixed (k,l) gives an integer interval [x,y], using squared comparisons. Expanding (kD)²+(kH−lq)²=2Lq shows
```
L = k² A + ((l²−k²)/2) q − kl H.
```
H is even, so the residue of the first two terms modulo 2kl must be reachable by an integer L in [ceil(k²D²/(2y)),L*]. The interval is taken modulo 2kl, never assuming it does not wrap. Restrict to odd q. Farey enumeration visits the reduced slopes, and the primitive basis condition leaves at most the two multiples 1,2 of their reduced pair. Two Euclidean floor sums count the residue-filtered q in a progression; prefix search locates them for the final exact square/primitivity test. These tests do not discard a genuine primitive chord.

## Whole-window square-test count

Here α≈K, |α'|≈K/Q_*, and its full span is O(1); these follow by differentiating α²=2A/q−1−D²/q² on the critical window. Write B≈sqrt(Q_*/D) for the upper limit on k and C=sqrt(DQ_*)/K. In a dyadic denominator block j≤k<2j, there are O(j²) reduced slopes, with admissible q-interval length O(1+C/j) each. If two passing odd q differ by 2t, their residues give ||t (α_0−1/α_0)/2||≪D/(Kj²), where α_0=l/k and t≪C/j. For each t the prohibited-near-equality complement can be counted by covering the near-equality set with O(t) intervals of length O(D/(Kj²t)): the derivative of (x−1/x)/2 is bounded below on the slope range. Farey spacing ≫j^(−2) bounds those slopes by O(t+D/K). Since C/j is at least a constant multiple of D/K up to B, summing over t gives O((C/j)^2) slopes with multiple hits; each has O(C/j) candidate integers. Summing small blocks directly and large blocks by this two-hit bound, split at sqrt(C), yields O(B²+C^(3/2)) = O(Q_*/D). Direct checking of odd q in the full window takes Θ(Q_*/K) square tests. This is a count of square tests, not a measured runtime or a claim about all n or all labels.

## Exact same-target replay and multiplier boundary

The two nearby K=396 subwindows are checked against direct exhaustive odd-q scanning. Square tests go from 262145 to 1 in the window with the true second chord and from 262144 to 0 in the disjoint negative window. There is no full K=396 window experiment. Here the short direction (914,627) has a 173-bit |k|; since L* times its squared norm is less than D², no independent direction fits this radius (its determinant with (914,627) would be a nonzero multiple of D). Thus one cannot impose a small-k rule for this exhibited actual chord. The test uses the lattice's primitive Gaussian congruence, and the two actual chord endpoints and all norm equations are also checked directly.

```python
from fractions import Fraction as F
from math import gcd, isqrt

def fs(n,m,a,b):
    s=0
    while True:
        u,a=divmod(a,m); v,b=divmod(b,m)
        s+=u*n*(n-1)//2+v*n
        if a*n+b<m: return s
        n,b=divmod(a*n+b,m); a,m=m,a

def first(a,b,p):
    while a<b:
        c=(a+b)//2
        if p(c): b=c
        else: a=c+1
    return a

def above(x,B):
    if x.denominator<=B: return x
    a,b=x.numerator,x.denominator
    p,q,r,s=0,1,1,0
    while b and q+(a//b)*s<=B:
        c=a//b
        p,q,r,s=r,s,p+c*r,q+c*s
        a,b=b,a%b
    c=(B-q)//s
    return max(F(p+c*r,q+c*s),F(r,s))

def successor(x,B):
    a,b=x.numerator,x.denominator
    d=(-pow(a,-1,b))%b
    d+=(B-d)//b*b
    return F((a*d+1)//b,d)

def norm(z): return sum(x*x for x in z)
def sub(z,w): return tuple(x-y for x,y in zip(z,w))

K=396
A5,B5=9**4,25**4
D,E=9*A5+2*B5,A5+50*B5
u=107631485777229402067141184459932727503114031274994405730
a,m=4479,6272660
x=a*u+D-(a*a+1)//2
M=m*m+1
assert (m*x+u)%M==(m*u-x)%M==0
P=(((m*m-1)*x+2*m*u)//M,((m*m-1)*u-2*m*x)//M)
Q=(x+1,a-u)
n=x*x+u*u+27*A5+5*B5
assert norm(P)==x*x+u*u and norm(Q)==norm(P)+2*D
assert 64*K*K*norm(sub(Q,(x,u)))>2*norm(P)

V=(-402027876083264712643034407366633865588710892230259818918608,
    266037776584567469843013189860709784275576321292507200145802)
W=(-402146554373700147282217986704201478331699512354938718599599,
    265858346725171887405552333993217862639834692105443252076883)
S=n-3*A5-125*B5; A=S+E; cap=isqrt(4*E*E//3)
assert norm(V)==S and norm(W)==S+2*E and 25**80<=n<=9**128
for X,Y in [(P,Q),(V,W)]:
    d=sub(Y,X); q=norm(d)//2
    assert all(t%2 for t in d) and 2**K<=norm(X)<2**(K+1)
    assert 64*K*K*q<norm(X)<64*K*(K+1)*q

d,e=sub(W,V); q0=(d*d+e*e)//2
H0=abs(d*V[1]-e*V[0])
h=914*d+627*e
b=914*(V[1]+W[1])-627*(V[0]+W[0])
k0,l0=abs(h)//E,abs(b)//E
L0=914**2+627**2
assert gcd(d,e)==gcd(q0,E)==1 and h%E==b%E==0 and k0.bit_length()==173
assert L0<=cap and cap*L0<E*E
assert (k0*E)**2+(k0*H0-l0*q0)**2==2*q0*L0

def f(q): return 2*A*q-q*q-E*E
def true(q):
    H=isqrt(f(q))
    if H*H!=f(q) or H%2: return False
    c=gcd(E,q); m=q//c
    if H%c: return False
    for x in range(H//c*pow(E//c,-1,m)%m,q,m):
        t=x if x%2 else x+q
        if (t*t+1)%(2*q)==0: return True
    return False

def sieve(a,b):
    assert E<a and A*a>E*E and f(b)>0
    B=isqrt(2*cap*b//(E*E))
    lo,hi=F(isqrt(f(b)),b),F(isqrt(f(a))+1,a)
    eps=F(isqrt(2*cap*a)+1,a)
    raw=pairs=checks=0; out=set(); j=1
    while j<=B:
        J=min(B,2*j-1)
        z=above(lo-eps/j,J)
        while z<=hi+eps/j:
            raw+=1
            for t in (1,2):
                k,l=t*z.denominator,t*z.numerator
                if not(j<=k<=J and (k-l)%2==0 and gcd((k+l)//2,l)==1):
                    continue
                pairs+=1
                low,high=(l-eps)/k,(l+eps)/k
                x=first(a,b+1,lambda q:f(q)*high.denominator**2<=(q*high.numerator)**2)
                y=first(x,b+1,lambda q:f(q)*low.denominator**2<(q*low.numerator)**2)-1
                x|=1
                if x>y: continue
                L=max(1,(k*k*E*E+2*y-1)//(2*y))
                if L>cap: continue
                m=2*k*l; U=(l*l-k*k)//2
                v=k*k*A+U*x-L; w=min(m,cap-L+1)
                N=(y-x)//2+1
                def cnt(t): return fs(t,m,2*U,v)-fs(t,m,2*U,v-w)
                count=cnt(N); checks+=count
                for i in range(1,count+1):
                    q=x+2*(first(0,N,lambda t:cnt(t)>=i)-1)
                    if true(q): out.add(q)
            z=successor(z,J)
        j*=2
    return out,(raw,pairs,checks)

R=262144
for a,b,X,Y in [(q0-R,q0+R,{q0},(96,24,1)),
                 (q0+R+1,q0+3*R,set(),(98,24,0))]:
    assert 64*K*K*b<S<64*K*(K+1)*a
    assert sieve(a,b)==(X,Y)
    assert {q for q in range(a|1,b+1,2) if true(q)}==X
print("PASS")
```
