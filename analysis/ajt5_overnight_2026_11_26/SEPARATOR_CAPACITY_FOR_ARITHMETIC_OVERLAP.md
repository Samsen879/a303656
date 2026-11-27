# Separator capacity certifies overlap of arithmetic deletion fibres

**A separator-capacity test certifies unavoidable overlap without comparing the maximizing tuples.** On the actual \(3,5\) rank-two panel, three separator states give a capacity of \(5\), while the two maximum deletions have total size \(6\). A second actual target shows why the separator must separate the reads. Conditioning on one digit gives a strict capacity inequality there, yet the two maximizing deletions are disjoint.

### The separator test

Let \(\Omega\) be the open-forest survivor set and let \(E,F\) be two deletion fibres, each specified by a tuple on its closing edge. Choose a set \(S\) of forest vertices such that **every component of the forest after removing \(S\) contains read vertices of at most one of the two fibres**. The fibres may both read vertices in \(S\).

For a separator assignment \(s\), let \(C_E(s)\) and \(C_F(s)\) bound the number of cells in that slice that any one tuple of the corresponding edge can delete. Suppose the fibres under consideration have sizes at least \(u_E,u_F\). Then
\[
\boxed{\quad
\lambda u_E+\mu u_F>
\sum_s\max\{\lambda C_E(s),\,\mu C_F(s)\},
\qquad \lambda,\mu>0
\quad}
\]
forces \(E\cap F\ne\varnothing\).

Given \(s\), the open survivor set is a product over the remaining components. If both fibres meet the slice, their restrictions apply to disjoint components and can be combined. Thus disjoint fibres can contribute on at most one side of each slice, giving the right-hand side as an upper bound and proving the test.

The capacities can be computed from **one-vertex marginals**. In each component, use its total count if a fibre reads nothing there. Otherwise use the largest count under a single pinned read vertex, taking the minimum of these bounds if the fibre reads several vertices there. Multiply the component bounds. For a fixed separator assignment, forest messages compute all these marginals without a table of joint endpoint tuples. To test only maximizing fibres, \(u_E,u_F\) can be lower bounds obtained from any exhibited tuples.

### Actual positive and negative controls

Write the binary labels at sources \(3,5,7,11\) as \((i,j,k,\ell)\), all on the \(3\)-axis, and fix \(d=2\). The open path \(j-k-i-\ell\) uses primes \(71,7,199\). The closing primes \(31,2003\) read \((i,j)\) and \((k,\ell)\), respectively. Each specified collision is imposed at **exact valuation one**.

At the positive target \(7279389990015072453608156343\), use \(S=\{i,k\}\). The components left over are the separate vertices \(j,\ell\).

| \((i,k)\) | Open cells | \(C_{31}\) | \(C_{2003}\) |
|---|---:|---:|---:|
| \((0,0)\) | 1 | 1 | 1 |
| \((1,0)\) | 2 | 2 | 1 |
| \((1,1)\) | 4 | 2 | 2 |

Since \(31\) fixes \(i\), its maximum loss is at most \(4\). Since \(2003\) fixes \(k\), its maximum loss is at most \(2\). Both bounds are attained. The test gives \(4+2>1+2+2\). If either deletion falls below its maximum, it already saves a cell. Thus **every closing-residue choice leaves at least two of the seven cells**. The terminal \(2311\) reads all four digits injectively modulo \(2311\), so every frozen terminal residue leaves at least one unit. The displayed target leaves exactly the cell \((1,1,1,1)\).

At the negative target \(9182222962623148199372481267\), the maximizing deletions both have size \(2\). Projecting onto \(j\) gives both capacity vectors \((1,2)\) and the apparent inequality \(2+2>3\). Yet the actual maximizing fibres \((i,j)=(0,1)\) and \((k,\ell)=(1,1)\) are disjoint. At \(j=1\), the first fibre uses \(i=0\), which forces \(k=0\), while the second uses \(k=1\). Removing \(j\) leaves that dependency intact. The two deletions leave one of five old cells, and the frozen terminal kills it at valuation one.

