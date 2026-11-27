# First rough-composite band removes most of the signed rough asymmetry

**The signed comparison extends from \(z\) to a row-dependent cutoff \(Y_d\), with the large switched prime \(s\) retained exactly.** In the range \(z<P^-(p)\le Y_d\), rough composites account for more than 99% of the previously computed positive secondary term. That percentage concerns the signed sieve term. The sign of the true prime-pair difference remains open.

### The comparison

Keep the original label \(\ell=(a,b,c,e)\), with \(A=3^a,\ B=5^b,\ S_0=A+25B,\ S=3^c+5^e\), and \(\kappa=(S_0-S)/45\). Use the original balance strip, label ranges, and seven deep phases. In the restricted central family from the preceding comparison, \(d=qrth\), \((d,\kappa)=1\), and
\[
\begin{gathered}
q\in(B^\rho,B^{2\rho}],\quad r\in(B^{2\rho},B^{3\rho}],\quad
t\in(B^{1/2-\delta},B^{1/2-25\delta/26}],\\
h=P h_0,\quad B^{14\delta/13}<P\le B^{3\delta/2},\quad h_0\le B^{\delta/32},
\qquad 13\rho\le\delta\le5/32.
\end{gathered}
\]
Here \(q,r,t\) are inert primes, \(P\) is split prime, and \(h\) is split-supported in the original central \(\Omega(h)\) band. The switched forms are \(p=wds-\kappa\), \(w=1,49\), with \(s\equiv3\pmod4\) prime. Their windows are exactly \(s\in(X_-/(wd),X_+/(wd)]\), where
\[
X_-=(1457A-123B-S)/45,\qquad X_+=(729A+625B-S)/45.
\]
Keep the lifts \(p+\kappa\equiv u\pmod{343}\) for \(w=1\), with \(45u\equiv-S\pmod{49}\), and \(p+\kappa\equiv49j\pmod{343}\) for \(w=49\), with \(1\le j\le6\). Each lift is normalized by \(1/588\). The full classes have densities \(1/84\) and \(1/98\).

Put \(N=B/d\), \(L=\log\log B\), and use
\[
z=B^{\log L/(1000L)},\qquad Y_d=N^{\log L/(3L)}.
\]
Write \(\Delta^+\) for normalized depth two minus depth zero. For a prime \(\lambda\in(z,Y_d]\), let \(C_{d,w}(\lambda)\) count the rows with \(P^-(p)=\lambda\). These \(p\) are composite because \(p\asymp B\). Define
\[
V_d(y)=\prod_{\substack{j\le y,\ j\ {\rm prime}\\j\nmid14d\kappa}}
             \left(1-\frac1{j-1}\right),\quad
g_d(\lambda)=\frac{V_d(\lambda^-)}{\lambda-1}\quad(\lambda\nmid14d\kappa),
\]
with \(g_d(\lambda)=0\) at excluded primes, and set
\[
J_d=\frac{\log49}{d}\int_{X_-}^{X_+}
           \frac{dx}{\log(x/d)\log(x/(49d))},\qquad D_d(y)=J_dV_d(y).
\]
The following estimate holds uniformly per row and per chosen pair of lifts:
\[
\sum_{z<\lambda\le Y_d}
 \left|\Delta^+C_d(\lambda)-J_d g_d(\lambda)\right|
 \ll (\log B)^{-1/10}D_d(z).
\]
In particular, the signed estimate applies to any subset of the least primes in this range with an error bounded by the same right-hand side.

