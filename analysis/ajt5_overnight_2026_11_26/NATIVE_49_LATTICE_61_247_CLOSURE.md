# A native 49-precision lattice strictly rejects and closes (61,247)

Fix the existing prime-to-7 smooth L and H=7^(bitlength R). For a word of direction (u,v), Z=(3^u 5^v)^L. The captured support is the saturation of gcd(R,Z^H−1), so each captured prime sees a purely 7-primary value. If the underlying prime passes native (E,k), comparison of the original two axes gives Z^s=x^(s L E(u+kv)), where s=(p−1)_(7′), and cancellation of s is valid inside the 7-group. At u+kv=0 mod49, necessarily Z^7=1, so the captured support minus saturation of gcd with Z^7−1 is strictly rejected. No inference is made on uncaptured primes. With the complete fixed menu E≡e mod49 on a specific k, all seven lifts have the same exact phase for these directions, allowing direct comparison with x^(L e(u+kv)) when needed.

For actual (61,247), the two verified menu bases of determinants 343/49 are ((5,17),(−19,4)) and ((−2,3),(−15,−2)), with k=262,E≡15 mod49. The old halfwidth-2401 box had no captured support, but the 49 lattice first captures at halfwidth 1343 with combination (1343,−777), direction (8969,5583). Its relation is 245 mod343, and its sevenfold old lattice coordinates (2897,−2542) exceed the old box. It directly extracts p=10267249262761 from full R without pre-entering a factor or known order, keeping B=2^19 fixed. Independent Lucas verification certifies p and remaining q=40531309920123069374824111166200974991. The exact raw norm 7R and native root and entire menu are replayed. The first prime has 7-primary orders 2401 on both axes and wrong sign; the second passes sign but the actual pair (257,104) has wrong first phase and ratio. Thus the whole specified native source closes.

The exact certified (70,180) control prime passes 49-projected axes on its (43,324) branch and no full 343 lift. A true order-seven word 3^19 5 on that same root shows exactly what raising to the seventh power forgets. The 49 search is useful but not a replacement for finer individual checks.

~~~python
from math import gcd, isqrt, prod
from functools import cache
from sympy import resultant, symbols

def menu(target):
    found = set()
    for a in range(36,343,49):
        A = a + 343*(-a % 6)
        g,h = (pow(t,A,2401) for t in (3,5))
        dh = {pow(h,j,2401):j for j in range(343)}
        for u0,I,J in [(17,(33,12,47),(39,11,46)),
                       (24,(40,5,26),(46,4,25)),
                       (38,(5,40,33),(11,39,32))]:
            for u in range(u0,343,49):
                delta = pow(g,u,2401)-pow(g,u+1,2401)
                for v in range((1-u)%7,343,7):
                    w = dh[(pow(h,v,2401)+delta)%2401]
                    if v%49 in I or w%49 in J:
                        continue
                    for k in range(1,343):
                        if k%7 == 0:
                            continue
                        P,Q = (0,k*v-u),(1,k*w-u)
                        b,c,d = min(((S[1-i]-S[i])*t%343,
                                     (T[1-j]-S[i])*t%343,d)
                            for S,T in ((P,Q),(Q,P))
                            for i in (0,1) for j in (0,1)
                            if (d:=(T[j]-S[i])%343)%7
                            for t in [pow(d,-1,343)])
                        if (b,c) == target:
                            found.add((pow(a*d,-1,343),k))
    return found

def root(a,b,x,n):
    assert pow(x,343,n) == 1 and gcd(pow(x,49,n)-1,n) == 1
    for j in range(1,343):
        if j%7:
            y = pow(x,j,n)
            assert gcd(1-y+pow(y,a,n)-pow(y,b,n),n) == (n if j==1 else 1)

R = 416145061896121189837051312545224068417504148610151
x = 377852984884652044595819504263976339275014335045675
t = symbols('t')
assert resultant(sum(t**i for i in range(0,343,49)),1-t+t**61-t**247,t) == 7*R
root(61,247,x,R)
assert menu((61,247)) == {(15+49*j,262) for j in range(7)}

B = 2**19
s = bytearray(b'\1')*(B+1)
s[:2] = b'\0\0'
for k in range(2,isqrt(B)+1):
    if s[k]:
        s[k*k::k] = b'\0'*((B-k*k)//k+1)

def power(k):
    z = k
    while z*k <= B:
        z *= k
    return z

L = prod(power(k) for k in range(2,B+1) if s[k] and k!=7)
H = 7**R.bit_length()
def W(a,b):
    return pow(3,a,R)*pow(5,b,R)%R

def chain(u,lo,hi):
    z = pow(u,lo,R)
    for _ in range(lo,hi+1):
        yield z
        z = z*u%R

def relation(M,h):
    A,C = (pow(W(a,b),L*H,R) for a,b in M)
    X = list(chain(A,-h,h))
    for j,y in enumerate(chain(C,0,h)):
        start = h+1 if j==0 else 0
        f = 1
        for z in X[start:]:
            f = f*(z-y)%R
        if gcd(f,R)>1:
            for i in range(start,len(X)):
                d = gcd(X[i]-y,R)
                if d>1:
                    return i-h,j,d

old,new = ((5,17),(-19,4)),((-2,3),(-15,-2))
for m,((a,b),(c,d)) in ((343,old),(49,new)):
    assert a*d-b*c == m and (a+262*b)%m == (c+262*d)%m == 0
assert relation(old,2401) is None and relation(new,1342) is None
i,j,p = relation(new,2401)
assert (i,j,p) == (1343,777,10267249262761)
u,v = -2*i+15*j,3*i+2*j
assert (u,v) == (8969,5583) and (u+262*v)%343 == 245
z = pow(W(u,v),L,R)
assert gcd(pow(z,H,R)-1,R) == p and gcd(pow(z,7,R)-1,R) == 1
q = R//p
assert p*q == R and (p%1372,q%1372) == (1,687)

r = 105252402993769124507
cert = {
    p:[11878441], 11878441:[179,79],
    q:[1040298144051883957,3786321097494083],
    1040298144051883957:[6765173,557899], 557899:[107,79],
    6765173:[1691293], 1691293:[1453], 3786321097494083:[2481206485907],
    2481206485907:[236573,40031], 236573:[71,17],
    r:[21927848918543], 21927848918543:[61979143],
    61979143:[10329857], 10329857:[40351],
}
@cache
def prime(n):
    if n<100000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    F = cert[n]
    assert (n-1)%prod(F)==0 and prod(F)**2>n
    assert pow(2,n-1,n)==1
    for d in F:
        prime(d)
        assert gcd(pow(2,(n-1)//d,n)-1,n)==1

def project(n,x):
    s = n-1
    while s%7==0:
        s//=7
    D = {pow(x,s*j,n):j for j in range(343)}
    return tuple(D.get(pow(b,s,n)) for b in (3,5))

for n in (p,q,r):
    prime(n)
assert (p-1)%2401==0 and (p-1)%16807!=0
assert project(p,x)==(None,None)
assert project(q,x)==(257,104)
assert 257%49!=15 and (104-262*257)%343==341

y = 35983878305134030475
root(70,180,y,r)
M = menu((70,180))
assert M == {(e+49*j,k) for e,k in ((15,58),(43,324)) for j in range(7)}
F,G = project(r,y)
assert (F,G)==(141,163)
for m,count in ((49,7),(343,0)):
    assert sum((F-E)%m==(G-E*K)%m==0 for E,K in M)==count
s = (r-1)//343
w = pow(3,19*s,r)*pow(5,s,r)%r
assert w!=1 and pow(w,7,r)==1
~~~
