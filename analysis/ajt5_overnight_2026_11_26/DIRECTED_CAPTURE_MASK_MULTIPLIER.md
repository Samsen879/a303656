# Choose a mask multiplier from captured determinants

At a prime p let the old 7-free capture character have cyclic image of order m_p and kernel Λ_p. Multiplying the mask L by M changes the capture condition to χ_p(w)^M=1, enlarging the kernel by index gcd(m_p,M); its new index in Z² is m_p/gcd(m_p,M). Captured old words (and their physical mod-7 transversality) remain. The 7-part of M does not affect this capture index. It **does** affect the unmasked 7-primary read: if M is prime to 7 the original primary read can be recovered by raising to M^(-1) modulo an annihilating 7-power, but a factor of 7 can erase precision and falsely pass an order gate.

For a fixed set of candidate short words, let t_p be the least common multiple of their orders under the original capture character. Their joint capture after M holds exactly on primes with t_p|M. Given a factored integer T, use saturated joint gcd at exponent T, and at exponents T/l^j for each l dividing T. The nested supports determine each v_l(t_p) on the first joint block; taking intersections resolves the entire divisor menu M|T, without factoring the source. For the two axis words, t_p=m_p. Any two independent words in the original kernel supply T equal to their nonzero determinant magnitude.

## Exact control

At actual source (16,186), use the independently detected physical words (−2095,−1233),(1136,−1946), whose determinant magnitude is T=5477558=2·2738779. Choosing the fixed leaf words (1,0),(0,1) gives these exact capture results:
- M=1 or 2 captures only 572493630662019608249.
- M=2738779 or T also captures 332548023739. Its residual index falls from 2738779 to 1 and the shortest independent pair is now in the half-width 1 box.
- M=49T has the same capture support as T but reduces the high block from order 7^5 to 343 in the uncorrected axis reads. That would be a false acceptance at a 343-order gate.

For the still-unfactored (14,152) remainder the exact replay verifies no nonzero half-width 1 capture after T, so its divisor menu cannot help there. The prior certified bound m_p>23068809 on each factor also rules out two independent half-width 1 words for every M≤11534404: the new index is >2, larger than the greatest determinant in the box. This does not determine where the first successful mask occurs.

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

def sat(n,d):
    while (g:=gcd(n,d*d))!=d:
        d=g
    return d

R=21831913108948893248715238773608846587809381120739
H=7**R.bit_length()
U,V=(pow(a,L,R) for a in (3,5))
A,B=(pow(a,H,R) for a in (U,V))
def capture(n,M,*words):
    return sat(n,gcd(n,*(
        pow(pow(A,u,n)*pow(B,v,n)%n,M,n)-1 for u,v in words)))

w,z=(-2095,-1233),(1136,-1946)
T=abs(w[0]*z[1]-w[1]*z[0])
m=T//2
assert T==2*m==5477558 and gcd(T,7)==1
assert all(m%d for d in range(2,isqrt(m)+1))
C=capture(R,1,w,z)
axes=((1,0),(0,1))
g1,g2,gm,gT=(capture(C,i,*axes) for i in (1,2,m,T))
assert g1==g2==572493630662019608249
assert gm==gT==C==190381625479819594969671932223011
p=C//g1
assert p==332548023739 and gcd(p,g1)==1
assert all(capture(R,1,w)==g1 for w in (*axes,(1,1),(1,-1)))
assert capture(R,T,*axes)==capture(R,49*T,*axes)==C

for a in (U,V):
    b=pow(a,T,C)
    assert [gcd(C,pow(b,7**j,C)-1) for j in (2,3,4,5)]==[1,p,p,C]
    assert pow(pow(b,49,C),343,C)==1

Q=1707542200628666649958800561642353
P,S=(pow(a,L*T*7**Q.bit_length(),Q) for a in (3,5))
assert all(gcd(Q,d)==1 for d in (P-1,S-1,P*S-1,P-S))
print("PASS")
```
