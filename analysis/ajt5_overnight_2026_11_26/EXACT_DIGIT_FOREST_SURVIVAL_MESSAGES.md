# Exact old and terminal phase mass on a forest of digit reads

**A tree-shaped read graph gives an exact count of the old surviving phases, including branches where odd-depth source pins propagate.** On a same-exponent digit grid, the terminal read can reject at most one of those phases. The count therefore gives both a deterministic exclusion test and the exact mass retained by the terminal.

The full old panel before \(q=10039\) has an actual \(3\to7\to239\) source chain for base 5. The replay below gives a target where the pins propagate to a singleton and the frozen terminal rejects it. Two other readings retain \(1194\) and \(1195\) of \(1195\) old phases, respectively.

### The arithmetic tree rule

Fix the exponent coordinates outside the selected digits. At each source prime \(p\), select digit \(a_p-1\) of the moved exponent’s \(p\)-primary coordinate. Assume the moved base is a unit and ordinary at \(p\). Form the old read graph by joining two digits whenever an old row reads both. The criterion applies when every old row reads at most two selected digits and this graph is a forest. Multiple rows on one edge are allowed.

At an ordinary source with one lower parent, the first-residue shift is injective in the parent digit and independent of the native digit. Thus all but at most one parent label give a unit remainder for **every** native choice. At the exceptional parent label, LTE gives the exact native rule:

- A fixed valuation below \(a_p\) gives the same parity test for every native choice.
- If the reading matches through depth \(a_p\), all but one native choice have exact valuation \(a_p\). Test the exceptional choice at its actual deeper valuation.

In particular, on an odd-depth matched branch there is at most one surviving native digit. Its value must be passed to the next source along the tree. [Local norm support and prime-power lifting](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Combine exact unary tests into \(U_v(t)\in\{0,1\}\), and combine all tests on an edge into \(\Phi_{uv}(s,t)\in\{0,1\}\). Root each tree and compute
\[
W_v(t)=U_v(t)\prod_{w\ {\rm child\ of}\ v} M_{w\to v}(t),
\qquad
M_{v\to u}(s)=\sum_t\Phi_{uv}(s,t)W_v(t).
\]
At each root sum \(W_v(t)\) over its digit choices, and multiply over components to get the exact old count \(N\). Each message counts the assignments in its subtree with the separating digit fixed, so the proof is induction from the leaves. On a source-only edge, the message is a single total at all nonexceptional parent labels. Only the exceptional label needs a restricted sum. This is where the arithmetic saves work beyond a general table computation.

At \(q\), the shift is injective on the grid because the selected prime-power order factors are coprime and belong to the same exponent. Thus:

- **With the \(q\)-primary coordinate frozen**, the new count is \(N-\delta\), where \(\delta=1\) exactly when the unique candidate matching \(n_q\bmod q\) passes the old rows and has odd terminal valuation. This preserves the entire old mass when the matching candidate passes the exact terminal test.
- **With an ordinary \(q\)-primary coordinate released**, the matching old tuple, if present, retains fraction \(1/(q+1)\). Older rows leave this coordinate unread, and LTE makes its remainder uniform in \(q\mathbb Z_q\). The new mass in grid-cell units is therefore \(N-q/(q+1)\) if the candidate is present, and \(N\) otherwise.

In particular, \(N\ge2\) excludes a frozen terminal zero, regardless of terminal lifting depth. These formulas apply fibre by fibre and can be integrated over the frozen coordinates.

### Actual chain and dependence control

For base 5 and \(q=10039\), use the first digits at \(3,7,239\). Their product is \(\operatorname{ord}_q(5)=5019\). The orders at 7 and 239 are 6 and 119, respectively, giving the directed chain. The full old panel has no edge from 3 to 239 and no triple read. Rows 43 and 3347 impose additional exact tests on the two existing edges.

The replay constructs each target as a single integer by CRT, with the whole chronological old panel included.

| Reading change | Old cells | Frozen terminal survivors |
|---|---:|---:|
| Both downstream sources read the propagated pin | 1 | 0 |
| Change only the reading at 7 to a unit reading | 1195 | 1194 |
| From that reading, change the terminal lift to exact valuation 2 at the anchor | 1195 | 1195 |

At the first target, the upper source 239 has a unit remainder on a different 7-digit. The old pin at 7 excludes that digit. This gives a same-target dependence countercontrol to multiplying the marginal choices. Releasing the ordinary terminal coordinate in the first case retains \(1/10040\) of the singleton’s old mass.

```python
from math import isqrt, lcm, prod

q, R = 10039, (3, 7, 239)
def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))
def v(n,p):
    assert n
    e = 0
    while n%p == 0: n,e = n//p,e+1
    return e
def reads(p,r):
    return (p-1)%r==0 and pow(5,(p-1)//r**v(p-1,r),p)!=1

P = [p for p in range(3,q,4) if prime(p)]
assert prime(q) and all(p in P for p in (*R,43,3347))
assert all(pow(5,p-1,p*p)!=1 for p in (*R,q))
assert pow(5,5019,q)==1 and all(pow(5,5019//r,q)!=1 for r in R)
scope = lambda p: {r for r in R if p==r or reads(p,r)}
assert scope(3)=={3} and scope(7)==scope(43)=={3,7}
assert scope(239)==scope(3347)=={7,239}
assert all(scope(p)<={3,7} or scope(p)<={7,239} for p in P)

m = {p:p for p in P}
m.update({2:4,3:27,7:343,239:239**3,43:43**2,3347:3347**2,q:q**3})
period = {p:a-a//p for p,a in m.items()}
L = lcm(*period.values())
def step(r):
    d = r**v(L,r)
    return (L//d)*pow(L//d,-1,d)
U = [step(r) for r in R]
def f(p,i=0,j=0,k=0):
    e = (L+i*U[0]+j*U[1]+k*U[2])%period[p]
    return (81+pow(5,e,m[p]))%m[p]

t = {p:81 for p in m}  # Every unmarked inert row has a unit remainder.
t[2] = 3
for p in R: t[p] = f(p)+p*p
t[43], t[3347], t[q] = f(43,0,2)+43, f(3347,0,1,1)+3347, f(q)+q
M = prod(m.values())
coef = {p:(M//a)*pow(M//a,-1,a) for p,a in m.items()}
def crt(): return sum(t[p]*a for p,a in coef.items())%M

def counts(n):
    def good(p,*x): return v((n-f(p,*x))%m[p],p)%2==0
    C = [sum(good(239,0,j,k) and good(3347,0,j,k) for k in range(239))
         for j in range(7)]
    N = sum(C[j] for i in range(3) for j in range(7)
            if good(3,i) and good(7,i,j) and good(43,i,j))
    loss = all(good(p) for p in (3,7,239,43,3347)) and not good(q)
    return N,N-loss

n = crt()
assert (n-f(7,1,0))%7 and (n-f(239,0,1))%239
assert counts(n)==(1,0)
t[7]=81
assert counts(crt())==(1195,1194)
t[q]=f(q)+q*q
assert counts(crt())==(1195,1195)
```

The replay passed. The singleton failure is a finite local obstruction with the terminal coordinate frozen. Computing a positive two-square remainder is a separate step.

Independent BigInt replay checked the entire old scope forest and all three CRT targets, including the 1→0 frozen singleton and the 1195→1195 no-loss terminal lift. The ordinary released-coordinate calculation refers to local Haar phase mass only.
