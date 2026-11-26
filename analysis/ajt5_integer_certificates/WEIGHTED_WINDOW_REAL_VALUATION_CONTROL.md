# A true odd-valuation blocker outside a positive weighted window panel

There is one actual integer \(n\) for which an active \(9\times9\) translated exponent subwindow has 62 surviving cells and weight \(475/625\) under a fixed ten-prime exact valuation-parity test. Nevertheless all 81 cells fail the true sum-of-two-squares condition at a single omitted prime 59. This finite result concerns the stated translated subwindow, not the whole exponent box or any specified asymptotic window; \(n\) has an explicit representation at the origin.

For \(11\le t\le19,\ 1\le s\le9\), put \(R_{t,s}=n-9^{29t}-25^{29s}\). For the \(n\) below, binomial expansion modulo \(59^2\) gives \(R_{t,s}\equiv-59(41t+s)\). No cell has \(41t+s\equiv0\bmod59\), so each has \(v_{59}=1\). All \(R_{t,s}\) are positive. The two axes each have step-29 orders 3 modulo 7 and 9 modulo 19, and \((t,s)=(13,4)\) has exact \(v_7=v_{19}=2\). Thus this test includes a shared small order factor and nontrivial square-modulus lifting.

A self-contained exact replay:

```python
from itertools import product

a = 2**2048 + 2959652075281432229956307366992653
b = 5186614880710251122967214263896868
n = 2 + a*a + b*b
panel = (3, 7, 11, 19, 23, 31, 43, 47, 79, 223)

def valuation(m, p):
    e = 0
    while m % p == 0:
        m //= p
        e += 1
    return e

for base in (9, 25):
    for p, order in ((7, 3), (19, 9)):
        assert next(j for j in range(1, order+1)
                    if pow(base, 29*j, p) == 1) == order

R = lambda t,s: n - 9**(29*t) - 25**(29*s)
assert valuation(R(13, 4), 7) == valuation(R(13, 4), 19) == 2
passed = []
for t, s in product(range(11, 20), range(1, 10)):
    r = R(t, s)
    assert r > 0 and r % 59**2 == (-59*(41*t+s)) % 59**2
    assert valuation(r, 59) == 1
    if all(valuation(r, p) % 2 == 0 for p in panel):
        passed.append((5-abs(t-15))*(5-abs(s-5)))
assert (len(passed), sum(passed)) == (62, 475)
```

## Exact maximal width at the fixed non-origin cell

For this same \(n\) and blocker 59, fix the anchor \((i,j)=(377,116)\) in ordinary \((9^i,25^j)\) exponents. Take strictly active square windows with independently chosen positive steps on the axes, and require odd \(v_{59}\) at every cell. The largest width is **10**. With both steps fixed at 29 the largest is **9**; if the anchor must be the lower corner with those steps, it is **7**.

For any width at least two on both axes, comparing successive cells on each axis modulo 59 forces both steps to be multiples of 29, since both multiplicative orders are 29. Thus both initial coordinates are also multiples of 29, since the specified anchor is in the window. The proof is a small complete enumeration with no bound on the original steps assumed: for \(n\) above, each coordinate alone must have \(9^{29t}<n\) or \(25^{29s}<n\), giving respectively \(0\le t<45,\ 0\le s<31\). For each positive step and each possible location of the anchor \((13,4)\) inside the window, subtract step times location to get the origin, and check positivity at the upper corner and the exact valuation of every cell. The width-10 witness is \(t=10+3u,\ s=2+2v\) for \(0\le u,v<10\). Exactly 192 width-11 windows are active; none has all valuations odd. Similarly with both scaled steps one, 45 width-nine windows are active (four blocked), and 50 width-ten windows are active (none blocked). For the lower-corner test, widths seven and eight have one active window each, and only width seven is blocked. Any larger active blocked window would contain a smaller one through the same anchor.

More generally, if \(q\) is an odd prime not dividing 15 and both ordinary steps are multiples of the corresponding orders, the divided residual modulo \(q\), starting from an activated corner, is affine in the two step counts. If both coefficients are nonzero, an all-\(v_q=1\) rectangle of side lengths \(M,N\) must have \(M+N\le q\): when an axis covers all classes it hits the excluded line, and otherwise the two residue sets of sizes \(M,N\) cannot avoid translating into each other if their sizes sum to more than \(q\). This last bound concerns valuation exactly one, not all odd valuations; the exact width-10 enumeration above tests all odd valuations.

## Growing active windows with one fixed surviving anchor

For each sufficiently large prime \(q\equiv3\bmod4\), let \(D=(q-1)/2,\ X=2^{q^2-1}\), \(W\) be the largest odd integer at most \(\sqrt{q-1}\), and write \(h=9^{377}+25^{116}\). There exists an actual integer \(n=2+u^2+v^2\in[X,2X)\) with the following properties:

1. At the fixed anchor the residual \(n-h\) is positive and is a unit at every prime \(p\equiv3\bmod4,\ p\le\sqrt{\log n}\). The \(\log\) is natural.
2. Every cell \(0\le i,j<W\) at exponents \((377+Di,116+Dj)\) is strictly active, with residual of exact \(q\)-valuation 1. Here \(q>\sqrt{\log n}\) is outside the observed panel.
3. The origin remains an explicit true norm. The guaranteed window width satisfies \(W/(\log n)^{1/4}\to(\log2)^{-1/4}\).

Indeed, \(9^D,25^D\equiv1\bmod q\). The \(W^2<q\) offsets have at most \(W^2\) divided shifts \((9^{377+Di}+25^{116+Dj}-h)/q\bmod q\), so choose a missing \(k\bmod q\) and set \(n\equiv h+qk\bmod q^2\). For all sufficiently large \(q\), this is a unit target for the norm \(n-2\), since \(q\nmid h-2\). Every nonzero target modulo \(q\) has a two-square representation by the finite-field norm map, and a coordinate with nonzero derivative lifts it modulo \(q^2\). Separately, for every \(p\equiv3\bmod4,\ p\le\sqrt{\log(2X)}\), prescribe \(u,v\equiv0,0\bmod p\) if \(h\not\equiv2\bmod p\), and \(1,0\bmod p\) otherwise. This enforces \(n-h\not\equiv0\bmod p\). These are independent from \(q\) because \(\sqrt{\log(2X)}=q\sqrt{\log2}<q\).

The common coordinate modulus has logarithm \(O(q\log q)\), even counting all integers in the panel as potential primes. Choose \(u\) between \(\sqrt X\) and \(\sqrt X\) plus one modulus, and \(v\) between zero and one modulus. This has \(X\le n<2X\) for sufficiently large \(q\). Since the maximum exponent is \(O(q^{3/2})\), all cells are active. The omitted \(k\) forces their exact valuation 1, whereas the panel at the anchor only sees units. This growing statement concerns one fixed observed survivor, not a positive density of survivors in the full box.

A finite control for this exact version is \(q=167,\ D=83,\ W=11,\ k=11,\ v=0\), and
\[
u=2^{13944}+6532292378186422400920212684040670 .
\]
Direct modular exponentiation verifies the panel (through prime 139), the stated height range, and exact valuation 1 on all 121 cells. This control is independent of the earlier \(q=59\) construction.
