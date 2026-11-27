# Verified partial obstructions at the new 29-ray bottleneck

The [native 157 extension](https://github.com/Samsen879/a303656/commit/0822ed65934d962a216f7d22758b2e8621a399f4) leaves a unique largest ratio \(29/27\) between \(30\) and \(290/9\). The next-largest ratio is \(35/33\), at \(22,70/3\). Hence any future certified interior phase in \([638/21,350/11]\) would reduce the maximum to \(35/33\) and raise the effective generated lower exponent to \(33/70\). No such ray is certified here.

For an integer norm \(25^U-9^V=x^2+3y^2\) with \(U,V>0\), both exponents must be odd. Opposite parity gives exact \(v_2=3\), whereas a nonzero integer norm \(x^2+3y^2\) has even 2-adic valuation (reduce common factors of two, then either the coordinates have opposite parity or both are odd). If both exponents are even, the odd half \((5^U+3^V)/2\equiv2\bmod3\) supplies an odd-valuation inert prime; such an odd prime cannot also divide the other sign. Thus the first in-gap scale \(2U/3\) requires \(U=47\), with 34 possible odd \(V\) once \(3^V<5^U\) is enforced. The replay below independently excludes 32 by exact inert valuations and \(V=17\) by odd \(v_2=5\). The \(V=39\) case is not asserted as independently excluded in this note.

The fresh-inert obstruction is independent of factoring a new large shell. If an odd inert \(q\) divides \(X-Y\) for \(X=25^u,Y=9^v,u,v>0\), then
\[
 D=\frac{X^q-Y^q}{q(X-Y)}
\]
is an integer prime to \(q(X-Y)\); for primes dividing \(X-Y\), the cyclotomic quotient reduces to \(qY^{q-1}\), and LTE gives valuation exactly one at \(q\). Also \(D\equiv2\bmod3\) and is odd, forcing a new inert prime of odd valuation, whose ratio order is exactly \(q\). This is the first step of the earlier persistence argument. It does not rely on odd valuation of the original \(q\) in \(X-Y\).

At the deeper phase \(2546/81\), the actual catalogue seed \((67,83)\) cannot take a step 19, by exact ratio order 19 and initial odd inert valuation at 647. At the scale-9 pair \((137,139)\), an exact coprime divisor \(475295400253176822377\equiv2\bmod3\) in the minus half suffices to certify a failure; no primality assertion about that divisor is needed. The distinct prime parities guarantee an inert factor of odd valuation cannot be repaired by another factor of the product.


```python
from math import gcd,isqrt
from fractions import Fraction as F
def vp(n,p):
    k=0
    while n%p==0:
        n//=p;k+=1
    return k
pairs=[(1,11),(3,17),(5,23),(7,5273),(9,971),(11,11),(13,1097),(15,47),(19,815939),(21,11),(23,1187),(25,257),(27,17),(29,53),(31,11),(33,83),(35,17),(37,113),(41,11),(43,17),(45,83117),(47,8273),(49,23),(51,11),(53,227),(55,53),(57,137),(59,17),(61,11),(63,317),(65,179),(67,17)]
legal={v for v in range(1,70,2) if 3**v<5**47}
assert len(legal)==34 and legal-{v for v,p in pairs}=={17,39}
for v,p in pairs:
    assert p%3==2 and all(p%d for d in range(2,isqrt(p)+1))
    assert vp(25**47-9**v,p)==1
assert vp(25**47-9**17,2)==5
p=647
assert p%3==2 and all(p%d for d in range(2,isqrt(p)+1))
z=pow(25,67,p)*pow(pow(9,83,p),-1,p)%p
assert z!=1 and pow(z,19,p)==1
assert (pow(25,67*19,p*p)-pow(9,83*19,p*p))%p**2==13*p
A,B=5**137,3**139
F0=(A-B)//2
q=475295400253176822377
assert F0%q==0 and q%3==2 and gcd(F0//q,q)==1 and gcd(q,A+B)==1
g=list(map(F,("18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 "
 "82/3 86/3 30 290/9 34 314/9 110/3 38 118/3 122/3 42 130/3 134/3 46 "
 "142/3 50 470/9 158/3 54").split()))
ratios=sorted(b/a for a,b in zip(g,g[1:]))
assert ratios[-2:]==[F(35,33),F(29,27)]
assert F(290,9)/ratios[-2]==F(638,21) and 30*ratios[-2]==F(350,11)
```
