# Two exponentially rich primitive chord families at one actual target

I obtained **two growing rotating-divisor families at the same integer target**. They share the original first anchor \(n-27A-5B\) and have different destination norms, \(n-9A-5B\) and \(n-A/9-5B\). For every sufficiently large \(L\), one target in the ordinary-height window has \(\exp(c\sqrt K)\) distinct primitive critical seeds in **each** family, for some absolute \(c>0\) and \(K=90L\). The numerical seed ranges can be made disjoint.

For the original two pairs of shifts, I also proved an obstruction. No two diagonal starting chords, including arbitrary integer multiples of the unit diagonal, can share an ordinary-height target. This rules out combining their diagonal parametrizations before applying the rational rotations.

### Two families at one target

Put \(A=9^L\), \(B=25^L\), \(a=3^{L-1}\), and \(H=27A+5B\). The identity
\[
243=81+2\cdot9^2=1+2\cdot11^2
\]
gives a common anchor and two destination norms. With \(P=(t,-t)\), \(S=2t^2\), \(n=H+S\), and \((c_1,c_2)=(9a,11a)\), take \(Q_i=P+c_i(1+i)\). Then
\[
N(Q_1)=n-9A-5B,\qquad N(Q_2)=n-A/9-5B.
\]
The exponent pairs are \((2L+3,2L+1)\) at the anchor and \((2L+2,2L+1)\), \((2L-2,2L+1)\) at the destinations. Both exponents grow with \(L\). The two destination changes are on the 3-axis.

Use bases \(X_1=2\) and \(X_2=4\). At base \(X\), set
\[
\pi_j=X^{2j+1}+(-1)^ji,\qquad
k_j=\mathbf1_{j=0}+6b_j,\qquad 0\le b_j\le X^2.
\]
Force \(G_X=\prod_{j=0}^J\bar\pi_j^{\,12X^2+2\mathbf1_{j=0}}\) into the corresponding \(Q_i\). A rotation uses \(Z=\prod_j\bar\pi_j^{2k_j}\) and replaces \(Q_i\) by \((Q_i/Z)\bar Z\).

Each \(G_X\) is primitive. A Gaussian prime common to \(\pi_j\) and \(\bar\pi_k\) would give opposite values for \(X^{(2j+1)(2k+1)}\) in odd characteristic. Also, a rational prime common to the **two** product norms would give \(2^{2e}=-1\) and \(2^{4f}=-1\) modulo that prime for odd \(e,f\). Raising the first equality to \(2f\) and the second to \(e\) is a contradiction. Thus the two norm moduli are coprime. For \(G_X=u+iv\), the condition \(G_X\mid Q_i\) is the single class
\[
t\equiv-c_iv\,u^{-1}\pmod{N(G_X)}.
\]
The two classes combine with \(t\equiv1\pmod{66}\). Their total period is \(66N(G_2)N(G_4)\), with base-2 logarithm less than
\[
876(J+1)^2+244(J+1)+7.
\]

