# Cubic differences and leafwise lifts certify phase 710/27

The first scale-9 choices in the gap (26,82/3), U=119 and U=121, are fully obstructed at native height. The higher-scale coprime (355,201) seed instead gives phase 710/27 and exact signed integral half-norms. Adding it creates a 37-ray catalogue; the unique largest ratio is 165/157 at (314/9,110/3). The effective constructed-population exponent in each of 3 and 21 mod 24 is 157/330, up from 39/82, with the usual ε loss. It measures only generated targets. The two actual eigenvalue orientations and same-height controls (a true norm and a failed label v19=1) are checked in the replay; no new natural density or arbitrary-n claim follows.

## Same-window comparisons and safe deepening

For ω²+ω+1=0, dividing the cube difference of a+ω,b+ω by the known integer a−b yields the product of (a+1+(2−b)ω) and (a+b−1+(b+1)ω). A linear query x+yω gives the root 1−2x/y when y is a unit. With (a,b)=(3,4), the square difference quotient has norm 39, whereas the cubic quotient 34+18ω has norm 868. At 7 the actual ratio on the distinguished evaluation component has order 3. Thus the cubic probe captures a genuine support missed by the square probe at the same two bases, not by extending the base range.

For a leaf with partial support gcd(h,N(x+yω)), first saturate to the prime-power blocks of h, then remove those sharing prime support with y. The linear root is good mod each prime. Since the modulus here is odd and prime to 3, 2r is a unit and Newton iteration r←r−(r²+3)/(2r) doubles each local precision without using the prime factors or their exponents.

The proof distinguishes a root of a particular leaf from a large product gcd. At the true (21,21) minus half, the three cubic leaves have gcds 7,43,49, and their product captures full 343. Two leaves giving 7 have opposite first digits mod 7, so the product depth alone never specifies a root. The first leaf actually lifts 264→208→306 mod 343 and then recovers the whole exact norm. The (121,149) case independently lifts a visible 7 to 49. Label discovery used finite sieving and ECM, while the supplied support and norm verification requires only the stated arithmetic.

~~~python
from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt, prod

N = lambda x,y: x*x+3*y*y
E = lambda x,y: x*x-x*y+y*y

def cube(a,b):
    return a*a+a*b+b*b-3, 3*(a+b-1)

