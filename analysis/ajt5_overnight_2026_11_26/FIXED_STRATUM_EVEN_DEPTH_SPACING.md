# Spacing between candidate depths in a fixed one-sided stratum

Keep the real labels, \(\Delta=5^b-3^a\ge0\), fixed \(S,D_0\), and the \(Y=109\) rough-part window of [the one-sided interval test](ONE_SIDED_FIXED_DEPTH_PRIME_INTERVAL.md). All candidates \(p^E\) use one common positive magnitude interval of endpoint ratio at most \(((U-1)/L)^2\), where \(L=127\cdot131,\ U=139\cdot151\). This is a necessary size window before solving the same-point CRT or checking the true norm.

If both \((p,E)\) and \((r,E+2j)\) pass the common size window for \(j\ge1\), then \(p>r\); otherwise the ratio in the other direction is at least \(r^2\ge49\), too large. Since the inert primes below 109 are \(3\bmod4\), one has \(r\le103\) and \(p/r\ge107/103\). Thus
\[
 \frac{p^E}{r^{E+2j}}\ge\frac{(107/103)^E}{103^{2j}}.
\]
If \(107^{E_0}L^2>103^{E_0+2h}(U-1)^2\), a hit at an even depth \(E\ge E_0\) rules out the next \(h\) even-depth slots. The choices \((E_0,h)=(256,1),(500,2),(744,3)\) give at most one candidate depth in each consecutive window of two, three, or four even depths, respectively. Combined with the earlier within-depth uniqueness, this gives the same bound for candidate primes counted with their depths. It applies only at fixed \(S,D_0\); changing either resets the common size window.

## Exact overlap before the cutoff

For actual labels \((0,755),(1106,0)\) and fixed \(S=3^{904}109^{45},D_0=5^{11}\), the adjacent even depths 254 and 256 give size-window candidates 107 and 103, respectively. Neither produces a same-point integer at the fixed smooth factors: both are too far from their required CRT residues. Thus one cannot move the **size-only** adjacent-depth exclusion earlier simply using this model. This is not a counterexample with two true norm certificates at adjacent depths.

```python
from math import isqrt
def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
L,U=127*131,139*151
for E,h in ((256,1),(500,2),(744,3)):
    assert 107**E*L**2>103**(E+2*h)*(U-1)**2
delta=5**755-3**1106
S,D0=3**904*109**45,5**11
assert delta>0
for e,expected,bounds in ((254,107,(16637,17026)),(256,103,(20974,20988))):
    matches=[]
    for p in range(7,110,4):
        if not prime(p):
            continue
        D=D0*p**e
        lo=max(L,(delta+S*L+D-1)//D)
        hi=min(U-1,(delta+S*(U-1))//D)
        if lo<=hi:
            matches.append(p)
            assert (lo,hi)==bounds
            assert all((D*w-delta)%S for w in range(lo,hi+1))
    assert matches==[expected]
```
