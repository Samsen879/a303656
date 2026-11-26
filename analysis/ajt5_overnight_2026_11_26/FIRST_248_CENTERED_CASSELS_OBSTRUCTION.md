# The centered five-column obstruction by a Cassels certificate

For the fixed base \(4,8,12\) of the [first-248 seed](FIRST_248_CENTERED_TWO_STAGE_PELL.md), there is no centered, positive-\(D\) rational Pell conic \(s^2-Dt^2=C_0\) through the seed on which **all** of \(s^2+h_0,s^2+h_{16},s^2+h_{20}\) are rational-function sums of two squares. This excludes the indicated kind of uniform extension, not individual fifth-column integers or other covers.

The values of \(S,h_0,h_{16},h_{20}\) are those in the linked note. Real nonnegativity requires \(C_0\ge-h_{20}\); at equality the seed would require \(\tau^2=(S^2+h_{20})/(h_0-h_{20})\), whose valuation at 3 is \(-1\). To see the inequality, a real conic point can have \(s^2=\max(C_0,0)\), and a negative residual there would stay negative on an open set, away from any poles. For strict inequality, the simple-zero points of \(s^2+h_j\) have residue fields contained in, and given by the indicated roots of, \(\mathbb Q(\sqrt{-h_j},\sqrt{-(C_0+h_j)/D})\). A sum of two squares at an odd-order zero must split in the constant extension by \(i\). Thus the square class of \(D(C_0+h_j)\) must be \(1\) or \(-h_j\). For \(h_0>0\) the latter is impossible over the reals, so rescale \(t\) rationally to set \(D=C_0+h_0\). With \(\tau=u/v\) at the seed, \(D=(S^2+h_0)/(1+\tau^2)\). The three choices involving a nontrivial square class for 16 or 20 are excluded by the exact modulo \(4,4,8\) tests in the replay below.

When both classes are ordinary squares, put \(T=270131477773693,\ B=381469726443,\ C=238418579101443\). The two equations are \(Tz_{16}^2=(T-B)v^2-Bu^2\) and \(Tz_{20}^2=(T-C)v^2-Cu^2\). Set \(R_1=C(T-B)\), \(R_2=B(T-C)\). The map to \(Y^2=X(X-R_1)(X-R_2)\) uses \(X=BC(u/v)^2,\ Y=TBCu z_{16}z_{20}/v^3\). The square-class triple in root order \(0,R_1,R_2\) is \((BC,-TC,-TB)\). The endpoints \(X=0,R_2\) fail by the odd valuations checked in the replay, and \(v=0\) is impossible over the reals.

