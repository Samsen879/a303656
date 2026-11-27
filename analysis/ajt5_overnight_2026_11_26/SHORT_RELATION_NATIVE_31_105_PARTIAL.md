# Detection-driven truncation finds a shorter strict relation

Keep the same 2^19 prime-to-7 smooth mask and signed halfwidth bound 2401. For masked words U,V use A=U^H and C=V^H with H a power of 7 sufficient to kill every 7-primary component. In a signed halfwindow h form P(X)=prod_(−h≤i≤h)(X−A^i) by a product tree. To batch P(C^j), with T_i=i(i−1)/2, use C^(i j)=C^(T_(i+j)−T_i−T_j); thus all evaluations are a convolution of packed modular coefficients followed by unit scaling. This works over a composite residue ring. Descend only on nontrivial column gcds, checking actual leaves; at each leaf a nontrivial strict failed support is the saturated collision support minus the support on which the original word U^i V^(−j) already equals one. A whole-column hit is not itself a failure. Adding j=0 and symmetry reduces the signed window to finitely many columns. The predicate that a strict rejecting leaf exists is monotone in h, so the binary truncation tests that predicate, not first-column order.

On the previous (131,173) composite page, using the exchanged basis (W₂,W₁^−1), the old column order stops at (−1709,418). The closed-window detector certifies no collision at halfwidth 1200 and obtains the same strict factor 24084983917 at minimal halfwidth 1201 from (−244,1201). On the original orientation, the old scan already found 1201; this is an exact order-dependence control, not a universal speedup.

The actual additional (31,105) source has raw norm 7N (checked by exact resultant) and menu E≡32 mod49,k=271 (regenerated frozen chart with 605,052 observations). There is no collision at halfwidth 1576; (742,1577) at 1577 extracts the Lucas-certified p=10172243299. Because 742 is divisible by 7, the old filter instead stopped at (−2389,1584). The detected word has exact order 49 on p. This prime has the required sign residue 687 mod1372 and its individual 7-primary orders are 343, but the native phase (141,26) fails both the ratio and the mod-49 gates. Its composite complement 3761750590401201195994834914266738531743 remains uncaptured at 2401, so this source is not fully closed.

The unrelated native (120,220) prime gives a true matching ratio (117,151) for k=271, although another menu gate fails. It gives no collision at 2401. The exact replay distinguishes support capture, ratio, and the full menu.

~~~python
from math import gcd, isqrt, prod
from functools import cache

