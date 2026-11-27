# Two mixed-torsion certificates give twenty-six sphere rays

The [twenty-four-ray catalogue](https://github.com/Samsen879/a303656/commit/3a66463bad8cc713ab7b5c352fdb2802528b5ed9) had widest gap from 42 to 46. Both smallest-scale candidates are now certified: \(130/3\) and \(134/3\) at \((m,e)=(130,122),(134,166)\). The new maximum adjacent ratio is \(99/91\), from \(182/9\) to 22. The existing effective sphere construction gives the uniform exponent \(91/198\) for generated targets in each odd class, up to logarithmic loss. It says nothing about coverage of a prescribed target.

For the first seed, the plus half has exact valuation two at 17, where \(-3\) is a nonsquare. Divide by \(17^2\), extract a root of \(-3\) from the prior elliptic 3-torsion construction, and rescale the recovered norm coordinates by 17. The second seed's plus half contains the verified prime 1320683444989 at which \(x^3=-400\) has no solution, so the previous fixed curve cannot certify that component via its nonzero-\(x\) 3-torsion condition.

On the alternate curve \(y^2=x^3+3x\), unit \(x\) at a point \((x,0)\) gives \(x^2=-3\). An odd scalar projects the point \((1,2)\) to components of different doubling depths. Extract the factor where \(y=0\) by gcd, then double on the complementary factor and combine the roots by CRT. On the plus half the actual components reach order two at successive depths, so a single scalar for the original point cannot land at nonzero order two on both. On the minus half an exact nonunit denominator gives 7, where the root is 2; the complementary factor is handled by doubling. The identities and CRT roots are checked directly, with no need to reproduce the point-count search.

The replay checks all four half-norm identities, the same-height positive and exact valuation-one failed controls over both classes and the first two cubing depths, and the exact phase gap. The remaining smallest-scale pairs in this gap are vetoed by explicit coprime divisors with residue 2 modulo 3.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt

def add(P,Q,H,A):
    if P is None: return Q
    if Q is None: return P
    x,y = P
    z,w = Q
    if x == z and (y+w)%H == 0: return None
    a,b = (3*x*x+A,2*y) if P == Q else (w-y,z-x)
    q = gcd(b,H)
    if q != 1: raise ArithmeticError(q)
    s = a*pow(b,-1,H)%H
    u = (s*s-x-z)%H
    return u,(s*(x-u)-y)%H

def mul(M,P,H,A):
    R = None
    for bit in bin(M)[2:]:
        R = add(R,R,H,A)
        if bit == '1': R = add(R,P,H,A)
    return R

def norm(H,r):
    assert (r*r+3)%H == 0
    r %= H
    a,b = H,min(r,H-r)
    while b*b > H: a,b = b,a%b
    d = isqrt((H-b*b)//3)
    assert b*b+3*d*d == H
    return b,d

def sqrt2(H,M):
    L,R,r,parts = H,mul(M,(1,2),H,3),0,[]
    for _ in range(2):
        x,y = R
        q = gcd(y,L)
        if q > 1:
            assert gcd(x,q) == 1 and (x*x+3)%q == 0
            r += x*(H//q)*pow(H//q,-1,q)
            parts.append(q)
            L //= q
        if L == 1: break
        U = (x%L,y%L)
        R = add(U,U,L,3)
    assert L == 1 and (r*r+3)%H == 0
    return r%H,parts

H = (5**65+3**61)//8
assert H%17**2 == 0 and H%17**3 != 0 and pow(-3,8,17) == 16
L,k = H//17**2,80520
assert (80531**2-121**3-k*k)%L == 0
x,y = mul(130262660092933545376435013006001898408516,(121,80531),L,0)
assert gcd(x,L) == 1 and (x**3+4*k*k)%L == 0
a,b = norm(L,y*pow(k,-1,L))
assert (17*a,17*b) == (2768098549348090575904,10506360126495080124225)

Hp,Hm = (5**67+3**83)//8,(5**67-3**83)//2
p = 1320683444989
assert all(p%d for d in range(2,isqrt(p)+1))
assert Hp%p == 0 and pow(-400,(p-1)//3,p) == 802411534424
r,parts = sqrt2(Hp,132348839769809278538674756186242149812520013)
assert parts == [p,Hp//p]
assert norm(Hp,r) == (41827349379466046356144,47331465275177089855419)
M = 605023498120586008376123843929684655283591901
try:
    mul(M,(1,2),Hm,3)
except ArithmeticError as exc:
    assert exc.args == (7,)
else:
    raise AssertionError("expected nonunit denominator")
L = Hm//7
r,parts = sqrt2(L,M)
assert parts == [L]
r += L*((2-r)*pow(L,-1,7)%7)
assert norm(Hm,r) == (102665719348243451525641,88206322459448311121184)

def veto(n,d):
    f = 1
    while n%d == 0: n,f = n//d,f*d
    return f%3 == 2 and gcd(n,f) == 1

panel = (2,17,11,23,59,47,113,233,431,443,467,773,857,1151,1163,1223,1319,
         2111,3533,6833,12377,19163,86813,184013,7697453,15727163,28998017,
         221236013,8022413591,52410884044703651)
assert [m for m in range(2,138,4) if 126 < m < 138] == [130,134]
left = []
for m,E in ((130,190),(134,194)):
    assert 3**E < 5**m < 3**(E+4)
    left.extend((m,e) for e in range(2,E+1,4)
                if not any(veto(5**m-3**e,d) for d in panel))
assert left == [(130,122),(134,166)]

rows = [
 (130,122,2768098549348090575904,10506360126495080124225,
          8273769260532091852213,20710685308397005664592,
          [(1,379,53060),(13,11,77)]),
 (134,166,41827349379466046356144,47331465275177089855419,
          102665719348243451525641,88206322459448311121184,
          [(1,47,188),(29,43,1634)]),
]
for m,e,a,b,c,d,tests in rows:
    A,B = 5**(m//2),3**(e//2)
    assert 8*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B
    Q,Z,v,w = A*A,B*B,8*(a*c-3*b*d),8*(a*d+b*c)
    for j,p,r in tests:
        s = isqrt(Z)
        W,V = max((abs(y),abs(x)) for x,y in
                  [(v,w),((v-3*w)//2,(v+w)//2),
                   ((-v-3*w)//2,(v-w)//2)] if y%3)
        assert s*s == Z and V*V+3*W*W == 4*(Q-Z) and 3*W*W >= Q-Z > 9*Z
        assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
        assert 0 < r < p*p and r%p == 0
        for L in (1,3):
            for t in (W,s+j):
                x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
                S = x*x+y*y
                n = 5*Q+L*Z-S
                R = n-Q-(4-L)*Z
                assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
                if t == W: assert R == V*V+(W+s)**2
                else: assert R > 0 and R%(p*p) == r
        x,y = (Q-Z)//2,(Q+Z)//2
        v,w,Q,Z = x*v-3*y*w,x*w+y*v,Q**3,Z**3

g = list(map(F,("18 166/9 170/9 178/9 182/9 22 70/3 74/3 26 82/3 86/3 30 290/9 "
                "34 110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(99,91)
print("PASS")
~~~
