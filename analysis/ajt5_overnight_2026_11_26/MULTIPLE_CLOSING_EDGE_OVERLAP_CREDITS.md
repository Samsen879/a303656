# Overlap credits for multiple arithmetic closing edges

A rank-two panel can retain **positive mass for every closing-row target and every frozen terminal target**, even when the separate deletion bounds fail to certify it. In the actual \(3,5\) control below, the open forest has seven cells. The two closing edges can individually delete four and two, but every pair of maximum-size deletions overlaps. Thus at least two cells reach the terminal, and at least one is a terminal unit.

### Counting several closing edges

Vary one digit of the \(3\)-exponent at each of several distinct odd source primes. Fix the \(5\)-exponent and the other relevant coordinates. Suppose each old row reads at most two selected digits, with one exact valuation test per old inert prime.

An edge read by a row at one of its own endpoints can be directed from that endpoint to the other, smaller prime. This follows because the prime-to-\(p\) part of the order modulo \(p^a\) divides \(p-1\). Each source gives at most one such outgoing edge, so these edges form a forest. Extend it to a spanning forest \(T\). All \(k\) closing edges are then read only by rows whose own digits are fixed.

Each such row can reject **at most one endpoint tuple**. Its two digit multipliers modulo the row prime have coprime prime-power orders and are injective on their respective digit ranges. Hence the zero congruence determines at most one tuple. At that tuple, exact valuation parity determines whether to delete it. Greater precision introduces no new prime-to-row-prime reads.

Let \(B_e\) be the set of tuples actually deleted by the rows on closing edge \(e\). Write \(W(P)\) for the open-forest count with partial assignment \(P\) pinned, and set \(W(P)=0\) for inconsistent pins. The exact closed count is
\[
N=\sum_{J\subseteq[k]}(-1)^{|J|}
  \sum_{(b_e)\in\prod_{e\in J}B_e}
  W\!\left(\bigcup_{e\in J}b_e\right).
\]
This takes at most \(\prod_e(1+|B_e|)\) forest passes. Each pass uses ordinary tree messages with the indicated labels pinned. Thus the cost is governed by the closing edges and their forbidden tuples. In particular, a large number of rows on one edge can still make the exact calculation expensive.

For a **uniform lower bound**, let \(U_e\) be the largest possible deletion count on edge \(e\). For two edges, let \(D_e,D_f\) be the counts under a candidate choice of their deletions, and \(I_{ef}\) their exact intersection count. Define
\[
\Delta_{ef}=\min\bigl[(U_e-D_e)+(U_f-D_f)+I_{ef}\bigr],
\]
over the permitted choices on those two edges. For any matching \(\mathcal M\) on the closing edges,
\[
N\ \ge\ W(\varnothing)-\sum_e U_e+\sum_{ef\in\mathcal M}\Delta_{ef}.
\]
Indeed, the deletion union within each matched pair costs \(D_e+D_f-I_{ef}\), and the union across groups costs at most the sum of their costs. In integer counts, \(\Delta_{ef}\ge1\) whenever every pair of maximum-size deletions intersects. Checking this only requires intersections among maximizing choices.

If a terminal \(q\) reads all the selected digits on this axis, its offset modulo \(q\) is injective. It can therefore remove at most one cell, regardless of its fixed primary coordinates or its greater valuation depths. **A lower bound of two on \(N\) suffices even for a genuinely common-Wieferich \(q\)** satisfying \(3^{q-1}\equiv5^{q-1}\equiv1\bmod q^2\). The surviving unit requires no primary-coordinate repair. If \(q\) reads only a subset, the corresponding charge is the open-forest count of its collision fibre, which may exceed one.

### Actual rank-two control

Use binary labels at source primes \(3,5,7,11\) on the \(c\)-axis, with \(d=2\). The open path \(5-7-3-11\) uses rows \(71,7,199\). Row \(31\) closes \(3-5\) and row \(2003\) closes \(7-11\). The terminal \(2311\) has \(\operatorname{ord}_{2311}(3)=2310\) and sees all four digits.

The open count is \(7\). The unique four-cell deletion on the first edge meets each of the three two-cell deletions on the second edge in exactly one cell. Hence the uniform bound is \(7-4-2+1=2\), giving terminal-unit mass at least \(1/16\) on the binary chart. The two additional targets below show that even identical single-edge counts do not determine the joint deletion.

