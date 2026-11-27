# A menu-selected word certifies a strict bad support in a second native source

For a fixed native menu proportion k, choose a short (a,b) with a+kb=0 mod 343. Any passing prime must have trivial 7-primary projection of W=3^a5^b, independently of the shared first-axis lift E. Take the prime-to-7 part L of lcm(1,…,2^19), and V=W^L modulo R. Let D₀,D₁ be the supports of gcd(R,V−1), gcd(R,V^H−1), saturated to full prime powers, with H=7^(bitlength R). At every prime in D₁/D₀, the projected V has nontrivial pure 7-power order. As L is prime to 7, W has nontrivial 7-primary projection there. The whole strict support can therefore be rejected without a prior factorization or primality test for D₁/D₀. A prime outside D₁ is not classified by the procedure.

For the native (80,17) source the independently reconstructed norm is 7R and the fixed menu is exactly E≡9 mod 49, k=236. The chosen direction (−3,16) yields D₀=1 and D₁=2216676309079. The same mask applied to 3 or 5 alone also finds that block, so the demonstrated improvement is a post-capture rejection rule, not faster factor discovery.

Both factors of R have been explicitly Lucas-certified and satisfy the same sign gate p≡687 mod 1372. At p=2216676309079 the actual pair is (78,43), with ratio discrepancy 157 mod 343; at q=431522833164362684190508359856042090391 it is (237,111), with discrepancy 88. Both factors independently reject, so this one source is fully closed. At q the W order contains the certified factor 3262828345754848069122262531, which exceeds the fixed mask envelope. Separately the exact absolute norm, finite difference, and tame field calculation verify the order-343 aggregate (315,154): derivative 109074 modulo 7⁶, tame (227,248), wild (88,249). The aggregate discrepancy is 245 and vanishes modulo 49. It does not locate either prime by itself.

The negative control is the previous closed (55,161) chart source. The positive control for the *ratio test* is prime 14990909229855917 of (120,220): the calibrated phase pair satisfies (117,151) with k=271, and the fixed mask fails to capture it but the calibrated mask gives D₀=D₁ at that prime. Its first-axis phase fails a different menu condition, so it is not a passing support for the full chart.

## Exact replay (Python 3.10+, SymPy for resultant)

~~~python
from math import gcd, isqrt, prod
from functools import cache
from sympy import symbols, resultant

R = 956546441102092568948733376010385312705193571959889
x = 817148019016772661492745320699017692394501233719785
R0 = 41972042533351331790887366901335366135158470044034151
x0 = 30015482896187807087217920276249313249092836022188472
Rm = 123373616887935250961105308119927409087
xm = 58553089124130792433606427932964087903
p, q = 2216676309079, 431522833164362684190508359856042090391
p0, pm = 878168614051, 14990909229855917

X = symbols("X")
F = sum(X**j for j in range(0,295,49))
assert resultant(F,1-X+X**80-X**17,X)==7*R

@cache
def normal(a,b):
    U,V=(0,a),(1,b)
    return min(((p[1-i]-p[i])*s%343,(q[1-j]-p[i])*s%343,d)
        for p,q in ((U,V),(V,U)) for i in (0,1) for j in (0,1)
        if (d:=(q[j]-p[i])%343)%7 for s in (pow(d,-1,343),))

menus = {(80,17):set(), (55,161):set(), (120,220):set()}
for a in range(36,343,49):
    z=a+343*((-a)%6)
    g,h=pow(3,z,2401),pow(5,z,2401)
    lookup={pow(h,v,2401):v for v in range(343)}
    for j,left,right in ((17,{33,12,47},{39,11,46}),
                         (24,{40,5,26},{46,4,25}),
                         (38,{5,40,33},{11,39,32})):
        for u in range(j,343,49):
            delta=pow(g,u,2401)-pow(g,u+1,2401)
            for v in range((1-u)%7,343,7):
                if v%49 in left: continue
                w=lookup[(pow(h,v,2401)+delta)%2401]
                if w%49 in right: continue
                for k in range(1,343):
                    if k%7:
                        i,j0,d=normal((k*v-u)%343,(k*w-u)%343)
                        if (i,j0) in menus:
                            menus[i,j0].add((pow(a*d,-1,343),k))
