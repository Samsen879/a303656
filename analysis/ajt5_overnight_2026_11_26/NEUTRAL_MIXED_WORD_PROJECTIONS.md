# Mixed-word projection tests in the neutral-depth chart

In the [neutral finite reduction](https://github.com/Samsen879/a303656/commit/127f12218184d3880aa8f0ac1da0a643c4c1a9f2), a retained order-343 root \(x\) at an eligible prime \(q\) can be combined with the actual 7-primary projections of 3 and 5. A phase tag \((e,k)\) prescribes \(\pi(3)=x^E,\ \pi(5)=x^{kE}\) for some lift \(E=e\bmod49\). Testing the two projections independently would lose the requirement of the same lift.

For an invertible word \(W=3^u5^v\), a 7-free mask \(L\), and a power \(H\) covering the anticipated 7-parts of \(q-1\), take \(d=\gcd(R,W^{LH}-1)\) on the composite support \(R\). At every prime divisor \(q\) of \(d\), \(W^L\) is 7-primary. Hence a viable tag must have
\[
W^L=x^{LE(u+kv)}\pmod q.
\]
Gcds can compare these congruences on an entire support. Two captured words with coefficient determinant prime to 7 determine the two projection logs modulo 343 at a prime with known root \(x\).

The first representative control has two actual primes with the same progression modulo 9604, same canonical source polynomial \(1+X^{71}-X-X^{54}\), and a unique contributing root congruent to the same recorded \(x\) at each prime. Both pass the local order and base-5 3-part conditions, but their projection logs are \((37,276)\) and \((37,305)\). This demonstrates why the canonical root and axis orders alone do not determine the phase. The second control shows an exact mixed-word capture when both individual axes escape the given mask. Its two words recover \((6,213)\). These are representative arithmetic tests, not an exhaustive audit of remaining resultants.

~~~python
from math import gcd, isqrt, lcm

R, x = 4586217387831944145793, 3884197799753059807579
for p, f in [(23065993343, 276), (198830257151, 305)]:
    assert R % p == 0 and all(p % d for d in range(2, isqrt(p) + 1))
    assert p % 9604 == 8919 and (p - 1) % 2401
    s, y = (p - 1) // 343, x % p
    assert pow(y, 343, p) == 1 and pow(y, 49, p) != 1
    assert [i for i in range(1, 343) if i % 7 and
            (1 + pow(y, 71*i, p) - pow(y, i, p) - pow(y, 54*i, p)) % p == 0] == [1]
    assert [pow(b, s, p) for b in (3, 5)] == [pow(y, s*j, p) for j in (37, f)]
    assert f % 7
    while s % 3 == 0:
        s //= 3
    assert pow(5, 9*343*s, p) == 1

R, p, x = 130689417709172543704281625219807, 1657123728989, 60816513812818033159421809301459
L, H = lcm(*range(1, 4001)), 1
while L % 7 == 0:
    L //= 7
while 7*H <= R // 4_000_000_000:
    H *= 7
assert all(gcd(R, pow(b, L*H, R)-1) == 1 for b in (3, 5))
for u, v, j in [(3, 5, 218), (-32, 3, 242)]:
    W = pow(3, u, R)*pow(5, v, R) % R
    assert gcd(R, pow(W, L*H, R)-1) == p
    assert pow(W, L, p) == pow(x, j, p) and L*(6*u + 213*v) % 343 == j
assert gcd(169, 343) == 1
~~~
