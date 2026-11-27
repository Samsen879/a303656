# Four shared-coordinate labels and a two-axis height obstruction

A genuine small example, with four **different** offsets, is
\[
 770=1+625+12^2=81+625+8^2=729+5+6^2=729+25+4^2.
\]
Every odd \(9\le t\le23\) gives a different \(n=770+t^2\) with all these true labels and common square coordinate \(t\), in the ordinary interval \(730<n<1354\).

There is a growing example with four labels but only three distinct numerical residuals. For \(B=5^b,\ b\ge2,\ K=B^2+28\), use \(28=3+25=27+1\). For \((c,d)=(1,2),(3,0),(1,2b),(3,2b)\), the respective complements \(K-3^c-5^d\) are \(B^2,B^2,5^2,1\). Hence every even \((B+3)/2\le t\le B-1\) yields \(n=K+t^2\) with four valid labels, a total of \((B-1)/4\) distinct such \(n\asymp B^2\). Here the 3 exponents stay bounded.

## Repetition of both axes at ordinary height is obstructed

Fix \(K\) and require \(K-3^c-5^d\) to be a nonnegative square at each label. Suppose two labels share \(d_*\) and have different 3 exponents, the smaller 3-power \(A_0=3^a\); suppose a pair of labels share \(c_*\) but use different 5 exponents, the smaller 5-power \(B_0=5^b\). It is not required that \((c_*,d_*)\) is one of the labels. Put
\[
 A_*=\min(A_0,3^{c_*}),\qquad B_*=\min(B_0,5^{d_*}).
\]
Then \(A_*B_*\le4K^{3/2}\).

For the first pair write the square-root difference as
\((u-v)(u+v)=3^a(3^{\Delta c}-1)\). The two factors have total 3-adic valuation \(a\), and are at most \(2\sqrt K\). If \(h\) is the smaller valuation, the other factor contains \(3^{a-h}\le 2\sqrt K\), so \(3^{2h}\ge A_0^2/(4K)\). Both \(u,v\) are divisible by \(3^h\), so \(K-5^{d_*}\) is divisible by \(3^{\min(a,2h)}\). Similarly \(K-3^{c_*}\) is divisible by a 5-power at least \(B_0^2/(4K)\), after the corresponding truncation at \(b\). Truncate the 3 modulus at \(c_*\) and the 5 modulus at \(d_*\). These moduli are at least \(A_*^2/(4K)\), \(B_*^2/(4K)\), because all powers in the given labels are at most \(K\). They are coprime and both divide \(K-3^{c_*}-5^{d_*}\). The latter integer is nonzero: if it vanished, a label in row \(d_*\) with 3 index different from \(c_*\) would require a difference of distinct 3-powers to be a square. A positive such difference is not a square since its 3-free unit part is \(2\bmod3\). Its absolute value is at most \(K\), proving the bound.

If all four powers involved in \(A_*,B_*\) are at least \(\eta K\), then \(K\le16\eta^{-4}\). This excludes unbounded same-coordinate ordinary-height families with repetition on both axes, including full rectangles. It says nothing about all-distinct matching or allowing different square coordinates.

```python
rows = [(0,4,12), (4,4,8), (6,1,6), (6,2,4)]
assert len({3**c + 5**d for c,d,x in rows}) == 4
for t in range(9,24,2):
    n = 770 + t*t
    assert 730 < n < 1354
    assert all(n-3**c-5**d == x*x+t*t for c,d,x in rows)

for b in (2,3,15):
    B = 5**b
    rows = [(1,2,B), (3,0,B), (1,2*b,5), (3,2*b,1)]
    lo, hi = (B+3)//2, B-1
    assert lo%2 == hi%2 == 0 and (hi-lo)//2+1 == (B-1)//4
    for t in (lo,hi):
        n = B*B + 28 + t*t
        assert 5*B*B < 4*n < 12*B*B and n%2
        assert all(n-3**c-5**d == x*x+t*t for c,d,x in rows)
```
