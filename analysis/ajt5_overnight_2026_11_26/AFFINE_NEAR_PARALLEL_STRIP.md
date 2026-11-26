# One shared strip can contain three incompatible lifts

Take the p-adic coordinates U=(3^c−1)/7 and V=(5^d−1)/7 for c,d≡0 mod 6 and n=2+2401(3^100+5^130). Use the three actual offsets (0,0),(6,36),(12,30). All residuals are divisible by 7. Outside U+V≡0 mod 7 their valuations are all 1. Inside that strip, substitute U=7T−W and V=W, then divide the residuals by 49. Modulo 7 the three results are 1−T, 3−T−2W, 3−T−4W. Each pair of lines meets but there is no triple intersection. Inside the strip, having all three valuations odd would require all three lines at once, so it is impossible, while each pair can have valuations 3 at an actual input as below.

The determinant bookkeeping in this example extends to any fixed finite affine label set. Display each normalized affine row as its two primitive linear coefficients and its constant. Restricting to a shared mod-p strip and dividing the surviving rows by p multiplies their augmented triple determinants by a unit times p^(-2), since the primitive strip coordinate change has determinant of valuation one. Restriction to an intersection mod-p point with dilation of both coordinates instead multiplies by a unit times p^(-1). Thus a descendant retaining an initially nonzero triple cannot continue indefinitely: its determinant valuation must fall. When all remaining augmented triple determinants vanish, all lines are parallel or pass through a common point (solve two nonparallel line equations if they exist). This bookkeeping alone is not a full distribution implementation or a claim about outer-phase complexity.

Independent replay of the actual strict controls:

```python
from itertools import product

n = 2 + 2401*(3**100 + 5**130)
R = [(0,0),(6,36),(12,30)]

def v(r):
    assert r > 0
    k = 0
    while r % 7 == 0:
        r //= 7
        k += 1
    return k

assert not any(t%7 == (3-2*w)%7 == (3-4*w)%7 == 0
               for t,w in product(range(7), repeat=2))
for c,d,want in [(72,54,(3,3,2)), (78,90,(3,2,3)),
                 (84,84,(2,3,3)), (30,12,(2,2,2))]:
    assert (3**c + 5**d - 2) % 49 == 0
    assert 4*max(max(3**(c+a),5**(d+b)) for a,b in R) < n
    assert tuple(v(n-3**(c+a)-5**(d+b)) for a,b in R) == want
```
