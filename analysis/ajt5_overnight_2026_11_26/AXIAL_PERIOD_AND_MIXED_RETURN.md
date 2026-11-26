# True axial periods exceed the active box; a mixed-return criterion

For large real \(z\), let Q consist of primes \(q\equiv3\bmod4\), \(5<q\le z\), outside any fixed finite panel. Write \(T_b=\operatorname{lcm}_{q\in Q}\operatorname{ord}_q b\) for \(b=9,25\). Then
\[
 \log\gcd(T_9,T_{25})\gg z^{11/20}\log z.
\]
In particular, neither separate first return to 1 can fit in the actual axis of length \(O(z^2)\) when \(z=\sqrt{\log X}\). The analogous periods modulo \(q^2\) can only increase. This controls separate returns, not mixed additive cancellation.

## Proof of the common prime-factor bound

Use the inert primes \(z/2<q\le z\) and decompose their \(\log(q-1)\) into the \(\log\ell\) weights of prime powers dividing \(q-1\). By PNT in progressions the total weight is \((1+o(1))z/4\). For primes \(\ell\le z^{49/100}\) the first-power weight is \((49/100+o(1))z/4\), by [Bombieri–Vinogradov](https://www.cambridge.org/core/journals/mathematika/article/abs/on-the-large-sieve/4AE92826645F6F3393D30AF0D2767346) applied to the interval and the single CRT class \(3\bmod4,\ 1\bmod\ell\). The prime 2 contributes only \(O(z/\log z)\). More explicitly, the main term for odd \(\ell\) is \((\operatorname{li}(z)-\operatorname{li}(z/2))/(2(\ell-1))\); the weighted aggregate error is \(o(z)\), and \(\sum_{\ell\le y}\log\ell/(\ell-1)\sim\log y\).

For \(z^{49/100}<\ell\le z^{11/20}\), [interval Brun–Titchmarsh](https://doi.org/10.1112/S0025579300004708) bounds the count in the same class by \(z/(2(\ell-1)\log(z/(8\ell)))\). Summing with weight \(\log\ell\) makes this at most \((2(0.55-0.49)/(1-0.55)+o(1))z/4\). Higher powers \(\ell^j\), \(j\ge2\), contribute \(o(z)\): for powers up to \(\sqrt z\) apply Brun–Titchmarsh with modulus \(4\ell^j\) and use convergence of \(\sum_{\ell,j\ge2}\log\ell/\varphi(\ell^j)\); for larger powers the trivial count \(z/\ell^j+1\) suffices, by convergence of the analogous tail and \(O(\sqrt z\log z)\) possible powers. For \(\ell=2\) there is no higher power under \(q\equiv3\bmod4\). The first two bounds add to \(227/300+o(1)\) of the total, leaving \(\gg z/\log z\) primes q with a factor \(\ell>z^{11/20}\) of \(q-1\); such a factor is unique for each q.

If \(\operatorname{ord}_q b\) omitted this factor, the order would be at most \(z^{9/20}\). All such q divide \(\prod_{j\le z^{9/20}}(b^j-1)\), whose log is \(O(z^{9/10})\). Thus only \(O(z^{9/10}/\log z)\) primes q are lost for either b. Each remaining \(\ell>z^{11/20}\) can recur for at most \(O(z^{9/20}/\log z)\) such primes q. For this uniform bound use Brun–Titchmarsh with modulus \(4\ell\) when \(\ell\le z^{9/10}\), and the trivial bound \(z/\ell+1=O(z^{1/10})\) otherwise. Hence at least \(\gg z^{11/20}\) distinct primes \(\ell\), each of log \(\gg\log z\), occur in both periods.

## Exact mixed criterion, and one finite box

With \(n=2+u^2+v^2\) and any fixed compatible panel, a cell \((i,j)\) with offset \(9^i+25^j\) evades every external valuation-one certificate for **all** legal external phases iff
\[
   9^i+25^j\equiv2\pmod{\prod_{q\in Q}q^2}.
\]
At an inert q the possible norm residues modulo \(q^2\) are all units and 0. If \(\delta=9^i+25^j-2\) is a unit, choose \(\delta+q\). If it has valuation one, choose 0. In each case there is a legal phase giving exact valuation one, realizable along with the remaining phases at suitable real height by the [previous CRT construction](PROPORTIONAL_BOX_EXTERNAL_COVER.md). If \(\delta=0\bmod q^2\), no legal phase hits. This criterion concerns the same **universal** cell across phases; a different cell can survive for each phase. Any non-origin universal mixed return must have both axes positive inside the active box by the period bound, and satisfies \(\max(i\log9,j\log25)\ge (1+o(1))z\) by divisibility and the prime number theorem in progressions. This is below the available \(O(z^2)\) scale.

For \(z=\sqrt{\log(2^{1024})}\) and fixed panel \((3,43,79,223)\), Q is \((7,11,19,23)\). In the specified \(323\times221\) exponent-index box there are non-origin mixed returns modulo the prime product, but none modulo the squared product. This is a finite control, not a proof of uniform nonexistence.

~~~python
from math import lcm,prod
Q=(7,11,19,23)
def order(b,m):
    a,n=b%m,1
    while a!=1:
        a,n=a*b%m,n+1
    return n
for e,T,expected in [(1,495,[(0,0),(45,180),(261,54)]),
                     (2,1514205,[(0,0)])]:
    assert all(lcm(*(order(b,q**e) for q in Q))==T for b in (9,25))
    m=prod(q**e for q in Q)
    got=[(i,j) for i in range(323) for j in range(221)
         if (pow(9,i,m)+pow(25,j,m)-2)%m==0]
    assert got==expected
~~~
