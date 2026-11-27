# All 361 internal lift pins at the actual center 19

Yes. At center **19**, the exact native guards **191 and 2851** can pin every point of \(\mathbb F_{19}^2\). Their full prime-square orders share exactly the modulus 19 in each coordinate. For each of the 361 digit pairs there is a choice of unit targets for which both guards are essential to the pin. There is also a choice for every pair that admits an exact center hit at the fixed center residue \(19\bmod361\). For **342** pairs, one choice does both.

The full grid uses several unit-target orbits. I proved a private-order barrier for obtaining the grid from just **one multiplicative translation orbit per guard**. I did not establish such pinning at unboundedly many centers.

## Barrier for two fixed translation orbits

Let \(A,B\subseteq\mathbb F_p^2\) be the two seed masks, and suppose the target translations move them along independent directions \(u,v\). If every \(A+iu\) and \(B+jv\) meet in exactly one point, then the differences \(A-B\) cover \(\mathbb F_p^2\) exactly once. In the nonredundant case \(|A|=|B|=p\).

Moreover, at least one seed must be an affine line. For each nonzero linear functional, summing a primitive \(p\)-th root of unity over the unique difference representations gives a product of two sums equal to zero. A sum of \(p\) such roots vanishes only when every residue occurs once. Thus at least one mask omits the direction given by the kernel of the functional. The masks have disjoint sets of determined directions. Two nonlinear \(p\)-point sets cannot do this, since each determines at least \((p+3)/2\) directions by the Rédei–Megyesi theorem. [Somlai, *A new proof of Rédei’s theorem on the number of directions*](https://arxiv.org/html/2212.12823v1)

Now consider a native guard with actual orders \(h_3=pr_3,\ h_5=pr_5\), each divisible by \(p\) exactly once, and a unit target \(t\bmod q\). If its mask contains a full affine line, then for any integers \(0\le a,b<p\) with \((a+1)(b+1)>p\),
\[
p\ \le\ a r_3+b r_5.
\]
Indeed, normalize the two digit coordinates using the order-\(p\) characters \(x\mapsto x^{r_3}\) and \(y\mapsto y^{r_5}\). Pigeonholing coefficient pairs in the box \([0,a]\times[0,b]\) gives a nonzero normal to the line with coefficients \(A,B\) satisfying \(|A|\le a,\ |B|\le b\). All pairs of power values on the line then satisfy \(x^{Ar_3}(t-x)^{Br_5}=\text{constant}\). Clearing denominators gives a nonzero polynomial of degree at most \(a r_3+b r_5\). It is nonzero because \(0\) and \(t\) are distinct and at least one exponent is nonzero. The \(p\) digit cells require \(p\) distinct solutions.

Thus two guards are too small for this fixed-orbit construction if each admits a box with \(a r_3+b r_5<p\). For example, it is impossible if both have \(\lfloor\sqrt p\rfloor(r_3+r_5)<p\). This bound allows varying the actual order ratios and leaves the multiple-orbit construction open.

## Native two-dimensional family

| Row | Orders of \(3,5\bmod q\) | Orders modulo \(q^2\) |
|---:|---:|---:|
| 19 | \(18,9\) | \(342,171\) |
| 191 | \(95,19\) | \(18145,3629\) |
| 2851 | \(38,95\) | \(108338,270845\) |

The guard lift factors 191 and 2851 are private. A prime-level match can therefore be made an exact hit without changing the shared digit pair. In the replay, the unit residues select the masks, then the prime-square target lifts are chosen explicitly from a witness. The center uses its full prime-square orders.

The largest unit mask has only 14 cells at 191 and 5 at 2851. Neither guard has a \(19\)-cell seed. Nevertheless, varying the unit targets makes all 361 singleton intersections possible, with both individual masks larger than the singleton.

For a fixed deletion control, use
\[
n=69\,445\,834\,912\,649,\qquad
n\equiv(19,26352,5542236)\pmod{(19^2,191^2,2851^2)}.
\]
The two guards pin \((c,d)\equiv(0,0)\pmod{19}\), and \((171,513)\) hits all three rows. At the **same** target, removing guard 191 admits \((3,66)\), and removing guard 2851 admits \((47,86)\). Both alternatives hit the center and change the pinned pair.

This certifies a two-dimensional family at one center, with a separate actual target for each selected pin. It gives neither an unbounded family of centers nor a growing minimal inconsistent star.

## Inline exact replay

The standard-library replay independently verifies the three counts in the opening paragraph, constructs actual targets and exact witnesses for all 361 center-usable pins, and checks both deletions at the fixed control.

```python
from math import gcd, isqrt

p, q, r = 19, 191, 2851
P = (p, q, r)

def cycle(base, m):
    a = [1]
    while a[-1]*base % m != 1:
        a.append(a[-1]*base % m)
    return a

assert all(all(m % d for d in range(2, isqrt(m)+1)) for m in P)
A = {m: tuple(cycle(b,m) for b in (3,5)) for m in P}
h = {m: tuple(map(len,A[m])) for m in P}
L = {
    m: tuple(k*(m if pow(b,k,m*m) != 1 else 1)
             for b,k in zip((3,5),h[m]))
    for m in P
}
assert list(h.values()) == [(18,9),(95,19),(38,95)]
assert list(L.values()) == [(342,171),(18145,3629),(108338,270845)]
assert tuple(gcd(x,y) for x,y in zip(L[q],L[r])) == (p,p)
for u in (q,r):
    assert all(k % u for m in P if m != u for k in L[m])
    assert any(x != y for x,y in zip(h[u],L[u]))

def rows(m):
    masks, odd, witness = [0]*m, [0]*m, {}
    X,Y = A[m]
    for c,x in enumerate(X):
        for d,y in enumerate(Y):
            t = (x+y) % m
            bit = 1 << (c % p*p + d % p)
            masks[t] |= bit
            witness[t,bit,False] = (c,d)
            if c % 2:
                odd[t] |= bit
                witness[t,bit,True] = (c,d)
    return masks, odd, witness

a,_,Wq = rows(q)
b,bodd,Wr = rows(r)
assert max(x.bit_count() for x in a[1:]) == 14
assert max(x.bit_count() for x in b[1:]) == 5

both, usable, usable_both = {}, {}, {}
for t,x in enumerate(a[1:],1):
    for u,y in enumerate(b[1:],1):
        bit = x & y
        if not bit or bit & (bit-1):
            continue
        if x != bit and y != bit:
            both[bit] = (t,u)
        if bodd[u] & bit:
            usable[bit] = (t,u)
            if x != bit and y != bit:
                usable_both[bit] = (t,u)
assert [len(s) for s in (both,usable,usable_both)] == [361,361,342]

def crt(eqs):
    x,M = 0,1
    for y,m in eqs:
        g = gcd(M,m)
        assert (y-x) % g == 0
        z = m//g
        x += M*((y-x)//g*pow(M//g,-1,z) % z)
        M *= z
    return x % M

def shift(m,c,d):
    return (pow(3,c,m*m)+pow(5,d,m*m)) % (m*m)

def hit(n,m,c,d):
    z = (n-shift(m,c,d)) % (m*m)
    return z != 0 and z % m == 0

def join_at_center(bit,t,u):
    X,Y = Wq[t,bit,False], Wr[u,bit,True]
    for d0,y in enumerate(A[p][1]):
        c0 = A[p][0].index(-y % p)
        w = tuple(crt(((X[i],h[q][i]),(Y[i],h[r][i]),(z,h[p][i])))
                  for i,z in enumerate((c0,d0)))
        if hit(p,p,*w):
            return w
    raise AssertionError("no exact center hit")

for bit,(t,u) in usable.items():
    t,u = usable_both.get(bit,(t,u))
    w = join_at_center(bit,t,u)
    assert 1 << (w[0] % p*p + w[1] % p) == bit
    T = (p,(shift(q,*w)+q) % (q*q),(shift(r,*w)+r) % (r*r))
    assert (T[1] % q,T[2] % r) == (t,u)
    n = crt(zip(T,(m*m for m in P)))
    assert all(hit(n,m,*w) for m in P)

T = (19,26352,5542236)
n = crt(zip(T,(m*m for m in P)))
assert n == 69445834912649
assert (T[1] % q,T[2] % r) == (185,2743)
assert a[185] & b[2743] == 1 and a[185] != 1 and b[2743] != 1
assert all(hit(n,m,171,513) for m in P)
for removed,w in [(q,(3,66)),(r,(47,86))]:
    assert (w[0] % p,w[1] % p) != (0,0)
    assert {m for m in P if hit(n,m,*w)} == set(P)-{removed}
```
## A center-31 control for hidden CRT constraints

An exact first-moment test certifies full two-dimensional pin coverage while allowing multiple target orbits. It also detects what can go wrong when a center shares extra CRT digits with a guard. In a new native panel at center **31**, the guards alone can pin all \(31^2=961\) digit pairs. Requiring an exact center hit leaves **930** usable pairs with unit guard targets. The missing 31 pairs form the line \(c\equiv3d\pmod{31}\).

I also obtained a cyclotomic sufficient condition for full coverage and a bounded-private-order barrier to using its numerical prime-size cutoff. The results do not establish coverage at unboundedly many native centers.

## An exact test across target orbits

Fix the desired digit pair \(\alpha\). For guard \(i\), let \(T_i(\alpha)\) be the unit targets admitting a chosen local witness for \(\alpha\). This set can be filtered to enforce additional CRT compatibility. For a rival pair \(\beta\ne\alpha\), let \(U_i(\beta)\) contain **all** unit targets admitting \(\beta\), without that filter. Define
\[
E_\alpha=
\sum_{\beta\ne\alpha}
\frac{|T_1(\alpha)\cap U_1(\beta)|}{|T_1(\alpha)|}
\frac{|T_2(\alpha)\cap U_2(\beta)|}{|T_2(\alpha)|}.
\]
If both target sets are nonempty and \(E_\alpha<1\), some target pair pins \(\alpha\). This is the expected number of surviving rivals when independently drawing targets from the two **actual** finite sets. A nonnegative integer with mean below one is zero for some draw. One can retain target multiplicities when grouping the calculation by multiplicative orbits.

This differs from the random-mask estimate \((m_1-1)(m_2-1)/(p^2-1)\) for independent uniform masks of sizes \(m_1,m_2\) containing \(\alpha\). Native masks can have systematic collisions, and that estimate gives no certificate for them.

The test certifies uniqueness on the queried digit grid. Exact realizability also requires compatible witnesses on **every** shared CRT digit. For independent guards whose full order gcds are confined to the queried grid, CRT supplies the joint witness. With other overlaps, the filtered target sets must enforce a common assignment there, or the witnesses must be joined explicitly. Private prime-square lifts are a separate check.

## Cyclotomic sufficient condition and its limit

Suppose both guard orders are divisible by the center prime \(p\) exactly once. In each guard, choose both power values in the common subgroup of order \(p\). Every digit pair has unique representatives there, and their sum is nonzero for odd \(p\).

Over \(\mathbb C\), a nonzero sum of two unit-circle points determines their unordered pair. Thus, if reduction at the guard prime introduces no new collisions for these targets, the digit mask consists of the desired pair and possibly its swapped pair. In exponent coordinates the swap is
\[
J_i(c,d)=(a_i d,a_i^{-1}c).
\]
If the two swap coefficients differ, \(J_1(\alpha)=J_2(\alpha)\) only at the origin, where the swap fixes \(\alpha\). The masks therefore intersect in exactly \(\alpha\) for every digit pair.

One sufficient reduction bound is \(q>4^{\varphi(N)}\), where \(N=\operatorname{lcm}(h_3,h_5)\) at that guard. A new collision would make a nonzero difference of two sums of \(N\)-th roots of unity vanish modulo a prime above \(q\). Its nonzero integer norm has magnitude at most \(4^{\varphi(N)}\).

That numerical cutoff **cannot** prove a growing family with bounded private ratios. If \(h_3=pr_3,\ h_5=pr_5\) and \(r_3,r_5\le R\) for fixed \(R\), every candidate guard divides
\[
\gcd(3^{pr_3}-1,5^{pr_5}-1).
\]
The Bugeaud–Corvaja–Zannier bound gives \(\log q=o(p)\), uniformly over the finitely many ratio pairs. It also bounds the number of candidate guards by \(o(p/\log p)\), since each is at least \(p+1\). Meanwhile \(\varphi(N)\ge p-1\). This rules out reaching the sufficient norm cutoff at large \(p\). It leaves open whether actual candidates avoid enough collisions at smaller sizes. [Bugeaud, Corvaja and Zannier, *An upper bound for the G.C.D. of \(a^n-1\) and \(b^n-1\)*](https://doi.org/10.1007/S00209-002-0449-Z)

## Native test of the additional CRT constraint

Use center \(31\) and guards \(683,1861\). Their prime-level order pairs are \((30,3),(31,682),(310,31)\), respectively. The two guards share exactly \((31,31)\) in their full orders, and their lift factors are private. The guard-only test gives \(\max_\alpha E_\alpha=63/220\) across all 961 pairs.

The center’s prime-level match requires \(c\equiv5\pmod{10}\), a digit also observed by guard 1861. With this digit fixed, the power pair at 1861 is uniquely determined by \((c,d)\bmod31\). Its sum is zero there exactly on \(c\equiv3d\pmod{31}\), so no unit target at that guard can use those pairs with the center. Off the line, the filtered test gives \(\max E_\alpha=6/11\). The replay constructs an exact joint witness for every one of those 930 pairs at the fixed center residue \(31\bmod31^2\).

The row at 1861 is an exact valuation-one guard in this experiment. Since \(1861\equiv1\bmod4\), it is not a bad-prime witness for the two-square criterion. The result concerns unrestricted exponent relations and gives no ordinary-height bound. [Public project theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Inline replay

The standard-library replay retains the full center condition, uses unfiltered masks for rivals, and verifies the three-row witnesses by direct modular powers.

```python
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt

p,q,r = 31,683,1861
P = (p,q,r)

def cycle(b,m):
    a = [1]
    while a[-1]*b % m != 1:
        a.append(a[-1]*b % m)
    return a

assert all(all(m % d for d in range(2,isqrt(m)+1)) for m in P)
A = {m:tuple(cycle(b,m) for b in (3,5)) for m in P}
h = {m:tuple(map(len,A[m])) for m in P}
L = {
    m:tuple(k*(m if pow(b,k,m*m) != 1 else 1)
            for b,k in zip((3,5),h[m]))
    for m in P
}
assert list(h.values()) == [(30,3),(31,682),(310,31)]
assert list(L.values()) == [(930,93),(21173,465806),(576910,57691)]
assert tuple(gcd(a,b) for a,b in zip(L[q],L[r])) == (p,p)
for m in (q,r):
    assert all(k % m for j in P if j != m for k in L[j])
    assert any(a != b for a,b in zip(h[m],L[m]))

def data(m, filter_center=False):
    masks = [set() for _ in range(m)]
    targets = [{} for _ in range(p*p)]
    for c,x in enumerate(A[m][0]):
        for d,y in enumerate(A[m][1]):
            t = (x+y) % m
            if t:
                a = c%p*p+d%p
                masks[t].add(a)
                if not filter_center or c%10 == 5:
                    targets[a][t] = c,d
    rivals = [Counter(j for t in row for j in masks[t] if j != i)
              for i,row in enumerate(targets)]
    return targets,masks,rivals

U,M,X = data(q)
V,N,Y = data(r)
W,_,Z = data(r,True)

def scores(U,V,X,Y):
    return [
        Fraction(sum(v*Y[a][j] for j,v in X[a].items()),
                 len(U[a])*len(V[a]))
        for a in range(p*p) if U[a] and V[a]
    ]

S = scores(U,V,X,Y)
F = scores(U,W,X,Z)
assert (len(S),max(S)) == (961,Fraction(63,220))
assert (len(F),max(F)) == (930,Fraction(6,11))
assert {divmod(i,p) for i,row in enumerate(W) if not row} == {
    (3*d % p,d) for d in range(p)
}

def crt(rows):
    x,M = 0,1
    for y,m in rows:
        g = gcd(m,M)
        assert (y-x) % g == 0
        z = m//g
        x += M*((y-x)//g*pow(M//g,-1,z) % z)
        M *= z
    return x % M

def shift(m,c,d):
    return (pow(3,c,m*m)+pow(5,d,m*m)) % (m*m)

def hit(n,m,c,d):
    z = (n-shift(m,c,d)) % (m*m)
    return z != 0 and z % m == 0

for a,row in enumerate(W):
    if not row:
        continue
    t,u = next((t,u) for t in U[a] for u in row if M[t]&N[u] == {a})
    C,D = U[a][t],row[u]
    for d0,y in enumerate(A[p][1]):
        c0 = A[p][0].index(-y % p)
        assert c0 % 10 == 5
        w = tuple(crt(((C[j],h[q][j]),(D[j],h[r][j]),(z,h[p][j])))
                  for j,z in enumerate((c0,d0)))
        if hit(p,p,*w):
            break
    else:
        raise AssertionError("missing center lift")
    T = (p,(shift(q,*w)+q) % (q*q),(shift(r,*w)+r) % (r*r))
    n = crt(zip(T,(m*m for m in P)))
    assert all(hit(n,m,*w) for m in P)
    assert (T[1]%q,T[2]%r) == (t,u)
    assert w[0]%p*p+w[1]%p == a
```
## All-inert full pins at center 23, preserving all full center residues

**Center 23 has full two-dimensional pin coverage with every row prime \(3\bmod4\).** The guards are 599 and 6211. For each of the \(23^2=529\) digit pairs, I verified one integer target that pins the pair, makes both guards essential, and admits an exact hit at the center. At each such target, **every** full center residue pair that already gives an exact center hit can be preserved when joining the guards.

## Guard coverage and center compatibility

| Row prime | Orders of \(3,5\bmod q\) | Orders modulo \(q^2\) |
|---:|---:|---:|
| 23 | \(11,22\) | \(253,506\) |
| 599 | \(299,299\) | \(179101,179101\) |
| 6211 | \(230,69\) | \(1428530,428559\) |

The guard-only first moment is at most **\(163/195<1\)** across all 529 pairs. For a desired pair, this moment averages the number of rival pairs in the intersection over the two sets of unit targets that admit the desired pair. The average is computed from the actual power cycles. It certifies a singleton intersection, and the replay also finds one with both individual masks larger than a singleton for every pair.

The separate CRT check is exact: **every pairwise gcd of full orders is 23 in both coordinates**. The guards therefore observe the center’s two 23-primary digits and no other center order digits. After choosing a unit target and one local witness for each guard, I set its prime-square target to the witness shift plus the guard prime. These lifts stay fixed while the center residue pair varies. CRT joins the **full** order residues, so the resulting hits have valuation exactly one at all three primes.

### Why the center has no missing line

Here is the general fact used to check center usability. Fix both \(p\)-primary exponent digits and take a target \(pt\bmod p^2\), with \(t\ne0\bmod p\). At a prime-level match \(3^c+5^d\equiv0\bmod p\), write
\[
-3^c/5^d\equiv1+p\lambda\pmod{p^2}.
\]
The fixed primary digits determine \(\lambda\). The sum modulo \(p^2\) is then \(-p\lambda5^d\). If \(\lambda=0\), every prime-level match gives an exact hit. Otherwise, at most one value of \(5^d\bmod p\) can cause cancellation. Distinct prime-level matches in the two actual order cycles have distinct \(5^d\) values.

At 23 there are 11 prime-level matches, so each pinned pair has at least 10 exact center residue pairs at the fixed center target \(23\bmod529\). The replay checks the full distribution: **253** digit pairs have 10 exact center residues each, and **276** have 11. It joins all **5,566** full center residue pairs to the already fixed guard targets.

## Fixed-target deletion control

Take
\[
n=4\,622\,086\,607\,680\,396,\qquad
n\equiv(23,601,7259220)\pmod{(23^2,599^2,6211^2)}.
\]
The guards pin \((c,d)\equiv(0,0)\pmod{23}\), and \((108129721336,58071887341)\) hits all three rows. At the **same** target, removing either guard permits a different pin while retaining an exact center hit:

| Guard removed | Witness \((c,d)\) | Pair modulo 23 |
|---:|---:|---:|
| 599 | \((2025,687)\) | \((1,20)\) |
| 6211 | \((1012,1111)\) | \((0,7)\) |

This is a finite family at a different center. I did not establish unboundedly many such centers or an ordinary-height bound on the witnesses. The exact bad-prime hits are conditions on the unrestricted exponent panel. [Public project theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Inline exact replay

The standard-library replay checks primality, all full order overlaps, the exact guard-only first moment, preservation of every exact center residue pair, and both deletion witnesses.

```python
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, isqrt

p, q, r = 23, 599, 6211
P = (p, q, r)

def cycle(base, m):
    a = [1]
    while a[-1]*base % m != 1:
        a.append(a[-1]*base % m)
    return a

assert all(m % 4 == 3 and all(m % d for d in range(2, isqrt(m)+1))
           for m in P)
A = {m: tuple(cycle(b,m) for b in (3,5)) for m in P}
h = {m: tuple(map(len,A[m])) for m in P}
L = {
    m: tuple(k*(m if pow(b,k,m*m) != 1 else 1)
             for b,k in zip((3,5),h[m]))
    for m in P
}
assert list(h.values()) == [(11,22),(299,299),(230,69)]
assert list(L.values()) == [(253,506),(179101,179101),(1428530,428559)]
for i,m in enumerate(P):
    for j in P[:i]:
        assert tuple(gcd(x,y) for x,y in zip(L[m],L[j])) == (p,p)

def data(m):
    masks = [set() for _ in range(m)]
    targets = [{} for _ in range(p*p)]
    X,Y = A[m]
    for c,x in enumerate(X):
        for d,y in enumerate(Y):
            t = (x+y) % m
            if t:
                a = (c % p)*p + d % p
                masks[t].add(a)
                targets[a][t] = c,d
    rivals = [
        Counter(j for t in row for j in masks[t] if j != i)
        for i,row in enumerate(targets)
    ]
    return targets,masks,rivals

U,M,X = data(q)
V,N,Y = data(r)
assert all(U+V)
scores = [
    Fraction(sum(v*Y[a][j] for j,v in X[a].items()),
             len(U[a])*len(V[a]))
    for a in range(p*p)
]
assert max(scores) == Fraction(163,195)

def crt(rows):
    x,M = 0,1
    for y,m in rows:
        g = gcd(M,m)
        assert (y-x) % g == 0
        z = m//g
        x += M*((y-x)//g*pow(M//g,-1,z) % z)
        M *= z
    return x % M

def shift(m,c,d):
    return (pow(3,c,m*m)+pow(5,d,m*m)) % (m*m)

def hit(n,m,c,d):
    z = (n-shift(m,c,d)) % (m*m)
    return z != 0 and z % m == 0

center = [[] for _ in range(p*p)]
for c,d in product(*(range(k) for k in L[p])):
    if hit(p,p,c,d):
        center[(c % p)*p+d % p].append((c,d))
assert Counter(map(len,center)) == {10:253,11:276}

for a in range(p*p):
    t,u = next((t,u) for t in U[a] for u in V[a]
               if M[t] & N[u] == {a} and len(M[t]) > 1 and len(N[u]) > 1)
    C,D = U[a][t],V[a][u]
    T = (p,(shift(q,*C)+q) % (q*q),(shift(r,*D)+r) % (r*r))
    assert (T[1] % q,T[2] % r) == (t,u)
    n = crt(zip(T,(m*m for m in P)))
    for phase in center[a]:
        w = tuple(
            crt(((phase[j],L[p][j]),(C[j],L[q][j]),(D[j],L[r][j])))
            for j in (0,1)
        )
        assert tuple(w[j] % L[p][j] for j in (0,1)) == phase
        assert (w[0] % p)*p+w[1] % p == a
        assert all(hit(n,m,*w) for m in P)

n = crt(zip((23,601,7259220),(m*m for m in P)))
assert n == 4622086607680396
assert M[601 % q] & N[7259220 % r] == {0}
assert all(hit(n,m,108129721336,58071887341) for m in P)
for deleted,w in [(q,(2025,687)),(r,(1012,1111))]:
    assert (w[0] % p,w[1] % p) != (0,0)
    assert {m for m in P if hit(n,m,*w)} == set(P)-{deleted}
```