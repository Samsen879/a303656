# Guarded rank-seven exclusion and an eleven-common-prime necessary condition

**A first essential nonlinear elimination at \(7\) cannot complete the muted slice with ten rigid sources. The exclusion holds through twelve.** The proof counts every live flat or nested witness and every centered simple pair. It allows the lower guards to have different depths in the \(3\)- and \(5\)-coordinates. [Muted slice and rank-five result](https://github.com/Samsen879/a303656/blob/9c2a6653449ff0016adb4b782b9db848c6227844/analysis/ajt5_overnight_2026_11_26/GUARDED_RANK_FIVE_SOURCE_BOUND.md)

### Exact rank-seven rule

After the linear higher steps, each surviving source has one fixed lower guard \(C_3\times C_5\) and one \(7\)-prefix. Let \(L\) be the union of guards of sources that do not read \(7\). Row \(7\) has exact base-\(5\) order \(6\) and lifting depth one. On the chosen parity, its guard \(H\) is either empty or one first ternary branch. When active, let \(u,v,w\) be the residues of its exponent center modulo \(7,49,343\).

Outside \(L\), the full-fibre rule through twelve sources has three alternatives.

- **Flat.** There is a live first-level source in every one of the seven branches. A deeper complete prefix tree would need at least thirteen leaves.
- **Simple pair on \(H\).** A live first-level source occupies \(u\). Row \(7\) rejects all other first branches.
- **Nested on \(H\).** Each of the six second-level branches inside \(u\) other than \(v\) has a live second-level source. The center is supplied by a live source at \(v\), or, when valuation \(3\) is detected, by a live third-level source at \(w\).

For the nested rule, the six side branches have valuation \(2\) throughout. Replacing one second-level source with deeper sources would cost seven in that branch, five for the other side branches, and one for the center. The same thirteen-source obstruction applies inside the center when its required prefix is missing. At precision at most \(3\), the branch \(v\) is entirely safe. At precision at least \(4\), row \(7\) rejects the six third-level siblings of \(w\), while the next shell and the center are safe.

Each flat or nested witness takes an **intersection** of seven live lower guards, and the elimination takes the union of all those intersections. With ten sources there are at most \(2^3=8\) alternatives of either shape. Flat and nested support in the same ledger would require fourteen sources because their prefixes have different depths. The simple pairs are counted separately. There can be at most four with a flat witness, or three with a nested witness, and all are confined to \(H\).

### Why the lower cover fails

The higher history is linear, so a source’s least helper can read only the odd coordinates still present in its guard. A smaller factor already eliminated would have required a still smaller helper. This gives the following restrictions from the actual orders. [Exact-order inventories](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md)

- A first-level \(7\)-source with an unrestricted lower guard would need a raw rigid order \(7\) or \(14\), or a least helper of one of those orders. The squarefree products \(\Phi_7(5)=19531\) and \(\Phi_{14}(5)=29\cdot449\) rule out the raw case. The sole inert helper \(19531\) is muted.
- Among lower-only sources, the first-level \(5\)-strips and the mixed guards of depths \((1,1)\) all lie in the **same** \(5\)-strip, supplied by \(11\). Row \(71\) is muted, orders \(15,30\) have no inert helper, and row \(7\) has yet to be eliminated. The latter fact, together with muting \(31\), also excludes pure first-level ternary guards.
- The pure depth-two ternary guards all lie in the one guard of \(19\), since \(5167\) is muted. All remaining lower-only guards have measure at most \(1/27\) outside \(H\) when \(H\) is active. This includes pure depth-two \(5\)-guards, whose measure there is at most \(2/75\).

An essential witness uses at least seven top sources, leaving at most five lower-only sources. If \(H\) is active, put \(W=H^c\). For any first ternary branch \(B\subset W\),
\[
\mu(L\cap W)\le \frac{2}{15}+\frac19+\frac3{27}=\frac{16}{45},
\qquad
\mu(L\cap B)\le \frac1{15}+\frac19+\frac3{27}=\frac{13}{45}.
\]

A nested witness without a flat witness leaves all of \(W\) to \(L\), which fails the first bound. If flat witnesses exist, one of the seven first branches has exactly one candidate source because there are fewer than fourteen sources. Its lower guard \(G\) is therefore required by **every** flat alternative. On \(W\), completeness requires \(W\subseteq L\cup G\), so \(\mu(G\cap W)\ge14/45>1/5\). The only proper product guard that large is a whole first ternary branch. The other branch \(B\subset W\) would then have to lie in \(L\), contradicting \(13/45<1/3\). If \(H\) is empty, the same singleton argument gives \(\mu(L\cup G)\le1/5+1/9+3/25+1/3<1\).

Together with the rank-five exclusion, this also rules out a ten-source cover on the selected slice. The ranks at least \(11\) are linear by sparsity. If the reductions remain linear down to \(3\), at most one first ternary leaf is available, so a full tree with at most ten leaves has depth at most three. The available guards at those depths have total measure at most \(1/3+1/9+6/27=2/3\). Thus the finite all-exponent route requires **at least eleven common exceptional primes**.

### Runnable replay

This uses the actual row \(7\) at the represented target \(77=3+1+3^2+8^2\), with \(c=1\) and even \(d\). The source guards in the two test ledgers are synthetic. The nested test disappears at precision \(7^3\), where valuation \(3\) is unresolved.

```python
from fractions import Fraction as F

# Each tuple is one source: (3-residue, depth, 5-residue, depth, 7-residue, depth).
def check(rows, K=4):
    result = set()
    for x in range(9):
        for y in range(5):
            live = [(j,g) for a,e,b,f,j,g in rows
                    if (x-a)%3**e == (y-b)%5**f == 0]
            flat = all((j,1) in live for j in range(7))
            nested = (all((j,2) in live for j in range(2,49,7) if j != 16)
                      and ((16,2) in live or K >= 4 and (261,3) in live))
            rule = (0,0) in live or flat or x%3 == 2 and ((2,1) in live or nested)

            def bad(z):
                d = z + 343*((-2*x-z)%6)  # even d with d=x mod 3
                r = (74-pow(5,d,7**K)) % 7**K
                row7 = r != 0 and r%7 == 0 and (r%49 != 0 or r%343 == 0)
                return row7 or any((z-j)%7**g == 0 for j,g in live)

            assert rule == all(bad(z) for z in range(343))
            if rule:
                result.add((x,y))
    return result

flat = [(0,1,1,1,j,1) for j in range(7)]
flat += [(2,1,2,1,j,1) for j in (0,1,2)]
assert check(flat) == {(x,1) for x in (0,3,6)} | {(x,2) for x in (2,5,8)}

sides = [(2,1,1,1,j,2) for j in range(2,49,7) if j != 16]
simple = [(2,1,2,1,2,1)]
centre = [(2,1,1,1,261,3)]
assert check(sides+simple+centre) == {(x,y) for x in (2,5,8) for y in (1,2)}
assert check(sides+simple+centre, 3) == {(x,2) for x in (2,5,8)}
assert check(sides+simple+[(2,1,4,1,261,3)]) == check(simple)

assert (74-pow(5,1976,2401)) % 2401 == 0
assert F(2,15)+F(1,9)+3*F(1,27) < F(2,3)-F(1,5)
assert F(1,15)+F(1,9)+3*F(1,27) < F(1,3)
from math import isqrt
for p, e in ((19531,7),(29,14),(449,14)):
    assert all(p%i for i in range(2,isqrt(p)+1))
    assert next(d for d in range(1,e+1) if pow(5,d,p)==1)==e
assert (5**7-1)//4==19531 and (5**7+1)//6==29*449
assert pow(5,6,7)==1 and pow(5,6,49)!=1
print("OK")
```

The eleven-prime consequence concerns a hypothetical finite all-exponent obstruction, using the exact local norm rules and singly exceptional muting from [the modulus bridge](EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md). It is not a search for eleven primes, does not establish an obstruction, and does not improve the numerical density bound. The rank-seven and rank-five exclusions concern a first nonlinear step after higher linear projections, not arbitrary histories containing other prior nonlinear projections.
