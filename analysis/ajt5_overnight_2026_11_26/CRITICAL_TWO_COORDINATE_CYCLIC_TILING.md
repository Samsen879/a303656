# Critical two-coordinate cyclic tilings and first-digit survival

**A two-coordinate cycle has an exact blocking criterion at the critical row count.** For a full \(\ell\times\ell\) chart with both step orders equal to \(\ell\), exactly \(\ell\) rows can block the chart only by tiling it with parallel zero-collision lines. On free first primary digits those lines share a point, so the tiling is impossible. On anchored second digits it can occur. The actual primes \(19,883,1747\) give such a tiling even though the two assigned loads are \(2/3\) and \(1/3\).

### Joint survival on a prime-order square

Freeze all other reads. At each row prime \(p\), write the collision equation as
\[
a_pu_p^x+b_pv_p^y=N_p\pmod p,
\qquad (x,y)\in\mathbb F_\ell^2,
\]
where \(\ell\) is an odd prime, \(u_p,v_p\) both have exact order \(\ell\), \(a_p,b_p\ne0\), and \(N_p=n\bmod p\). Each row’s collision set is a partial matching, since either coordinate determines at most one value of the other. One can compute it by tabulating the \(y\)-powers and looking up \(N_p-a_pu_p^x\) for each \(x\). Exact parity is tested only on the returned pairs, and taking their union gives the exact survivor count.

If \(N_p\ne0\), the matching has fewer than \(\ell\) edges. Otherwise the two cosets \(a_pH\) and \(N_p-b_pH\), with \(|H|=\ell\), would coincide. Their sums are \(0\) and \(\ell N_p\). If \(N_p=0\), a nonempty collision set is a full affine line
\[
x=\alpha_p y+\beta_p
\]
obtained by taking discrete logs in \(H\).

Consequently, **with exactly \(\ell\) rows, full odd-valuation blocking occurs if and only if all rows give zero-collision lines with the same slope and distinct intercepts, and each collision has odd valuation**. Counting forces every row to have \(\ell\) collisions and the lines to be disjoint. The stated parallel lines tile the square.

For free first \(\ell\)-primary digits, when both orders have \(\ell\)-part exactly \(\ell\), every nonempty zero line contains the common phase \(c\equiv d\equiv0\bmod\ell\). Indeed, existence of a zero collision equates the prime-to-\(\ell\) components of \(3^c\) and \(-5^d\). At that common phase both \(\ell\)-components are trivial. Thus at most \(\ell\) such rows always leave a unit cell.

There is a further margin for \(\ell\ge5\). A nonzero row has at most \(\ell-2\) collisions. If the two cosets above differed by just one point each, say \(s\) and \(t\), their first three power sums would give
\[
t-s=\ell N_p,\qquad t+s=N_p,\qquad t^2+ts+s^2=N_p^2.
\]
These imply \(\ell^2=1\bmod p\), impossible since \(p\ge2\ell+1\). On first digits, \(z\) distinct zero lines cover \(1+z(\ell-1)\) cells and \(z\le\ell-1\). With at most \(\ell+1\) rows, charging each remaining row \(\ell-2\) leaves **at least two unit cells**. This bound assumes the full digit square is available.

### Actual \(3,5\) cyclic countercontrol

At \(p=19,883,1747\), the order-nine projections of base \(5\) are respectively the \(4\)th, \(1\)st, and \(7\)th powers of the order-nine projections of base \(3\). Put
\[
E=47530,\quad C=30555,\quad
c=C+E(a+3x),\quad d=E(a+3y),
\qquad x,y\in\{0,1,2\}.
\]
At the single CRT target \(n=4476061166823081\), anchor \(a=1\) gives the three lines \(x-y=1,0,2\bmod3\), each with exact valuation one throughout. Assigning two rows to \(x\) and one to \(y\) gives loads \(2/3,1/3\), yet all nine cells fail. At the **same target**, anchor \(a=0\) makes all three lines coincide and leaves six cells. The \(2,3\) tests pass throughout both charts.

```python
from itertools import product
from math import isqrt

P = (19, 883, 1747)
E, C, n = 47530, 30555, 4476061166823081
G = set(product(range(3), repeat=2))

def order(g, p):
    return next(j for j in range(1, p) if pow(g, j, p) == 1)

assert all(p % 4 == 3 and all(p % k for k in range(2, isqrt(p)+1))
           for p in P)
assert tuple(n % (p*p) for p in P) == (19, 0, 0)
for a in (0, 1):
    bad = set()
    for p, k in zip(P, (4, 1, 7)):
        assert pow(3, C, p) == p-1
        assert order(pow(3,E,p),p) == order(pow(5,E,p),p) == 9
        assert pow(5,E,p) == pow(3,k*E,p)
        hits = set()
        for x,y in G:
            c,d = C+E*(a+3*x), E*(a+3*y)
            def rem(m):
                return (n-pow(3,c,m)-pow(5,d,m)) % m
            assert rem(4) == 1 and rem(3) != 0
            if rem(p) == 0:
                assert rem(p*p) != 0
                hits.add((x,y))
        assert hits == {(x,y) for x,y in G if (x-y-a*((k-1)//3))%3 == 0}
        bad |= hits
    assert len(G-bad) == (6 if a==0 else 0)
```

This joint test can replace the acyclic rule for a two-coordinate component once its other reads are fixed. The countercontrol concerns a frozen chart, and all three primes in it are ordinary. A sufficiently large lift of the target preserving its CRT residues makes the displayed exponents active. The test gives neither a height bound at a prescribed target nor a two-square certificate. Any cofinal-prefix application still requires a verified protected closure and a survival argument for every remaining component. [Finite-obstruction framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Independent BigInt replay checked all projected orders, exact valuation-one incidences and both complete charts. The critical tiling refers to the full prime-order square with other coordinates frozen; it is not a global obstruction or an example of a common-Wieferich prime.
