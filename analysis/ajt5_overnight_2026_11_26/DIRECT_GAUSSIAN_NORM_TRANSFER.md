# Direct Gaussian norm transfers on actual exponent points

Both constructions below preserve the same \(n\) and use true square coordinates. They do not require factoring a new residual. They construct families of targets, not representations for arbitrary targets.

## Commuting two-step transfers

For a known \(R=a^2+b^2\), an exponent increase subtracts a known amount \(\Delta\). If \(4uv=\Delta\) and \(|a|=u+v\), then replacing \(a\) by \(u-v\) certifies the new residual, by difference of squares. For an increase by 2 of the 3 exponent, \(\Delta=8\cdot3^c\); for the 5 exponent, \(\Delta=24\cdot5^d\).

Set \(x=3^{\lfloor c/2\rfloor},y=5^{\lfloor d/2\rfloor}\). For the 3 axis use \(a=3x\) if \(c\) is even and \(5x\) if it is odd; then \(a^2-x^2=8\cdot3^c\). For the 5 axis use \(b=5y\) if \(d\) is even and \(11y\) if it is odd; then \(b^2-y^2=24\cdot5^d\). Define \(n=a^2+b^2+3^c+5^d\). The two replacements act on separate square coordinates, so this same \(n\) has four positive-residual points \((c,d),(c+2,d),(c,d+2),(c+2,d+2)\). Also \(n\le10\cdot3^c+26\cdot5^d\), so the exponents can be genuinely large relative to the target. For example at \(n=5418\) and initial \((5,3)\) the four coordinates are \((45,55),(9,55),(45,5),(9,5)\).

When \(c\equiv1\bmod4\) with \(c\ge5\) and \(d\ge3\) is odd, these \(n\) are \(2\bmod8\) and \(3\bmod5\), so cannot themselves be a sum of the two powers with zero square terms. Indeed, \(3^j+5^k\equiv2\bmod8\) forces both exponents even, and then cannot be \(3\bmod5\), whether or not \(k=0\).

## Iteration at a designated center

Fix an odd positive integer \(A\), set \(n=3^A+5^D\), and hold \(d=D\) fixed. At \(c=A-m\) with \(m>0\) odd, the residual is \(3^{A-m}(3^m-1)\). If \(z\) is a Gaussian integer certifying it and \(3m\le A\), put
\[
 z'=\frac{z}{3^m}\big((3^m-1)+i\,3^{(m+1)/2}\big).
\]
It is integral because \(-1\) is not a square mod 3: iterating division by 3 on the two square coordinates shows each is divisible by \(3^{(A-m)/2}\), hence by \(3^m\). The identity
\[
 (3^m-1)^2+3^{m+1}=3^{2m}+3^m+1=\frac{3^{3m}-1}{3^m-1}
\]
shows that \(z'\) certifies the residual at \(c=A-3m\). Starting at \(m=1\) with \(z=3^{(A-1)/2}(1+i)\) gives all \(m=1,3,\ldots,3^J\) whenever \(3^J\le A\). Only the first gap is 2; later gaps are \(2m\). The target in this chain already has a zero-square representation at the designated center.

Even there, ordinary neighbor transfer need not hold: when odd \(A\ge15\), the point \(m=9\) has coordinates \(3^{(A-9)/2}(19,139)\), but \(m=11\) has odd valuation at 23 since \(3^{11}\equiv1+20\cdot23\bmod23^2\). It is not a square sum.

```python
for c in range(12):
    for d in range(10):
        x,y=3**(c//2),5**(d//2)
        a,b=x*(5 if c%2 else 3),y*(11 if d%2 else 5)
        n=a*a+b*b+3**c+5**d
        assert n <= 10*3**c+26*5**d
        for i,j in ((0,0),(0,2),(2,0),(2,2)):
            v,w=x if i else a,y if j else b
            assert n==v*v+w*w+3**(c+i)+5**(d+j)
A,m=247,1
a=b=3**((A-1)//2)
while 3*m<=A:
    q=3**m
    r,s=q-1,3**((m+1)//2)
    assert a%q==b%q==0
    a,b=(a*r-b*s)//q,(a*s+b*r)//q
    m*=3
    assert a*a+b*b==3**(A-m)*(3**m-1)
assert m==243
assert 3**9-1==19**2+139**2
assert pow(3,11,23**2)==1+20*23
```
