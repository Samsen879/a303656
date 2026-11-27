# A long-variable dyadic band below the secondary scale

In the deep switched row let \(p=49ds-\kappa\), \(N=B/d\), and \(s\equiv3\bmod4\) prime. The parent condition is \(ds\equiv u_0\bmod7\). Inside it the [complementary-lift correction](https://github.com/Samsen879/a303656/commit/1968edf214343aad579cd264eb2bad464031ae53) has bounded weight proportional to \(1-7\,1_{ds=u_0\bmod49}\).

Let \(E_d(T)\) denote this weighted count for composite \(p\) whose least prime \(\lambda\) lies in \((T,2T]\). For fixed \(\eta,\epsilon>0\), with \(T\ge B^\eta\) and \(2T\le NB^{-\epsilon}\),
\[
|E_d(T)|\ll_{\eta,\epsilon} \frac{N F(d\kappa)}{\log^3 B},
\qquad
F(m)=\prod_{\ell\mid m,\ \ell>2}\frac{\ell-1}{\ell-2}.
\]
The product is over prime divisors. A contributing \(\lambda\) is coprime to \(14d\), because the target residue has \(p\) odd and a unit at 7, and the row has \((d,\kappa)=1\). For fixed \(\lambda\) write
\[
s=\sigma+28\lambda j,\quad
v=p/\lambda=(49d\sigma-\kappa)/\lambda+28\cdot49d\,j.
\]
The interval for \(j\) has length \(X\asymp N/\lambda\). Prime \(s\) and \(P^-(v)\ge\lambda\) force both forms to avoid prime divisors through \(z=\min(T^{1/2},X^{1/100})\). The prime \(s\) itself is above \(z\), since the original sharp window gives \(s\asymp N\). Outside \(2,7\), the two forms have distinct roots except at divisors of \(d\kappa\lambda\); counting at most one excluded local root for those exceptions costs at most \(F(d\kappa)\) since \(\lambda>z\). For squarefree moduli the CRT combines the root counts; the counting remainder is at most the product of these counts. The dimension-two upper beta sieve (e.g. [Nath and Xie, Lemma 3.6](https://arxiv.org/html/2501.16723v1#S3.SS2)), with level \(X^{1/4}\), bounds the sifted count by \(O(XF(d\kappa)/\log^2 B)\). Indeed \(\log z\asymp_{\eta,\epsilon}\log B\) and the remainders up to the level, each \(O(2^{\omega(m)})\), sum to \(O(X^{1/4}\log X)\). The dyadic prime sum \(\sum_{T<\lambda\le2T}1/\lambda\ll1/\log B\) completes the proof. The bound is absolute, with no assumption of cancellation between rows.

At the [paired-window rough secondary scale](https://github.com/Samsen879/a303656/commit/f8df60ea0dffcb1da32f1c17997e9a89b8a52dcf) \(D_d(Y_d)\asymp NF(d\kappa)/(\log^2 B\log Y_d)\), with \(Y_d=N^{\log L/(3L)}\) and \(L=\log\log B\), this is a relative \(O(\log L/L)\) bound for one common dyadic band, uniformly when \(B^{1/20}\le T\le B^{17/50}\) and \(N\ge B^{0.35}\). The same relative bound holds after summing over rows. It does not bound the full range of least primes or settle its signed sum, and it loses the long-variable input when \(\lambda\) approaches \(N\).

The following exact replay gives weights \(-6,+1\) before the common normalization in the same switched row, sharp window, parent lift and dyadic band, with prime \(s\) and the same certified least prime of composite \(p\).

~~~python
from math import gcd, isqrt

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
r=(pow(3,716,49)+pow(5,488,49)+7)%49
u0=-r*pow(45,-1,49)%49
assert rem==0 and S%49==r==27 and u0==19
assert 39*A<40*B and 125*B<122*A and B<59**375<B**2<67**375<B**3
assert 16**2048>=B**5 and 32**1024<=B**5
assert all(all(n%i for i in range(2,isqrt(n)+1)) for n in (59,67,127,257))

R0=(1<<127)-1
v=4
for _ in range(125): v=(v*v-2)%R0
assert v==0                         # Lucas–Lehmer
m=514*R0
t=m*((1<<394)//m+114)+1
cert(t,m,(2,3),(257,2),(R0,2))
assert t%4==3 and B**11<t**32 and t**832<=B**291
R=(1<<157)+(307<<90)+1
cert(R,1<<90,(2,11))
J,Q,T=1<<89,1<<202,1<<60
F=T+13*(1<<21)+1
cert(F,1<<21,(2,5))
assert T<F<=2*T and B<T**20 and T**50<B**17

C=49*59*67*t*25
z=crt(1+J,2*J,(k+F)*pow(C,-1,R),R)
P=first(z,2*J*R,1<<259)+173*2*J*R
cert(P,J,(2,7))
assert P%4==1 and B**35<P**208 and P**64<=B**15
G=C*P
d=G//49
assert gcd(d,k)==1 and (d<<440)<B<(d<<465) and B<2**1200

for x,i,a in [(19,38948,11),(26,2894,13)]:
    z=crt((k+F*(1+Q))*pow(G,-1,2*Q)%(2*Q),2*Q,1,R)
    z=crt(z,2*Q*R,x*pow(d,-1,49),49)
    M=2*Q*R*49
    z=crt(z,M,k*pow(G,-1,F),F); M*=F
    s=first(z,M,(L+k+G-1)//G)+i*M
    p=G*s-k
    v,rem=divmod(p,F)
    cert(s,2*R,(2,3),(R,2))
    cert(v,Q*R,(2,a),(R,2))
    assert rem==0 and v>F and L<=p<=U and s>t and s%4==3 and p%4==1
    assert (p+k)%2401==49*x and (p+k)%343==245 and (S0+45*p)%49==r
    print(x, F, 1-7*(x==u0))
~~~
