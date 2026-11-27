# Uniform twenty-four centers, or twenty-three with strict unit heads

**The audit confirms the 23-center result and strengthens it to 24 on the same 37-offset menu.** The valuation-two convention at \(23\) gives 24 centers for every target. Requiring units at both \(23\) and \(67\) still gives **23 centers for every target**, including the previously unresolved strict-unit cases.

The improvement comes from using a different head to control \(127\), then using a free \(D\bmod5\) choice to clear \(211\) and \(631\). No second menu is needed.

### Audit of the \(23^2\) lock

The late-stage budgets can be recomputed with room for **25** candidates, covering both the audited 24-candidate construction and the exceptional head in the new proof. Each row can have at most 12 repeated classes. The fresh phase counts remain sufficient after inserting \(23^2\).

| Late block | Maximum exclusions | Distinct choices |
|---|---:|---:|
| \(19531,1303,519499\) | 25 | 31 |
| \(251\) | 12 | 25 |
| \(47,31051\), with \(23\) a unit | 22 | 23 |
| \(47,31051\), on the repair line | \(6+10\) | 23 |
| \(8971\), after the \(23^2\) lock | 12 | 13 |
| \(59\) | 8 | 29 |
| \(5167,35671\) | 17 | 41 |
| Remaining singleton blocks | At most 12 each | At least 67 each |

At the coupled step, \(K=19286363250\) is divisible by **both** axis periods of every previously fixed row. The line \(y=16x+t\bmod23\) enforces the first digit. At \(47\), its two factors are \(X,X^{10}\), as follows from \(3^K=(5^K)^{20}\) and \(20\cdot10\equiv16\bmod23\). The exact cap is six for each of the two possible repeated-index sets. At \(31051\), the \(D\)-move is invisible and at most ten choices are excluded. The top \(D\)-digit \(23K\) preserves both readings. All following \(C\)-moves use a multiple of \(23^2K\), and both ordinary repair locks include \(22\cdot23^2\).

### Save the seven-phase deletion

For the generic head, keep the two index classes other than \(1\bmod3\). The endpoint cut at \(23,67\) then leaves 24 candidates with the valuation-two convention, or 23 with the unit convention.

**Choose the head to control \(127\).**

- If \(n\not\equiv0\bmod127\), the two-coset cap at \(127\) is **three**. Among the seven \(C\)-phases, at most three can produce any repeated hit there for any \(D\)-phase.
- If \(n\equiv0\bmod127\), equal parities of \(C,D\) clear the row. With opposite parities, \(3\nmid C\) also clears it, because \(\operatorname{ord}_{127}(3)=126\) and \(\operatorname{ord}_{127}(5)=42\).
- The small-head table permits \(3\nmid C\) in every even-\(C\) case. In the odd-\(C\), even-\(D\) case it permits this except when both \(7,19\) read zero, or when \((n_7,n_{19},n_{11},n_{31})=(4,0,8,27)\). In the double-zero case, alignment of the classes removed at \(7,19\) forces \(3\mid C\). Moving \(C\) by \(30\) then makes \(9\mid C\) while preserving the early tests: the forbidden residues at 7 and 19 are \(C+D\) and \(2C+D\) modulo 3, respectively, so this move preserves their common omitted residue; the 11 and 31 orders divide 30. The identities \(3=5^5\bmod7\), \(3^2=5^5\bmod19\), and \(3^3=5^{29}\bmod127\) show that the \(127\)-hit class lies in the already omitted class at \(7\). For the isolated entry, \(C=27,D=2\) omits class \(2\bmod3\) and puts the \(127\)-hits in that same class. Rotate it to class \(1\) as usual.

At least four \(C\)-choices make \(71\) a unit for the **entire** order-five orbit on the \(D\)-axis. Thus one also clears the repeated hits at \(127\). For this \(C\), row \(43\) excludes at most six of the seven \(D\)-choices. Choose a survivor.

Now vary \(D\) by \(1386j\), \(0\le j<5\). This preserves \(43,127\) and the earlier readings, apart from \(11\), where the unit test remains valid on the entire order-five orbit. The \(71\) test also remains valid on that orbit. At \(211,631\) this move has order five. Each row has at most one repeated representative in the generic head, so together they exclude at most two choices. **Finalize the \(D\)-reading at \(11\) here**, then freeze the usual \(6930\) periods. The generic seven-phase loss is zero.

