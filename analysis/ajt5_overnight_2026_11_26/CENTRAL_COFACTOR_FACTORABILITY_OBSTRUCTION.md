# Central split cofactors with no usable balanced divisor split

**A central value of \(\Omega(h)\) does not make the split cofactor \(h\) well-factorable.** In the upper residual, a positive share of the corrected harmonic weight has no balanced divisor split. This holds even after restricting every prime factor of \(h\) to be below the square-root cutoff. There are also certified actual central-cofactor failures in both 7-adic classes, each paired with a true alternate at the same lift modulo \(343\). The harmonic obstruction does not determine the normalized prime-pair sign.

### The subrange that can be removed

Keep \(A=3^a,\ B=5^b\), with \(a,b\) even and \(39/40<B/A<122/125\). Write \(S_0=A+25B,\ S=3^c+5^e,\ \kappa=(S_0-S)/45\). Use the original label bounds \(a/10\le c\le a/3,\ b/5\le e\le b/3\), the congruences \(c\equiv a\pmod4,\ e\equiv b+2\pmod6\), and all seven deep phases \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). The prime anchor \(n=S_0+45p\), \(p\equiv1\pmod4\), stays in
\[
1457A-123B<n\le729A+625B.
\]
The \(w=1\) class has \(n\equiv0\pmod{49}\). The \(w=49\) class has \(v_7(p+\kappa)=2\). Normalize by \(\alpha_1=1/84\) and \(\alpha_{49}=1/98\), respectively.

Take \((\log B)^{-1/2}\le\rho<1/250\) and \(B^{1/2-13\rho}<t\le B^{1/2-12\rho}\). In this range the exact switched factorization is
\[
(p+\kappa)/w=qr\,t\,s\,h,\qquad t\le s,\qquad h\le H=32B^{26\rho},
\]
with \(q,r\) in the original marked bands, \(t,s\) inert, and \(h\) split-supported. Put \(F(m)=\prod_{j>2,\ j\mid m}(j-1)/(j-2)\), with the product over primes, and let \(F_S(\kappa)\) use just split primes. The cofactor weight in the two-form upper sieve is
\[
\mathcal W(X)=F_S(\kappa)
  \sum_{\substack{h\le X,\ (h,\kappa)=1\\h\ {\rm split\text{-}supported}}}\frac{F(h)}h.
\]

