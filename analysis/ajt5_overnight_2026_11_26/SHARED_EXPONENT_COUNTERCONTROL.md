# Marginal local survival does not imply a shared edge

Set m = 22207 and r = 2. For the actual shared index pair c ≡ 2 and d ≡ 0 (mod 6), let P = m − 3^c − 5^d and C = 5m+r − 3^c − 5^d. As an old condition require E = m − 3^(c+6) − 5^d to have odd 7-adic valuation. All three residuals are divisible by 7 throughout the specified index class, by reduction modulo 7. The difference C−P = 88830 has valuation exactly 1 at 7. Thus the two endpoints cannot both pass the local odd-valuation obstruction, even allowing zero as a pass: either valuation at least 2 forces the other to be exactly 1. In contrast, each marginal passes on a nonempty stable cylinder within the old condition. For pairs (2,0) and (2,6), the valuation triples (E,P,C) are respectively (1,2,1) and (1,1,2). These actual integer points have all residuals positive. The cylinders refer to exponent-space local conditions, not to simultaneous positivity of residuals for unbounded integers at fixed m.

Minimal replay (Python 3, standard library only):

```python
def v7(x):
    assert x > 0
    j = 0
    while x % 7 == 0:
        x //= 7
        j += 1
    return j

m = 22207
assert v7(4*m + 2) == 1
for d, expected in [(0, (1, 2, 1)), (6, (1, 1, 2))]:
    assert tuple(map(v7, (m-3**8-5**d, m-9-5**d, 5*m+2-9-5**d))) == expected
```

This only refutes an inference from positive marginals to simultaneous survival for a prescribed local edge. It does not refute a statement about an entire menu or the original conjecture.
