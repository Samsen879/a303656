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