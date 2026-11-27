# Only exact-lift rows need to enter the witness compression periods

For an original \(3,5\) finite panel of \(s\) inert primes greater than 3, fix nonnegative forward bounds \(c\ge C,d\ge D\) and compatible natural seed moduli \(m_3,m_5\). Assume a strictly positive residual witness exists with each panel valuation 0 or 2. Let \(H\) be precisely the rows of valuation 2 for that witness and put
\[
 P_b=\operatorname{lcm}\bigl(m_b,\{\operatorname{ord}_{p^2}(b):p\in H\}\bigr).
\]
There is a new positive witness of the same unit/exact-two type with each exponent at most its original value and increments from the starting bounds strictly less than \(2^sP_b\). No unit row is needed in \(P_b\). The result compresses a witness once one is available; it does not show how to choose a low-cost \(H\) for an arbitrary input.

On one axis keep the original class modulo \(P_b\), leaving the other exponent fixed. If a row is a unit, a mod-prime collision forbids at most one class of the free parameter in the actual multiplicative period (or no class). For a row in \(H\), the residual stays zero modulo \(p^2\); the forbidden depth-\(\ge3\) condition is affine in the free parameter mod \(p\), because \(b^{P_b}=1\bmod p^2\). A constant condition must already pass, since the original parameter passes. Thus each row forbids at most one residue class \(a_i\bmod m_i\). Their complement indicator can be detected by the nonvanishing of \(\prod_i(1-\zeta_{m_i}^{x-a_i})\), which is a sum of at most \(2^s\) distinct exponential frequencies and is not identically zero. The Vandermonde identity forbids a run of \(2^s\) consecutive zeros. Starting from the least forward representative gives a passing parameter within the budget, or retain the original if already smaller. Repeat for the other exponent after the first compression; the current point already passes at that step. The new exponents do not exceed the original, which preserves strict positivity. If \(H\) is empty each axis needs at most \(2^s-1\) seed steps; generally \(P_b\le m_b\prod_{p\in H}p^2\).

## Exact two-row control

For \(Q=\{7,1006003\}\) choose
\[
 n=3^{46}+1+7452015604202281^2+7406123619975220^2.
\]
From \((4,0)\) the valuations are \((3,1)\). At \((46,0)\) they are \((2,0)\), with true square coordinates as displayed. Only row 7 supplies exact-lift periods, both equal to 42. The bad final digit for the 7 row on \(c=4+42i,d=42j\) is precisely \(3i+6j=0\bmod7\). At the other row base 3 has higher than ordinary initial depth, while base 5 is ordinary; nonetheless no period of 1006003 is needed for the compression of this particular witness.

```python
from math import isqrt
def v(r,p):
    j=0
    while r%p==0:
        r//=p; j+=1
    return j
p=1006003
assert all(p%d for d in range(2,isqrt(p)+1))
assert pow(3,p-1,p*p)==1 and pow(5,p-1,p*p)!=1
assert all(next(k for k in range(1,49) if pow(b,k,49)==1)==42 for b in (3,5))
n=3**46+1+7452015604202281**2+7406123619975220**2
assert [tuple(v(n-3**c-1,q) for q in (7,p)) for c in (4,46)]==[(3,1),(2,0)]
for i in range(7):
    for j in range(7):
        r=(n-pow(3,4+42*i,343)-pow(5,42*j,343))%343
        assert r%49==0 and (r==0)==((3*i+6*j)%7==0)
```
