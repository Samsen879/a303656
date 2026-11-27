# Rank-eleven escape through sixteen sources

**A first essential nonlinear projection at 11 cannot complete the selected muted slice with 15 or 16 rigid sources.** At least \(8/135\) of the lower \(3,5\) phase pairs admit an escape through both 7 and 11. Combined with the draft’s other bounds, this leaves first pivot **7** as the remaining case at budgets 15–16. The global bound stays at 15 common exceptional primes. [Integrated fifteen-prime bound](https://github.com/Samsen879/a303656/commit/7e8a1199597c2b27c705b454fdbf497d0d8155c0)

### Why all rank-11 alternatives fit inside six guards and one strip

Fix the same \(n,c\) and parity of \(d\) throughout. Write \(H_{11}\) for row 11’s actual order-five guard. After the higher linear history, let \(t\) sources read 11 and let \(L_1,\ldots,L_\ell\) be the lower-only guards. Essentiality requires \(t\ge11\), so \(\ell\le5\).

Outside \(H_{11}\), a full fibre must be flat. A deeper rigid frontier needs at least \(21\) sources. On \(H_{11}\), row 11 admits the centered simple pair or the basic nested witness with ten second-level side prefixes and one center prefix. The center can be supplied at depth two, or at depth three when valuation 3 is detectable. An expansion of any of those eleven requirements again costs \(21\) sources. Charging the entire strip \(H_{11}\) therefore includes all dynamic alternatives, with their precision and lower guards intact. [Guarded rank-11 rule](https://github.com/Samsen879/a303656/commit/d4491ad99d97b61ea18ce0851a79bb76b206fdae)

If flat support exists, at least \(22-t\ge6\) first branches have a unique source. **Every** flat alternative needs each of those sources. An unrestricted-lower singleton must come from a raw order \(11,22\) or a least helper of one of those orders. The exact products give just three inert candidates, \(23,67,12207031\). Each supplies one first digit at the fixed target. Thus some singleton has a proper lower guard \(G\), and the projected forbidden set is contained in
\[
H_{11}\ \cup\ G\ \cup\ \bigcup_{i=1}^{\ell} L_i.
\]
If flat support is absent, omit \(G\).

### The lower window survives

Let \(X\) consist of the two first ternary branches outside row 7’s actual guard. Let \(Y\) consist of the four first quinary branches outside \(H_{11}\). If either row has an empty guard, discard any one first branch on its axis. On \(X\times Y\), both actual rows are inactive.

The strip \(H_{11}\) is 7-blind. Even before restricting to \(Y\), at most six guards in the overcover can read 7. On \(X\), those guards cannot complete a 7-fibre, since rigid coverage of that fibre needs at least seven prefixes. Thus only the **unchanged 7-blind guards** can forbid a lower pair in \(X\times Y\).

For these \(L_i\), the actual shallow orders give three restrictions.

- A pure first ternary guard is absent. Row 7 is still below the pivot and row 31 is muted.
- Pure first quinary guards and mixed depth-\((1,1)\) guards are absent on \(Y\). Their only possible live shallow head is row 11. Row 71 is muted, and orders \(15,30\) have no inert head.
- Pure second ternary guards all use row 19’s one fixed prefix, since 5167 is muted. Their union has mass at most \(4/45\) in the box. Every other \(L_i\) costs at most \(4/135\). For example, a pure second quinary guard costs at most \(2/75\), and a guard of depths \((2,1)\) costs at most \(1/45\).

Here mass is normalized on the entire lower CRT space. The proper guard \(G\) costs at most \(4/15\) in the box. With at most five \(L_i\), the uncovered mass is therefore at least
\[
\frac{8}{15}-\left(\frac{4}{15}+\frac{4}{45}+4\frac{4}{135}\right)
=\frac{8}{135}.
\]
If the row-19 prefix is absent, charge all five \(L_i\) at the smaller rate. Each uncovered pair lifts first through 7 and then through 11. This bypasses the possible nonlinear projection at 5 by exhibiting lower pairs that survive regardless of which rank-5 alternatives occur elsewhere.

### Inline replay

The replay uses a single represented target with live guards \(H_7=2\bmod3\), \(H_{11}=4\bmod5\), and \(H_{19}=4\bmod9\). The six lower rectangles in the last check are synthetic and attain the \(8/135\) margin in the overcover. The runnable replay checks the same-target guard fixture and the exact margin.

```python
from math import isqrt, prod
from fractions import Fraction as F

for o, value, fs, inert in (
    (11, (5**11-1)//4, (12207031,), {12207031}),
    (22, (5**11+1)//6, (23,67,5281), {23,67}),
):
    assert prod(fs) == value and len(set(fs)) == len(fs)
    assert {q for q in fs if q % 4 == 3} == inert
    for q in fs:
        assert all(q % j for j in range(2,isqrt(q)+1))
        assert pow(5,o,q) == 1 and pow(5,o,q*q) != 1
        assert all(pow(5,j,q) != 1 for j in range(1,o))
assert 22-16 == 6 > 3

P = 8*3*7*19*31*71*5167*19531
u,v = (a + P*((2-a)*pow(P,-1,11) % 11) for a in (3,8))
n = 3 + 1 + u*u + v*v

def guard(q,o):
    odd = o//(2 if o % 2 == 0 else 1)
    return {d % odd for d in range(0,2*o,2)
            if (n-3-pow(5,d,q)) % q == 0}

assert (guard(7,6),guard(11,5),guard(19,9)) == ({2},{4},{4})
assert all(not guard(q,o) for q,o in ((3,2),(31,3),(71,5),(5167,18),(19531,7)))

box = {(x,y) for x in range(27) for y in range(5) if x%3 != 2 and y != 4}
holes = {(x,y) for x,y in box if x%3 != 0 and x%9 != 4 and x not in (1,7,10,19)}
assert len(box) == 72 and holes == {(x,y) for x in (16,25) for y in range(4)}
assert F(len(holes),135) == F(8,15)-F(4,15)-F(4,45)-4*F(4,135)
print("PASS")
I=1
history=[I]
for leaves in (1,1,6,4):
    I=3*I-leaves
    history.append(I)
assert history==[1,2,5,9,23] and 1+2*sum(history)==81

```

### A separate lower bound for all-linear covers

With the actual inventories at the first four ternary depths on this slice, the number of distinct leaves at these depths is bounded by \((1,1,6,4)\); see the [certified depth-four inventory](GUARDED_RANK_ELEVEN_SOURCE_BOUND.md). An entirely linear history cannot increase the number of sources. In a hypothetical full ternary cover, after discarding contained and duplicate cylinders, let \(I_j\) be the number of internal nodes at depth \(j\) and \(L_j\) the number of leaves there. With \(I_0=1\), the recursion is \(I_j=3I_{j-1}-L_j\). Thus \(I_1,I_2,I_3,I_4\) are at least \(2,5,9,23\), respectively, so the full tree has at least \(1+2(1+2+5+9+23)=81\) leaves. This bound is for the all-linear case only; it leaves rank 7 at 15–16 sources unresolved.