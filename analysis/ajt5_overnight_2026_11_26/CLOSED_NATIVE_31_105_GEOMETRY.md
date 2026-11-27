# Native (31,105) is closed; exact geometry explains the original miss

The source with menu E≡32 mod49, k=271 has exact raw norm 7R. The previously found prime 10172243299 and the two residual factors 54953659416013 and 68453140889559413961981211 all have exact recursive Lucas verification here. The latter split was discovered by ECM, not predicted by the geometric search. All three separately violate the ratio-271 test. Their separate first-axis or sign/order failures are checked too: the first passes the sign, the middle fails it and has phases (218,8), and the last passes it but both original axes have 7-primary order 2401 beyond 343. Thus this particular native chart source is completely closed.

The residual is useful as a strict geometric negative control. Keep the same B=2^19 and the unshifted old basis w₁=(17,5), w₂=(−4,19). For the fully projected unit pair A,C, use the convention A^i C^j=1. On the middle factor, A has prime order 13351229207 and C=A^8056171448; the two certified integral relation vectors (81497,7993),(−48215,159096) have determinant that order. Inverse coordinates show every relation within halfwidth 81496 would be a multiple of the first vector, which is already outside. On the largest factor the projection to order 578693 forces i+21224j=0 mod578693; the entire exact list in the same box is numerically excluded in the full group. Thus this box misses both residual factors.

For a transformed box write M for its change of basis in the old relation coordinates, d for its center and h₁,h₂ for the two halfwidths. If |d_i|+|M_i1|h₁+|M_i2|h₂≤81496 on each row, no nonzero relation is possible. This includes all centered halfwidth-2401 transforms with row absolute sum at most 33 and all such centered bases whose actual four native coordinates have absolute value at most 253. For two translated windows the bound applies to the difference, and a common translation cancels.

An exact upper-triangular shear first reaches a residual part at absolute shear 2194, yielding (u,j)=(1939,764) and old (i,j)=(1678155,764). The new native basis vector (37294,10989) is long. It recovers the middle factor under direct gcd and the unprojected phase has exact order 343 there, but the constructive choice used the known factor orders; it is a retrospective threshold, not a factor-free discovery method or convergence guarantee.

~~~python
from math import gcd, isqrt, prod
from functools import cache

R=38265442235717912587509245095261070528107830540157
Q=3761750590401201195994834914266738531743
x=26163736471527006267107110028486752379081206737979
p0,p,q=10172243299,54953659416013,68453140889559413961981211
e,r,t=13351229207,578693,1642221509572199
assert R==p0*Q and Q==p*q
assert pow(x,343,R)==1 and gcd(pow(x,49,R)-1,R)==1
assert (1-x+pow(x,31,R)-pow(x,105,R))%R==0

cert={
 p0:(2,[2,3,7,7,7,4942781]),4942781:(2,[2,2,5,53,4663]),
 p:(5,[2,2,3,7,7,7,e]),e:(7,[2,7,19,29,1730779]),
 1730779:(2,[2,3,7,7,7,29,29]),
 q:(3,[2,3,5,7,7,7,7,r,t]),r:(2,[2,2,199,727]),
 t:(23,[2,2129,752593,512467]),752593:(5,[2,2,2,2,3,15679]),
 15679:(11,[2,3,3,13,67]),512467:(2,[2,3,85411]),
 85411:(2,[2,3,3,5,13,73]),
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

for n in (p0,p,q):
    prime(n)

B=2**19
s=bytearray(b'\1')*(B+1)
s[:2]=b'\0\0'
for i in range(2,isqrt(B)+1):
    if s[i]:
        s[i*i::i]=b'\0'*((B-i*i)//i+1)
parts=[]
for i in range(2,B+1):
    if s[i] and i!=7:
        z=i
        while z*i<=B:
            z*=i
        parts.append(z)
L=prod(parts)
H=7**Q.bit_length()

def W(a,b,n):
    return pow(3,a,n)*pow(5,b,n)%n

U,V=(pow(W(a,b,Q),L,Q) for a,b in ((17,5),(-4,19)))
A,C=(pow(z,H,Q) for z in (U,V))
assert (A,C)==(1056000989733190777360396580075734960736,
               3579382741425606374246421410695893847263)
assert {(a,b) for a in range(-19,20) for b in range(-19,20)
        if (a+271*b)%343==0}=={(0,0),(17,5),(-17,-5),(-4,19),(4,-19)}

c=8056171448
assert A%p!=1 and pow(A,e,p)==1 and pow(A,c,p)==C%p
u,v=(81497,7993),(-48215,159096)
assert u[0]*v[1]-u[1]*v[0]==e
assert all((a+c*b)%e==0 for a,b in (u,v))
assert (81496*sum(map(abs,v))//e,81496*sum(map(abs,u))//e)==(1,0)

f=21224
assert pow(C,t,q)==pow(A,t*f,q)
assert all(pow(z,r*t,q)==1 and pow(z,r,q)!=1 and pow(z,t,q)!=1
           for z in (A,C))

def no_box(X,Y):
    step=pow(A,r,q)
    c=1
    count=0
    for j in range(Y+1):
        i=(-f*j+X)%r-X
        z=pow(A,i,q)*c%q
        while i<=X:
            if i or j:
                assert z!=1
                count+=1
            i+=r
            z=z*step%q
        c=c*C%q
    return count

assert no_box(81496,81496)==22952
assert 33*2401<=81496<34*2401 and (46*253)//343==33

h=2401
trials=[]
for j in range(1,h+1):
    i=(-c*j+e//2)%e-e//2
    lo,hi=(i-h+j-1)//j,(i+h)//j
    if lo<=hi:
        m=0 if lo<=0<=hi else min((lo,hi),key=abs)
        trials.append((abs(m),m,i,j,i-m*j))
assert min(trials)==(2194,2194,1678155,764,1939)
assert 2195*h<e//2 and no_box(2195*h,h)==43752
z=pow(U,1678155,Q)*pow(V,764,Q)%Q
assert gcd(z-1,Q)==1 and gcd(pow(z,H,Q)-1,Q)==p
assert pow(z,49,p)!=1 and pow(z,343,p)==1

for n,pair,ratio in ((p0,(141,26),7231062019),
                     (p,(218,8),25652286594888),
                     (q,None,61405735424183074217728738)):
    m=n-1
    while m%7==0:
        m//=7
    assert pow(W(-271,1,n),m,n)==ratio!=1
    if pair:
        assert (n-1)//m==343
        assert all(pow(u,m,n)==pow(x,m*j,n) for u,j in zip((3,5),pair))
        assert pair[0]%49!=32 and pair[1]%49!=271*32%49
    else:
        assert (n-1)//m==2401
        assert all(pow(u,343*m,n)!=1 for u in (3,5))
assert (p0%1372,p%1372,q%1372)==(687,1,687)

from sympy import symbols,resultant
X=symbols("X")
assert resultant(sum(X**i for i in range(0,295,49)),1-X+X**31-X**105,X)==7*R
~~~
