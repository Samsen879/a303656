# A fixed-trace shared-weight branch certifies a new Eisenstein support and phase

Fix normalized inputs u=(1+kr/7)/2 and v=(1+kr/15)/2 at r²=−3. Both have trace one, keeping the prior bases 4+ω and 8+ω fixed at k=1. At a good split prime, u²=v³ with nonzero v lets τ=u/v, hence u=τ³ and v=τ². Eliminating kr gives (τ−2)(7τ²−τ−2)=0. The conjugate residual is (1−τ³)²−(1−τ²)³=τ²(τ−1)²(2τ²+4τ+3). When 57 is a nonsquare and p∤2·3·5·7·19, only τ=2 is possible. This is the exact weight condition 105²+3k²=0 at the rational prime and gives conjugate residual 76, so the governing congruence is one-sided. Its two weight classes on 67 are ±12, lifting to ±414 on 67².

On the actual whole (113,145) minus half, the weighted rule extracts 67 where all tested old same-degree and original-weight probes on these same bases miss. The actual (127,147) half lifts the weight without a factor-input gcd; the separate inert veto 35268137 prevents that label from becoming a true ray. This isolates local support rather than confusing it with both signed norms.

The coprime seed (371,219) independently gives both signed half-norms and a new phase 742/27. Growth is (742,438)·3^k in the order (5,3). Initial label search used finite sieving and ECM; plus-side smoothness was informed by discovery. The arithmetic replay starts from the whole half moduli and requires no supplied factorization. In the 39-ray order the unique largest ratio is 89/85 at (170/9,178/9), improving the effective constructive-population exponent from 41/86 to 85/178 with ε loss, in each odd class 3/21 mod24. Its actual target and failed-label checks and two orientation characters are explicit. Lower-scale U=125/127 are not exhausted in this note; global density and arbitrary n are not claimed.

~~~python
from fractions import Fraction as F
from math import gcd, isqrt, lcm

N = lambda x,y: x*x+3*y*y

def weight(H,k):
    g = gcd(H,105**2+3*k*k)
    L = H.bit_length()
    d = gcd(H,pow(g,L,H))
    d //= gcd(d,pow(2*3*5*7*19*k,L,d))
    if d==1:
        return None
    assert gcd(d,H//d)==1
    while (105**2+3*k*k)%d:
        k = (k-(105**2+3*k*k)*pow(6*k,-1,d))%d
    r = 105*pow(k,-1,d)%d
    assert (r*r+3)%d==0
    return d,k,r

def sheets(d,k,r):
    return [((7+k*R)*pow(14,-1,d)%d, (15+k*R)*pow(30,-1,d)%d)
            for R in (r,-r)]

H = (5**113-3**145)//2
assert N(712692616649604072467461661006842232479,
         1198178352664290256996635855826393026640)==H
assert [weight(H,k) for k in range(1,12)]==[None]*11
assert weight(H,12)==(67,12,59)
assert pow(57,33,67)==66 and (105**2+3)%67==40
assert [k for k in range(1,67) if (105**2+3*k*k)%67==0]==[12,55]
assert gcd(H,124)==1 and gcd(H,9373)==7  # 同底旧平方差、三次差的范数
for u,v in sheets(67,1,59):
    assert (u*u-v**3)%67!=0
for u,v in sheets(67,12,59):
    assert (u*u-v*v)%67!=0 and (u**3-v**3)%67!=0
assert sheets(67,12,59)==[(8,4),(60,64)]

H = (5**127-3**147)//2
assert gcd(H,105**2+3*12**2)==67
assert weight(H,12)==(4489,414,1399)
assert sheets(4489,414,1399)==[(8,4),(4482,4486)]
d = 35268137
assert d%3==2 and H%d==0 and gcd(d,H//d)==1

def strip3(n):
    while n%3==0:
        n //= 3
    return n

def cubic(H,b,e,j=0):
    z = pow(b,e*3**j,H)
    d = gcd(H,z*z+z+1)
    assert d>1 and gcd(d,H//d)==1
    return d,(2*z+1)%d

def recover(H,parts):
    r,h = 0,H
    for d,z in parts:
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

A,S = 5**371,3**219
Hm,Hp = (A-S)//2,(A+S)//8
assert Hm%2==Hp%2==1 and gcd(371,219)==1
m = recover(Hm,[cubic(Hm,2,strip3(Hm-1),3)])
L = lcm(*(i for i in range(1,16562) if i%3))
d,r = cubic(Hp,2,L)
assert d==30804453661
h = Hp//d
p = recover(Hp,[(d,r),cubic(h,7,strip3(h-1))])
assert m==(
  2522249378021882991641959791689182385548763566495822059549798578648633339593017869188080792681083310227695209925346621266358170999,
  1159549889786711392279698153426126723149397876332569941992339940905567810210530287640832710240209645293018106449711266694305714076)
assert p==(
  903859216347029331700233193197294838788371285645021269362853564962022398615493546276935886037592093556806876762008076814747818334,
  770690374152888722659910775339778211399142324012693433967396910200812223368080273063910057870532368755528554445449107139106399109)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def mul(z,w):
    a,b = z
    c,d = w
    return a*c-3*b*d,a*d+b*c

def rot(z):
    x,y = z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

Q,Z = A*A,S*S
z = tuple(8*t for t in mul(m,p))
assert tuple(t%15 for t in z)==(2,0) and 1000*Z<Q
assert min(48*w*w for _,w in rot(z))>=4*(Q-Z)

q,s,zj = Q,Z,z
for rr in ([4,10],[4,5]):  # 深度 1、2
    zj = mul(zj,((q-s)//2,(q+s)//2))
    q,s = q**3,s**3
    assert N(*zj)==4*(q-s)
    assert sorted(w%15 for _,w in rot(zj) if w%3)==rr
    for L0 in (1,3):
        assert {pow(3*w*w+8*L0,2,5) for w in rr}=={1,4}

W,V = max((abs(w),abs(v)) for v,w in rot(z) if w%3)
assert W>3*S and N(V,W)==4*(Q-Z)
for L0 in (1,3):
    for t in (W,S+5):
        x,y = (t-S,t) if L0==1 else (t+S,t-2*S)
        n = 5*Q+L0*Z-x*x-y*y
        R = n-Q-(4-L0)*Z
        assert Q<n<5*Q and n%24==(21 if L0==1 else 3) and R>0
        assert R==V*V+(W+S)**2 if t==W else R%49==35

P = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9 206/9
70/3 218/9 74/3 674/27 26 710/27 82/3 86/3 30 278/9 290/9 298/9 314/9 34
106/3 110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 146/3 50 470/9 158/3 54""".split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)

assert len(P)==39 and gaps(P)[0]==(F(43,41),F(82,3),F(86,3))
P = sorted(P+[F(742,27)])
g = gaps(P)
assert len(P)==40 and g[0]==(F(89,85),F(170,9),F(178,9)) and g[1][0]<g[0][0]
~~~
