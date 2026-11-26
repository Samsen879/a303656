# An ordinary P2 height gap from two exact divisor pairs

**The second factor pair gives an unconditional height gap inside the ordinary window.** On the pinned cofinal subfamily with \(39/40\le B/A\le122/125\), there is a rationally defined height \(K_0\) between \(1032A\) and \(1046A\). No four-square P2 solution occurs within \(32\sqrt A\) of \(K_0\). The argument uses the products of the two exact factor pairs. [Pinned joint sieve](https://github.com/Samsen879/a303656/commit/3974a3164490be9d05c8dd6cdaf0f31f177c4ecc)

### The second divisor interval

Let \(W=\sqrt A\) and \(D=f-e=162A-31B\). If the last two half-roots are integers \(P,Q\), put \(r=P-Q\) and \(s=P+Q\). Then
\[
rs=D,\qquad r(K)=\frac{\sqrt{K-S_2}-\sqrt{K-S_3}}2.
\]
In \(1000A<K\le1100A\), the exact interval is \([r(1100A),r(1000A))\). On the stated strip it is contained in \(5W<r<6W\). These bounds follow by evaluating the decreasing function \((r+D/r)^2\) at \(5W\) and \(6W\).

This gives a reversible test. For a true earlier divisor \(\ell\mid E\), set \(v=w_*R\ell\) and \(u=d/v\). The remaining task is to find a divisor \(r\) in the second interval, set \(s=D/r\), and check
\[
(u+v)^2-(r+s)^2=4e.
\]
Since \(D\) is odd, \(r,s\) are odd. A passing pair reconstructs the two integer half-roots as \((s+r)/2\) and \((s-r)/2\), at the same height as the first pair.

### The height gap

The two real short factors coincide at \(K_0\). Its exact definition is
\[
v_0^2=\frac{d^2-D^2}{4e-2(d-D)},\qquad
K_0=S_0+2d+v_0^2+\frac{d^2}{v_0^2}.
\]
Rational bounds verify \(v_0^2<\min(d,D)\) and \(1032A<K_0<1046A\). Throughout the target height window, both short-factor functions are decreasing with derivative magnitude below \(1/(64W)\). Thus \(|r(K)-v(K)|<1\) whenever \(|K-K_0|\le32W\).

If both factors are integers, they must then be equal. But
\[
81d-D=12181B,\qquad \gcd(d,B)=1,
\]
so a common divisor of the two products is at most \(12181\), whereas \(r>5W>12181\) in this family.


For sufficiently large \(A\), the whole indicated gap lies inside the tested height interval, and \(5\sqrt A>12181\). In the selected earlier-share allocation it corresponds to an interval for \(\ell\) of width less than \(1/(w_*R)\), hence at most one integer can land there. The restriction does not rule out the rest of the window or prove an existing divisor lands specifically in the gap. The exact rational endpoint test below uses \(B/A\) in the stated strip.

```python
from fractions import Fraction as F
lo,hi=F(39,40),F(122,125)
d0,d1=2+150*lo,2+150*hi
D0,D1=162-31*hi,162-31*lo
x0=(d0*d0-D1*D1)/(400-262*lo)
x1=(d1*d1-D0*D0)/(400-262*hi)
assert 0<x0<=x1<min(d0,D0)
k0=(1+25*lo)+2*d0+x0+d0*d0/x1
k1=(1+25*hi)+2*d1+x1+d1*d1/x0
assert 1032<k0 and k1<1046
assert 81+125*lo+(5+D0/5)**2>1100
assert 81+125*hi+(6+D1/6)**2<1000
assert 1000-(9+625*hi)>16**2
assert 1000-(729+hi)>16**2
for t in (lo,hi):
 d,D,e=2+150*t,162-31*t,20+25*t
 assert 81*d-D==12181*t
 assert 4*e-2*(d-D)==400-262*t
print('OK',float(k0),float(k1))
```
