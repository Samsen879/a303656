# Exact complementary-lift identity and fixed-row pairing obstruction

After the [one-digit matching criterion](https://github.com/Samsen879/a303656/commit/0b7685221c9212f40c1cd282b4765bb67ac3ce22), ask what is needed to put the discarded deep classes back. All counts below keep the same target window and actual prime restrictions. Let \(V_x\) be the deep count on \(p+\kappa\equiv49x\bmod2401\), normalized at the refined scale, and \(D_j=\frac17\sum_{x\equiv j(7)}V_x\) the normalized parent count. Write \(S\) for the normalized shallow count, \(D=\frac16\sum_jD_j\), and \(j_0=u_0\bmod7\) for the matched parent. The exact identity is
\[
D-S=(V_{u_0}-S)
+\frac17\sum_{\substack{x\equiv j_0(7)\\x\ne u_0}}(V_x-V_{u_0})
+\frac16\sum_{j=1}^6(D_j-D_{j_0}).
\]
For an individual parent \(D_j\), the last term is \(D_j-D_{j_0}\). In the Fourier expansion on \(x=u_0(1+7i)\bmod49\), the middle functional equals minus the sum of the six nontrivial Fourier coefficients. All extend to primitive conductor-49 characters. Parent totals alone cannot reproduce this functional. This identifies the required coefficients, without estimating their value on actual prime counts.

For a fixed shallow/deep row pairing write \(p=d_Ss_S-\kappa_S=49d_Ds_D-\kappa_D\) when comparing equal \(p\). For eligible auxiliary \(e\), coprime to \(14d_Sd_D\kappa_S\kappa_D\), the residues forced by \(e\mid p\) agree (equivalently all their character factors agree) if and only if
\[
e\mid49d_D\kappa_S-d_S\kappa_D.
\]
The right-hand integer is a 7-adic unit for the actual legal rows. Thus some eligible prime separates every fixed pairing. The excluded product has polynomial height in \(B\), so Chebyshev's bound for the product of small primes even gives a separating prime \(O(\log B)\) for sufficiently large \(B\). This does not exclude signed averaging across many rows.

If the two labels have the same fixed anchor and the same \(S_{\rm label}\bmod49\), then \(\kappa_D-\kappa_S\equiv0\bmod49\). Matching the sharp target window endpoints by an increasing affine map forces \(s_D=(d_Ss_S+\kappa_D-\kappa_S)/(49d_D)\). This is also the unique map preserving actual \(n\). At every admissible shallow point its numerator is a 7-adic unit, so it never gives an integer \(s_D\).

The standalone replay gives actual prime pairs in both \(x=19\) and \(26\bmod49\) in the same deep row and parent lift. It also gives two matched-digit rough semiprimes in the sharp windows (one shallow and one deep), with prime switched variable and common exact least prime \(F\). Their forced residues differ both modulo \(F\) and modulo 3. These controls establish separation, not a sign.

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
assert rem==0 and S%49==r==27 and -r*pow(45,-1,49)%49==19
assert 39*A<40*B and 125*B<122*A and B<59**375<B**2<67**375<B**3
assert all(all(n%i for i in range(2,isqrt(n)+1)) for n in (59,67,127,257))
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
J=1<<89
F=(1<<60)+13*(1<<21)+1
cert(F,1<<21,(2,5))

out=[]
for w,l,i,a,q,x,d,j,b,c in [
    (1,1,46,3,222,19,49,93654,13,5),
    (49,1,52,5,222,1,7,36203,3,5),
    (49,1,52,5,222,19,49,30098,3,5),
    (49,1,52,5,222,26,49,8424,3,5),
    (1,F,54,3,202,264,343,49291,5,11),
    (49,F,173,7,202,19,49,38948,3,11)
]:
    C=w*59*67*t*25
    z=crt(1+J,2*J,(k+l)*pow(C,-1,R),R)
    P=first(z,2*J*R,1<<259)+i*2*J*R
    cert(P,J,(2,a))
    assert P%4==1 and B**35<P**208 and P**64<=B**15
    G,Q=C*P,1<<q
    z=crt((k+l*(1+Q))*pow(G,-1,2*Q)%(2*Q),2*Q,1,R)
    z=crt(z,2*Q*R,x*pow(G//w,-1,d),d)
    M=2*Q*R*d
    if l>1:
        z=crt(z,M,k*pow(G,-1,l),l); M*=l
    s=first(z,M,(L+k+G-1)//G)+j*M
    p=G*s-k
    v,rem=divmod(p,l)
    cert(s,2*R,(2,b),(R,2))
    cert(v,Q*R,(2,c),(R,2))
    assert rem==0 and v>l and L<=p<=U and s>t and s%4==3 and p%4==1
    assert (p+k)%(w*d)==w*x and (S0+45*p)%49==(0 if w==1 else r)
    if w==1: assert (p+k)%343==264
    if l==F:
        assert B<(G//w)<<465 and (G//w)*s%49==19  # Y_d < 2**52 < F
        out.append((G,s))

(G1,s1),(G2,s2)=out
assert (s1%F,s2%F)==(178844661957652585,493572851894234920)
assert pow(s1*pow(s2,-1,F)%F,(F-1)//8,F)==F-1
assert gcd(14*G1*G2*k,3)==1
assert (k*pow(G1,-1,3)%3,k*pow(G2,-1,3)%3)==(1,2)
~~~
