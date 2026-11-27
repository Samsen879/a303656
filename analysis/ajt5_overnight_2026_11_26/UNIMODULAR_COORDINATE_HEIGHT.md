# Quadratic height and a cubic obstruction in the determinant-one construction

Use the system in [TWO_PARAMETER_THREE_LABEL_TRANSFER.md](TWO_PARAMETER_THREE_LABEL_TRANSFER.md), with \(T=3^C\), \(A=81T,B=91T\), and \(p=(a,b),q=(c,d)\) of determinant 1. Put \(P=|p|^2,\ \lambda=p\cdot q/P,\ p^\perp=(-b,a)\). From \(q=\lambda p+p^\perp/P\) one gets the exact transverse coordinate
\[
 |Z_\perp|=\sqrt P\,|B-\lambda A+\lambda(1-\lambda)P-P^{-1}|.
\]

## An actual quadratic-height subfamily

Fix \(b=243,d=271,\lambda_0=d/b>1\) and
\(P_*=(91-81\lambda_0)T/(\lambda_0(\lambda_0-1))\), which is positive. With \(L=\sqrt T\), choose the integer \(a\equiv7021\bmod7290\) nearest \(\sqrt{P_*-b^2}\), and put \(c=(ad-1)/b\). These choices retain \(p\equiv(1,3),q\equiv(0,1)\bmod30\). They give \(P-P_*=O(L)\) and \(\lambda-\lambda_0=O(L^{-1})\), so the bracket is \(O(L)\) and \(|Z|=O(L^2)\); its longitudinal component is \(O(L)\). With even \(D\) chosen so that \(5^D\asymp T^2\), both exponent scales remain logarithmic in the constructed target. This gives one direction for each \(C\), not two free directions of this height.

## Cubic height on a two-parameter subfamily

Choose \(a\in[L,1.1L]\) with \(a\equiv1\bmod30\) and \(r\in[0.4L,0.6L]\) coprime to \(a\). Take the least positive \(b\equiv3\bmod30\) with \(br\equiv-1\bmod a\). Möbius inversion counts \(\gg L^2\) such \((a,r)\), and each gives a distinct primitive \(p\) with \(b=O(L)\). All determinant-one completions have \(c\equiv r\bmod a\), hence \(\lambda=c/a+O(L^{-2})\) has fractional part in a fixed interior subinterval of \((0,1)\). Take \(T\asymp L^2\) with \(91T\le L^2/10\). The bracket divided by \(P\) is a downward quadratic in \(\lambda\), whose roots for sufficiently large \(L\) lie in \((-0.2,0)\) and \((1,1.2)\). Each allowed \(\lambda\) remains uniformly separated from both, so \(|Z|\gg L^3\) for every completion. A completion of size \(O(L)\) satisfying the same mod-30 conditions still exists. This obstruction is for determinant one, not for all coordinate parameterizations.

## Counting the quadratic-height directions

For \(a\asymp L, |b|=O(L), T\asymp L^2\), the quadratic-height condition forces \(\lambda\) within \(O(1/L)\) of one of two uniformly separated roots. Regarding \(b\) as the variable, the roots have derivative \(O(1/L)\) (differentiate their coefficients via \(P=a^2+b^2\)), so \(c=a\lambda+O(1/L)\) is within \(O(1)\) of two bounded-slope curves. At fixed \(a\), cover them by \(O(L^{3/4})\) grid squares of side \(H=c_0 L^{1/4}\), \(c_0>0\) sufficiently small.

Inside a square \(bc\equiv-1\bmod a\) means the translated \(uv\) column is a linear combination of \(1,u,v\) modulo \(a\). Thus the integer determinant of any four \((1,u,v,uv)\) rows is divisible by \(a\), and its magnitude is \(O(H^4)<a\), so it vanishes. Three collinear distinct points cannot occur: there is at most one point on each vertical or horizontal line since the coordinates in the congruence are units and \(H<a\). On any other line the \((1,u,uv)\) determinant of three points is nonzero as \(uv\) restricts to a genuine quadratic in \(u\). Yet it is divisible by \(a\) (the \((1,u,v)\) determinant is zero) and is \(O(H^3)<a\), a contradiction.

If a square has at least three points, their noncollinearity gives a single integral bilinear relation with nonzero \(uv\) coefficient, and bounded integer coefficients from the minors. Completing the product reduces it to an integer factorization with constant of size \(O(H^8)\). A zero constant gives two lines with only boundedly many points; a nonzero constant gives \(L^{o(1)}\) choices by the divisor bound. Summing over \(a\) proves \(O_\varepsilon(L^{7/4+\varepsilon})\) directions of quadratic height in this model. This counts directions, not necessarily distinct targets.

```python
from math import gcd

def check(C, D, a, b, c, d, expected):
    assert a*d-b*c == 1 and (a%30,b%30,c%30,d%30) == (1,3,0,1)
    A, B = 81*3**C-a*a-b*b, 91*3**C-c*c-d*d
    x, y = d*A-b*B, a*B-c*A
    Z = [(x,y), (x+2*a,y+2*b), (x+2*c,y+2*d)]
    zs = [(u-v,u+v) for u,v in Z]
    R = [u*u+v*v for u,v in zs]
    n = 3**(C+6)+5**D+R[0]
    assert n == expected
    assert all(n-3**e-5**D == r > 0 and r%8 == 2 and r%3 == 1
               for e,r in zip((C+6,C+4,C),R))
    assert gcd(R[0],R[1]) == 2 and gcd(R[1],R[2]) == 10
    assert all((u+2*v)%5 == 0 and (u-2*v)%5 for u,v in zs[1:])

check(4, 20, 301, 1503, -150, -749, 14288966225328005036)
check(16, 20, 14311, 243, 15960, 271, 2307595020872046198596)
```
