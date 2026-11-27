# Whole-modulus cubic roots certify a new phase 218/9

The coprime native seed (109,149) is certified without supplying prime factors or prime-group orders to the discovery procedure. Its two signed halves are recovered from full composite moduli by modular powering, gcd, CRT and a final exact Cornacchia check. The exponent ray is (218,298)·3^k in the order (5,3). This adds phase 218/9 and splits the old largest gap (70/3,74/3) into ratios 109/105 and 111/109.

The unique largest gap of the resulting 33-ray catalogue is (142/3,50), ratio 75/71. The effective lower exponent for the constructed population rises from 35/74 to 71/150, with the usual ε loss, in each of classes 3 and 21 modulo 24. This does not improve the separate density bound or show that prescribed integers are represented.

## Recovery rule and actual gates

For the current odd residual h, use s equal to the prime-to-3 part of h−1, to the LCM of positive integers ≤ B excluding multiples of 3, or to their LCM. Each is prime to 3. For a small unit b, test z=b^(s·3^j) modulo h, and extract D=gcd(h,z²+z+1) when D is coprime to h/D. Then (2z+1)²≡−3 modulo D. At p≠3, if ord_p(b)=3^e d with 3∤d, the p component passes the mod-p test precisely if e≥1, d|s and j=e−1. The algorithm recovers only full coprime blocks; this prime-level criterion by itself does not promise the needed prime-power coverage.

The minus half closes even at B=1. The plus half first peels 331; its actual residual contains p=1135819 and h−1≡67 modulo 709. All eight tested bases have order divisible by 709 modulo p, so B<709 cannot cover that prime at this residual for these rules. B=709 succeeds with base 5, of order 9·89·709 modulo p, and then the remaining block closes. This is an exact threshold on the stated path and base set, not a universal minimum for all methods.

Modulo 331 at this same valid plus half, the single fixed E₂ point (1,2) is killed by 83 and has no nontrivial two-torsion in its cyclic subgroup. On the single fixed E₃ curve y²=x³+120², [10](9,123)=(0,−120) and [30](9,123)=O. Any point with y/120 a root of −3 must have x³=−4·120², x≠0; substituting in the tangent rule gives [2]P=−P. The possible nonidentity three-torsion points in the fixed cyclic subgroup are instead (0,±120). Thus arbitrary scalar choices on these two particular old orbits cannot recover a root on this block. Other starting points are not excluded.

The same elementary rule fully recovers only two of the four signed halves from the independently certified (101,109),(103,77) seeds within the tested B≤768 path. This demonstrates test-specific incomplete discovery. For actual (109,5), the minus half is a norm but the plus half has inert v83=1 and is genuinely impossible. The replay distinguishes each of these claims.

## Effective rotations and exact replay

The cube factors are inverses modulo 15; choose net sign sum 0 at even depth and 1 at odd depth. Two rotated second coordinates give opposite nonzero quadratic characters of 3w²+2LZ modulo 5 for each L=1,3. The base angular lower bound and cumulative drift <1/32 ensure w remains a constant fraction of √Q; the effective sphere count can therefore avoid the single exceptional discriminant using distinct squarefree kernels. Exact same-height positive outputs and failed prescribed labels (v31=1) are checked below.

~~~python
from math import gcd, isqrt, lcm
from fractions import Fraction as F

bases = (2,5,7,3,11,13,17,19)
N = lambda x,y: x*x+3*y*y

