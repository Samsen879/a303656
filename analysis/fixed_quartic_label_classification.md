# Exactly three rational-function labels on each fixed quartic layer

Fix \(s\ge1\), \(A=9^s\), \(B=25^s\), \(z=A/B\), \(\rho=(2+i)^{2s}\), and \(H=A+125B\). Define
\[
p(t)=\frac12\bigl(-15t^2+(3z-147)t-38z+138,\ 
                    5t^2+(49-z)t+12z-16\bigr),\quad
P(t)=\rho\,p(t)
\]
using complex multiplication on the coordinate pair, and \(n(t)=H+N(P(t))\), \(N(x,y)=x^2+y^2\). Then
\[
n(t)-3^c-5^d\text{ is a sum of two squares in }\mathbb Q(t)
\quad\Longleftrightarrow\quad
(c,d)\in\{(2s,2s+3),(2s+1,2s+2),(2s+3,2s)\}.
\]
The statement is about rational-function identities at each fixed actual layer. A particular specialized integer may have more labels.

## Reduce to a quadratic pair and two branches

For a polynomial \(f\) represented as \(w\bar w\) with \(w\in\mathbb Q(i)(t)\), any conjugation-fixed monic irreducible has nonnegative valuation in \(w\); in each pair \(g,\bar g\) the two valuations sum to a nonnegative number. Multiplying \(w\) by a suitable power of \(g/\bar g\) makes both valuations nonnegative without altering the norm. Clear all such poles this way. The resulting polynomial has degree half the degree of \(f\), since its leading norm is positive. Here we may thus take degree at most two.

Normalize by \(\rho\) and rotate by a constant norm-one element of \(\mathbb Q(i)\) to match the leading coefficient of \(p(t)\). Put \(V=(-3,1)\), \(W=(1,3)\), \(d_*=50-z\), \(e_*=62-13z\), and \(g=(H-C)/(2B)\) for a candidate label \(C\). Write \(p=vt^2+wt+c_*\), where \(v=(5/2)V\), \(w=(d_*-1)V/2\), \(c_*\cdot W=d_*-5\) and \(c_*\cdot V=2d_*-5e_*-5\). The cubic coefficient forces the new point to be \(p+hWt+b\) with rational \(h,b\). If \(h=0\), comparison of the quadratic coefficient gives \(b=rW\) and \(g=r(d_*-5)+5r^2\). If \(h\ne0\), the quadratic and linear coefficients give \(V\cdot b=-2h^2\), \(W\cdot b=h(d_*-1)-d_*+5\). The constant coefficient gives
\[
20g=4h^4+(z^2-350z+3261)h^2-(d_*-5)^2.
\]
Conversely these equations supply the rational coordinates. The original three labels use \(p\), \(p+W\), and \(p+Wt+(1,1)\).

## Thirteen possible label sums

Let \(R=A^2-350AB+3265B^2\), \(M=(45B-A)^2+10B(H-C)\). In the first branch \(M\) must be an integer square. It satisfies \(M\equiv A^2\bmod5B\), \(0\le M<3275B^2\) and \(M\equiv0\bmod4\), since \(C\) is positive and even. The nonnegative root is \(x=\pm A+5Bk\) by the two unit square-root branches at 5. Bounds and parity force \(k=1,3,5,7,9,11\). These give twelve possible values \(C=(-8\mp k)A+(655-5k^2)B/2\).

In the second branch \(4B^2h^4+(R-4B^2)h^2=M\), so \(h^2<3275/2912\). If \(h\) is an integer only \(\pm1\) is possible, giving \(C=27A+B\). Otherwise, a negative valuation at any prime other than 5 makes the quartic term uniquely lowest; this also holds at 2 because \(v_2(R-4B^2)\ge3\), \(v_2(M)\ge2\). At 5 the quadratic and quartic terms must tie, since \(R-4B^2\) and \(M\) are units; hence \(h=a/B\) with \(5\nmid a\). Rearrangement implies the integer \(k=(4a^2+R-4B^2)/B^2\) satisfies \(M=ka^2\), \(4a^2=-A^2\bmod B\), and \(k=-4\bmod B\). The bounds give \(2912<k<3266\), impossible for \(s\ge3\). At \(s=1,2\), substitute the exact ratio \((R-4B^2)/B^2\) into \(k=(R-4B^2)/B^2+4h^2\), giving \(3136\le k\le3140\) and \(3216\le k\le3220\), respectively; neither interval has the required residue. Thus there are at most thirteen possible sums.

## Exact finite obstruction at all exponents, and uniqueness

The standard-library script below verifies that none of the ten extra candidate sums belongs to the set of all actual label residues modulo \(76310916361680\). It checks the periods including the independent zero-exponent cases, and exhausts the complete finite sets. That leaves the three displayed sums.

To see their unique exponent decompositions, let \((c_0,d_0)\) be one displayed pair. If another has \(c>c_0\), then \(d<d_0\) and \(v_3(5^{d_0-d}-1)=c_0\ge2s\); for a positive exponent at most \(2s+3\) this is impossible by LTE, with \(s=1\) checked at the only two even exponents 2 and 4. If \(c<c_0\), then \(d>d_0\) and \(v_5(3^{c_0-c}-1)=d_0\ge2s\); the only positive valuations occur at multiples of 4 and equal \(1+v_5((c_0-c)/4)\), strictly smaller, including \(s=1\). Equality of the first exponent forces equality of the second.

The same replay explicitly verifies four genuine representations at \(s=1,t=88974\). The fourth occurs at a specialization, not in \(\mathbb Q(t)\).

```python
"""Independent full-sum-set proof of the global native closure.

Does not import the constructor or the per-3-power lookup implementation.
"""
from math import prod
Q=240*prod((7,11,13,17,31,41,61,241))
assert Q==76310916361680
for b in (3,5):
    assert pow(b,241,Q)==b
    assert pow(b*b,121,Q)==b*b
left={(pow(3,c,Q)+pow(5,d,Q))%Q
      for c in range(241) for d in range(241)}
assert len(left)==56280
negative=((7,325),(9,325),(5,305),(11,305),(3,265),
          (13,265),(1,205),(15,205),(17,125),(19,25))
for s in range(1,121):
    A,B=pow(9,s,Q),pow(25,s,Q)
    assert all((b*B-a*A)%Q not in left for a,b in negative)
    assert all((a*A+b*B)%Q in left for a,b in ((1,125),(3,25),(27,1)))
print('PASS independent full residue set:',Q,len(left),'residues; zero exponents included')

n=97941657550601575485198
assert 25**16<n<9**32
rows=((2,5,-257310241780,-178137859608),(3,4,-257310241789,-178137859595),
      (5,2,-257311042547,-178136702939),(5,4,-71503461823,304678375501))
assert all(a*a+b*b+3**c+5**d==n for c,d,a,b in rows)
t=88974
B=25
A=9
px=A*(3*t-38)+B*(-15*t*t-147*t+138)
py=A*(-t+12)+B*(5*t*t+49*t-16)
assert (3*px-4*py,4*px+3*py)==tuple(2*B*v for v in rows[0][2:])
for s, lo, hi in [(1,3136,3140),(2,3216,3220)]:
    A,B=9**s,25**s
    c=A*A-350*A*B+3261*B*B
    assert (lo-1)*B*B <= c < lo*B*B
    assert 2912*(c-(hi+1)*B*B)+4*3275*B*B<0
    assert all((j+4)%B for j in range(lo,hi+1))
```