B = 2**19
s = bytearray(b'\1')*(B+1)
s[:2] = b'\0\0'
for p in range(2,isqrt(B)+1):
    if s[p]:
        s[p*p::p] = b'\0'*((B-p*p)//p+1)
parts = []
for p in range(2,B+1):
    if s[p] and p != 7:
        z = p
        while z*p <= B:
            z *= p
        parts.append(z)
L = prod(parts)

def sat(n,d):
    while (e := gcd(n,d*d)) != d:
        d = e
    return d

def mul(a,b,n):
    d = len(a)+len(b)-1
    k = (2*n.bit_length()+d.bit_length()+7)//8
    def pack(f):
        return int.from_bytes(b''.join(t.to_bytes(k,'little') for t in f),'little')
    z = (pack(a)*pack(b)).to_bytes(k*d,'little')
    return [int.from_bytes(z[i:i+k],'little')%n for i in range(0,len(z),k)]

def tri(c,d,n):
    a = b = 1
    out = []
    for _ in range(d+1):
        out.append(a)
        a,b = a*b%n,b*c%n
    return out

def setup(n,k,W):
    (a,b),(c,d) = W
    assert a*d-b*c == 343 and (a+k*b)%343 == (c+k*d)%343 == 0
    U,V = (pow(pow(3,a,n)*pow(5,b,n)%n,L,n) for a,b in W)
    H = 7**n.bit_length()
    return U,V,pow(U,H,n),pow(V,H,n)

def probe(n,data,h,old=False):
    U,V,A,C = data
    def build(l,r):
        if l==r:
            return (l,[-pow(A,l,n)%n,1],())
        m=(l+r)//2
        S,T=build(l,m),build(m+1,r)
        return (l,mul(S[1],T[1],n),(S,T))
    def reject(i,j,g):
        d=sat(n,g)
        W=pow(U,i,n)*pow(V,-j,n)%n
        J=d//sat(d,gcd(d,W-1))
        return (i,j,J) if 1<J<n else None
    def find(T,g,y,j):
        i,P,kids=T
        if not kids:
            return reject(i,j,g) if not old or i%7 else None
        for child in kids:
            z=0
            for c in reversed(child[1]):
                z=(y*z+c)%n
            f=gcd(g,z)
            if f>1 and (ans:=find(child,f,y,j)):
                return ans

    seen=1
    if not old:
        for i in range(1,h+1):
            g=gcd(pow(A,i,n)-1,n)
            seen=gcd(seen*g,n)
            if g>1 and (ans:=reject(i,0,g)):
                return ans,seen
    T=build(-h,h)
    P=T[1]
    d=len(P)-1
    f=tri(pow(C,-1,n),d,n)
    F=mul([(a*b)%n for a,b in zip(P,f)][::-1],tri(C,d+h,n),n)
    y=1
    for j in range(1,h+1):
        y=y*C%n
        g=gcd(F[d+j],n)
        seen=gcd(seen*g,n)
        if g>1 and (ans:=find(T,g,y,j)):
            return ans,seen
    return None,seen

def minimum(n,data):
    lo,hi=0,1
    while not probe(n,data,hi)[0]:
        if hi==2401:
            return None
        lo,hi=hi,min(2*hi,2401)
    while hi-lo>1:
        m=(lo+hi)//2
        if probe(n,data,m)[0]:
            hi=m
        else:
            lo=m
    return hi,probe(n,data,hi)[0]

Q0=719449312651056334876743505070694181
U,V,A,C=setup(Q0,82,((15,4),(-7,21)))
S=(V,pow(U,-1,Q0),C,pow(A,-1,Q0))
assert probe(Q0,S,2401,True)[0]==(-1709,418,24084983917)
assert probe(Q0,S,1200)==(None,1)
assert minimum(Q0,S)==(1201,(-244,1201,24084983917))

N=38265442235717912587509245095261070528107830540157
x=26163736471527006267107110028486752379081206737979
assert pow(x,343,N)==1 and gcd(pow(x,49,N)-1,N)==1
assert (1-x+pow(x,31,N)-pow(x,105,N))%N==0
W=((17,5),(-4,19))
data=setup(N,271,W)
assert probe(N,data,2401,True)[0]==(-2389,1584,10172243299)
assert probe(N,data,1576)==(None,1)
h,(i,j,p)=minimum(N,data)
assert (h,i,j,p)==(1577,742,1577,10172243299)
q=N//p
assert p*q==N and q==3761750590401201195994834914266738531743
assert pow(2,q-1,q)==1912805840069870855336725805082439011550
assert probe(q,setup(q,271,W),2401)==(None,1)
z=pow(data[0],i,p)*pow(data[1],-j,p)%p
assert z==1129338793 and pow(z,7,p)!=1 and pow(z,49,p)==1

pm=14990909229855917
xm=1006038794010550
cert={
    p:(2,[2,3,7,7,7,4942781]),4942781:(2,[2,2,5,53,4663]),
    pm:(2,[2,2,7,7,7,10926318680653]),
    10926318680653:(2,[2,2,3,7687,118450183]),
    118450183:(3,[2,3,19741697]),19741697:(3,[2]*10+[13,1483]),
}
@cache
def prime(n):
    if n<10000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    a,F=cert[n]
    assert prod(F)==n-1 and pow(a,n-1,n)==1
    for d in set(F):
        prime(d)
        assert gcd(pow(a,(n-1)//d,n)-1,n)==1

for n,y,uv in ((p,x%p,(141,26)),(pm,xm,(117,151))):
    prime(n)
    s=(n-1)//343
    assert s%7 and pow(y,343,n)==1 and pow(y,49,n)!=1
    assert all(pow(u,s,n)==pow(y,s*v,n) for u,v in zip((3,5),uv))
assert p%1372==687 and (26-271*141)%343==231
assert 141%49!=32 and 26%49!=271*32%49
assert (1-xm+pow(xm,120,pm)-pow(xm,220,pm))%pm==0
assert (151-271*117)%343==0 and 117%49!=15
assert probe(pm,setup(pm,271,W),2401)==(None,1)
print('old page minimum 1201; new source minimum 1577; matching control uncaptured')
~~~
