# Two native seeds fill the (22, 70/3) gap

The coprime native seeds (101,109) and (103,77) certify phases 202/9 and 206/9. In the cyclic phase catalogue the previously largest gap (22,70/3) is split into three. The new, unique largest ratio is 37/35 at (70/3,74/3); 54 is the cyclic copy of 18. The effective generated-population exponent in each of 3 and 21 modulo 24 is now 35/74, up from 33/70, with the usual arbitrary ε loss. This counts constructed targets; it does not improve the separate natural-density result or guarantee representation for any prescribed integer.

## Exact half-norms

Write N(x,y)=x²+3y². For each row (U,V), 5^U−3^V equals 2N of the minus pair and 5^U+3^V equals 8N of the plus pair.

| (U,V) | Minus pair | Plus pair |
|---|---|---|
| (101,109) | (134505721115081142418157003781136007, 23307606897300789798085313403355168) | (36271252392788442408010473314510897, 34712038773745161453916798733119392) |
| (103,77) | (516886587308423003022092908620522097, 274387998780184980182927690306593118) | (249849724913664503113496177706265372, 142401581687551572290958798000241472) |

Multiplication gives an integral norm of 4(5^(2U)−3^(2V)). The exact replay checks true same-height targets with positive two-square residuals and other targets at the same height whose indicated label fails with inert valuation one (31 for U=101, and 11 for U=103). These failures are about one label only.

## Whole-half recovery and two distinct failures

The two-twist channel supplies a root from x on y²=x³+3x. The three-twist channel supplies a root from y/k on y²=x³+k². Nonunit denominators are not accepted; when they reveal a coprime block, verify each block separately. Retain only exact roots of −3 on complete coprime blocks, combine them by CRT, and then recover and check an actual integer norm by Cornacchia. The search scalars used factor-group orders at the discovery stage. The verifier itself takes the scalars as data and does not require a prime factorization.

For (101,109) on the plus half the specified two-twist scalar lands at infinity on the whole odd modulus, but the three-twist scalar gives a root on the whole modulus. For the same U=101 and V=117 the plus half divided by 8 really is a norm but contains 23², and −3 is a quadratic nonresidue modulo 23. No full primitive root exists. Its minus half is separately obstructed: 22960331 is 2 mod 3 and divides the half coprimely, so some inert valuation is odd. Thus failure of a chosen recovery chart, impossibility of a primitive root notwithstanding an imprimitive norm, and failure of the norm itself are distinguishable.

## Effective count

