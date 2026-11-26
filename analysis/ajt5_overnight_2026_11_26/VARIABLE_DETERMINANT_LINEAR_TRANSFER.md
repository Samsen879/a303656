# A growing determinant permits a linear-height three-label family

The exact identities \(3^{12}+2\cdot639^2=3^8+2\cdot819^2=1+2\cdot821^2=1348083\) yield three distinct labels of one actual integer. Let positive \(j\equiv0\bmod4,\ f=3^j,\ D\ge4\) even, and positive \(a\equiv82\bmod1230\). Put
\[
 n=1348083 f^2+5^D+2a^2,\quad
 Z=(-a,639f),\quad p=(a,90f),\quad q=(0,91f).
\]
Multiply \(Z,Z+2p,Z+2q\) by \(1+i\); their norms give the respective positive residuals at \((2j+12,D),(2j+8,D),(2j,D)\). The determinant of \(p,q\) is \(91af\). Even though this determinant grows, the two integer dot-product equations are exact: the second reduces to \(91fZ_y=91f\cdot639f\), and the first then gives \(aZ_x=-a^2\).

The residuals are \(2\bmod8\), so each contains precisely one ramified Gaussian factor above 2. They are \(2\bmod3\), so 3 does not enter a common factor. Modulo 5 the first Gaussian point vanishes only at \(i=-2\), whereas the other two vanish only at \(i=2\). The first norm difference is \(80\cdot3^{2j+8}\); the second is \(6560\cdot3^{2j}\), and its extra prime 41 is absent from the residual at \(Z+2p\) since \(41\mid a,\ 41\nmid819f\). Both differences have 5-adic valuation 1. The actual Gaussian gcd norms of the first and second consecutive pairs are therefore 2 and 10, respectively, even though the first pair's *integer norm* gcd is 10. Also \(n\equiv4\bmod8\) and \(n\equiv0\bmod3\), excluding a representation using just the two powers.

For each large \(X\) choose \(j,D\) so the two offsets \(1348083 f^2,5^D\) are each comparable to \(X\) and at most \(X/4\) (the geometric steps are bounded constants). Vary \(a\in[\sqrt X/4,\sqrt X/3]\) in its residue class. This gives \(\gg\sqrt X\) distinct targets up to \(X\) at one set of three ordinary-height labels, with \(|Z|=O(\sqrt X)\), a linear height in the direction scale. The family has one free coordinate per fixed \(j,D\), not two.

Across all allowed inputs the number of distinct targets up to \(X\) is \(\Theta(\sqrt X(\log X)^2)\): the upper bound counts parameters. For the lower bound restrict the center offset to \([X^{1/10},X^{1/5}]\) and the 5-power to \([X^{3/10},X^{2/5}]\); then each index has \(\gg\log X\) choices. Their combined variation is \(o(\sqrt X)\) and cannot bridge two different \(2a^2\) values in the chosen interval; for fixed \(a\), distinct even \(D\)'s are separated by more than the center variation. Finally distinct \(j\)'s give distinct centers. This is a count of the explicit family, not a density-one or arbitrary-target result.

```python
def norm(z):
    return sum(t*t for t in z)

def gg(z, w):
    while w != (0, 0):
        a, b = z
        c, d = w
        m = norm(w)
        u = (2*(a*c+b*d)+m)//(2*m)
        v = (2*(b*c-a*d)+m)//(2*m)
        z, w = w, (a-u*c+v*d, b-u*d-v*c)
    return z

f, a, D = 81, 82, 14
n = 1348083*f*f + 5**D + 2*a*a
z = [(x-y,x+y) for x,y in [(-a,639*f),(a,819*f),(-a,821*f)]]
assert n == 14948301636 and 91*a*f == 604422
assert all(norm(w) == n-3**c-5**D > 0 for c,w in zip((20,16,8),z))
assert norm(gg(z[0],z[1])) == norm(gg(z[0],(2,0))) == 2
assert norm(gg(z[1],z[2])) == norm(gg(z[1],(10,0))) == 10
```
