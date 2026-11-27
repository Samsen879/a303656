# Primitive rational weight boxes add real support and certify phase 266/9

A selected trace branch has kr=C with r²=−3. Allowing rational k=Cb/a converts its weight equation to a²+3b²=0 in the verified component, for primitive coordinates 1≤a,b≤W. For an odd full half modulus H coprime to 6, a gcd at a primitive leaf means both coordinates are units there. Use a product tree to find actual leaves; saturate their gcds to the full prime-power depths of H and apply modular Newton lifting to r=a/b. The method acts on support, not on the product's accidental aggregate valuation. If p is a split prime below (W+1)², the pigeonhole principle on i+jr in the (W+1)-square guarantees a nonzero coordinate difference, both nonzero when p>W; taking absolute values and removing common divisors produces a valid leaf. The p≤W case uses a shortest root and b=1. Conversely no leaf detects primes above 4W².

At W=15 the 143 primitive leaves decisively differ from a 160-leaf five-trace integer-weight benchmark. On the full actual (133,37) plus half the benchmark detects 19, while the new box detects 19·709. Their verified CRT common root is 3291 mod 13471, and τ=−1/3 gives least positive common weight 795. The 1381 component, although compatible with the chosen discriminant, exceeds 900 and is genuinely missed. On the full (131,115) minus half the box adds 223 to the older 7·367 support, and switching τ from −1/3 to +1/3 genuinely changes the quadratic discrimination at 223. Actual (131,19) verifies the shallow 7 leaf lifting to full 49 and root 37.

Separately the coprime (133,23) seed has both exact integer half-norms, giving phase 266/9 and genuine growing ray (266,46)·3^k in the (5,3) order. Discovery used exponent-label sieving and ECM; this certification uses exact integer substitutions and does not infer the ray from the partial boxes. The 41-ray catalogue's unique largest gap is (50,470/9), ratio 47/45; constructive-family effective exponent improves to 45/94 in each actual odd class 3 and 21 mod24 with ε loss. The parity-dependent rotated chars, actual same-height positive controls and v47=1 failed indicated labels are replayed. This count says nothing new about the natural-density bound or an arbitrary prescribed target. U=131 is still not exhausted.

~~~python
from fractions import Fraction as F
from itertools import product
from math import gcd, prod

def N(a,b):
    return a*a+3*b*b

P=[((a,b),N(a,b)) for a,b in product(range(1,16),repeat=2) if gcd(a,b)==1]
T=((-1,3,21),(1,3,21),(2,3,3),(2,1,7),(4,5,35))
I=prod((t*(2*a**3-b**3))**2+3*b**6*k*k
       for a,b,t in T for k in range(1,33))
assert len(P)==143

def blocks(H,P):
    if gcd(H,prod(n for _,n in P))==1:
        return []
    if len(P)==1:
        (a,b),n=P[0]
        d=gcd(H,pow(gcd(H,n),H.bit_length(),H))
        r=a*pow(b,-1,d)%d
        while (r*r+3)%d:
            r=(r-(r*r+3)*pow(2*r,-1,d))%d
        return [(d,r)]
    i=len(P)//2
    left=blocks(H,P[:i])
    return left+blocks(H//prod(d for d,_ in left),P[i:])

def err(t,s,k,r,p):
    uv=[((t+k*x)*pow(2*t,-1,p)%p,(s+k*x)*pow(2*s,-1,p)%p)
        for x in (r,-r)]
    return [(u*u-v**3)%p for u,v in uv]

def crt(a,b,p,q):
    return a+p*((b-a)*pow(p,-1,q)%q)

H=(5**133+3**37)//8
assert gcd(H,I)==19
(p,r),(q,s)=blocks(H,P)
assert (p,q)==(19,709)
assert H%1381==0 and 1381>4*15**2
assert all(pow(2,(j-1)//2,j)==j-1 for j in (p,q,1381))
ks=sorted(crt(-609*pow(27*x,-1,p)%p,-609*pow(27*y,-1,q)%q,p,q)
          for x,y in product((r,-r),(s,-s)))
assert ks==[795,1504,11967,12676]
k=ks[0]
d=gcd(H,609**2+3*27**2*k*k)
R=-609*pow(27*k,-1,d)%d
assert (d,R)==(13471,3291)
for j in (p,q):
    e,f=err(21,29,k,R,j)
    assert e==0 and f!=0

H=(5**131-3**115)//2
assert gcd(H,I)==7*367
assert sorted(d for d,_ in blocks(H,P))==[7,223,367]
assert pow(2,111,223)==1 and pow(92,111,223)==222
H=(5**131-3**19)//2
assert gcd(H,7)==7 and blocks(H,[((2,1),7)])==[(49,37)]
assert err(3,11,6,37,49)[0]==0 and err(3,11,6,37,49)[1]%7!=0

A,S=5**133,3**23
m=(20545392562693284644384637886087735400246635261,
   3514935999169995489797558912862627624253200474)
p=(996465818327706923877110216328632044839102412,
   6159042838796558433682659260361950264266519400)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def mul(z,w):
    x,y=z
    a,b=w
    return x*a-3*y*b,x*b+y*a

def rot(z):
    x,y=z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

Q,Z=A*A,S*S
z=tuple(8*t for t in mul(m,p))
assert N(*z)==4*(Q-Z) and Q>1000*Z
assert all(29*w*w>=4*(Q-Z) for _,w in rot(z))
assert (Q%30,Z%30)==(25,9)
assert tuple(t%15 for t in mul((8,2),(8,-2)))==(1,0)
u=z
for j in (1,2):
    q,s=Q**(3**(j-1)),Z**(3**(j-1))
    u=mul(u,((q-s)//2,(q+s)//2))
    assert N(*u)==4*(q**3-s**3)
    ww=sorted(w%15 for _,w in rot(u) if w%3)
    assert ww==[5,14]
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in ww}=={1,4}

W,V=max((abs(w),abs(v)) for v,w in rot(z) if w%3)
for L in (1,3):
    for t in (W,S+5):
        x,y=(t-S,t) if L==1 else (t+S,t-2*S)
        n=5*Q+L*Z-x*x-y*y
        R=n-Q-(4-L)*Z
        assert Q<n<5*Q and R>0 and n%24==(21 if L==1 else 3)
        if t==W:
            assert R==V*V+(W+S)**2
        else:
            assert R%47**2==29*47

P=sorted(map(F,'''18 166/9 170/9 514/27 178/9 182/9 62/3 190/9 22
202/9 206/9 70/3 218/9 74/3 674/27 26 710/27 82/3 742/27 86/3
30 278/9 290/9 298/9 314/9 34 106/3 110/3 38 118/3 122/3 42
130/3 134/3 46 142/3 146/3 50 470/9 158/3 54'''.split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)
assert len(P)==41 and gaps(P)[0]==(F(45,43),F(86,3),F(30))
g=gaps(sorted(P+[F(266,9)]))
assert g[0]==(F(47,45),F(50),F(470,9)) and g[1][0]<F(47,45)
assert F(45,94)-F(43,90)==F(2,2115)
print("PASS")
~~~