def lift(h,x,y):
    L = h.bit_length()
    d = gcd(h,pow(gcd(h,E(x,y)),L,h))
    d //= gcd(d,pow(y,L,d))
    if d==1:
        return None
    assert gcd(d,h//d)==1 and gcd(y,d)==1
    r = (y-2*x)*pow(y,-1,d)%d
    hist = [r]
    while (r*r+3)%d:
        r = (r-(r*r+3)*pow(2*r,-1,d))%d
        hist.append(r)
        assert len(hist)<=L.bit_length()+1
    return d,r,hist

def batch(H,P):
    def tree(P):
        if len(P)==1:
            return E(*P[0])%H,P[0],None,None
        k = len(P)//2
        a,b = tree(P[:k]),tree(P[k:])
        return a[0]*b[0]%H,None,a,b

    h,out = H,[]
    def visit(T):
        nonlocal h
        n,t,a,b = T
        if gcd(h,n)==1:
            return
        if t is None:
            visit(a)
            visit(b)
        else:
            q = lift(h,*t)
            if q:
                d,r,_ = q
                out.append((d,r))
                h //= d
    visit(tree(P))
    return out,h

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

C = cube(3,4)
assert C==(34,18) and E(*C)==868 and E(7,2)==39

H = (5**119-3**151)//2
assert gcd(H,39)==1 and lift(H,*C)==(7,5,[5])
assert recover(H,[(7,5),(H//7,
    10381057263509082930731861745658749736001320582970178946688898620888475371260227599)]) == (
    260247670817815572064007248537743453658609,
    50009293422900650812837599499007648739044)

H = (5**121-3**149)//2
assert gcd(H,39)==1 and gcd(H,868)==7
assert lift(H,*C)==(49,12,[19,12])
d = 48371
assert d%3==2 and H%d==0 and gcd(d,H//d)==1  # 全半部的惰性否决

H = (5**21-3**21)//2
P = [cube(a,b) for a,b in combinations((3,4,5),2)]
assert gcd(H,39*52*67)==1
assert [gcd(H,E(*x)) for x in P]==[7,43,49]
assert gcd(H,prod(E(*x) for x in P))==343*43
assert lift(H,*P[0])==(343,306,[264,208,306])
assert lift(H,*P[2])==(343,37,[282,37])
q,h = batch(H,P)
assert q==[(343,306),(43,13)] and h==16164712789
assert recover(H,q+[(h,10761516792)])==(13162969,4660100)

# 缩放 9 的完整否决。偶 V 给 25**U-9**V ≡ 8 mod 16。
small = [p for p in range(2,20000,3)
         if all(p%d for d in range(2,isqrt(p)+1))]
D = {
 119:{23:13736117,39:13358628716384879,79:128657,143:53874551,
      149:26513,151:1511303,165:38459},
 121:{1:30971,25:116927,57:80783,59:2650939163,83:24659,
      89:62145807313579079,91:30293,107:34391702573,139:209697893,
      145:195413,161:52571,169:58067,171:147033760697},
}
def veto(h,d):
    q = 1
    while h%d==0:
        h //= d
        q *= d
    return q%3==2 and gcd(q,h)==1

for u,end in ((119,173),(121,177)):
    assert 3**end<5**u<3**(end+2)
    left = {v for v in range(1,end+1,2)
            if not any(veto(25**u-9**v,p) for p in small)}
    assert left==D[u].keys()
    assert all(veto(25**u-9**v,D[u][v]) for v in left)

# 高尺度真种子。两半的恢复只输入完整模数和小底。
def cubic(H,b,j):
    e = H-1
    while e%3==0:
        e //= 3
    r = (2*pow(b,e*3**j,H)+1)%H
    assert (r*r+3)%H==0
    return r

A,S = 5**355,3**201
Hm,Hp = (A-S)//2,(A+S)//32
assert Hm%2==Hp%2==1 and gcd(355,201)==1
m = recover(Hm,[(Hm,cubic(Hm,7,0))])
p = tuple(2*t for t in recover(Hp,[(Hp,cubic(Hp,2,1))]))
assert m==(
  8053252048479775630379085409217513833733532471112530171512008699412739561017225014314699670375538373792712310579497071737569,
  1044427895035795670934454445669292602107759095859784328528207971840758939117836816900078562751989131576492603912292975185810)
assert p==(
  1817019146604558562124269790044582941108361512003826974680620609012260602002368306115507730248515264817504557771933298565132,
  2139336406529296068231216082592387417966070711093117153054109693762789586371915006096279705048977806313808241087680908247442)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def mul(z,w):
    x,y = z
    a,b = w
    return x*a-3*y*b,x*b+y*a

def rot(z):
    x,y = z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

Q,Z = A*A,S*S
z = tuple(8*t for t in mul(m,p))
assert tuple(t%15 for t in z)==(4,4) and 1000*Z<Q
assert all(48*w*w>=4*(Q-Z) for _,w in rot(z))
for T,rr in [((8,2),[10,14]),(mul((8,2),(8,2)),[5,14])]:
    assert sorted(w%15 for _,w in rot(mul(z,T)) if w%3)==rr
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in rr}=={1,4}

W,V = max((abs(w),abs(v)) for v,w in rot(z) if w%3)
assert W>3*S and N(V,W)==4*(Q-Z)
for L in (1,3):
    for t in (W,S+13):
        x,y = (t-S,t) if L==1 else (t+S,t-2*S)
        n = 5*Q+L*Z-x*x-y*y
        R = n-Q-(4-L)*Z
        assert Q<n<5*Q and n%24==(21 if L==1 else 3) and R>0
        assert R==V*V+(W+S)**2 if t==W else R%19**2==3*19

P = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9 206/9
70/3 218/9 74/3 674/27 26 82/3 86/3 30 278/9 290/9 298/9 314/9 34 110/3 38
118/3 122/3 42 130/3 134/3 46 142/3 146/3 50 470/9 158/3 54""".split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)

assert gaps(P)[0]==(F(41,39),F(26),F(82,3))
P = sorted(P+[F(710,27)])
g = gaps(P)
assert len(P)==38 and g[0]==(F(165,157),F(314,9),F(110,3)) and g[1][0]<g[0][0]
~~~
