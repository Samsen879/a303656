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

## Refinement: three independently excluded classes on the (5,5) shared grid

## When an order class can be excluded

Fix a prime \(p>5\), write \(h_q=\operatorname{ord}_p(q)\), and fix exponent classes modulo \(s_q\mid h_q\), for \(q=3,5\). The two powers range over multiplicative cosets with indices
\[
I=s_3\frac{p-1}{h_3},\qquad J=s_5\frac{p-1}{h_5}.
\]
Let \(K=IJ\). For a nonzero target residue \(t\bmod p\), let \(N_t\) count pairs of coset values summing to \(t\).

Writing \(g=\gcd(I,J)\), the character expansion gives
\[
KN_t\ge p-2-E-(K-1-E)\sqrt p,\qquad E=I+J+g-3.
\]
The trivial character pair contributes \(p-2\). There are \(E\) other pairs with one trivial character or with nontrivial inverse characters, each contributing a term of magnitude 1. The remaining pairs have Jacobi sums of magnitude \(\sqrt p\). [Jacobi-sum identities](https://doi.org/10.3934/math.2020192)

Consequently, a missing nonzero residue requires
\[
K\ge 1+\frac{p-2}{\sqrt p}+E\left(1-\frac1{\sqrt p}\right).
\]
In particular, \(K>\sqrt p\). Using \(E\ge2\sqrt K-2\) sharpens the product-only test to
\[
K>\sqrt p+2p^{1/4}-1-2p^{-1/4}.
\]
Thus a growth scheme with bounded base-index product and \(s_3s_5=o(\sqrt p)\) cannot use arbitrarily large primes to exclude classes at nonzero targets. For exact valuation-one hits, this conclusion applies when at least one base supplies a private \(p\)-lifting digit.

The threshold is necessary for an exclusion. Above it, the character bound alone certifies no missing residue. A separate sufficient test is \(K>p-1\), since then there are fewer than \(p-1\) pairs of coset values. If at least one coset has more than one element, some nonzero sum also occurs. Neither test yields independent exclusions across several rows. Those require the joint checks below.

## Three independently excluded classes

Use the least CRT target
\[
n=31\,071\,269\,389\,206,\qquad
n\equiv(2,2,3,1)\pmod{(11^2,71^2,131^2,151^2)}.
\]

| \(p\) | Orders of \(3,5\) modulo \(p\) | Orders modulo \(p^2\) | \(K\) | Effect on the classes left by 11 |
|---:|---:|---:|---:|---|
| 11 | \(5,5\) | \(5,55\) | 100 | Leaves \((0,0),(2,3),(4,4)\) |
| 71 | \(35,5\) | \(2485,355\) | 700 | Excludes only \((2,3)\) |
| 131 | \(65,65\) | \(8515,8515\) | 100 | Excludes only \((0,0)\) |
| 151 | \(50,75\) | \(7550,11325\) | 150 | Excludes only \((4,4)\) |

Every pairwise gcd of prime-square orders is 5 in each coordinate. Every row has a base whose order gains a factor \(p\) modulo \(p^2\). Hence a local match modulo \(p\) can be turned into valuation exactly 1, if needed, by adding one prime-level order to that base’s exponent. This preserves the class modulo 5, and generalized CRT joins the chosen local exponents.

The table therefore certifies that no exponent pair hits all four primes. Each deletion has an unrestricted actual exponent pair giving exact valuation-one hits at the other three primes:

| Deleted prime | \((c,d)\) |
|---:|---:|
| 11 | \((905698020,1322839342)\) |
| 71 | \((10992882,211018778)\) |
| 131 | \((2370725,1381660)\) |
| 151 | \((638654,6130854)\) |

As a control, changing only the residue modulo \(151^2\) from 1 to 2 gives target \(216\,849\,182\,105\,514\). All four hits hold at \((4689644794,1662034389)\).

This proves three independently excludable classes on a larger actual shared grid. It does not establish an unbounded family. The exponents in this experiment are unrestricted. The CRT blocking construction below \(X\) instead attaches an odd-valuation witness to each low shift, which is an avoidance problem inside a height window.

## Inline replay

The standard-library replay checks the exact orders, all three exclusions, the four deletion witnesses, and the control.

```python
from math import gcd, prod

P = (11, 71, 131, 151)
T = (2, 2, 3, 1)

def cycle(q, m):
    a = [1]
    while a[-1]*q % m != 1:
        a.append(a[-1]*q % m)
    return a

def crt(residues):
    M = prod(p*p for p in P)
    return sum(r*(M//(p*p))*pow(M//(p*p), -1, p*p)
               for r, p in zip(residues, P)) % M

h = {p: tuple(len(cycle(q, p)) for q in (3, 5)) for p in P}
L = {p: tuple(len(cycle(q, p*p)) for q in (3, 5)) for p in P}
assert list(h.values()) == [(5,5),(35,5),(65,65),(50,75)]
assert list(L.values()) == [(5,55),(2485,355),(8515,8515),(7550,11325)]
assert all(gcd(L[p][j], L[r][j]) == 5
           for p in P for r in P if p != r for j in (0, 1))
assert all(any(L[p][j] == p*h[p][j] for j in (0, 1)) for p in P)

def row(p, t):
    a, b = (cycle(q, p) for q in (3, 5))
    return {(c % 5, d % 5) for c, x in enumerate(a)
            for d, y in enumerate(b) if (x+y-t) % p == 0}

R = [row(p, t) for p, t in zip(P, T)]
C = R[0]
assert C == {(0,0),(2,3),(4,4)}
assert [C-S for S in R[1:]] == [{(2,3)},{(0,0)},{(4,4)}]
assert (0,2) in set.intersection(*R[1:])
assert not set.intersection(*R)

def hit(n, p, c, d):
    r = (n-pow(3,c,p*p)-pow(5,d,p*p)) % (p*p)
    return r != 0 and r % p == 0

n = crt(T)
assert n == 31071269389206
W = [(905698020,1322839342),(10992882,211018778),
     (2370725,1381660),(638654,6130854)]
for deleted, w in zip(P, W):
    assert {p for p in P if hit(n,p,*w)} == set(P)-{deleted}

n = crt((2,2,3,2))
assert n == 216849182105514
assert all(hit(n,p,4689644794,1662034389) for p in P)
```