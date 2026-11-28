# A logarithmic worst-label lower bound for the dyadic menu

There is an absolute \(\gamma>0\) such that for every sufficiently large \(k\), some real adjacent pair \((c,d),(c+1,d+1)\) with \(c\) even has the following property. In the low-residual zero class modulo \(Q=27\,2^k\), every integer displacement realizing a common target has length larger than \(\gamma Q^{1/4}(\log Q)^{1/4}\). No primitivity or parametrization restriction is imposed on the lower bound. The pair can be chosen with a genuine common target in the original window.


Set \(r=\lceil k/2\rceil\), \(m=2^{r+1}\), and \(Q=27\cdot2^k\). For even \(c\), a displacement of squared length \(A\) that serves the zero residual class must satisfy \(A+D\equiv0\bmod m\), where \(D=2\cdot3^c+4\cdot5^d\). The odd-\(k\) case uses the extra parity bit: after extracting \(2^{\lfloor k/2\rfloor}\) from both low-endpoint coordinates, those coordinates have the same parity. Their dot product with the odd-odd displacement is therefore even.

Landau’s bound counts **distinct norm values**. Below \(Y=\delta m\sqrt{\log m}\), there are fewer than \(m/16\) such values for sufficiently small fixed \(\delta\) and sufficiently large \(m\). Hence at least one class \(10\bmod16\) has no norm value up to \(Y\). For every fixed \(d\), the actual differences \(2\cdot9^{c/2}+4\cdot5^d\) with even \(c\) run through every class \(6\bmod16\). Indeed, \(9\) generates \(1+8\mathbb Z\) modulo \(2^r\), by \(v_2(9^a-1)=3+v_2(a)\). Choose \(d\) large and then an even \(c\) in the required exponent class with \(0.45d\le c\le0.55d\). This realizes the missing norm class using actual labels. [Landau’s 1908 paper](https://books.google.de/books?id=e3XBnQAACAAJ)

For existence at ordinary height, the elementary bounded-coordinate CRT construction gives a primitive displacement with \(A=O(Q)\) and \(27m\mid A+D\). The scaled integral line then has step \(O(Q)\) and minimum target \(L+(A+D)^2/(4A)\). At \(X=5^{2d+2}\), its minimum has \(\limsup \mu/X\le2/25\), as \(A\ge2\) and \(D=(4+o(1))5^d\). Its forward gap from \(X\) is \(O(Q\sqrt X+Q^2)=o(X)\) as \(d\to\infty\) for fixed \(k\). Both adjacent labels fit the original windows, since \(c/d\in[.45,.55]\) puts all required powers strictly inside their asymptotic ratio margins. The quantifiers are **for each sufficiently large \(k\), there exists a pair of labels**. The count gives no logarithmic improvement for a single pair fixed across all \(k\).

A compact exact control uses \(k=12\), labels \((14,26),(15,27)\), and displacement \((1,77)\). The relevant norm class is \(42\bmod128\), whose least norm is \(170\). The actual witness has low coordinates \((-7449349284982519488,135449110698140736)\).

```python
from math import gcd

p = [(14,26), (15,27)]
L,U = [3**c+5**d for c,d in p]
x,y = -7449349284982519488,135449110698140736
N = L+x*x+y*y

assert (U-L)%128 == 86
assert min(a*a+b*b for a in range(14) for b in range(14)
           if (a*a+b*b)%128==42) == 170
assert N == U+(x-1)**2+(y-77)**2
assert gcd(1,77)==1 and (N-L)%(27*2**12)==0
assert 5**54<N<2*5**54
for c,d in p:
    assert 3**(4*c)<=N<=3**(8*c) and 5**(2*d)<=N<=5**(3*d)
```

