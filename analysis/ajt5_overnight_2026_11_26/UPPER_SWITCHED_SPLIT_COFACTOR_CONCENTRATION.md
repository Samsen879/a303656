# Split-cofactor concentration in the upper switched residual

The upper residual can be narrowed by the number of split prime factors in its remaining cofactor. In the band \(B^{1/2-13\rho}<t\le B^{1/2-12\rho}\), cofactors outside any fixed relative neighborhood of the usual half-dimensional prime-factor count contribute **\(o(\rho^{3/2}\mathcal M)\)** to the normalized contrast. This is below the previous error scale for the marked sign. The normalized sign for the cofactors inside that neighborhood remains open.

### A switched cofactor bound

Keep \(A=3^a,\ B=5^b\), with even \(a,b\) and \(39/40<B/A<122/125\). As before,
\[
S_0=A+25B,\qquad S=3^c+5^e,\qquad \kappa=(S_0-S)/45.
\]
Use \(a/10\le c\le a/3,\ b/5\le e\le b/3,\ c\equiv a\pmod4,\ e\equiv b+2\pmod6\), and all seven phases with \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). A prime anchor is \(n=S_0+45p\), with \(p\equiv1\pmod4\) prime, in the exact window \(1457A-123B<n\le729A+625B\). For \(w=1\) require \(n\equiv0\pmod{49}\), and for \(w=49\) require \(v_7(p+\kappa)=2\). The progression densities remain \(\alpha_1=1/84,\ \alpha_{49}=1/98\).

Mark the inert primes \(q\in(B^\rho,B^{2\rho}]\), \(r\in(B^{2\rho},B^{3\rho}]\), and let \(t\) be the least additional inert prime. Take
\[
(\log B)^{-1/2}\le\rho<1/250,\qquad
12\rho<\delta\le5/32,\qquad
B^{1/2-\delta}<t\le B^{1/2-12\rho}.
\]
Parity and the size bound give the exact form
\[
(p+\kappa)/w=qr\,t\,s\,h,\qquad t\le s,\qquad
h\le H=32B^{2\delta},
\]
where \(s\) is inert and every prime divisor of \(h\) is \(1\bmod4\). Indeed the cofactor after \(qr\) is \(1\bmod4\), and three inert factors of size at least \(t\) already exceed \(32B\) for large \(B\). Repetitions \(t=s\) contribute \(O(B^{21/32})\) per label by counting square divisors.

Put \(L_H=\log\log H\) and \(I(\gamma)=\tfrac12-\gamma+\gamma\log(2\gamma)\). For \(0<\gamma<1/2\), count the stratum \(\Omega(h)\le\gamma L_H\). For \(1/2<\gamma<5/2\), count \(\Omega(h)\ge\gamma L_H\). In either case the absolute **normalized** difference between the two classes is at most
\[
\boxed{\displaystyle
 O_\gamma\!\left(
 M_\ell\,\delta^{3/2}(\delta\log B)^{-I(\gamma)}
 (\log\log B)^{(1-2\gamma)_+/2}
 \right)+O(B^{21/32}),}
\qquad
M_\ell=\frac{B}{(\log B)^{3/2}}
\prod_{\substack{j\mid\kappa\\ j\equiv3\ (4),\ j\ {\rm prime}}}
\frac{j-1}{j-2}.
\]
The estimate is uniform over the actual labels. At \(\delta=13\rho\), either fixed tail cutoff has \(I(\gamma)>0\), so the bound is \(o(\rho^{3/2}M_\ell)\). This is an absolute loss bound at the scale of the previous sign criterion. It does not require a lower bound for the population of this upper band.

