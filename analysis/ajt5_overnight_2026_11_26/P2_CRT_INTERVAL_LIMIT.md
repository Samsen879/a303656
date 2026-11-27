# A limit of modular and interval tests for P2

Use the [P2 two-sided allocation filter](P2_TWO_SIDED_ALLOCATION_FILTER.md). Its separate range tests and compatible modular half-roots cannot by themselves prove that the balanced ordinary-height window is empty when the congruence modulus is too small. This note isolates the missing *exact* product.

Write \(A=3^a,B=5^b\) with \(19A<20B<22A\), \(d=(S_1-S_0)/4\), and \(H=729A+625B-\min(A,B)\). Let \(R_*=\sqrt{1000A-S_0}/2,\ Y_*=\sqrt{1000A-S_1}/2\), \(u_*=R_*+Y_*,v_*=R_*-Y_*\). Direct substitution of the balance bounds gives \(15\sqrt A<R_*<16\sqrt A\), \(8\sqrt A<Y_*<10\sqrt A\), so \(u_*v_*=d\). Suppose any compatible pair of half-root factor classes \(u_0,v_0\bmod M\) has been fixed, where \(M\le\sqrt A/2\). Take the unique representatives \(u\in(u_*,u_*+M]\), \(v\in(v_*,v_*+M]\).

Each chosen factor separately remains within the full allowable factor interval: for \(u\) use the real complement \(d/u\), for \(v\) use \(d/v\). The sum \(s+d/s\) has derivative \(1-d/s^2\), hence on the long side it increases by at most \(M\); on the short side it decreases by at most \((26/5)M\), since \(u_*<26\sqrt A,v_*>5\sqrt A\) and \(v\) remains below \(\sqrt d\). Both exact-complement sums lie strictly between \(27\sqrt A\) and \(33\sqrt A\), hence their resulting heights \(S_0+(s+d/s)^2\) lie in \((S_3,H)\). Indeed \(B/A\in(0.95,1.1)\) makes \(S_0+729A>S_3\) and \(S_0+1089A<H\).

The common integer \(K=S_0+(u+v)^2\) also lies in that window, with true first square residual and all congruence witnesses that the supplied root classes guarantee. But \(uv>d\), because both representatives were rounded strictly to the right. Thus the modular equality of products and the two separate intervals do not enforce \(uv=d\). An independent divisor mechanism or stronger conditions would be needed to rule out all exact pairs.

At an isolated nondouble-split block prime, reversing the sign of the local half-root \(Y\) exchanges the two assignments of the whole prime power without disturbing the same local height and other half-roots. The example below checks all four ways of assigning the independent exact powers \(331^1,727^2\) in one balanced real exponent pair, with modular half-roots valid for all displayed primes and modulus small enough for the argument. It does not give an integer \(K\) satisfying the four exact squares, nor exclude one.

~~~python
from fractions import Fraction as F
from itertools import product
from math import isqrt

a,b = 182986688501791627983199859542,124907847079800385175916116884
data = [(2,7,6,124),(3,3,8,21),(5,2,23,16),(7,3,298,203),
        (11,3,1085,76),(13,1,8,0),(17,1,4,2),(19,3,218,124),
        (61,1,37,58),(331,2,79109,30466),(727,3,360985307,23255278)]

def log_bounds(n):
    z = F(n-1,n+1)
    lo = 2*sum(z**(2*i+1)/(2*i+1) for i in range(120))
    return lo,lo+2*z**241/(241*(1-z*z))

def strip(x,p):
    assert x
    m=0
    while x%p==0:
        x//=p
        m+=1
    return m,x

l,h=log_bounds(3)
L,H=log_bounds(5)
assert -F(1,25)<b*L-a*h<b*H-a*l<F(1,25)
s,t=(a-1)//11,(b+2)//11
assert (a%720,b%720)==(22,4) and (a-1,b+2)==(11*s,11*t)
assert (a-1)%121!=0 and s%29==t%29==0
for p,m,mu in ((331,1,1),(727,2,-1)):
    assert all(p%d for d in range(2,isqrt(p)+1)) and p%66==1
    w=pow(3,s,p)*pow(5,-t,p)%p
    assert pow(w,11,p)==p-1 and w!=p-1
    assert pow(59,(p-1)//2,p)==p-1 and pow(3414,(p-1)//2,p)==mu%p
    q=p**(m+1)
    Fnum=(pow(3,a-1,q)+pow(5,b+2,q))%q
    assert strip(Fnum,p)[0]==m

for state in product((0,1),repeat=2):  # 1 表示整幂分给 u
    u0=v0=0
    M=1
    for p,k,x,y in data:
        q=p**k
        A,B=pow(3,a,q),pow(5,b,q)
        S=[(9**i*A+5**t*B)%q for i,t in enumerate((2,4,3,0))]
        assert x*y%q==(2*A+150*B)%q
        K=(S[0]+(x+y)**2)%q
        if p==3: assert (K-125*B)%27==9
        if p==5: assert K%25==5
        for z in S:
            m,w=strip((K-z)%q,p)
            assert m%2==0 and k>=m+(3 if p==2 else 1)
            assert (w%8==1 if p==2 else pow(w,(p-1)//2,p)==1)
        if p in (331,727):
            assert strip(x,p)[0]==k-1 and y%p
            if not state[(331,727).index(p)]:x,y=y,x
        inv=pow(M,-1,q)
        u0+=M*((x-u0)*inv%q)
        v0+=M*((y-v0)*inv%q)
        M*=q
    assert M==153542302760616817765248112982400
    assert (2*M).bit_length()<a//2
    print(state,M,u0,v0)

~~~