Both axes grow as (2U,2V)·3^k, in the order (5,3). The signed net cube-factor counts are 0 at even k and +1 or −1 respectively at odd k. The base rotation bounds keep the selected coordinates a fixed positive fraction of √Q, using the tiny angular drift under cubing. The exact modulo 15 tests give two opposite nonzero characters of 3w²+2LZ modulo 5 for each L=1,3 and every depth; their squarefree kernels differ. As in the [30-ray construction](https://github.com/Samsen879/a303656/commit/0b08cc4c82aafe7a11b0882d30cfec13756203b6), the effective three-square count can avoid the single exceptional discriminant. Interpolating by the new maximal ratio gives 1/(2·37/35)=35/74.

## Exact replay (Python 3)

~~~python
from math import gcd, isqrt
from fractions import Fraction as F

def point(h, a, m, P):
    def zero(t):
        d = gcd(t, h)
        if 1 < d < h:
            raise ZeroDivisionError(d)
        return d == h

    def add(P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x, y = P
        u, v = Q
        n, d = v-y, u-x
        if zero(d):
            if not zero(n):
                return None
            n, d = 3*x*x+a, 2*y
            if zero(d):
                return None
        w = n*pow(d, -1, h) % h
        z = (w*w-x-u) % h
        return z, (w*(x-z)-y) % h

    T = None
    for bit in bin(m)[2:]:
        T = add(T, T)
        if bit == '1':
            T = add(T, P)
    return T

def blocks(h, l, m, k, x, y):
    a = 3 if l == 2 else 0
    assert (y*y-x**3-a*x-k*k) % h == 0
    try:
        out = []
        T = point(h, a, m, (x % h, y % h))
        for _ in range(8):
            if T is None:
                break
            n, d = (T[0], 1) if l == 2 else (T[1], k)
            q = gcd(h, n*n+3*d*d)
            if q > 1 and gcd(q, d*(h//q)) == 1:
                out.append((q, n*pow(d, -1, q) % q))
            T = point(h, a, l, T)
        return out
    except ZeroDivisionError as e:
        q = e.args[0]
        assert gcd(q, h//q) == 1
        return blocks(q,l,m,k,x,y) + blocks(h//q,l,m,k,x,y)

# U,V,sign, T2 scalar, remainder (0 means H), T3=(scalar,k,x,y)
data = [
(139,123,-1,441357868820383539727129835270905981390931069081735233913543870282026778983482002674708866125,
 18517032083803586722528893666799917403,(228584943004656841993791898627305700,20746,77,20757)),
(139,123,1,113148145015806705450367273548887894805774195966133513773135249188074401026661977041137489046795,
 0,(7269498431186078769525512158290806674021342679323021095659359921247473631401005036988008701875,13119,54,13125)),
(101,109,-1,86364093145044772629229384399524952388070737883424673355744556585,
 88635187,(3283417,2247,30,2253)),
(101,109,1,1232595164407830946272831375147109060662454511836532262992652614470493,
 0,(547820073070147087232369500065381820733208673017263226073293082235044,120,9,123)),
(103,77,-1,17608502348683299227940369760776478243162624186893917390815941602862971,
 70434009394733196911761479043105912972650496747575669563263766411451883,
 (2608667014619748033768943668263181943920404996562749900971421962210441,252,16,260)),
(103,77,1,240756605609444957881707314763729884716000320425607138556384064031529,
 36214861,(4022572,120,9,123)),
]

P = {}
for u,v,s,M,R,C in data:
    n = 5**u+s*3**v
    e = (n & -n).bit_length()-1
    h = H = n >> e
    r = 0
    for l,m,k,x,y in [(2,M,0,1,2), (3,*C)]:
        for q,z in blocks(h,l,m,k,x,y):
            q = gcd(q,h)
            if q == 1:
                continue
            assert (z*z+3) % q == 0 and gcd(q,H//q) == 1
            r += z*(H//q)*pow(H//q,-1,q)
            h //= q
        if l == 2:
            assert h == (R or H)
    assert h == 1 and (r*r+3) % H == 0
    r %= H
    a,b = H,min(r,H-r)
    while b*b > H:
        a,b = b,a%b
    c = isqrt((H-b*b)//3)
    assert b*b+3*c*c == H
    f = e-(1 if s == -1 else 3)
    assert f >= 0 and f % 2 == 0 and gcd(u,v) == 1
    P[u,v,s] = b << (f//2), c << (f//2)

assert point((5**101+3**109)//8,3,data[3][3],(1,2)) is None
A,B = 5**101,3**117
assert (A+B)//8 == 23**2*(3030162549200624680125036043139681**2
                         +3*214713145458628107721399891026454**2)
assert pow(-3,11,23) == 22
h,d = (A-B)//2,22960331
assert d % 3 == 2 and h % d == 0 and gcd(d,h//d) == 1

def mul(z,w):
    a,b = z
    c,d = w
    return a*c-3*b*d,a*d+b*c

def rot(z):
    x,y = z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

for u,v,j,p,c,sgn in [(101,109,29,31,12,1),(103,77,5,11,10,-1)]:
    Q,Z,S = 25**u,9**v,3**v
    z = tuple(8*t for t in mul(P[u,v,-1],P[u,v,1]))
    assert 1000*Z < Q and min(48*w*w for _,w in rot(z)) >= 4*(Q-Z)
    for T in ((1,0),(8,2*sgn)):
        w15 = [w % 15 for _,w in rot(mul(z,T)) if w % 3]
        for L in (1,3):
            assert {pow(3*w*w+8*L,2,5) for w in w15} == {1,4}
    W,V = max((abs(w),abs(x)) for x,w in rot(z) if w % 3)
    for L in (1,3):
        for t in (W,S+j):
            x,y = (t-S,t) if L == 1 else (t+S,t-2*S)
            n = 5*Q+L*Z-x*x-y*y
            R = n-Q-(4-L)*Z
            assert Q < n < 5*Q and n % 24 == (21 if L == 1 else 3)
            assert R > 0
            assert R == V*V+(W+S)**2 if t == W else R % p**2 == c*p

old = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22
70/3 74/3 26 82/3 86/3 30 278/9 290/9 314/9 34 110/3 38
118/3 122/3 42 130/3 134/3 46 142/3 50 470/9 158/3 54""".split()))
new = sorted(old+[F(202,9),F(206,9)])
gaps = sorted(((b/a,a,b) for a,b in zip(new,new[1:])), reverse=True)
assert gaps[0] == (F(37,35),F(70,3),F(74,3)) and gaps[1][0] < F(37,35)
~~~
