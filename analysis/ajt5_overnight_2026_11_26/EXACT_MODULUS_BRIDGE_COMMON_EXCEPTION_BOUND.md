# Exact modulus bridge and a common-exception necessary bound

**The modulus bridge is exact. It also gives a stronger necessary condition. Any finite all-exponent obstruction in the sense of \(f108fd3\) must contain at least eight inert primes that are Wieferich to both bases \(3\) and \(5\).** In particular, if its modulus has exactly eight exceptional base-\(5\) primes, all eight must also be exceptional to base \(3\). This is a condition on a hypothetical obstruction. [All-exponent obstruction definition](https://github.com/Samsen879/a303656/blob/f108fd396480eaa4524b7aeea6d4dda794a7561c/analysis/ajt5_overnight_2026_11_26/EXACT_DENSITY_ALL_EXPONENTS.md) · [Four-anchor bound](https://github.com/Samsen879/a303656/blob/a2386de11cf3ed911d4c1cbbfdf4cf4a035c630c/analysis/ajt5_overnight_2026_11_26/FOUR_ANCHOR_EIGHT_EXCEPTION_CERTIFICATE_BOUND.md)

### Exact translation

Factor the witness modulus as \(M=\prod p^{e_p}\). CRT identifies the square-sum residues modulo \(M\) with the product of the square-sum residues modulo its prime powers. The two square coordinates can be joined by CRT separately.

| Factor | Exact local rule |
|---|---|
| \(p\equiv1\pmod4\) | Every residue passes, including at \(5\). |
| \(p\equiv3\pmod4\) | A nonzero residue fails exactly when its valuation below \(e_p\) is odd. Zero passes. The factor contributes no test if \(e_p=1\). |
| \(2^{e_2}\) | A nonzero residue fails when \(v_2\le e_2-2\) and its odd part is \(3\bmod4\). Zero and the top valuation \(e_2-1\) pass. |

For an inert prime, a unit is a square sum modulo \(p\) and lifts with a nonzero derivative in one coordinate. Removing square powers of \(p\) gives the even-valuation criterion. At \(2\), a unit \(1\bmod4\) is a square or four plus a square in \(\mathbb Z_2\), and \(2\) is a Gaussian norm. The top valuation has a norm representative \(2^{e_2-1}\). These rules give one admitted row per relevant prime, with the original shared residue of \(n\).

The coarse-step quantifiers also agree. On fixing \(d\) modulo the lcm of the odd row orders modulo their primes and the full \(2\)-adic period, any remaining \(p\)-primary digits affect only row \(p\). If each row has a safe lift, CRT joins those lifts into one safe \(d\). The translation therefore preserves the same \(n\) and every fixed-\(c\) phase, including the small exponents. No extra hypothesis on \(M\) is needed.

### Why eight primes must be exceptional to both bases

The structural input is a fixed-slice consequence of the seven-source proof. **With rows \(3\) and \(31\) inactive, a fixed-\(c\), fixed-parity cover needs at least eight rigid seeds.** Here a rigid seed is a collision class carrying an accepted odd valuation below \(v_p(5^{\operatorname{ord}_p(5)}-1)\). This counts rigid seeds on that slice. Other exceptional rows may still act as dynamic helpers.

The proof of the normal form uses this seed count directly. With at most seven seeds, elimination at primes at least \(11\) is linear and creates at most one descendant per seed. The rank-\(7\) and rank-\(5\) exclusions use the same seven-source budget and the actual small-order inventories, even if some helpers are nonregular. The resulting cover at \(3\) would have to contain the two depth-one leaves from \(7\) and \(31\). An inactive row \(31\) removes the second leaf. [Sparse elimination and ranks \(5,7,3\)](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md)

Now choose \(c\bmod30\) with the parity that allows both \(d\)-parities at \(2\), and with row \(31\) inactive. This is always possible. The order of \(3\bmod31\) is \(30\), so the prescribed parity gives fifteen values of \(3^c\bmod31\), and at most three put \(n-3^c\) in \(\{1,5,25\}\).

Process the base-\(5\) exceptional primes with ordinary base-\(3\) lifts in increasing order. At \(q\), keep \(c\bmod30\), the previous rows modulo their prime cubes, and \(3^c\bmod q\) fixed. The step used to vary \(c\) is prime to \(q\), since the previously fixed prime-power orders only involve smaller primes. If \(e\) is the base-\(5\) collision log modulo \(q\), the ordinary base-\(3\) lift lets us arrange
\[
n-3^c-5^e\equiv q^2\pmod{q^3}.
\]
This removes the rigid seed at \(q\). If the base-\(5\) lifting depth is two, the row can remain dynamic. If its lifting depth is greater, the residual has the fixed even valuation two. A row with no collision modulo \(q\) already has no seed.

Finally choose the \(d\)-parity on which row \(3\) is inactive. Row \(31\) is still inactive, and every remaining rigid seed belongs to a prime exceptional to both bases. The fixed-slice bound requires eight such seeds on this one slice.

### Same-target check

Take \(n=840955481=3+5^4+13038^2+25903^2\), \(q=20771\), and \(r=40487\). Both primes are exceptional to base \(5\) and ordinary to base \(3\). At the collision log \(d=0\), successive changes of \(c\) give these residuals modulo \(q^3\) and \(r^3\).

| \(c\) | Modulo \(q^3\) | Modulo \(r^3\) |
|---:|---:|---:|
| \(1\) | \(qr\) | \(qr\) |
| \(14781263025780811\) | \(q^2\) | \(6138091353325\), valuation \(1\) |
| \(17620428032262670841383591\) | \(q^2\) | \(r^2\) |

All three exponents are \(1\bmod30\), and \(n-3^c\equiv2\bmod31\) throughout. The second lift preserves the first one.


The sparse-elimination argument is about the rigid-source count on the chosen slice, not the total number of rows that are nonordinary to base 5. A row which becomes dynamic there obeys the same one-parity shell condition and can serve as a helper; it adds no rigid seed. The rank-five and rank-seven exclusions only use the number of initial seeds, their fixed predecessors, and actual shallow-order inventories. They do not require helpers to be ordinary on both bases. The proof is an alternative modulo-obstruction bridge; it makes no claim of improving the separate unrestricted ten-target bound.

The independent replay checks exact local square-sum rules on six prime powers and a composite modulus, the mod-31 choice for every residue and parity, and the displayed two simultaneous-preserving lifts. It does not provide a finite all-exponent obstruction.

```python
from itertools import product
from math import prod
def accepted(x,p,e):
    m=p**e
    x%=m
    if not x or p%4==1:return True
    v=0
    while x%p==0:
        x//=p;v+=1
    return (v>=e-1 or x%4==1) if p==2 else v%2==0
for p,e in ((2,2),(2,5),(3,3),(7,2),(5,2),(13,2)):
    m=p**e
    sq={x*x%m for x in range(m)}
    N={(a+b)%m for a,b in product(sq,repeat=2)}
    assert N=={x for x in range(m) if accepted(x,p,e)}
M=2**4*3**2*5
sq={a*a%M for a in range(M)}
R={(a+b)%M for a,b in product(sq,repeat=2)}
assert R=={x for x in range(M) if all(accepted(x,p,e) for p,e in ((2,4),(3,2),(5,1)))}
assert len({pow(3,c,31) for c in range(30)})==30
assert {pow(5,d,31) for d in range(3)}=={1,5,25}
for n in range(31):
    for b in range(2):
        assert sum((n-pow(3,c,31))%31 not in (1,5,25) for c in range(b,30,2))>=12
n=840955481
q,r=20771,40487
assert n==3+5**4+13038**2+25903**2
for p in (q,r):
    assert pow(5,p-1,p*p)==1 and pow(3,p-1,p*p)!=1
for c,u,v in ((1,q*r,q*r),(14781263025780811,q*q,6138091353325),
              (17620428032262670841383591,q*q,r*r)):
    assert c%30==1 and (n-pow(3,c,31))%31==2
    assert ((n-pow(3,c,q**3)-1)%q**3,(n-pow(3,c,r**3)-1)%r**3)==(u,v)
print("OK")
```
