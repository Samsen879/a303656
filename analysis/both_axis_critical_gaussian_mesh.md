# Primitive critical Gaussian meshes on a mixed 3/5 edge

There is a **growing primitive critical mesh on an edge that changes both exponents**, starting from the non-diagonal displacement \((1,3)\). The same argument gives a direction-independent obstruction to adding a second edge in a natural class of affine constructions. In that class, a repeated exponent on either axis rules out both-axis motion with an integral critical certificate. Even with both axes all distinct, a span of at most seven on the 5-axis allows at most two labels if any edge has a critical certificate.

### Where the two-mesh construction stops

Take \(a=3^L,\ b=5^L\), and labels with fixed offsets \((2L+\alpha_i,2L+\beta_i)\). Consider starting endpoints
\[
P_i(t)=V_i t+aW_{i,3}+bW_{i,5}
\]
with fixed rational vectors, nonzero directions \(V_i\), and endpoints made integral on a common parameter progression. Allow the directions \(V_i\) to differ. Assume the label plus \(N(P_i(t))\) is the same target polynomial for all labels, for infinitely many \(L\).

Equality of the quadratic and linear coefficients in \(t\) gives a common leading norm \(\lambda=N(V_i)\) and a common translation of \(t\). Completing the square leaves a perpendicular offset \(\lambda(u_i a+v_i b)^2\), with rational \(u_i,v_i\). Comparing the coefficients of \(9^L,15^L,25^L\) then gives
\[
C_3=3^{\alpha_i}+\lambda u_i^2,\qquad
C_5=5^{\beta_i}+\lambda v_i^2,\qquad
u_i v_i=\text{constant}.
\]

**If either axis repeats, the common product is zero.** For example, equal \(\beta_i\) gives equal \(v_i^2\). With nonzero product this also gives equal \(u_i^2\), hence equal \(\alpha_i\). With product zero and variation on both axes, there must be both a nonzero pure-3 offset and a nonzero pure-5 offset. In particular \(C_3\) is a power of 3, \(C_5\) is a power of 5, and a nonzero 5-power difference must be \(\lambda\) times a rational square.

An even exponent gap on the 5-axis is impossible in that last equality. If \(s\) is the odd part of the gap, then \((5^s+1)/2\equiv3\bmod4\). It has an inert prime to odd depth, and that depth persists in the full power difference. A rational Gaussian norm has even valuation at every inert prime, and \(\lambda\) is such a norm. An odd 5-exponent gap instead gives valuation exactly 2 at 2, forcing \(v_2(\lambda)\) even. Then every 3-exponent has the same parity as the exponent of \(C_3\), since an opposite-parity 3-power difference has valuation 1 at 2. Every half norm gap \(D\) is therefore even. The critical identity \(2qS=(D-q)^2+4w^2\) with odd \(q\) and integral \(w\) requires \(D\) odd, independently of the starting directions or subsequent rotations.

**If the common product is nonzero**, every pair of distinct labels has the necessary condition
\[
-\frac{3^{\alpha_i}-3^{\alpha_j}}{5^{\beta_i}-5^{\beta_j}}
=\left(\frac{u_i u_j}{u_i v_i}\right)^2.
\]
The axes are strictly ordered in opposite directions. For an odd 3-exponent gap, the 5-exponent gap \(e\) must have odd \(v_2(e)\). In a span of seven this leaves \(e=2\) or \(6\). Gap 6 fails at 7, since \(v_7(5^6-1)=1\) and 3 has order 6 modulo 7. Gap 2 forces the lower 3-exponent odd by the valuation at 3. If there were three labels and an opposite-parity pair, the two opposite-parity comparisons would both have 5-gap 2. Their common label would have to be the middle one, so the two lower 3-exponents in those comparisons have opposite parity. This is a contradiction.

The two-label bound in the last case is attained at the level of the affine identity:
\[
3A+25B+2(2a+2b)^2
=9A+B+2(a+4b)^2
=11A+16ab+33B,\qquad A=a^2,\quad B=b^2.
\]
The actual labels here change on both axes. The obstruction leaves open larger 5-spans with all offsets distinct and constructions outside the affine model.

### A genuine mixed edge from \((1,3)\)

Use those same two shifts \(H=3A+25B\) and \(9A+B\), with half gap \(D=12B-3A\). Set
\[
P=(D-5-3t,t),\qquad Q=P+(1,3),\qquad n=H+N(P).
\]
Then \(N(Q)=n-9A-B\). For \(K=90L\), \(W=2^{K/2}\), take \(W/3\le t<3W/8\). For sufficiently large \(L\), this gives \(2^K\le N(P)<2^{K+1}\) and \(B^{16}\le n\le A^{32}\).

