# Two rationally related thin sectors carry a common-residual correlation

Use the shift set \(S_X\) from [thin-sector recovery](DETERMINISTIC_THIN_SECTOR_RECOVERY.md). Compare the near-axis sector \(0\le b<wa\) to its image under a fixed unit rotation \(\rho=\alpha/\beta\) with coprime Gaussian \(\alpha,\beta\). Choose a fixed small upper width to make the sectors disjoint in the first quadrant. Write \(D=N(\alpha)=N(\beta)\). Count actual integers \(n\in[X,2X)\) admitting a shift and a squarefree sum-of-two-squares residual within each sector, and write \(B\asymp Xw(\log X)^2\) for either sector's coordinate-count main term. For fixed \(\epsilon>0\) and \(X^{-1/2+\epsilon}\le w=o((\log X)^{-2})\), both hit sets have size \((1+o(1))B\), and their intersection has size \((f(D)+o(1))B\), where
\[
f(D)=\begin{cases}
\prod_{p\mid D}(p+2)^{-1},&D\text{ squarefree},\\
0,&\text{otherwise}.
\end{cases}
\]
This is specific to the stated thin sectors, not a result about the conjecture's overall miss rate. In this range even the union has density tending to zero.

An exact matching pair at the same shift needs \(z\in\beta\mathbb Z[i]\). Equal norms and Gaussian coprimality exclude inert and ramified divisors of \(D\). If \(p^2\mid D\), every such coordinate has nonsquarefree norm. Otherwise, at each split \(p\mid D\), the Gaussian prime dividing \(\beta\) occurs exactly once and its conjugate is absent. Its local density in all coordinate pairs is \(p^{-1}(1-p^{-1})^2\), compared to \((1-p^{-1})^2(1+2/p)\) for squarefreeness at \(p\). Their ratio is \(1/(p+2)\). A fixed finite cutoff gives these products by CRT, with main term proportional to sector area, including for the rotated sector. Larger primes remove at most \(O(Xw/P+\sqrt X\log X)\) coordinates using the square-lattice count in the linked note; take \(X\) large and then let the fixed \(P\) grow. The product of squarefree local densities is positive. The Gaussian coincidence lattice background is described by [Baake](https://arxiv.org/abs/math/0605222).

To bound pairs other than exact matches, map the coordinates to \(Dz\) and \(D\rho^{-1}z'\), both integer points in a near-axis sector. Their squared norm gap is \(D^2(s-s')=O_\rho(X^{1/3})\). With nonzero horizontal difference, the line argument of the linked note bounds each gcd contribution by \(O_\rho(Xw^3/g^2+Xw^2/g)\). For different shifts, average the divisor factor as in that proof; the fixed \(D^2\) adds only a bounded factor. For equal shifts, summing over all \(g\) and the \(O((\log X)^2)\) shifts costs \(O_\rho(Xw^2(\log X)^3)\). At zero horizontal difference and unequal shifts the vertical difference of squares factors, costing \(O_{\rho,\eta}(X^{1/2+\eta}(\log X)^4)\) for any \(\eta>0\), using the standard divisor estimate \(O_{\eta}(X^\eta)\) and the at most \(O(\sqrt X)\) horizontal choices. A zero gap and zero horizontal difference gives identical transformed coordinates, hence an exact rotation match. The total nonmatching count is \(O_{\rho,\eta}(Xw^2(\log X)^4+X^{1/2+\eta}(\log X)^4)=o(B)\) for \(\eta<\epsilon\). The same argument with the identity shows multiple witnesses inside each sector contribute only \(o(B)\), so coordinate counts transfer to hit counts.

## Exact controls

For \((4+3i)/5\) the overlap coefficient is \(1/7\); for \((24+7i)/25\) it is zero because the denominator norm after Gaussian reduction is 25. At \(X=2^{19}\) the shifts are 28 and 32. Exact controls:
- \(528562=727^2+1^2+32=581^2+437^2+32\), first rotation and squarefree residual.
- \(552082=743^2+1^2+32=713^2+209^2+32\), second rotation and residual divisible by 25, so this exact pair is discarded by squarefreeness.
- \(527397=726^2+17^2+32=580^2+437^2+28\), distinct squarefree residuals. Both coordinates are within the sectors for \(w=1/32\); such pairs are not the exact-rotation main term.

```python
from math import isqrt
def sqf(n):
    return all(n%(d*d) for d in range(2,isqrt(n)+1))
def pair(n,a,b,c,d,s,t):
    assert a*a+b*b+s==c*c+d*d+t==n
    return sqf(n-s),sqf(n-t)
assert ((4*727-3)//5,(3*727+4)//5)==(581,437)
assert pair(528562,727,1,581,437,32,32)==(True,True)
assert ((24*743-7)//25,(7*743+24)//25)==(713,209)
assert pair(552082,743,1,713,209,32,32)==(False,False)
assert (552082-32)%25==0
assert pair(527397,726,17,580,437,32,28)==(True,True)
for p,u,v in [(5,2,1),(13,3,2)]:
    all_good=on_lattice=0
    for a in range(p*p):
        for b in range(p*p):
            if (a*a+b*b)%(p*p):
                all_good+=1
                on_lattice+=(u*a+v*b)%p==0
    assert all_good==(p+2)*on_lattice
```
