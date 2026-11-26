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
