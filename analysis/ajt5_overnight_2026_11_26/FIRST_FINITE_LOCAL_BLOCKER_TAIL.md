# Summable tail for the first finite local blocker

Fix a healthy phase of the [unmarked paired rows](ALL_BASE_CLASSES_NORM_MATCHING.md): \(c=c_0+120i,\ d=d_0+3240j\), with endpoints at \(c,c+24\) and with the stated conditions at fixed support primes. Let the phase indices \((i,j)\) range over \(\widehat{\mathbb Z}^2\). At each non-support inert prime \(p\), take \(n_p\) independently Haar in \(\mathbb Z_p\). A phase is killed at \(p\) if either endpoint difference \(n_p-3^c-5^d\) or \(n_p-3^{c+24}-5^d\) has finite odd valuation. Exact zero survives this local test. All powers at these primes are well-defined by reducing exponents modulo their finite orders at each depth. The support contains every prime dividing the difference of the two endpoints, which are therefore distinct modulo each non-support inert prime.

Let \(T\) be the first prime, in ascending order, at which the panel of old primes and this prime kills every phase; write \(T=\infty\) if no finite initial panel does. Then, unconditionally,
\[
 \Pr(Y<T<\infty)\ll \frac{1+\log\log Y}{\log Y}\quad(Y\ge 3).
\]
If every phase is killed by the infinite panel, the open killed sets cover the compact phase space, so some finite panel already kills every phase. The estimate therefore bounds the error from counting only first blockers at primes up to \(Y\) in this local Haar model. It gives no statement about density one for ordinary integers or a signed four-shift correlation.

## A single-prime bound

Put \(b=5^{3240}\); \(\operatorname{ord}_q(b)\) is odd at inert \(q\). For \(r^e\Vert\operatorname{ord}_q(b)\), take \(h=e-1\) if \(r\) is not itself a non-support inert prime. If it is and \(e\ge2\), choose \(h\in\{e-1,e-2\}\) so \(h+v_r(5^{r-1}-1)\) is even. Otherwise take \(h=0\) and temporarily drop \(r\)'s condition. Set \(m=r^{h+1}\) and
\[
 S=\{p<q:\ p\ne r,\ p\text{ non-support inert},\ m\mid\operatorname{ord}_p(b)\}.
\]
Drop \(S\) as well and select one phase satisfying the retained panel, if possible. This choice need not read any dropped observations. More formally the retained survivor set is closed in the compact phase space; pick the first intersecting cylinder at each level of a nested finite cylinder partition. Intersecting is measurable: the joint viable relation in phase and observation variables is closed, and the phase projection of its intersection with a cylinder is closed by compactness.

Generate \(r\) phases by adding \(xr^h\) to the \(r\)-primary coordinate of \(j\) for \(0\le x<r\), leaving all other primary coordinates and \(i\) unchanged. For \(p\ne r\) the \(r\)-part of \(\operatorname{ord}_{p^k}(b)\) does not change with \(k\); only primes in \(S\) can newly kill variants among those old primes. At a retained \(r\), differences between two variant shifts have exact valuation \(h+v_r(5^{r-1}-1)\), even, by lifting the exponent (a non-support \(r\) does not divide 3240). At most one endpoint collides modulo \(r\), and its variants share the same digits through that depth. If these digits agree with the observation, all except at most one variant have the even valuation. If they disagree, the valuation is unchanged from the retained phase. Thus at most one variant is lost. If \(r\) was dropped, none is lost unless one of two roots is hit modulo \(r\), an event of probability at most \(2/r\).

Each variant loses at any \(p\in S\) with probability at most \(2/p\), by independence from the selected phase. At \(q\) the \(r\) shifts of the \(d\)-term are distinct modulo \(q\), and each of the two endpoints forbids at most one variant for each value of \(n_q\bmod q\). Thus three old survivors suffice to prevent first blocking at \(q\). If fewer survive but some old phase survives, the final observation must hit one of its two roots, conditionally with probability at most \(2/q\). Markov's inequality on the number of dropped-panel losses now gives
\[
 \Pr(T=q)\le \frac{2}{q}\left(\frac{2\eta}{r}
     +\frac{2r}{r-\delta-2}\sum_{p\in S}\frac1p\right),
\]
where \(\eta=1\) means \(r\) was dropped and \(\delta=1\) means its condition was retained using the even depth. The denominator is positive since \(r\ge3\), and in the retained case \(r\ge19\). This proof does not require any assertion about the distribution of common Wieferich primes.

## Summation

Choose \(m\) largest among the choices above. Every candidate for its prime \(r\) was at least \(r\) and at least \(r^{e-1}\), so
\(\log\operatorname{ord}_q(b)\le\vartheta(m)+\psi(m)\ll m\).
Only when \(e=1,\ h=0\) can \(\eta=1\), and then \(m=r\). The sum over \(S\) is bounded by the reciprocal-prime sum for the class \(1\bmod m\), which is \(O((1+\log\log q)/m)\) by partial summation of the [Montgomery–Vaughan Brun–Titchmarsh bound](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED). Here \(\varphi(m)\asymp m\) since \(m\) is an odd prime power; the contribution through \(2m\) is \(O(1/m)\). Thus for order exceeding \(q^{1/4}\) the summand is \(O((1+\log\log q)/(q\log q))\). Ordinary prime counting and partial summation give the asserted logarithmic tail. Primes of lower order in \([Q,2Q]\) divide \(\prod_{j\le (2Q)^{1/4}}(b^j-1)\); its logarithm is \(O_b(Q^{1/2})\), so their dyadic reciprocal tails total \(O_b(Y^{-1/2})\).

## Concrete primary-digit replay

The input uses the real bases and the same exponent pair across the four local tests. Of the 31 variants, \(x=1,2,3\) are individually removed at 31, 17299, 44207 respectively, while 311 reads a lower digit and removes none. This checks the reset mechanism and odd valuations, not a full blocker.

~~~python
from math import isqrt, lcm, prod

P = (31, 311, 17299, 44207)
M = 32 * prod((3, 5, 7, 11, 13, 41, 73, 6481))
n = 1102541849640247813272282332105584344150762
E = 31 * lcm(30, 10*311**2, 18*17299, 46*44207)
assert n % M == 131082
assert all(all(p % j for j in range(2, isqrt(p)+1)) for p in P)
assert [next(k for k in range(1,p) if pow(5,3240*k,p) == 1)
        for p in P] == [1, 31, 961, 22103]

def s(x, c, m):
    return (pow(3,c,m) + pow(5,50+3240*(130719+x*E),m)) % m

def valuation(a, p):
    assert a
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v

for p, k, expected in zip(P, (4,3,2,2), ([1], [], [2], [3])):
    m = p**k
    assert [x for x in range(31) if
            any(valuation((n-s(x,c,m)) % m,p) % 2
                for c in (26,50))] == expected

assert len({s(x,26,44207) for x in range(31)}) == 31

~~~