def cover(H, B):
    L = lcm(*(i for i in range(1,B+1) if i%3))
    h,r,parts = H,0,[]

    def peel(h):
        if h%3 != 1:
            return None
        a = h-1
        while a%3 == 0:
            a //= 3
        for b in bases:
            if gcd(b,h) != 1:
                continue
            for s in (a,L,lcm(a,L)) if L>1 else (a,):
                z = pow(b,s,h)
                for _ in range(9):
                    if z == 1:
                        break
                    d = gcd(z*z+z+1,h)
                    if d>1 and gcd(d,h//d)==1:
                        return d,(2*z+1)%d
                    z = pow(z,3,h)

    while h>1:
        step = peel(h)
        if step is None:
            return parts,h,None
        d,z = step
        assert (z*z+3)%d==0 and gcd(d,H//d)==1
        r += z*(H//d)*pow(H//d,-1,d)
        h //= d
        parts.append(d)

    r %= H
    assert (r*r+3)%H==0
    a,b = H,min(r,H-r)
    while b*b>H:
        a,b = b,a%b
    c = isqrt((H-b*b)//3)
    assert N(b,c)==H
    return parts,1,(b,c)

A,S = 5**109,3**149
Hm,Hp = (A-S)//2,(A+S)//8
m = (44540214916596693909147796170771609689,
     43664735458509364174066078461108940840)
p = (25496589837608381188550560555659227237,
     20622554539685243520855475748409300088)
assert 2*N(*m)==A-S and 8*N(*p)==A+S
assert cover(Hm,1)==([7,Hm//7],1,m)
assert cover(Hp,708)==([331],Hp//331,None)
assert cover(Hp,709)==([331,1135819,Hp//(331*1135819)],1,p)

q = 1135819
assert all(all(n%d for d in range(2,isqrt(n)+1))
           for n in (q,709,89,331,83,31))
assert (Hp//331-1)%709==67
assert all(pow(b,(q-1)//709,q)!=1 for b in bases)
o = 9*89*709
assert pow(5,o,q)==1 and all(pow(5,o//d,q)!=1 for d in (3,89,709))

assert cover((5**101+3**109)//8,1)[1]==1
assert cover((5**103-3**77)//2,1)[1]==1
assert cover((5**101-3**109)//2,768)[0]==[7,223]
assert cover((5**103+3**77)//128,768)[0]==[]

def emul(n,a,P):
    q = 331
    def add(P,T):
        if P is None: return T
        if T is None: return P
        x,y = P
        u,v = T
        if x==u and (y+v)%q==0: return None
        d,e = (3*x*x+a,2*y) if x==u else (v-y,u-x)
        t = d*pow(e,-1,q)%q
        w = (t*t-x-u)%q
        return w,(t*(x-w)-y)%q
    R = None
    for bit in bin(n)[2:]:
        R = add(R,R)
        if bit=='1': R = add(R,P)
    return R

assert emul(83,3,(1,2)) is None
assert emul(10,0,(9,123))==(0,211)
assert emul(30,0,(9,123)) is None

B = 3**5
assert (A-B)//2 == N(77165686217613678471997606132270841527,
                      24146612240738380650482428083265300648)
assert ((A+B)//8)%83**2==32*83

def rot(z):
    x,y = z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

a,b = m
c,d = p
Q,Z = A*A,S*S
x,y = 8*(a*c-3*b*d),8*(a*d+b*c)
assert (x%15,y%15)==(14,11)
assert 10000*Z<Q and all(300*w*w>=4*(Q-Z) for _,w in rot((x,y)))
for z,want in [((x,y),[5,11]),((8*x-6*y,2*x+8*y),[10,11])]:
    assert sorted(w%15 for _,w in rot(z) if w%3)==want
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in want}=={1,4}

W,V = max((abs(w),abs(v)) for v,w in rot((x,y)) if w%3)
assert W>3*S and N(V,W)==4*(Q-Z)
for L in (1,3):
    for t in (W,S+29):
        x,y = (t-S,t) if L==1 else (t+S,t-2*S)
        n = 5*Q+L*Z-x*x-y*y
        R = n-Q-(4-L)*Z
        assert Q<n<5*Q and n%24==(21 if L==1 else 3) and R>0
        assert R==V*V+(W+S)**2 if t==W else R%31**2==6*31

P = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9 206/9
70/3 74/3 26 82/3 86/3 30 278/9 290/9 314/9 34 110/3 38 118/3 122/3
42 130/3 134/3 46 142/3 50 470/9 158/3 54""".split()))
P = sorted(P+[F(218,9)])
g = sorted(((b/a,a,b) for a,b in zip(P,P[1:])), reverse=True)
assert g[0]==(F(75,71),F(142,3),F(50)) and g[1][0]<g[0][0]
~~~
