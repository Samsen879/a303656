# Exact two-coordinate blocks for coupled guard placement

**Yes. Two reciprocally read digits can be eliminated as one block.** On a real two-by-two block, the base-\(5\) exceptional row \(20771\) and the ordinary row \(311\) forbid exactly the same diagonal. Neither digit can be fixed first while guaranteeing that the other remains free. The direct union bound uses up all four cells, but exact elimination leaves both off-diagonal cells and preserves the ordinary lift at \(31\).

### Exact block test

Let the two moving digits be \(x=d_r\) and \(y=d_s\), with allowed sets \(D_r,D_s\). Freeze the other \(d\)-digits read by each guard. If the retained free \(c\)-digits make \(3^c\bmod p\) range over \(A_pH_{u_p}\), the forbidden cells for guard \(p\) are exactly those satisfying
\[
(N-5^{d(x,y)})^{u_p}=A_p^{u_p}\pmod p.
\]

Pack the two digits into a common CRT label. For a row that reads a joint order component of size \(k_p\), the full block of \(5\)-powers is a coset \(B_pH_{k_p}\). Its bad values are the roots of
\[
\gcd\!\left(Z^{k_p}-B_p^{k_p},\ (N-Z)^{u_p}-A_p^{u_p}\right)
\quad\text{over }\mathbb F_p.
\]
Decode each row’s roots back to the common digit labels and restrict to \(D_r\times D_s\). The block passes exactly when the union of the resulting forbidden cells leaves a cell. In graph terms, the forbidden bipartite graph must be missing an edge. This permits contracting a reciprocal dependency into one block, then processing that block in the order of the remaining dependencies. [Relocation baseline](https://github.com/Samsen879/a303656/blob/7bc8e91bc95018ccc6f3546193c9f5e1303d7ff5/analysis/ajt5_overnight_2026_11_26/ALTERNATE_PRIMARY_GUARD_RELOCATION.md)

For a row that reads both digits injectively, the direct degree bound is \(|F_p|\le u_p\). Even the sharper direct union bound using *exact* row counts can fail to certify a viable block when rows forbid the same cells. The gcds are taken separately in their own prime fields; the union is taken after decoding the digit labels.

### Same-target real control

Take
\[
N=10+442545519052721660967469^2+103809791795892016724352^2.
\]
The actual orders of both bases are \(5\cdot31\cdot67\) at \(20771\) and \(5\cdot31\) at \(311\). Keep \(c\equiv0\bmod22110,\ d\equiv5\bmod10854\). These prelocks retain \(d\bmod67\), the low-prime conditions, and the order cofactors for both guards. They leave both \(d_{31},d_5\) available and leave \(c_{31}\) free. The \(c\)-orbit at each guard is the order-\(31\) subgroup.

On the deliberately restricted box \(D_{31}=\{10,30\},\ D_5=\{2,1\}\), the exact modular tests are:

| Guard | \((10,2)\) | \((10,1)\) | \((30,2)\) | \((30,1)\) |
|---|---:|---:|---:|---:|
| \(20771\) | 1 | 73 | 17216 | 1 |
| \(311\) | 1 | 305 | 305 | 1 |

Each entry is \((N-5^d)^{31}\bmod p\); **1 means forbidden**. Both rows genuinely depend on both digits on this box. Every first-digit choice has a bad extension, so neither uniform sequential order certifies it. The exact union has two cells, while the direct sum is \(2+2=4\). On the full 155-cell block, the gcd degrees are \(2\) and \(16\), so the direct union bound already suffices there.

The row types are distinct:
\[
N-1-5^{72}\equiv20771\pmod{20771^2},\qquad
5^{10385}\equiv1\pmod{20771^2}.
\]
This is a genuine base-\(5\) hard row at the indicated fixed \(c=0\) phase. At \(311\), \(N-1-5^{61}\equiv311\bmod311^2\), but \(5^{155}\not\equiv1\bmod311^2\). It is an ordinary unit guard in this control and could be handled differently if that protection requirement were relaxed.

Choose the surviving cell \((10,1)\). The local phase
\[
(c,d)=(18682950,\ 50568791)
\]
uses the free \(c_{31}\) coordinate to change the residue at \(31\) from valuation \(1\) to valuation \(2\), while both guards remain units. The large phase is a local witness. The displayed square coordinates give the actual short representation with \(c=2,d=0\).

```python
from math import isqrt
N = 10 + 442545519052721660967469**2 + 103809791795892016724352**2
M=10854
def d_for(i,j):
    k=int(i-5)*pow(M,-1,31)%31
    z=5+M*k
    return z+M*31*((j-z)*pow(M*31,-1,5)%5)
for p,o,e,exc,expected in ((20771,10385,72,True,2),(311,155,61,False,16)):
    assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
    for b in (3,5):
        assert pow(b,o,p)==1
        assert all(pow(b,o//l,p)!=1 for l in (5,31,67) if o%l==0)
    assert pow(5,o,p*p)==1 if exc else pow(5,o,p*p)!=1
    assert (N-1-pow(5,e,p*p))%(p*p)==p
    assert sum(pow((N-pow(5,d_for(i,j),p))%p,31,p)==1
               for i in range(31) for j in range(5))==expected
    row=[pow((N-pow(5,d_for(i,j),p))%p,31,p) for i,j in ((10,2),(10,1),(30,2),(30,1))]
    assert row==([1,73,17216,1] if exc else [1,305,305,1])
c,d = 18682950, 50568791
assert (c%22110,d%M,d%31,d%5)==(0,5,10,1)
assert (N-1-pow(5,d,31**2))%31**2==9*31
for m,z in ((4,1),(27,18),(11,6),(31**3,961),(67,59),(311,11),(20771,1359)):
    assert (N-pow(3,c,m)-pow(5,d,m))%m==z
print("OK")
```

The example obstructs universal sequential allocation on the restricted box. Sequential search with backtracking still finds an off-diagonal cell, and the full box does not need the sharper block test.
