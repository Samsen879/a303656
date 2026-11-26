# Rank-seven escape through sixteen sources and the seventeen-common-prime condition

**Rank seven is excluded at both 15 and 16 sources.** On the selected muted slice, a first essential nonlinear projection at 7 leaves at least \(8/135\) of the lower CRT phase pairs with an uncovered 7-fibre. This closes the remaining first-pivot case at those budgets. Together with the earlier pivot bounds and the modulus bridge, it raises the necessary bound for a hypothetical finite all-exponent obstruction to **17 distinct inert primes Wieferich to both bases 3 and 5**. [Previous pivot and all-linear bounds](https://github.com/Samsen879/a303656/commit/e80d98299a361f515c77dca2fa71def8f2f85405) · [Rank-five bound](https://github.com/Samsen879/a303656/commit/9c2a6653449ff0016adb4b782b9db848c6227844) · [Exact modulus bridge](https://github.com/Samsen879/a303656/commit/1c648df4be90efe9065023067ec0125f4d1dbf59)

### The two-strip argument

Fix the same \(n,c\) and parity of \(d\). Keep the two first ternary branches outside row 7’s actual guard and the four first quinary branches outside row 11’s actual guard. If a guard is absent, discard any one first branch on its axis. Call the resulting box \(W\). In units of \(1/135\) of the full lower phase space, \(W\) has mass \(72\), and each of its two ternary halves has mass \(36\).

Let \(t\) sources read 7 and \(\ell\) be lower-only. Essentiality gives \(t\ge7\), and \(t+\ell\le16\). On \(W\), the lower-only union costs at most
\[
A(0)=0,\qquad A(\ell)=12+4(\ell-1)\quad(\ell\ge1).
\]
The shallow 5-strips and mixed depth-\((1,1)\) guards disappear with row 11’s strip. The pure second ternary guards all share row 19’s one position, worth at most 12 units. The remaining guards cost at most four units each. The first ternary lower-only guards are absent because row 7 is still unprocessed and row 31 is muted. [Shallow orders and rank-seven normal form](https://github.com/Samsen879/a303656/commit/7e8a1199597c2b27c705b454fdbf497d0d8155c0)

A first-level 7-prefix with an unrestricted lower guard is impossible on the muted slice. One with an entire first ternary branch as its lower guard must use one of the five actual order-\(21,42\) heads \(379,519499,43,127,7603\). At fixed \(n,c\) and parity, each head supplies **one pair** of ternary and 7 digits. Reusing a head cannot supply an additional pair, and distinct heads can share a 7 digit. Thus at least two 7-branches lack such a source. In either of those branches, each first-level source costs at most 18 units on \(W\), or 12 on either ternary half.

### Flat and nested alternatives

On \(W\), row 7 is inactive. A rigid full fibre can use seven first-level prefixes or six first-level prefixes and seven children in one expanded branch. A second expansion needs at least 19 sources.

- **Nested support is possible.** Only one branch can be expanded within budget 16. Among the six other branches, at least three have a unique source. Every flat or nested witness needs such a shared source. Its proper guard costs at most 36 units. Here \(\ell\le3\), so the uncovered mass is at least \(72-36-A(3)=16\).
- **Only flat support is possible.** Every flat alternative needs a live source in each branch. If either of the two branches missing a whole-ternary-branch guard is a singleton, its 18-unit cap leaves at least \(72-A(9)-18=10\) uncovered. Otherwise, let \(m\ge2\) be the smaller multiplicity of those two branches. If another branch is a singleton, its guard either costs at most 18 units or confines every flat alternative to one ternary half. In the latter case, the smaller branch caps flat coverage at \(\min(36,12m)\). With **two or three extra top sources** (\(t=9,10\)), \(m=2\). This leaves at least \(72-A(7)-24=12\) or \(72-A(6)-24=16\) units, respectively. With \(t\ge11\), the singleton bound gives at least \(72-A(5)-36=8\).
- **No branch is a singleton.** Then \(t=14,15,16\), and the smaller of the two branches has at most \(2,2,3\) sources, respectively. Charging 18 units per source and adding \(A(16-t)\) leaves at least \(20,24,18\) units uncovered.

If neither rigid alternative is possible, the lower-only union leaves at least \(72-A(9)=28\) units. Dynamic simple and nested alternatives on row 7’s guard have no effect on \(W\). These bounds concern CRT phases of a fixed target. The resulting 17-prime requirement concerns finite modulus certificates.

### Runnable replay

The first check uses one represented target with all five **actual** mixed heads live at distinct positions, alongside the actual guards of rows 7 and 11. The \(9\)- and \(10\)-top ledgers are **synthetic** and attain the 12- and 16-unit bounds for those cases. The exact-order and guard replay is included below.

```python
from math import isqrt, prod

for o, value, fs in (
    (21, (5**14+5**7+1)//31, (379,519499)),
    (42, (5**14-5**7+1)//21, (7,43,127,7603)),
):
    assert prod(fs) == value and len(set(fs)) == len(fs)
    for q in fs:
        assert q % 4 == 3 and all(q % j for j in range(2,isqrt(q)+1))
        w = next(j for j in range(1,o+1) if pow(5,j,q) == 1)
        assert w == (6 if q == 7 else o) and pow(5,w,q*q) != 1

m, u, v = 8*3*7*19*31*71*5167*19531, 3, 8
heads = [(379,0,0),(519499,1,135762),(43,0,13),(127,1,69),(7603,2,3245)]
for q,a,b in [(11,2,2)] + heads:
    u += m*((a-u)*pow(m,-1,q) % q)
    v += m*((b-v)*pow(m,-1,q) % q)
    m *= q
n = 3 + 1 + u*u + v*v

def roots(q,o):
    return [d for d in range(0,2*o,2) if (n-3-pow(5,d,q)) % q == 0]

assert {d%3 for d in roots(7,6)} == {2}
assert {d%5 for d in roots(11,5)} == {4}
assert {d%9 for d in roots(19,9)} == {4}
assert [{(d%3,d%7) for d in roots(q,21)} for q,_,_ in heads] == [
    {(0,j)} for j in (0,6,5,4,3)
]

W = {(x,y) for x in range(27) for y in range(4) if x%3 != 2}
top = [(j,0,3) for j in (0,6,5,4,3)]
top += [(j,a,9) for j in (1,2) for a in (0,3)]
low = [(4,9)] + [(x,27) for x in (1,7,10,16,19,25)]

def holes(top, low):
    return {(x,y) for x,y in W
            if not any(x%m == a for a,m in low)
            and {j for j,a,m in top if x%m == a} != set(range(7))}

assert len(W) == 72
assert len(holes(top,low)) == 12
assert len(holes(top+[(1,6,9)],low[:-1])) == 16
print("PASS")
def A(k): return 12+4*(k-1) if k else 0
assert 72-36-A(3)==16 and 72-A(9)-18==10
assert min(72-A(7)-24,72-A(6)-24,72-A(5)-36)==8
assert [72-A(16-t)-18*(j//2) for t,j in [(14,4),(15,5),(16,6)]]==[20,24,18]

```
The integrated result excludes, at total budget at most 16, first rank 5 by the rank-five theorem, rank 7 here, rank 11 by the preceding sixteen-source theorem, and rank 13 by the five-guard theorem. The separate all-linear tree bound also excludes this budget. A first essential nonlinear rank larger than the budget is not possible by the sparse projection rule. This does not claim a new numerical density bound or existence of a finite obstruction.