All rotations in each family preserve coordinates modulo 66 relative to the endpoint obtained by the single switch \(k_0=1\). At the inert primes 3 and 11, a Gaussian unit of norm one has order dividing 4 and 12, respectively. The variable switches are twelfth powers. The fixed switch is nonidentity at both primes since \(\pi_0^2-\bar\pi_0^2=4Xi\). Since \(t\equiv1\pmod{66}\), this makes every resulting chord primitive. Indeed, an odd common divisor of its coordinates has a prime factor dividing \(D_i=c_i^2\). The only possibilities are 3 and 11, and at those primes \(Q_i\equiv P\ne0\) before switching whenever \(p\mid D_i\). It also follows that \(\gcd(S,D_i)=\gcd(q,D_i)=1\), where \(q=N(Q_i'-P)/2\).

The variable angle steps have magnitudes \(24\arctan(X^{-(2j+1)})\) and alternating signs. Reversing digits on the negative axes gives a translate of a positive digit box. Consecutive step sizes have ratio at most \(X^2\), so greedy subtraction gives a full-turn mesh with largest gap at most \(24X^{-(2J+1)}\).

For \(W=2^{K/2}\), take \(3W/4\le t<7W/8\). This gives \(2^K\le S<2^{K+1}\) and \(B^{16}\le n\le A^{32}\). The CRT period fits inside this interval for \(J\) a sufficiently small constant times \(\sqrt K\). At rotation angle \(\phi\), the **exact** physical ratio is
\[
\frac{q_i}{S}=1-\cos\phi+\frac{c_i^2}{S}+\frac{c_i}{t}\sin\phi.
\]
Write \(r_-=1/[64K(K+1)]\) and \(\Delta=1/[64K^2(K+1)]\). The last two terms have magnitude below \(\Delta/16\) for sufficiently large \(L\), uniformly over the height interval. Choose \(1-\cos\phi-r_-\) in \((\Delta/4,3\Delta/8)\) for the first family and \((5\Delta/8,3\Delta/4)\) for the second. Both angle intervals have length \(\gg K^{-2}\), both give the original strict critical band, and their numerical \(q\) ranges are disjoint. Packing intervals of twice the mesh size gives \(\exp(c\sqrt K)\) distinct angles in each. The exact ratio is strictly increasing on these positive angle intervals, so these count distinct seeds at the **same** \(t\) and \(n\). Every \(t\) in the combined CRT class inside the height window works. The labels share the 5-power, so the two destination changes vary only the 3-exponent even though both exponent values grow across layers.

### Obstruction for the original two diagonal parametrizations

Write the original shifts as \((H,D)=(27A+5B,9A+2B)\) and \((J_0,E)=(3A+125B,A+50B)\). A diagonal chord \((d,d)\) in the first pair forces \(d\mid D\) and the target form \(H+2(t^2+h^2)\), where \(h=(D/d-d)/2\). The second pair similarly has target \(J_0+2(u^2+j^2)\) with \(j=(E/e-e)/2\).

At a common target \(n\ge B^{16}\), one has \(|t|,|u|\ge B^8/2\) and \(|t^2-u^2|<1000B^2\). The spacing of integer squares forces \(t^2=u^2\), so \(h^2-j^2=60B-12A\). Modulo 5, a diagonal offset square lies in \(\{0,4\}\) when its chord product is \(1\), and in \(\{0,1\}\) when that product is \(-1\). Here \(D\equiv-A\) and \(E\equiv A\). If \(A\equiv1\), the possible differences are \(\{0,1,2\}\) and the required value is 3. If \(A\equiv-1\), the possible differences are \(\{0,3,4\}\) and the required value is 2. Both cases fail. This applies before any norm-preserving rotations. The original pair with a non-diagonal starting parametrization remains open in this argument.

### Inline replay

The finite replay forces only the exponents used by its two displayed rotations. It checks the same target, both disjoint seed intervals, the congruences, and the unrotated failures. The last two assertions check the mod-5 table.

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
def divide(z,w):
    a,b=mul(z,bar(w))
    d=N(w)
    assert a%d==b%d==0
    return a//d,b//d

L=1456
K=90*L
W=2**(K//2)
a=3**(L-1)
A,B=9*a*a,25**L
digits=((1,18,12,24,12,18,18,12,12,6,12,6,0,12,0,6,12,6,12,18,0,6,18,12),
        (1,18,42,78,0,30,72,6,84,30,0,6,24))
t,M=1,66
factors=[]
for X,c,ks in zip((2,4),(9*a,11*a),digits):
    assert ks[0]%6==1 and all(k%6==0 for k in ks[1:])
    Z=(1,0)
    for j,k in enumerate(ks):
        assert 0<=k-(j==0)<=6*X*X
        Z=mul(Z,power((X**(2*j+1),-(-1)**j),2*k))
    u,v=Z
    d=N(Z)
    assert gcd(u,v)==gcd(M,d)==1
    root=-c*v*pow(u,-1,d)%d
    t+=M*((root-t)*pow(M,-1,d)%d)
    M*=d
    factors.append((c,Z,power((X,-1),2)))
lo=3*W//4
assert M<=W//8
t=lo+(t-lo)%M
assert t<7*W//8 and t%66==1

P=(t,-t)
S=N(P)
n=S+27*A+5*B
assert B**16<=n<=A**32 and 2**K<=S<2**(K+1)
qs=[]
for (c,Z,Z0),offset,(left,right) in zip(factors,(9*A,A//9),((3,7),(9,13))):
    Q=(t+c,c-t)
    Q0=mul(divide(Q,Z0),bar(Z0))
    R=mul(divide(Q,Z),bar(Z))
    assert all((x-y)%66==0 for x,y in zip(R,Q0))
    assert N(R)==n-offset-5*B==S+2*c*c
    x,y=R[0]-P[0],R[1]-P[1]
    assert x%2==y%2==1 and gcd(x,y)==1
    q=(x*x+y*y)//2
    w=abs(x*P[1]-y*P[0])//2
    assert gcd(q,c*c)==gcd(S,c*c)==1 and 2*q*S==(c*c-q)**2+4*w*w
    assert left*S<16*(64*K*K*(K+1)*q-K*S)<right*S
    assert 64*K*(K+1)*c*c<S
    qs.append(q)
assert qs[0]<qs[1]

def c2(d):
    return {((d*pow(j,-1,5)-j)*3)**2%5 for j in range(1,5)}
for A5 in (1,4):
    assert 3*A5%5 not in {(x-y)%5 for x in c2(-A5) for y in c2(A5)}
print(K,M.bit_length(),*[q.bit_length() for q in qs])
```

Output: `131040 61652 131001 131001`. The construction supplies simultaneous families on a generated CRT progression. It leaves the prescribed-target problem open.