Use the Gaussian factors \(\pi_j=6^{2j+1}+(-1)^ji\), forcing \(\prod_{j=0}^J\bar\pi_j^{73}\mid Q\). The even switches \(0\le 2k_j\le72\) preserve coordinates modulo 6 and have a full-turn mesh with gap at most \(4\cdot6^{-(2J+1)}\) radians. This follows by greedy subtraction after reversing the negative-angle digits. Successive step sizes have ratio at most 36. The product is primitive and its norm \(M\) is coprime to 30. Indeed, if a rational prime divides two factor norms, the order of 6 modulo that prime has the form \(4r\) with \(r\) odd, and both indexed exponents \(2j+1\) are odd multiples of \(r\). The ratio of their powers of 6 is \((-1)^{j_1-j_2}\), as is the ratio of their imaginary signs. Hence these factors use the same Gaussian prime above it, never conjugate Gaussian primes. If the product is \(u+iv\), put \(I=-u/v\bmod M\). The required scalar class is
\[
t\equiv -(D-4+3I)(I-3)^{-1}\pmod M.
\]
The inverse exists because the direction \((-3,1)\) has norm 10.

For \(R=(Q/Z)\bar Z\), \(Z=z+iw_0\), the remaining primitive-chord test is particularly simple. At an odd \(p\mid D\) outside \(6M\), a common coordinate divisor is equivalent to
\[
z+(2t+3)w_0\equiv0\pmod p.
\]
This follows by dividing \(Z(R-P)\) by \(1+3i\) modulo \(p\). It forbids at most one class, since \(Z\) is primitive. At \(p\mid D\cap M\), a reserved original copy of the Gaussian factor keeps \(R\) zero in a component where \(P=Q-(1+3i)\) is nonzero. Modulo 6 the chord retains \((1,3)\).

The CRT period is at most \(6MD\), which fits for \(J\) a sufficiently small constant times \(\sqrt K\). The physical ratio \(q/N(P)\) differs from \(1-\cos\phi\) by at most \((D+\sqrt{10N(P)})/N(P)\). This is exponentially smaller than the critical ratio width. The critical angle interval, defined by \(64K^2q<S<64K(K+1)q\) for \(S=N(P)\), has length \(\gg K^{-2}\). Selecting separated mesh angles there and choosing each remaining local class of \(t\) to retain at least a \(1-1/p\) fraction of the survivors gives (the product over primes dividing \(D\) costs at most a factor of order \(\log\log(3D)\)) \(\exp(c\sqrt K)\) distinct primitive critical seeds at one target. The square determinant really is \(4w^2\), since the coordinates of \(P\) have the same parity and both chord coordinates are odd.

### Exact replay

The replay forces the factors needed for one rotation. It checks the genuine integral certificate and the unrotated failure at the same target.

```python
from math import gcd

def mul(z,w):
    x,y=z
    a,b=w
    return x*a-y*b,x*b+y*a
def bar(z): return z[0],-z[1]
def N(z): return z[0]**2+z[1]**2
def div(z,w):
    x,y=mul(z,bar(w))
    m=N(w)
    assert x%m==y%m==0
    return x//m,y//m
def crt(a,m,b,d):
    assert gcd(m,d)==1
    return a if d==1 else a+m*((b-a)*pow(m,-1,d)%d)
def support(a,b):
    return gcd(a,pow(b,a.bit_length(),a))

L=205
K=90*L
W=2**(K//2)
a,b=3**L,5**L
A,B=a*a,b*b
H,D=3*A+25*B,12*B-3*A
assert H+2*(2*a+2*b)**2==9*A+B+2*(a+4*b)**2
assert pow(5,6,7)==1 and pow(5,6,49)!=1
assert pow(3,3,7)==6 and pow(3,2,7)!=1

G=Z=(1,0)
for j,k in enumerate((1,36,12,7,10,1,2,3)):
    axis=(6**(2*j+1),-(-1)**j)
    for _ in range(2*k):
        Z=mul(Z,axis)
    G=mul(G,axis)
G=mul(G,Z)
u,v=G
M=N(G)
assert gcd(u,v)==gcd(M,30)==1
I=-u*pow(v,-1,M)%M
t=-(D-4+3*I)*pow(I-3,-1,M)%M
t=crt(t,M,0,6)
d=D//support(D,6*M)
z,w0=Z
g=support(d,z+3*w0)
t=crt(t,6*M,crt(1,g,0,d//g),d)
lo=(W+2)//3
t=lo+(t-lo)%(6*M*d)
assert lo<=t<3*W//8

P=(D-5-3*t,t)
Q=(P[0]+1,P[1]+3)
div(Q,G)
R=mul(div(Q,Z),bar(Z))
x,y=R[0]-P[0],R[1]-P[1]
S,q=N(P),(x*x+y*y)//2
n=H+S
h=abs(x*P[1]-y*P[0])
assert 2**K<=S<2**(K+1) and B**16<=n<=A**32
assert N(R)==n-9*A-B==S+2*D
assert all((u-v)%6==0 for u,v in zip(Q,R))
assert x%2==y%2==1 and gcd(x,y)==1 and h%2==0
assert 2*q*S==(D-q)**2+h*h
assert 64*K*K*q<S<64*K*(K+1)*q
assert 64*K*(K+1)*5<S
print(K,M.bit_length(),(6*M*d).bit_length(),q.bit_length())
```

Output `18450 4364 5317 18416`. This supplies one growing mixed edge. Two independent primitive meshes at the same two-axis target remain open outside the excluded affine cases.
