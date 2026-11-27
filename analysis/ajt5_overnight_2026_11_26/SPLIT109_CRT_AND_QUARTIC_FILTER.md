# A fixed split prime gives a unique CRT candidate and a quartic obstruction

Use the negative cross-sum setting of [the fixed-place obstruction](ASYMMETRIC_FIXED_PLACE_HEIGHT_OBSTRUCTION.md). Put \(X=3^u,Z=5^v,\Delta=Z-X,\ R_s=n-1-Z,\ R_d=n-1-X\). Assume matched high powers, odd \(n\), both residuals positive, and \(n<X+Z\). The fixed support is \(S=\{2,3,5,109\}\), with a single additional inert panel prime \(p\). The candidate requirements include \(f=v_{109}(R_s)\), \(t=v_p(R_s)=v_p(\Delta)<E=v_p(R_d)\), and both \(t,E\) even. Let the positive rough parts satisfy the strong product window and \(w_sw_d=O(Y^4)\).

## Uniqueness on a specified label and valuation tuple

Suppose \(109^f\ge n^\eta,\ p^t\le n^\tau,\ Y\le n^\gamma\), with \(\tau+4\gamma<\eta\). The fixed-support rough-product theorem gives
\[
 p^E109^f\gg_{S,\epsilon}n^{1+\eta-\tau-4\gamma-\epsilon}.
\]
For sufficiently large targets and small fixed \(\epsilon\), the modulus exceeds the entire eligible interval length and the relevant residual heights. Thus a prescribed tuple \(u,v,p,E,f\) leaves at most one \(n\). Its deep residual has to be \(p^E r\), where \(r\) is the least nonnegative residue of \(\Delta (p^E)^{-1}\bmod109^f\); discard zero or values outside the ordinary height interval. On a dyadic block with fixed comparison constants, there are only \(O(1)\) possible labels \(u,v\), since the high powers are both comparable to \(n\). Enumerating the two valuation depths and the one additional prime therefore leaves \(O(Y_{\max}(\log n)^2)\) targets. The bound allows sparse infinite families.

## Quartic filter independent of unknown base-prime depths

Write \(d=v_{109}(\Delta)\). If \(f>d\), the deep residual has \(v_{109}=d\), and \(R_d/109^d\equiv\Delta/109^d\bmod109\). At mod 109 we have \(3^{54}=5^{27}=1\). Since \(n\) is odd and \(v_3(R_d)\) is even in the stated panel, taking 27th powers removes the unknown 3- and 5-factors, leaving
\[
 w_d^{27}(p^{54})^{E/2}\equiv(\Delta/109^d)^{27}\pmod{109}.
\]
When \(p\) is a square modulo 109 this is a quartic-coset condition for \(w_d\), stronger than the quadratic character condition. It is necessary, not sufficient.

## Reproducible label controls

At \((0,180),(264,0)\), the additional prime \(p=7\) has \(t=2\) on the gap and is a square mod 109. With \(Y=109\), the coprime rough parts \(16637,16649\) pass both strict product conditions, but \(16649\) is a quartic residue while the gap's quartic character is \(-1\). They cannot supply the requested deep side. At \(E=80,f=29\), the least CRT candidate for the deep residual exceeds twice its allowed upper bound.

```python
from math import gcd,isqrt
X,Z=3**264,5**180
D=Z-X
assert D%49==0 and D%343!=0 and D%109!=0
assert pow(D,27,109)==108 and pow(7,54,109)==1
a,b=16637,16649
assert gcd(a,b)==1 and 127*131<=a<=b<139*151
assert a*b<127*131*139*151
assert b%4==1 and all(b%d for d in range(2,isqrt(b)+1))
assert pow(b,54,109)==1 and pow(b,27,109)==1
r=(D*pow(7**80,-1,109**29))%(109**29)
assert 7**80*r>2*(Z-1)
```
