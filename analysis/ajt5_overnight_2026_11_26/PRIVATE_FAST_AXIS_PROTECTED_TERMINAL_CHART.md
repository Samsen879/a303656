# Axis-specific ordinary repairs preserve a full terminal chart

**All 2,401 phases of a legal unit-at-\(7\) chart can be made available while preserving a terminal that reads an upstream repair prime.** In the explicit example below, the terminal \(q=18{,}571{,}099\) reads the \(43\)-digit on base 5 only. Repairing \(43\) on base 3 preserves the terminal readings throughout the chart. On the same target, a valid base-5 repair at the corner turns a terminal unit into an exact valuation-one failure.

### Deterministic repair with protected readings

Protect the two power residues individually at each retained modulus and at the terminal modulus. For an ordinary row \(p>23\), define
\[
e_b=v_p(b^{p-1}-1),\qquad
L_b=\max_m v_p(\operatorname{ord}_m(b)),\qquad
\rho=\min(3,e_3+L_3,e_5+L_5),
\]
where \(m\) runs over protected moduli and an empty maximum is zero. Hold all non-\(p\) exponent coordinates fixed. A permitted change on axis \(b\) must be divisible by \(p^{L_b}\) in its \(p\)-primary coordinate. By LTE, the attainable changes of its power modulo \(p^3\) fill exactly the subgroup of multiples of \(p^{\min(3,e_b+L_b)}\). Hence the attainable changes of the sum fill exactly the multiples of \(p^\rho\).

In particular, a valuation-one failure can be repaired by this method **exactly when a fast axis is invisible to every protected reading at its first \(p\)-digit**, meaning \(\rho=1\). If the remainder is zero modulo \(p^3\), \(\rho\le2\) suffices to give exact valuation two. These are criteria for preserving the two residues separately.

For a full chart, apply the \(\rho=1\) test to every row designated for repair, then repair in increasing prime order. A \(p\)-primary edit preserves every smaller row’s reading modulo its cube, since the smaller row’s order has no factor \(p\). It also preserves the head, both \(7\)-digits, and every protected reading. **Each cell keeps its own terminal reading.**

If a row lacks a private fast axis, one can park it and add its cube reading to the protected set. Inspecting rows in decreasing order makes this a single pass, since parking a smaller row cannot constrain an already selected larger repair prime. The full chart is available if every parked row passes on every provisional cell. This replaces whole-output isolation by an axis-by-axis test. [Earlier output-isolated repair rule](https://github.com/Samsen879/a303656/commit/2e2c5d54904e266ee271fb9ea237dcd12cc86780)

### Same-target availability and failure

Use the legal head \((2,3)\bmod3960\), retain the two readings modulo \(31^3\), and protect the terminal readings modulo \(q^2\). The terminal has
\[
q-1=2\cdot3\cdot49\cdot13\cdot43\cdot113,\qquad
(\operatorname{ord}_q(3),\operatorname{ord}_q(5))=(431886,9285549).
\]
Both axes read the two free \(7\)-digits. Among earlier inert primes above 23, only \(43\) divides a terminal order. It divides only the base-5 order. The replay verifies that **all 592,895 inert primes between 23 and \(q\) are ordinary**. The increasing-order rule therefore extends every cell through the entire earlier inert prefix.

At the displayed integer target, 49 raw cells need repair at \(43\), and none has a terminal hit. The safe repair preserves all 2,401 distinct terminal shifts. At the same corner and target, the unsafe repair gives the following exact valuations.

| Corner operation | \(v_{43}(n-3^c-5^d)\) | \(v_q(n-3^c-5^d)\) |
|---|---:|---:|
| Before repair | 1 | 0 |
| Repair on base 3 | 2 | 0 |
| Repair on base 5 | 2 | 1 |

A base-5-only move preserving the terminal reading must keep the first \(43\)-digit, so it cannot clear this valuation-one failure. Subsequent ordinary repairs at larger inert primes cannot undo the terminal change. This is an ordinary finite comparator. For a genuine common-Wieferich terminal, the availability proof applies when its protected periods and upstream rows pass the stated tests. The capacity bound can then be applied to the available chart.

```python
from math import isqrt, lcm

n, p, q = 2320523495091138236199490729443, 43, 18571099
K = lcm(3960, 31**2, (q-1)//49, q)
H = lcm(3960, 31**2, 49, q*(q-1)//43)

def S(c,d,m):
    return (pow(3,c,m) + pow(5,d,m)) % m

assert q%4==3 and all(q%i for i in range(2,isqrt(q)+1))
assert q-1 == 2*3*49*13*43*113 and 113%4==1
assert K%7 and H%49==0 and H%43
for b,d in ((3,431886),(5,9285549)):
    assert (q-1)%d==0 and d%49==0 and d%343
    assert pow(b,d,q)==1
    assert all(pow(b,d//t,q)!=1
               for t in (2,3,7,13,43,113) if d%t==0)
    assert pow(b,q-1,q*q)!=1 and pow(b,p-1,p*p)!=1
assert pow(3,H,q*q)==1
assert pow(5,H,q)!=1 and pow(5,43*H,q)==1
assert pow(5,43*H,p*p)==1
assert (n-S(2,3,32))%4==1 and (n-S(2,3,3))%3!=0
assert all((n-S(2,3,m))%m==1 for m in (7,11,19,23,31**3))

def safe(c,d):
    if (n-S(c,d,p))%p:
        return c,d
    for step,m,target in ((H,p*p,0),(p*H,p**3,p*p)):
        k, = [k for k in range(p) if (n-S(c+k*step,d,m))%m==target]
        c += k*step
    return c,d

def readings(c,d):
    return tuple((pow(3,c,m),pow(5,d,m)) for m in (31**3,q*q))

profile, touched = set(), 0
for x in range(49):
    for y in range(49):
        c,d = 2+K*x,3+K*y
        assert S(c,d,31**3)==S(2,3,31**3)
        C,D = safe(c,d)
        touched += (C,D)!=(c,d)
        assert (n-S(C,D,p))%p or (n-S(C,D,p**3))%p**3==p*p
        assert readings(C,D)==readings(c,d)
        assert (C-c)%lcm(3960,49)==0 and D==d
        profile.add(S(C,D,q))
assert touched==49 and len(profile)==2401 and n%q not in profile
assert safe(2,3)==(2+1424*H,3)
assert [(n-S(c,d,p**3))%p**3
        for c,d in ((2,3),safe(2,3),(2,3+H))]==[12169,1849,1849]
assert (n-S(2,3+H,q*q))%(q*q)==q

# Exact ordinariness check for this comparator's finite inert prefix.
P = bytearray(b'\1')*q
P[:2] = b'\0\0'
for k in range(2,isqrt(q-1)+1):
    if P[k]:
        P[k*k:q:k] = bytes((q-1-k*k)//k+1)
total = 0
for u in range(27,q,4):
    if P[u]:
        total += 1
        assert pow(3,u-1,u*u)!=1 or pow(5,u-1,u*u)!=1
assert total==592895
```

Availability here is in phase space. A common CRT translate can make the remainders positive for all finitely many restored representatives. A bound in a prescribed exponent window would require a separate height estimate.

Independent BigInt verification reproduced all 2401 distinct protected shifts, the 49 actual changes at 43, and the exact same-target failed alternative repair. A separate sieve scanned and checked all 592895 earlier inert rows for ordinariness. The remaining repairs follow by increasing-prime induction; no particular exponent-height range or common-Wieferich example is asserted.
