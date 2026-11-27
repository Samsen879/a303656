# Signed rough anchors with the large switched prime retained

**Keeping the large switched prime \(s\) in the sum gives an unconditional signed comparison for rough anchors.** On a concrete central-cofactor family, the normalized depth-two count exceeds the depth-zero count after sieve screening of \(p\), with an explicit positive secondary term. For true prime anchors, the exact remaining statistic is the signed count of rough **composite** anchors in the same windows and lifts. There are explicit certified composites in both lifts, with \(s\) still prime.

### The actual paired windows

Keep \(A=3^a,\ B=5^b\), even \(a,b\), and \(39/40<B/A<122/125\). Write \(S_0=A+25B,\ S=3^c+5^e,\ \kappa=(S_0-S)/45\). Use the original ranges \(a/10\le c\le a/3,\ b/5\le e\le b/3\), the congruences \(c\equiv a\pmod4,\ e\equiv b+2\pmod6\), and all seven phases \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). The target is \(n=S_0+45p\), with \(p\equiv1\pmod4\), in the unchanged window \(1457A-123B<n\le729A+625B\).

Take \((\log B)^{-1/2}\le\rho<1/250\) and \(13\rho\le\delta\le5/32\). Mark \(q,r\) in the original inert bands \((B^\rho,B^{2\rho}],(B^{2\rho},B^{3\rho}]\). Use the restricted central family
\[
 B^{1/2-\delta}<t\le B^{1/2-25\delta/26},\qquad
 h=P h_0,\quad B^{14\delta/13}<P\le B^{3\delta/2},\quad h_0\le B^{\delta/32},
\]
where \(t\) is inert prime, \(P\) is split prime, \(h_0\) is split-supported, and
\(\left|\Omega(h)-\tfrac12\log\log(32B^{2\delta})\right|\le\tfrac1{10}\log\log(32B^{2\delta})\).
Set \(d=qrth\) and require \((d,\kappa)=1\). The switched forms are \(p=wds-\kappa\), \(w=1,49\). For each marked \(d\), their paired \(s\)-intervals are exactly
\[
\left(\frac{X_-}{wd},\frac{X_+}{wd}\right],\qquad
X_-=\frac{1457A-123B-S}{45},\quad X_+=\frac{729A+625B-S}{45}.
\]
The size bounds give \(d\le B^{0.65}\) and \(s/t\gg B^{3\delta/416}\). Thus \(s>t\) throughout both windows for large \(B\), and the switched prime has scale \(B/d\ge B^{0.35}\).

For one lift in each class, choose a unit \(u\bmod343\) with \(45u\equiv-S\bmod49\), and \(j\in\{1,\ldots,6\}\). Impose
\[
s\equiv3\pmod4,\qquad
s\equiv d^{-1}u\pmod{343}\quad(w=1),\qquad
s\equiv d^{-1}j\pmod7\quad(w=49).
\]
These give \(p+\kappa\equiv u\) and \(49j\pmod{343}\), respectively. Both lifts have density \(\alpha=1/588\) in the \(p\)-variable. Summing the seven and six lifts gives the original \(\alpha_1=1/84,\alpha_{49}=1/98\).

### Signed comparison with \(s\) prime

Let \(R_{d,w}(z)\) count **prime \(s\)** in the specified interval and lift for which \(p=wds-\kappa\) has no prime factor at most \(z\). Put \(L=\log\log B\) and \(z=B^{\log L/(1000L)}\). Uniformly over these rows and each fixed lift,
\[
\frac{R_{d,w}(z)}{\alpha}
 =\frac{V_d(z)}{d}\int_{X_-}^{X_+}\frac{dx}{\log(x/(wd))}
 +O\!\left(\frac{B}{d(\log B)^8}\right),
\qquad
V_d(z)=\prod_{\substack{\lambda\le z,\ \lambda\ {\rm prime}\\
                         \lambda\nmid14d\kappa}}
                  \left(1-\frac1{\lambda-1}\right).
\]
The same formula holds for the full classes with their respective normalizations.

