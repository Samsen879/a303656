# Batched square differences recover a new phase 674/27

For the current old gap (74/3,26), all legal V at the first scale-9 candidates U=113,115 are excluded. The table replay exhausts odd V and verifies fixed exact-valuation witnesses on all points left by the inert-prime panel; even V cannot be a norm modulo 16. At the higher scale the actual coprime seed (337,467) instead supplies both exact signed norms. Finite sieving and ECM aided choosing the seed and some lower-scale witnesses; the supplied high-scale two-half replay starts from whole moduli with no hidden factor inputs.

Adding phase 674/27 gives 36 certified rays. The unique largest remaining ratio is 41/39 at (26,82/3), giving constructive-family effective lower exponent 39/82 (previously 37/78), with arbitrary ε loss in each odd class, 3 or 21 mod 24. The new ray has actual growing exponent pair (674,934)·3^k in the order (5,3). The even/odd cube-depth rotations use net sign sum 0/−1 and give distinct opposite mod-5 values, allowing the established effective sphere count. The replay checks two actual outputs and same-height failed indicated labels with v₂₃=1. This counts generated targets only.

## An exact batch compression

For different integers a,b in {2,…,m+1}, divide the square difference in the Eisenstein ring by its known integer factor a−b. The result is a+b+2ω = t+√(−3), t=a+b−1. Across all such pairs only 2m−3 different t values occur; probe their norms t²+3 with a product tree. A gcd with the remaining full modulus prunes subtrees; accept only verified full coprime prime-power blocks at a leaf, with root −t. These are valid regardless of whether a−b is a unit. On a split prime where both actual evaluated bases and a−b are units, a one-component hit is exactly a separation by the square of their quotient.

At the actual lower-scale (113,145) minus half, corresponding p=67 thresholds on the same finite squared-probe family are 28 bases for one base, 8 for products, and 4 for pair differences; the 3-base batch peels 7 only, while the 4-base batch also peels 67. Its minus half is then a true explicit norm, and the independent total inert valuation veto forces a plus-half failure. On the new (337,467) minus half p=223 has the contrasting thresholds 38,8,40: products can be earlier, so this is not a uniform dominance claim. Here the batch at m=40 compresses 780 pairs to 77 leaf values and visits 25 gcd nodes, extracting 7 and 223 directly from the complete minus half. Exact norm calculation checks all subsequent steps.

~~~python
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import gcd, isqrt, lcm

N = lambda x,y: x*x+3*y*y

