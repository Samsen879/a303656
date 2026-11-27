# An elliptic half-norm phase gives twenty-four rays

The [twenty-three-ray construction](https://github.com/Samsen879/a303656/commit/41221211dd508dbbfda85ebb251c1078ce5655da) had its widest multiplicative gap between \(82/3\) and \(30\). A new phase \(86/3\) from \((m,e)=(258,278)\) splits this gap. The new widest ratio is \(23/21\), between \(42\) and \(46\). The existing effective sphere estimate gives uniform generated-population exponent \(21/46\), up to logarithmic loss, in both odd classes. This does not concern preassigned targets.

For \(A=5^{129}\), \(B=3^{139}\), use the two odd halves \((A+B)/2048,(A-B)/2\). On each, scalar multiplication of the same point \((5,15)\) on \(y^2=x^3+100\), with a different displayed scalar, gives \(x^3=-400\) and \(y^2=-300\). The replay explicitly checks invertible denominators and the congruences over each composite modulus, making \(y/10\) a square root of \(-3\). Cornacchia reduction reconstructs the two norm pairs, each verified by an integer identity. No group-order or primality assumption on the halves is necessary for verifying this certificate.

The scale-three candidate \(m=86\) is excluded for all 31 admissible upper exponents by the displayed coprime norm vetoes. In particular \(e=34\) has a positive elliptic certificate for the plus half, but the minus half has a coprime divisor congruent to 2 modulo 3. The scale-nine seed does have both halves. The replay then checks growing actual exponent pairs, positive two-square residuals and perturbed residuals of exact valuation one at an inert prime, both at the seed and its first common cubing. The phase catalogue remains a generated family.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt

def add(P,Q,H):
    if P is None: return Q
    if Q is None: return P
    x,y = P
    z,w = Q
    if x == z and (y+w)%H == 0: return None
    a,b = (3*x*x,2*y) if P == Q else (w-y,z-x)
    s = a*pow(b,-1,H)%H
    u = (s*s-x-z)%H
    return u,(s*(x-u)-y)%H

def mul(M,P,H):
    R = None
    for bit in bin(M)[2:]:
        R = add(R,R,H)
        if bit == '1': R = add(R,P,H)
    return R

def halfnorm(H,k,P,M):
    assert gcd(H,6*k) == 1 and (P[1]**2-P[0]**3-k*k)%H == 0
    x,y = mul(M,P,H)
    assert gcd(x,H) == 1 and (x**3+4*k*k)%H == 0
    r = y*pow(k,-1,H)%H
    assert (r*r+3)%H == 0
    a,b = H,min(r,H-r)
    while b*b > H: a,b = b,a%b
    d = isqrt((H-b*b)//3)
    assert b*b+3*d*d == H
    return b,d

def veto(n,d):
    f = 1
    while n%d == 0: n,f = n//d,f*d
    return f%3 == 2 and gcd(n,f) == 1

panel = (2,17,11,23,47,59,83,173,239,797,248243,379528381571)
assert [m for m in range(2,90,4) if 82 < m < 90] == [86]
assert 3**122 < 5**86 < 3**126
assert all(any(veto(5**86-3**e,d) for d in panel) for e in range(2,123,4))

H = (5**43+3**17)//32
M = 438841035271450960932126352
assert halfnorm(H,226891,(147,226898),M) == (161098645039303,56492959309120)
assert mul(M,(29,12195),H) == (0,12194)

A,B = 5**129,3**139
Mplus = 79718312637145148923661174051846489254021542491133777182563613436660133405270827593437
Mminus = 81631552140436632497828810162887761367585492203211404015067095745529033103518138324188333
a,b = 26476139091867224435566460250626053934027791,2343705934512442516751588789967942786775796
c,d = 828720756612648749298686861077720313732401931,126367027375668276344503946764797184072515166
assert halfnorm((A+B)//2048,10,(5,15),Mplus) == (a,b)
assert halfnorm((A-B)//2,10,(5,15),Mminus) == (c,d)
assert 2048*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B

Q,Z = A*A,B*B
v,w = 128*(a*c-3*b*d),128*(a*d+b*c)
for j,p,rem in [(1,71,1917),(25,79,158)]:
    s = isqrt(Z)
    W,V = max((abs(y),abs(x)) for x,y in
              [(v,w),((v-3*w)//2,(v+w)//2),
               ((-v-3*w)//2,(v-w)//2)] if y%3)
    assert s*s == Z and V*V+3*W*W == 4*(Q-Z) and 3*W*W >= Q-Z > 9*Z
    assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
    assert 0 < rem < p*p and rem%p == 0
    for L in (1,3):
        for t in (W,s+j):
            x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
            S = x*x+y*y
            n = 5*Q+L*Z-S
            R = n-Q-(4-L)*Z
            assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
            if t == W: assert R == V*V+(W+s)**2
            else: assert R > 0 and R%(p*p) == rem
    x,y = (Q-Z)//2,(Q+Z)//2
    v,w,Q,Z = x*v-3*y*w,x*w+y*v,Q**3,Z**3

g = list(map(F,("18 166/9 170/9 178/9 182/9 22 70/3 74/3 26 82/3 86/3 30 290/9 "
                "34 110/3 38 118/3 122/3 42 46 142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(23,21)
print("PASS")
~~~
