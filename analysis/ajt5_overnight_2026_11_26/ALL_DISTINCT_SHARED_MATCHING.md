# All-distinct shared-coordinate labels and four ordinary-ratio candidates

At \(K=24226088\), the four triples \((c,d,x)\)
\[
 (1,0,4922),\quad(9,1,4920),\quad(11,7,4896),\quad(15,10,334)
\]
satisfy \(3^c+5^d+x^2=K\), with distinct indices on each axis and distinct offsets. In the same block, every odd \(3001\le t\le4501\) gives a different actual \(n=K+t^2\) in \((K,2K)\) with four true labels. This is a finite ordinary-height control, not an unbounded family with all eight powers of order \(K\).

## Reduction under a high-ratio hypothesis

For any four all-distinct labels sharing \(K\), put \(a=\min_i c_i,\ b=\min_i d_i,\ A=3^a,\ B=5^b,\ m=\min(A,B)\). Suppose \(a,b\ge2\) and \(K<3125m\). Mod 4 all \(c_i\) have the same parity, since \(3^c+5^d+x^2\bmod4\) for even and odd \(c\) lie in disjoint sets. The height bound then forces the ordered \(c\)'s to be \(a+(0,2,4,6)\): span 8 would give \(3^8A>K\). The \(d\)'s span at most 4 and must have both parities. Mod 3 this forces \(K\equiv2\) and \(3\mid x_i\) at the odd \(d_i\). Two odd \(d_i\)'s would thus have equal powers mod 9, requiring their difference to be divisible by 6, impossible within span 4. Consequently \(b\) is even, and the set of \(d-b\) values is \(\{0,1,2,4\}\) or \(\{0,2,3,4\}\).

If \(a\) were odd, the four \(3^{c_i}\) would alternate between 2 and 3 mod 5. Their shifted square residue sets intersect only at 2 and 3; thus the two \(x_i\)'s of one of these classes must vanish mod 5. The associated \(c\)'s differ by 4, and mod 25 (where the 5-powers vanish) this would require \(3^4=1\bmod25\), impossible. Hence \(a\) is even. Mod 8 with both \(d\) parities now forces all \(x_i\) even. Divide the congruences mod 256 by the odd square \(A\); the square set of even residues is preserved, and \(B/A\equiv1\bmod8\). The exact finite remainder test below leaves only:
 
| \(d-b\) paired with increasing \(c\) | Necessary \(K/m\) |
| --- | ---: |
| \(0,2,4,3\) | 854 |
| \(2,4,3,0\) | 730 |
| \(3,0,2,4\) | 1354 |
| \(4,3,0,2\) | 754 |

The numerical bounds are the maxima of \(3^{2i}+5^{d_i-b}\), because \(A,B\ge m\). These are necessary residue-and-weight restrictions, not guarantees that any candidate has an integer lift.

In any \([X,2X]\) where every power is at least \(\eta X\) with fixed \(\eta>0\), only \(O_\eta(1)\) exponent tuples are possible. Distinct two-axis labels there cannot have the same offset for large \(X\): \(v_3(5^d-5^{d'})\) is zero for odd exponent difference and \(1+v_3(d-d')\) otherwise, incompatible with a smaller 3-power at least \(\eta X\). For each candidate tuple, two distinct offsets bound the admissible \(K\)'s by the divisor count of their difference via difference of squares. Varying \(t\) then gives at most \(O_{\eta,\varepsilon}(X^{1/2+\varepsilon})\) distinct \(n\) in this specific common-coordinate model.

```python
from itertools import permutations

a = (1, 9, 81, 729)
sq = {x*x % 256 for x in range(0, 256, 2)}

def allowed(p):
    for r in range(1, 256, 8):
        pools = [{(s+u+r*5**d) % 256 for s in sq}
                 for u,d in zip(a,p)]
        if set.intersection(*pools):
            return True
    return False

assert not any(allowed(p) for p in permutations((0,1,2,4)))
rows = [p for p in permutations((0,2,3,4)) if allowed(p)]
assert rows == [(0,2,4,3), (2,4,3,0), (3,0,2,4), (4,3,0,2)]
assert [max(u+5**d for u,d in zip(a,p)) for p in rows] == [
    854, 730, 1354, 754
]

K = 24226088
rows = [(1,0,4922), (9,1,4920), (11,7,4896), (15,10,334)]
assert len({3**c+5**d for c,d,x in rows}) == 4
for t in range(3001,4502,2):
    n = K+t*t
    assert K < n < 2*K and n%2
    assert all(n-3**c-5**d == x*x+t*t for c,d,x in rows)
```
