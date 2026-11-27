# Single-remainder Gaussian probe and its isolation limit

One modular power and one gcd recover a split prime that every pairwise directional gcd misses. At the fixed target \(n=2661\), the probe recovers the isolated **proper** factor \(41\) of \(2661-3^3-5^4=2009\). The cofactor is small enough to certify the whole remainder. There is also an infinite family in the full \(n/4\) box where every rung of the same exponent rule misses the isolated large prime.

### A probe on one remainder

Take \(n\equiv9\pmod{12}\), odd \(c\ge1\), even \(d\ge0\), and \(R=n-3^c-5^d>1\). Then \(R\equiv5\pmod{12}\). Compute
\[
t=3^{(R-1)/4}\bmod R,\qquad D=\gcd(R,t^2+1).
\]
This costs \(O(\log R)\) modular multiplications and one integer gcd. It uses only the selected remainder.

Every output \(D\) is a primitive Gaussian norm. The root \(t^2\equiv-1\pmod D\) makes \((D,t+i)\) the kernel of evaluation at \(i=-t\) from \(\mathbb Z[i]\) onto \(\mathbb Z/D\mathbb Z\). Its Gaussian gcd generator therefore has norm \(D\), the index of the ideal. The generator’s coordinates are coprime because it divides \(t+i\). If \(R\) is prime, quadratic reciprocity gives \((3/R)=-1\), so Euler’s criterion gives \(D=R\). The returned root certifies the norm directly, with no primality test needed.

For a proper \(D\), put \(C=R/D\). In this sector \(C\equiv1\pmod4\) and \(3\nmid C\). If \(C\) fails to be a two-square norm, an even positive number of distinct primes congruent to \(3\bmod4\) have odd valuation in \(C\). The smallest possible pair is \(7,11\). Thus **\(C<77\) certifies the whole remainder**. If a panel has already verified even valuations, the same argument uses the first two inert primes left unchecked.

At the previously pinned \(n=5277\), the probe recovers \(D=5273\) from \((1,0)\), the isolated prime in the published pairwise-gcd control. At the second fixed target \(n=2661\), the full box has \(0\le c\le5\), \(0\le d\le4\). Its only cell divisible by \(41\) is \((3,4)\), where the probe gives \(D=41\) and \(C=49<77\). Indeed \(2009=28^2+35^2\). At the same \(n\), cell \((1,4)\) gives \(D=1\) and the genuine nonnorm \(2033=19\cdot107\). [Published pairwise-gcd baseline](https://github.com/Samsen879/a303656/commit/eb261c48159823afc9e2a55564191b4b17a6ab7f)

### Exact limit of the exponent rule

Write \(R-1=2^sK\) with \(K\) odd. Consider all gcds \(\gcd(R,a^{2^jK}+1)\) for \(1\le j<s\). For \(p^e\parallel R\), \(p\nmid a\), let \(o=\operatorname{ord}_p(a)\) and \(C=R/p^e\). A rung detects \(p\) exactly when
\[
o\mid C-1,\qquad 2\le v_2(o)\le s.
\]
Indeed, \(a^{2^jK}=-1\bmod p\) requires the odd part of \(o\) to divide \(K\) and \(v_2(o)=j+1\). Also \(R=p^e C\equiv C\bmod o\). Consequently, for a composite remainder with \(2\le C\le L\), detection by a fixed base \(a\ge2\) forces \(p\le a^{L-1}-1\).

For every prime \(p\equiv1\pmod{12}\), \(p>80\), take \(n=5p+52\). The active cell \((3,2)\) has the true norm \(R=5p\), and \(p\) is isolated in the **entire** \(n/4\) box. Any offset divisible back into this remainder modulo \(p\) must be \(52\), \(52+p\), or \(52+2p\), by the active upper bound \(3^c+5^d\le n/2\). The first occurs only at \((3,2)\). The second is \(5\bmod12\), which no offset attains. The third is \(6\bmod12\), which forces \(c=0\) and \(5^d=51+2p>n/4\). There are infinitely many such primes, as the prime divisors of \(x^4-x^2+1\) for \(6\mid x\) have order \(12\) for \(x\), and taking \(x\) divisible by any given finite list avoids that list.

Here \(C=5\), so a successful base would itself have order \(4\bmod p\), making it already a root of \(-1\bmod p\). All base-3 rungs miss \(p>80\), and any fixed finite base menu misses \(p\) for all sufficiently large members of the family. At \(p=109\), the cell gives \(D=1\) despite \(545=4^2+23^2\). The same \(n=597\) has another active cell \((1,0)\) that the probe certifies. The obstruction concerns extraction at the selected cell. A guarantee of selecting a successful active cell for arbitrary \(n\) remains open.

### Standalone replay

```python
from math import gcd, isqrt

def box(n):
    return {(c,d): n-3**c-5**d
            for c in range(n.bit_length()) for d in range(n.bit_length())
            if 4*max(3**c,5**d) <= n}

def probe(n,c,d):
    r = box(n)[c,d]
    assert r > 0 and r % 12 == 5
    t = pow(3,(r-1)//4,r)
    return r,t,gcd(r,t*t+1)

def solo(n,c,d,p):
    assert p % 4 == 1 and all(p % k for k in range(2,isqrt(p)+1))
    assert [ij for ij,r in box(n).items() if r % p == 0] == [(c,d)]

assert probe(5277,1,0) == (5273,944,5273)
solo(5277,1,0,5273)
assert 28**2 + 67**2 == 5273
assert all(r % 5273 for r in box(5349).values())

assert probe(2661,3,4) == (2009,893,41)
solo(2661,3,4,41)
assert 4**2 + 5**2 == 41 and 2009 == 41*49
assert 28**2 + 35**2 == 2009
assert probe(2661,1,4) == (2033,575,1)
assert 2033 == 19*107 and 2033 % 19**2 != 0

assert probe(597,3,2) == (545,221,1)
solo(597,3,2,109)
assert 4**2 + 23**2 == 545 and 545-1 == 2**5*17
assert [gcd(545,pow(3,2**j*17,545)+1) for j in range(1,5)] == [5,1,1,1]
assert probe(597,1,0) == (593,77,593)
assert 8**2 + 23**2 == 593
print("all exact checks passed")
```

For the Gaussian gcd, any rational integer dividing both generator coordinates would divide \(t+i\), hence divide its imaginary coordinate 1. For the infinitude argument, at a prime divisor \(\ell\) of \(x^4-x^2+1\) with \(6\mid x\), the identity \((x^2+1)(x^4-x^2+1)=x^6+1\) gives order dividing 12 but not 6. Order 4 would imply \(\ell\mid 3\), which is excluded. This proves the required order 12 without a prime distribution estimate. The universal failure concerns fixed bases on this family of isolated factors only; it does not exclude choosing a different active cell or using a different algorithm.
