# Short-cofactor exclusion at a doubly deep 31-reader

**The bounded-order class is excluded at the \(31\)-sink.** Let \(p\equiv3\pmod4\) be a common Wieferich prime for bases \(3,5\), and put
\[
d_b=\operatorname{ord}_p(b),\qquad u_b=d_b/31^{v_{31}(d_b)}.
\]
If \(31^2\) divides at least one of \(d_3,d_5\), and every prime power dividing either order is at most \(961\), then **both \(u_3\) and \(u_5\) exceed \(81\)**. The short cofactor can be on either axis, including the axis that does not read the second \(31\)-digit.

### Exact order test

Set \(r=31\), \(B=9\cdot10^{14}\), and
\[
L=\operatorname{lcm}\{j\le961:4\nmid j,\ r\nmid j\},\qquad E=r^2L.
\]
The order cap and \(p\equiv3\pmod4\) imply \(d_3,d_5\mid E\). For a proposed short axis \(b\), write \(c=8-b\) and choose \(m\mid L\). Form
\[
G=\gcd(b^{r^2m}-1,c^E-1),\qquad
D=\gcd(G,b^{rm}-1,c^{E/r}-1).
\]
Let \(H\) be \(G\) with every prime power supported on \(D\) removed.

For \(p>B\), the test \(p^2\mid H\) is **equivalent** to common Wieferich, \(d_b\mid r^2m\), \(d_c\mid E\), and at least one order having \(r\)-depth two. Indeed, \(p\nmid E\), so replacing an exact order by any of the indicated multiples preserves its \(p\)-adic lifting valuation. Among primes dividing \(G\), membership in \(D\) means both orders already divide the lower periods. This eliminates the shallow branch even when the short axis is shallow. The test also works with \(m=L\) for the entire capped class, although that operand is much larger than those evaluated here.

Every admissible \(u_b\le81\) divides one of 33 divisibility-maximal \(m\)'s in that range. On the resulting 66 blocks, the largest \(H/\gcd(H,K)\) was **1,555,314,631,021,545,381,274,988,219**, below \(B^2\). Here \(K\) is the product of the seven explicit integers in the replay. Each is below \(B\), so stripping them cannot weaken any test at \(p>B\). Below \(B\), the existing published search and the base-5 checks of \(11,1006003\) already exclude common Wieferich primes. [Dorais–Klyve, §4.1 and Tables 2, 5–6](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

### Consequence for an overloaded sink

On the predecessor’s full 28,830-point repair chart with nonzero observations, a stalled \(31\)-sink with \(s\le5\) shallow readers needs at least **\(31-6s\) distinct depth-two readers** outside the excluded class. If the remaining depth-two readers are all doubly deep, the requirement is \(\lceil(28830-5580s)/173\rceil\). Under the order cap, every one of those readers must now have both cofactors above 81. For any fixed remaining order pair, the odd part \(D_*\) of its lcm is at least \(41\cdot961\). Its physical primes occupy \(2D_*+1\bmod 4D_*\), with spacing at least 157,604. The spacing applies per order pair. [Verified repair capacities](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

**Ordinary control.** The prime \(640027=(4\cdot167-2)961+1\) has exact order pair \((640026,213342)\), with cofactors \((666,222)\). Thus the cap alone does allow both axes to read the second digit with long cofactors. The replay gives a real small-head point \((c,d)=(2,3)\) with exact valuation two at \(31\) and exact valuation one at this reader. Both bases are ordinary there. This ordinary case shows why the common-Wieferich hypothesis matters.

The conclusion is a necessary order restriction on a stall under the full-chart hypotheses. Longer cofactors, zero observations, and unavailable repair digits still need separate arguments. The verified exception-density bound remains below \(0.000062192085\%\).

### Standalone replay

Python uses exact integers throughout. Optional `gmpy2` accelerates the 66 modular powers. The 66 block checks were independently rerun in BigInt, as were the ordinary order and lifting checks; the same maximum was obtained.

```python
from math import gcd, isqrt, lcm, prod

try:
    from gmpy2 import mpz
except ImportError:
    mpz = int

r, B = 31, 9 * 10**14
E = r*r*lcm(*(j for j in range(1, 962) if j % 4 and j % r))
small = (31, 18162901, 1165279771, 108180394159891,
         30255018851, 403621, 11849850751)
assert max(small) < B
K = prod(small)
U = [m for m in range(1, 82) if m % 4 and m % r]
top = [m for m in U if not any(j > m and j % m == 0 for j in U)]

out = []
for m in top:
    for b, c in ((3, 5), (5, 3)):
        A = mpz(b)**(r*r*m) - 1
        g = gcd(int(A), int(pow(mpz(c), E, A) - 1))
        d = gcd(g, b**(r*m)-1, int(pow(mpz(c), E//r, mpz(g))-1))
        while d > 1:
            g //= d
            d = gcd(g, d)
        out.append(g // gcd(g, K))
assert len(out) == 66
assert max(out) == 1555314631021545381274988219 < B*B
assert [pow(5, p-1, p*p) for p in (11, 1006003)] == [78, 31695130519]

p = 640027
assert all(p % t for t in range(2, isqrt(p)+1))
assert p == (4*167-2)*r*r+1 and p-1 == 2*9*r*r*37
factors = (2, 3, 31, 37)
rows = ((3, 640026, 542429), (5, 213342, 282537))
for b, d, quotient in rows:
    assert (p-1) % d == 0 and pow(b, d, p) == 1
    assert all(pow(b, d//t, p) != 1 for t in factors if d % t == 0)
    assert pow(b, d, p*p) == 1 + p*quotient
    assert pow(b, 30, r*r) != 1

n = 44376063028842876977656599206390030747442627
R = n - 3**2 - 5**3
assert n % 3 == 0 and n % 32 == 3
assert all(R % t for t in (7, 11, 19, 23))
assert R % r**3 == r*r and R % p**2 == p
print(len(out), max(out))
```