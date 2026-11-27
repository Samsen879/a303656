# A uniform separator-slice bound on an inherited arithmetic chart

A free separator digit gives a uniform guarantee when each reader has a bounded capacity to empty its slices. In the actual \(3,5\) panel below, **at least four of the seven separator labels retain a terminal-unit cell for every choice of the listed odd-prime target readings**, with the \(2,3\) conditions fixed. Four is sharp. At the preceding digit depth, the native valuation test can instead force a single label, which the frozen terminal can kill.

### Capacity bound for inherited charts

Let \(s\) be a free digit at source \(r\). After fixing \(s\), suppose the remaining reads split into components. In each component \(C\), let \(X_C\) be the nonempty set of alternatives inherited from tests that are constant in \(s\). The sets \(X_C\) may depend on the earlier target readings.

Work on one exponent axis, with different moving primary primes. For a row \(p\ne r\) that reads \(s\) and a projection of \(X_C\), a collision modulo \(p\) fixes **one value of \(s\) across the whole component**. Projecting onto the \(r\)-primary character gives this value because all other moving digits have coprime character orders. Within that slice, the collision fixes the tuple of other digits the row reads. Thus it can delete at most \(b_p\) alternatives, where \(b_p\) is the largest fibre of that read projection on \(X_C\). Charging first divisibility gives a valid upper bound on actual odd-valuation deletions.

Allow native tests in \(C\) to delete at most \(b_C^0\) pairs \((s,x)\) in total. Each empty slice in \(C\) costs \(|X_C|\) deletions, and each pair belongs to just one slice. A terminal that reads \(s\) can have a collision in at most one slice by the same character projection. Consequently the number of labels with a surviving terminal-unit cell is at least
\[
|D_r|-1-
\sum_C\left\lfloor
\frac{b_C^0+\sum_{p\text{ reading }C}b_p}{|X_C|}
\right\rfloor .
\]
At a surviving label, take one surviving alternative from each component. This uses separation **after fixing the same \(s\)** and requires no independence between separator slices. The bound is uniform whenever the inherited sizes and deletion budgets hold uniformly.

The native parity check matters. If varying \(s\) changes \(3^c\) first at an **even** valuation \(h\) at \(r\), an alternative with a forced odd valuation below \(h\) must be excluded before computing \(|X_C|\). For every other alternative, the native test can reject at most one label. Indeed, when the remainder is zero modulo \(r^h\), all but one label have exact valuation \(h\). At odd \(h\), the same calculation can leave only that exceptional label.

### Exact \(3,5\) control

Fix \(d=2\). On the \(c\)-axis use the second \(7\)-primary digit \(s\), the first \(3\)-primary digit \(i\), and the first \(5\)-primary digit \(j\). The five rows \(1471,2647,3823,4999,6763\) each read \((s,i)\). Row \(7351\) reads \((s,j)\). The terminal \(8527\) reads \(s\) alone. The orders are checked below.

- **The \(i\) component.** At \(7\), first divisibility selects at most one of the three \(i\)'s. The \(s\)-step changes the offset first at valuation \(2\). If the selected \(i\) has valuation \(1\), discard it and retain two alternatives with no further native loss. Otherwise retain all three, with at most one native deletion in the entire component. The five \((s,i)\) rows therefore empty at most \(\max(\lfloor5/2\rfloor,\lfloor6/3\rfloor)=2\) slices.
- **The \(j\) component.** The inherited row \(11\) leaves at least four of five \(j\)'s for any reading. Row \(7351\) can delete at most one pair \((s,j)\), so it empties no slice.

This proves \(7-2-1=4\), uniformly over the readings at \(7,11\), the six reader primes, and the terminal. To attain the bound, set the \(7\)-reading to discard one \(i\), use four readers to delete both remaining \(i\)'s at two distinct labels, and put the terminal collision at a third label. CRT realizes any choice of those three distinct labels. The pinned target below has old slice counts \((0,0,4,6,8,8,8)\) and terminal slice counts \((0,0,4,6,8,8,0)\).

```python
from itertools import product
from math import isqrt, lcm, prod

q = 8527
R = (1471,2647,3823,4999,6763)
P = R + (7351,q)
def order(p):
    assert p % 4 == 3 and all(p % d for d in range(2,isqrt(p)+1))
    return next(k for k in range(1,p) if pow(3,k,p) == 1)
assert list(map(order,P)) == [294,2646,3822,4998,6762,2450,2842]
assert order(7) == 6 and order(11) == 5

def v(a,p):
    assert a
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k

m = {p:p*p for p in P+(11,)} | {2:4,3:3,7:7**4}
L = lcm(*(a-a//p for p,a in m.items() if p != 3))
def e(p):
    a = p**v(L,p)
    return (L//a)*pow(L//a,-1,a)
A,B,C = map(e,(7,3,5))
def f(p,s=0,i=0,j=0,high=True):
    return 25+pow(3,L+(7 if high else 1)*A*s+B*i+C*j,m[p])
def crt(t):
    M = prod(m[p] for p in t)
    return sum(r*(M//m[p])*pow(M//m[p],-1,m[p])
               for p,r in t.items()) % M
def good(n,p,s=0,i=0,j=0,high=True):
    return v((n-f(p,s,i,j,high)) % m[p],p) % 2 == 0

assert v((f(7,1)-f(7)) % m[7],7) == 2
t = {2:3,3:0,7:f(7)+7,11:f(11,j=4)+11,
     7351:f(7351,s=3)+7351,q:f(q,s=6)+q}
t.update({p:f(p,s,i)+p
          for p,(s,i) in zip(R,((0,1),(0,2),(1,1),(1,2),(2,1)))})
n = crt(t)
def counts(rows):
    return [sum(all(good(n,p,s,i,j) for p in rows)
                for i,j in product(range(3),range(5))) for s in range(7)]
old = (2,3,7,11,7351)+R
assert n == 2308099835306108010159862552653025306194985171803371438703
assert counts(old) == [0,0,4,6,8,8,8]
assert counts(old+(q,)) == [0,0,4,6,8,8,0]

# First 7-primary digit, with i=j=0 and an odd native shell.
z = crt({2:3,3:0,7:f(7,2,high=False)+49,q:f(q,2,high=False)+q})
assert z == 1683507753303
assert [s for s in range(7) if good(z,7,s,high=False)] == [2]
assert not good(z,q,2,high=False)

# The actual terminal is ordinary. Releasing its primary digit repairs z.
E = L//q
assert all(pow(3,E,m[p]) == 1 for p in (2,7))
assert pow(3,E,q) == 1
assert (z-25-pow(3,L+2*A+2406*E,q**3)) % q**3 == 5248*q*q
```

**Scope.** The uniform bound covers the specified chart and rows. At a constructed target, any additional inert primes in a finite prefix can be made units by imposing \(n\equiv25\bmod p\) at those primes. Uniformity over their arbitrary readings would require new capacity bounds. A sufficiently large positive lift of either CRT target puts the displayed offsets below \(n/4\) and preserves the finite tests.

The shallow example is a frozen-chart failure, and its actual terminal repairs when released. The unit-survival proof would also apply to a common-Wieferich terminal with the stated read condition, since it uses no release. A complete finite obstruction requires blocking every legal exponent phase. A positive two-square representation requires controlling every inert prime in a positive remainder. Neither follows from these chart counts. [Finite-obstruction framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Independent BigInt verified all exact reader orders, the high-digit old and terminal counts across the seven slices, both CRT representatives, and the shallow coordinate's ordinary repair. The four-slice lower bound is uniform over the listed target reads, not over arbitrary rows added later.
