# Pinned center OR: deletion-minimal exact odd-valuation stars

A pinned lift digit can implement a native **OR condition** on the edge digits. This gives deletion-minimal inconsistent stars of arbitrary size, with exact valuation 1 at every leaf and one exact **odd** valuation at the center. I verified a four-row star in which the center also has valuation 1, so the entire example uses prime-square orders. I did not establish that growing stars can always keep the center at valuation 1.

There is also a sharp structural restriction in the fully zero-target lane. When every row has \(n\equiv0\pmod{p^2}\), any inconsistency in the edge-labelled Kummer family is already witnessed by at most **two rows**, even with fixed coarse congruences.

## The star construction

Assign distinct odd primes \(\ell_1,\ldots,\ell_k>5\) to the edges of a star. Choose the center prime \(p\) and the leaf primes \(p_i\) by the cyclotomic and Kummer construction, with \(p_j\equiv47\pmod{60}\). Each edge label occurs to the first power in the two incident \(p_j-1\), and the remaining odd order factors and row primes are private. At the center, prescribe
\[
3^{(p-1)/\ell_i}=5^{(p-1)/\ell_i}\ne1\pmod p.
\]
At leaf \(i\), prescribe
\[
3^{(p_i-1)/\ell_i}
=\bigl(5^{(p_i-1)/\ell_i}\bigr)^2\ne1\pmod{p_i}.
\]
These prescriptions use Kummer actions \((1,1)\) and \((2,1)\), respectively, on the two radicals. They are available because 3 and 5 have independent classes modulo \(\ell_i\)-th powers in the cyclotomic field. Chebotarev gives the row primes with the required Frobenius actions and order-factor exclusions. At a prime-level match with \(n\equiv0\bmod p_j\), the equations on edge \(i\) are therefore \(d=c\bmod\ell_i\) at the center and \(d=2c\bmod\ell_i\) at the leaf. [Sutherland, *Global class field theory and the Chebotarev density theorem*](https://math.mit.edu/classes/18.785/2025/lectures.html)

Fix \(c\) even and \(d\) odd. Pin both exponents to zero on the odd private factors of the \(p_j-1\). At each leaf also pin both exponents to zero modulo \(p_i\), and take \(n\equiv p_i\pmod{p_i^2}\). Then every prime-level match at that leaf is an exact valuation-one hit. The two unit powers have zero sum modulo \(p_i^2\) whenever their sum is zero modulo \(p_i\), since both exponents are multiples of \(p_i\).

At the center, choose a base \(q\in\{3,5\}\) and let \(s=v_p(q^{p-1}-1)\). Take the least odd \(r\ge s\). Start from the baseline with all edge digits zero and both exponents zero modulo \(p^r\). Add \((p-1)p^{r-s}\) to the exponent of \(q\), and fix the resulting two residues modulo \(p^r\) as part of the coarse stratum. Let \(c_0,d_0\) be the resulting baseline and prescribe
\[
n\equiv 3^{c_0}+5^{d_0}\pmod{p^{r+1}}.
\]
This target residue has valuation exactly \(r\), by the binomial lifting formula.

On any prime-level match at the center, the ratio \(\rho=-3^c/5^d\) has the same residue modulo \(p^{r+1}\) as at the baseline. Indeed, the quotient of two such ratios is killed by \(p-1\) because the exponents agree modulo \(p^r\), and it reduces to 1 modulo \(p\). Consequently,
\[
3^c+5^d\equiv 5^d(1-\rho)\pmod{p^{r+1}},
\qquad v_p(1-\rho)=r.
\]
The exact center hit \(v_p(n-3^c-5^d)=r\) is therefore equivalent to \(5^d\not\equiv5^{d_0}\pmod p\). With the private order components pinned, this says **at least one edge digit is nonzero**.

All leaves together force every edge digit to zero, making the center fail. Deleting the center admits the zero assignment. Deleting leaf \(i\) admits the assignment \(c=d=1\bmod\ell_i\), with every other edge digit zero. CRT supplies exponents in the same fixed coarse stratum for every deletion witness. The row targets also join by CRT to one fixed integer \(n\).

This construction is unconditional for the stated odd valuations. It gives an exact-valuation-one star whenever the chosen center is non-Wieferich to at least one base. The Kummer prescription alone does not give that prime-square condition for arbitrarily many incident labels.

## Why zero targets cannot create the same obstruction

In the edge-labelled Kummer family, fix the parities and allow any additional coordinate-wise coarse congruences. If every \(n\equiv0\pmod{p_j^2}\), the prime-level equation separates into one linear relation on each edge label and conditions on private factors. Once the prime-level equation holds, valuation exactly 1 asks whether the private \(p_j\)-component of \(-3^c/5^d\) differs from 1 modulo \(p_j^2\). That test depends only on the private lift digits, including any coarse pins.

Thus failure occurs either in one row’s private constraints or on a single edge, where only its two endpoints impose constraints. Distinct edge labels are independent under CRT. The two-row bound is attained by putting different slopes at the endpoints of one edge and fixing \(c\equiv1\) modulo its label. Each row allows a value of \(d\), but the two values differ. Twisting slopes in this zero-target family therefore does not propagate a contradiction around a cycle of distinct labels.

## Exact prime-square replay

The star below uses edge labels \(7,11,13\). At one fixed target and within one fixed coarse stratum, the replay checks that all four rows are inconsistent, each single deletion is feasible, and all \(1001\) center-diagonal assignments have the stated OR behavior. It also checks two positive controls. One changes only the center target. The other keeps the target and changes the pinned lift digit. The standard-library replay below verifies every claimed finite assignment.

```python
from itertools import combinations, product
from math import gcd, isqrt, prod

P = (376662287, 376688747, 376727627, 376857287)
E = (7, 11, 13)
S = (E, (7,), (11,), (13,))
p = P[0]

def factors(n):
    out = set()
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out

def order(q, r):
    h = r*(r-1)
    for f in factors(r-1) | {r}:
        while h % f == 0 and pow(q, h//f, r*r) == 1:
            h //= f
    return h

def crt(values, moduli):
    M = prod(moduli)
    return sum(x*(M//m)*pow(M//m, -1, m)
               for x, m in zip(values, moduli)) % M

for i, (r, labels) in enumerate(zip(P, S)):
    assert r % 60 == 47
    assert all(r % d for d in range(3, isqrt(r)+1, 2))
    for ell in labels:
        assert (r-1) % ell == 0 and (r-1) % (ell*ell) != 0
        z = pow(5, (r-1)//ell, r)
        assert z != 1
        assert pow(3, (r-1)//ell, r) == pow(z, 1 if i == 0 else 2, r)

L = [tuple(order(q, r) for q in (3,5)) for r in P]
for i, j in combinations(range(len(P)), 2):
    shared = prod(set(S[i]) & set(S[j]))
    for x, y in zip(L[i], L[j]):
        g = gcd(x, y)
        assert g // gcd(g, 2) == shared
assert pow(3, p-1, p*p) != 1

private = [(r-1)//(2*prod(labels)) for r, labels in zip(P,S)]
mods = [2, *private, *P, *E]
A = prod(mods[:-len(E)])
assert all(A*prod(E) % h == 0 for row in L for h in row)

def exponents(xs, pin=p-1):
    c = crt([0, *([0]*4), pin, 0, 0, 0, *xs], mods)
    d = crt([1, *([0]*8), *xs], mods)
    return c, d

def local_sum(r, c, d):
    return (pow(3,c,r*r) + pow(5,d,r*r)) % (r*r)

zero = (0,0,0)
baseline = exponents(zero)
t0 = local_sum(p, *baseline)
assert t0 == 84929873115388207 and t0 % p == 0
n = crt([t0, *P[1:]], [r*r for r in P])

def hits(target, exps):
    out = set()
    for r in P:
        residual = (target-local_sum(r,*exps)) % (r*r)
        if residual != 0 and residual % r == 0:
            out.add(r)
    return out

assert hits(n, baseline) == set(P[1:])
for i, deleted in enumerate(P[1:]):
    xs = tuple(int(j == i) for j in range(len(E)))
    assert hits(n, exponents(xs)) == set(P)-{deleted}

# Any center hit must be diagonal by the power tests above.
for xs in product(*(range(ell) for ell in E)):
    w = exponents(xs)
    assert all((a-b) % A == 0 for a,b in zip(w,baseline))
    observed = hits(n,w)
    assert (p in observed) == any(xs)
    assert observed & set(P[1:]) == {
        r for x,r in zip(xs,P[1:]) if x == 0
    }

control = crt([(t0+p) % (p*p), *P[1:]], [r*r for r in P])
assert hits(control, baseline) == set(P)
assert hits(n, exponents(zero, pin=0)) == set(P)
```

The growing inconsistency requires the prescribed coarse stratum. The last replay assertion demonstrates why the distinction matters: freeing the center’s pinned digit restores a common hit at the original target. This is separate from the project’s restricted active-shift obstructions and does not bound the ordinary height of the witnesses. [Public theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)
## Finite internal pin and a necessary dependency path

Two exact auxiliary rows can pin a center digit **without a prescribed coarse stratum**. I verified a native example at primes \(7,547,883\): the auxiliaries force \((c,d)\equiv(0,33)\pmod{42}\), which makes the center fail. Removing any row restores feasibility at the same target.

I also proved an obstruction for extending the star. A center whose target has valuation one can be relaxed to its prime-level equation unless a chain of actual order divisibilities reaches it from a row with a unit target. I did not establish auxiliary pins for arbitrarily large stars.

## Which auxiliaries can force a lift digit?

For each row prime \(q>5\), write \(L_{q,b}=\operatorname{ord}_{q^2}(b)\) for \(b=3,5\). Use the following set of rows:

1. Start with the rows for which \(q\nmid n\).
2. Add a row at \(p\) with \(v_p(n)=1\) whenever \(p\mid L_{q,b}\) for some already included row \(q\) and some base \(b\).
3. Repeat until no row can be added.

**Normalization lemma.** For all rows with \(v_p(n)=1\) outside this set, replace the exact valuation-one condition by its divisibility condition modulo \(p\). This preserves feasibility of the full panel over unrestricted nonnegative exponents. In fact, any solution of the relaxed panel can be converted to an exact solution by setting both exponents’ \(p\)-primary components to zero simultaneously at all the relaxed rows.

To prove it, work modulo the lcm of the full orders in each coordinate. Reset those odd primary components by CRT. Every included row retains both full order residues by construction. At every other row \(q\), the prime-level equation is \(3^c=-5^d\bmod q\). In discrete logs, its right side has order two, so all its odd primary equations are homogeneous. Resetting the selected components to zero preserves these equations.

Once the prime-level match holds, \(-3^c/5^d\bmod q^2\) belongs to the kernel of reduction modulo \(q\). Its value depends only on the \(q\)-primary exponent components. If \(q^2\mid n\), these components were left alone and the exact hit is preserved. At a relaxed row, the reset makes the ratio 1 modulo \(q^2\), so \(3^c+5^d\equiv0\pmod{q^2}\). Since \(v_q(n)=1\), this gives the exact hit.

In particular, adding only auxiliaries whose targets vanish modulo their row primes cannot internalize the star’s nonzero center lift digit. More generally, an auxiliary mechanism that prevents this reset must reach the center from a unit-target row. For distinct odd rows, an order-divisibility step \(q\to p\) requires \(p\mid q-1\), hence \(q\ge2p+1\). A chain of \(j\) steps to center \(p\) must begin at a unit-target prime at least \(2^j(p+1)-1\).

## A native internal pin

Take the target residues
\[
n\equiv(14,\ 262793,\ 558102)\pmod{(7^2,\ 547^2,\ 883^2)}.
\]
Their least nonnegative CRT representative is \(10{,}538{,}571{,}804{,}544\). The auxiliary targets are units at 547 and 883. The actual orders are:

| Prime | Orders of \(3,5\) modulo \(p\) | Orders modulo \(p^2\) |
|---:|---:|---:|
| 7 | \(6,6\) | \(42,42\) |
| 547 | \(14,546\) | \(7658,298662\) |
| 883 | \(126,126\) | \(111258,111258\) |

The two auxiliary relations, projected onto \((c\bmod42,d\bmod42)\), intersect in exactly \(\{(0,33)\}\). This internally fixes \((c,d)\equiv(0,5)\pmod7\) and the rest of the center’s order residues. The auxiliary prime-square lifting factors are private, so their prime-level projections are exact. At 7 the full periods are needed: the forced shift is \(14\bmod49\), equal to the target, and the residual is zero modulo 49.

| Row removed | Exact-hit witness \((c,d)\) for the remaining rows |
|---:|---:|
| 7 | \((0,75)\) |
| 547 | \((40,5)\) |
| 883 | \((36,375)\) |

Changing only the center residue from 14 to 21 gives the positive control \(n=740{,}393{,}232{,}502\), where \((0,75)\) hits all three rows.

This is an unrestricted, deletion-minimal exact-hit obstruction and uses only explicitly verified primes and orders. It does not establish a growing family of internal pins or an ordinary-height bound. It also differs from the public project’s N-009, which concerns restricted active-shift families. [Public theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Inline exact replay

The standard-library replay uses the full prime-square orders at the center, checks the private lifting conditions at the auxiliaries, and verifies the deletion witnesses and control.

```python
from itertools import product
from math import gcd, isqrt, prod

P = (7, 547, 883)
T = (14, 262793, 558102)
G = set(product(range(42), repeat=2))

def cycle(q, m):
    values = [1]
    while values[-1]*q % m != 1:
        values.append(values[-1]*q % m)
    return values

assert all(all(p % d for d in range(2, isqrt(p)+1)) for p in P)
h = {p: tuple(len(cycle(q,p)) for q in (3,5)) for p in P}
L = {
    p: tuple(b*(p if pow(q,b,p*p) != 1 else 1)
             for q,b in zip((3,5),h[p]))
    for p in P
}
assert list(h.values()) == [(6,6),(14,546),(126,126)]
assert list(L.values()) == [(42,42),(7658,298662),(111258,111258)]
for p in P[1:]:
    assert all(b % p for r in P if r != p for b in L[r])
    assert any(a != b for a,b in zip(h[p],L[p]))
for i,p in enumerate(P):
    for r in P[:i]:
        assert all(42 % gcd(x,y) == 0 for x,y in zip(L[p],L[r]))

def projected(p, t):
    u,v = (gcd(42,b) for b in h[p])
    A,B = (cycle(q,p) for q in (3,5))
    allowed = {(c % u,d % v) for c,x in enumerate(A)
               for d,y in enumerate(B) if (x+y-t) % p == 0}
    return {(c,d) for c,d in G if (c % u,d % v) in allowed}

def hit(n, p, c, d):
    m = p*p
    r = (n-pow(3,c,m)-pow(5,d,m)) % m
    return r != 0 and r % p == 0

def target(residues):
    M = prod(p*p for p in P)
    return sum(r*(M//(p*p))*pow(M//(p*p),-1,p*p)
               for r,p in zip(residues,P)) % M

pin = set.intersection(*(projected(p,t) for p,t in zip(P[1:],T[1:])))
assert pin == {(0,33)}
assert not any(hit(T[0],7,c,d) for c,d in pin)

n = target(T)
assert n == 10538571804544
for removed,w in zip(P, [(0,75),(40,5),(36,375)]):
    assert {p for p in P if hit(n,p,*w)} == set(P)-{removed}

control = target((21,*T[1:]))
assert control == 740393232502
assert all(hit(control,p,0,75) for p in P)
```
## Projection-density obstruction and exact translated internal pins at 19

At center **19**, two native unit-target rows give an unrestricted, deletion-minimal obstruction. One row, at 2851, pins \((c,d)\equiv(1,7)\pmod{19}\) by itself. Its multiplicative orbit gives **19 distinct exact pins** at the same center. I also proved a projection-size bound that rules out singleton pins for sufficiently dense independent guards. These results leave open whether suitable guards exist at unboundedly many centers.

## When independent guards are too dense to pin

Consider a guard prime \(q>5\) and a unit target \(t\ne0\bmod q\). Let \(h_3,h_5\) be the actual prime-level orders. Suppose the guard observes exponent residues modulo \(s_3\mid h_3\) and \(s_5\mid h_5\). Write \(r_b=h_b/s_b\) for the private order size, and let \(M_t\) be the number of pairs of power values summing to \(t\bmod q\). If \(B_t\) is the number of occupied projected cells, then for \(M_t>0\),
\[
B_t\ \ge\
\max\!\left\{
\left\lceil\frac{M_t}{\min(r_3,r_5)}\right\rceil,\ 
\left\lceil
\frac{M_t^2}{M_t+(r_3-1)(r_5-1)-(\gcd(r_3,r_5)-1)}
\right\rceil
\right\}.
\]
If \(M_t=0\), the projected relation is empty.

The first bound counts the maximum number of matches in a cell. For the second, two matches in the same cell have the form \((x,y)\) and \((ux,vy)\), where \(u,v\) belong to the two private subgroups. The identity pair contributes \(M_t\) to the second moment. If exactly one multiplier is 1, or if \(u=v\ne1\), there is no match with nonzero summands and \(t\ne0\). Each remaining multiplier pair determines at most one solution to \(x+y=ux+vy=t\). Counting those pairs and applying Cauchy–Schwarz gives the bound.

For independent guards on a common digit grid of size \(D\), put \(S_i=s_{i,3}s_{i,5}\). Assume their full pairwise order gcds are contained in the common grid, and that each discarded prime-square lift digit is private and adjustable. Then at least
\[
D\left(1-\sum_i(1-B_i/S_i)\right)
\]
grid points survive, with zero as a lower bound when the expression is negative. Each missing local cell rules out \(D/S_i\) grid points, and CRT joins the remaining local choices. In particular, a singleton pin requires a total missing fraction of at least \(1-1/D\). This gives an impossibility test using the lower bounds for \(B_i\), without computing the joint intersection.

This density test complements the earlier order-divisibility obstruction. If no chain from a unit-target row reaches a valuation-one center, its lift digit can be reset to zero. When a guard does reach the center, sufficient projected density can still rule out a pin. The independence hypothesis matters for the counting bound because additional shared digits can make locally surviving choices incompatible.

## A family of native pins at center 19

There is a simple translation rule. Suppose \(v_p(h_3)=v_p(h_5)=1\) at a guard \(q\), and a unit target \(t\) pins one digit pair modulo \(p\). Choose \(\lambda\) of order \(p\) in the intersection of the two base subgroups, and write \(\lambda=3^u=5^v\bmod q\). Multiplying both summands by \(\lambda^j\) bijects the representations of \(t\) and \(t\lambda^j\). The translated target pins the original pair plus \(j(u,v)\bmod p\). Thus one certified pin yields a line of \(p\) distinct pins. The target translation is modulo \(q\). Exact valuation-one lifts require the separate prime-square check.

At \(q=2851\), the actual orders are \(38=2\cdot19\) and \(95=5\cdot19\). Target \(1151\bmod2851\) has exactly one prime-level exponent pair, \((1,7)\), in those cycles. Since \(9=3^2=5^{75}\bmod2851\) has order 19, the 19 unit targets \(1151\cdot9^j\) pin
\[
(c,d)\equiv(1+2j,\ 7+75j)\pmod{19}.
\]
The replay supplies an exact prime-square lift for every member of the family.

For an unrestricted inconsistency, add guard 271 and take
\[
n\equiv(152,\ 4958,\ 80979)\pmod{(19^2,\ 271^2,\ 2851^2)}.
\]
The least CRT representative is \(86{,}044{,}526{,}251{,}904\). The guard at 2851 fixes \(c\bmod38\) and \(d\bmod19\). Guard 271 has two prime-level matches, \((1,7)\) and \((16,4)\) in its cycles, and constrains the remaining shared residues. Together with the center’s divisibility condition, only \((1,7)\) survives modulo the center’s full order pair \((342,171)\). Its shift is \(152\bmod361\), so the center fails the exact hit.

| Row removed | Exact-hit witness for the other two |
|---:|---:|
| 19 | \((1,7)\) |
| 271 | \((39,102)\) |
| 2851 | \((1,34)\) |

Changing only the center residue to 171 gives the positive control \(52{,}018{,}763{,}302{,}367\), hit at all three rows by \((1,7)\). These are unrestricted exponent relations, with no ordinary-height claim. The public project’s N-009 concerns restricted active-shift families. [Public theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Inline exact replay

The standard-library replay retains the full orders at 19, checks the auxiliary lift conditions, and verifies all deletion witnesses and translated pins.

```python
from math import gcd, isqrt, prod

P = (19, 271, 2851)
T = (152, 4958, 80979)
Q = (3, 5)

def cycle(q, m):
    a = [1]
    while a[-1]*q % m != 1:
        a.append(a[-1]*q % m)
    return a

def pairs(p, t):
    a, b = (cycle(q, p) for q in Q)
    index = {y: d for d, y in enumerate(b)}
    return [(c, index[(t-x) % p]) for c, x in enumerate(a)
            if (t-x) % p in index]

assert all(all(p % d for d in range(2, isqrt(p)+1)) for p in P)
h = {p: tuple(len(cycle(q,p)) for q in Q) for p in P}
L = {
    p: tuple(b*(p if pow(q,b,p*p) != 1 else 1)
             for q,b in zip(Q,h[p]))
    for p in P
}
assert list(h.values()) == [(18,9),(30,27),(38,95)]
assert list(L.values()) == [(342,171),(8130,7317),(108338,270845)]
for p in P[1:]:
    assert all(b % p for r in P if r != p for b in L[r])
    assert any(a != b for a,b in zip(h[p],L[p]))
assert tuple(gcd(a,b) for a,b in zip(L[271],L[2851])) == (2,1)

assert pairs(271,T[1]) == [(1,7),(16,4)]
assert pairs(2851,T[2]) == [(1,7)]
p = P[0]
A,B = (cycle(q,p*p) for q in Q)
survivors = {
    (c,d) for c,x in enumerate(A) for d,y in enumerate(B)
    if (x+y) % p == 0 and c % 38 == 1 and d % 19 == 7
    and (c % 6,d % 9) in {(1,7),(4,4)}
}
assert survivors == {(1,7)}
assert (A[1]+B[7]) % (p*p) == T[0]

def crt(residues):
    M = prod(p*p for p in P)
    return sum(t*(M//(p*p))*pow(M//(p*p),-1,p*p)
               for t,p in zip(residues,P)) % M

def hit(n,p,c,d):
    z = (n-pow(3,c,p*p)-pow(5,d,p*p)) % (p*p)
    return z != 0 and z % p == 0

n = crt(T)
assert n == 86044526251904
for removed,w in zip(P,[(1,7),(39,102),(1,34)]):
    assert {p for p in P if hit(n,p,*w)} == set(P)-{removed}

control = crt((171,*T[1:]))
assert control == 52018763302367
assert all(hit(control,p,1,7) for p in P)

q = 2851
targets = set()
for j in range(19):
    c,d = 1+2*j, 7+75*j
    t = 1151*pow(9,j,q) % q
    targets.add(t)
    assert {(x % 19,y % 19) for x,y in pairs(q,t)} == {(c % 19,d % 19)}
    lift = (pow(3,c,q*q)+pow(5,d,q*q)+q) % (q*q)
    assert lift % q == t and hit(lift,q,c,d)
assert len(targets) == 19
```