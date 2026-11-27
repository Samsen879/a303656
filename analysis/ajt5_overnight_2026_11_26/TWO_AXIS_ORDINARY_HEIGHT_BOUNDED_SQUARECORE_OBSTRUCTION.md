# An ordinary-height two-axis obstruction to bounded squarecore selection

This continues [the three-label ordinary-height selector](https://github.com/Samsen879/a303656/commit/629ade482f820d22869f07ded0b2f19dc89b2896). A broad target family specified solely by local tests contains \(X^{1-o(1)}\) integers that have true witnesses at a chosen menu label yet fail every bounded-small-cofactor choice, even outside that menu. This does not show that every local target has a witness. In the genuine-witness count, the chosen label may be the upper corner of the menu, so both actual exponents tend to infinity. The enlarged gate is tested against **all nonnegative exponent pairs with positive remainder**. Its failure is not an obstruction to representations themselves.

Independently replayed both native \(H=224\) inputs, the raw changes on both axes, all four surviving panel rows, and all 13,675 ordinary-height candidates on the matched failing input. The asymptotic count uses only the finite-field norm count, CRT, the elementary representation bound and fixed-modulus prime asymptotics. At an inert prime the two coordinates of a nonzero norm run through exactly \(p+1\) pairs; even the head-conditioned coordinate box has side much longer than the CRT modulus, allowing direct counting without an unproved independence assumption across different labels.

**The small-cofactor gate misses almost all targets in an explicit growing two-axis valuation family.** At scale \(X\), the family contains \(X^{1-o(1)}\) distinct targets with a genuine two-square witness at a specified menu label. Only \(X^{1/2+o(1)}\) targets can pass the gate at **any** positive exponent pair, even if the gate may first strip arbitrary powers of every prime through the cutoff. The target family is defined by local tests alone.

### The two-axis menu

Take \(X=2^H\) for even \(H\), and define
\[
Y=\lfloor H/16\rfloor,\qquad K=\max(8,\lfloor(\log_2 H)/4\rfloor),\qquad
m=\lfloor\sqrt{K/2}\rfloor .
\]
Use the full inert panel through \(Y\). Set \(L\) to the lcm of \(72\) and the numbers \(p-1\) for inert primes \(7\le p\le K\). The menu consists of the pairs
\[
(c_i,d_j)=(3+iL,1+jL),\qquad 0\le i,j<m.
\]
Both axes grow. The elementary bound \(\operatorname{lcm}(1,\ldots,K)\le4^K\) gives \(mL=o(H)\), so every menu remainder is positive for \(X/2\le n<X\) once \(H\) is sufficiently large.

Define the target set \(\mathcal T_X\) by \(n\equiv1\bmod32\), \(n\equiv14\bmod27\), and
\[
n\bmod p\notin S_p,\qquad
S_p=\{3^{c_i}+5^{d_j}\bmod p:0\le i,j<m\}
\]
at every inert \(7\le p\le Y\). Every menu remainder is \(1\bmod32\), has exact valuation two at \(3\), and is a unit at the other panel primes. For \(p\le K\), \(|S_p|=1\), and for \(p>K\), \(|S_p|\le m^2\le K/2\). The CRT density is therefore
\[
\delta=\frac1{32\cdot27}\prod_{7\le p\le Y,\ p\equiv3(4)}
          \left(1-\frac{|S_p|}{p}\right)
       \ge \exp[-O((\log H)^2)].
\]
The product is over primes. The CRT modulus is \(X^{1/8+o(1)}\) or smaller, so \(|\mathcal T_X|=X^{1-o(1)}\).

This really changes raw reads on both axes. The primes where at least one first step freezes divide \((3^L-1)(5^L-1)\), so their total log mass is at most \(L\log15=o(Y)\). The panel has log mass \(\sim Y/2\). The fixed-modulus prime number theorem also gives \(q_1q_2=O(Y^2)\) for the first two omitted inert primes. [Explicit bounds for primes in arithmetic progressions, v3](https://doi.org/10.1112/S0010437X12000802)

### The gate obstruction

Give the selector the more permissive test
\[
R=h t^2u,\qquad 1\le u<B,
\]
where \(h\) is any integer supported on primes at most \(Y\). This includes the earlier square-divisor gate and removal of all certified small prime powers. For each label, the number of possible remainders at most \(X\) is at most
\[
\sqrt X\sum_{u<B}u^{-1/2}\prod_{p\le Y}(1-p^{-1/2})^{-1}
 \le 2\sqrt{XB}\exp(O(\sqrt Y)).
\]
There are \(O(H^2)\) nonnegative exponent pairs with positive remainder across the entire window. With \(B=q_1q_2\), the total is \(X^{1/2+o(1)}\). The same count rules out covering \(X^{1-o(1)}\) targets with any threshold \(B\le X^{1-\epsilon}\) for fixed \(\epsilon>0\).

There are also \(X^{1-o(1)}\) **genuine witnesses** among the targets the gate misses. To see this, fix any one menu label with shift \(s=3^c+5^d\), and count \(n=s+a^2+b^2\) with \(a,b\in[\sqrt X/2,5\sqrt X/8]\). At each inert panel prime \(p\ge7\), every allowed nonzero norm value has \(p+1\) coordinate pairs over \(\mathbb F_p\), by surjectivity of the norm from \(\mathbb F_{p^2}\). The allowed fraction of coordinate pairs is thus at least \(1-|S_p|/p\). At the head, take \((a,b)\equiv(1,0)\bmod32\) and \((3,0)\bmod27\). The coordinate box is longer than the CRT modulus on each axis, giving \(\gg X\delta\) pairs. Each target has at most \(4\tau(n-s)=X^{o(1)}\) pairs. Subtracting all gate hits leaves \(X^{1-o(1)}\) distinct targets with a true witness at the specified label and no gate hit anywhere in the positive exponent window.

### Matched exact replay

The two inputs below have the same reads mod \(32\) and every panel \(p^3\), and all four labels survive. Both have a true witness at \((75,73)\). The first passes the gate there. The second fails even the enlarged gate at all **13,675** nonnegative exponent pairs with positive remainder.

```python
from itertools import product
from math import gcd, isqrt, prod

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

def powers(base, stop):
    value = 1
    while value < stop:
        yield value
        value *= base

H, Y = 224, 14
X, T = 1 << H, 1 << (H // 2)
panel = [7, 11]                 # 3 is handled mod 27
menu = [3**c + 5**d for c, d in product((3, 75), (1, 73))]
S = 3**75 + 5**73
assert len(set(menu)) == 4
assert (3**75 - 3**3) % 11 and (5**73 - 5) % 11

residues = {32: 1, 27: 3}
for p in panel:
    residues[p**3] = next(a for a in range(1, p)
                          if all((S + a*a - s) % p for s in menu))
M = prod(residues)
a0 = sum(a*(M//m)*pow(M//m, -1, m) for m, a in residues.items()) % M

def lift(lo, r):
    return lo + (r-lo) % M

a = lift(3*T//4, a0)
b, c = lift(T//2, a0), lift(T//2, 0)
hit, miss = S+a*a, S+b*b+c*c
assert hit != miss and (hit-miss) % M == 0
for n in (hit, miss):
    assert X//2 <= n < X
    for s in menu:
        R = n-s
        assert R > 0 and R % 32 == 1 and R % 27 == 9
        assert all(R % p for p in panel)

assert [p for p in range(Y+1, 24) if p % 4 == 3 and prime(p)] == [19, 23]
small = [p for p in range(2, Y+1) if prime(p)]
Q = prod(small)
cofactors = [u for u in range(1, 19*23) if gcd(u, Q) == 1]

def gate(R):
    # Stripping all small factors is exact for the enlarged gate.
    for p in small:
        while R % p == 0:
            R //= p
    for u in cofactors:
        v, r = divmod(R, u)
        if r == 0 and isqrt(v)**2 == v:
            return True
    return False

assert gate(hit-S)
checked = 0
for v in powers(3, miss):
    for w in powers(5, miss-v):
        assert not gate(miss-v-w)
        checked += 1
assert checked == 13675 and miss-S == b*b+c*c
print(hit, miss, checked)
```

The obstruction applies to bounded cofactors after square and small-prime removal. It leaves open selection methods that certify a large nonsquare norm factor or certify the full remainder by another route.
