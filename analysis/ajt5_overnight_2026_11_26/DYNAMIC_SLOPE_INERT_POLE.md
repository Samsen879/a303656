# A dynamic norm certificate with an unavoidable odd inert pole

For the true labels $(d,2;d+1,3)$, $d=8+6j$, put $A=5^d-131770$, $B=A-4$, and define the plus-sign slope chart by
$$
 x=\frac{175784622475}{67595335390054}(9\cdot5^d+1),\qquad
 r=A/x,\qquad H=r+x-4.
$$
It has the exact algebraic certificate
$$
 xH=\left(x-\frac{456583435}{74047}\right)^2+
       A\left(\frac{1259978}{74047}\right)^2 .
$$
After cancellation of $x^2$, this is linear in $5^d$, so two exact evaluations suffice to check the polynomial identity. Unlike the constant-slope near miss, the slope here is a 2-adic unit: $9\cdot5^d+1$ has valuation one, the prefactor has valuation minus one, and $A$ is odd. At the first label $d=8$, the exact value at $t=1$ is integral at 2, 3 and 5 with residue 26 modulo 30 in those local rings.

Nevertheless, at the inert prime $p=1185931=9\cdot131770+1$, there is no integral anchor, for any of these labels. The prime divides the numerator of the prefactor and not its denominator. Since $p\equiv3\bmod4$, $9\cdot5^d+1=(3\cdot5^{d/2})^2+1$ is never zero modulo $p$, and $9A\equiv9\cdot5^d+1$ gives $v_p(A)=0$. Consequently $x$ has positive valuation, $r$ has negative valuation, and $H=r+x-4$ inherits the pole. In the norm identity
$$
 (w-H/2)^2+(rt^2+2)^2=w^2-B
$$
an integral $w$ would make the right side integral at $p$, but the pole of the first coordinate is impossible in an integral sum of two rational squares when $p\equiv3\bmod4$. This demonstrates that the formal polynomial identity and correcting the dyadic slope do not suffice. It does not classify all dynamic slope certificates.

```python
from fractions import Fraction as F
from math import isqrt
p=1185931
assert p==9*131770+1 and p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
assert 175784622475%p==0 and 67595335390054%p!=0
for d in (8,14):
    A=5**d-131770
    x=F(175784622475,67595335390054)*(9*5**d+1)
    r=F(A,1)/x
    H=r+x-4
    assert x*H==(x-F(456583435,74047))**2+A*F(1259978,74047)**2
    if d==8:
        w=((r+2)**2+(H/2)**2+A-4)/H
        assert w.numerator*pow(w.denominator,-1,30)%30==26
```
