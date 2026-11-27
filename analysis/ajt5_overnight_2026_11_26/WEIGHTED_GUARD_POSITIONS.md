# Weighted guard positions through multiple nonlinear projections

**Distinct guard positions can be charged through successive nonlinear pivots. The invariant must retain sets of positions until the pivots are eliminated.** A scalar charge based only on individual guard masses can fail even on a \(2\times2\) lower window, with half the phases still escaping. [Seventeen-prime starting point](https://github.com/Samsen879/a303656/commit/eb8c39342b2b4c6f84ccd3dc2dacb50c81cc39d1)

### The weighted invariant

Fix \(n,c\) and the parity of \(d\). Let \(W\) be a retained lower phase window with normalized measure \(\mu\). Give each distinct fixed guard position \(P_i\subseteq W\) one label. A least-helper guard that also reads an eliminated coordinate keeps that restriction in the corresponding fibre. Two helpers with the same position on \(W\) share a label even if they read different higher digits.

At a higher phase, represent the forbidden event by a family of finite label sets. A set \(S\) witnesses the event when **all** positions in \(S\) are active. The rules are exact for an exact input ledger and give an upper bound for an input overcover.

- Alternatives take the union of their families.
- To eliminate a coordinate, choose a witness set from **each** fibre and take their set union.
- Discard any set containing another witness set. An empty family means failure to cover. A family containing the empty set means unconditional coverage.

The second rule is distributivity applied to “every fibre has a witness.” It works at each nonlinear pivot. Set union counts a shared position once, even when several fibres require it.

For the resulting minimal witness family \(\mathcal F\), any weights satisfying
\[
w_i\ge0,\qquad \sum_{i\in S}w_i\ge1\quad(S\in\mathcal F)
\]
give
\[
\mu(\text{unavoidable phases})\ \le\ \sum_i w_i\mu(P_i).
\]
Indeed, at every unavoidable phase the active labels contain a witness, so their weight is at least one. A charge below one certifies an escape. This is a finite linear program once the witness sets are known. The family can grow exponentially, and the criterion can lose information when it replaces joint positions by their marginal masses.

### Actual mixed orders at 7 and 11

The named prime \(463\) has \(\operatorname{ord}_{463}(5)=462=2\cdot3\cdot7\cdot11\) and \(5^{462}\equiv17595\pmod{463^2}\). It is an ordinary inert helper whose actual order guard reads **both** pivot coordinates.

At the represented target
\[
n=35974890041509937764240647419591826365,\qquad c=1,\quad d\ \text{even},
\]
write \(x,y,z,t\) for \(d\bmod3,5,7,11\). At square precision, row 7 rejects exactly \(x=2,\ z\ne2\), and row 11 rejects exactly \(y=4,\ t\ne0\). Charge row 463’s whole actual order guard \(x=2,\ z=2,\ t=0\) as an overcover. Writing \(A=[x=2]\) and \(B=[y=4]\), elimination at 11 followed by 7 gives the sole witness \(\{A,B\}\). Its exact overcover mass is \(1/15\), while the best individual-position charge is \(1/5\).

A second represented CRT target preserves both square-precision rows and shifts the actual 463 guard from \(t=0\) to \(t=1\). Then the cell \(z=2,t=0\) is uncovered for every lower phase. The two cases have identical lower positions and marginals. The difference lies in the higher digit. The inline replay also checks \(d=621434\) at the first target, where the three genuine rows all have zero residue at square precision. Thus the charged guard at 463 is genuinely an overcover of its arithmetic row.

### Sharp synthetic limit

On an equally weighted \(2\times2\) lower window, set \(A=[x=0]\), \(C=[x=1]\), \(B=[y=0]\), and \(D=[y=1]\). At the seven rank-7 branches, use the clauses \(A\vee C,\ A\vee D,\ B\vee C,\ B\vee D\), repeating clauses to fill the seven branches. Install each clause separately at all eleven rank-11 digits. These are **synthetic rigid supports**. Both projections require full fibres, and the final minimal witnesses are \(\{A,B\}\) and \(\{C,D\}\).

Each position has mass \(1/2\). The two witness inequalities force total additive charge at least one, and this is attained. Yet only the two diagonal cells are covered. Both witnesses are feasible, so pruning infeasible witnesses does not help. Charging the two **joint** positions instead gives the exact mass \(1/2\). This identifies where the marginal-only policy loses the escape.

### Inline replay

```python
from itertools import product
from math import isqrt, prod

def meet(families):
    out = {frozenset()}
    for family in families:
        unions = {a | b for a in out for b in family}
        out = {s for s in unions if not any(t < s for t in unions)}
    return out

def project(cell):
    return meet(meet(cell(z,t) for t in range(11)) for z in range(7))

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

q = 463
assert all(q % j for j in range(2,isqrt(q)+1))
assert pow(5,462,q) == 1 and pow(5,462,q*q) == 17595
assert all(pow(5,462//p,q) != 1 for p in (2,3,7,11))

M = 8*3*49*31*71*5167*19531
for a,b,k in ((2,168,0),(1,30,1)):
    u = crt([(3,M),(2,121),(a,q)])
    v = crt([(8,M),(2,121),(b,q)])
    n = 4+u*u+v*v
    if k==0:
        assert n==35974890041509937764240647419591826365
        assert all((n-3-pow(5,621434,p*p))%(p*p)==0 for p in (7,11,q))
    for x,y,z,t in product(range(3),range(5),range(7),range(11)):
        d = crt([(0,2),(x,3),(y,5),(z,7),(t,11)])
        for p,expected in ((7,x==2 and z!=2),(11,y==4 and t!=0)):
            r = (n-3-pow(5,d,p*p)) % (p*p)
            assert (r != 0 and r%p == 0) == expected
        assert ((n-3-pow(5,d,q))%q == 0) == ((x,z,t) == (2,2,k))

    def cell(z,t):
        return {frozenset(label) for label,live in
                [('A',z!=2 or t==k),('B',t!=0)] if live}

    assert project(cell) == ({frozenset('AB')} if k == 0 else set())

# Synthetic two-pivot ledger on a 2x2 lower window.
clauses = ('AC','AD','BC','BD')
S = project(lambda z,t: {frozenset(i) for i in clauses[z%4]})
assert S == {frozenset('AB'),frozenset('CD')}
active = [frozenset(x+y) for x,y in product('AC','BD')]
assert [any(s <= a for s in S) for a in active] == [True,False,False,True]
assert all(sum(i in a for a in active) == 2 for i in 'ABCD')
assert sum(sum(s <= a for a in active) for s in S) == 2
print("PASS")
```

The lower-position labels denote subsets of one fixed lower phase space. Any dependence on a pivot variable remains in the relevant fibre, rather than being absorbed into an independent lower label. The projection rules give exact forbidden sets when starting from exact local events; taking an input overcover preserves only the stated upper containment. The replay's mixed-order example demonstrates both the soundness and the possible strictness of that containment.