for r,y,a,b,e,k in ((R,x,80,17,9,236),(R0,x0,55,161,27,118),
                     (Rm,xm,120,220,15,271)):
    assert menus[a,b]=={(z,k) for z in range(e,343,49)}
    assert pow(y,343,r)==1 and gcd(pow(y,49,r)-1,r)==1
    assert (1-y+pow(y,a,r)-pow(y,b,r))%r==0

B=2**19
sieve=bytearray(b'\1')*(B+1)
sieve[:2]=b'\0\0'
for l in range(2,isqrt(B)+1):
    if sieve[l]:
        sieve[l*l::l]=b'\0'*((B-l*l)//l+1)
parts=[]
for l in range(2,B+1):
    if sieve[l] and l!=7:
        d=l
        while d*l<=B: d*=l
        parts.append(d)
L=prod(parts)
assert L%343==104

def sat(r,d):
    while (e:=gcd(r,d*d))!=d: d=e
    return d

def read(r,k,L):
    _,_,a,b=min((abs(a)+b,max(abs(a),b),a,b)
        for b in range(1,172) if b%7
        for a in [(-k*b+171)%343-171])
    v=pow(pow(3,a,r)*pow(5,b,r)%r,L,r)
    d0=sat(r,gcd(r,v-1))
    d1=sat(r,gcd(r,pow(v,7**r.bit_length(),r)-1))
    return (a,b),v,d0,d1,d1//d0

assert read(R,236,L)==(
    (-3,16),42366579159232551451336491305070999212894115069154,1,p,p)
assert all(gcd(R,pow(pow(u,L,R),7**R.bit_length(),R)-1)==p
           for u in (3,5))
assert read(R0,118,L)[2:]==(1,p0,p0)
assert read(Rm,271,L)[2:]==(1,1,1)
assert read(Rm,271,(pm-1)//343)[2:]==(pm,pm,1)
assert p*q==R

ell=3262828345754848069122262531
C={
 p:(3,[2,3,7,7,7,11,11,19,468509]),
 468509:(2,[2,2,117127]),117127:(6,[2,3,3,3,3,3,241]),
 q:(7,[2,5,7,7,7,53,79,9209,ell]),
 ell:(2,[2,3,3,3,5,23,31,67,911,7557997,36740159527]),
 7557997:(2,[2,2,3,17,37049]),37049:(6,[2,2,2,11,421]),
 36740159527:(5,[2,3,7,7,124966529]),
 124966529:(3,[2,2,2,2,2,2,2,976301]),976301:(3,[2,2,5,5,13,751]),
 pm:(2,[2,2,7,7,7,10926318680653]),
 10926318680653:(2,[2,2,3,7687,118450183]),
 118450183:(3,[2,3,19741697]),
 19741697:(3,[2,2,2,2,2,2,2,2,2,2,13,1483]),
 p0:(3,[2,3,3,5,5,7,7,7,13,437651]),437651:(2,[2,5,5,8753])
}
@cache
def prime(n):
    if n<10000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    a,F=C[n]
    assert prod(F)==n-1 and pow(a,n-1,n)==1
    for d in set(F):
        prime(d)
        assert gcd(pow(a,(n-1)//d,n)-1,n)==1

def check(p,r,x,V):
    prime(p)
    y=x%p
    assert r%p==0 and p%343==1
    assert all(pow(u,(p-1)//343,p)==pow(y,j,p)
               for u,j in zip((3,5),V))

check(p,R,x,(78,43))
check(q,R,x,(237,111))
check(p0,R0,x0,(45,4))
check(pm,Rm,xm,(117*153%343,151*153%343))
assert (p%1372,q%1372)==(687,687)
assert (43-236*78)%343==157 and (111-236*237)%343==88
assert ((78+237)%343,(43+111)%343)==(315,154)
assert (151-271*117)%343==0 and 117%49!=15
W=pow(3,-3,q)*pow(5,16,q)%q
assert (q-1)%ell==0
assert pow(W,(q-1)//ell,q)==150766622782009359467385558045892576602
print("strict rejection", p, "independent complement rejection", q)
~~~
