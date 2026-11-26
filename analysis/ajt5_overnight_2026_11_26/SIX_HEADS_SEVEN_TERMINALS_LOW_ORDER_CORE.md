# Seven targets with six preselected heads via the low-order core

**The same six terminal-blind heads suffice for seven terminals.** No seventh head is needed. Release the \(3,5,7\) coordinates together, clear the lowest-order rows on their own coordinates, and charge the remaining rows against the surviving fraction. The only equality case is seven pure \(7\)-readers. Their actual \(3,5\) orders rule out a full cover. [Six-head baseline](https://github.com/Samsen879/a303656/blob/0afc5d8f578b9f5d59230937a3b6173f6a815a41/analysis/ajt5_overnight_2026_11_26/SIX_FIXED_HEADS_JOINT_3_5_AVOIDANCE.md)

Precisely, in any finite panel with at most seven designated inert terminals above \(23\), if every other required inert row above \(23\) is ordinary, some phase in the unchanged menu gives units at all the designated terminals and passes the ordinary rows. The designated terminals may be genuine common Wieferich primes. The proof does not assume that any exist.

### Clear the low-order rows jointly

Peel free sources above \(7\) as in the six-head proof. The active count never increases, and each restored reader at those sources has at least eleven free values on one axis. At the bottom, choose a head passing the pinned rows. There are only five such rows, and each vetoes at most one of the six heads.

At an unpinned target let \(x,y\) be the free orders of \(3,5\), respectively, after the mod \(3960\) lock. There are at most two rows with \(\max(x,y)=3\), namely \(271,2971\), and both read only the first free \(3\)-digit of \(d\). If either is present, fix that digit to avoid both. The remaining denominator for a row is then \(\max(x,y/\gcd(y,3))\). If neither is present, keep the whole block.

The exact gcd in the replay certifies all restricted denominators below \(9\). Indeed, if \(x,y/\gcd(y,3)\in\{1,3,5,7\}\), both full orders divide \(311850=990\cdot9\cdot5\cdot7\). The low-order rows that remain are:

| Denominator | Possible rows | Coordinates read after the restriction |
|---:|---|---|
| \(3\) | \(1783\), only after fixing the digit of \(d\) | \(3\) only |
| \(5\) | \(151,4951\) | \(5\) only |
| \(7\) | \(43,71,127,211,463,631,883,2311,34651\) | \(7\) only |

Let \(a\) be the number of shallow rows cleared by fixing the digit of \(d\), and let \(e,b,c\) count the three rows or groups in the table, respectively. Since the groups read disjoint coordinates, the surviving fraction is at least
\[
(1-e/3)(1-b/5)(1-c/7).
\]
The remaining rows together cost at most \((7-a-e-b-c)/9\) of that same grid before the low-order exclusions. The first expression exceeds the second in every admissible case except \((a,e,b,c)=(0,0,0,7)\). The minimum positive slack is \(2/63\) without the digit restriction and \(1/15\) with it.

### Seven pure \(7\)-readers cannot cover the grid

Each reader excludes at most seven cells of the \(7\times7\) grid. A cover would require seven disjoint sets of size seven. Only \(71,2311\) read one axis. Such a set is a column and intersects every full matching from a two-axis reader.

If all seven read both axes, they include \(43\) and \(127\). A full matching at a two-axis reader forces \(n\equiv0\bmod p\), by summing the seven shift equations over the matching. At zero, each full matching is a line in the two exponent digits. The slopes at \(43\) and \(127\) are \(2\) and \(5\bmod7\), as certified by \(3^{3960}\equiv(5^{3960})^m\bmod p\). These lines intersect for every choice of intercepts. This rules out the cover.

The reusable test is to compare the surviving fraction of a jointly cleared core with the sum of reciprocal restricted orders of the remaining rows. The product bound here uses disjoint exponent coordinates. Exact union counts can replace it when the core rows share coordinates.

### Standalone replay

```python
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt, prod

C = 3960
P = (2,7,11,19,23,31,61,67,181,199,331,661,991)
Q = (7,43,71,109,127,151,163,211,271,379,421,463,541,631,
     811,883,1051,1621,1783,2269,2311,2971,3301,3851,4051,
     4159,4621,4951,6301,8101,9901,11551,14851,28351,34651,
     56701,89101,103951,170101,669901,1247401)

def prime(p):
    return p>1 and all(p%j for j in range(2,isqrt(p)+1))

def free(b,p):
    o = next(j for j in range(1,p) if pow(b,j,p)==1)
    return o//gcd(o,C)

assert all(map(prime,P+Q))
G = gcd(3**990-1,5**990-1)
assert G == 44*prod(P)
assert gcd(3**311850-1,5**311850-1) == G*prod(Q)
assert [p for p in P if p>23 and p%4==3] == [31,67,199,331,991]

both = (43,127,211,463,631,883,34651)
one = (71,2311)
small = {}
for p in Q:
    if p>23 and p%4==3:
        x,y = free(3,p),free(5,p)
        if max(x,y//gcd(y,3))<9:
            small[p]=(x,y)
assert small == ({151:(5,5),271:(1,3),1783:(3,9),
                  2971:(1,3),4951:(1,5)}
                 | dict.fromkeys(both,(7,7)) | dict.fromkeys(one,(7,1)))
assert pow(5,2*C,43)==pow(3,C,43)
assert pow(5,5*C,127)==pow(3,C,127)

slack = [[],[]]
for a,b,c,e in product(range(3),range(3),range(8),range(2)):
    H = 7-a-b-c-e
    if H<0 or (a==0 and e) or (a,b,c,e)==(0,0,7,0):
        continue
    slack[bool(a)].append((1-F(e,3))*(1-F(b,5))*(1-F(c,7))-F(H,9))
assert list(map(min,slack)) == [F(2,63),F(1,15)]

# Same-integer ordinary control with seven full matchings.
n,c,d = 29407723963969150905396789,495,990
def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

assert (n-S(c,d,32))%32==1 and (n-pow(5,d,3))%3==2
assert all((n-S(c,d,p))%p==1 for p in (7,11,19,23))
sets = []
for p in both:
    assert n%p==0 and all(pow(b,p-1,p*p)!=1 for b in (3,5))
    bad = {(i,j) for i,j in product(range(7),repeat=2)
           if S(c+C*i,d+C*j,p)==0}
    assert len(bad)==7
    sets.append(bad)
assert len(set.union(*sets))==25  # 24 of 49 cells survive
print("OK")
```

The replay’s seven readers are ordinary. It illustrates the intersection mechanism at an actual integer, while the theorem applies to genuine exceptional terminals under the stated panel hypothesis. This is a fixed-menu finite-local result. It supplies no new numerical density bound or pointwise conclusion.

The earlier unrestricted ten-target theorem remains stronger when no small-head menu is fixed. This result preserves an explicit six-head menu selected independently of all terminal readings.
