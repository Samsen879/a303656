# An actual short-prime bound for positive shared depth

In [the fixed-109 setting](SPLIT109_ONE_CRT_REP_PER_PRIME.md), take actual labels \((0,mb),(ma,0)\), \(A=3^a,\ B=5^b\), \(X=A^m,\ Z=B^m\), and \(n\) in the positive negative-cross-offset interval \(\max(X,Z)+1<n<X+Z\). This bound concerns the branch where the extra inert prime \(p>5\) divides both residuals and their unequal valuations have positive even minimum \(t=v_p(Z-X)\). It does not cover the one-sided \(t=0\) branch.

Writing \(m=2^kh\) with \(k\ge1\), \(h\) odd, let \(C_-=\lvert B^h-A^h\rvert\), \(C_+=B^h+A^h\). Factor \(B^m-A^m\) as \(C_-C_+\) up to sign times the factors \(B^{2^jh}+A^{2^jh}\), \(1\le j<k\). The latter are sums of squares of units at \(p\), so an inert \(p\) cannot divide them. Since \(A,B\) are coprime, \(C_-\) and \(C_+\) share no odd prime. Thus the exact \(p\)-depth comes from just one of \(C_\pm\), including the actual odd exponent \(h\).

In any integer interval \([P,P+H]\), \(P\ge7\), the number of candidates with \(t\ge T\ge2\) is at most
\[
 \min\left(\lfloor H/4\rfloor+1,\
   \left\lfloor\frac{\log C_-}{T\log P}\right\rfloor+
   \left\lfloor\frac{\log C_+}{T\log P}\right\rfloor\right).
\]
The first term counts the allowable mod-4 class. For the second, the product of the distinct \(p^T\)'s in each branch divides its \(C_\pm\). In particular there are no candidates if \(P^T>C_+\), before even imposing the CRT representative, quartic filter, or full rough-part window.

This gives a subexponential no-candidate cutoff for infinitely many balanced actual label pairs. Choose infinitely many \(a,b\) with \(|a\log3-b\log5|<\log3/b\) via continued fractions, and let \(m\) be the largest power of two at most \(b\) (so \(h=1\)). Then \(1/3<X/Z<3\), \(b/2<m\le b\), and the active height satisfies \(\log n\ge mb\log5\). Hence \(\log C_+\le b\log5+O(1)\le\sqrt{2\log5\,\log n}+O(1)\). For \(T=2\) this excludes \(p\) with \(\log p>(\sqrt{\log5/2}+\epsilon)\sqrt{\log n}\) for each fixed \(\epsilon>0\) and large enough targets in these labels. It does not prove the existence of any complete strong product certificate.

## True-label controls

For \(a=66,b=45,m=4\), the only inert prime between 7 and 109 with positive even depth is 7, of depth two, and it occurs in the sum branch. With \(m=28\) the actual depth at 7 becomes three, illustrating why the odd part of \(m\) matters. In the original \(m=4\) labels, depths \(E=f=44\) give a positive CRT candidate in the allowed height interval; both rough parts nevertheless exceed the stipulated upper cutoff, and the deep residual fails at 191.

```python
from math import isqrt
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
def v(x,p):
    e=0
    while x%p==0:
        x//=p; e+=1
    return e
A,B=3**66,5**45
X,Z=A**4,B**4
p=7
assert v(B+A,p)==v(Z-X,p)==2 and v(B**28-A**28,p)==3
assert [q for q in range(7,110,4) if prime(q) and
        v(Z-X,q)>0 and v(Z-X,q)%2==0]==[7]
Q,V=109**44,7**44
n=X+1+V*((Z-X)*pow(V,-1,Q)%Q)
assert max(X,Z)+1<n<X+Z
r,s=n-1-Z,n-1-X
assert (v(r,7),v(s,7),v(r,109),v(s,109))==(2,44,44,0)
def rough(r):
    for p in range(2,110):
        if prime(p):
            r//=p**v(r,p)
    return r
assert min(rough(r),rough(s))>139*151 and v(s,191)==1
```
