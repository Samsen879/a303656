# Two adjacent columns without permanent quadratic shifts

Set (d,c,r)=(0,7,2), so the true parent shift is A=2188. The two child columns e=0,1 give C_e=10941,10937 and shifts K_f=C_e−3^f. Neither column has K_f=0 or a positive norm: check f=0,…,8 using the primes in the replay; larger f are negative. This is in contrast to the single-column control e=d+1,r=0,c odd, where K_f=5·3^c−3^f is negative for f≥c+2, has odd 3-adic valuation for odd f<c or f=c,c+1, and is 6 or 14 mod 16 for even f<c.

For positive norms T≤B and f≤F in the actual two-column example, force an exact odd obstruction at some auxiliary prime for each residual 5Tp²+K_f, as in FINITE_LABEL_QUADRATIC_HEIGHT.md. There are at most 2(F+1)s(B) pairs, where s(B) counts positive norms up to B. A quantitative choice uses quadratic reciprocity to set the signs at a reduced class modulo 8·rad_odd(5TK_f), and one separate tagging prime ell of size O(B·3^F) larger than every tag U+jB+T, where U=5B(3^F+10941), j indexes the 2(F+1) labels. The tags keep auxiliary primes distinct and above U; ell exceeds all prime divisors of the tagged coefficients. Linnik gives log of each auxiliary prime O(F+log(B+1)). Select the work prime in the resulting reduced CRT class, with p≡3 mod 4, avoiding prime divisors of every K_f, and with a representative modulo ell large enough that p>3^(F/2). The added modulus for these exclusions has log O(F²), and ell ensures strict activation even at T=1. A second Linnik application bounds log p by O(s(B)(F+1)(F+log(B+1))). Thus prefixes F on the scale of sqrt(log p) are attainable with fixed B, and a growing common scale for B=F is (log p*sqrt(log log p))^(1/3), using the classical upper bound s(B)=O(B/sqrt(log B)).

The active range extends to f≤floor(log_3(5Bp²+C_e−1)), potentially far beyond the blocked prefix. A true bridge immediately beyond the forced prefix is included in the replay. No entire-column obstruction is inferred.

```python
from math import isqrt

def prime(q):
    return q > 1 and all(q % d for d in range(2, isqrt(q) + 1))

def norm(n):
    return n >= 0 and any(isqrt(n-a*a)**2 == n-a*a
                          for a in range(isqrt(n//2) + 1))

data = [
    (10941, (547,) + (3,)*8),
    (10937, (1367, 7, 683, 1091, 23, 5347, 11, 7, 547)),
]
for C, qs in data:
    assert 3**8 < C < 3**9
    for f, q in enumerate(qs):
        K = C - 3**f
        assert prime(q) and q % 4 == 3 and K % q == 0 and K % (q*q)

p, m = 239, 59309
assert prime(p) and p % 4 == 3 and m - 2188 == p*p
for C, _ in data:
    for f in range(4):
        S = 5*p*p + C - 3**f
        assert S > 0 and S % p and not norm(S)
assert 5*m + 2 - 1 - 3**4 == 23**2 + 544**2
```