```python
from itertools import product
from math import isqrt, lcm, prod

q = 2311
P = (7,31,71,199,2003,q)
def prime(p):
    return p > 1 and all(p % d for d in range(2,isqrt(p)+1))
def order(p):
    assert prime(p) and p % 4 == 3
    return next(k for k in range(1,p) if pow(3,k,p) == 1)
def v(a,p):
    assert a
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k

assert list(map(order,P)) == [6,30,35,198,1001,2310]
m = {p:p*p for p in P} | {2:4,3:3,7:343}
L = lcm(*(a-a//p for p,a in m.items() if p != 3))
def step(p):
    a = p**v(L,p)
    return (L//a)*pow(L//a,-1,a)
U = tuple(map(step,(3,5,7,11)))
def c(x):
    return L+sum(a*b for a,b in zip(U,x))
def f(p,x):
    return 25+pow(3,c(x),m[p])
def crt(t,mod):
    M = prod(mod.values())
    return sum(t[p]*(M//a)*pow(M//a,-1,a) for p,a in mod.items()) % M

O = (0,0,0,0)
D = range(2)
G = list(product(D,repeat=4))
cases = [
    ((1,0,0,0),(0,1,0,0),(0,0,0,1),(0,0,1,0),O),
    ((0,1,0,0),O,(1,0,0,0),(0,0,1,1),(1,1,0,1)),
]
for ix, roots in enumerate(cases):
    t = {2:3,3:0,7:f(7,O)+49} | {
        p:f(p,x)+p for p,x in zip(P[1:],roots)}
    n = crt(t,m)
    def ok(p,x):
        return v((n-f(p,x)) % m[p],p) % 2 == 0
    assert all(ok(2,x) and ok(3,x) for x in G)
    old = {x for x in G if all(ok(p,x) for p in (7,71,199))}
    E = {x for x in old if not ok(31,x)}
    F = {x for x in old if not ok(2003,x)}
    end = {x for x in old-E-F if ok(q,x)}
    J = [sum(ok(71,(0,j,k,0)) for j in D) for k in D]
    H = [sum(ok(199,(i,0,0,l)) for l in D) for i in D]
    rows = [(i,k,J[k]*H[i],H[i],J[k]) for i,k in product(D,repeat=2)
            if ok(7,(i,0,k,0)) and J[k]*H[i]]
    if ix == 0:
        assert rows == [(0,0,1,1,1),(1,0,2,2,1),(1,1,4,2,2)]
        assert end == {(1,1,1,1)}
        x, = end
        p = 3319
        assert prime(p) and p % 4 == 3
        extra = {r:r for r in range(7,q,4) if prime(r) and r not in m}
        nn = crt(t | {r:25 for r in extra} |
                 {p:25+pow(3,c(x),p*p)+p}, m | extra | {p:p*p})
        assert len(extra) == 168 and nn % prod(m.values()) == n
        assert (nn-25-pow(3,c(x),p*p)) % (p*p) == p
    else:
        for axes in [(0,1),(2,3)]:
            assert [max(sum(x[1]==j and tuple(x[a] for a in axes)==b
                            for x in old) for b in product(D,repeat=2))
                    for j in D] == [1,2]
        assert {x[1] for x in E} & {x[1] for x in F} == {1}
    result = tuple(map(len,(old,E,F,E&F,end)))
    assert result == [(7,4,2,1,1),(5,2,2,0,0)][ix]
    print(n,result)
```

**Panel scope.** The positive control can include every inert prime through \(2311\) at one CRT target. The 168 added primes take \(n\equiv25\bmod p\), so their valuations are zero throughout the chart. At that same enlarged target, \(3319\) can have exact valuation one at the sole survivor. A sufficiently large positive lift modulo the enlarged CRT modulus makes every displayed offset active and preserves all these tests. Thus even the full prime prefix through \(2311\) can leave a survivor that fails the two-square test. This establishes failure on the displayed chart, with other exponent phases still available.

The actual terminal \(2311\) is ordinary. The unit-count argument also applies to a hypothetical common-Wieferich terminal satisfying the same injective-read condition, since it needs no primary release. It gives no obstruction or density conclusion over all exponent phases. [Finite-obstruction framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Independent BigInt verified positive and negative cell enumerations, the exact full-prefix CRT extension with all 168 additional unit reads, and the same enlarged target’s later valuation-one failure at 3319. Capacity only proves overlap when the selected separator really separates the two read sets.