Use the [Cassels pairing formula and good-place rule, §2.1 and Lemma 2.2](https://arxiv.org/pdf/2303.05059#page=4), with companion triple \((3816554486630,-2849145,-1204866164300214)\) in the **same** root order. The script gives the diagonal conics with prescribed rational tangent points, the exact tangent coefficients, and all 16 bad-prime witnesses for both covers. It verifies by Hensel precision that the root representatives give the displayed local Hilbert products, regardless of the signs of the two lifted coordinates. Away from these primes all six minors for both covers are units, so their reductions are smooth genus-one curves with finite-field points by the Hasse bound, and the tangent reductions satisfy the good-place rule. At the real place choose \(u=0,v=1\), both radicals negative. The second and third tangents are then negative and the first companion entry is positive, giving real product \(+1\). Real local solvability of the companion is obtained from \(0<X'<R_2\).

The exact product is negative at 2, 19 and 73 only. A rational point on the target cover would give product \(+1\) by using that same point everywhere and Hilbert reciprocity, since the product is independent of local point choices. Its tangent values cannot vanish: tangency would make the respective projection proportional to the tangent point; the omitted coordinate would then require \(u^2=-v^2\), a rational square with nonsquare unit residue 2 modulo 11, or a negative square, respectively. Thus the negative product rules out a rational point. This argument needs no rank computation.

## Standalone exact replay

```python
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd, isqrt, prod

T, B, C = 270131477773693, 381469726443, 238418579101443
R1, R2 = C*(T-B), B*(T-C)
e = (0,R1,R2)
d = (B*C,-T*C,-T*B)
dp = (3816554486630,-2849145,-1204866164300214)
# p, u, v, k, z16 mod p**k, z20 mod p**k, companion abscissa x'
rows = (
 (2,1,0,7,117,65,38),
 (3,0,1,4,58,7,-9),
 (5,1,0,18,3053556225682,2290616772557,R1+4*5**17),
 (13,0,1,4,19176,2692,R2+52),
 (19,0,1,2,351,39,57),
 (53,1,1,2,490,425,1),
 (73,1,1,2,4819,164,73),
 (461,4,1,2,32744,101151,-2),
 (769,831,1,2,565221,426198,R1-7*769),
 (1097,2,1,2,668131,433316,-1),
 (231169,1,0,2,18531045633,19819130431,17),
 (4667581,5,1,2,10761565575142,4774246608065,-3),
 (5534003,1,1,2,23741151424803,21453132631810,1),
 (133990069,0,1,2,1611600392315441,5873316052168654,1),
 (275166149,1,0,2,57798258895617624,70147511522581967,-275166149),
 (351276303997,2625508324779,1,2,109078255812695902649724,32907861124624712421527,1),
)
# Coordinate order: (v,u,z16,z20). L_i is the polar form divided by scale_i.
H = ((B-C,0,C,-B),(-(T-C),C,0,T),(-(T-B),B,T,0))
Q = ((1,0,1,1),(1214575917614,354673167315,0,249318512345),
     (1421958879284,34253989886155,601805666935,0))
scales = (39,5,5)
L = ((-6103515625000,0,6113296900037,-9781275037),
     (-7703544601009569197602300,16912134519330131099387109,0,13469755635218714267348017),
     (-76714683825943518263633800,2613372030290567312619333,32513330828346888972588191,0))

def unit(x,p):
    x = F(x)
    a,b = x.numerator,x.denominator
    assert a
    n = 0
    while a%p == 0:
        a //= p
        n += 1
    while b%p == 0:
        b //= p
        n -= 1
    return n,F(a,b)

def mod(x,m):
    x = F(x)
    return x.numerator*pow(x.denominator,-1,m)%m

def chi(a,p):
    r = pow(a%p,(p-1)//2,p)
    assert r in (1,p-1)
    return 1 if r == 1 else -1

def local_square(x,p):
    n,a = unit(x,p)
    return n%2 == 0 and (mod(a,8)==1 if p==2 else chi(mod(a,p),p)==1)

def hilbert(x,y,p):
    n,a = unit(x,p)
    m,b = unit(y,p)
    if p==2:
        a,b = mod(a,8),mod(b,8)
        j = ((a-1)//2)*((b-1)//2)+n*((b*b-1)//8)+m*((a*a-1)//8)
        return (-1)**(j%2)
    return (-1)**(n*m*((p-1)//2)%2)*chi(mod(a,p),p)**(m%2)*chi(mod(b,p),p)**(n%2)

def radicand(b,u,v):
    return F((T-b)*v*v-b*u*u,T)

P = tuple(row[0] for row in rows)
assert len(P)==len(set(P))==16 and all(p>=2 and all(p%a for a in range(2,isqrt(p)+1)) for p in P)
disc = 16*R1**2*R2**2*(R1-R2)**2
assert prod(d)==(T*B*C)**2 and isqrt(prod(dp))**2==prod(dp)
assert all(disc%p==0 for p in P)
for n in (disc,2*T*B*C*(T-B)*(T-C)*(C-B),*d,*dp,*scales):
    assert n
    for p in P:
        while n%p==0:
            n //= p
    assert abs(n)==1
for ds in (d,dp):
    A0,A1 = (-R1,ds[0],-ds[1],0),(-R2,ds[0],0,-ds[2])
    for i,j in combinations(range(4),2):
        minor = A0[i]*A1[j]-A0[j]*A1[i]
        assert minor
        for p in P:
            while minor%p==0:
                minor //= p
        assert abs(minor)==1
for h,q,l,g in zip(H,Q,L,scales):
    assert gcd(*q)==1 and sum(a*x*x for a,x in zip(h,q))==0
    raw = tuple(a*x for a,x in zip(h,q))
    assert gcd(*raw)==g and raw==tuple(g*x for x in l)
assert mod(radicand(B,Q[1][1],Q[1][0]),11)==2 and chi(2,11)==-1
assert radicand(C,Q[2][1],Q[2][0])<0
assert 0 < B < C < T and R1 > R2 > 0 and dp[0]>0>dp[1] and dp[2]<0
assert all((F(R2,2)-r)/a>0 for r,a in zip(e,dp))
for b,q,j in ((C,Q[1],3),(B,Q[2],2)):
    assert (T-b)*q[0]**2-T*q[j]**2==b*q[1]**2>0
assert [1+sum((y*y-x*(x-R1)*(x-R2))%p==0 for x,y in product(range(p),repeat=2))
        for p in (7,11)] == [4,8]

negative = []
for p,u,v,k,z,w,xp in rows:
    assert (u%p or v%p) and 0<z<p**k and 0<w<p**k
    assert all(xp!=r and local_square(F(xp-r,a),p) for r,a in zip(e,dp))
    for b,r in ((B,z),(C,w)):
        s,_ = unit(2*r,p)
        assert k>s and mod(radicand(b,u,v)-r*r,p**(k+s))==0
    signs = set()
    for a,b in product((1,-1),repeat=2):
        vals = tuple(sum(x*y for x,y in zip(l,(v,u,a*z,b*w))) for l in L)
        assert all(x and unit(x,p)[0]+(3 if p==2 else 1)<=k for x in vals)
        trip = tuple(hilbert(x,y,p) for x,y in zip(vals,dp))
        signs.add(prod(trip))
        if a==b==1:
            print(p,trip)
    assert len(signs)==1
    if signs=={-1}:
        negative.append(p)
assert negative==[2,19,73]

S, h0, h16, h20 = 5409768750,446373525337120,-40882056637497500,-25829822486324997500
q,g = 19499950,270850
assert h0==q*q+F(g*(5**13-239),5) and isqrt(h0)**2!=h0
assert (h16,h20)==tuple(q*q+g*(5**12-5**j) for j in (16,20))
f0 = S*S+h0
assert F(h0-h16,f0)==F(B,T) and F(h0-h20,f0)==F(C,T)
assert unit(F(T-C,T),2)[0]==1 and unit(F(T-C,C),3)[0]==-1
for i,j,m in ((0,1,4),(1,0,4),(1,1,8)):
    pairs = []
    for h,k in ((h16,i),(h20,j)):
        f = f0*(-h)**k
        a,b = F(S*S+h,f),F(h-h0,f)
        scale = F(2)**(-2*(min(unit(a,2)[0],unit(b,2)[0])//2))
        pairs.append((mod(scale*a,m),mod(scale*b,m)))
    squares = {r*r%m for r in range(m)}
    assert not any((u%2 or v%2) and all((a*v*v+b*u*u)%m in squares for a,b in pairs)
                   for u,v in product(range(m),repeat=2))
    print((i,j),'excluded mod',m,pairs)
print('negative places:',negative,'global product: -1')
```
