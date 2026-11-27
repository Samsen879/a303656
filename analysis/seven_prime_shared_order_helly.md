# Exact shared-order Helly bound and a deletion-minimal seven-prime panel

This is a finite obstruction result for simultaneous exact valuation-one hits at unrestricted exponent pairs. It does not obstruct all ordinary two-square representations, and it is separate from CRT panels blocking shifts inside a prescribed height window.

## A shared-order bound for unrestricted simultaneous hits

Let \(P\) be a finite panel of primes \(p>5\), \(p\equiv3\bmod4\). A hit means \(v_p(n-3^c-5^d)=1\), with no height restriction. Put \(L_{p,q}=\operatorname{ord}_{p^2}(q)\) for \(q=3,5\).

Start \(E\) with every prime \(p\) for which \(p\nmid n\). Repeatedly add any \(p\in P\) with \(v_p(n)=1\) that divides an order \(L_{r,q}\) for some \(r\in E\). Define
\[
D_q=\gcd\!\left(\operatorname{lcm}_{r\in E}L_{r,q},
                 \operatorname{lcm}_{p\notin E}L_{p,q}\right).
\]
Let \(m\) count the distinct jointly feasible pairs \((c\bmod D_3,d\bmod D_5)\) for the hits in \(E\). In particular, \(m\le D_3D_5\).

**Bound.** If the full panel is inconsistent, there is an inconsistent subpanel of size at most \(|E|+3m\). If \(m=0\), \(E\) itself is inconsistent.

To prove it, fix one of the \(m\) residue pairs. For \(p\notin E\), take discrete logs \(A_p=\log 3\), \(B_p=\log 5\) to a primitive root modulo \(p^2\). The prime-level condition is
\[
A_pc-B_pd\equiv(p-1)/2\pmod{p-1}.
\]
Together with the fixed residue pair, this is an affine linear system on each primary component of the exponent periods. For \(p^2\mid n\), the additional hit condition is \(A_pc-B_pd\ne0\bmod p\), confined to the \(p\)-primary component. For \(v_p(n)=1\), the closure defining \(E\) guarantees that the fixed residue pair imposes no condition on the \(p\)-primary component. That component can be set to zero. Its odd-primary equations are homogeneous, and setting it to zero makes \(3^c+5^d\equiv0\pmod{p^2}\), giving the hit.

An inconsistent affine system over a common prime-power modulus is witnessed by at most three augmented rows, because the row module has a generating subset of at most three original rows. If the equations are consistent but force a forbidden zero, translate by one solution. The resulting homogeneous row module has a generating subset of at most two original rows, so two equations and the inequality suffice. The generator claims follow by projecting a submodule of \((\mathbb Z/\ell^a)^d\) onto one coordinate and inducting on \(d\), then selecting generators from the original rows modulo \(\ell\) times the module and lifting. Thus each fixed residue pair can be ruled out by at most three primes outside \(E\). Taking their union with \(E\) proves the bound.

Here are two realized obstructions. In each row, the listed residues are taken modulo the corresponding **prime squares** and joined by CRT. Each proper subpanel admits exact simultaneous hits. The control changes only the final residue and admits all hits.

| Panel | Inconsistent residues | Control change |
|---|---|---|
| \(7,19,163,199\) | \(0,0,161,0\) | \(0\to1\) at 199 |
| \(7,79,139,151,163,191,199\) | \(0,77,138,146,127,162,188\) | \(188\to2\) at 199 |

The first example shows that **one** nonzero target residue modulo its prime suffices to exceed the three-prime bound from the all-divisible stratum. The second gives a lower bound of seven for any uniform Helly bound. The shared-order bound is panel-dependent. I did not establish a uniform constant or an unbounded family of unrestricted hit obstructions. The height construction proves unbounded deletion minimality for **blocking** shifts inside a height window. The public index’s N-009 concerns restricted active-shift families. [Public theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Independent replay

The script checks cycles, private lifting digits, exact shared-grid intersections, every one-prime deletion, and the success of the indicated control with one changed residue. The control exponents are unrestricted, with no ordinary-height assertion.

~~~python
from itertools import product
from math import gcd, isqrt, lcm, prod

def crt(values, moduli):
    M = prod(moduli)
    return sum(x*(M//m)*pow(M//m, -1, m)
               for x, m in zip(values, moduli)) % M

def hit(n, s, p):
    return (n-s) % (p*p) in range(p, p*p, p)

def cycle(q, p):
    values = [1]
    while values[-1]*q % p != 1:
        values.append(values[-1]*q % p)
    return values

def verify(P, residues, control, witness):
    n = crt(residues, [p*p for p in P])
    A = {p: [cycle(q, p) for q in (3, 5)] for p in P}
    h = {p: tuple(map(len, A[p])) for p in P}
    assert all(h[r][j] % p for p in P for r in P if p != r
               for j in (0, 1))
    assert all(any(pow(q, h[p][j], p*p) != 1
                   for j, q in enumerate((3, 5))) for p in P)
    S = {p: tuple(gcd(h[p][j], lcm(*(h[r][j] for r in P if r != p)))
                  for j in (0, 1)) for p in P}
    grid = list(product(*(range(lcm(*(S[p][j] for p in P)))
                          for j in (0, 1))))
    rows = {}
    for p in P:
        u, v = S[p]
        local = {(c % u, d % v) for c, x in enumerate(A[p][0])
                 for d, y in enumerate(A[p][1]) if (n-x-y) % p == 0}
        rows[p] = {(c, d) for c, d in grid if (c % u, d % v) in local}
    assert not set.intersection(*rows.values())
    assert all(set.intersection(*(rows[p] for p in P if p != r)) for r in P)

    n = crt((*residues[:-1], control), [p*p for p in P])
    c, d = witness
    assert all(hit(n, pow(3, c, p*p) + pow(5, d, p*p), p) for p in P)

verify((7, 19, 163, 199), (0, 0, 161, 0), 1, (4041147939, 340531800))
verify((7, 79, 139, 151, 163, 191, 199), (0, 77, 138, 146, 127, 162, 188),
       2, (8056974975698731970456, 6037121740808871512479))

~~~