| Exact CRT target | First deletion | Second deletion | Intersection | Old survivors | Frozen terminal survivors |
|---:|---:|---:|---:|---:|---:|
| 7279389990015072453608156343 | 4 | 2 | 1 | 2 | 1 |
| 3672010644034068804197550315 | 2 | 2 | 0 | 3 | 2 |
| 1752745348393472602135105263 | 2 | 2 | 1 | 4 | 3 |

```python
from itertools import product
from math import isqrt, lcm, prod

q = 2311
P = (7, 31, 71, 199, 2003, q)
def order(p):
    assert p % 4 == 3 and all(p % d for d in range(2, isqrt(p)+1))
    return next(k for k in range(1,p) if pow(3,k,p) == 1)
def v(a,p):
    assert a
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k

assert list(map(order,P)) == [6,30,35,198,1001,2310]
m = {p:p*p for p in P} | {2:4, 3:3, 7:343}
L = lcm(*(a-a//p for p,a in m.items() if p != 3))
def step(p):
    a = p**v(L,p)
    return (L//a)*pow(L//a,-1,a)
U = tuple(map(step,(3,5,7,11)))
def f(p,x):
    return 25+pow(3,L+sum(a*b for a,b in zip(U,x)),m[p])

O = (0,0,0,0)
t = {2:3,3:0,7:f(7,O)+49,71:f(71,(0,1,0,0))+71,
     199:f(199,(0,0,0,1))+199}
M = prod(m.values())
D = (0,1)
targets = []
for a,b,z in [((1,0),(1,0),O), ((1,1),(0,0),(1,0,0,1)),
              ((1,1),(1,0),(1,0,0,1))]:
    r = t | {31:f(31,a+(0,0))+31, 2003:f(2003,(0,0)+b)+2003, q:f(q,z)+q}
    n = sum(r[p]*(M//s)*pow(M//s,-1,s) for p,s in m.items()) % M
    targets.append(n)
    def ok(p,x):
        return v((n-f(p,x)) % m[p],p) % 2 == 0
    assert ok(2,O) and ok(3,O)
    assert not ok(31,a+(0,0)) and not ok(2003,(0,0)+b) and not ok(q,z)

    def pin(indices, labels):
        return dict(zip(indices,labels))
    def W(h):
        I,J,K,H = [(h[s],) if s in h else D for s in range(4)]
        return sum(sum(ok(71,(0,j,k,0)) for j in J) *
                   sum(ok(199,(i,0,0,l)) for l in H)
                   for i in I for k in K if ok(7,(i,0,k,0)))
    A,B = (0,1),(2,3)
    X = {x:W(pin(A,x)) for x in product(D,repeat=2)}
    Y = {y:W(pin(B,y)) for y in product(D,repeat=2)}
    assert X == {(0,0):1,(0,1):0,(1,0):4,(1,1):2}
    assert Y == {(0,0):2,(0,1):1,(1,0):2,(1,1):2}
    assert all(W(pin(range(4),(1,0)+y)) == 1 for y in Y if Y[y] == 2)
    both = W(pin(range(4),a+b))
    old = W({})-X[a]-Y[b]+both
    loss = int(W(pin(range(4),z)) and z[:2] != a and z[2:] != b)
    print(n, X[a], Y[b], both, old, old-loss)

# Ordinary repair of the first target's frozen terminal hit.
E = L//q
assert pow(3,2310,q*q) == 1786404
assert pow(3,E,q) == 1
assert all(pow(3,E,m[p]) == 1 for p in (2,7,31,71,199,2003))
assert (targets[0]-25-pow(3,L+11*E,q**3)) % q**3 == 1609*q*q
```

The replay’s terminal is **ordinary**. Its initially blocked cell has valuation one, and the displayed release changes that to exactly two at the same target while preserving the old tests. The common-Wieferich result is the conditional unit-count theorem above. The replay supplies no example of such a prime.

The chart has \(c\) between \(L\) and \(L+\sum U\). A sufficiently large positive lift of a target modulo \(Mq\) puts every displayed offset below a quarter of that target and preserves the reported valuations. The result concerns the specified local chart and panel. It gives neither an ordinary-height certificate at the least CRT representative nor a full two-square representation or a density conclusion.

Independent BigInt directly enumerated all 16 cells for the three exact CRT targets, checked all three maximum-size overlaps, and verified the ordinary lift. The perfect-match-type sum of overlap credits is a sufficient lower bound on a specified local chart, and cannot by itself guarantee that another chart is available or that an integer remainder is a true norm.
