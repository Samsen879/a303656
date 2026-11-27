# A joint menu-lattice relation splits and closes native (131,173)

Here the [previous residual-exponent method](https://github.com/Samsen879/a303656/commit/cf319be53637cf4bce69997aa4e5ec763120886d) missed a genuinely composite residual Q. Keep the same prime-to-7 smooth bound 2^19. For the fixed k=82 menu, use independent kernel words W₁=3^15·5^4 and W₂=3^(−7)·5^21, determinant 343. If a support passed, any product of these words would have trivial 7-primary phase.

Define A=W₁^(LH), C=W₂^(LH), with H=7^(bitlength Q). Search the fixed 2401 relation window by gcd of Q against column products of A^i−C^j, then verify actual hit terms. The first reported strict failing relation (i,j)=(1201,244) gives Z=3^19723·5^(−320). Its short relation modulus is not a post hoc guessed factor: the discovery gcd from Q is 24084983917, while gcd(Q,Z^L−1)=1. Thus this entire strict block rejects before a primality assumption. The explored ECM check was independent of this actual search; no ECM or order factor is required by the replay.

The split parts of the exact non-7 norm are 242299349945339, 24084983917 and 29871280592520743383344793; exact recursive Lucas certificates prove all prime. The first and last have both individual 7-primary orders 2401, not the required 343. The middle part returns actual projected exponents (45,126), whose mod-49 reduction (45,28) disagrees with the requirement (47,32). All three individually fail the ratio-82 word test too. The two newly separated parts also have the wrong sign residue 1 mod 1372, whereas the old part has the right sign 687. This closes one source and is not a cohort claim.

The same two original masked directions each have exact order 1950517 on the smaller new prime and 2689027366521929 on the larger. The residual Q has respective orders 650172 and 1344513683260964 modulo these order primes. Therefore adding Q−1 or any product/lcm of Φ_m(Q) with all m<650172 cannot cancel either long masked order. Indeed each Φ_m(Q) divides Q^m−1. The tested coefficient boxes also give no nontrivial relation up to 1024 on both; the 2401 search succeeds on the smaller, not the larger. This is a fixed source-specific limitation, not a theorem for arbitrary maps of Q.

~~~python
from math import gcd, isqrt, prod
from functools import cache

Q = 719449312651056334876743505070694181
D = 242299349945339
R = 174322100773971907875197891074653227374413135372359
x = 147615206520187653669163177547231933830209706601484
assert R == D*Q and gcd(D,Q)==1
assert pow(x,343,R)==1 and gcd(pow(x,49,R)-1,R)==1
assert (1-x+pow(x,131,R)-pow(x,173,R))%R==0

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

assert 15*21-4*(-7)==343
assert (15+82*4)%343==(-7+82*21)%343==0
w1,w2=W(15,4,Q),W(-7,21,Q)
A,C=pow(w1,L*H,Q),pow(w2,L*H,Q)

def first():
    row=[(i,pow(A,i,Q)) for i in range(-2401,2402) if i%7]
    b=1
    for j in range(1,2402):
        b=b*C%Q
        t=1
        for _,a in row:
            t=t*(a-b)%Q
        if gcd(t,Q)>1:
            for i,a in row:
                p=gcd(a-b,Q)
                if 1<p<Q:
                    z=pow(pow(w1,i,Q)*pow(w2,-j,Q)%Q,L,Q)
                    if gcd(z-1,p)==1:
                        return i,j,p,z
    raise AssertionError("no separating relation")

i,j,p,z=first()
q=Q//p
assert (i,j,p,q)==(1201,244,24084983917,29871280592520743383344793)
assert p*q==Q and gcd(p,q)==1
assert z==558198888919747964086847403389957221
assert gcd(z-1,Q)==1 and gcd(pow(z,H,Q)-1,Q)==p
v=pow(W(15,4,R),L,R)
assert gcd(v-1,R)==1 and gcd(pow(v,7**R.bit_length(),R)-1,R)==D

e,f=1950517,2689027366521929
cert={
    D:(2,[2,7,7,7,7,188633,267493]),
    188633:(3,[2,2,2,17,19,73]),267493:(2,[2,2,3,22291]),
    22291:(3,[2,3,5,743]),
    p:(2,[2,2,3,3,7,7,7,e]),e:(6,[2,2,3,3,54181]),
    54181:(2,[2,2,3,3,5,7,43]),
    q:(5,[2,2,2,3,3,7,7,7,7,13,4943,f]),
    f:(3,[2,2,2,271,229403,5406757]),229403:(2,[2,23,4987]),
    5406757:(2,[2,2,3,450563]),450563:(2,[2,7,32183]),
    32183:(5,[2,16091]),16091:(6,[2,5,1609]),
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

def free7(n):
    while n%7==0:
        n//=7
    return n

for n,obs,ratio in ((D,(4,127),169775742190621),
                    (p,(118,56),12994793023),
                    (q,(135,261),26808142509191643952257107)):
    prime(n)
    m=free7(n-1)
    assert all(pow(u,(n-1)//343,n)==pow(x,a,n)
               for u,a in zip((3,5),obs))
    assert pow(W(-82,1,n),m,n)==ratio!=1
    w=pow(W(15,4,n),m,n)
    assert gcd(w-1,n)==1 and pow(w,7**n.bit_length(),n)==1
    if n!=p:
        assert (n-1)//m==2401
        assert all(pow(u,343*m,n)!=1 for u in (3,5))

assert (D%1372,p%1372,q%1372)==(687,1,1)
m=free7(p-1)
assert all(pow(u,m,p)==pow(x,m*a,p) for u,a in ((3,45),(5,126)))
assert 45%49!=47 and 126%49!=82*47%49

for n,l,d,F,r in ((p,e,650172,[2,3,54181],1024),
                   (q,f,1344513683260964,[2,271,229403,5406757],2401)):
    assert A%n!=1 and C%n!=1 and pow(A,l,n)==pow(C,l,n)==1
    assert pow(Q,d,l)==1 and all(pow(Q,d//v,l)!=1 for v in F)
    S,T=({pow(u,j,n) for j in range(-r,r+1)} for u in (A,C))
    assert len(S)==len(T)==2*r+1 and S&T=={1}

from sympy import symbols,resultant
X=symbols("X")
assert resultant(sum(X**i for i in range(0,295,49)),
                 1-X+X**131-X**173,X)==7*R
print("strict split",p,q,"all three blocks reject")
~~~
