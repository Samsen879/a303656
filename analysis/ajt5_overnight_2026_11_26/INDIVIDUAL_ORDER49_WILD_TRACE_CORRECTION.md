# Individual order-49 wild corrections on native residues

This follows [the coupled-word order-49 control](https://github.com/Samsen879/a303656/commit/1651b89dcd2fcfb6aae23a08f39d5a78b96f23e7). The individual wild terms reveal a mismatch the locally trivial coupled word misses, but are still aggregate symbols on an unsplit composite. The fully split row is recertified rather than a new closure. Exact independent replay formed both relative norms, used integer multiplication determinants for both finite differences, and checked all four primewise symbol values.

In [Sen's trace formula as recorded by Vostokov](https://arxiv.org/pdf/math/0012139), take the uniformizer \(\pi=\zeta_{49}-1\), the root polynomial \(1+T\) and the second input given by \(A(1+T)\). For the first input \(u^6\), the valuation of \(u^6-1\) is 42 in uniformizer units, exceeding \(2\cdot42/(7-1)\). Divide the resulting symbol exponent by 6, which is invertible modulo 49. The arithmetic local reciprocity convention is inverse to the convention used for that trace exponent; confirm the sign at \(A=\zeta_{49}\) by the cyclotomic action of \(u^{-42}\). The tame normalization in the product formula must use that same arithmetic convention. No order-343 correction or primewise localization is claimed.

**The individual order-49 wild corrections expose the previously invisible \((66,129)\) prime.** Its corrected axis logs are \((6,30)\), while the native lift requires \((13,37)\). The coupled word \(3^2 5^5\) gives \(15\bmod49\) for both pairs. Both residual primes fail on the known split, recertifying the old closure.

### Exact wild correction

Put \(\zeta=\zeta_{49}\) and \(P(X)=1+X^a-X-X^b\). Compute \(A(\zeta)=N_{\mathbb Q(\zeta_{343})/\mathbb Q(\zeta)}P(\zeta_{343})\) by multiplying the seven \(P(X^{1+49j})\) modulo \(\Phi_{343}(X)\), then replacing \(X^7\) by \(\zeta\). Write
\[
T=\operatorname{Tr}\!\left(\frac{\zeta A'(\zeta)}{A(\zeta)}\right),
\qquad
D(h)=N\bigl(A((1+h)\zeta)\bigr).
\]
Then \(D'(0)=D(0)T\). For \(u=3,5\), the arithmetic-normalized wild log is \(-T\log_7(u^6)/(6\cdot49)\). Sen’s trace formula applies to \(u^6\), since \(v_{\zeta-1}(u^6-1)=42>14\). An independent Brückner–Vostokov residue calculation gives the same logs. The sign check on \(A=\zeta\) gives \((22,1)\) from \((u^{-42}-1)/49\bmod49\). [Vostokov, §§8.1.1–8.1.2](https://arxiv.org/pdf/math/0012139)

Here \(D(0)=7N_0\). Evaluating \(D(2401)-D(0)\bmod2401^2\) and dividing by 2401 gives \(D'(0)\bmod2401\). Both derivatives are multiples of 49, so \(T/7\bmod49\) is \((D'(0)/49)N_0^{-1}\bmod49\). The two values of \(\log_7(u^6)/(6\cdot7)\) are \(29,8\), obtained from \((q-7q^2/2)/6\bmod49\) with \(q=(u^6-1)/7\). The global product formula adds the wild logs to the logs of \(A^{(u^{42}-1)/49}\bmod u\). [Hilbert product formula and tame normalization](https://openmaths.org/courses/NT-CFT/power-residue-symbols-and-reciprocity-laws.html)

| Native source | \(D'(0)\bmod2401\) | \(T/7\bmod49\) | Finite-field logs | Wild logs | Corrected logs |
|---|---:|---:|---:|---:|---:|
| \((66,129)\) | 1176 | 24 | \((7,42)\) | \((39,4)\) | \((46,46)\) |
| \((15,131)\) | 735 | 15 | \((7,45)\) | \((6,27)\) | \((13,23)\) |

### Native control and closure scope

For \((66,129)\), the full norm is \(7N_0\) with \(N_0=157662833878877367213009917598207232174012765021751\). The order-343 root modulo \(N_0\) is \(38519862799307894148512565859690422138485697855661\). The residual modulus is \(237581583404462689945386635341\), its root is \(216785655954312809247291330593\), and its complete menu is \(\{(44,180)\}\).

The following direct check uses \(u^{(p-1)/49}\equiv y^{7j_u}\pmod p\) at each certified prime. It independently sums to \((46,46)\bmod49\).

| Prime \(p\) | Native root \(y\bmod p\) | \((j_3,j_5)\) | Status |
|---:|---:|---:|---|
| 3089059 | 1995083 | \((25,17)\) | Below the chart cutoff |
| 214827736571729 | 95184918813664 | \((23,33)\) | \(1\bmod1372\), fails the sign gate |
| 374998168847 | 174742218538 | \((41,15)\) | Requires \((25,41)\) |
| 633553982769970403 | 428593093328306329 | \((6,30)\) | Requires \((13,37)\) |

Subtracting the first two pairs gives residual logs \((47,45)\) versus the all-primes-passing requirement \((38,29)\). The coupled word still gives \(25\bmod49\) on both. The last two rows are the primewise evidence for complete rejection.

For the **unsplit** \((15,131)\) control, the norm is \(7M\), where \(M=26717908551918972727509122511988955591425904906909\), with root \(3088177783201613341856596606977577493764097037402\) and complete menu \(\{(24,145)\}\). The corrected logs \((13,23)\) disagree with \((41,16)\), even though both pairs reduce to \((6,2)\bmod7\). This detects at least one failing prime and leaves its support unidentified. No new native row closes.



```python
from math import gcd,isqrt,prod

def red(z,i,k,s):
    i%=7*s
    if i<6*s: z[i]+=k
    else:
        for j in range(6): z[i-6*s+j*s]-=k
def basis(s,i=0): return [int(j==i) for j in range(6*s)]
def mul(a,b,s):
    c=[0]*(6*s)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if x*y: red(c,i+j,x*y,s)
    return c
def powel(a,n,p,s):
    c=basis(s)
    while n:
        if n%2: c=[x%p for x in mul(c,a,s)]
        a=[x%p for x in mul(a,a,s)]; n//=2
    return c
def rel(a,b):
    z=basis(49)
    for j in range(7):
        v=[0]*294
        for i,k in ((0,1),(a,1),(1,-1),(b,-1)): red(v,i*(1+49*j),k,49)
        z=mul(z,v,49)
    assert all(t==0 for i,t in enumerate(z) if i%7)
    return z[::7]
def det(A):
    A=[r[:] for r in A]
    d,s=1,1
    for i in range(len(A)-1):
        if not A[i][i]:
            j=next(j for j in range(i+1,len(A)) if A[j][i])
            A[i],A[j]=A[j],A[i]; s=-s
        v=A[i][i]
        for j in range(i+1,len(A)):
            for k in range(i+1,len(A)):
                x=v*A[j][k]-A[j][i]*A[i][k]
                assert x%d==0
                A[j][k]=x//d
            A[j][i]=0
        d=v
    return s*A[-1][-1]
def norm(a): return det([mul(a,basis(7,j),7) for j in range(42)])

N=157662833878877367213009917598207232174012765021751
M=26717908551918972727509122511988955591425904906909
x=38519862799307894148512565859690422138485697855661
y=3088177783201613341856596606977577493764097037402
for a,b,n,u,expect in [(66,129,N,x,(1176,24,[7,42],[46,46])),
                       (15,131,M,y,(735,15,[7,45],[13,23]))]:
    A=rel(a,b)
    D0=norm(A)
    assert D0==7*n and pow(u,343,n)==1 and gcd(pow(u,49,n)-1,n)==1
    assert (1+pow(u,a,n)-u-pow(u,b,n))%n==0
    P=2401
    # Remainder does not require large values of A((1+P)*zeta).
    D1=norm([v*pow(1+P,i,P*P)%(P*P) for i,v in enumerate(A)])
    d=(D1-D0)%(P*P)
    assert d%P==0 and (d//P)%49==0
    t=(d//P//49)*pow(n,-1,49)%49
    L=[]
    for p in (3,5):
        a1=powel(A,(p**42-1)//49,p,7)
        L.append(next(j for j in range(49) if powel(basis(7,1),j,p,7)==a1))
    assert (d//P,t,L,[(l-t*j)%49 for l,j in zip(L,(29,8))])==expect

ps=(3089059,214827736571729,374998168847,633553982769970403)
assert prod(ps)==N
assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in ps[:-1])
p=ps[-1];F=(2,7,7,7,61,139,108921816233)
assert prod(F)==p-1 and all(all(a%d for d in range(2,isqrt(a)+1)) for a in F)
assert pow(2,p-1,p)==1 and all(gcd(pow(2,(p-1)//a,p)-1,p)==1 for a in F)
for p,L in zip(ps,((25,17),(23,33),(41,15),(6,30))):
    assert [pow(b,(p-1)//49,p) for b in (3,5)]==[pow(x,7*j,p) for j in L]
```
