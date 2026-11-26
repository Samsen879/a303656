# At large critical width, two sectors can hit different true residuals

Take dyadic \(X\), the shifts \(S_X=\{3^c+5^d:X^{1/4}\le3^c\le X^{1/3},\ 5^d\le X^{1/8}\}\), the near-axis sector \(0\le b<wa\), and its image under \((4+3i)/5\). The shifts are distinct. If \(w(\log X)^2\to C\) for a sufficiently large fixed \(C\), every sufficiently large block has a positive fraction of integers admitting squarefree two-square residuals in both sectors, using **different** shifts. This is distinct from the [same-residual rotated overlap](THIN_SECTOR_ROTATION_CORRELATION.md) for subcritical width. The statement leaves the unrestricted small fixed \(C\) case open.

Count near-axis witnesses \(W_s(n)\) with squarefree norm and \(b\equiv3a\bmod5\), so the rotation is integral. Put \(W(n)=\sum_sW_s(n)\). By the sector sieve already proved, including the ratio \(1/7\) for the rotation lattice, \(\sum_n W(n)=(\mu+o(1))X\), where \(\mu=\kappa C/(7\cdot192\log3\log5)\) and \(\kappa\) is the squarefree coordinate density. Indeed the area per shift is asymptotic to \(Xw/2\) and the number of shifts to \((\log X)^2/(96\log3\log5)\). The union bound in the [squarefree coordinate sieve](DETERMINISTIC_THIN_SECTOR_RECOVERY.md) gives \(\kappa\ge197/900\). In particular \(X=2^k,w=60000/k^2\) has limiting \(\mu>2\). The earlier narrow-sector second-moment bound also gives \(\sum_n W(n)^2=O_C(X)\).

The equal-shift off-diagonal contribution is \(o(X)\): for each shift the zero norm gap in the line calculation gives \(O(Xw^2\log X)\) pairs of distinct coordinates, and there are \(O((\log X)^2)\) shifts. Consequently the distinct-shift ordered coordinate-pair count has liminf divided by \(X\) at least \(\mu(\mu-1)\), by Cauchy–Schwarz and subtracting the diagonal and equal-shift repetitions. For actual distinct integers, use \(\sum_n(W(n)-1)_+\ge(\mu-1+o(1))X\); Cauchy–Schwarz and \(\sum_n W(n)^2=O_C(X)\) give \(\gg_C X\) integers with at least two witnesses. Only \(o(X)\) could be explained by same-shift repetitions. Rotate one of the two witnesses on the remaining integers. This does not treat any two coordinates of the same residual as different residuals.

Conversely, one can deliberately impose a congruence partition making cross hits impossible at any width. On both sides require odd \(c\) and squarefree residual \(1\bmod8\); require odd \(d\) on the near-axis side, even \(d\) on the rotated side. The resulting hit sets have \(n\equiv1,5\bmod8\) respectively. For each fixed \(C>0\) each side still has individual positive density: the parity-restricted shifts retain logarithmic lengths, the local coordinate conditions modulo 8 and 25 are compatible, and CRT plus the squarefree tail estimate gives a positive first moment of order \(X\). The same \(O_C(X)\) second-moment upper bound applies. This partition does not rule out other unrestricted representations.

## Exact controls

At \(X=2^{38}, w=1/400\), the one integer \(277268198319\) has two distinct squarefree residuals in the near-axis sector, both rotatable. The shifts are 754 and 734. The controls at \(X=2^{19},w=1/32\) separately exhibit the two residue classes required by the congruence partition.

```python
from math import isqrt,prod
n=277268198319
for a,b,s,u,v,f in [(526562,811,754,420763,316586,(5,41,1352527793)),
                     (526561,1308,734,420464,316983,(5,55453639517))]:
    assert a*a+b*b==u*u+v*v==n-s==prod(f)
    assert 400*b<a and (5*u,5*v)==(4*a-3*b,3*a+4*b)
    assert len(set(f))==len(f)
    assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in f)
assert 528817==727**2+16**2+3**3+5
assert 528813==572**2+449**2+3**3+1
assert (528817%8,528813%8)==(1,5)
```
