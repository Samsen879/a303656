# Rank-seven fourteen-source escape and the fifteen-common-prime bound

**A first essential nonlinear projection at 7 cannot complete the selected muted slice with 13 or 14 rigid sources.** In fact, at least \(2/45\) of the lower CRT phase pairs have an uncovered 7-fibre. The proof allows flat and nested witnesses to coexist and keeps row 7’s actual guard. The final section below supplies a separate all-linear argument using only the first two ternary depths. [Previous projection bounds](https://github.com/Samsen879/a303656/commit/c94891822bf99e26b42c36e4ad9fe45fe4376917)

### Exact alternatives at 7

Fix \(n,c\) and the parity of \(d\). After the higher linear projections, each source has one lower guard on the \(3,5\) coordinates and at most one 7-prefix. Let \(L\) be the union of the lower-only guards. A source is live when its lower guard contains the chosen phase pair.

Row 7 has order \(6\) and ordinary lifting. Its actual guard \(H\) is empty or one first ternary branch. Write \(C_j\) for the prefix of its exponent center modulo \(7^j\), and \(7^K\) for its precision. Outside \(L\), the full-fibre alternatives are as follows.

- **Outside \(H\).** Either all seven first-level prefixes are live, or six are live and the seventh branch has all seven second-level prefixes live. The two shapes use 7 and 13 sources. A complete prefix tree with two expanded branches needs at least 19.
- **On \(H\).** A live \(C_1\) completes the fibre. Otherwise, six second-level side branches inside \(C_1\) require rigid coverage, and the center needs the coverage in the table. At most one of these seven requirements can use an expansion. Expanding a side means using all seven of its children.

| Precision \(K\) | Basic center requirement | Expanded center requirement |
|---|---|---|
| \(2,3\) | \(C_2\) | All seven children of \(C_2\) |
| \(4,5\) | \(C_2\) or \(C_3\) | All seven children of \(C_3\) |
| \(\ge6\) | \(C_2\) or \(C_3\) | The six depth-four siblings of \(C_4\), and \(C_4\) or \(C_5\) |

This follows by alternating the rejected odd-valuation shells and safe even-valuation shells. The terminal zero class remains safe. Each expansion replaces one requirement by seven and costs six additional sources. The projection takes the **union** of the live alternatives, each of which takes the **intersection** of its constituent lower guards. A flat and a rigid nested witness can share six sources and coexist at exactly 14. A flat and an unexpanded dynamic nested witness can also coexist at 14, using disjoint sources. [Earlier guarded rank-seven rule](https://github.com/Samsen879/a303656/commit/c0d8aee19ff506f97e4e0bf63b2efc6025d4692e)

### The actual-order obstruction

Use the selected mutes \(3,31,71,5167,19531\). A first-level 7-source with unrestricted lower guard is impossible. Its raw order or least helper would have order \(7\) or \(14\), and the sole inert head, 19531, is muted. A first-level 7-source whose lower guard is an entire first ternary branch can come only through one of **five** heads. The new identities are
\[
\Phi_{21}(5)=379\cdot519499,\qquad
\Phi_{42}(5)=7\cdot43\cdot127\cdot7603.
\]
The factor 7 has order 6. The other five are ordinary inert primes of exact orders 21 or 42. The products are squarefree, so there is no raw rigid source of either order. The least-helper argument applies because an extra odd order factor could disappear only through a still smaller helper, and intersection preserves prefix depth. At the fixed target and parity, each head supplies only one first-level 7 position. Thus at least **two** 7-branches lack a source carrying an entire first ternary branch.

Put \(W=H^c\) if \(H\) is active. Otherwise take any two first ternary branches for \(W\), so \(\mu(W)=2/3\) in both cases. Let \(t\) be the number of top sources and \(\ell\) the number of lower-only sources. Essentiality gives \(t\ge7\), so \(\ell\le7\). The actual lower orders give the following bounds.

- The shallow 5-strips and mixed depth-\((1,1)\) guards all lie in row 11’s one 5-strip. Pure second-level ternary guards lie in row 19’s one prefix. Every other lower-only guard costs at most \(1/27\) on \(W\). There are no pure first-level ternary lower-only guards.
- Consequently \(\mu(L\cap W)\le58/135\). For \(\ell\le5\), the bounds are \(16/45\) on \(W\) and \(13/45\) on any one first ternary branch. For \(\ell\le1\), the bound on \(W\) is \(2/15\).

If a rigid nested witness is structurally possible, then \(\ell\le1\). Only one branch can have seven second-level prefixes, and at least five of the six other branches have a unique first-level source. Any rigid witness, flat or nested, needs that source. Its proper lower guard costs at most \(1/3\), leaving at least \(2/3-1/3-2/15=1/5\) uncovered on \(W\).

Otherwise, only flat witnesses matter on \(W\). If none is structurally possible, \(L\) alone leaves a gap. If \(t\le8\), at least one of the two branches missing a whole-ternary-branch source is a singleton. Its guard costs at most \(2/15\) on \(W\), even when \(\ell=7\). If \(9\le t\le13\), some branch is a singleton and \(\ell\le5\). Either its guard costs at most \(2/15\), or it is a whole first ternary branch and the other branch of \(W\) has at least \(1/3-13/45=2/45\) uncovered. Finally, if \(t=14\), then \(L\) is empty. A singleton already leaves a gap. Without one, every branch has two first-level sources, and in a branch missing whole-ternary-branch guards the pair covers at most \(4/15\) of \(W\).

### Inline replay

The modular control uses the actual row 7 at \(77=3+1+3^2+8^2\), with \(c=1\) and even \(d\). The rigid ledgers are synthetic. The replay below verifies the named order data, competing witnesses, and the lower-phase measures.

```python
from math import isqrt, prod

for o, value, fs in (
    (21, (5**14+5**7+1)//31, (379,519499)),
    (42, (5**14-5**7+1)//21, (7,43,127,7603)),
):
    assert prod(fs) == value and len(set(fs)) == len(fs)
    for q in fs:
        assert all(q % j for j in range(2,isqrt(q)+1))
        w = next(j for j in range(1,o+1) if pow(5,j,q) == 1)
        assert q % 4 == 3 and w == (6 if q == 7 else o)
        assert pow(5,w,q*q) != 1

# Each source is (live lower y, 7-prefix residue, depth). -1 means any y.
def full(rows, x, y, K):
    live = [(z,7**g) for a,z,g in rows if a in (-1,y)]
    M = max([7**(K-1)] + [m for z,m in live])
    for t in range(M):
        d = t + M*((-2*x-t) % 6)   # d even, d = x mod 3
        r, v = (74-pow(5,d,7**K)) % 7**K, 0
        while r and r % 7 == 0:
            r, v = r//7, v+1
        if not (v % 2 or any(t % m == z for z,m in live)):
            return False
    return True

seconds = list(range(2,49,7))
flat = [(-1,j,1) for j in range(7) if j != 2] + [(0,2,1)]
nested = [(1,j,2) for j in seconds]
both = flat + nested
assert len(both) == 14
assert [full(both,0,y,4) for y in range(3)] == [True,True,False]
assert not full(both[:-1],0,1,4)
assert full(nested,2,1,4) and not full(nested,0,1,4)

expanded = ([(-1,j,2) for j in seconds if j not in (2,16)]
            + [(2,j,3) for j in range(2,343,49)] + [(-1,261,3)])
assert len(expanded) == 13 and full(expanded,2,2,4)
assert not full(expanded,2,1,4) and not full(expanded,2,2,3)
print("PASS")
from fractions import Fraction as F
assert F(2,15)+F(1,9)+5*F(1,27)==F(58,135)
assert F(2,3)-F(58,135)-F(2,15)>F(2,45)
assert F(1,3)-(F(1,15)+F(1,9)+3*F(1,27))==F(2,45)

```

### Closing the all-linear case without any depth-five factorization

On the same muted slice, an entirely linear history above 3 yields at most one retained proper ternary cylinder per original rigid source. There is at most one **distinct** first-level guard: row 31 is inactive and row 7 supplies one fixed guard. There is at most one **distinct** second-level guard: row 5167 is inactive and row 19 supplies one fixed guard. In both statements, a shallow original rigid row is excluded by the squarefree cyclotomic inventory, and a contracted shallow source must use a least helper with one of these actual orders. These are upper bounds on positions, not assumptions about independence.

Discard contained and duplicate ternary cylinders. If the remaining cylinders form a full ternary prefix cover, take their full ternary tree. Let \(a\le 1\) be the number of first-level leaves. There are \(3-a\) internal first-level nodes and \(3(3-a)\) second-level nodes. At most one second-level node is a leaf. Therefore there are at least \(1+(3-a)+3(3-a)-1=4(3-a)\ge8\) internal nodes, counting only depths zero through two. A finite full ternary tree with \(I\) internal nodes has \(1+2I\) leaves, so at least **17** source positions are required. In particular the all-linear route with fourteen sources is impossible regardless of the depth-five inventory.

For at most fourteen sources, any first nonlinear projection above 3 has rank at most thirteen. Rank 5 is excluded by the [21-source rank-five bound](GUARDED_RANK_FIVE_SOURCE_BOUND.md); rank 7 is excluded here or by the [earlier rank-seven bound](GUARDED_RANK_SEVEN_SOURCE_BOUND.md); ranks 11 and 13 are ruled out by the [five-guard theorem](FIVE_GUARD_FIRST_NONLINEAR_ESCAPE.md). If there is no such first projection then the rank-three tree bound applies. Combining these with the [exact modulus bridge](EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md), any hypothetical finite all-exponent obstruction needs at least **15 inert primes exceptional to both 3 and 5**. No such obstruction or pointwise solution is asserted.