# Conditional endpoint fibres across an arithmetic read cycle

On a single-axis digit cycle, **the closing edge can be charged by its exact conditional fibre sizes**. This gives a sharp criterion for preventing a frozen terminal singleton. An actual \(3,5\) triangle shows why the conditioning matters. At one fixed CRT target, the open path has two survivors, the closing row leaves one, and the frozen terminal kills that one. At another target, the closing row’s forbidden pair has two positive endpoint marginals and an empty joint fibre.

### Cycle criterion

Vary one digit of the \(3\)-exponent at each of several distinct odd source primes. Freeze the \(5\)-exponent and the other relevant coordinates. Suppose each old test reads at most two selected digits, and the graph of two-digit reads is a simple cycle, possibly with trees attached. Use one exact valuation test per old inert prime.

Call an edge native if a test on that edge reads its own prime’s digit. Its other endpoint is a smaller prime, since the prime-to-\(p\) part of an order modulo \(p^k\) divides \(p-1\). Each source has at most one native edge directed toward a smaller source. Native edges therefore form a forest. In particular the cycle has an edge \(xy\) with no native test.

Remove the \(h\) tests on \(xy\). Let \(N_0\) be the open-tree survivor count and \(W(i,j)\) the open-tree count conditional on endpoint labels \(x=i,y=j\). Each removed test can reject at most one pair. Indeed, for its prime \(p\), the two digit multipliers of \(3^c\bmod p\) have coprime prime-power orders, and each is injective on its own digit range. The congruence \(3^c=n-5^d\bmod p\) thus singles out at most one pair. At that pair, use the **actual valuation parity** to decide rejection. Higher \(p\)-adic powers introduce no new prime-to-\(p\) reads, and the test’s own primary coordinate is fixed.

If \(B\) is the union of rejected pairs, the exact count is
\[
N=N_0-\sum_{(i,j)\in B} W(i,j).
\]
A tree count computes \(N_0\), and a tree count with the two endpoints pinned computes each required \(W(i,j)\). This takes at most \(h+1\) tree passes. The candidate pair for a closing row can itself be recovered by powering into the two coprime character factors and testing each digit separately.

The sharp uniform bound over closing-row target residues is \(N_0\) minus the sum of the \(h\) largest \(W(i,j)\), padding with zeros. To attain it, assign one closing prime to each chosen pair and set its target to the offset plus \(p\bmod p^2\). Extra closing rows can take target \(5^d\bmod p\), which makes every remainder a unit there. CRT combines these choices while preserving the other target residues. A cheaper sufficient condition, using the open-tree endpoint marginals \(M_x,M_y\), is
\[
N_0-h\min\{\max_i M_x(i),\max_j M_y(j)\}\ \ge 2.
\]
If the terminal reads all selected digits on this same axis, its offset map modulo the terminal prime is injective by the same coprime-order argument. Two remaining cells then guarantee at least one terminal unit. This is a criterion for the specified chart with its other coordinates fixed.

### Actual triangle and replay

Take \(d=2\), source digits \(3,5,7\) on the \(c\)-axis, and terminal \(q=211\). The active path uses \(7\) on \((3,7)\) and \(71\) on \((5,7)\). The closing test is \(31\) on \((3,5)\). The other pair readers \(43,127\) are present and unit throughout. The control retains every inert prime below \(211\), together with the conditions at \(2\) and \(3\).

| Target construction | Open path | Closed old panel | Frozen terminal |
|---|---:|---:|---:|
| Closing test hits \((0,2)\) | 2 | 1 | 0 |
| Closing test hits \((1,2)\) | 2 | 2 | 1 |
| Restore one unary label, close at \((0,2)\) | 3 | 2 | 1 |
| Restore a different unary label, close at \((0,1)\) | 22 | 22 | 21 |

In the third row the largest endpoint-fibre bound is \(1\), so **every** closing residue leaves at least two cells. In the fourth row the endpoint marginals at the forbidden pair are \(2\) and \(6\), but its exact joint count is zero. Each row uses one target across the full panel.

