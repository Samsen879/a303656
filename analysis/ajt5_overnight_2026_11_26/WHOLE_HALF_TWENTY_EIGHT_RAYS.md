# Whole-half mixed Jacobian certificates and twenty-eight rays

Two new normalized phases, \(62/3\) and \(190/9\), are certified by \((m,e)=(186,74),(190,78)\). On the [prior twenty-six-ray catalogue](https://github.com/Samsen879/a303656/commit/eba87c449a14b18256193b0c95a1554f933d2391) this splits the largest gap \((182/9,22)\). The new largest ratio is \(55/51\), from 34 to \(110/3\). The effective sphere estimate gives uniform generated-population exponent \(51/110\) up to logarithmic loss in both odd classes. These are generated targets only.

This uses the two elliptic charts modulo each **whole** half \((5^{m/2}+3^{e/2})/8\) or \((5^{m/2}-3^{e/2})/2\); no factor list is needed by the verifier. The Jacobian triple proposes \(X/Z^2\) in the 2-chart, or \(Y/(kZ^3)\) in the 3-chart. For a proposed numerator and denominator \(n,d\), keep the full prime powers of the remaining modulus \(R\) on which \(n^2+3d^2=0\) and \(d\) is a unit. To do so, start with \(G=\gcd(R,n^2+3d^2)\) and strip the prime support shared with \(R/G\), then the support shared with \(d\), by gcd with sufficiently high powers. The resulting coprime block gives an exact root of \(-3\) regardless of the track that proposed it. Nonunit denominators and partial prime-power hits are rejected. CRT combines the roots and the recovered norm coordinates are checked by substitution.

Three of the four halves use both charts and neither supplied chart alone exhausts any of those three. The minus half for \((190,78)\) includes an intact composite block 5280552787 from the 3-chart. Roots propagate through common cubing via the coprime cyclotomic shell, so extending a certified ray needs no new scalar search.

The replay checks the scale-three exclusions, four half-norms, generated exponents and positive two-square residuals, and same-height failed controls with valuation one at a Gaussian inert prime at depths zero and one. The largest ratio is checked on the complete cyclic catalogue.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt

def dbl(P,H,a):
    x,y,z = P
    s,m = 4*x*y*y,3*x*x+a*z**4
    u = (m*m-2*s)%H
    return u,(m*(s-u)-8*y**4)%H,2*y*z%H

def add(P,Q,H):
    X,Y,Z = P
    U,V,W = Q
    x,y,u,v = X*W*W,Y*W**3,U*Z*Z,V*Z**3
    h,r = u-x,v-y
    w = (r*r-h*h*(x+u))%H
    return w,(r*(x*h*h-w)-y*h**3)%H,h*Z*W%H

def mul(M,P,H,a):
    R = P
    for bit in bin(M)[3:]:
        R = dbl(R,H,a)
        if bit == '1': R = add(R,P,H)
    return R

def part(R,n,d):
    g = gcd(R,n*n+3*d*d)
    b = R.bit_length()
    g //= gcd(g,pow(R//g,b,g))
    return g//gcd(g,pow(d,b,g))

def cover(H,charts):
    R,r = H,0
    for l,k,M,P,count in charts:
        a = 3 if l == 2 else 0
        x,y,z = P
        assert z == 1 and y*y == x**3+a*x+k*k
        J = mul(M,P,H,a)
        for _ in range(count):
            x,y,z = J
            n,d = (x,z*z) if l == 2 else (y,k*z**3)
            q = part(R,n,d)
            if q > 1:
                u = n*pow(d,-1,q)%q
                assert (u*u+3)%q == 0
                r += u*(H//q)*pow(H//q,-1,q)
                R //= q
            if R == 1:
                assert (r*r+3)%H == 0
                return r%H
            D = dbl(J,H,a)
            J = D if l == 2 else add(D,J,H)
    return None

def norm(H,r):
    a,b = H,min(r,H-r)
    while b*b > H: a,b = b,a%b
    d = isqrt((H-b*b)//3)
    assert b*b+3*d*d == H
    return b,d

def C2(M,L): return (2,0,M,(1,2,1),L)
def C3(k,M,x,y,L): return (3,k,M,(x,y,1),L)

# m, e, plus charts, minus charts, (a,b,c,d), failed controls by depth
rows = [
 (186,74,
  [C2(2098034322396308049930252724056627998445397164903804389872789,3)],
  [C2(7043400939895708023906338338023044889539267597788049816658067,2),
   C3(729876,2012511658958846717430207699991,217,729883,2)],
  (97474505412458047285470166661053,32251590545443779356323572384828,
   222181318402745459834264330962207,19343902458419959122986361687188),
  [(1,31,651),(17,239,1673)]),
 (190,78,
  [C2(616297582203915474351263971177736000215039214268088665524446535,6),
   C3(1542,78128353205503919346804060530229178547413798801,21,1545,1)],
  [C2(1040237517928505775634850193873199937024052432878891841193545,2),
   C3(1802350,21702772,341,1802361,1)],
  (236330369999304925895201871395068,294217786854339335225036647322115,
   999736126270122635003915401601489,295919542096624804426477998064544),
  [(1,19,209),(5,367,29360)]),
]
assert part(49,2,1) == 1 and part(49,0,0) == 1
assert [[m for m in range(2,22*t,4) if 182*t < 9*m] for t in (1,3,9)] == [
    [],[62],[186,190,194]]
assert 3**90 < 5**62 < 3**94
ps = [2,11,2,28493,2,17,11,23,2,17,2,11,2,83,953,353897,2,17,2,5477,2,11,15473]
assert len(ps) == len(range(2,91,4))
for e,p in zip(range(2,91,4),ps):
    N,f = 5**62-3**e,1
    while N%p == 0: N,f = N//p,f*p
    assert f%3 == 2 and gcd(N,f) == 1

for m,e,cp,cm,(a,b,c,d),tests in rows:
    A,B = 5**(m//2),3**(e//2)
    for H,charts,want in (((A+B)//8,cp,(a,b)),((A-B)//2,cm,(c,d))):
        if len(charts) > 1:
            assert all(cover(H,[C]) is None for C in charts)
        assert norm(H,cover(H,charts)) == want
    assert 8*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B

    Q,Z,v,w = A*A,B*B,8*(a*c-3*b*d),8*(a*d+b*c)
    for j,p,rr in tests:
        s = isqrt(Z)
        W,V = max((abs(y),abs(x)) for x,y in
                  [(v,w),((v-3*w)//2,(v+w)//2),
                   ((-v-3*w)//2,(v-w)//2)] if y%3)
        assert s*s == Z and V*V+3*W*W == 4*(Q-Z) and 3*W*W >= Q-Z > 9*Z
        assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
        assert 0 < rr < p*p and rr%p == 0
        for L in (1,3):
            for t in (W,s+j):
                x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
                S = x*x+y*y
                n = 5*Q+L*Z-S
                R = n-Q-(4-L)*Z
                assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
                if t == W: assert R == V*V+(W+s)**2
                else: assert R > 0 and R%(p*p) == rr
        x,y = (Q-Z)//2,(Q+Z)//2
        v,w,Q,Z = x*v-3*y*w,x*w+y*v,Q**3,Z**3

g = list(map(F,("18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 82/3 86/3 "
                "30 290/9 34 110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(55,51)
print("PASS")
~~~
