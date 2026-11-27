# Positive lower density of true squarefree residuals on a two-power grid

There exist absolute \(a,b>0\) such that every sufficiently large \([X,2X)\) contains at least \(aX\) integers \(n\equiv107\bmod196\) with at least \(b(\log X)^{3/2}\) distinct active exponent pairs \((c,d)\) for which \(n-3^c-5^d\) is positive, squarefree, and a genuine sum of two squares. The set of integers with this property has positive lower natural density; each has \(v_7(n-2)=1\), so \((0,0)\) fails. This result counts actual norms over an ordinary interval, rather than members of [an explicit moving cofactor progression](COFACTOR_FAMILY_POSITIVE_PROPORTION.md). It does not show density one, and it makes no claim of priority.

Use \(c=2e,d=2f\) with \(e,f\equiv1\bmod21\) and
\[
X^{1/8}\le9^e\le X^{1/4},\qquad X^{1/3}\le25^f\le X^{1/2}.
\]
Each axis has \(\asymp\log X\) indices, all offsets \(s_{ef}=9^e+25^f\) are \(34\bmod196\), and the offsets are distinct: the minimum gap between different second-axis powers exceeds the entire first-axis range for large \(X\). The whole grid is active even in the box with both powers below \(n/4\). Denote the count of squarefree-norm residuals by \(r(n)\), restricted to \(n\equiv107\bmod196\) in \([X,2X)\).

## First moment

There are \(\gg X/\sqrt{\log X}\) positive squarefree norms congruent to \(73\bmod196\) in \([X,3X/2)\). To construct them, take \(u=Av\) with \(A\) a squarefree product of primes \(p\equiv1\bmod4,\ p\le X^\delta\), and \(A\le X^{1/4}\). By [Williams' Mertens theorem in progressions](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf), the unrestricted harmonic weight of these products is \(\gg\sqrt{\log X}\) for any fixed \(\delta>0\). The normalized harmonic weight has mean \(\log A = \sum_{p}\log p/(p+1)=O(\delta\log X)\), by partial summation of the prime upper bound. For sufficiently small fixed \(\delta\), at least half the weight is on \(A\le X^{1/4}\). For each such \(A\), the prime number theorem in fixed arithmetic progressions gives \(\gg X/(A\log X)\) primes \(v\in[X/A,3X/(2A))\) in the unit class \(73 A^{-1}\bmod196\). This class is \(1\bmod4\), and \(v>\sqrt{2X}\), so \(u\) is squarefree and counted only once. Adding any offset to these \(u\)'s gives allowed \(n\), since the largest offset is \(o(X)\). Thus \(\sum r(n)\gg X(\log X)^{3/2}\).

## Second moment: average the gap factor on one actual axis

For distinct offsets, write \(h=s_{ef}-s_{e'f'}\ne0\). The pair count, even without squarefreeness or the target residue condition, is
\[
 \ll \frac X{\log X} C(h),\qquad C(h)=\prod_{p\mid h,\ p\equiv3(4)}(1+1/p).
\]
This is Rieger's pair upper bound (1965), in the uniform form recorded in Theorem 3.2 of [Kurlberg and Ueberschär](https://arxiv.org/pdf/1311.1396#page=8). Alternatively the local factors of the [direct uniform pair sieve](COFACTOR_FAMILY_POSITIVE_PROPORTION.md) give this bound; one may drop the mod-196 restriction, assign variable \(n\) directly, and omit \(7\) at a constant cost.

Drop the factor at \(3\) at cost at most \(4/3\), and expand the product over squarefree inert divisors \(m\le2\sqrt X\) coprime to \(3\). Fix \(f,e',f'\). For each \(m\) the divisibility condition restricts \(i=(e-1)/21\) to at most one class modulo \(\operatorname{ord}_m(9^{21})\), even when the other terms are not a unit modulo \(m\) (in that case there is no class). For \(m=1\) use order one. A class meets the actual consecutive index interval at most \(1+O(\log X)/\operatorname{ord}_m(9^{21})\) times. The endpoint errors sum to \(O(\log X)\) using the weights \(1/m\).

The series \(\sum_m 1/(m\operatorname{ord}_m(9^{21}))\) converges on these squarefree inert \(m\). In fact the \(m\)'s of order at most \(T\) all divide \(P_T=\prod_{1\le j\le T}(9^{21j}-1)\), with \(\log P_T=O(T^2)\). The sum of their reciprocals is at most \(\prod_{p\mid P_T,\ p\equiv3(4)}(1+1/p)\ll\sqrt{\log(3T)}\): split the product at \(\max(2,\log P_T)\), apply Mertens to the small primes, and bound the total reciprocal contribution of the large primes using the number of prime divisors and \(\log P_T\). Dyadic summation in the order proves convergence. Thus each fixed triple contributes \(O(\log X)\) to the sum of \(C(h)\), and the full off-diagonal sum of gap factors is \(O((\log X)^4)\). The diagonal contribution to \(\sum r(n)^2\) is bounded by \(O(X(\log X)^2)\) even without the norm condition. It follows that \(\sum r(n)^2\ll X(\log X)^3\). Removing rows below a sufficiently small multiple of \((\log X)^{3/2}\) retains a sum \(\gg X(\log X)^{3/2}\); Cauchy–Schwarz proves the asserted number of rows. Applying it on dyadic blocks yields positive lower natural density.

## True controls and a fixed-class obstruction

At \(X=10^4\) the label \((c,d)=(2,2)\) is eligible. At \(n=11279\) it leaves \(11245=106^2+3^2=5\cdot13\cdot173\). At \(n=12063\) the same label leaves \(12029=23\cdot523\), which is squarefree and passes the inert cutoff \(p\le\sqrt{\log n}\) but has two larger odd valuations. Both are in the stated class and have \(n-2\equiv7\bmod49\). More generally, if \(n\equiv1\bmod9\) in the same mod-196 class, every grid residual has \(v_3=1\) since \(25^f\equiv7\bmod9\). This rules out density one for this fixed grid, not for all exponent choices. A square factor common to two different residuals also divides their gap: \(D^2\mid h\) implies \(D^2\le2\sqrt X\), so the common-square route cannot compress either residual below order \(\sqrt X\) on this grid.

```python
from math import isqrt, log

def factors(n):
    out = []
    for d in range(2, isqrt(n) + 1):
        while n % d == 0:
            out.append(d)
            n //= d
    return out + ([n] if n > 1 else [])

assert pow(9,21,196) == pow(25,21,196) == 1
assert pow(25,1,9) == 7 and pow(25,21,9) == 1
for n,w in ((11279,[5,13,173]),(12063,[23,523])):
    assert n % 196 == 107 and (n-2) % 49 == 7
    assert factors(n-34) == w and len(w) == len(set(w))
assert 11279-34 == 106**2+3**2 and 3*3 < log(12063) < 7*7
assert (12063-34)%3 != 0
```
