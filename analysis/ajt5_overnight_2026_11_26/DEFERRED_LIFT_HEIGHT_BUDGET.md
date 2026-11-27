# Deferred exact lifts and a linear numerical height gap with fixed ordinary rows

For a finite inert panel \(Q\subset(3,\infty)\), suppose each row has at least one ordinary direction (base 3 or 5 with initial LTE depth one). Put \(s=|Q|\), \(Y=\max Q\), \(J=\{p\in Q:p>s,\ p^2>Y\}\), and \(h=|J|\). Set \(P_b\) to the lcm of the seed period, \(\operatorname{ord}_{p^3}(b)\) for \(p\notin J\), and \(\operatorname{ord}_{p^2}(b)\) for \(p\in J\). For the usual parity and 3-adic seed take periods 2 and 18, and representatives \(c\ge3\). A sufficient positivity budget for the finite panel is
\[
 n>3^{(h+1)P_3+2}+5^{(h+1)P_5-1}.
\]

Process rows in ascending order. At a current collision use the ordinary direction and take the step to be the lcm of preceding preservation periods and the current phase order mod \(p\); it is coprime to \(p\). LTE makes the residual zero mod \(p^2\) for \(J\), and of exact valuation 2 for all remaining rows. Units can simply be preserved. Reduce the resulting exponents to representatives in \([3,P_3+2]\) and \([0,P_5-1]\). Now add \((iP_3,jP_5)\), \(0\le i,j\le h\). Any deferred colliding row has \(v_p(b^{P_b}-1)=2\) on an ordinary direction: its own squared-modulus order contributes one \(p\), and no other row introduces \(p^2\) because \(p^2>Y\). Thus each row's bad last digit defines a nonconstant affine line mod \(p\); it hits at most \(h+1\) points of the grid because \(p>h\). Fewer than \((h+1)^2\) points are bad, proving the budget. For a given start from which exponents may only increase, retain the cumulative steps instead of reducing; a sufficient check is positivity at the upper right corner after adding the reserve \((hP_3,hP_5)\). For \(Q=\{7,11\}\) the deferred periods are \(210,6930\) instead of \(16170,533610\).

## A growth obstruction for numerical height, not for exponent steps

Let \(C\equiv70,D\equiv48\bmod3028410\) with \(A=3^C,\ B=5^D,\ A\le B\le2A\). There are arbitrarily large such anchors by density of an irrational rotation after imposing the two exponent classes. Write \(S=9A+25B\), \(U=81A+B\). Independently choose the true target
\[
 n=3^6+1+(16738952329+27174124824t)^2+20813280436^2
\]
using the first nonnegative \(t\) with \(n>S\). For large anchors \(n=S+O(\sqrt S)<U\). The progression fixes \(n\bmod24\) and the required residues mod \(7^2,11^2,19^2,23^2\). The anchor congruence fixes both powers at all four prime squares.

Search all \(c\ge C,d\ge D\) with positive residual and \(R\equiv1\bmod4\). Since \(n\equiv3\bmod24\), these have \(v_3(R)=0\) and \(c\) even. Exactly six candidates are positive, at \(c=C,C+2\), \(d=D,D+1,D+2\). Their respective once-dividing inert rows are \((7,19,11)\), \((11,23,7)\). On the narrower natural \(R\equiv1\bmod8\) branch the even \(d\)-columns alone remain, and rows 7 and 11 suffice. The actual start has \(n-A-B>16n/17\), since \(S\ge17(A+B)\). Yet the active menu cannot pass the panel. Keeping the same target modular data, the first new candidate beyond this menu arrives just above \(U\), at \((C+4,D)\), and it is a unit at all four rows. Since \((U-S)/S=(72-24(B/A))/(9+25(B/A))\ge24/59\), the numerical gap is at least \((24/59-o(1))n\). The extra exponent increment is four, not a growing lower bound on the number of exponent steps. The target's independent true representation uses \((6,0)\), outside the monotone menu.

```python
from math import lcm,isqrt
ps=(7,11,19,23)
P,M=3028410,27174124824
C,D=70,48
A,B=3**C,5**D
S,U=9*A+25*B,81*A+B
def target(t):
    return 3**6+1+(16738952329+M*t)**2+20813280436**2
a=16738952329
w=max(0,S-(3**6+1+20813280436**2))
t=max(0,(isqrt(w)-a)//M+1)
n=target(t)
assert n==111346247159348327523668634708223947
assert A<=B<=2*A and S<n<U and n%24==3
assert t==0 or target(t-1)<=S
for p in ps:
    assert M%(p*p)==0 and pow(3,P,p*p)==pow(5,P,p*p)==1
for i,row in [(0,(7,19,11)),(2,(11,23,7))]:
    for j,p in enumerate(row):
        r=n-3**i*A-5**j*B
        assert r>0 and r%(p*p) in range(p,p*p,p)
assert all((n-U)%p for p in ps) and 17*(n-A-B)>16*n
```
