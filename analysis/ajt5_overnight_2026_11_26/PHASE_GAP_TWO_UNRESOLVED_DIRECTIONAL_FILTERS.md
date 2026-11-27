# Exact directional filters for two unresolved phase candidates

Neither \((141,205)\) nor \((427,259)\) is certified or vetoed by this note. The certified phase gap stays \((278/9,290/9)\).

For \((141,205)\) let \(C=(5^{141}+3^{205})/(8\cdot84454939)\). The removed factor \(84454939=5476^2+3\cdot4261^2\) is coprime to \(C\), and \(C\) is a 90-digit composite. The polynomial pair \(T^5-5\) and \(5^{28}T+3^{41}\) has the explicit common root \(f=-3^{41}/5^{28}\pmod C\). In particular \(\gcd(f,C)=\gcd(f^2+3,C)=1\).

Let \(M=\operatorname{lcm}(1,\ldots,50000)\), and let \(\ell\) run over primes at most \(10^6\). Exact products have
\[
\gcd\!\left(C,\prod_{\ell}(f^{M\ell}-1)\right)=1,\qquad
\gcd\!\left(C,\prod_{\ell}\left(\Re U^{M\ell}-1\right)\right)=1,
\quad U=\frac{f+\sqrt{-3}}{f-\sqrt{-3}}.
\]
Here \(\Re\) means the scalar coefficient in \((\mathbb Z/C)[\sqrt{-3}]\). The first product rules out \(p-1\mid M\ell\) for any \(p\mid C\); the second rules out \(p+1\mid M\ell\) for any inert \(p\mid C\), since \(U\) has norm one in the nonsplit quadratic extension. This covers only the stated smoothness form and does not find the factorization.

For \((427,259)\) put \(A=5^{61}, B=3^{37}\). The separate homogeneous factors \((A^7-B^7)/(A-B)\) and \((A^7+B^7)/(A+B)\) have no factor 7; any prime dividing them is \(1\bmod14\), by the order of \(A/B\). The first has unitary norm factor \(43=4^2+3\cdot3^2\), the second unitary norm factor \(421=11^2+3\cdot10^2\). The remaining cofactors are composite and have 255 and 254 digits, respectively. This is the exact partial decomposition, not a claim about the exhaustiveness of a trial factor search.

~~~python
from math import gcd

k=84454939
C,r=divmod(5**141+3**205,8*k)
assert not r and k==5476**2+3*4261**2 and gcd(k,C)==1
assert len(str(C))==90 and pow(2,C-1,C)!=1
f=-3**41*pow(5**28,-1,C)%C
assert pow(f,5,C)==5 and gcd(f*(f*f+3),C)==1
den=pow(f*f+3,-1,C)
def mul(a,b):
    return ((a[0]*b[0]-3*a[1]*b[1])%C,(a[0]*b[1]+a[1]*b[0])%C)
def power(a,e):
    b=(1,0)
    while e:
        if e&1: b=mul(b,a)
        a=mul(a,a)
        e>>=1
    return b
u=((f*f-3)*den%C,2*f*den%C)
B=10**6
s=bytearray(B+1)
pr=[]
for p in range(2,B+1):
    if not s[p]:
        pr.append(p)
        if p*p<=B: s[p*p::p]=b'\1'*((B-p*p)//p+1)
assert len(pr)==78498
for p in pr:
    if p>50000: break
    q=p
    while q*p<=50000: q*=p
    f,u=pow(f,q,C),power(u,q)
a=b=1
for ell in pr:
    a=a*(pow(f,ell,C)-1)%C
    b=b*(power(u,ell)[0]-1)%C
assert gcd(a,C)==gcd(b,C)==1
A,B=5**61,3**37
for s,p,x,y,nd in [(-1,43,4,3,255),(1,421,11,10,254)]:
    H,r=divmod(A**7+s*B**7,A+s*B)
    R,t=divmod(H,p)
    assert not r and not t and H%7 and gcd(p,R)==1 and p==x*x+3*y*y
    assert len(str(R))==nd and pow(2,R-1,R)!=1
~~~