**Proof.** Fix \(q,r,t,h\), and apply the two-form upper sieve in \(s\) to \(s\) and \(wqrhts-\kappa\). The variable has scale \(N\asymp B/(wqrht)\), with \(N\gg B^{11/32}\) whenever a pair occurs. Write \(F(m)=\prod_{j>2,\ j\mid m}(j-1)/(j-2)\). The upper bound is \(O(NF(wqrht\kappa)/(\log B)^2)\). At odd primes outside the coefficient and \(\kappa\) there are two distinct roots, and at primes dividing exactly one there is one root. A common prime divisor of the coefficient and \(\kappa\) would divide the much larger prime \(p\), so such rows contribute nothing. The selected split primes dividing \(\kappa\) that exceed \(H\) cost a bounded product, since their reciprocal sum is \(O(\log B/(H\log H))\). The two marked harmonic sums are bounded and the \(t\)-sum costs \(O(\delta)\). The exact 7-adic lifts remain in the counts. Dropping them for this upper bound costs only a fixed normalization factor. [Nath and Xie, Lemma 3.6](https://arxiv.org/html/2501.16723v1#S3).

For \(z=2\gamma<5\), either tail indicator is bounded by \(z^{\Omega(h)-\gamma L_H}\). For each split prime \(j\nmid\kappa\) the weighted harmonic Euler factor is \(1+F(j)z/(j-z)\), with logarithm \(z/j+O_\gamma(j^{-2})\). Multiplying by the split singular factors from \(\kappa\) leaves the correction
\[
(1-z)\sum_{\substack{j\le H,\ j\mid\kappa\\j\equiv1\ (4)}}\frac1j+O_\gamma(1)
\]
in the logarithm. The sum is at most \(\tfrac12\log\log\log B+O(1)\), by splitting at \((\log B)^2\) and using \(\kappa\ll B\). Thus the weighted \(h\)-sum including the split correction is
\[
O_\gamma\!\left((\log H)^{\gamma-\gamma\log(2\gamma)}
(\log\log B)^{(1-2\gamma)_+/2}\right).
\]
Combining this with the \(t\)-sum proves the bound.

### Where the progression shortcut stops

Marking both \(t,s\) produces modulus \(196qrts\) or \(1372qrts\), even before a sieve divisor is attached. It exceeds \(B^{11/16+3\rho}\) throughout this band. This is beyond \(B^{3/5}\) even if one grants the other hypotheses of the triply well-factorable progression theorem. The exact \(h=1\) examples below have modulus of order \(B\). [Maynard, *Primes in arithmetic progressions to large moduli II*, Theorem 1.1](https://arxiv.org/pdf/2006.07088).

Fixing just \(wqrht\) and using a linear lower sieve for prime \(s\) hits a separate limit. Detecting primality up to \(N\) requires sieving through order \(\sqrt N\). A positive linear lower-sieve main term needs \(\log D/\log\sqrt N>2\), while any progression level \(B^{1-\varepsilon}\) allows only \(D\ll NB^{-\varepsilon}\). Thus a direct progression theorem followed by that lower sieve cannot compare the two prime forms. A signed estimate for the switched prime pair with the split cofactor retained would address a different statistic and remains unresolved. [Iwaniec, *Rosser’s sieve*](https://eudml.org/doc/205669).

### Exact same-label controls

This replay uses \((a,b,c,e)=(712,486,80,122)\), \(\rho=1/375\) and \(\delta=5/32\). It verifies a true alternate and an \(h=1\) failure with four distinct odd inert valuations in each class. The failures have \(395\)-bit \(t\) and \(728\)- or \(722\)-bit \(s\). The two depth-two controls have the same lift \(p+\kappa\equiv49\pmod{343}\).

In `cert`, the order tests force every prime divisor to be \(1\bmod m\). If \(n<m^3\) were composite, two factors \(1+mu,1+mv\) would give base-\(m\) digits \(uv,u+v\) for \((n-1)/m\), with square discriminant.

```python
from math import gcd, isqrt

def cert(n,m,rows):
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

A,B=3**712,5**486
S0,S=A+25*B,3**80+5**122
k,rem=divmod(S0-S,45)
L,U=(1457*A-123*B-S0)//45+1,(729*A+625*B-S0)//45
r0=(pow(3,716,49)+pow(5,488,49)+7)%49
assert rem==k%8==0 and S%49==r0==27 and 39*A<40*B and 125*B<122*A
assert B<59**375<B**2<67**375<B**3
assert all(all(v%d for d in range(2,isqrt(v)+1)) for v in (59,67,127,257))
Q,R0=1<<378,(1<<127)-1
v=4
for _ in range(125): v=(v*v-2)%R0
assert v==0  # Lucas–Lehmer
R=(1<<245)+(299<<128)+1
cert(R,1<<128,[(2,3)])
Qt=2*257*R0
t=Qt*((1<<394)//Qt+114)+1
cert(t,Qt,[(2,3),(257,2),(R0,2)])
assert t%4==3 and B**11<t**32 and t**250<B**117

def lift(x,m,b,d): return x+m*((b-x)*pow(m,-1,d)%d)
def check(p,w):
    cert(p,Q,[(2,5)])
    assert L<=p<=U and p%4==1
    assert (S0+45*p)%49==(0 if w==1 else r0)
    assert (p+k)%7!=0 if w==1 else (p+k)%343==49

for w,i,j in [(1,71134,1088),(49,6989,88)]:
    G=w*59*67*t
    d=49 if w==1 else 7
    b=-S*pow(45*G,-1,49) if w==1 else pow(59*67*t,-1,7)
    z=lift((k+1+Q)*pow(G,-1,2*Q)%(2*Q),2*Q,1,R)
    z=lift(z,2*Q*R,b,d)
    M=2*Q*R*d
    s=z+M*(((L+k+G-1)//G-z+M-1)//M+i)
    cert(s,2*R,[(2,3),(R,2)])
    assert s>t and s%4==3
    check(G*s-k,w)

    f=4*((isqrt((L+k)//w)+4)//4+j)
    h,rem=divmod(((k+1+Q)*pow(w,-1,2*Q)-f*f-1)%(2*Q),8)
    assert rem==0
    x=h%2
    for b in range(2,377): x+=(h-2*x*x-x)%(1<<b)
    x=1+4*x
    a=-S*pow(45,-1,49) if w==1 else 1
    z=next(v for v in range(d) if (v*v+f*f-a)%d==0)
    x=lift(x,Q,z,d)
    check(w*(x*x+f*f)-k,w)
```
