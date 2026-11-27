# Equal multiplicative orders do not anchor the actual gap

Use the setup in [FIXED_OFFSET_ANCHOR.md](FIXED_OFFSET_ANCHOR.md): \(X_0=3^{18},Z_0=5^{13}\), \(S=81\cdot109,\ D=25\cdot47^2\), \(u=19141,w=18149\), and \(\Delta_0=Z_0-X_0=Dw-Su\). Both residuals \(Su,Dw\) are true norms. Replace \(u\) by \(18269\): its new residual is \(180^2+12699^2\), and \(Dw=4418^2+31349^2\). The gap \(\xi=Dw-S\cdot18269\) differs from \(\Delta_0\) by \(8S\cdot109\). Yet each gap has order 36 mod 109 and its 36th power is \(1+87\cdot109\bmod109^2\). The binomial lift therefore gives order \(36\cdot109^{j-1}\) for both at every \(109^j\).

## Infinitely many examples at every fixed agreement depth

Put \(K=X_0-Su=Z_0-Dw=218424600\), a unit mod \(p=109\). Take \(A=9^h,\ B=25^\ell\) and new labels \(X=X_0A,Z=Z_0B\). Use residuals \(SAu,DBw\); their square coordinates are scaled by \(3^h,5^\ell\). The two proposed targets \(Z+1+SAu\), \(X+1+DBw\) differ, since the free gap minus the prescribed gap is \(K(A-B)\).

Let \(m=27\cdot1081\). For any \(k\ge2\) choose \(h\equiv mp^{k-1}\pmod{mp^k}\), \(\ell\equiv0\pmod{mp^k}\). At \(p\) both bases have order 27 and their 27th powers are nontrivial mod \(p^2\). Binomial lifting gives \(v_p(A-1)=k\), \(v_p(B-1)\ge k+1\), hence \(v_p(K(A-B))=k\). Both \(A,B\) equal 1 mod \(8\cdot47^2\), and both gaps equal \(\Delta_0\bmod p^2\), so they retain all the equal orders and the phase mod \(47^2\).

There are infinitely many positive pairs on these fixed progressions with \(999/1000<A/B<1001/1000\). The logarithm of this ratio is a fixed shift of multiples of \(mp^k\log9\) minus multiples of \(mp^k\log25\); the rotation modulo \(mp^k\log25\) is irrational by prime factorization and visits the indicated open interval infinitely often. For sufficiently large visits the resulting \(\ell\) is positive.

On that ratio interval the targets both lie in \((\max(X,Z)+1,X+Z)\), since \(Z>KA,\ X>KB,\ KA,KB>1\). The cross-reconstructed rough parts \(u+(K/S)(1-B/A)\) and \(w+(K/D)(1-A/B)\) stay in the original \([16637,20988]\) and satisfy the strict product cutoff against the fixed opposite rough parts. The latter bounds follow by checking the endpoints below. This keeps the rough parts but varies the scales, and does not keep the full varying shallow modulus: \(v_3(K(A-B))=4\) for positive \(h\). The anchoring lemma with its full modulus assumption remains valid.

```python
from fractions import Fraction as Q
from math import gcd, isqrt
p,m=109,27*1081
X,Z,S,D,u,w=3**18,5**13,81*p,25*47**2,19141,18149
K=X-S*u
assert K==Z-D*w==218424600 and gcd(K,p)==1
assert K%3**4==0 and K%3**5!=0
assert S*18269==180**2+12699**2 and D*w==4418**2+31349**2
assert any(isqrt(S*u-a*a)**2==S*u-a*a for a in range(isqrt(S*u)+1))
de,xi=Z-X,D*w-S*18269
assert xi-de==8*S*p
for n in (xi,de):
    assert pow(n,36,p*p)==1+87*p
    assert pow(n,12,p)!=1 and pow(n,18,p)!=1
for b,r in ((9,105),(25,14)):
    assert pow(b,27,p*p)==1+r*p and pow(b,9,p)!=1
    assert pow(b,m,8*47**2)==1
L,U=16637,20989
assert gcd(u,w)==1 and u*w<L*U
assert all(u%d and w%d for d in range(2,110))
for a in (Q(999,1000),Q(1001,1000)):
    assert Z>K*a and X*a>K
    r=u+Q(K,S)*(1-1/a)
    t=w+Q(K,D)*(1-a)
    assert L<=r<=U-1 and L<=t<=U-1
    assert r*w<L*U and t*u<L*U
```
