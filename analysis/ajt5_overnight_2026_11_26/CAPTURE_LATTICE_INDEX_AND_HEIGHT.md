# Capture-lattice index and certified short-word height

Let A=3^(LH), B=5^(LH) modulo a prime p dividing the source, with H a power of 7 killing its 7-primary subgroup. The capture lattice ker[(u,v)↦A^uB^v] has index m=lcm(ord A,ord B). Any two independent captured words have determinant a nonzero multiple of m. If an integer-primitive captured word w is known, complete it to a determinant-one basis w,τ. Then m is the exact order of χ(τ), and the lattice consists precisely of j m τ+t w. For the minimum sup norm of a captured word independent of w,
```
ceil(m/||w||_1) ≤ height ≤ floor(m/||w||_1 + ||w||_∞/2).
```
The determinant gives the lower bound. On the real line det(w,z)=m the shortest sup norm is m/||w||_1, and rounding the coefficient along w moves the point by at most ||w||_∞/2. This layer is also transverse modulo 7 because the residual index is prime to 7. For an exact height h, test only 1≤j≤h||w||_1/m using the intersection of the two corresponding integer coordinate intervals for t.

If a longer independent captured word exists on common composite support, its determinant with w provides an exponent multiple T for χ(τ) on that support. Factoring the integer T (not necessarily the source) and testing its divisors using saturated gcd can split the support by exact m. The geometric upper bound by itself does not supply such a multiple or a guaranteed small search.

In actual source (16,186), w=(2663,260) and an existing longer captured word give T=5477558. The two parts of the composite support have residual indices 1 and 2738779. On the latter, the exact successive sup-norm minima are **973 and 2095**, witnessed by (−568,973) and (−2095,−1233). At the first radius the determinant against w permits only layers 0 and ±m, and layer 0 has no nonzero word that short. At the second radius the same statement holds relative to the first witness, which is primitive; the least independent word comes from one of the layers ±m. The perpendicular-height minimization in the replay uses the two adjacent integers to the real minimizer.

For the still-unfactored remainder 1707542200628666649958800561642353 from (14,152), a direct finite certificate gives ord(A),ord(B)>23068809 at **every** factor prime. Indeed each product of A^j−1 (or B^j−1) for 1≤j≤23068809 has gcd 1 with the remainder; prime factors are not input. Since two words of sup norm h have determinant at most 2h², no factor admits two independent captured words in any box of half-width ≤3396 with this fixed mask. This lower bound says neither that the next box works nor where the first capture lies.

```python
from math import gcd, isqrt, prod

K = 2**19
s = bytearray(b'\1')*(K+1)
s[:2] = b'\0\0'
for a in range(2,isqrt(K)+1):
    if s[a]:
        s[a*a::a] = b'\0'*((K-a*a)//a+1)
def pp(a):
    b=a
    while b*a<=K:
        b*=a
    return b
L=prod(pp(a) for a in range(2,K+1) if s[a] and a!=7)

def det(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(w): return max(map(abs,w))
def l1(w): return sum(map(abs,w))
def tau(w):
    u,v=w
    if not v:
        return (0,u)
    y=pow(u,-1,abs(v)) if abs(v)>1 else 0
    return ((u*y-1)//v,y)
def least_layer(w,m):
    z=tuple(m*x for x in tau(w))
    j=-sum(x*(1 if a>=0 else -1) for x,a in zip(z,w))//l1(w)
    return min((tuple(x+i*a for x,a in zip(z,w)) for i in (j,j+1)),key=norm)

R=21831913108948893248715238773608846587809381120739
A,B=(pow(a,L*7**R.bit_length(),R) for a in (3,5))
def chi(w): return pow(A,w[0],R)*pow(B,w[1],R)%R
w,b=(2663,260),(3799,-1686)
C=gcd(R,chi(w)-1,chi(b)-1)
while (g:=gcd(R,C*C))!=C:
    C=g
eta=chi(tau(w))
T=abs(det(w,b))
m=T//2
assert det(w,tau(w))==1 and T==2*m==5477558 and pow(eta,T,C)==1
assert all(m%d for d in range(2,isqrt(m)+1))
high=gcd(C,eta-1)
p=C//high
assert (high,p)==(572493630662019608249,332548023739) and gcd(high,p)==1
assert pow(eta,m,p)==1 and gcd(p,pow(eta,2,p)-1)==1
for a in (3,5):
    raw=pow(a,L*m,C)
    assert [gcd(C,pow(raw,7**j,C)-1) for j in (2,3,4,5)]==[1,p,p,C]
z=least_layer(w,m)
v=least_layer(z,m)
assert (z,v)==((-568,973),(-2095,-1233)) and gcd(*z)==1
assert chi(z)%p==chi(v)%p==1
assert 2*m>norm(z)*l1(w) and norm(w)>norm(z)
assert 2*m>norm(v)*l1(z)
assert all(2401*l1(c)<m for c in ((-269,798),(73,114),(853,114)))

Q=1707542200628666649958800561642353
M=(2*2401+1)**2
for a in (3,5):
    A=pow(a,L*7**Q.bit_length(),Q)
    z=f=1
    for _ in range(M):
        z=z*A%Q
        f=f*(z-1)%Q
    assert gcd(f,Q)==1
assert isqrt(M//2)+1==3397
print("PASS")
```