def batch(H,m):
    def tree(l,r):
        if r-l==1:
            return (l*l+3)%H,l,None,None
        i = (l+r)//2
        a,b = tree(l,i),tree(i,r)
        return a[0]*b[0]%H,None,a,b

    h,out,calls = H,[],0
    def visit(T):
        nonlocal h,calls
        n,t,a,b = T
        d = gcd(h,n)
        calls += 1
        if d==1:
            return
        if t is None:
            visit(a)
            visit(b)
        else:
            d //= gcd(d,pow(h//d,h.bit_length(),d))
            if d>1:
                assert gcd(d,h//d)==1
                out.append((d,(-t)%d))
                h //= d
    visit(tree(4,2*m+1))
    return out,h,calls

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
    h,r = H,0
    for d,z in parts:
        assert h%d==0 and gcd(d,H//d)==1 and (z*z+3)%d==0
        r += z*(H//d)*pow(H//d,-1,d)
        h //= d
    assert h==1
    r %= H
    assert (r*r+3)%H==0
    a,b = H,min(r,H-r)
    while b*b>H:
        a,b = b,a%b
    c = isqrt((H-b*b)//3)
    assert N(b,c)==H
    return b,c

def thresholds(p):
    a = range(2,42)
    z = {i:(i*i-1,2*i-1) for i in a}
    def hit(x,y):
        return y%p!=0 and (x*x-x*y+y*y)%p==0
    s = min(i-1 for i in a for e in (-1,1)
            if hit(z[i][0]-e,z[i][1]))
    t = 41
    for i,j in combinations_with_replacement(a,2):
        x,y = z[i]
        u,v = z[j]
        X,Y = x*u-y*v,x*v+y*u-y*v
        if hit(X-1,Y) or hit(X+1,Y):
            t = min(t,j-1)
    d = min(j-1 for i,j in combinations(a,2)
            if hit(z[i][0]-z[j][0],z[i][1]-z[j][1]))
    return s,t,d

assert thresholds(67)==(28,8,4) and thresholds(223)==(38,8,40)

# Exhaustion at scale 9. Even V gives 25**U-9**V == 8 mod 16.
P2 = [p for p in range(2,20000,3)
      if all(p%d for d in range(2,isqrt(p)+1))]
D = {
  113:{3:84377,41:8958857,51:56093,81:6973757408158234766165453,
       91:40059728297,123:61007,145:991051449014214313489628324003,
       147:744263293171973},
  115:{19:3063115439323757,43:164549695441441472636098838370191,
       51:4180097093,83:15627486604005165716273,91:46103,
       107:64313455538993,131:32057},
}
def veto(h,d):
    k = 1
    while h%d==0:
        h //= d
        k *= d
    return k%3==2 and gcd(h,k)==1

for U,end in ((113,165),(115,167)):
    assert 3**end<5**U<3**(end+2)
    left = {v for v in range(1,end+1,2)
            if not any(veto(25**U-9**v,p) for p in P2)}
    assert left==D[U].keys()
    assert all(veto(25**U-9**v,D[U][v]) for v in left)

A,S = 5**113,3**145
H = (A-S)//2
assert batch(H,3)[0]==[(7,2)]
p,h,_ = batch(H,4)
assert p==[(7,2),(67,59)]
u = cubic(h,2,lcm(*(i for i in range(1,513) if i%3)))
h //= u[0]
assert u[0]==186583
assert recover(H,p+[u,cubic(h,13,strip3(h-1))])==(
    712692616649604072467461661006842232479,
    1198178352664290256996635855826393026640)

# Two exact integer half-norms for the new ray.
A,S = 5**337,3**467
Hm,Hp = (A-S)//2,(A+S)//32
assert Hm%2==Hp%2==1 and gcd(337,467)==1
parts,h,calls = batch(Hm,40)
assert parts==[(7,2),(223,144)] and calls==25
m = recover(Hm,parts+[cubic(h,2,strip3(h-1))])
p = tuple(2*t for t in recover(Hp,[cubic(Hp,2,strip3(Hp-1),1)]))
assert m==(
  3141770302096624468119425408136902600450154175477730752123495604632059933843786694738473084185044527337421252483879363,
  1631814670609171971741900300112851127132075425761333977171165663852020115801461000819499863970112497717455507172593050)
assert p==(
  1643062136873812754576781745173341440199083016641164727747648071368177715328894630311918982729756482321873619257496186,
  767059604717665653467603919601239416539488249131226427719089156644432029359514328308516699762556207132126170053781884)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def rot(x,y):
    return (x,y),((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

a,b = m
c,d = p
Q,Z = A*A,S*S
x,y = 8*(a*c-3*b*d),8*(a*d+b*c)
assert (x%15,y%15)==(4,6) and 1000*Z<Q
assert all(48*w*w>=4*(Q-Z) for _,w in rot(x,y))
for X,Y,rr in [(x,y,[5,14]),(8*x+6*y,-2*x+8*y,[10,14])]:
    assert sorted(w%15 for _,w in rot(X,Y) if w%3)==rr
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in rr}=={1,4}

W,V = max((abs(w),abs(v)) for v,w in rot(x,y) if w%3)
assert W>3*S and N(V,W)==4*(Q-Z)
for L in (1,3):
    for t in (W,S+1):
        x,y = (t-S,t) if L==1 else (t+S,t-2*S)
        n = 5*Q+L*Z-x*x-y*y
        R = n-Q-(4-L)*Z
        assert Q<n<5*Q and n%24==(21 if L==1 else 3) and R>0
        assert R==V*V+(W+S)**2 if t==W else R%23**2==23

old = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9 206/9
70/3 218/9 74/3 26 82/3 86/3 30 278/9 290/9 298/9 314/9 34 110/3 38
118/3 122/3 42 130/3 134/3 46 142/3 146/3 50 470/9 158/3 54""".split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)

assert len(old)==36 and gaps(old)[0]==(F(39,37),F(74,3),F(26))
assert F(74,3)<F(674,27)<F(26)
new = sorted(old+[F(674,27)])
g = gaps(new)
assert len(new)==37 and g[0]==(F(41,39),F(26),F(82,3)) and g[1][0]<g[0][0]
~~~