For a sieve divisor \(e\) of \(p\), the prime variable is \(s\), and the progression modulus is \(1372e\) or \(28e\). The large coefficient \(d\) enters the residue, not the modulus. For \(\lambda\nmid14d\kappa\) there is one reduced residue for \(s\), with density \(1/(\lambda-1)\). Primes dividing \(d\) give no root, and primes dividing \(\kappa\) can only force \(s\equiv0\), impossible since \(s>z\). Apply Bombieri–Vinogradov in \(s\) with divisor level \((B/d)^{2/5}\). The fundamental lemma has sieve parameter at least \(140L/\log L\), making its relative error smaller than \((\log B)^{-10}\). This gives the formula on the two exact endpoints. [Bombieri, *On the large sieve*](https://doi.org/10.1112/S0025579300005313) · [Kurlberg, Lester and Rosenzweig, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

The normalized depth-two excess therefore has positive main term
\[
D_d(z)=\frac{\log49\,V_d(z)}d
       \int_{X_-}^{X_+}
          \frac{dx}{\log(x/d)\log(x/(49d))}.
\]
The sign comes from the ordinary density of \(s\) in the interval scaled by \(1/49\). If each term is weighted by \(\log s\), the two main terms agree.

Summing over the restricted family for label \(\ell\) gives \(D_\ell(z)=\sum_d D_d(z)\asymp\delta^{3/2}M_\ell/\log z\), where
\[
M_\ell=\frac{B}{(\log B)^{3/2}}
       \prod_{\substack{\lambda\mid\kappa,\ \lambda\ {\rm prime}\\
                        \lambda\equiv3\ (4)}}\frac{\lambda-1}{\lambda-2}.
\]
This evaluates the **rough** contrast. The harmonic calculation uses bounded \(q,r\) and \(P\) sums, a \(t\)-sum of order \(\delta\), and corrected central \(h_0\)-weight of order \(\sqrt{\delta\log B}\). It gives no lower bound for the prime-pair mass.

Let \(C_{\ell,w}(z)\) count the survivors with \(p\) composite, still with \(s\) prime. Write \(\Delta^+\) for depth two minus depth zero after normalization. The normalized true prime-pair difference satisfies
\[
\boxed{\displaystyle
\Delta^+\mathrm{PrimePair}_\ell
=D_\ell(z)-\Delta^+C_\ell(z)
 +O\!\left(\delta^{3/2}M_\ell(\log B)^{-6}\right).}
\]
Thus an upper bound \(\Delta^+C_\ell(z)\le(1-\varepsilon)D_\ell(z)\) would suffice for a positive sign. The composite statistic has an exact least-divisor range \(z<P^-(p)\le\sqrt p\). A neighboring portion is already comparable: the composite band \(z^{1/2}<P^-(p)\le z\) has signed contrast \((1+o(1))D_\ell(z)\), by subtracting the two rough formulas and using \(V_d(z^{1/2})\sim2V_d(z)\) uniformly. The signed composite tail above \(z\) remains unresolved.

### Exact same-lift replay

The code checks three controls in each class at \((a,b,c,e)=(712,486,80,122)\): a true alternate, a certified prime anchor with four odd inert valuations, and a composite \(p\) with certified prime \(s\), no divisor through \(1000\), and an exact factor \(65537\). Each class uses one fixed lift modulo \(343\). The two switched controls have the same \(d\) within their class and meet the geometric bands above at \(\rho=1/375,\delta=5/32\). The finite roughness check uses \(1000\); the fixtures make no asymptotic error claim at their finite height.

`cert` uses order tests to force every prime divisor to be \(1\bmod m\). A composite below \(m^3\) would have two such factors, giving a square discriminant from the two base-\(m\) digits of \((n-1)/m\).

```python
from math import factorial, gcd, isqrt, log

def cert(n,m,*rows):
    assert 1<n<m**3 and (n-1)%m==0
    rem=m
    for ell,a in rows:
        assert rem%ell==0
        while rem%ell==0: rem//=ell
        y=pow(a,(n-1)//ell,n)
        assert pow(y,ell,n)==1 and gcd(y-1,n)==1
    assert rem==1
    if n>=m*m:
        hi,lo=divmod((n-1)//m,m)
        D=lo*lo-4*hi
        assert D<0 or isqrt(D)**2!=D

def crt(x,m,b,d): return x+m*((b-x)*pow(m,-1,d)%d)
def first(x,m,L): return x+m*((L-x+m-1)//m)

A,B=3**712,5**486
S0,S=A+25*B,3**80+5**122
k,rem=divmod(S0-S,45)
L,U=(1457*A-123*B-S0)//45+1,(729*A+625*B-S0)//45
r0=(pow(3,716,49)+pow(5,488,49)+7)%49
assert rem==k%8==0 and S%49==r0==27 and 39*A<40*B and 125*B<122*A
assert B<59**375<B**2<67**375<B**3
assert all(all(n%d for d in range(2,isqrt(n)+1)) for n in (59,67,127,257,65537))
R0=(1<<127)-1
v=4
for _ in range(125): v=(v*v-2)%R0
assert v==0                         # Lucas–Lehmer
m=514*R0
t=m*((1<<394)//m+114)+1
cert(t,m,(2,3),(257,2),(R0,2))
assert t%4==3 and B**11<t**32 and t**832<=B**291
assert 25**1024<=B**5 and 5<log(log(32)+5*log(B)/16)<6
R=(1<<157)+(307<<90)+1
cert(R,1<<90,(2,11))
J,Q=1<<89,1<<222

def check(p,w,res):
    assert L<=p<=U and p%4==1 and (p+k)%343==res
    assert (S0+45*p)%49==(0 if w==1 else r0)
    assert (p+k)%7!=0 if w==1 else res==49

for w,j,wp,i,ws,res,j0,ic,wc in [
    (1,46,3,93654,13,264,66,73,19), (49,52,5,36203,3,49,88,993,2)
]:
    C=w*59*67*t*25
    z=crt(1+J,2*J,(k+1)*pow(C,-1,R),R)
    P=first(z,2*J*R,1<<259)+j*2*J*R
    cert(P,J,(2,wp))
    assert P%4==1 and B**35<P**208 and P**64<=B**15
    G=C*P
    d=49 if w==1 else 7
    b=-S*pow(45*G,-1,49) if w==1 else pow(G//w,-1,7)
    z=crt((k+1+Q)*pow(G,-1,2*Q)%(2*Q),2*Q,1,R)
    z=crt(z,2*Q*R,b,d)
    M=2*Q*R*d
    s=first(z,M,(L+k+G-1)//G)+i*M
    cert(s,2*R,(2,ws),(R,2))
    assert s>t and s%4==3 and gcd(G,k)==1
    p=G*s-k
    cert(p,Q*R,(2,5),(R,2))
    check(p,w,res)                  # four exact odd inert valuations

    Q0=1<<378
    f=4*((isqrt((L+k)//w)+4)//4+j0)
    h,rem=divmod(((k+1+Q0)*pow(w,-1,2*Q0)-f*f-1)%(2*Q0),8)
    assert rem==0
    x=h%2
    for e in range(2,377): x+=(h-2*x*x-x)%(1<<e)
    x=1+4*x
    d0,a0=(343,264) if w==1 else (7,1)
    z=next(z for z in range(d0) if (z*z+f*f-a0)%d0==0)
    x=crt(x,Q0,z,d0)
    p=w*(x*x+f*f)-k
    cert(p,Q0,(2,5))
    check(p,w,res)                  # true alternate

    d1,b1=(343,res*pow(G,-1,343)) if w==1 else (7,b)
    z=crt(crt(3,4,1,R),4*R,b1,d1)
    M=4*R*d1
    F=65537
    z=crt(z,M,k*pow(G,-1,F),F)
    M*=F
    s=first(z,M,(L+k+G-1)//G)+ic*M
    cert(s,2*R,(2,wc),(R,2))
    p=G*s-k
    check(p,w,res)
    assert s>t and s%4==3 and p>F and p%F==0 and p%(F*F)!=0
    assert gcd(p,factorial(1000))==1
```