```python
from math import isqrt, lcm, prod

def prime(p):
    return all(p % d for d in range(2, isqrt(p) + 1))

def v(a, p):
    assert a
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k

q = 211
P = [p for p in range(7, q, 4) if prime(p)]
def order(p):
    return next(k for k in range(1, p) if pow(3, k, p) == 1)

def reads(p):
    return {r for r in (3, 5, 7) if order(p) % r == 0} | (
        {7} if p == 7 else set())

assert [(p, sorted(reads(p))) for p in P if len(reads(p)) > 1] == [
    (7,[3,7]), (31,[3,5]), (43,[3,7]), (71,[5,7]), (127,[3,7])]
assert prime(q) and order(q) == 210 and pow(3,210,q*q) == 3799

m = {p:p for p in P}
m.update({2:4, 3:3, 7:343, **{p:p*p for p in (11,19,31,71,79,131,q)}})
L = lcm(*(a-a//p for p,a in m.items() if p != 3))
def step(p):
    a = p**v(L,p)
    return (L//a)*pow(L//a,-1,a)

u,w,z = map(step,(3,5,7))
def f(p,i=0,j=0,k=0):
    return 25 + pow(3,L+i*u+j*w+k*z,m[p])

t = {p:25 for p in m}
t.update({2:3, 3:0, 7:f(7)+49, 11:f(11,0,3)+11,
          19:f(19,1)+19, 79:f(79,2)+79, 131:f(131,0,4)+131,
          71:f(71,0,1)+71, 31:f(31,0,2)+31, q:f(q)+q})
M = prod(m.values())
def crt(t):
    return sum(t[p]*(M//a)*pow(M//a,-1,a) for p,a in m.items()) % M

cases = [(t,(0,2)), (t|{31:f(31,1,2)+31},(1,2)),
         (t|{131:25},(0,2)), (t|{79:25,31:f(31,0,1)+31},(0,1))]
out = []
for residues,(i,j) in cases:
    n = crt(residues)
    def ok(p,a=0,b=0,k=0):
        return v((n-f(p,a,b,k)) % m[p],p) % 2 == 0
    assert ok(2) and ok(3) and not ok(31,i,j) and not ok(q)
    A = [[ok(19,a) and ok(79,a) and ok(7,a,0,k)
          for k in range(7)] for a in range(3)]
    B = [[ok(11,0,b) and ok(131,0,b) and ok(71,0,b,k)
          for k in range(7)] for b in range(5)]
    left, right = [list(map(sum,zip(*T))) for T in (A,B)]
    opened = sum(a*b for a,b in zip(left,right))
    loss = sum(a and b for a,b in zip(A[i],B[j]))
    closed = opened-loss
    out.append((opened,closed,closed-int(A[0][0] and B[0][0] and ok(31))))
assert out == [(2,1,0),(2,2,1),(3,2,1),(22,22,21)]
assert (sum(a*b for a,b in zip(A[0],right)),
        sum(a*b for a,b in zip(B[1],left)),loss) == (2,6,0)

# Release the ordinary 211-primary coordinate at the first target.
D = L//q
assert all(pow(3,D,a) == 1 for p,a in m.items() if p not in (3,q))
assert pow(3,D,q) == 1
assert (crt(t)-25-pow(3,L+83*D,q**3)) % q**3 == 90*q*q
print(out)
```

The first target’s least CRT representative is \(309556147383103172525882060462209726124806009458268994834787\). A sufficiently large positive lift of this representative modulo \(Mq\) makes every displayed remainder positive and preserves the reported valuations. The construction gives no ordinary-height guarantee for the least representative.

**The ordinary terminal repairs.** At the first target the frozen survivor has \(v_{211}=1\), but changing \(c\) from \(L\) to \(L+83D\) gives \(v_{211}=2\) and preserves the old panel. In general, releasing an ordinary terminal’s primary coordinate gives the matching cell an even-valuation fraction \(1/(q+1)\). At a genuinely common-Wieferich terminal, releasing either primary coordinate leaves the offset fixed modulo \(q^2\). A depth-one odd shell can therefore persist. The example establishes the closing-edge obstruction on a frozen chart and its ordinary repair. A complete finite obstruction would still require blocking every other legal chart, and panel survival alone gives no two-square certificate. [Finite-obstruction framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Independent BigInt replay enumerated each full chart directly, rather than using the proposed tree aggregation, and verified 2→1→0, 2→2→1, 3→2→1, and 22→22→21. The empty joint fibre with positive endpoint marginals and the ordinary terminal lift were also checked. This is local to the specified charts, not a global obstruction.
