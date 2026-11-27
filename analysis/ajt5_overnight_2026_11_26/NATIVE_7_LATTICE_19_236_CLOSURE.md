# A 7-lattice strict rejection and the exact native (19,236) closure

Use the same fixed prime-to-7 L and H=7^(bitlength R). For Z=(3^u5^v)^L, a captured prime p is in the saturated support of gcd(R,Z^H−1). On that support Z is 7-primary. If a native label (E,k) passes, cancellation of s=(p−1)_(7′) gives Z=x^(LE(u+kv)). Thus in the 7 lattice u+kv≡0 mod7, Z^49 must equal 1 for a passing label, including at primes with deeper than order 343 available. For v₇(u+kv)=1, full Z can distinguish E mod49; its seventh power only E mod7; its 49th power retains no E information. No 7-lattice word can distinguish the seven lifts E=e+49j using this native relation alone.

With several labels, for each label union all supported failure blocks, then intersect the resulting failure supports across all labels. A short word from another k may still be tested against x^(49LE(u+kv)), but this expected value cannot in general be replaced by 1. Saturation keeps complete prime-power factors; set union/intersection correspond to lcm/gcd. A whole-modulus discrepancy without the support intersection does not imply that every prime fails.

At actual (19,236), the exact source menu is E≡12 mod49,k=75 and the raw norm is 7R. Old 343/49 tests only captured 654625886041, which fails its sign gate. On the residual the first 7-lattice strict relation at halfwidth 1721 has coordinates (−1721,1372) in ((2,1),(−1,3)), giving word (−2070,−5837). It captures and rejects 81798114438038027 without factor or local-order input. That prime passes the sign gate but both original axes have 7-primary order 2401. Remaining prime 3456047809568765549111 has actual phases (289,147) and independently fails the required first-axis phase and ratio. Exact primality certificates and the native norm close this one source.

In the certified (31,105) control p=10172243299, every captured 7-lattice word passes the coarse 49th-power test because the original ratio mismatch vanishes mod7. The exact replay checks one real short word whose full Z requires E≡18 mod49 and whose seventh power is still blind, and a different one requiring E≡29 mod49 that the seventh-power comparison already rejects. The native root, hierarchy, and full-axis phase tests must not be conflated.

~~~python
from math import gcd, isqrt, prod
from sympy import symbols, resultant

def menu(target):
    out = set()
    for a in range(36,343,49):
        g,h = (pow(b,a+343*(-a%6),2401) for b in (3,5))
        inv = {pow(h,j,2401):j for j in range(343)}
        for u0,I,J in ((17,(33,12,47),(39,11,46)),
                       (24,(40,5,26),(46,4,25)),(38,(5,40,33),(11,39,32))):
            for u in range(u0,343,49):
                for v in range((1-u)%7,343,7):
                    w = inv[(pow(h,v,2401)+pow(g,u,2401)-pow(g,u+1,2401))%2401]
                    if v%49 in I or w%49 in J:
                        continue
                    for k in range(1,343):
                        if not k%7:
                            continue
                        P,Q = (0,k*v-u),(1,k*w-u)
                        b,c,d = min(((S[1-i]-S[i])*t%343,(T[1-j]-S[i])*t%343,d)
                            for S,T in ((P,Q),(Q,P)) for i in (0,1) for j in (0,1)
                            if (d:=(T[j]-S[i])%343)%7 for t in [pow(d,-1,343)])
                        if (b,c)==target:
                            out.add((pow(a*d,-1,343),k))
    return out

def native(a,b,x,n,e,k):
    assert pow(x,343,n)==1 and gcd(pow(x,49,n)-1,n)==1
    for j in range(1,343):
        if j%7:
            y=pow(x,j,n)
            assert gcd(1-y+pow(y,a,n)-pow(y,b,n),n)==(n if j==1 else 1)
    assert menu((a,b))=={(e+49*j,k) for j in range(7)}

B=2**19
s=bytearray(b'\1')*(B+1)
s[:2]=b'\0\0'
for a in range(2,isqrt(B)+1):
    if s[a]:
        s[a*a::a]=b'\0'*((B-a*a)//a+1)
def power(a):
    b=a
    while b*a<=B:
        b*=a
    return b
L=prod(power(a) for a in range(2,B+1) if s[a] and a!=7)

def W(n,u,v):
    return pow(3,u,n)*pow(5,v,n)%n

def support(n,h,M):
    A,C=(pow(W(n,u,v),L*7**n.bit_length(),n) for u,v in M)
    X=[pow(A,i,n) for i in range(-h,h+1)]
    f=prod(z-1 for z in X[h+1:])%n
    for j in range(1,h+1):
        y=pow(C,j,n)
        for z in X:
            f=f*(z-y)%n
    d=gcd(n,f)
    while (g:=gcd(n,d*d))!=d:
        d=g
    return d

R=185061555880290233438157732215664417723117422145877
x=156015315297934526501862785519800758148818078980183
t=symbols('t')
assert resultant(sum(t**i for i in range(0,343,49)),1-t+t**19-t**236,t)==7*R
native(19,236,x,R,12,75)
M7,M49,M343=((2,1),(-1,3)),((-3,2),(-2,-15)),((11,9),(-10,23))
for m,((a,b),(c,d)) in ((7,M7),(49,M49),(343,M343)):
    assert a*d-b*c==m and (a+75*b)%m==(c+75*d)%m==0
D=support(R,2401,M343)
assert D==support(R,2401,M49)==654625886041
i,j=-1721,1372
u,v=2*i+j,i-3*j
assert (u,v)==(-2070,-5837) and (u+75*v)%343==224
z=pow(W(R,u,v),L,R)
p=gcd(pow(z,7**R.bit_length(),R)-1,R)
assert p==81798114438038027 and gcd(pow(z,49,R)-1,R)==1
assert support(R//D,1720,M7)==1 and support(R//D,2401,M7)==p
q=R//(D*p)
assert R==D*p*q and (D%1372,p%1372,q%1372)==(1,687,687)

r=10172243299
cert={D:[5301473],5301473:[15061],p:[12788123,257],
      12788123:[4657],q:[13573764513167],13573764513167:[3637,3547],
      r:[4942781],4942781:[4663]}
def prime(n):
    if n<100000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    F=prod(cert[n])
    assert (n-1)%F==0 and F*F>n and pow(2,n-1,n)==1
    for d in cert[n]:
        prime(d)
        assert gcd(pow(2,(n-1)//d,n)-1,n)==1

def logs(n,x):
    s=n-1
    while s%7==0:
        s//=7
    table={pow(x,s*j,n):j for j in range(343)}
    return tuple(table.get(pow(b,s,n)) for b in (3,5))

for n in (D,p,q,r):
    prime(n)
assert (p-1)%2401==0 and (p-1)%16807!=0 and logs(p,x)==(None,None)
assert logs(q,x)==(289,147) and 289%49!=12 and (147-75*289)%343==81
N=38265442235717912587509245095261070528107830540157
y=26163736471527006267107110028486752379081206737979
native(31,105,y,N,32,271)
assert N%r==0 and r%1372==687 and logs(r,y)==(141,26)
assert (26-271*141)%7==0
for i,j,E,agree in ((1223,1729,18,True),(-1756,1559,29,False)):
    u,v=2*i+j,i-3*j
    ell=(u+271*v)%343
    z=pow(W(r,u,v),L,r)
    assert pow(z,49,r)==1 and ell%7==0 and ell%49!=0
    assert z==pow(y,L*E*ell,r)
    want=pow(y,L*32*ell,r)
    assert z!=want and (pow(z,7,r)==pow(want,7,r))==agree
~~~
