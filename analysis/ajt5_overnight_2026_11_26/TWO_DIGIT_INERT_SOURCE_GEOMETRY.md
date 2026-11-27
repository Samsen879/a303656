# Deterministic two-digit survival with one inert unit source

**An inert-unit source can be included in the deterministic two-digit bound.** Its own norm test costs at most one choice on its native digit at even lifting depth, or at most one column when it reads the other digit. The first rule gives an actual \(3,5\) panel where both one-digit counts are inconclusive and the two-digit count guarantees survival. The second applies to the full chronological panel before \(q=600311\).

### Deterministic rule

Move two primary digits of the **same** base \(g\in\{3,5\}\). Their sizes are distinct odd primes \(r,s\), and the selected depths correspond to \(r^a,s^b\mid\operatorname{ord}_q(g)\). Assume \(r\) is inert with \(g\) a unit there, and the source at \(s\) imposes no digit constraint, as when \(s\) is split or \(s=g\) is nonunit.

Set aside the source row at \(r\). Among the other old rows, let \(A,B,C\) count those reading just the \(r\)-digit, just the \(s\)-digit, or both. The source row at \(r\) has either of the following deterministic charges.

- **Even native depth.** If \(s^b\nmid\operatorname{ord}_r(g)\) and \(h=a-1+v_r(g^{r-1}-1)\) is even, charge \((\epsilon_r,\epsilon_s)=(1,0)\). Within a grid, the source remainder mod \(r^h\) is fixed as the native digit varies. An odd valuation below \(h\) rejects the entire grid, and an even valuation below \(h\) accepts it. In the matching class, LTE gives distinct next digits for the \(r\) choices, so at least \(r-1\) have exact even valuation \(h\). The auxiliary digit preserves these readings. [Earlier even-depth reset arithmetic](https://github.com/Samsen879/a303656/blob/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)
- **Cross-read at the source.** If \(s^b\mid\operatorname{ord}_r(g)\), charge \((0,1)\), at any native depth. The native digit is invisible mod \(r\), while the \(s\) choices give distinct shifts mod \(r\). Discard the one column that can match \(n_r\bmod r\). Every other column passes the source row with a unit remainder.

Set
\[
N=(r-A-\epsilon_r)_+(s-B-\epsilon_s)_+-C.
\]
If \(N\ge2\), a positive old head stays positive at \(q\), with
\[
\frac{\alpha_q}{\alpha_{q^-}}\ge 1-\frac1N,
\]
where \(\alpha\) is the unnormalized phase mass.

To prove this, fix all coordinates other than the selected digits. Nonreaders preserve the grid. After the source charge, each exclusive row can remove at most one choice on its side, since its shift is injective along the digit it reads. Each shared row can remove at most one cell, since both primary components belong to the order of the same base. This gives at least \(N\) old survivors on every grid that can contribute. The terminal shift is injective on the entire grid, so the terminal read rejects at most one old survivor per grid. Integrating gives the mass ratio. The argument is pointwise in the target readings and works at every terminal lifting depth.

### Actual order patterns

| Terminal and moved base | Source rule | Other old readers | Guaranteed cells before terminal |
|---|---|---:|---:|
| \(991,\ g=5,\ r^a=9,\ s^b=5\) | Even native depth \(h=2\) at 3 | \(A=0,\ B=3,\ C=1\), specified finite panel | \(3\) |
| \(600311,\ g=3,\ r=347,\ s=173\) | The source 347 reads the 173-digit | \(A=74,\ B=136,\ C=1\), full old panel | \(9827\) |

In the first panel, the old rows besides 3 are \(11,71,131,811\). Their orders of 5 are \(5,5,65,405\), and the terminal order is \(495\). Each one-digit count guarantees only one old choice. The grid guarantees three, so two survive the terminal read. The replay attains both counts. At the **same target**, moving the shallow \(3\)-digit instead gives source valuations \((2,1,1)\). This checks why even depth matters when the source cannot read the auxiliary digit.

In the full panel before \(600311\), the only shared reader is \(360187\). The resulting local survival ratio is at least \(9826/9827\) on every positive old head. These are finite local certificates. A positive two-square remainder remains a separate question.

### Standalone replay

```python
from math import lcm, prod, isqrt

def prime(p):
    return p > 1 and all(p % i for i in range(2, isqrt(p) + 1))

def copart(n, p):
    while n % p == 0:
        n //= p
    return n

def val(t, p):
    assert t
    a = 0
    while t % p == 0:
        a, t = a+1, t//p
    return a

P = (11, 71, 131, 811, 991)
assert all(prime(p) and p%4 == 3 for p in P)
assert [next(i for i in range(1,p) if pow(5,i,p)==1) for p in P] == [5,5,65,405,495]
L = lcm(54, *(p*(p-1) for p in P))
U, V = copart(L,3), copart(L,5)

def f(i,j,m,k=3):
    return (81 + pow(5,2+k*U*i+V*j,m)) % m

data = [(4,3), (81,f(2,0,81)+27)]
data += [(p*p,f(i,j,p*p)+p)
         for p,i,j in [(11,0,2),(71,0,3),(131,0,4),(811,0,0),(991,0,1)]]
M = prod(m for m,t in data)
n = sum(t*(M//m)*pow(M//m,-1,m) for m,t in data) % M
old = [(i,j) for i in range(3) for j in range(5)
       if val((n-f(i,j,81))%81,3)%2==0
       and all(val((n-f(i,j,p*p))%(p*p),p)==0 for p in P[:-1])]
assert old == [(0,1),(1,0),(1,1)]
assert [ij for ij in old if (n-f(*ij,991))%991] == [(1,0),(1,1)]
assert val((n-f(0,1,991**2))%(991**2),991) == 1
assert [val((n-f(i,0,81,k=1))%81,3) for i in range(3)] == [2,1,1]

q,r,s = 600311,347,173
assert all(prime(p) for p in (q,r,s)) and (q%4,r%4,s%4)==(3,3,1)
reads = lambda p,d: (p-1)%d==0 and pow(3,copart(p-1,d),p)!=1
assert reads(r,s) and reads(q,r) and reads(q,s)
R = {p for p in range(2*r+1,q,4*r) if prime(p) and reads(p,r)}
S = {p for p in range(2*s+1,q,4*s) if p!=r and prime(p) and reads(p,s)}
assert (len(R-S),len(S-R),R&S) == (74,136,{360187})
assert (r-74)*(s-136-1)-1 == 9827
```

The replay passed. The exclusion is deterministic for the stated reader patterns, including a terminal whose own lifting gives no escape. Coverage of all order patterns remains open.

Independent BigInt CRT replay reproduced the old three and final two cells and the shallower source valuation control. A separate sieve scan of all prior inert primes confirmed 74 native-only, 136 auxiliary-only, and one shared row in the full 600311 panel. The 9826/9827 ratio bounds a local phase step, not the probability of a genuine two-square representation.
