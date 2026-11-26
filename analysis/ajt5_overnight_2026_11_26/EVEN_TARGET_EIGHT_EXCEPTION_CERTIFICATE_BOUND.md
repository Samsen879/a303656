# Even-target certificates need at least eight exceptional original rows

**The seven-row proof applies separately to a locked parity when the row at \(3\) is inactive. I could not extend it to an arbitrary \(3\)-active parity. But for an even target, a single finite certificate covering both \(c=0,1\) on all their \(2\)-adically allowed parities requires at least eight distinct base-5 exceptional primes.** This strengthens the total bound without assuming seven hard rows on each channel. It applies to finite local certificates in the admitted original-row class. [Seven-row proof](https://github.com/Samsen879/a303656/blob/21ca85cc4eb2058ea165ceedabeb60425532a54d/analysis/c1_seven_prime_audit_phase_b/SEVEN_PRIME_INDEPENDENT_PROOF.md) · [Exactly-seven normal form](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md)

### Why exactly seven fails for even targets

Let \(F\) be the anchor with both \(d\)-parities allowed at \(2\). Let \(G=1-F\), and let \(b\) be the single parity allowed at \(G\). Assume there are exactly seven exceptional primes. On a \(3\)-inactive parity at \(F\), the existing normal form gives seven disjoint order closures. After eliminating their ordinary rows above \(3\), the resulting ternary cylinders have depths \(1,1,2,2,3,3,3\). The depth-one rows are \(7,31\), and the depth-two rows are \(19,5167\).

On another anchor or parity, each of those seven closures gives either one cylinder of its original depth or no cylinder. The closures are disjoint above \(3\), so at each ordinary coordinate there is at most one incoming cylinder and the same exact single-cylinder elimination applies. The surviving depth is the maximum \(3\)-order depth inherited from the closure.

Row \(31\) cannot be active on both anchors because the difference set of \(\{1,5,25\}\bmod31\) omits \(2\). Its closure therefore disappears at \(G\). The other six cylinders have total ternary measure at most \(2/3\), so \(3\) must be active at \(G\). The two anchor residuals differ by \(2\), which makes \(3\) inactive at \(F\) on the **same** parity \(b\). Thus \(b\) is the parity on which the normal form at \(F\) was obtained.

Row \(5167\) also cannot be active on both anchors at the same parity. Neither of its two parity cosets contains a pair differing by \(2\). With \(31\) and \(5167\) gone at \(G\), the depth-two and depth-three cylinders have total measure at most \(1/9+3/27=2/9\). Inside the first ternary branch centered at the logarithm of row \(3\), the exact valuation-\(2\) and valuation-\(4\) shells alone give safe measure \(2/9+2/81\). Hence the depth-one cylinder from row \(7\) must survive at \(G\) and equal that first branch.

The remaining congruences are small. Requiring row \(3\) to be active at \((G,b)\) and at \((F,1-b)\), row \(7\) to be active on both anchors at \(b\), and the two first digits at \(G\) to agree gives exactly these cases.

| \(n\bmod504\) | \(F\) | \(b\) | Row \(7\) first digit at \((F,b)\) | Row \(3\) center digit at \((F,1-b)\) |
|---:|---:|---:|---:|---:|
| \(404\) | \(1\) | even | \(1\) | \(1\) |
| \(482\) | \(0\) | odd | \(1\) | \(1\) |

But row \(7\), of order \(6\), loses its entire cylinder when parity flips at \(F\). The other surviving cylinders retain their original positions and are disjoint from that branch. The table puts the safe center of row \(3\) in precisely the lost branch. So \((F,1-b)\) has an escape, contradicting completeness.

### What transfers to the locked pair

Both shared-parity channels have \(3\) inactive exactly when \(n\equiv6,10,12,16\pmod{24}\). On these classes, the seven-hard-row count applies to each channel taken separately. If an independently proved cofactor restriction leaves at most \(u\) eligible common primes, the two channels then require at least \(14-u\) distinct hard primes. The earlier same-order test supplies such a cap when every proposed shared ratio has order dividing a fixed odd \(K\): the product of the common primes divides \(\big((n-1)^K-(n-3)^K\big)/2\). The repair schedule alone does not force that order restriction. [Shared-parity cofactor test](https://github.com/Samsen879/a303656/blob/76b31c2047e7367df42eb2ed1e7b8b36d367e532/analysis/ajt5_overnight_2026_11_26/FIXED_SMALL_CHANNEL_SHARED_PARITY.md)


The proof uses the sibling-basin conclusions of the pinned exactly-seven normal form; it does not assert they persist for eight or more original rows. On a different channel, a root that ceases to be rigid has no dependent row in any other basin, and its own primary may be repaired. Within any one basin the exact single-cylinder elimination above 3 applies since no other root supplies a seed there. On flipping the parity at fixed \(F\), an original row whose logarithm period is odd keeps its logarithm and valuation data. For an even period it can only disappear. Thus a surviving cylinder cannot move into the centered branch vacated by the order-6 row 7. The two safe shells counted at row 3 have exact valuations two and four; accepting only a subset of the odd valuations cannot make them fatal.

The independent replay verifies the two mod-504 cases, the small-order differences, and the inactive paired residue classes. The eight-prime result is strictly confined to the stated finite admitted original-row class and even targets. It does not prove impossibility for all finite local blockers.

```python
from fractions import Fraction as Q
def index(n,c,b,p):
    ds=[d for d in range(b,6,2) if (n-3**c-pow(5,d,p))%p==0]
    assert len(ds)<=1
    return (ds[0]%3 if ds else None)
out=[]
for n in range(0,504,2):
    F=int(n%4==0)
    G=1-F
    b=int(n%8 in (0,2))
    assert (n-3**G-pow(5,b,8))%8==2
    f7,g7=index(n,F,b,7),index(n,G,b,7)
    cG,cF=index(n,G,b,9),index(n,F,1-b,9)
    if (n-3**G-pow(5,b,3))%3 or (n-3**F-pow(5,1-b,3))%3:
        continue
    if f7 is None or g7 is None or g7!=cG:continue
    out.append((n,F,b,f7,cF))
assert out==[(404,1,0,1,1),(482,0,1,1,1)]
assert 2*Q(1,3)+2*Q(1,9)+3*Q(1,27)==1
assert Q(2,9)+Q(2,81)>Q(1,9)+3*Q(1,27)
assert Q(1,3)+2*Q(1,9)+3*Q(1,27)==Q(2,3)
assert all((x-y)%31!=2 for x in (1,5,25) for y in (1,5,25))
for p,o in ((7,6),(31,3),(19,9),(5167,18)):
    assert pow(5,o,p)==1 and all(pow(5,i,p)!=1 for i in range(1,o))
assert all((pow(5,i,5167)-pow(5,j,5167))%5167!=2
           for b in (0,1) for i in range(b,18,2) for j in range(b,18,2))
off=[]
for n in range(0,24,2):
 b=int(n%8 in (0,2))
 if all((n-3**c-pow(5,b,3))%3 for c in (0,1)):off.append(n)
assert off==[6,10,12,16]
print('OK')
```