The exceptional small head \((1,1,2,0,8,27)\) starts from all 27 candidates at \(C=D=89\). Each cut class \(5,9\bmod11\) contains three candidates. Keep one member of the chosen class for the valuation-two convention, dropping the reserved endpoint \(27\) or \(9\). This leaves 25. Under the strict convention, drop the whole class and keep 24. The \(199\) test still cannot veto both cuts, and the old one-deletion seven-phase bound applies. Both branches therefore meet the stated guarantees.

The reserved endpoint and the \(379\) triple exclusion remain intact. At \(191,6271\), twelve repeated classes per row still leave \(19(19-12)=133>6\cdot12\) phase pairs in the mixed zero/nonzero case. The audited late budgets then finish the construction.

### Same-target controls

The replay starts with \(C=22,D=631\) and 24 indices.

- With \(D=631\), the \(211\)-reading ties indices \(0,35\), with first readings \(38,99\). The free move \(D\mapsto2017\) clears that row.
- On the **same target**, repairing \(23\) on the \(D\)-axis alone gives exact valuation two there, but ties indices \(0,23\) at \(47\) with first readings \(11,24\). The coupled move clears \(47\). Ordinary repair through \(211\) then gives exact remainders \(17\cdot23^2\bmod23^3\) and \(3\cdot67^2\bmod67^3\).
- Protecting only the first digit at \(23\) is insufficient. The replay gives a later \(C\)-move that preserves every retained ordinary reading modulo its cube and changes the \(23\)-valuation to **exactly three**.

The unchanged squarefree certificate bounds each genuine common-Wieferich reader to one hit **within the selected menu**. Consequently a blocking finite panel must contain at least 24 such readers under the valuation-two convention, or 23 under the strict convention. This is a finite-phase result. It gives no ordinary exponent-height bound for the input \(n\).

