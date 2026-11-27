# Growing Gaussian divisors and exponentially fine exact chord meshes

A growing Gaussian divisor gives an **unconditional angular mesh of \(\exp(-c_m\sqrt K)\)** for a fixed coordinate modulus \(m\), within the ordinary-height budget. The divisor can be inserted into an actual 3,5 endpoint by a single CRT parameter. This reaches the original \(t=8\) critical band, with primitive chords and distinct numerical seeds. The construction chooses the target \(n\). At a prescribed target, the angular theorem applies when the actual endpoint contains the required divisor.

### A growing divisor with a controlled angle mesh

Let \(X=\operatorname{lcm}(2,m)\), \(r=X^2\), and
\[
\pi_j=X^{2j+1}+(-1)^ji,\qquad
G=\prod_{j=0}^{J}\bar\pi_j^{\,2r+1}.
\]
If \(G\mid Q\) in \(\mathbb Z[i]\), choose \(0\le k_j\le r\), put \(Z=\prod_j\bar\pi_j^{2k_j}\), and replace \(Q\) by \(Q'=(Q/Z)\bar Z\). This preserves its norm and both coordinates modulo \(m\); it preserves parity as well because each factor has odd norm and the exponent swaps are even. Indeed, \(\pi_j\equiv-\bar\pi_j\pmod m\), and all the factors are units modulo \(m\).

The rotation steps have alternating signs and magnitudes \(\alpha_j=4\arctan(X^{-(2j+1)})\). Reversing the digits on the negative axes makes the phase set a translate of the unsigned digit box. Since \(r\alpha_0>2\pi\) and \(\alpha_{j-1}\le r\alpha_j\), greedy subtraction approximates every full-turn phase to within a forward gap of \(\alpha_J<4X^{-(2J+1)}\) radians. The factor cost is explicit:
\[
\log_2 N(G)<(2r+1)\bigl(2(J+1)^2\log_2 X+J+1\bigr).
\]
Thus a mesh of width \(\varepsilon\) costs \(O_m(\log^2(1/\varepsilon))\) bits. This improves the previous fixed-axis rate obtained by transference from linear forms in logarithms. [Gouillon, Corollary 2.2](https://www.numdam.org/item/JTNB_2006__18_1_125_0.pdf#page=5)

The entire product \(G\) is primitive. Its norm is odd. If an odd Gaussian prime divided \(\pi_j\) and \(\bar\pi_k\), writing \(e_j=2j+1\) would give \(X^{e_j}=(-i)^{e_j}\) and \(X^{e_k}=i^{e_k}\) in its residue field. Raising to the opposite exponents gives a contradiction since \(e_je_k\) is odd. Consequently one orientation per rational prime suffices to force the whole product, even when its blocks share prime factors. Every rational prime in the product is split.

### Actual 3,5 targets in the critical band

Set \(K=90L\), \(A=9^L\), \(B=25^L\), \(H=27A+5B\), \(D=9A+2B\), and \(c=(D-1)/2\). Use the two integral endpoints
\[
P=(1+i)(c-it),\qquad Q=P+1+i,\qquad n=H+N(P).
\]
Then \(S=N(P)=n-27A-5B\) and \(N(Q)=S+2D=n-9A-B\). For \(W=2^{K/2}\) and \(3W/4\le t<7W/8\), the actual heights satisfy \(2^K\le S<2^{K+1}\) and \(B^{16}\le n\le A^{32}\).

Write \(G=u+iv\) and \(M=N(G)\). Since \(\gcd(u,v)=1\), the single congruence
\[
t\equiv -(c+1)v\,u^{-1}\pmod M
\]
forces \(G\mid Q\). It is independent of any prescribed \(t\bmod m\).

There is a common interval of rotation angles that works for **every** \(t\) in the height window. With \(q=N(Q'-P)/2\) and rotation angle \(\phi\),
\[
\left|\frac qS-(1-\cos\phi)\right|
\le \frac{D+\sqrt{2S}}{S}
<\frac{\Delta}{8},\qquad
\Delta=\frac1{64K^2(K+1)}.
\]
Take \(1-\cos\phi\) in the middle half of \((1/[64K(K+1)],1/[64K^2])\). Its inverse cosine interval has length greater than \(1/[32K(K+1)]\), since \(\sin\phi<1/(4K)\) there. Any rotation in this interval satisfies \(64K^2q<S<64K(K+1)q\).

The primitive-chord check also fits the CRT budget. The chord coordinates are odd, and a prime dividing both must divide \(D\). Primes dividing \(m\) are already handled by coordinate preservation. If \(p\mid N(G)\), the reserved copy of each original factor makes \(Q'\) vanish at a Gaussian prime above \(p\) where \(P=Q-(1+i)\) is nonzero. For any remaining \(p\mid D\), writing \(Z=a+ib\) gives the exact identity modulo \(p\)
\[
Z(Q'-P)/(1+i)=a-2bt.
\]
It forbids at most one residue of \(t\). The combined CRT period is at most \(mMD\), so \(mMD\le W/8\) suffices.

For fixed \(m\), taking \(J\) proportional to \(\sqrt K\) with a sufficiently small constant meets that budget for every sufficiently large \(L\). In fact, one can choose a single \(t\) retaining **\(\exp(c_m\sqrt K)\) distinct critical seeds** for some \(c_m>0\). Pack disjoint intervals of length \(2\alpha_J\) into the common angle interval and select one rotation per interval. At each remaining prime \(p\mid D\), choose a residue retaining at least a \(1-1/p\) fraction. The total loss is at most a factor \(1+\omega(D)\), and \(q\) is strictly increasing over the selected positive-angle interval, since the original endpoint's angular offset is exponentially small compared with the interval's distance from zero. For just one critical seed, the construction also works uniformly for \(m\le K^\eta\) with any fixed \(\eta<1/2\), since choosing \(J=O(1+\log K/\log X)\) costs \(O(m^2\log^2 K)=o(K)\) bits.

### Exact replay

This uses the digits selected before choosing \(t\). The CRT removes the bad residues without factoring \(D\). At the resulting same target, the unrotated chord has \(q=1\) and misses the band.

```python
from math import gcd

def mul(z,w):
    x,y=z
    a,b=w
    return x*a-y*b,x*b+y*a
def bar(z): return z[0],-z[1]
def N(z): return z[0]**2+z[1]**2
def power(z,k):
    a=(1,0)
    for _ in range(k):
        a=mul(a,z)
    return a
def div(z,w):
    u,v=mul(z,bar(w))
    d=N(w)
    assert u%d==v%d==0
    return u//d,v//d
def crt(a,M,b,d):
    assert gcd(M,d)==1
    return a if d==1 else a+M*((b-a)*pow(M,-1,d)%d)
def support(d,x):
    return gcd(d,pow(x,d.bit_length(),d))

L,m=205,6
K=90*L
A,B=9**L,25**L
H,D=27*A+5*B,9*A+2*B
c=(D-1)//2
G=Z=(1,0)
for j,k in enumerate((1,36,12,7,10,1,2,3)):
    z=(m**(2*j+1),-(-1)**j)
    G=mul(G,power(z,2*k+1))
    Z=mul(Z,power(z,2*k))
M=N(G)
u,v=G
t=crt(-(c+1)*v*pow(u,-1,M)%M,M,0,m)
d=D//support(D,M*m)
g=support(d,Z[0])
t=crt(t,M*m,crt(1,g,0,d//g),d)
W=2**(K//2)
lo=3*W//4
t=lo+(t-lo)%(M*m*d)
assert lo<=t<7*W//8 and t%m==0

P,Q=(c+t,c-t),(c+t+1,c-t+1)
div(Q,G)
Q1=mul(div(Q,Z),bar(Z))
assert all((x-y)%m==0 for x,y in zip(Q,Q1))
x,y=Q1[0]-P[0],Q1[1]-P[1]
S=N(P)
q=(x*x+y*y)//2
n=H+S
w=abs(x*P[1]-y*P[0])//2
assert 2**K<=S<2**(K+1) and B**16<=n<=A**32
assert N(Q1)==n-9*A-B==S+2*D
assert x%2==y%2==1 and gcd(x,y)==gcd(S,D)==gcd(q,D)==1
assert 2*q*S==(D-q)**2+4*w*w
assert 64*K*K*q<S<64*K*(K+1)*q
assert N((Q[0]-P[0],Q[1]-P[1]))==2 and S>64*K*(K+1)
print(K,M.bit_length(),(M*m*d).bit_length(),q.bit_length())
```

The output is `18450 4364 5320 18416`. The two extra gcd equalities in this fixture are individual checks. The growing theorem guarantees chord primitivity. Simultaneous construction for the separate second chord pair, and forcing the divisor at an arbitrary prescribed \(n\), remain open in this argument.