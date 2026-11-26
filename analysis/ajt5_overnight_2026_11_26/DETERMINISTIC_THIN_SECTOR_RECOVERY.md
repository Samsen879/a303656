# Deterministic thin-sector recovery with positive lower density

For dyadic \(X\), put \(T=\lfloor X^{1/4}\rfloor,\ L=1+\lfloor\log_2 X\rfloor,\ K=\lceil T/L^2\rceil\), and \(w=K/T\). Use the distinct shifts \(s=3^c+5^d\) with \(X^{1/4}\le3^c\le X^{1/3}\), \(5^d\le X^{1/8}\), and \(c,d\ge0\). There are \(\asymp(\log X)^2\) shifts: the minimum separation between first-axis powers exceeds the entire second-axis range. There is an absolute \(\delta>0\) such that for every sufficiently large block \([X,2X)\), at least \(\delta X\) integers have a true **squarefree** residual \(n-s=a^2+b^2\) with \(0\le b<wa\). Thus the first \(K\) consecutive slope bands of width \(1/T\) work, with no random seed or offline optimization. The proof does not compute \(\delta\) or the starting height.

## First moment

For each shift the sector \(X-s\le a^2+b^2<2X-s,\ 0\le b<wa\) has area \(\asymp Xw\) and boundary length \(O(\sqrt X)\). For \(p^2\mid a^2+b^2\), the excluded coordinate pairs lie in one square lattice of spacing \(p\) when \(p=2\) or \(p\equiv3\bmod4\), and in the union of at most three rotated such lattices when \(p\equiv1\bmod4\). The latter follows from the Gaussian ideals \((p),(\pi^2),(\bar\pi^2)\) when \(p=\pi\bar\pi\); the inert and ramified cases require both coordinates divisible by \(p\). Tiling the plane by squares of side \(p\) bounds the lattice count by area divided by \(p^2\), with error \(O(1+\sqrt X/p)\) from cells meeting the circular or straight edges. Only \(p\le\sqrt{2X}\) matter. The total area fractions excluded are bounded above by \(1/4+1/9+3\sum_{m\ge5,\,m\text{ odd}}m^{-2}\le703/900\), by the integral bound on the tail. Total boundary error is \(O(\sqrt X\log X)=o(Xw)\). Thus each shift contributes \(\gg Xw\) valid coordinate pairs, and the sum of witness counts is \(\gg X\).

## Second moment

If \(n=s+a^2+b^2=s'+a'^2+b'^2\), set \(h=a'-a,\ k=b'-b,\ \Delta=s-s'\). Then \((a'+a)h+(b'+b)k=\Delta\). In the sector, \(a,a'\asymp\sqrt X\), \(b,b'=O(w\sqrt X)\), and \(|\Delta|=O(X^{1/3})\). If \(h\ne0\), then \(|h|\ll w|k|\), since the scaled \(\Delta\) contributes only \(O(X^{-1/6})\). For \(g=\gcd(h,k)\), we have \(g\mid\Delta\). The primitive direction has vertical size \(v=|k|/g\ll w\sqrt X/g\); there are \(O(wv)\) nonzero horizontal choices for each \(v\). The corresponding line has \(O(1+\sqrt X/v)\) lattice points in the range of the first coordinate. Summing over \(v\) gives \(O(Xw^3/g^2+Xw^2/g)\). For distinct shifts this is \(O(Xw^2\sigma_{-1}(|\Delta|))\) after summing \(g\). At \(h=0,\ \Delta\ne0\), the factorization \((b'-b)(b'+b)=\Delta\) gives \(O(\sqrt X\sqrt{|\Delta|})=O(X^{2/3})\) possibilities. The equal-shift cases contribute \(O(Xw)\) per shift from identical coordinates, and \(O(Xw^2\log X)\) per shift from nonzero directions, by summing over all \(g\).

For clarity, the nonzero shift gaps have mean \(\sigma_{-1}\) bounded uniformly. Absorb the 5-part of each gap in a factor at most \(5/4\). For \(q\) coprime to 5, fixing three of the four exponents leaves at most one class for the fourth base-5 exponent mod \(\operatorname{ord}_q5\). With \(U=\log X\), the collision count is \(O(U^4/\operatorname{ord}_q5+U^3)\). For \(q\le e^{\sqrt U}\), the endpoint contributions weighted by \(1/q\) total \(O(U^{7/2})\). The order series \(\sum_{(q,5)=1}1/(q\operatorname{ord}_q5)\) converges: moduli of order at most \(J\) divide \(\prod_{j\le J}(5^j-1)\), whose log is \(O(J^2)\); the sum of reciprocals of its divisors is \(O(\log(3J))\) by splitting its Euler product at its log and applying Mertens. For the excluded \(q>e^{\sqrt U}\), the sum of \(1/q\) over divisors of each nonzero \(\Delta\) is at most \(U^{-1/2}\sum_{q\mid\Delta}(\log q)/q=o(1)\): this last log-weighted divisor sum is \(O((\log\log(3|\Delta|))^2)\), by the product bound \(\sigma_{-1}(|\Delta|)\sum_{p\mid\Delta}(\log p)/(p-1)\) and splitting the prime factors at \(\max(2,\log|\Delta|)\). Hence the off-diagonal gap-factor sum is \(O((\log X)^4)\).

Consequently \(\sum_n Z(n)^2=O(X)\) for sector witness count \(Z(n)\). Cauchy–Schwarz proves the positive proportion. Neither the squarefreeness requirement nor the sector restriction is necessary for the original conjecture, and the proof does not yield density one or a pointwise result.

## Scan cost, matching menu lower bound, and controls

Given \(n\), for each shift check the integers \(a\) with \((n-s)/(1+w^2)<a^2\le n-s\), and test the remaining square. This takes \(O(\sqrt X/(\log X)^2+(\log X)^2)\) **coordinate** checks; squarefree certification costs separately. Any shared menu of \(k\) slope bands of width \(1/T\) covers at most \(O(kX(\log X)^2/T)\) targets, since each band contains \(O(X/T+\sqrt X)\) lattice points of norm at most \(2X\), and each coordinate pair combines with \(O((\log X)^2)\) legal shifts. Thus \(K\)'s order of magnitude is necessary within this shared-band model.

At \(X=2^{19}\), \(T=26,\ K=1\), the rule finds \(524289=724^2+9^2+3^3+5\), whose residual is prime. The integer \(524341=722^2+55^2+3^3+5\) also has a prime residual, but that coordinate lies in the second band and the first band finds no positive residual witness even over all legal shifts.

```python
from math import isqrt
X=2**19
T=isqrt(isqrt(X))
assert T==26
def offsets(n):
    a=1
    while a+1<n:
        b=1
        while a+b<n:
            yield a+b
            b*=5
        a*=3
def witness(n,s,T):
    r=n-s
    lo=isqrt(r*T*T//(T*T+1))+1
    for a in range(lo,isqrt(r)+1):
        b=isqrt(r-a*a)
        if b*b==r-a*a and b*T<a:
            yield a,b
def prime(r):
    return r>1 and all(r%d for d in range(2,isqrt(r)+1))
assert list(witness(524289,32,T))==[(724,9)]
assert 524341-32==722**2+55**2 and 722<=55*T<2*722
assert all(prime(n-32) for n in (524289,524341))
assert all(not list(witness(524341,s,T)) for s in offsets(524341))
```
