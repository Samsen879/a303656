# Protected order closure and a full chronological separator chart through 8527

**The full chronological panel through \(8527\) has a uniform positive budget.** For every integer target \(n\), at least **six of the seven** second \(7\)-primary digit labels extend to a \(3,5\) exponent phase that passes every earlier local norm test and is a unit at \(8527\). If five selected readers are kept frozen, at least **four** labels still extend. Both bounds are attained on the displayed chart. The argument allows arbitrary readings at the earlier primes.

### Repair in increasing prime order

Fix the moving axis \(a^c\), and protect the rows whose chosen residues must be preserved, including the terminal. Put every inert row with an unavailable primary coordinate or with \(a^{p-1}\equiv1\bmod p^2\) into the protected set. Close this set downward: if a protected row at \(t\) reads the primary coordinate of an inert \(p<t\), protect \(p\) too. For unit rows, the read is detected by \(p\mid\operatorname{ord}_t(a)\). Higher \(t\)-adic precision adds only factors of \(t\) to that order.

After satisfying the protected rows, process every other inert prime in increasing order. At an ordinary \(p\), let \(E_p\) move its own primary coordinate and preserve the others. Then \(v_p(a^{E_p}-1)=1\). If the remainder is divisible by \(p\), choose the first digit to make it zero modulo \(p^2\), and choose the next digit to keep it nonzero modulo \(p^3\). This gives exact valuation two. The move preserves all protected rows by closure. It preserves every earlier repair because an exponent period at \(t<p\) has no factor \(p\). A later repairable reader can see the move and then repair its own row. This uses the ordinary-primary repair from the finite-obstruction framework. The closure identifies which rows can be removed from the separator budget while preserving a terminal unit. [Finite-obstruction framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Group the frozen readers by their projection on each inherited component \(X\). A row reading the separator \(s\) can delete alternatives at only one \(s\)-label, by projecting its collision onto the separator’s primary character. At that label it can delete at most the largest fibre of its projection on \(X\). Emptying a label costs \(|X|\) deletions. This charges only the rows left after repair closure.

### The actual \(3,5\) prefix

Take \(s\) on the second \(7\)-primary digit of \(c\), with alternatives \(i\) on its first \(3\)-primary digit and \(j\) on its first \(5\)-primary digit. The complete list of earlier nonnative readers of \(s\), projected onto these three digits before repairs, is:

| Projection | Earlier inert readers |
|---|---|
| \(s\) | \(491,1667,4019,5783,6959,7547\) |
| \((s,i)\) | \(1471,2647,3823,4999,6763\) |
| \((s,j)\) | \(7351\) |

Among the 532 inert primes \(7\le p<8527\), only \(11\) is nonordinary on the \(3\)-axis. The protected unit rows are \(7,11,8527\), with orders \(6,5,2842=2\cdot29\cdot49\). Their closure adds no inert unit row. At \(7\), at least two \(i\)-labels give units. At \(11\), at least four \(j\)-labels give units. The terminal order reads \(s\) and neither \(i\) nor \(j\), so it excludes at most one of seven labels. The other 530 earlier rows can all be repaired.

For the four-label version, also freeze \(1471,2647,3823,4999,7351\). Their order factors add no further inert unit row. The four \((s,i)\) readers can empty at most two labels, since each deletes one pair and there are at least two inherited \(i\)'s. The \((s,j)\) reader can empty none. Charging one label for the terminal gives \(7-2-1=4\).

The tests at \(2,3\) allow every \(n\). Choose \(d\in\{2,3\}\) so \(n-5^d\) is a unit at \(3\). For odd \(n\), choose the parity of \(c\) to make the remainder \(1\bmod4\). For even \(n\), write \(A=n-5^d\). When \(A\bmod8\) is \(3\) or \(5\), choose \(c\) to give remainder \(2\bmod8\). For \(A\equiv7\bmod8\), odd \(c\bmod4\) gives a choice with remainder \(4\bmod16\). For \(A\equiv1\bmod8\), even \(c\bmod8\) gives a choice with remainder \(8\bmod32\). All subsequent moves preserve this \(c\bmod8\).

```python
from itertools import product
from math import isqrt, lcm

q = 8527
F = (1471,2647,3823,4999,7351)
def prime(p):
    return p > 1 and all(p % k for k in range(2,isqrt(p)+1))
P = [p for p in range(7,q,4) if prime(p)]
assert prime(q) and len(P) == 532
assert [p for p in P if pow(3,p-1,p*p) == 1] == [11]

def order(p):
    return next(k for k in range(1,p) if pow(3,k,p) == 1)
assert list(map(order,(7,11)+F+(q,))) == [6,5,294,2646,3822,4998,2450,2842]
groups = {():[], (3,):[], (5,):[]}
for p in P:
    if (p-1) % 49 == 0:
        o = order(p)
        if o % 49 == 0:
            groups[tuple(r for r in (3,5) if o%r == 0)].append(p)
assert list(groups.values()) == [
    [491,1667,4019,5783,6959,7547],
    [1471,2647,3823,4999,6763], [7351]]

T = {p:p*p*(p-1) for p in P}
L = lcm(16,q-1,*T.values())
def step(p):
    a = p
    while L % (a*p) == 0:
        a *= p
    return (L//a)*pow(L//a,-1,a)
U = {p:step(p) for p in set(P)|{3,5}}
def two(z):
    return z%4 == 1 or z%8 == 2 or z%16 == 4 or z%32 == 8

def solve(n, frozen=()):
    d = next(d for d in (2,3) if (n-5**d)%3)
    A = n-5**d
    a = next(a for a in range(8) if two(A-pow(3,a,32)))
    protected = (7,11)+frozen
    def rem(c,p):
        return (A-pow(3,c%T[p],p**3)) % p**3
    def unit(c,p):
        return (A-pow(3,c%(p-1),p)) % p
    out = []
    for s in range(7):
        b = L+a+7*s*U[7]
        if not unit(b,q):
            continue
        options = (b+i*U[3]+j*U[5] for i,j in product(range(3),range(5)))
        c = next((c for c in options if all(unit(c,p) for p in protected)),None)
        if c is None:
            continue
        fixes = 0
        for p in P:
            if p in protected:
                continue
            z = rem(c,p)
            if z%p == 0:
                fixes += 1
                g = (pow(3,U[p]%T[p],p**3)-1)//p % p
                c += (z//p*pow(pow(3,c%T[p],p)*g,-1,p)%p)*U[p]
                if rem(c,p) == 0:
                    c += p*U[p]
        assert two(A-pow(3,c%8,32)) and A%3 and unit(c,q)
        assert all((z:=rem(c,p)) and (z%p or z%p**2 == 0) for p in P)
        out.append((s,fixes))
    return out

n = 2308099835306108010159862552653025306194985171803371438703
assert solve(n) == [(0,1),(1,1),(2,1),(3,1),(4,0),(5,0)]
assert solve(n,F) == [(2,1),(3,0),(4,0),(5,0)]
assert len(solve(3920)) == 7
```

**Height and norm scope.** This excludes a complete *local phase* obstruction through \(8527\) for every target. It gives no height bound at a prescribed \(n\). The distinction is real at \(3920\): all seven separator labels extend in the replay, yet each of the 35 active pairs \(0\le c\le6,\ 0\le d\le4\) in the quarter box has an odd-valuation inert divisor below \(8527\). Outside that box, \(3920=24^2+34^2+3^7+5^0\). The terminal-unit proof uses no repair at \(8527\) and would apply to a common-Wieferich terminal with a protected core and a positive separator budget of the same kind. Extending the uniform exclusion beyond this prefix remains open.

Independent BigInt checked all 532 earlier inert rows, all actual fixes and terminal units in the three displayed runs, and all 35 active quarter-height failures at 3920. This is a uniform local phase conclusion with no ordinary-height guarantee.
