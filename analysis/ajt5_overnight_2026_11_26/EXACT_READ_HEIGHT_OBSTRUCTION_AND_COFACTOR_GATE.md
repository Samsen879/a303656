# The exact-read height obstruction and a valuation-preserving countercontrol

This follows [uniform finite-phase coverage](https://github.com/Samsen879/a303656/commit/f734a1c14e0515cbdbd4dd5f439c76d47ad19a0d). The matched family shows a specific limitation of locking the exact earlier residues: every nontrivial locked shift eventually lies beyond ordinary height, while a change of four in \(D\), altering a read but preserving its valuation test, gives a true witness at the same target. The conditional small-cofactor test is separate and is not guaranteed for a general input.

For the elementary bound on \(L(Y)\), each prime power newly entering \((\lceil Y/2\rceil,Y]\) contributes its prime factor to the central binomial coefficient, by the floor-sum formula for valuations. For odd \(Y\), the two equal central coefficients are individually at most \(2^{Y-1}\). This proves \(L(Y)\le4^Y\) by induction. Separately, the exponent compression preserves the chosen finite prime valuations but need not preserve unlisted reads. Its guaranteed panel width is only of order \(\log\log n\). All finite controls and exact periods below were independently replayed.

**Exact preservation of old reads can prevent every in-height repair, even when changing \(D\) by four gives a true two-square remainder.** I proved this for both axes moving together and for exact multiplicative orders, already when the old reads are only modulo \(p\). A separate transfer lemma makes a slowly growing panel compatible with positive remainders and gives a sharp test on the remaining cofactor.

### From finite phases to a true witness

Use the independently replayed 25-center theorem as finite-phase input. For \(Y\ge31\), take the panel of inert primes \(p\le Y\), with \(3\) handled by the head. Let \(\mathcal P\) be the primes where the chosen center actually has the certified valuation \(0\) or \(2\). The transfer applies whether or not there are common-Wieferich primes outside \(\mathcal P\). Require also that the center’s reading mod \(32\) certifies \(v_2\le3\) and odd part \(1\bmod4\).

Set
\[
M=\operatorname{lcm}\!\left(72,\ \{p^2(p-1):7\le p\le Y,\ p\text{ prime},\ p\equiv3\bmod4\}\right).
\]
Keep \(C\) if \(C\le2\), and otherwise take its representative in \([3,M+2]\). For the menu offsets in \([-24,304]\), take \(D\) in \([25,M+24]\). These choices preserve the readings mod \(32\), mod \(27\), and mod \(p^3\) on the panel. Every resulting exponent is at most \(M+328\), so \(n>2\cdot5^{M+328}\) makes every remainder positive. This compression keeps the selected panel readings. A subsequent repair that needs other readings must keep those too.

An explicit growing choice is \(Y=\lfloor(\log_2\log_2 n)/8\rfloor\), for sufficiently large \(n\). Indeed \(M\mid L(Y)^2\) for \(L(Y)=\operatorname{lcm}(1,\ldots,Y)\), and \(L(Y)\le4^Y\). For the latter bound, each prime power newly entering between \(\lceil Y/2\rceil\) and \(Y\) contributes its prime to \(\binom{Y}{\lfloor Y/2\rfloor}\). Induction gives the bound, using the two equal central coefficients for odd \(Y\). Thus \(M\le\sqrt{\log_2 n}\).

For the selected positive remainder \(R\), let \(G\) be a certified odd sum-of-two-squares divisor of its odd part. Define
\[
u=\frac{R}{2^{v_2(R)}G},
\]
and let \(q_1<q_2\) be the first two inert primes outside \(\mathcal P\). Then **\(u<q_1q_2\) guarantees a true witness**. In fact, \(u\equiv1\bmod4\), so if any inert prime occurs to odd exponent in \(u\), at least two distinct inert primes do. Both must lie outside \(\mathcal P\). The test needs no factorization of \(u\).

The strict threshold is sharp for these data. With all inert primes through \(31\) passing, the same exponents \((C,D)=(2,1)\) give \(1861=30^2+31^2\) at \(n=1875\) and \(2021=43\cdot47=q_1q_2\) at \(n=2035\). Both remainders are \(5\bmod32\). The growing-panel argument supplies no bound of this size on \(u\) for arbitrary \(n\).

### A sharp obstruction for period-preserving repair

Use the actual 25 offsets \(8j\), where
\[
I=\{0\le j\le38:j\not\equiv1\bmod5,\ j\not\equiv1\bmod9,\ 
j\bmod11\notin\{6,10\}\}.
\]
This set contains \(0,2\). Start at \((C,D)=(2,1)\). For \(k=1\) or \(3\), preserving the old remainder readings mod \(p^k\) at every inert \(7\le p\le Y\) is **equivalent** to
\[
C'\equiv2\pmod{M_3^{(k)}},\qquad
D'\equiv1\pmod{M_5^{(k)}},\qquad
M_b^{(k)}=\operatorname{lcm}_{7\le p\le Y,\ p\equiv3(4)}
                \operatorname{ord}_{p^k}(b),
\]
where the lcm is over primes. Subtracting the two readings at \(j=0,2\) forces \((5^{D'}-5)(5^{16}-1)\equiv0\bmod p^k\). The second factor is a unit. If the order of \(5\bmod p\) divided \(16\), it would divide \(\gcd(16,p-1)=2\), forcing \(p\mid24\). The first reading then forces \(3^{C'}\equiv9\bmod p^k\). The converse follows directly.

Here is an infinite family of matched targets. Let \(P\) be the product of inert primes through \(Y\), including \(3\), and choose
\[
a=2P^3-392,\qquad n_+=14+a^2+b^2,\qquad n_-=n_++16P^3 .
\]
Choose \(b\equiv2\bmod4\) and, for each \(p\mid P\), choose \(b\bmod p\) so that \(a^2+b^2+5\) is outside the odd powers of \(5\bmod p\). There are \((p+1)/2\) square residues and at most \((p-1)/2\) odd powers, so the choices exist. CRT gives \(0\le b<4P\).

All 25 seed readings are units at every panel prime, and the two targets have identical seed readings mod \(p^3\). At \(n_+\) the seed remainders are \(8\bmod32\); at \(n_-\) they are \(24\bmod32\), which has odd part \(3\bmod4\). At \(n_-\) changing \(D\) from \(1\) to \(5\) changes the read at \(7\), keeps every panel unit, restores the \(8\bmod32\) guard, and gives the genuine witness
\[
n_- -9-5^5=(a+4)^2+b^2.
\]
At \(n_+\) the seed gives \(a^2+b^2\). For sufficiently large \(Y\), every remainder in both menus and in the repaired menu is positive.

For the exact \(8\bmod32\) repair at \(n_-\), a locked shift satisfies
\[
\Delta C+3\Delta D\equiv4\bmod8.
\]
Both periods are twice an odd number. With \(C\) fixed, the least legal increase in \(D\) is exactly \(2M_5^{(k)}\). With both axes free, the minimum of \(\max(\Delta C,\Delta D)\) is \(2\min(M_3^{(k)},M_5^{(k)})\), except that when \(M_3^{(k)}+M_5^{(k)}\equiv0\bmod8\), the pair of single-period shifts gives the additional candidate \(\max(M_3^{(k)},M_5^{(k)})\). Take the smaller candidate. This exhausts the possibilities because any other successful pair uses at least two periods on one axis.

Even the mod-\(p\) periods grow faster than every power of \(\log n_\pm\) in this family. To see this, group the primes by \(d=\operatorname{ord}_p(b_0)\) for \(b_0=3\) or \(5\). In each group the product divides \(b_0^d-1\) and each prime is \(1\bmod d\). Its log mass is at most \(\min(d\log b_0,Y\log Y/d)\). Consequently the total log mass is at most
\[
\tau(M_{b_0}^{(1)})\sqrt{Y\log Y\log b_0}.
\]
The fixed-modulus prime number theorem gives total log mass \(\sim Y/2\). The divisor bound \(\tau(m)\ll_\epsilon m^\epsilon\) then rules out \(M_{b_0}^{(1)}\le Y^A\) for every fixed \(A\), eventually. Since \(\log n_\pm=6\log P+O(1)=\Theta(Y)\), every nonzero locked shift eventually exceeds the positive-remainder exponent window. [Fixed-modulus prime number theorem reference](https://doi.org/10.1112/S0010437X12000802)

For a small exact control, \(Y=11\) gives \(n_-=607740529973574\), exponent ceilings \((30,21)\), and first-order periods \((30,30)\). The same target has the true cheap witness at \((2,5)\). For the full 25-label replay at \(Y=211\), the ceilings are \((570,389)\) and the first-order periods are \((14019911826253883550,4673303942084627850)\).

```python
from math import isqrt, lcm, prod

def prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))

def order(base, p, k):
    m = p**k
    phi = p**(k - 1) * (p - 1)
    r, x = phi, phi
    for f in range(2, isqrt(phi) + 1):
        if x % f == 0:
            while x % f == 0:
                x //= f
            while r % f == 0 and pow(base, r // f, m) == 1:
                r //= f
    if x > 1:
        while r % x == 0 and pow(base, r // x, m) == 1:
            r //= x
    return r

def ilog(n, base):
    e = 0
    while n >= base:
        n //= base
        e += 1
    return e

def replay(Y, indices):
    primes = [p for p in range(3, Y + 1, 4) if prime(p)]
    P = prod(primes)
    a = 2 * P**3 - 392
    residues = {4: 2}
    for p in primes:
        odd_powers = {pow(5, d, p) for d in range(1, p, 2)}
        residues[p] = next(b for b in range(p)
                           if (a*a + b*b + 5) % p not in odd_powers)
    m = 4 * P
    b = sum(v * (m // p) * pow(m // p, -1, p)
            for p, v in residues.items()) % m
    plus = 14 + a*a + b*b
    minus = plus + 16 * P**3
    assert minus - 9 - 5**5 == (a + 4)**2 + b*b
    assert pow(5, 5, 7) != pow(5, 1, 7)
    for n, D, guard in [(plus, 1, 8), (minus, 1, 24), (minus, 5, 8)]:
        for j in indices:
            R = n - 9 - 5**(D + 8*j)
            assert R > 0 and R % 32 == guard
            assert all(R % p for p in primes)
    assert all((minus - plus) % p**3 == 0 for p in primes)
    rows = [p for p in primes if p >= 7]
    assert all((pow(5, 16, p) - 1) % p for p in rows)
    assert all(any(pow(base, p-1, p*p) != 1 for base in (3, 5))
               for p in rows)
    B3, B5 = ilog(minus, 3), ilog(minus, 5)
    for k in (1, 3):
        M3, M5 = (lcm(*(order(base, p, k) for p in rows))
                  for base in (3, 5))
        assert 2 + M3 > B3 and 1 + M5 > B5
        assert (minus - 9 - pow(5, 1 + 2*M5, 32)) % 32 == 8
        if k == 1 or Y == 11:
            print(Y, k, M3, M5, B3, B5)
    return minus

I = [j for j in range(39)
     if j % 5 != 1 and j % 9 != 1 and j % 11 not in (6, 10)]
assert len(I) == 25 and {0, 2} <= set(I)
assert replay(11, [0, 2]) == 607740529973574
replay(211, I)
assert 1875 - 14 == 30**2 + 31**2 and 2035 - 14 == 43 * 47
assert [p for p in range(32, 48) if prime(p) and p % 4 == 3] == [43, 47]
assert all(R % 32 == 5 and all(R % p for p in range(3, 32, 4) if prime(p))
           for R in (1861, 2021))
```

The remaining height problem is to select new in-window residues while retaining the old **valuation tests**, or to certify a sufficiently small residual cofactor. The obstruction applies even to exact first reads, and the same-target witness shows why it does not extend to valuation-preserving reselection.