```python
from collections import Counter
from itertools import product
from math import gcd, isqrt, lcm, prod

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p
def prime(p):
    return p>1 and all(p%q for q in range(2,isqrt(p)+1))
def fq(b,p):
    return (pow(b,p-1,p*p)-1)//p

# The certified tie set and factor support of its q-1 values.
T={31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,4159,
   5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,595123,3981071,
   5096867,9384251,12207031,16018507,190771747,28086211607,386478495679,
   6090817323763,42272797713043,625552508473588471}
A=(2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,911,
   1367,3701,4523,13967,37537,87877,391337,2061161,25654001,453003413,5855734783)
assert all(map(prime,A))
def order(b,q):
    r=u=q-1
    for p in A:
        while r%p==0: r//=p
        while u%p==0 and pow(b,u//p,q)==1: u//=p
    assert r==1
    return u
O={q:(order(3,q),order(5,q)) for q in T|{7,11,19,23}}
U,V=lcm(3960,*(q-1 for q in T)),lcm(3960,*range(2,71,4))
assert all(V%p and fq(5,p) for p in A if p>23 and p%4==3 and p!=31)

G=[(7,(19531,1303,519499)),(1,(251,)),(1,(47,31051)),
   (1,(8971,)),(1,(59,)),(1,(5167,35671))]
G += [(1,(q,)) for q in (12207031,5227,38923,3981071,7603,42272797713043,
       9384251,16018507,5096867,6090817323763,28086211607,625552508473588471,
       595123,190771747,386478495679)]
K=187110*19
locked={7,11,19,23,31,67,199,71,43,127,211,631,271,379,4159,163,487,191,6271}
for s,Q in G:
    assert all(K%O[q][0]==0 for q in locked)
    r=sum(min(12,m,37-m) for q in Q for m in (O[q][1]//gcd(8,O[q][1]),))
    assert all(O[q][0]//gcd(s*K,O[q][0])>r for q in Q)
    if Q==(47,31051):
        assert K==19286363250 and K%23 and K%22==0
        assert all(K%O[q][1]==0 for q in locked)
        K*=23**2
    K=lcm(K,*(O[q][0] for q in Q))
    locked.update(Q)
assert K%4==2 and K%(22*23**2)==0

# Small-head table. A bit represents a pair (n11,n31).
def excluded(nonzero):
    bad=set()
    for a,b in product(range(2),repeat=2):
        rows=[]
        for c,d,k in product(range(a,90,2),range(b,18,2),range(3)):
            if nonzero and c%3==0: continue
            X,Y,Z=[{S(c,d+8*i,q) for i in range(9) if i%3!=k}
                   for q in (7,19,31)]
            M=sum(1<<(31*u+v) for u,v in product(range(11),range(31))
                  if v not in Z and (u-pow(3,c,11))%11 not in (1,3,4,5,9))
            rows.append((X,Y,M))
        for u,v in product(range(7),range(19)):
            M=0
            for X,Y,W in rows:
                if u not in X and v not in Y: M|=W
            bad.update((a,b,u,v,j//31,j%31) for j in range(341) if not (M>>j)&1)
    return bad

rare=(1,1,2,0,8,27)
assert excluded(False)=={rare}
assert excluded(True)==({rare,(1,1,6,0,8,27),(1,0,4,0,8,27)}
    | {(1,0,0,0,u,v) for u,v in product(range(11),range(31))})
assert all(S(27,2+8*i,q)!=r for i in range(45) if i%3!=2
           for q,r in ((7,4),(19,0),(11,8),(31,27)))
assert pow(5,5,7)==3 and pow(5,5,19)==pow(3,2,19)
assert pow(5,29,127)==pow(3,3,127) and O[127]==(126,42)

def cap(q,b,shifts):
    X={pow(i,(q-1)//7,q) for i in range(1,q)}
    Y={pow(i,(q-1)//b,q) for i in range(1,q)}
    W={pow(5,8*j,q)*y%q for y in Y for j in shifts}
    return max(max(k for n,k in Counter((x+t*y)%q for x in X for y in W).items() if n)
               for t in range(1,q))
assert cap(71,5,(0,))==3
assert [cap(127,7,(0,j)) for j in (1,2)]==[3,3]
assert all(pow(5,1386,q)==1 for q in (7,19,23,31,43,67,127,199))
assert all(O[q][1]//gcd(O[q][1],1386)==5 for q in (211,631))

# Actual same-target fixture.
I=[i for i in range(37) if i%3!=1 and i!=27]
c,d0,d=22,631,2017
K=19286363250
assert [i for i in I if S(c,d0+8*i,211)==3]==[0,35]
assert all(S(c,d+8*i,211)!=3 for i in I)
n23=2047
t=((n23-S(c,d+40,23**2))%23**2//23)*pow(
    pow(5,d+40,23)*((pow(5,K,23**2)-1)//23),-1,23)%23
assert t==2
badD=d+K*t
C,D=c+K,d+18*K
assert (n23-S(c,badD+40,23**3))%23**3==9*23**2
assert (n23-S(C,D+40,23**3))%23**3==17*23**2

P=tuple(q for q in range(27,212,4) if prime(q))
R=[(32,23),(3,1),(23**3,n23),(47,31),(67**3,283812),(211**2,3)]
for q in (T|{7,11,19}|set(P))-{47,67,211}:
    F={S(C,D+8*i,q) for i in I}
    if q in {7,11,19,31}: F|={S(c,d0+8*i,q) for i in I}
    R.append((q,next(r for r in range(q) if r not in F)))
M=prod(q for q,r in R)
n=sum(r*(M//q)*pow(M//q,-1,q) for q,r in R)%M
assert [(n-S(c,d0+8*i,211**2))%211**2 for i in (0,35)]==[38*211,99*211]
assert [(n-S(c,badD+8*i,47**2))%47**2 for i in (0,23)]==[11*47,24*47]

k=23**2
for p in P:
    hits=[i for i in I if (n-S(C,D+8*i,p))%p==0]
    if hits:
        i,=hits
        B,b=next((lcm(k,W,p-1),b) for W,b in ((V,5),(U,3))
                 if lcm(k,W,p-1)%p and fq(b,p))
        E=C if b==3 else D+8*i
        j=((n-S(C,D+8*i,p*p))%(p*p)//p)*pow(
            pow(b,E,p)*((pow(b,B,p*p)-1)//p),-1,p)%p
        if b==3: C+=B*j
        else: D+=B*j
        if (n-S(C,D+8*i,p**3))%p**3==0:
            if b==3: C+=B*p
            else: D+=B*p
    k=lcm(k,p*p*(p-1))
assert (n-S(C,D+40,23**3))%23**3==17*23**2
assert (n-S(C,D+40,67**3))%67**3==3*67**2
assert all((n-S(C,D+8*i,q))%q for i in I if i!=5 for q in (23,67))
for i,p in product(I,P+(23,)):
    r=(n-S(C,D+8*i,p**3))%p**3
    assert r%p or (r and r%p**2==0)

# Preserve the ordinary prefix and the first digit at 23, but omit 23^2.
B=lcm(U,*(q*q*(q-1) for q in P))
assert B%23==0 and B%23**2
assert (n-S(C+7*B,D+40,23**4))%23**4==12*23**3
assert all(S(C+7*B,D+8*i,q**3)==S(C,D+8*i,q**3) for i in I for q in P)
```
