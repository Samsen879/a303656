# An explicit moving-parent quartic at a real 3,5 label

Use the real label $(10,2;11,3)$ and set $A=5^{10}+3^2-131779$, $B=(5^{11}+3^3-658897)/5$, $H=A+5$, and $m=H/2$. We have $A-B=4$. For a parameter $t$, define
$$
z=t^2-2,\quad w=(z^2+m^2+B)/H,\quad D=(t^2+A)/m,\quad
(P,Q)=(w-D,t(D-1)).
$$
Direct expansion gives $P^2+Q^2=w^2-A$ and $(w-m)^2+z^2=w^2-B$. Thus the parent difference $D$ varies quadratically; the normalized child has a constant difference $m$. Multiplying the child coordinates by $1+2i$ gives the target norm $5(w^2-B)$.

The parent has integer coordinates after the fixed rational rotation $(a+bi)/L$, where $(a,b,L)=(-1647087,1757216,2408465)$ and $a^2+b^2=L^2$, evaluated at $t=8404257$. The replay below checks the integer anchor. The polynomials for $w$ and both pairs after rotation and scaling have integer coefficients after multiplication by $HL$. Consequently replacing $t$ by $8404257+30HLn$ gives integer polynomials in $n$: all nonconstant coefficients are multiples of $30$ and the constants are integers by the anchor check. This also preserves $w\equiv26\bmod30$. The leading coefficient of the quartic $w$ is positive, hence this is an unbounded family.

This only certifies the single given label with a moving parent and fixed normalized child. It does not certify a growing menu of labels, a simultaneously moving pair, or the original conjecture.

Replay (Python standard library):

```python
from fractions import Fraction as F

A=5**10+3**2-131779
B=F(5**11+3**3-658897,5)
H=A+5
m=F(H,2)
a,b,L=-1647087,1757216,2408465
assert A-B==4 and a*a+b*b==L*L and m.denominator==1

def orbit(n):
    t=8404257+30*H*L*n
    z=t*t-2
    w=(z*z+m*m+B)/H
    D=F(2*(t*t+A),H)
    P,Q=w-D,t*(D-1)
    X,Y=(a*P-b*Q)/L,(b*P+a*Q)/L
    U,V=w-m-2*z,2*(w-m)+z
    assert all(v.denominator==1 for v in (w,X,Y,U,V))
    assert w%30==26
    assert X*X+Y*Y==w*w-A and U*U+V*V==5*(w*w-B)
    return w
assert orbit(0)==517841637563222283536
assert orbit(1)>orbit(0)
assert orbit(3)>orbit(1)
```
