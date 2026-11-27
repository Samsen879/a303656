# Private order digits and actual locked collision circuits

**Private order digits give an exact acyclic elimination rule. Shared orders can give a genuine circuit.** The known \(19,271\) rows admit the elimination. Three known depth-four rows give a stronger locked example: after anchoring \(d\bmod54\), their actual collision classes exhaust the three remaining branches. Ordinary prime-power lifting still repairs that example. [Pinned one-row criterion](https://github.com/Samsen879/a303656/commit/9657b2d24f1eb5b015af584bc6e405cb9785dc8a)

### Exact graph condition

Fix \(c\) and an anchor \(d=d_0+At\), including parity and any phases that must stay frozen. A zero row with true order \(b_i=\operatorname{ord}_{q_i}(5)\) forbids a collision class \(d\equiv a_i\bmod b_i\). Discard rows incompatible with the anchor. Each remaining row forbids one class in \(t\) of period
\[
m_i=b_i/\gcd(A,b_i).
\]

For a set \(S\) of remaining rows, row \(i\) can be deleted and **restored over every phase of the other rows** exactly when
\[
m_i\nmid\operatorname{lcm}_{j\in S\setminus\{i\}}m_j.
\]
In that case the other phases leave at least two choices modulo \(m_i\), so one avoids its collision. Equivalently, \(i\) has a prime-power digit strictly deeper than every competitor’s on that coordinate.

Choose a witnessing prime \(\ell_i\) for each row and draw \(j\to i\) whenever \(j\ne i\) and \(v_{\ell_i}(m_j)\ge v_{\ell_i}(m_i)\). **A full deletion order exists exactly when a choice of witnesses makes this graph acyclic.** Delete in topological order and restore in reverse. Equivalently, every nonempty subset must have a private digit. Testing a joint lcm matters because different rows can supply different factors of the same order.

This graph tests phase-preserving deletion one row at a time. A locked row can still be redundant if its collision class is already covered by the other forbidden classes. A true collision obstruction on the anchor requires the union of the actual classes to cover it. The numerical order DAG from reader primes to factors of their orders can remain acyclic while these row-to-row dependencies cycle.

### Two actual controls

- **Removable.** At \(c=15\), the \(19,271\) collision classes are \(6\bmod9\) and \(0\bmod27\). On \(d\equiv0\bmod6\) the effective periods are 3 and 9. Delete \(271\) first. When restoring it, changing \(d=0\) to \(18\) preserves the \(19\)-phase and clears the \(271\) collision.
- **Locked.** The known primes \(1783,5023,Q\), with \(Q=11419697846380955982026777206637491\), have true orders \(162,162,81\). The replay fixes one odd \(c\) for which their collision branches on \(d=54t\) are \(t\equiv0,2,1\bmod3\), respectively. All effective periods are 3, and each class is needed for the cover. [Known cyclotomic primes](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md#3-exact-selected-cyclotomic-arithmetic)

The locked control also rejects at exact valuation one throughout the stronger anchor \(d\equiv0\bmod54(1783)(5023)Q\). Releasing the reader-primary digits while keeping \(d\equiv0\bmod54\) allows a lift to exact valuation two at \(1783\), with the other two residuals units. So the unavoidable collision cover is confined to its phase scope. It is not a whole finite norm obstruction, and these are ordinary controls.

### Runnable replay

```python
from math import gcd, isqrt, lcm, prod

def peel(orders, anchor):
    left, out = set(orders), []
    while left:
        q = next((q for q in sorted(left)
                  if lcm(anchor, *(orders[r] for r in left-{q})) % orders[q]),
                 None)
        if q is None:
            break
        left.remove(q)
        out.append(q)
    return out, left

p,t = 19,271
assert pow(5,9,p)==1 and pow(5,3,p)!=1
assert pow(5,27,t)==1 and pow(5,9,t)!=1
assert pow(-3,15,p)==pow(5,6,p)!=1 and pow(-3,15,t)==1
assert peel({p:9,t:27},6)==([t,p],set())
n0 = 21*p*t
assert n0%24==9 and (n0-pow(3,15,t)-1)%t==0
assert pow(5,18,p)==1
assert all((n0-pow(3,15,q)-pow(5,18,q))%q for q in (p,t))

q0,q1,Q = 1783,5023,11419697846380955982026777206637491
# One-factor Pocklington certificates for the large known prime.
chain = [1838773,871578403,1770336106919153,584210915283320491,
         143715885159696840787,Q]
for q in (p,t,q0,q1,chain[0]):
    assert all(q%i for i in range(2,isqrt(q)+1))
for f,q in zip(chain,chain[1:]):
    assert f*f>q and (q-1)%f==0
    assert pow(2,q-1,q)==1 and gcd(pow(2,(q-1)//f,q)-1,q)==1

rows = (q0,q1,Q)
O = dict(zip(rows,(162,162,81)))
for q,b in O.items():
    assert q%4==3 and pow(5,b,q)==1
    assert all(pow(5,b//ell,q)!=1 for ell in (2,3) if b%ell==0)

P = prod(rows)
c = 27*lcm(11,31,70491962014697259148313439547145)*P
A = 54*P
assert c%2 and peel(O,A)==([],set(rows))
assert {q:[j for j in range(3) if (pow(3,c,q)+pow(5,A*j,q))%q==0]
        for q in rows} == {q0:[0],q1:[2],Q:[1]}

pairs = [(9,24)] + [(q,q*q) for q in rows]
M = prod(m for _,m in pairs)
n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M

def rem(d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

for q,j in zip(rows,(0,2,1)):
    assert rem(A*j,q*q)==q and pow(5,3*A,q*q)==1
    assert all(rem(A*j,r) for r in rows if r!=q)

u = (pow(5,162,q0*q0)-1)//q0
assert u%q0
d = 162*pow(u,-1,q0)
assert rem(d,q0*q0)==0
if rem(d,q0**3)==0:
    d+=162*q0
assert rem(d,q0**3) in range(q0*q0,q0**3,q0*q0)
assert d%54==0 and all(rem(d,r) for r in (q1,Q))
assert rem(d,4)==1 and rem(d,3)!=0
```

The deletion statement is about restoring row i over every *period phase* of the other rows, with the anchor kept, not a claim that every phase passing the other rows must exhibit a lock. An edge j→i requires j to be deleted earlier, so the constructive orientation is precisely the stated topological order. A failed peeling condition does not itself establish collision coverage or norm obstruction; the actual computations here distinguish all three.
