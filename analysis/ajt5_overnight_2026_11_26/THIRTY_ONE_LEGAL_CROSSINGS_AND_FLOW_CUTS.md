# Legal strip crossings and count-allocation cuts for the 31-sink

**The mixed-strip overlap can be counted exactly.** On the full \(31\)-chart, this gives a stronger joint cover test and an orientation restriction: if at most 59 mixed readers cover the chart without doubly deep help, one orientation must cover every lower pair not already removed by shallow readers. At the 46-reader threshold for a mixed-only full chart, all 46 must have that orientation, with only five strip incidences to spare.

### Count the legal crossings

Remove the lower pairs hit by shallow readers. Before their observations are fixed, the shallow matching test bounds how many pairs they can remove. In each remaining lower pair \(i\), the source excludes one upper cell in every row and column. Write this excluded permutation as \(b=\pi_i(a)\). It comes from the affine equation modulo \(31^3\) for the upper digits, whose two coefficients are nonzero at the doubly ordinary source. [Predecessor repair chart](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

Let \(A_i,B_i\) be the **distinct** row and column digits struck by actual mixed readers. Write \(a_i=|A_i|\), \(b_i=|B_i|\). The exact number of legal cells left is
\[
R_i=930-30(a_i+b_i)+a_i b_i-|\pi_i(A_i)\cap B_i|.
\]
The last two terms count the legal crossings that were subtracted twice. Repeated strips on one axis are collapsed before counting. Each crossing can be checked from the two readers’ actual common lower pair and their upper digits.

For any set \(J\) of surviving lower pairs, a full cover requires
\[
\sum_{i\in J}R_i
\ \le\
\sum_{p\ {\rm doubly\ deep}}
\min\!\left(C_p,\ \sum_{i\in J}\min(2,R_i,31-a_i,31-b_i)\right),
\]
where \(C_p=62\), or \(31\) for an aligned reader. A doubly deep reader can hit at most two cells in a lower pair, and its hits there use distinct rows and columns. These inequalities are the cuts of one capacitated reader-to-block flow. Passing them certifies a feasible allocation of **counts**. Certifying a cover still requires the reader hits to occupy the assigned cells.

### What strip supports alone can prove

If only the readers’ lower support sets are known, let \(x_i,y_i\) be the active counts by orientation, capped at 31. The sharp bound in the strip-incidence model is
\[
R_i\ge(31-x_i)(31-y_i)-\min(31-x_i,31-y_i).
\]
It is attained in that model by taking distinct strips and nesting the two surviving coordinate sets under \(\pi_i\).

A lower pair can be completely covered by mixed strips if one orientation strikes all 31 coordinates, or if both leave exactly one coordinate and their surviving crossing is excluded. The latter takes **60 distinct strips**. Thus with at most 59 mixed readers, one orientation must strike all 31 coordinates in each remaining lower pair. Only one orientation can have 31 readers in such a panel, so it must do so on every remaining pair.

In particular, for a full chart with 46 mixed readers and no shallow help, all 46 must have the same orientation. The \(46\cdot21-31^2=5\) spare incidences pay for both unused reader capacity and duplicate strips. At least 41 readers must strike 21 lower pairs. The abstract assignment of row \(a\) in block \(i\) to reader \((31i+a)\bmod46\) attains this boundary using only the 21-strip and one-strip-per-block rules. A larger universal threshold therefore needs additional arithmetic.

### Same-target \(3,5\) controls

The replay uses one target and one chart. The shallow readers \(311,683\) remove four lower pairs. The fixed mixed reader \(21143\) strikes row 0 in lower pair 30. Each comparison reader strikes a column **only** in lower pair 30.

| Comparison reader | Column | Crossing with row 0 | Survivors on full chart |
|---|---:|---|---:|
| \(86491\) | 19 | Excluded | 25,050 |
| \(355571\) | 0 | Legal | 25,051 |

The controls have identical lower supports and opposite answers to the legal-overlap test. All observations are nonzero and all hits have exact valuation one. These ordinary controls establish the finite-chart distinction. The cover test is conditional on the frozen chart and gives no density subtraction by itself.

```python
from collections import Counter
from math import isqrt

r, p, q, t = 31, 21143, 86491, 355571
W = 307654935875658360 * 962 * q * t
n = 1492554032931413599145569413292041970079174515790883
depths = {311:(1,1), 683:(1,1), p:(2,1), q:(1,2), t:(1,2)}

def S(x,y,m):
    return (pow(3,2+W*x,m) + pow(5,3+W*y,m)) % m

for z, ds in depths.items():
    assert z%4 == 3 and all(z%d for d in range(2,isqrt(z)+1))
    for b, d in zip((3,5),ds):
        assert pow(b,z-1,z*z) != 1
        assert pow(b,W*r**d,z*z) == 1
        assert pow(b,W*r**(d-1),z) != 1

assert W%3960 == 0 and W%r
assert all(pow(b,30,r*r) != 1 for b in (3,5))
assert (n%32,n%3,n%r**3) == (3,0,1095)
assert all((n-S(0,0,z))%z for z in (7,11,19,23))
assert [n%z for z in depths] == [178,57,18768,5465,31133]

shallow = {z:set() for z in (311,683)}
strips = {z:set() for z in (p,q,t)}
survivors, cells = Counter(), 0
for i in range(r):
    j, = [j for j in range(r) if S(i,j,r*r) == n%(r*r)]
    assert j == 14*i%r
    for z in shallow:
        if S(i,j,z) == n%z:
            shallow[z].add(i)
    seam = {}
    for a in range(r):
        b, = [b for b in range(r)
              if S(i+r*a,j+r*b,r**3) == n%r**3]
        seam[a] = b
    assert len(set(seam.values())) == r
    if i == 30:
        assert seam[0] == 19
    for a in range(r):
        for b in range(r):
            if b == seam[a]:
                continue
            x,y = i+r*a,j+r*b
            cells += 1
            hit = {z for z in depths if S(x,y,z) == n%z}
            assert all(S(x,y,z*z) != n%(z*z) for z in hit)
            for z,digit in ((p,a),(q,b),(t,b)):
                if z in hit:
                    strips[z].add((i,digit))
            for z in (q,t):
                if hit.isdisjoint((311,683,p,z)):
                    survivors[z] += 1

assert cells == 28830
assert shallow == {311:{20,24},683:{9,19}}
assert strips == {p:{(20,13),(30,0)},q:{(30,19)},t:{(30,0)}}
assert survivors == {q:25050,t:25051}
hist = Counter((31*i+a)%46 for i in range(31) for a in range(31))
assert Counter(hist.values()) == {20:5,21:41}
```

A sufficiently large common CRT translate of the replay target makes every remainder in the finite chart positive while preserving both controls.

Independent BigInt replay checked each excluded permutation, all 28,830 legal cells, and the comparison survivor counts 25,050 and 25,051. The flow test assigns counts only; it does not decide whether hits from different readers coincide at the same legal cells.
