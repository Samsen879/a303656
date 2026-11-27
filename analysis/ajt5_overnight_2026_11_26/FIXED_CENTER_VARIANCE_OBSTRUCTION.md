# An omitted inert prime forces nonvanishing centered variance

Fix a modulus \(4\mid M\), an integer class \(N\bmod M\), exponent classes \(c\equiv c_0\bmod L_3,d\equiv d_0\bmod L_5\), and a fixed two-axis grid whose consecutive index intervals grow as \(\asymp\log X\) (for example, the separated power ranges in [the direct density note](TWO_AXIS_SQUAREFREE_POSITIVE_DENSITY.md)). Assume all offsets \(s=3^c+5^d\) in these exponent classes agree modulo \(M\), that \(N-s\) is a unit modulo \(M\) and \(1\bmod4\), and that the offsets are \(o(X)\) uniformly. The same result applies after division by an exactly fixed admissible factor if the resulting class is a unit and \(1\bmod4\) in a fixed modulus. Let \(Z_X\) count **all** true two-square residuals at the grid's labels on \(n\in[X,2X)\), \(n\equiv N\bmod M\), with mean \(\mu_X\).

For any fixed inert \(q\nmid M\), let \(P_q(a)\) be the fraction of cells on the product of the two complete local cycles whose offset equals \(a\bmod q\). These cycles have lengths \(\operatorname{ord}_q(3^{L_3})\) and \(\operatorname{ord}_q(5^{L_5})\). Then
\[
 \frac{\mathbb E[Z_X\mid n\equiv a\bmod q]}{\mu_X}
 \longrightarrow 1+\frac1q-P_q(a).
\]
In particular
\[
 \liminf_X \frac{\operatorname{Var}(Z_X)}{\mu_X^2}
 \ \ge \frac1q\sum_{a\bmod q}(P_q(a)-1/q)^2>0.
\]
All means and variances are on the progression \(n\equiv N\bmod M\).

For the proof, use [Prachar's fixed-modulus reduced-class asymptotic, recorded in §1A](https://arxiv.org/pdf/2111.12662#page=1). For a single offset with \(a\not\equiv s\bmod q\), imposing \(n\equiv a\bmod q\) introduces a unit class at \(q\). The unnormalized count is multiplied to first order by \((1+1/q)/q\), hence its *conditional* mean by \(1+1/q\). When \(a\equiv s\bmod q\), a norm divisible by the inert prime must be divisible by \(q^2\); conversely multiplication of a norm by \(q^2\) preserves normhood. After this division the quotient is in the transformed reduced class modulo \(M\) and the interval's length is divided by \(q^2\). This conditional mean is multiplied by \(1/q\). The offsets displace endpoints by \(o(X)\), uniformly; the reduced-class asymptotic gives uniform leading terms over their finite residue possibilities and endpoints tending to the fixed ratios. The two axial intervals approach uniform counts over each fixed cycle as their lengths grow. Summing the per-offset first moments, and using the variance of the conditional mean, proves the result. Strict positivity follows because the product of the local periods divides \((q-1)^2\), so an exactly uniform table of \(q\) categories is impossible.

The obstruction comes from fixed-modulus first moments, with no assumed pair asymptotic. In the separated two-axis setting the already verified Rieger pair bound gives the matching order upper bound. A normalized fixed real linear combination of finitely many such offset distributions cannot be uniform at all omitted \(q\) either: uniformity for each \(q\), together with weights summing to one, is a linear system of rational constraints in finitely many unknowns. If a real solution exists, a finite set of independent equations gives a rational solution that satisfies the whole system. Choose \(q\) not dividing the denominators of those weights or \(M\). Each period table has denominator coprime to \(q\), so their rational weighted sum cannot be \(1/q\). These arguments disprove a normalized variance tending to zero under fixed centering, not density one by other methods and not the original pointwise conjecture.

## Exact local replay

Take \(M=672,\,N=527,\,c,d\equiv2\bmod24\), \(q=11\). The table counts are \((0,2,3,2,2,2,3,3,3,2,3)\) with denominator 25, giving \(18/15125\) in the displayed lower bound. Both \(n=11279,16655\) lie in the same mod-672 class and admit the label \((2,2)\). The residuals respectively give \(106^2+3^2\) and \(11\cdot1511\) with both factors inert and valuation one.

```python
from fractions import Fraction
from math import gcd, isqrt
assert pow(3,26,672)==pow(3,2,672) and pow(5,24,672)==1
assert gcd(527-34,672)==1
counts=[0]*11
for i in range(5):
    for j in range(5):
        counts[(pow(3,2+24*i,11)+pow(5,2+24*j,11))%11]+=1
assert counts==[0,2,3,2,2,2,3,3,3,2,3]
assert sum((Fraction(k,25)-Fraction(1,11))**2 for k in counts)/11==Fraction(18,15125)
assert 11279%672==16655%672==527
assert 11279-34==106**2+3**2 and 16655-34==11*1511
assert 1511%4==3 and all(1511%d for d in range(2,isqrt(1511)+1))
```