**Proof.** Force \(\lambda\mid p\), then sieve the primes strictly below \(\lambda\). For each eligible prime \(j\), divisibility of \(p\) imposes one reduced residue on the prime \(s\), with density \(1/(j-1)\). The progression modulus for \(s\) is \(1372\lambda e\) or \(28\lambda e\), where \(e\) is the additional sieve divisor. This uses the actual coefficient \(d\) in the residue and retains the exact lifts. [Bombieri, *On the large sieve*](https://doi.org/10.1112/S0025579300005313)

To obtain precision below the signed secondary term, partition the sieve primes into blocks with successive upper ends \(\lambda,\lambda^{1/10},\lambda^{1/100},\ldots\). Each block has bounded sum of local densities and a local product bounded below. Use the even and odd Bonferroni truncations at degrees \(k\) and \(k+1\), with \(k\) even and \(k\sim6L/(5\log L)\). Multiplying the upper truncations gives a majorant. Subtracting the sum of the single-block upper-minus-lower differences times the other upper truncations gives a minorant. Their relative main-term gap is
\[
O\!\left(L\,\frac{C^{k+1}}{(k+1)!}\right)
=O((\log B)^{-11/10}).
\]
The forced prime and all sieve divisors together use level at most
\[
Y_d^{\,1+(k+1)/(1-1/10)}=N^{4/9+o(1)}.
\]
Thus Bombieri–Vinogradov absorbs the progression errors, even summed absolutely over \(\lambda\). A modulus has \(O(\log B)\) choices for its marked prime, and each sieve coefficient is \(O(L)\). Subtraction of the two normalized logarithmic integrals gives \(J_d\). The sieve gap above costs \(O((\log B)^{-1/10})\) relative to that signed term.

The least-prime weights telescope exactly:
\[
\sum_{z<\lambda\le Y_d}g_d(\lambda)=V_d(z)-V_d(Y_d).
\]
Since \(B^{0.35}\le N\le B^{0.5}\), Mertens’ theorem gives, uniformly (the excluded primes above \(z\) dividing \(d\kappa\) have reciprocal sum \(O(\log B/(z\log z))\)),
\[
\Delta^+ C_d(z<P^-(p)\le Y_d)
 =\left(1-\frac{3\log B}{1000\log N}+o(1)\right)D_d(z).
\]
The fraction subtracted from the old positive term is at least \(1-3/350+o(1)\). For the true prime-pair comparison the remaining equation is
\[
\Delta^+\mathrm{PrimePair}_d
 =D_d(Y_d)-\Delta^+C_d(P^-(p)>Y_d)+o(D_d(Y_d)).
\]
These estimates can be summed over the original rows and labels. They give a smaller sufficient threshold for the remaining signed composite count, without determining that count.

At a fixed-power least prime \(\lambda\asymp B^\theta\), the same direct progression argument has a precise limit. Writing \(N=B^\nu\), the forced \(\lambda\) leaves sieve parameter at most \(\nu/(2\theta)-1+o(1)\). For \(\theta\ge\nu/6\) the linear lower-sieve main term vanishes. Below that threshold, at any fixed positive \(\theta\), the separate linear sieve envelopes still have a fixed positive gap, larger than the \(1/\log B\) relative signed signal. This identifies the limitation of the separate-envelope argument. [Iwaniec, *Rosser’s sieve*](https://eudml.org/doc/205669) · [Nath and Xie, §5](https://arxiv.org/html/2501.16723v1#S5)

### Exact same-lift replay

At \((a,b,c,e)=(712,486,80,122)\) the replay verifies, in each lift, a true alternate, a prime anchor with four exact odd inert valuations, and a composite \(p\) with certified prime \(s\) and **exact least prime \(65537\)**. The switched controls use the same \(d\) within each class. They fit the geometric bands at \(\rho=1/375,\delta=5/32\). For the composites, \(z<65537<Y_d\) follows from \(6<L<7\), \(N>2^{440}\), and the cutoff definitions.

```python
from math import factorial, gcd, isqrt

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
F=65537
assert all(all(n%d for d in range(2,isqrt(n)+1)) for n in (59,67,127,257,F))
R0=(1<<127)-1
v=4
for _ in range(125): v=(v*v-2)%R0
assert v==0                         # Lucas–Lehmer
m=514*R0
t=m*((1<<394)//m+114)+1
cert(t,m,(2,3),(257,2),(R0,2))
assert t%4==3 and B**11<t**32 and t**832<=B**291 and 25**1024<=B**5
R=(1<<157)+(307<<90)+1
cert(R,1<<90,(2,11))
J,Q=1<<89,1<<222
panel=factorial(F-1)

def check(p,w,res):
    assert L<=p<=U and p%4==1 and (p+k)%343==res
    assert (S0+45*p)%49==(0 if w==1 else r0)
    assert (p+k)%7!=0 if w==1 else res==49

for w,j,wp,i,ws,res,j0,ic,wc in [
    (1,46,3,93654,13,264,66,73,19), (49,52,5,36203,3,49,88,993,2)
]:
    C=w*59*67*t*25
    u=crt(1+J,2*J,(k+1)*pow(C,-1,R),R)
    P=first(u,2*J*R,1<<259)+j*2*J*R
    cert(P,J,(2,wp))
    assert P%4==1 and B**35<P**208 and P**64<=B**15
    G=C*P
    assert B>(G//w)<<440 and gcd(G,k)==1
    d,b=(343,res*pow(G,-1,343)) if w==1 else (7,pow(G//w,-1,7))
    for composite,d0,b0,offset,base in [
        (False,49 if w==1 else 7,-S*pow(45*G,-1,49) if w==1 else b,i,ws),
        (True,d,b,ic,wc)
    ]:
        M,u=(4,3) if composite else (2*Q,(k+1+Q)*pow(G,-1,2*Q)%(2*Q))
        u=crt(u,M,1,R); M*=R
        u=crt(u,M,b0,d0); M*=d0
        if composite:
            u=crt(u,M,k*pow(G,-1,F),F); M*=F
        s=first(u,M,(L+k+G-1)//G)+offset*M
        cert(s,2*R,(2,base),(R,2))
        assert s>t and s%4==3
        p=G*s-k
        check(p,w,res)
        if composite:
            assert p>F and p%F==0 and p%F**2!=0 and gcd(p,panel)==1
        else:
            cert(p,Q*R,(2,5),(R,2))  # odd valuations at 59, 67, t, s

    Q0=1<<378
    f=4*((isqrt((L+k)//w)+4)//4+j0)
    h,rem=divmod(((k+1+Q0)*pow(w,-1,2*Q0)-f*f-1)%(2*Q0),8)
    assert rem==0
    x=h%2
    for e in range(2,377): x+=(h-2*x*x-x)%(1<<e)
    x=1+4*x
    d0,a0=(343,264) if w==1 else (7,1)
    u=next(u for u in range(d0) if (u*u+f*f-a0)%d0==0)
    x=crt(x,Q0,u,d0)
    p=w*(x*x+f*f)-k
    cert(p,Q0,(2,5))
    check(p,w,res)                  # true alternate
```

The order tests in `cert` force every prime divisor to be \(1\bmod m\). Two such factors of a composite below \(m^3\) would give a square discriminant from the base-\(m\) digits of \((n-1)/m\), which the replay excludes.
