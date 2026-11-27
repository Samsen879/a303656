# Two words exclude incompatible top lifts on one actual multiple-ratio prime

For actual neutral source (32,118), the raw norm is 7R and the complete frozen menu is E=e+49j for e,k in {(6,46),(16,52),(16,199)}. Keeping the old fixed B=2^19, two words from the 7-lattice for k=46 are w₁=(−1,2) and w₂=(27,−5). The latter is coordinate (−6,7) in the difference convention A^i−C^j, i.e. i times (−1,2) minus j times (−3,−1). Each independent masked-power capture gcd equals the same certified prime p=2529047568419 before any factor is supplied. This is not a claim of global minimum word length.

At that p both words' coarse mod-7 and mod-49 reads retain all 14 lifts of k=52 and 199. Full word one retains only (65,52),(16,199); full word two retains only (114,52),(65,199). Their intersection is empty. The actual lift (65,52) passes full word one and both projected tests but is rejected by full word two. That is a same-prime masked blind spot, not an intersection of unrelated roots. Its independently rebuilt true axes are (180,179). The scaled original directions (7,−14) and (49,−98) remain coarse here, and the seven specified 2401-window native tests capture the same established prime. The new gain is exact joint filtering, not different factor discovery.

For coarse e,k let ℓ_i=u_i+kv_i, T=x^(49L) and D_i=Z_i x^(−Leℓ_i) on a common captured prime component. A surviving lift must have D_i=T^(jℓ_i). When 7|ℓ_i, only D_i=1 can be tested. At nonzero ℓ_i modulo 7, require D_i^7=1 first, then the common top digit is equivalent to D₁^ℓ₂=D₂^ℓ₁. In this fixture both ℓ_i are 5 mod7 for both remaining k, and the residuals differ by T^5, independently rejecting both coarse types. For each exact lift union its word-failure supports, then intersect across lifts. This must use local saturated blocks, not a whole-modulus mismatch.

The complementary q=187664448287159920981812028994224167817 is independently certified prime and has wrong sign 1 mod1372. With p·q=R and the exact resultants, the entire specified native chart source closes. The replay explicitly regenerates the menu, root, captures, and arithmetic. No inference about all sources follows.

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

R = 474612316619334967618443891052367357812987645371323
x = 385608873838308627834867514380194323956738642945858
t = symbols('t')
assert resultant(sum(t**i for i in range(0,343,49)),1-t+t**32-t**118,t)==7*R
assert pow(x,343,R)==1 and gcd(pow(x,49,R)-1,R)==1
for j in range(1,343):
    if j%7:
        y=pow(x,j,R)
        assert gcd(1-y+pow(y,32,R)-pow(y,118,R),R)==(R if j==1 else 1)
T = menu((32,118))
assert T == {(e+49*j,k) for e,k in ((6,46),(16,52),(16,199)) for j in range(7)}

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
H=7**R.bit_length()
def W(n,u,v):
    return pow(3,u,n)*pow(5,v,n)%n

words=[]
for m,(a,b),(c,d),i,j in (
    (7,(-1,2),(-3,-1),1,0), (7,(-1,2),(-3,-1),-6,7),
    (49,(3,1),(-1,16),2,1), (343,(-4,15),(-21,-7),-7,1)):
    assert a*d-b*c==m and (a+46*b)%m==(c+46*d)%m==0
    assert 0<max(abs(i),abs(j))<=2401
    words.append((a*i-c*j,b*i-d*j))
assert words==[(-1,2),(27,-5),(7,-14),(49,-98)]
Z=[pow(W(R,*w),L,R) for w in words]
p=gcd(pow(Z[0],H,R)-1,R)
assert p==2529047568419 and all(gcd(pow(z,H,R)-1,R)==p for z in Z)
q=R//p
assert p*q==R and q==187664448287159920981812028994224167817

def kept(i,m):
    u,v=words[i]
    f=343//m
    return {(E,k) for E,k in T
            if pow(Z[i],f,p)==pow(x,f*(L%343)*E*(u+k*v),p)}
thin={(E,k) for E,k in T if k in (52,199)}
A={(65,52),(16,199)}
C={(114,52),(65,199)}
assert all(kept(i,m)==thin for i in (0,1) for m in (7,49))
assert kept(0,343)==A and kept(1,343)==C and not A&C
assert kept(2,343)==kept(3,343)==thin
zeta=pow(x,49*L,p)
assert zeta!=1 and pow(zeta,7,p)==1
for k,js in ((52,(1,2)),(199,(0,1))):
    obs=[((u+k*v)%7,Z[i]*pow(x,-(L%343)*16*(u+k*v),p)%p)
         for i,(u,v) in enumerate(words[:2])]
    assert obs==[(5,pow(zeta,5*j,p)) for j in js]

cert={p:[449209,283],q:[39775417050676789,27279689],
      39775417050676789:[201251,277,197],27279689:[55901]}
def prime(n):
    if n<500000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    F=prod(cert[n])
    assert (n-1)%F==0 and F*F>n and pow(2,n-1,n)==1
    for d in cert[n]:
        prime(d)
        assert gcd(pow(2,(n-1)//d,n)-1,n)==1
prime(p)
prime(q)
assert (p%1372,q%1372)==(687,1)
s=(p-1)//343
assert s%7 and L%s==0
assert pow(3,s,p)==pow(x,180*s,p) and pow(5,s,p)==pow(x,179*s,p)
assert 179*pow(180,-1,343)%343==243

lenses=[((1,2),(-3,1)),((-1,2),(-3,-1)),
        ((-3,1),(-1,-16)),((3,1),(-1,16)),
        ((-4,15),(-21,-7)),((10,13),(-21,7)),((13,12),(-8,19))]
for M in lenses:
    U,V=(pow(W(q,*w),L*H,q) for w in M)
    I,J=({pow(u,i,q) for i in range(-2401,2402)} for u in (U,V))
    assert len(I)==len(J)==4803 and I&J=={1}
~~~
