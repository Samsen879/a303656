# Native graph realization in shared 3/5 order panels

**Every finite simple graph occurs as the hidden shared-order graph of an actual 3/5 exact-hit panel.** The construction gives each edge its own prime modulus \(\ell_e\). At one fixed integer target per panel, every assignment of edge digits \(c\equiv d\equiv x_e\pmod{\ell_e}\) is realized by an actual nonnegative exponent pair, without an ordinary-height claim. Thus native treewidth is unbounded, and large separators can have many **realized** states.

The inline replay verifies a four-cycle of treewidth two and exhausts its \(7\cdot11\cdot13\cdot17=17{,}017\) edge assignments.

## Construction

Give each edge \(e\) a distinct prime label \(\ell_e>5\). Select one row prime \(p_i\) per vertex, in increasing order and larger than every edge label. Require:

- \(p_i\equiv47\pmod{60}\).
- For each incident label \(\ell\), require \(v_\ell(p_i-1)=1\) and
  \[
  3^{(p_i-1)/\ell}\equiv5^{(p_i-1)/\ell}\not\equiv1\pmod{p_i}.
  \]
- Keep all nonincident labels out of \(p_i-1\). Also keep out every earlier row prime and every odd factor of an earlier \(p_j-1\) other than the labels incident to \(i\).

These conditions are simultaneously realizable. Put the congruences in a cyclotomic field \(F=\mathbb Q(\zeta_M)\), using \(1+\ell\bmod\ell^2\) at incident labels and \(2\bmod r\) at excluded odd primes. For each incident \(\ell\), adjoin the \(\ell\)-th roots of 3 and 5. Their classes are independent in \(F^\times/F^{\times\ell}\): if a nontrivial product \(3^a5^b\) were an \(\ell\)-th power in \(F\), its positive real \(\ell\)-th root would generate a non-Galois subfield of the abelian extension \(F/\mathbb Q\). Indeed, its minimal polynomial has degree \(\ell\), since a rational constant term of any smaller factor would force \(\ell\mid da\) and \(\ell\mid db\) for some \(0<d<\ell\). The two radicals therefore give independent cyclic actions of order \(\ell\). The extensions for distinct labels are disjoint over \(F\) by their coprime degrees.

