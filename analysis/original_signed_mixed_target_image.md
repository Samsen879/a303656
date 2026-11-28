# Exact residue image of the original #93 mixed-edge anchor



Write \(A=9^L,\ B=25^L,\ h=12B-3A-5,\ H=3A+25B\). Reducing the numerator of the #93 formula for \(t\) modulo \(2\) and \(5\) gives the exact integrality condition \(10\mid y\). With \(y=10z\),
\[
t=50z^2-hz+13(B/5)-A-1,\qquad n(z)=H+(h-3t)^2+t^2.
\]
Modulo \(3\), \(t\) is a unit for all three \(z\)-classes, \(h\equiv H\equiv1\), and \(n\equiv0\). Modulo \(32\), substitution gives \(n\equiv14\). In fact, the exact image modulo \(128\) is

| \(L\bmod4\) | Possible \(n\bmod128\) |
|---:|---|
| 1 | \(14,78,110\) |
| 2 | \(14,46,110\) |
| 3 | \(14,46,78\) |
| 0 | \(46,78,110\) |

For any fixed modulus \(m\), one may prescribe \(z\bmod m\) before choosing the sector primes. Exclude the finitely many primes dividing \(10m\), then append the parameter congruence by CRT. This multiplies the period by at most \(m\) and leaves the exponent ledger unchanged. Consequently the CRT imposition is compatible with every class in the table, including both lifts \(78,174\bmod192\) of the forced class modulo \(96\). This note does not assert the analytical construction of any particular mesh. A prescribed integer outside that forced class is inaccessible to this parametrization. An integer inside the class still has no pointwise guarantee.

The following replay verifies the complete residue table and two actual three-label targets in the different lifts modulo \(192\). The table is exhaustive because the coefficients repeat with period \(16\) in \(L\) modulo \(128\), and the polynomial depends only on \(z\bmod128\) there.

```python
rows = [{14,78,110}, {14,46,110}, {14,46,78}, {46,78,110}]
assert pow(9,16,128) == pow(25,16,128) == 1

def point(L,z):
    A,B = 9**L,25**L
    H,h = 3*A+25*B,12*B-3*A-5
    t = 50*z*z-h*z+13*(B//5)-A-1
    x = h-3*t
    return H+x*x+t*t,x,t

for L in range(1,17):
    assert {point(L,z)[0]%128 for z in range(128)} == rows[(L-1)%4]
    assert all(point(L,z)[0]%3==0 for z in range(3))

for z,want in [(1100,174),(1103,78)]:
    n,x,t = point(2,z)
    y = 10*z
    for c,d,a,b in [(5,6,x,t),(6,4,x+1,t+3),(4,5,x+3-y,t-1-3*y)]:
        assert n == 3**c+5**d+a*a+b*b
    assert n%192 == want
    print(y,n,want)
```

The two targets are `27585780689211246` and `27910999167935118`. These are exact residue controls. The two examples are three-label controls, not mesh witnesses.
