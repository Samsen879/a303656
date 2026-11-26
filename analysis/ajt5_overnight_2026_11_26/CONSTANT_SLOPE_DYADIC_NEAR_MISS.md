# A constant-slope quartic anchor passes odd primes but fails at 2

For the square-difference labels $(d,2;d+1,3)$, $d=8+6j$, let $A=5^d-131770$, $B=A-4$. In the minus-sign chart put $r=u+u^{-1}-2$ and $H=r+A/r+4$. Then $rH=A+(u-u^{-1})^2$ identically. The concrete choice $u=5$ gives $r=16/5$ and $H=(25A+576)/80$, so $H\equiv3\bmod9$ and $v_2(H)=-4$.

In this chart $w=((rt^2-2)^2+(H/2)^2+B)/H$. Substitution of $t=3/2$ gives $w=5+5A/64$, integral at every odd prime and $2\bmod3$. For the 5-adic requirement alone, $t=13/2$ changes $w$ by $1417216/(25A+576)$, a 5-adic unit congruent to 1, so the target digit is locally obtainable there. These calculations require no information about factorization of the varying $H$.

However the identity $(w-H/2)^2+(rt^2-2)^2=w^2-B$ forbids an integer $w$ for every rational $t$. If the right side is integral at 2, each coordinate of the rational sum of squares must be integral at 2: after factoring out a pole of order $j\ge1$, the two squares' sum has valuation $-2j$ or $-2j+1$, both negative. But $v_2(H/2)=-5$, so $w-H/2$ necessarily has a pole. Thus the odd-prime controls do not transfer to a global integral anchor on this slope; other slopes are open.

```python
for d in (8,14,20):
    A=5**d-131770
    h=25*A+576  # H=h/80
    assert h%2 and h%9==6
    assert 1024*26**2+h*h+25600*(A-4)==25*h*(64+A)
    assert 1024*(666**2-26**2)//320==1417216
    assert 1417216%5==h%5==1
```
