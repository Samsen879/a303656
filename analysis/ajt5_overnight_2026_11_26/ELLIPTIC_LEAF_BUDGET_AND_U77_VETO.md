# Elliptic norm leaves improve the same-budget support and settle U=77

A split prime p>3 has a unique positive representation p=a²+3b². In the norm-Euclidean Eisenstein ring either prime ideal has a generator; the unit group maps onto the unit classes modulo 2, so the generator can be brought into the integer suborder. Only signs and conjugation remain there for this odd split prime. This proves the uniqueness needed for a sharp finite-box test.

For p>W² a primitive square leaf with 1≤a,b≤W can only hit p,2p,3p below 4W². Every even primitive Eisenstein-suborder norm has precisely v₂=2, not one, so 2p cannot occur. From 3|a²+3b² follows 3|a; switching to (b,a/3) shows a 3p hit already implies the positive p representation lies within the same box. At W=15 the first missed split prime is 283=16²+3·3². The 143 rectangular leaves are beaten by 124 elliptic primitive opposite-parity leaves with norm ≤900, which contain all split primes ≤900. With 143 elliptic leaves the limit reaches 1039, first missing 1051.

The minimum number under norm limit 900 for that exact split-prime set is actually 71: all 71 primes >30 require distinct bins by their products, and the remaining 7,13,19 can respectively be packed with 61,43,37. More generally a group of distinct split primes can be hit by one primitive leaf under a given norm budget iff their product fits; the forward direction is divisibility, and the reverse direction multiplies their Eisenstein generators and chooses integral suborder coordinates, primitive since the product is squarefree. This criterion pertains to distinct primes, not multiple unrelated full root sign constraints.

Exact actual controls: on the (17,13) minus half the rectangular gcd is 7 and the elliptic gcd is 7·283, with true minus norm and companion plus inert v17=1. On the (77,47) plus odd part the rectangular gcd is 19 and the elliptic gcd is 19·751. The exact shared trace-weight 410 and root 4651 mod 14269, followed by an actual complement cubic root, recover the full norm; the companion minus half fails a coprime 2 mod3 factor. Finally, the replay exhausts V=0,…,112 at U=77 using ordinary small inert valuations and seven remaining coprime exact vetoes. No complete new ray is claimed; higher scales and the current constructive exponent 45/94 are unchanged.

~~~python
from math import gcd, isqrt, prod

def N(a,b):
    return a*a+3*b*b

def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def ellipse(B):
    return sorted((N(a,b),a,b)
        for a in range(1,isqrt(B)+1) for b in range(1,isqrt(B//3)+1)
        if N(a,b)<=B and gcd(a,b)==1 and (a-b)%2 and a%3)

Q=[N(a,b) for a in range(1,16) for b in range(1,16) if gcd(a,b)==1]
E,L=ellipse(900),ellipse(1039)
assert (len(Q),len(E),len(L))==(143,124,143)
P=[p for p in range(7,1052,6) if prime(p)]
assert next(p for p in P if all(n%p for n in Q))==283
assert [p for p in P if any(n%p==0 for n,_,_ in E)]==[p for p in P if p<=900]
assert [p for p in P if all(n%p for n,_,_ in L)]==[1051]
B=[p for p in P if 30<p<=900]
C=[p for p in B if p not in (37,43,61)]+[19*37,13*43,7*61]
assert len(B)==len(C)==71 and set(C)<={n for n,_,_ in E}
assert all(prod(C)%p==0 for p in P if p<=900)

H0=(5**17-3**13)//2
assert H0==381468929401==N(535307,177872)
assert gcd(H0,prod(Q))==7
assert gcd(H0,prod(n for n,_,_ in E))==7*283
assert (5**17+3**13)%17**2==68

A=5**77
H=(A+3**47)//128
assert 128*H==A+3**47 and H%2 and gcd(H,prod(Q))==19
roots=[]
h=H
for n,a,b in E:
    d=gcd(h,n)
    if d>1:
        roots.append((d,a*pow(b,-1,d)%d))
        h//=d
assert roots==[(19,4),(751,606)]
d=gcd(H,105**2+3*125**2*410**2)
r=105*pow(125*410,-1,d)%d
assert (d,r)==(14269,4651)
for p,other in ((19,4),(751,319)):
    assert pow(-87,(p-1)//2,p)==p-1
    dif=[]
    for z in (r,-r):
        u=(35+410*z)*pow(70,-1,p)%p
        v=(3+410*z)*pow(6,-1,p)%p
        dif.append((u*u-v**3)%p)
    assert dif==[0,other]

e=h-1
while e%3==0:
    e//=3
z=pow(2,e,h)
assert (z*z+z+1)%h==0
roots.append((h,(2*z+1)%h))
R=sum(r*(H//d)*pow(H//d,-1,d) for d,r in roots)%H
assert (R*R+3)%H==0
x,y=H,min(R,H-R)
while y*y>H:
    x,y=y,x%y
w=isqrt((H-y*y)//3)
assert (y,w)==(49689534977066616683944559,30004604881136141329737104)
assert N(y,w)==H and 8*N(4*y,4*w)==A+3**47

def oddval(n,p):
    e=0
    while n%p==0:
        n//=p
        e+=1
    return e%2

small=[p for p in range(2,20001,3) if prime(p)]
extra={13:120983462693,23:381047,39:3861059,47:807729579959,
       71:75680634679733,87:3724439,111:20507}
assert 3**112<A<3**113
tail={v for v in range(113) if not any(oddval(A*A-9**v,p) for p in small)}
assert tail==extra.keys()
for v,d in extra.items():
    D=A*A-9**v
    assert d%3==2 and D%d==0 and gcd(d,D//d)==1
assert (A-3**47)%extra[47]==0
print("PASS")
~~~
