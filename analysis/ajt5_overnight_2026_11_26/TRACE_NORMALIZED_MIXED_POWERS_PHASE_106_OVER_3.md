# Trace-normalized mixed powers certify the native phase 106/3

At coprime (U,V)=(53,21), both exact signed Eisenstein half-norms give a new phase 106/3 and exponent ray (106,42)·3^k in the order (5,3). It occurs at the first admissible odd scale in the prior gap. The largest ratio of the new 38-ray catalogue is 43/41 at (82/3,86/3), giving effective exponent 41/86 (previously 157/330), with ε loss in each of the two odd classes 3 and 21 mod 24. The parity-dependent mod-15 rotations give independent opposite nonzero mod-5 characters; the same effective three-square criterion applies. The exact replay includes both true positive targets and failed same-height prescribed labels (v7=1). Nothing is asserted here about density one or arbitrary n.

## Trace on the inputs, not on the compared outputs

For α=a+ω, β=b+ω, t=2a−1 and s=2b−1, the normalized inputs u=α/t,v=β/s have trace 1 and conjugates 1−u,1−v. The bilinear-coordinate probe is the difference s³α²−t²β³. At a split prime away from ts, a match u²=v³ only on one evaluation implies a factor in its rational norm and extracts a root 1−2x/y from the one vanishing component x+yω. If both evaluations match, subtract the two identities to get 2u=v(2v²−3v+3); squaring gives v²(v−1)²(4v²−4v+9)=0. Consequently a match excluding those values must be one-sided. In contrast if the compared outputs themselves have equal trace, their difference has trace zero and cannot distinguish the two evaluations at a split odd prime.

On the full actual minus half of (53,21), bases (16,21) yield 8734616+925691ω and extract precisely 1423 by the norm gcd. The observed pairs of (u²,v³) are (560,560) and (748,644). All old unnormalized square and cubic differences from bases 2,…,21 miss, even as gcds with the entire half. Both same-degree trace-normalized probes from the narrower same panel 16,…,21 miss as well. The wider same-degree normalized cubic panel can hit with (8,20), so there is no general dominance. The remaining CRT roots are supplied as witness data checked by exact substitution. A finite sieve and some factorization aided discovery, not the advertised weighted-gcd block replay.

~~~python
from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt, prod

N = lambda x,y: x*x+3*y*y
E = lambda x,y: x*x-x*y+y*y

def power(a,k):
    if k==2:
        return a*a-1,2*a-1
    return a**3-3*a+1,3*a*a-3*a

def mix(a,b,i,j):
    x,y = power(a,i)
    z,w = power(b,j)
    T,S = (2*b-1)**j,(2*a-1)**i
    return T*x-S*z,T*y-S*w

def old(a,b,k):
    if k==2:
        return a+b,2
    return a*a+a*b+b*b-3,3*(a+b-1)

def recover(H,blocks):
    h,r = H,0
    for d,z in blocks:
        assert h%d==0 and gcd(d,H//d)==1 and (z*z+3)%d==0
        r += z*(H//d)*pow(H//d,-1,d)
        h //= d
    assert h==1
    r %= H
    a,b = H,min(r,H-r)
    while b*b>H:
        a,b = b,a%b
    c = isqrt((H-b*b)//3)
    assert N(b,c)==H
    return b,c

A,S = 5**53,3**21
H,J = (A-S)//2,(A+S)//8
assert H%2==J%2==1 and gcd(H,prod(range(3,42,2)))==1

pairs = list(combinations(range(2,22),2))
assert all(gcd(H,E(*old(a,b,k)))==1 for a,b in pairs for k in (2,3))
hits = []
for a,b in pairs:
    x,y = mix(a,b,2,3)
    d = gcd(H,E(x,y))
    if d>1:
        hits.append((a,b,x,y,d))
assert hits==[(16,21,8734616,925691,1423)]
assert all(gcd(H,E(*mix(a,b,k,k)))==1
           for a,b in combinations(range(16,22),2) for k in (2,3))
assert [(a,b) for a,b in pairs if gcd(H,E(*mix(a,b,3,3)))>1]==[(8,20)]

a,b,x,y,d = hits[0]
r = (1-2*x*pow(y,-1,d))%d
assert r==1287
for r0,want in [(r,(560,560)),(-r,(748,644))]:
    w = (r0-1)*pow(2,-1,d)%d
    u = (a+w)*pow(2*a-1,-1,d)%d
    v = (b+w)*pow(2*b-1,-1,d)%d
    assert (u*u%d,pow(v,3,d))==want

m = recover(H,[(d,r),(H//d,1564456675747600511204086495403464)])
p = recover(J,[(J,1231263098896650553000902888294155071)])
assert m==(164526791703507193,1356963037808759852)
assert p==(811765528340055707,492887920924637758)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def mul(z,w):
    a,b = z
    c,d = w
    return a*c-3*b*d,a*d+b*c

def rot(z):
    x,y = z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

Q,Z = A*A,S*S
z = tuple(8*q for q in mul(m,p))
assert tuple(q%15 for q in z)==(4,4) and 1000*Z<Q
assert all(75*w*w>=4*(Q-Z) for _,w in rot(z))
for T,rr in [((8,2),[10,14]),(mul((8,2),(8,2)),[5,14])]:
    assert sorted(w%15 for _,w in rot(mul(z,T)) if w%3)==rr
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in rr}=={1,4}

W,V = max((abs(w),abs(v)) for v,w in rot(z) if w%3)
assert W>3*S and N(V,W)==4*(Q-Z)
for L in (1,3):
    for t in (W,S+5):
        x,y = (t-S,t) if L==1 else (t+S,t-2*S)
        n = 5*Q+L*Z-x*x-y*y
        R = n-Q-(4-L)*Z
        assert Q<n<5*Q and n%24==(21 if L==1 else 3) and R>0
        assert R==V*V+(W+S)**2 if t==W else R%49==35

P = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9 206/9
70/3 218/9 74/3 674/27 26 710/27 82/3 86/3 30 278/9 290/9 298/9 314/9 34
110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 146/3 50 470/9 158/3 54""".split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)

assert len(P)==38 and gaps(P)[0]==(F(165,157),F(314,9),F(110,3))
P = sorted(P+[F(106,3)])
g = gaps(P)
assert len(P)==39 and g[0]==(F(43,41),F(82,3),F(86,3)) and g[1][0]<g[0][0]
~~~
