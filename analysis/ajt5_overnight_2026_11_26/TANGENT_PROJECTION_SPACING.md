# Near-tangent projection spacing for actual norm points

This note gives a per-edge bound in a fixed-width scaled window; it is not a bound on the full third moment.

Fix positive scales \(A,B\), a bounded positive lattice denominator \(q\), an initial marked direction \((h,k)\) with \(h\ge0\), \(k\asymp B\), and a target \(n\). Consider actual third points \((x,y)\) in a fixed translate of the grid of mesh \(1/q\), where \(x\asymp A,\ y\asymp B\) are positive and \(x^2+y^2=n-s\) for shifts in a set of diameter \(R=o(\min(A,B))\). Set \(\Pi=q(ky-hx)\). Then distinct such points have \(\Pi\)-spacing \(\gg A\) uniformly even if they use different shifts.

**Proof.** If the horizontal coordinates agree, different \(y\)'s change \(y^2\) by \(\gg B\), impossible under the shift bound. Otherwise order the two points by \(x_1<x_2\), so \(x_2^2-x_1^2\gg A\). The identity
\[
 y_1^2-y_2^2=x_2^2-x_1^2+s_2-s_1
\]
gives \(y_1>y_2\) and \(y_1-y_2\gg A/B\). Thus \(\Pi_1-\Pi_2=q(k(y_1-y_2)+h(x_2-x_1))\gg A\). In particular, each window \(|\Pi|\le M_0 A\) for fixed \(M_0\) contains a bounded number of third points for a fixed marked edge, counting distinct points only.

For a base point \((a,b)\), write \(x=a-j/q,\ y=b+\ell/q,\ D=kj-h\ell\), and \(W=q(kx+hy)\), \(P=k^2+h^2\). Then
\[
 \Pi^2+W^2=q^2P(n-s),\qquad
 D-q(ka+hb-\sqrt{P(n-s)})
 =\frac{\Pi^2}{q\sqrt{P(n-s)}+W}.
\]
Under the positive-scale assumptions \(W\gg AB\), so the scaled window is within \(O(A/B)\) of its tangent determinant for the chosen third shift. This identity makes no global assertion about how many marked edges there are.

## Genuine three-point replay

At \(n=430366009736318019\), the shifts \((59074,59054,59174)=(3^{10}+5^2,3^{10}+5,3^{10}+5^3)\) have genuine points \((656022847,184256),(656022834,225847),(656022843,197986)\). The third point is in the tangent window \(|\Pi|<2^{29}\).

```python
from math import gcd
n=430366009736318019
ss=[3**10+5**d for d in (2,1,3)]
p=[(656022847,184256),(656022834,225847),(656022843,197986)]
assert all(n==x*x+y*y+s for (x,y),s in zip(p,ss))
(a,b),(v,w),(x,y)=p
h,k,j,l=a-v,w-b,a-x,y-b
D,Pi,W=k*j-h*l,k*y-h*x,k*x+h*y
assert (h,k,j,l,D,Pi)==(13,41591,4,13730,-12126,-293861233)
assert gcd(h,j)==gcd(k,l)==1 and abs(Pi)<2**29
assert Pi*Pi+W*W==(k*k+h*h)*(n-ss[2])
```
