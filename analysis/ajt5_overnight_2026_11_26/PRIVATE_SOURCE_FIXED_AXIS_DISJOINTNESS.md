# Fixed-axis private orders do not force forbidden-set overlap

**Large private order coordinates do not guarantee synchronization or any strict improvement over the union bound.** On the archived target, the two genuine base-5 exceptional guards have disjoint hard sets at fixed \(c=6\), even after the ordinary rows are repaired and both private \(d\)-digits are fully free. The same target gives a stronger test with movable \(c\): the private source orders are \(335\) and \(653\), both larger than the square roots of their guard primes, yet no common exponent pair hits both guards in the specified block. [Fixed-target baseline](https://github.com/Samsen879/a303656/blob/fe439b734c6f683a4cb796036d8810f69d91dc23/analysis/ajt5_overnight_2026_11_26/FIXED_TARGET_COFACTOR_SYNCHRONIZATION.md)

### Fixed-\(c\) obstruction and usable capacity

Fix \(N,C\). At an inert prime \(p>3\), put \(o_p=\operatorname{ord}_p(5)\) and \(w_p=v_p(5^{o_p}-1)\). If \(N-3^C\) lies in \(\langle5\rangle\) modulo \(p\), there is a unique collision class \(d\equiv e_p\pmod{o_p}\). The order modulo \(p^{w_p}\) is still \(o_p\). Thus, if the residual on that class has an odd valuation below \(w_p\), **the exact hard set is that entire class**. If \(N-3^C\equiv0\pmod p\), every residual is a unit. Two hard classes can intersect only if their anchors agree modulo \(\gcd(o_p,o_q)\). Movement on other primary coordinates and ordinary repairs cannot change this condition while \(C\) stays fixed.

Private digits still give a useful escape criterion. Condition on the shared digits and suppose each hard row has a genuinely free private coordinate, unread by the other rows, with \(k_p\) distinct available choices at its actual read depth. Each row removes at most one of its choices. The surviving fraction is at least \(\prod_p(1-1/k_p)\). This applies after accounting for the ordinary repairs: rows that read a reserved digit must already be certified or included in that digit’s allowed choices. When the remaining ordinary lifting digits are unread by the protected rows, they can be repaired in increasing prime order, since the order modulo a smaller prime power cannot read a larger prime’s digit. This gives a sufficient escape from such a finite panel. The actual orders alone do not certify the required freedom.

### Exact control on the archived target

Use
\[
N=10+9752781853725239220214221361^2+
11075246640031221347570696376^2.
\]
At \(p=20771\) and \(q=40487\), the base-5 orders are \(31\cdot335\) and \(31\cdot1306\), respectively, and both lift unchanged modulo the prime square. Fix \(C=6\) and \(d\equiv1229\pmod{10890}\).

| Guard | Collision anchor \(e_p\) | Exact hard condition on the free digits | Repaired representative \(d\) |
|---|---:|---|---:|
| \(20771\) | \(2274\) | \(d_{31}=11,\ d_{67}=63\) | \(6742139\) |
| \(40487\) | \(17049\) | \(d_{31}=30,\ d_{653}=71\) | \(104066069\) |

For the entire progression, the residuals modulo \(4,27,11^3,67\) are \(1,18,363,24\), respectively. At \(31\), \(N-3^6\equiv17\) lies outside \(\{1,5,25\}\), so that row is a unit throughout. The two listed representatives have exact valuation \(1\) at their specified guard and are units at the other guard. Since \(31,67,653\) are coprime to \(10890\), the three digits are fully independent. The union therefore has measure exactly
\[
\frac1{31\cdot67}+\frac1{31\cdot653}.
\]
The union bound is attained, with both hard sets nonempty after the ordinary repairs.

### Allowing both private \(c\)-sources to move

On the same \(N\), allow \(c\ge2\), \(c\equiv0\pmod{66}\), and lock \(d\equiv7542150\pmod{14437830}\). Write \(j=d\bmod31\). At each guard, take the base-3 log of \(N-5^d\) when it exists, then reduce that log modulo \(31\) to obtain the required \(i=c\bmod31\). The private source orders \(335=5\cdot67\) and \(653\) are fully available. The only \(j\) with a log at both guards give
\[
(j,i_p,i_q)=(1,25,2),(7,15,1),(13,25,15),(24,1,21),(27,2,22).
\]
Thus the projected \(d\)-labels overlap in five places, and none admits the same \(c\). The replay checks these values using both direct logs and the primary projection with actual slopes \(6,7\).

On the \(c\equiv0\pmod{330}\) branch the ordinary \(31\)-adic repair requires \(14i+22j=0\pmod{31}\), or \(i=25j\). The next \(31\)-digit can set valuation exactly \(2\) while preserving both guards modulo their squares. After this repair, the two hard projections on that branch are the singletons \(\{1\}\) and \(\{13\}\). Exact witnesses are \((c,d)=(11859540,195233940)\) and \((100527900,79731300)\), respectively. Each has valuation \(1\) at its guard, is a unit at the other, and passes the ordinary rows. The pair \((153450,354050070)\) passes the whole displayed panel.

The large representatives certify congruences at the archived \(N\). To activate all of them simultaneously, write \(N=10+A^2+B^2\), take \(M=\operatorname{lcm}(4,27,11^3,31^3,67,p^2,q^2)\), and use \(N_t=10+(A+Mt)^2+B^2\) for every sufficiently large integer \(t\). This preserves all checked residues and the actual representation at \((c,d)=(2,0)\). The result rules out a uniform overlap saving from private orders alone. Excluding a full finite blocker still requires finding a repair-compatible escape for every candidate panel.

```python
from math import gcd
N=10+9752781853725239220214221361**2+11075246640031221347570696376**2
p,q=20771,40487
def rem(c,d,m):return (N-pow(3,c,m)-pow(5,d,m))%m
for z,o3,o5,e,rep,y in ((p,10385,10385,2274,6742139,14782),(q,20243,40486,17049,104066069,8370)):
    for b,o in ((3,o3),(5,o5)):
        assert pow(b,o,z)==1 and all(pow(b,o//l,z)!=1 for l in (2,5,31,67,653) if o%l==0)
    assert pow(5,o5,z*z)==1 and rem(6,e,z*z)==y*z
    assert rep%10890==1229 and rep%o5==e and rem(6,rep,z*z)==y*z
    assert rem(6,rep,p+q-z)
assert (N-pow(3,6,31))%31==17 and {pow(5,d,31) for d in range(3)}=={1,5,25}
for m,R in ((4,1),(27,18),(1331,363),(67,24)):
    assert rem(6,1229,m)==R and pow(5,10890,m)==1
M,base=14437830,7542150
L=[{pow(3,i,z):i%31 for i in range(o)} for z,o in ((p,10385),(q,20243))]
hits=[[],[]]
common=[]
for j in range(31):
    d=base+M*((j-base)*pow(M,-1,31)%31)
    labels=[log.get((N-pow(5,d,z))%z) for log,z in zip(L,(p,q))]
    if None not in labels:common.append((j,*labels))
    for i,y in enumerate(labels):
        if y==25*j%31:hits[i].append(j)
assert common==[(1,25,2),(7,15,1),(13,25,15),(24,1,21),(27,2,22)]
assert hits==[[1],[13]]
for c,d,st in ((11859540,195233940,(0,1)),(100527900,79731300,(1,0)),(153450,354050070,(1,1))):
    assert c%330==0 and d%M==base
    assert bool(rem(c,d,p))==bool(st[0]) and bool(rem(c,d,q))==bool(st[1])
    for z,a in zip((p,q),st):
        if not a: assert rem(c,d,z*z)%z==0 and rem(c,d,z*z)>0
    assert rem(c,d,31**3) in range(31**2,31**3,31**2)
    assert rem(c,d,4)==1
print("OK")
```

This is a limitation on uniform overlap claims. Fully private repair-compatible digits still give the product escape bound under the stated hypotheses.