Lift the prescribed cyclotomic automorphism so it acts on both radicals for each incident \(\ell\) by the same nontrivial \(\ell\)-th root of unity. Chebotarev supplies arbitrarily large row primes with that Frobenius class. Reducing the radical action at such a prime yields precisely the displayed equal-power test. [Sutherland, *Global class field theory and the Chebotarev density theorem*](https://math.mit.edu/classes/18.785/2025/lectures.html)

Use the **full** prime-square orders. Any additional factor in a base order from \(p_i\) to \(p_i^2\) is \(p_i\), which is private by the choice of row primes. After fixing \(c\) even and \(d\) odd, the only shared digits between two rows are their edge label in each coordinate, if the rows are adjacent. The hidden graph is exactly the graph specified at the start.

### Pointwise realization at one target

Fix \(n\equiv p_i\pmod{p_i^2}\) at each row and join these residues by CRT. Given arbitrary edge digits \(x_e\), impose \(c\equiv d\equiv x_e\pmod{\ell_e}\). At each row set both exponents to zero modulo \(p_i\) and modulo the remaining odd part of \(p_i-1\) after removing its incident labels. These congruences are compatible.

The equal-power tests cancel the incident \(\ell\)-components of \(3^c/5^d\). Its other odd components are trivial by the chosen congruences. Since \(5\) is a nonsquare at \(p_i\), the prescribed parities give \(3^c/5^d=-1\bmod p_i\). Both exponents are multiples of \(p_i\), so the ratio is killed by \(p_i-1\) modulo \(p_i^2\). Its reduction therefore determines it uniquely, giving \(3^c+5^d\equiv0\pmod{p_i^2}\). The residual is \(p_i\bmod p_i^2\), an exact hit.

Conversely, a hit implies \(3^c=-5^d\bmod p_i\). Raising this equality to \((p_i-1)/\ell_e\) gives \(c\equiv d\pmod{\ell_e}\) on every incident edge. Thus the realized joint edge-label set is **exactly** the product of the diagonals.

## Separator cost

For a cut \(A\mid B\) of the rows, the separator has
\[
\prod_{e\in E(A,B)}\ell_e
\]
distinct realized tuples. In particular, a binary decomposition of the \(m\)-vertex complete graph has a cut with both sides between \(m/3\) and \(2m/3\). Explicitly listing the feasible tuples at that cut requires at least \(7^{\lceil2m^2/9\rceil}\) entries. This is a cost for tuple listings. The diagonal product itself has a compact symbolic description.

The construction does not assume that a non-Wieferich base always supplies an adjustable digit. When using the shorter prime-level test in another panel, a lifting base must be free to change its exponent by a multiple of its prime-level order that also preserves the coarse congruence and is coprime to \(p\). If the coarse congruence fixes that digit, retain the prime-square order. The replay includes a local example where pinning it changes an exact hit into valuation at least two while retaining the prime-level match.

## Native four-cycle replay

The row primes, in cycle order, are \(2722007,3116807,11729147,14565227\). The successive edges carry labels \(7,11,13,17\). The standard-library replay verifies the exact order gcds and every edge assignment at the same target. The general existence proof gives no numerical upper bound on the row primes.

```python
from itertools import combinations, product
from math import gcd, isqrt, prod

P = (2722007, 3116807, 11729147, 14565227)
S = ((7, 17), (7, 11), (11, 13), (13, 17))
E = (7, 11, 13, 17)

def prime_factors(n):
    result = set()
    d = 2
    while d*d <= n:
        if n % d == 0:
            result.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        result.add(n)
    return result

def order(q, p, k):
    m, h = p**k, (p-1)*p**(k-1)
    for r in prime_factors(p-1) | {p}:
        while h % r == 0 and pow(q, h//r, m) == 1:
            h //= r
    return h

def weights(moduli):
    M = prod(moduli)
    return M, [M//m * pow(M//m, -1, m) for m in moduli]

def hit(n, p, c, d):
    return (n-pow(3, c, p*p)-pow(5, d, p*p)) % (p*p) == p

for p, labels in zip(P, S):
    assert p % 60 == 47
    assert all(p % d for d in range(3, isqrt(p)+1, 2))
    for ell in labels:
        assert (p-1) % ell == 0 and (p-1) % (ell*ell) != 0
        assert pow(3, (p-1)//ell, p) == pow(5, (p-1)//ell, p) != 1

L = [tuple(order(q, p, 2) for q in (3, 5)) for p in P]
for i, j in combinations(range(4), 2):
    edge = prod(set(S[i]) & set(S[j]))
    shared = [gcd(x, y) for x, y in zip(L[i], L[j])]
    assert tuple(g // gcd(g, 2) for g in shared) == (edge, edge)

N, w = weights([p*p for p in P])
n = sum(p*b for p, b in zip(P, w)) % N
assert n == 1817788477368534308812322984345475506496837697426771014

private = [(p-1)//(2*prod(labels)) for p, labels in zip(P, S)]
M, w = weights([2, *E, *private, *P])
count = 0
for digits in product(*(range(ell) for ell in E)):
    c = sum(x*b for x, b in zip(digits, w[1:5])) % M
    d = (c+w[0]) % M
    assert c % 2 == 0 and d % 2 == 1
    assert all(c % ell == d % ell == x for ell, x in zip(E, digits))
    assert all(hit(n, p, c, d) for p in P)
    count += 1
assert count == 17017

# Pinning the private digit can invalidate a prime-level match.
p = P[0]
c, d = 0, w[0] % M
step = order(3, p, 1)
slope = (pow(3, step, p*p)-1)//p
c_bad = c + pow(slope, -1, p)*step
assert hit(n, p, c, d)
assert (n-pow(3, c_bad, p*p)-pow(5, d, p*p)) % (p*p) == 0
```

These are feasible, unrestricted simultaneous-hit panels. The width result leaves open whether large native widths can force growing **minimal inconsistency**, and it places no ordinary-height bound on the realizing exponents.