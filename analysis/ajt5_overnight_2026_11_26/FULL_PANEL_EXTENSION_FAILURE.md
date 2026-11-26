# Full finite-panel data cannot certify the selected true norm

This extends the two-point example in [ACTUAL_LIFT_CONFLICTS.md](ACTUAL_LIFT_CONFLICTS.md). Even keeping complete old residues at arbitrarily high fixed depths and preserving the entire ordinary positive window does not guarantee that its unique finite optimum is a sum of two squares.

## Concrete two-point example

For even \(D\ge12\), take \(n^+=5^D+170231714\) and \(n^-=5^D+272969426\). The positive residuals starting at \((14,D)\) with steps \((2,2)\) are exactly:

| Point | At \(n^+\) | At \(n^-\) |
| --- | --- | --- |
| \((14,D)\) | \(308^2+12859^2\) | \(1309^2+16324^2\) |
| \((16,D)\) | \(817^2+11248^2\) | \(5\cdot17\cdot19^2\cdot59\cdot127\) |

The complete valuations at inert primes up to 58 are identical at corresponding points. The finite optimum still chooses \((16,D)\) with cost 19 over cost 77, but at \(n^-\) that point fails the square-sum test at 59 and 127. The first point remains a genuine representation at that same \(n^-\).

## Any fixed panel, with specified missed primes

Let \(Q\) be any fixed finite panel of inert primes greater than 3 containing \(7,11,19\), and fix read depths \(k_p\ge3\). Independently specify a nonempty finite set of missed inert primes \(q>3\) outside \(Q\). Put \(M=8\prod_{p\in Q}p^{k_p}\); use integer vectors
\[
 a=(308,12859),\qquad b=(817,-11248),\qquad h=(24107,509).
\]
They satisfy \(h\cdot(a-b)=0\) and \(\|a\|^2-\|b\|^2=8\cdot3^{14}\).

Take \(t\) tending to infinity through multiples of \(\varphi(M)\), and set \(s=3^t,\ C=14+2t,\ D=10+2t\). Set \(A=sa+Mh,\ B=sb+Mh\). Their squared norm difference is exactly \(8\cdot3^C=3^{C+2}-3^C\); hence \(n^+=5^D+3^C+\|A\|^2\) has true representations at both points.

Construct \(A'=A+3M(u,v)\) so that \(\|A'\|^2\equiv8\cdot3^C+q\bmod q^2\) for each specified \(q\). The prescribed residue is nonzero mod \(q\). Every residue mod \(q\) is a sum of two squares: the squares and a translate of their negatives each have size \((q+1)/2\) in a set of size \(q\), so they intersect. Here at least one of the two coordinates is nonzero mod \(q\), and changing that coordinate by a multiple of \(q\) supplies the required lift mod \(q^2\). As \(3M\) is invertible at each missed prime, CRT provides \(u,v\) bounded independently of \(t\).

Set \(n^-=5^D+3^C+\|A'\|^2\). It shares the whole residue table of \(n^+\) at the old moduli, because \(n^--n^+\equiv0\bmod M\) independently of the exponent pair subtracted. At the two corresponding points, those old residues are the original ones: \(s\equiv1\bmod M\) and the residuals at \(n^+\) are the respective norms of \(A,B\). Thus the unique finite optimum is still the second point. Its residual at \(n^-\) has valuation exactly 1 at every specified \(q\). The first point at \(n^-\) is a true norm by construction.

For both targets, \((n^\pm-5^D)/3^{2t}\to170231714\) and \(5^D/3^{2t}\to\infty\). Because \(3^{16}<170231714<3^{18}\), for all sufficiently large \(t\) the window starting at \((C,D)\) with steps \((2,2)\) is exactly \((C,D),(C+2,D)\): the next step on either axis makes the residual nonpositive. The construction concerns every *fixed finite* panel, with the size of the eventual example allowed to depend on the panel. It does not rule out a size-dependent or factored residual certificate.

```python
from math import isqrt
def v(r,p):
    e=0
    while r%p==0:
        r//=p
        e+=1
    return e

def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

C0,C1=170231714,272969426
assert 3**16<C0<C1<3**18 and 24*5**12>C1-3**14
r=[[c-3**j for j in (14,16)] for c in (C0,C1)]
assert r==[[308**2+12859**2,817**2+11248**2],
           [1309**2+16324**2,5*17*19**2*59*127]]
for p in (p for p in range(3,59,4) if prime(p)):
    assert [v(R,p) for R in r[0]]==[v(R,p) for R in r[1]]
assert v(r[1][1],59)==v(r[1][1],127)==1
assert 24107*(308-817)+509*(12859+11248)==0
assert r[0][0]-r[0][1]==8*3**14
```