For any fixed \(0<\beta<1\), the slice \(h\le \exp((\rho\log B)^\beta)\) contributes
\[
O\!\left(\rho^{3/2}M_\ell(\rho\log B)^{-(1-\beta)/2}\right)
+O(B^{1/2+13\rho})
\]
to the absolute normalized difference, where \(M_\ell=B(\log B)^{-3/2}\prod_{j\mid\kappa,\ j\equiv3(4)}(j-1)/(j-2)\), over prime \(j\). This is \(o(\rho^{3/2}M_\ell)\) uniformly. To see it, \(\mathcal W(X)\ll\sqrt{\log X}\) at this cutoff. The cancellation at split primes dividing \(\kappa\) follows from \(1+F(j)/(j-1)=F(j)\), and primes dividing \(\kappa\) above \(X\) have negligible reciprocal sum. The upper sieve in \(s\) for \(s,\ wqrhts-\kappa\) costs \(B/(\log B)^2\) times the harmonic weights and the inert singular factors. The marked \(q,r\) sums are bounded, the \(t\)-sum is \(O(\rho)\), and the square exception \(t=s\) gives the last error. The counts retain their exact lifts and endpoints. [Nath and Xie, Lemma 3.6](https://arxiv.org/html/2501.16723v1#S3).

### Central cofactors that defeat the factorization

Fix any \(\epsilon>0\), and require \(\left|\Omega(h)-\tfrac12\log\log H\right|\le\epsilon\log\log H\), counting prime factors with multiplicity. A well-factorable coefficient of level \(H\) can be nonzero at \(h\) only if \(h=h_1h_2\) with both \(h_i\le\sqrt H\). This follows by testing the definition at the equal split. There are two disjoint central families violating this condition. In both, \(h_0\le B^{\rho/10}\) is split-supported and coprime to \(\kappa\).

| Cofactor | Obstruction |
|---|---|
| \(h=P h_0\), \(B^{14\rho}<P\le B^{15\rho}\), \(P\) split prime | \(P>\sqrt H\). |
| \(h=P_1P_2P_3h_0\), with split primes in exponent bands \((6.55,6.57],(6.57,6.59],(6.59,6.60]\) in units of \(\rho\log B\) | Every prime factor is below \(\sqrt H\), but any two of \(P_1,P_2,P_3\) exceed \(\sqrt H\) when multiplied. |

Both families fit the ordinary window on the half-band \(B^{1/2-13\rho}<t\le B^{1/2-25\rho/2}\). In fact \(h\le B^{19.86\rho}\) and \(qr\le B^{5\rho}\), so the entire corresponding \(s\)-interval is above \(t\) for large \(B\). That interval has growing length and contains integers in the required \(s\equiv3\pmod4\) and 7-adic lifts. This size and congruence check does not assert primality. [Maynard, *Primes in arithmetic progressions to large moduli II*, Definitions 1–2](https://arxiv.org/pdf/2006.07088).

Each family carries \(\asymp\sqrt{\rho\log B}\) corrected harmonic weight, the order of \(\mathcal W(H)\). For a short proof, form the Euler product for \(h_0\) over split primes \(j\le Y=B^{\rho/100}\) omitting \(\kappa\), with local weights \(1,F(j)/j,F(j)/j^2,\ldots\). After normalization, the probability of exponent \(e\ge1\) is \(j^{-e}\). Hence
\[
\mathbb E\log h_0\le(\tfrac12+o(1))\log Y,\qquad
\mathbb E\Omega(h_0)=\tfrac12\log\log H+O(\log\log\log B),\qquad
\operatorname{Var}\Omega(h_0)=O(\log\log H).
\]
Markov and Chebyshev leave a positive fraction satisfying the size and central restrictions, also after adding one or three primes to \(\Omega\). The split singular correction makes the product \(\asymp\sqrt{\log Y}\). Each macroscopic prime band then contributes a positive constant harmonic factor, unchanged to first order by omitting primes dividing \(\kappa\). Thus discarding the obstructed families leaves an error allowance of order \(\rho^{3/2}M_\ell\) in the available upper-sieve estimate, even on this half-band. This is a positive share of the **harmonic bound**, with no lower bound asserted for the actual prime-pair share.

Even making the cofactor weight itself triply well-factorable does not fix the marked modulus. On central \(h\le B^{6\rho}<H^{1/3}\), any \(1\)-bounded cofactor weight is trivially triply well-factorable at level \(H\), by putting it on the largest component. Yet \(s\gg B^{1/2+\rho}\), so the full modulus containing \(s\) fails even the equal **two-way** split at level \(CB\) for any fixed \(C\). Throughout the upper residual, \(t>B^{1/3+\eta}\) for a fixed \(\eta>0\), so a modulus containing \(t\) fails the equal **three-way** split at that level. These are support obstructions to applying the theorem directly to the marked modulus. A signed switched estimate that keeps the prime \(s\) in the summand remains open.

### Same-lift certified controls

The replay uses \((a,b,c,e)=(712,486,80,122)\), \(\rho=1/375\), and the broader upper band with \(\delta=5/32\), so \(H=32B^{5/16}\). This is an exact finite control, with no asymptotic error claim at the fixture's height. Each failure has \(h=25P\) with \(\Omega(h)=3\) in the central band of relative width \(1/10\), and \(P>\sqrt H\). The true and failed controls use \((p+\kappa)\bmod343=264\) in the \(w=1\) class and \(49\) in the \(w=49\) class. The two targets in a pair share a label and lift.

`cert` forces every prime divisor to be \(1\bmod m\) by order tests. A composite below \(m^3\) would either be too small for two such divisors or give a square discriminant from the two base-\(m\) digits of \((n-1)/m\).

```python
from math import gcd, isqrt, log

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

def crt(x,m,b,d): return x+m*((b-x)*pow(m,-1,d)%d)
def first(x,m,L): return x+m*((L-x+m-1)//m)

A,B=3**712,5**486
S0,S=A+25*B,3**80+5**122
k,rem=divmod(S0-S,45)
L,U=(1457*A-123*B-S0)//45+1,(729*A+625*B-S0)//45
r0=(pow(3,716,49)+pow(5,488,49)+7)%49
assert rem==k%8==0 and S%49==r0==27 and 39*A<40*B and 125*B<122*A
assert B<59**375<B**2<67**375<B**3
assert all(all(n%d for d in range(2,isqrt(n)+1)) for n in (59,67,127,257))
R0=(1<<127)-1
v=4
for _ in range(125): v=(v*v-2)%R0
assert v==0                         # Lucas–Lehmer
m=2*257*R0
t=m*((1<<394)//m+114)+1
cert(t,m,[(2,3),(257,2),(R0,2)])
assert t%4==3 and B**11<t**32 and t**250<B**117
R=(1<<157)+(307<<90)+1
cert(R,1<<90,[(2,11)])
J,Q=1<<89,1<<222
assert 5<log(log(32)+5*log(B)/16)<6

def check(p,w,res):
    assert L<=p<=U and p%4==1 and (p+k)%343==res
    assert (S0+45*p)%49==(0 if w==1 else r0)
    assert (p+k)%7!=0 if w==1 else res==49

for w,j,wp,i,ws,res,j0 in [(1,46,3,93654,13,264,66),
                           (49,52,5,36203,3,49,88)]:
    C=w*59*67*t*25
    z=crt(1+J,2*J,(k+1)*pow(C,-1,R),R)
    P=first(z,2*J*R,1<<259)+j*2*J*R
    cert(P,J,[(2,wp)])
    assert P%4==1 and P**32>32**16*B**5>(25*P)**16
    G=C*P
    d=49 if w==1 else 7
    b=-S*pow(45*G,-1,49) if w==1 else pow(G//w,-1,7)
    z=crt((k+1+Q)*pow(G,-1,2*Q)%(2*Q),2*Q,1,R)
    z=crt(z,2*Q*R,b,d)
    M=2*Q*R*d
    s=first(z,M,(L+k+G-1)//G)+i*M
    cert(s,2*R,[(2,ws),(R,2)])
    assert s>t and s%4==3
    p=G*s-k
    cert(p,Q*R,[(2,5),(R,2)])
    check(p,w,res)                  # exact odd valuations at 59, 67, t, s

    Q0=1<<378
    f=4*((isqrt((L+k)//w)+4)//4+j0)
    h,rem=divmod(((k+1+Q0)*pow(w,-1,2*Q0)-f*f-1)%(2*Q0),8)
    assert rem==0
    x=h%2
    for b in range(2,377): x+=(h-2*x*x-x)%(1<<b)
    x=1+4*x
    d,a0=(343,264) if w==1 else (7,1)
    z=next(z for z in range(d) if (z*z+f*f-a0)%d==0)
    x=crt(x,Q0,z,d)
    p=w*(x*x+f*f)-k
    cert(p,Q0,[(2,5)])
    check(p,w,res)                  # true alternate by the displayed norm
```
