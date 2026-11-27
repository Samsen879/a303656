# Two-digit survivor grids with exclusive and shared readers

**Two order digits give a product saving even with overlapping old readers.** The shared readers can be fixed first. Their effect is bounded by how many cells they can delete, and the probability bound multiplies only the charges from the two exclusive reader groups. The same geometry gives a deterministic obstruction test that can succeed when both one-digit counts are inconclusive.

### Two-digit bound

At an inert terminal prime \(q\), choose distinct odd prime powers \(r^a,s^b\) dividing the order of the **same** base, 3 or 5. Vary digit \(a-1\) at \(r\) and digit \(b-1\) at \(s\) of that exponent, keeping all other coordinates fixed. Assume both source rows leave these digits free. This holds for split sources and for a source equal to the moved base, whose power has stabilized to zero there.

Partition the old inert rows into \(\mathcal A\), which read only the \(r\)-digit, \(\mathcal B\), which read only the \(s\)-digit, and \(\mathcal C\), which read both. Put
\[
S_{\mathcal A}=\sum_{p\in\mathcal A}\frac1{p+1},\qquad
S_{\mathcal B}=\sum_{p\in\mathcal B}\frac1{p+1},\qquad h=|\mathcal C|.
\]
Let \(J_q\) be a drop from a positive normalized head to less than \(1/q\) of its old value, including a drop to zero. If \(h\le(\min(r,s)-1)/2\), then
\[
\boxed{\displaystyle
\Pr(J_q\mid \text{old nonreader and shared-reader coordinates})
\le \frac{32}{q}S_{\mathcal A}S_{\mathcal B}.}
\]
The exclusive coordinates and \(n_q\) must remain unread. This applies to the full chronological panel or to a specified finite panel. [Single-digit phase-mass framework](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

Remove all readers to form a reference family \(\Omega\). Its digit fibres are uniform \(r\times s\) grids. The shift mod \(q\) is injective on each grid, by the two coprime primary order factors. A shared reader also has an injective shift on each grid and can delete at most one cell. LTE ensures that an exclusive reader is independent of the other digit throughout its full prime-power read.

For \(J_q\) to occur, one terminal residue must contain more than \(q/(q+1)\) of the actual old survivors. It contains at most \(1/(rs)\) of \(\Omega\), so the actual old family has mass at most \((1+1/q)/(rs)\) relative to \(\Omega\). The shared rows delete at most \(h/(rs)\). Thus one of the two exclusive groups must delete at least \(1/4\) of \(\Omega\). For \(\mathcal A\), this costs at most \(4S_{\mathcal A}\) by Markov.

Now fix that group's readings. Its surviving family still has the whole \(s\)-digit free on every orbit. A terminal residue holds at most \(1/s\) of this family, and the already fixed shared rows can delete at most \(h/s\). To reach \(J_q\), the \(\mathcal B\)-rows must therefore delete at least \(1-(h+1+1/q)/s\ge1/4\) of this family. Their targets are still independent Haar coordinates, so this costs at most \(4S_{\mathcal B}\) conditionally on the first group's readings. The opposite exposure order gives the same bound. Finally, at most one unread residue of \(n_q\bmod q\) can trigger the drop, giving the factor \(1/q\).

### A deterministic obstruction test

On each reference grid the two exclusive groups leave a Cartesian product with side lengths at least \((r-|\mathcal A|)_+\) and \((s-|\mathcal B|)_+\). Put
\[
N=(r-|\mathcal A|)_+(s-|\mathcal B|)_+-h.
\]
If \(N\ge2\), every reference grid has at least \(N\) old survivors, and a terminal read can reject at most one. On a positive old head the normalized terminal ratio is therefore at least \((1+1/q)(1-1/N)\). This test works at any terminal lifting depth, including a common Wieferich terminal satisfying the order conditions.

For actual base 3, take \(q=211\), \(r=3\), \(s=5\), and the old finite panel
\[
\mathcal A=\{7\},\qquad \mathcal B=\{11,71,131\},\qquad \mathcal C=\{31\}.
\]
Each separate digit count leaves only one guaranteed old choice. The grid count gives \(N=2\cdot2-1=3\), so the terminal read leaves at least two. The replay attains both counts. In the **full** panel before 211 the exclusive lists are longer, but 31 is still the sole shared reader, so the product estimate applies there too. The actual terminal 211 is ordinary and the replay checks the finite local support claim.

### Exact shared-reader countercontrol

At 31, the two digit lines through their common anchor have 3 and 5 distinct shifts. Their intersection contains exactly the anchor shift. Over Haar \(n_{31}\), the two line-failure events have probabilities \(3/32\) and \(5/32\), and their intersection has probability \(1/32\), exceeding \(15/32^2\). The replay counts the exact valuation-one versions mod \(31^2\), with sizes \(90,150,30\). This is why the shared reader is charged by its grid capacity and never multiplied as two independent observations.

```python
from math import isqrt, lcm, prod

q = 211
plan = [(7,2,0), (11,0,2), (71,0,3), (131,0,4), (31,0,0), (q,0,1)]
P = [p for p, _, _ in plan]
L = lcm(*(p*(p-1) for p in P))
cells = [(i,j) for i in range(3) for j in range(5)]

def shift(i,j,m):
    return (pow(3,2+i*(L//3)+j*(L//5),m)+5) % m

assert [len({shift(i,j,p) for i,j in cells}) for p in P] == [3,5,5,5,15,15]
res = [(4,3),(3,0)] + [(p*p,shift(i,j,p*p)+p) for p,i,j in plan]
M = prod(m for m,_ in res)
n = sum(a*(M//m)*pow(M//m,-1,m) for m,a in res) % M

def hit(t,i,j,p):
    x = (t-shift(i,j,p*p)) % (p*p)
    return x != 0 and x%p == 0

assert all((n-shift(i,j,p*p))%(p*p) for p in P for i,j in cells)
live = [ij for ij in cells if all(not hit(n,*ij,p) for p in P[:-1])]
assert live == [(0,1),(1,0),(1,1)]
assert [ij for ij in live if not hit(n,*ij,q)] == [(1,0),(1,1)]

A = {t for t in range(31**2) if any(hit(t,i,0,31) for i in range(3))}
B = {t for t in range(31**2) if any(hit(t,0,j,31) for j in range(5))}
assert (len(A),len(B),len(A&B)) == (90,150,30)

old = [p for p in range(7,q,4) if all(p%d for d in range(2,isqrt(p)+1))]
order = lambda p: next(k for k in range(1,p) if pow(3,k,p)==1)
assert order(q) == 210 and [p for p in old if order(p)%15==0] == [31]
```

The arithmetic replay passed. The product bound limits the probability of a drop including zero; the grid test deterministically excludes terminal zero when its separate count condition holds. Excluding every terminal zero, or proving a true two-square remainder from these finite local checks alone, remains open.

Independent BigInt replay recovered the CRT target, three old surviving cells, two final cells, and the exact shared-event counts 90,150,30 modulo 31 squared. The product estimate requires both source digits to remain free and the exclusive target coordinates to be unread.
