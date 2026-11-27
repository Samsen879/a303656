# Twenty-three interlaced sphere rays

Two certified phases \(166/9\) and \(170/9\) fill the gap from \(18\) to \(178/9\) in the [twenty-one-ray construction](https://github.com/Samsen879/a303656/commit/0efe2bcae4361ad6cb315f62a96e3ecfcde2f1cf). Their seeds \((m,e)=(166,54),(170,62)\) certify both odd half-norm factors of \(5^m-3^e\). The replay verifies the four exact positive identities and checks genuinely failing offsets at the seed and its first common cubing. All results are for generated targets, not for a preassigned integer.

For an odd half \(H\) coprime to 3, choose a base \(T\) and exponent \(E=3^a t\), \(3\nmid t\). The gcd with \(T^E-1\) gives candidate prime powers. Remove the partial powers by dividing it by its gcd with \((H/\gcd(H,T^E-1))^{\operatorname{bitlength}(H)}\). On each surviving prime power, the part of the base order contributed by the lift is prime to 3, so the first stage \(j\) at which the order divides \(3^jt\) is the same at the prime and its full power. Remove the powers with \(j=0\). In each coprime block entering at \(j>0\), \(T^{3^{j-1}t}\) solves \(X^2+X+1=0\). CRT then gives a square root of \(-3\), and Cornacchia reconstruction has its output checked by substitution. For \((170,62)\), \(E=\operatorname{lcm}(1,\ldots,42829)\) and base 2 recover the two displayed composite blocks without needing to split them. Each complementary block is checked with its own exponent and base.

Common cubing preserves the phase and extends the half-norm certificate: each new factor is coprime to the old factor (a common prime would divide 3), and the appropriate signed ratio of old powers gives a primitive cubic root on the new factor. Thus no new smooth-order assumption is used along a ray. With \(Q=5^{m3^k}\), \(Z=3^{e3^k}\), and \(s=\sqrt Z\), the existing rotation and sphere construction uses \(V^2+3W^2=4(Q-Z)\). The positive residual is \(V^2+(|W|+s)^2\); the two labels use actual exponent pairs \((e3^k+1,m3^k)\) and \((e3^k,m3^k)\) in classes 21 and 3 modulo 24. Tiny signed perturbations in the same windows give the explicit valuation-one countercontrols in the replay. At scale 3 in the filled gap, the only candidate lower exponent is 58; the exact vetoes below rule out its eligible upper exponents in this mechanism.

On the new cyclic phase catalogue the largest consecutive ratio is \(45/41\), between \(82/3\) and \(30\). Applying the existing effective sphere population estimate at each completed scale gives the uniform generated-population lower exponent \(41/90\) in both classes (up to logarithmic loss). This change improves the earlier \(81/178\) exponent for that catalogue and says nothing about norm coverage at arbitrary inputs.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt, lcm

def veto(n, d):
    f = 1
    while n % d == 0:
        n, f = n//d, f*d
    return f % 3 == 2 and gcd(n, f) == 1

assert [m for m in range(2,60,4) if 486 < 9*m < 534] == [58]
assert 3**82 < 5**58 < 3**86
assert all(any(veto(5**58-3**e,d) for d in
               (2,17,11,47,59,479,1217,3748739,13650977,95876687))
           for e in range(2,83,4))

def strip3(E):
    while E % 3 == 0:
        E //= 3
    return E

def fragment(H,T,E):
    C = gcd(H,pow(T,E,H)-1)
    C //= gcd(C,pow(H//C,H.bit_length(),C))
    return C//gcd(C,pow(T,strip3(E),C)-1)

def root(H,T,E):
    assert fragment(H,T,E) == H
    t, d, r = strip3(E), 1, 0
    while t < E:
        x = pow(T,t,H)
        t *= 3
        n = gcd(H,pow(T,t,H)-1)
        q, d = n//d, n
        if q > 1:
            r += x*(H//q)*pow(H//q,-1,q)
    assert d == H and (r*r+r+1)%H == 0
    return r%H

def reconstruct(H,U,E):
    q = fragment(H,2,E)
    R = H//q
    X,Y = root(q,2,E),root(R,U,R-1)
    z = (X+q*((Y-X)*pow(q,-1,R)%R))%H
    c = (2*z+1)%H
    a,b = H,min(c,H-c)
    while b*b > H:
        a,b = b,a%b
    y = isqrt((H-b*b)//3)
    assert b*b+3*y*y == H
    return q,(b,y)

E = lcm(*range(1,42830))
q1,plus = reconstruct((5**85+3**31)//32,11,E)
q2,minus = reconstruct((5**85-3**31)//2,2,E)
assert E.bit_length() == 61945 and (q1,q2) == (1279*1759,67*18502129)
for p,r,T in ((18502129,42829,2),(736302231271,118567187,5)):
    assert all(r%d for d in range(2,isqrt(r)+1))
    assert (p-1)%r == 0 and pow(T,p-1,p) == 1
    assert pow(T,(p-1)//r,p) != 1
assert ((5**85-3**31)//2)%18502129 == 0
assert ((5**75+3**11)//8)%736302231271 == 0

# m, e, plus 2-adic valuation, plus norm, minus norm, failed controls by depth
rows = [
 (166,54,3,(30412534957042670953870908386,11068685929244466045413195891),
           (13387239116696515798379459287,40786683518393654178791323380),
           [(5,7,35),(1,199,21691)]),
 (170,62,5,(69523028026344851244403101647,32886087451034311333468851448),
           (101460221960206493130527604667,199125416150388502064694049230),
           [(1,179,2685),(5,227,8626)]),
]
assert (plus,minus) == tuple(rows[1][3:5])
for m,e,h,(a,b),(c,d),tests in rows:
    A,B = 5**(m//2),3**(e//2)
    assert 2**h*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B
    f = 2**((h+3)//2)
    Q,Z,v,w = A*A,B*B,f*(a*c-3*b*d),f*(a*d+b*c)
    for j,p,rem in tests:
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
                if t == W:
                    assert R == V*V+(W+s)**2
                else:
                    assert R > 0 and R%(p*p) == rem
        x,y = (Q-Z)//2,(Q+Z)//2
        v,w,Q,Z = x*v-3*y*w,x*w+y*v,Q**3,Z**3

g = list(map(F,("18 166/9 170/9 178/9 182/9 22 70/3 74/3 26 82/3 30 290/9 "
                "34 110/3 38 118/3 122/3 42 46 142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(45,41)
print("PASS")
~~~
