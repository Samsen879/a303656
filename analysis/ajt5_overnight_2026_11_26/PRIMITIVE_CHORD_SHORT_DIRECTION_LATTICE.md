# Primitive Gaussian chord: a complete short-direction lattice

Let P,Q be integer endpoints in the primitive second-label chord chart, δ=Q−P, W=P+Q, 2q=N(δ), H=det(δ,P), and N(Q)−N(P)=2D>0. Assume both coordinates of δ are odd; then those of W are odd too. Write Jδ=(-δ_y,δ_x).

**Exact lattice.** The integer span of W and (W+Jδ)/2 equals {g∈Z²: g·δ=0 mod D}. Both displayed generators have scalar product a multiple of D; their determinant has magnitude D, and primitivity makes the reduction modulo D surjective. Gauss reduction gives a nonzero g with L=N(g)≤2D/√3: the other reduced basis vector has length at least √L and projection at most √L/2. If q>D/√3, g cannot be perpendicular to δ since every nonzero integral perpendicular direction has length at least √(2q).

Writing h=g·δ=kD and b=det(g,W)=ℓD, the two basis vectors give k≡ℓ mod 2. The identity kH−ℓq=det(δ,g), from W=(D/q)δ+(H/q)Jδ, gives |ℓ−kH/q|≤√(2L/q). Cauchy gives |k|≤√(2qL)/D. Thus every primitive odd chord satisfying the threshold has a witness in this direction radius. A search using those bounds must still validate integral endpoints, real labels, and the original window; the radius alone is no runtime improvement.

**Unit read can be much larger.** Unit directions satisfy g·δ=1. Their signed transverse coordinate λ=det(δ,g) runs through one class modulo 2q because all solutions differ by integer multiples of Jδ. For the centered representative, N(g_min)=(1+λ²)/(2q). On the same actual target at K=396 below, the second chord has N(g_min)>2^368. Its shortest lattice direction is (914,627), yet |(g·δ)/D| has 173 bits. This finite same-target example rules out using a short unit direction or silently imposing a small multiplier on this exhibited short direction. This is not an asymptotic same-target result or an arbitrary-target selector.

## Independent exact replay (Python standard library)

```python
from math import gcd, isqrt

def add(z,w): return z[0]+w[0],z[1]+w[1]
def sub(z,w): return z[0]-w[0],z[1]-w[1]
def sm(k,z): return k*z[0],k*z[1]
def dot(z,w): return z[0]*w[0]+z[1]*w[1]
def det(z,w): return z[0]*w[1]-z[1]*w[0]
def N(z): return dot(z,z)
def bar(z): return z[0],-z[1]
def perp(z): return -z[1],z[0]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def div(z,w):
    v=mul(z,bar(w)); m=N(w)
    assert not any(x%m for x in v)
    return tuple(x//m for x in v)
def minbez(d):
    q=N(d)//2
    r=pow(d[0],-1,abs(d[1]))
    s=(1-r*d[0])//d[1]
    t=(det(d,(r,s))+q)%(2*q)-q
    v=add(d,sm(t,perp(d)))
    assert all(x%(2*q)==0 for x in v)
    return tuple(x//(2*q) for x in v)
def short(v,w):
    while True:
        if N(w)<N(v): v,w=w,v
        A,B=N(v),dot(v,w)
        if 2*abs(B)<=A: return v
        w=sub(w,sm((2*B+A)//(2*A),v))
def seed(P,Q,D,K):
    d=sub(Q,P); q=N(d)//2; S=N(P); H=det(d,P)
    assert all(x%2 for x in d) and q%2 and H%2==0 and N(Q)==S+2*D
    assert 2*q*S==(D-q)**2+H*H
    assert 2**K<=S<2**(K+1) and 64*K*K*q<S<64*K*(K+1)*q
    return d,q,H

K,a=396,4479
A,B=9**4,25**4
D,E=9*A+2*B,A+50*B
C=D-(a*a+1)//2
u=107631485777229402067141184459932727503114031274994405730
P=(a*u+C,u); Q=(P[0]+1,a-u); gam=(6272660,1)
P1=mul(div(P,gam),bar(gam))
assert 64*K*K*N(sub(Q,P))>2*N(P)
seed(P1,Q,D,K)
V=(-402027876083264712643034407366633865588710892230259818918608,
    266037776584567469843013189860709784275576321292507200145802)
W=(-402146554373700147282217986704201478331699512354938718599599,
    265858346725171887405552333993217862639834692105443252076883)
n=N(P)+27*A+5*B
assert n==N(V)+3*A+125*B and 25**80<=n<=9**128
d,q,H=seed(V,W,E,K)
assert gcd(*d)==gcd(q,E)==1
g=minbez(d); t=det(d,g)
assert dot(g,d)==1 and 25*N(g)<q<36*N(g) and N(g)>2**368
r=H*pow(E,-1,q)%q
r=r if r%2 else r+q
assert (r+q)%(2*q)-q==t

U=add(V,W)
g=short(U,tuple(x//2 for x in add(U,perp(d))))
assert g==(914,627) and 3*N(g)**2<=4*E**2
h,b=dot(g,d),det(g,U)
assert h%E==b%E==0 and abs(h//E).bit_length()==173
assert (h//E-b//E)%2==0 and (h//E)*H-(b//E)*q==det(d,g)
assert n==N(Q)+9*A+B==N(W)+A+25*B
print('both genuine labels and direction checks pass')
```
