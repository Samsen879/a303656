# A real obstruction to native-root-derived mask templates

On the undisposed composite block Q=1707542200628666649958800561642353 of source (14,152), the original 343rd root x satisfies 1−x+x^14−x^152=0. Since 1−x is a unit, (1−x^138)/(1−x)=−x^(-14), which has exact order 98 at each prime of Q. Thus the root and that quotient see only 2- and 7-primary orders. At an inert sign-gate prime p≡687 mod 1372 the projected 3,5 residual index m_p is odd and prime to 7, and m_p|p−1. Hence 686 m_p|p−1, with (p−1)/(686 m_p) odd. This yields p≡1+686 m_p mod 1372m_p, a constraint on a proposed index rather than an annihilator of the original axes.

Let R be the reduced source norm and N=7R. Form the template integer
```
D = 2 · (R^294−1)_{7'} · (Q^294−1)_{7'} · (N²−1)_{7'}.
```
For each of six fixed actual short words, the exact gcd calculation with exponent D^111 equals 1. Since each residual order at each p|Q is <2^111, if every prime factor of such an order appeared in D then the order would divide D^111. Consequently **arbitrary powers** of the template primes still cannot capture any of these six words on any prime divisor of Q. This includes the factor support of every R^j−1 or Q^j−1 for j|294 after dropping 7, and N±1 after dropping 7. The result only rules out this specified template on these six words; it does not say the remainder is inert or resolve that source.

The same replay contrasts the (16,186) genuine determinant-driven positive: the two already captured independent words provide T=5477558 without factoring the source, expanding the axis support to the pre-certified composite block. Native root order information alone has not supplied an analogous multiplier for the negative fixture.

```python
from math import gcd, isqrt, prod

K=2**19
s=bytearray(b'\1')*(K+1)
s[:2]=b'\0\0'
for a in range(2,isqrt(K)+1):
    if s[a]:
        s[a*a::a]=b'\0'*((K-a*a)//a+1)
def pp(a):
    b=a
    while b*a<=K:
        b*=a
    return b
L=prod(pp(a) for a in range(2,K+1) if s[a] and a!=7)
def no7(n):
    while n%7==0:
        n//=7
    return n
def sat(n,d):
    while (g:=gcd(n,d*d))!=d:
        d=g
    return d

R=7794092988996359616004983264299816596361951171
Q=1707542200628666649958800561642353
N=7*R
x=13637500586108896670367803493377664812606052%Q
assert R%Q==0 and (R%1372,Q%1372)==(687,1)
assert pow(x,343,Q)==1 and gcd(Q,pow(x,49,Q)-1)==1
assert (1-x+pow(x,14,Q)-pow(x,152,Q))%Q==0 and pow(x,Q,Q)==x
r=(1-pow(x,138,Q))*pow(1-x,-1,Q)%Q
assert r==-pow(x,-14,Q)%Q
assert pow(r,98,Q)==1 and pow(r,49,Q)==Q-1
assert gcd(Q,pow(r,14,Q)-1)==1

D=2*prod(no7(n) for n in (R**294-1,Q**294-1,N*N-1))
assert Q.bit_length()==111
A,B=(pow(a,L*7**Q.bit_length(),Q) for a in (3,5))
P,S=(pow(a,D**111,Q) for a in (A,B))
for u,v in ((1,0),(0,1),(1,1),(1,-1),(-2,1),(-1,-3)):
    assert gcd(Q,pow(A,u,Q)*pow(B,v,Q)-1)==1
    assert gcd(Q,pow(P,u,Q)*pow(S,v,Q)-1)==1

R=21831913108948893248715238773608846587809381120739
A,B=(pow(a,L*7**R.bit_length(),R) for a in (3,5))
w,z=(-2095,-1233),(1136,-1946)
T=abs(w[0]*z[1]-w[1]*z[0])
assert T==5477558 and gcd(T,7)==1
C=sat(R,gcd(R,*(pow(A,u,R)*pow(B,v,R)-1 for u,v in (w,z))))
old=sat(R,gcd(R,A-1,B-1))
new=sat(R,gcd(R,pow(A,T,R)-1,pow(B,T,R)-1))
assert old==572493630662019608249
assert new==C==190381625479819594969671932223011
print("PASS")
```
