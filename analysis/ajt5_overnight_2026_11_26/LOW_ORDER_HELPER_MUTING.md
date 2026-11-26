# Simultaneous muting of low-order helpers at a fixed target

On the positive-\(c\), fixed-\(d\)-parity slice in the [exact modulus bridge](EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md), it is possible to keep rows \(3,31\) inactive and also keep \(5167,71,19531\) units before and during the singly exceptional base-3 adjustments. All row statements are for the same target \(n\).

Start with a suitable \(c\bmod30\) and fixed parity \(b\) of \(d\) from the bridge, and choose any refinement modulo \(90\). With the other digits in the relevant orders fixed, choose the following digits in order.

| Row \(p\) | \(\operatorname{ord}_p(3)\) | Fresh digit of \(c\) | Values of \(3^c\) | Values of \(5^d\), \(d\equiv b\bmod2\) |
|---:|---:|---:|---:|---:|
| 5167 | \(18\cdot41\) | \(41\) | 41 | 9 |
| 71 | \(5\cdot7\) | \(7\) | 7 | 5 |
| 19531 | \(30\cdot7\cdot31\) | \(31\) | 31 | 7 |

The table follows from the exact base-3 order and the order of \(25\). The number of forbidden distinct values of \(3^c\) is at most the size of the parity coset of \(5^d\); at each step there is a strictly larger number of possible \(3^c\) values. CRT preserves all earlier digits. This reserves a class modulo \(800730=2\cdot3^2\cdot5\cdot7\cdot31\cdot41\). Its inert prime factors \(3,7,31\) are ordinary to base \(5\). Thus at any inert base-5 exceptional prime used by the muting proof, the new reservation still has period prime to the lifting prime. Keeping the successive old prime-cube orders in the bridge does not change that, since their prime factors are smaller.

For the same target \(2045=3+1+4^2+45^2\), rows \(5167,71\) have valuation-one collisions at \(c=1\) on even \(d\); \(c=91\) makes all three tabulated rows units for all even \(d\). The next low row does not admit a blanket argument of this kind: for \(n=77=3+1+3^2+8^2\), all odd \(c\) have some collision at row \(7\) on even \(d\). These are congruence claims; they are not statements of nonrepresentation at either \(n\).

This note gives a uniform input restriction on the order elimination. It does not claim a new seed threshold, a nonlinear-pivot classification, or a numerical density improvement.

```python
from math import lcm,isqrt
def order(a,p):
    x=a%p;k=1
    while x!=1:
        x=x*a%p;k+=1
    return k
rows=((5167,738,9),(71,35,5),(19531,6510,7))
assert lcm(90,*(a for _,a,_ in rows))==800730
for p,a,b in rows:
    assert all(p%j for j in range(2,isqrt(p)+1))
    assert order(3,p)==a and order(25,p)==b
for p in (3,7,31):
    assert pow(5,p-1,p*p)!=1
for p,_,b in rows:
    assert all((2045-pow(3,91,p)-pow(5,d,p))%p for d in range(0,2*b,2))
for p,_,b in rows[:2]:
    assert any((2045-pow(3,1,p*p)-pow(5,d,p*p))%(p*p) in range(p,p*p,p) for d in range(0,2*b,2))
assert all((-pow(3,c,7))%7 in {pow(5,d,7) for d in (0,2,4)} for c in (1,3,5))
print("OK")
```
