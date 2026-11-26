# Preselected mod-3960 menus for up to three terminal unit tests

**Three preselected mod \(3960\) heads suffice for any two terminals.** The original two heads can be kept. The third depends only on the small-head readings. Three is the minimum for a uniform **pinned-unit** guarantee. With one additional arithmetic check, four heads also suffice for three terminals.

More precisely, in any finite panel with \(k\le 3\) designated inert terminals above \(23\), the construction below selects \(k+1\) heads before seeing the terminals or their readings. If every other required inert row above \(23\) is ordinary, some phase in the menu gives units at all \(k\) terminals and passes every ordinary row. The terminals may be genuine common Wieferich primes. The proof makes no assumption about their existence or distribution. [Two-terminal descent](https://github.com/Samsen879/a303656/blob/d5a65214efd6035346f81e3182ebf9674d1bede1/analysis/ajt5_overnight_2026_11_26/DUAL_HEAD_TWO_TERMINAL_DESCENT.md)

### Why the menu works

After descent, a pinned terminal has both orders dividing \(3960\), hence dividing \(990\) by inertness. The exact gcd calculation gives five possibilities above \(23\).

| Pinned prime \(p\) | \(\operatorname{ord}_p(3)\) | A separating factor |
|---:|---:|---:|
| 31 | 30 | 5 |
| 67 | 22 | 11 |
| 199 | 198 | 11 |
| 331 | 330 | 5 |
| 991 | 330 | 5 |

So the heads only need distinct \(c\bmod5\) and distinct \(c\bmod11\), with a common \(d\). Keep \(d\) and \(c\bmod8\) from the existing menu. To add a head, take the first legal adjustment at each of \(7\) and \(19\). At \(11\), the five choices in steps of \(72\) give five different \(c\bmod5\), and the row excludes at most one. At \(23\), the eleven choices in steps of \(360\) give eleven different \(c\bmod11\), again with at most one excluded. Choose the first legal residue unused by the menu at each stage. The \(23\) stage preserves \(c\bmod5\). This adds heads until there are four, without changing any old head. [Small-head selection policy](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

Each pinned row now vetoes at most one head. During descent, remove all targets reading the largest free prime \(s\), and insert \(s\) as one auxiliary unit target if it is inert and above \(23\). The target count never increases. On restoration, vary the free \(s\)-primary digits on both axes. A reader with \(D\) distinct values on its stronger axis excludes at most a fraction \(1/D\) of the grid. The other live targets are unchanged. An ordinary row above \(s\) can be repaired using its own primary digit, which no current target reads.

For two terminals, the total exclusion at any step is at most \(2/s<1\), including shared sources. For three terminals, only \(s=3\) needs an extra check. A reader extending to \(3^4\) or higher has at least nine free values, so the total exclusion is at most \(1/9+2/3<1\). Otherwise all current orders divide \(2970\). Writing \(G_m=\gcd(3^m-1,5^m-1)\), the exact identity
\[
G_{2970}=G_{990}\cdot109\cdot271\cdot541\cdot2971
\]
leaves only \(271\) and \(2971\) as inert readers of the newly freed digit. Their combined exclusion is at most \(2/3\).

**Minimality at the pinned rows.** With at most \(k\) preselected heads, assign each head a different pinned prime and set the observation there equal to that head’s shift. CRT realizes these readings while preserving all small-head readings. This defeats every head, even if the menu uses different \(d\)'s. It proves the \(k+1\) minimum for the pinned-unit test. It does not establish a lower bound for menus tested only against genuine exceptional terminals.

### Standalone replay

On the earlier ordinary countercontrol, the rule adds \((3,275)\) to \((339,275),(11,275)\). It gives units at both pinned rows and at both higher readers, for the same integer.

```python
from math import gcd, isqrt, prod

P = (2,7,11,19,23,31,61,67,181,199,331,661,991)
extra = (109,271,541,2971)

def prime(p):
    return p > 1 and all(p % j for j in range(2,isqrt(p)+1))

def order(b,p):
    return next(i for i in range(1,p) if pow(b,i,p)==1)

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

assert all(map(prime,P+extra))
G = gcd(3**990-1,5**990-1)
assert G == 44*prod(P)
assert gcd(3**2970-1,5**2970-1) == G*prod(extra)
assert [p for p in extra if p%4==3] == [271,2971]
pinned = [p for p in P if p>23 and p%4==3]
assert [(p,order(3,p),order(5,p)) for p in pinned] == [
    (31,30,3), (67,22,22), (199,198,33), (331,330,165), (991,330,495)]

rows = ((7,8,3),(19,24,3),(11,72,5),(23,360,11))
for i,(p,h,k) in enumerate(rows):
    assert h%8==0 and len({pow(3,j*h,p) for j in range(k)})==k
    assert all(pow(3,h,t)==1 for t,_,_ in rows[:i])
    assert all(pow(b,3960,p)==1 for b in (3,5))
assert 72%5 and 360%5==0 and 360%11

n, d = 1352683603486061699285433, 275
heads = (339,11)
c = 3
for p,h,k in rows:
    c = next(x for x in (c+j*h for j in range(k))
             if (n-S(x,d,p))%p and
             (p not in (11,23) or all((x-y)%k for y in heads)))
assert c==3
for x in heads+(c,):
    assert (n-S(x,d,32))%32==1 and (n-pow(5,d,3))%3
    assert all((n-S(x,d,p))%p for p,_,_ in rows)
assert (n-S(339,d,31))%31==0 and (n-S(11,d,67))%67==0
assert [(n-S(c,d,p))%p for p in (31,67,2791,19163)] == [2,39,1740,3766]
assert all(pow(b,q-1,q*q)!=1 for q in (2791,19163) for b in (3,5))
print("OK")
```

The ordinary replay tests unit avoidance. Its two higher readers are ordinary, and a failed unit there can still pass the norm test by an even-valuation repair. The theorem excludes finite local blockers with up to two exceptional rows using three heads, or up to three using four heads. Global density one and the pointwise conjecture remain open.

This fixed-menu result addresses preselection under the specific small-head lock; the earlier unrestricted ten-target count remains stronger in count. In the restoration, the free primary block includes all digits read at the chosen prime, so the larger number of values for depth at least four at the source 3 is actually available. No improvement to the density estimate is implied.
