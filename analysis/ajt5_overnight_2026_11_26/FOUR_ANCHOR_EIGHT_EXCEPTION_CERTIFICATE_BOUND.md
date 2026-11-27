# Four fixed anchors exclude every seven-exception certificate

**The eight-exception bound extends to every odd target.** In fact, for any integer \(n\), a finite local certificate in the admitted original-row class needs at least eight distinct base-5 exceptional primes if it covers every \(d\)-phase at the following two anchors.

| \(n\bmod4\) | Required anchors |
|---|---|
| \(2,3\) | \(c=0,2\) |
| \(0,1\) | \(c=1,3\) |

Thus every finite all-exponent blocker in this class needs at least eight, with no restriction on the parity of \(n\). This uses the verified exactly-seven normal form. [Exactly-seven normal form](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md) · [Previous even-target result](https://github.com/Samsen879/a303656/blob/28a9a12ead83cd9dd42d2856d7ed73736a1403b1/analysis/ajt5_overnight_2026_11_26/EVEN_TARGET_EIGHT_EXCEPTION_CERTIFICATE_BOUND.md)

**Both \(d\)-parities are available at each listed anchor.** Put \(A=n-3^c\). Then \(A\equiv1\pmod4\) for even \(n\) and \(A\equiv2\pmod4\) for odd \(n\). For either prescribed parity \(b\), choose a two-square value \(T\) from \(\{0,4\}\) or \(\{1,5\}\), respectively, so that \(A-T\equiv5^b\pmod8\). Powers of \(5\) with parity \(b\) attain every lift of this unit modulo \(2^k\). The odd row periods read at most the parity of \(d\), so choosing the higher binary digits preserves all odd row tests.

To apply the original \(c=0,1\) normal form at a higher fixed anchor \(C\), shift every odd row residue by \(1-3^C\) and set the auxiliary target to \(3\bmod4\) by CRT. At auxiliary \(c=0\) the odd residuals are the original ones at \(C\). At auxiliary \(c=1\) every residual is \(3\bmod4\). Thus coverage at \(C\) on both parities gives a complete auxiliary \(c=0,1\) certificate with the same exceptional primes. With exactly seven, the parity where row \(3\) is inactive must have distinct depth-one ternary leaves from rows \(7,31\), and a depth-two leaf from \(5167\) below neither. [Seven-row proof](https://github.com/Samsen879/a303656/blob/21ca85cc4eb2058ea165ceedabeb60425532a54d/analysis/c1_seven_prime_audit_phase_b/SEVEN_PRIME_INDEPENDENT_PROOF.md)

- **At \(c=0,2\)**, row \(31\) must be active at both anchors. That would require two elements of \(\langle5\rangle\bmod31=\{1,5,25\}\) to differ by \(9-1=8\). No such pair exists.
- **At \(c=1,3\)**, the same parity can be chosen to make row \(3\) inactive at both anchors, since both powers of \(3\) vanish modulo \(3\). The actual difference is \(27-3=24\). For even \(d\), the paired logs at rows \(31\) and \(7\) both give first ternary digits \((2,0)\) across the two anchors, so the required depth-one leaves coincide. For odd \(d\), row \(7\) gives digits \((0,2)\); the only paired odd logs at \(5167\) are \((9,11)\), giving those same first digits. Its depth-two leaf therefore lies inside the row-\(7\) depth-one leaf.


The auxiliary row shift is explicit: at an odd modulus the residue becomes \(r_q+1-3^C\); CRT combines the shifted odd residues with an auxiliary two-adic residue congruent to 3 mod 4. The latter blocks \(c=1\) at every exponent parity, while the \(c=0\) odd subsystem is the original fixed anchor. This is only an invocation of the pinned admitted-class normal form, not a new unrestricted modulus theorem.

The independent replay verifies all required parity options and exact paired logarithms; it does not claim that any real prime family blocks the original conjecture.

```python
from itertools import product
def logs(p,o,b,diff):
    return [(i,j) for i,j in product(range(o),repeat=2)
            if (o%2 or i%2==j%2==b) and (pow(5,i,p)-pow(5,j,p))%p==diff%p]
assert not logs(31,3,0,8)
for n in range(32):
    anchors=(0,2) if n%4 in (2,3) else (1,3)
    for c in anchors:
        A=n-3**c
        ts=(1,5) if n%2 else (0,4)
        for b in range(2): assert any((A-t-pow(5,b,8))%8==0 for t in ts)
assert logs(31,3,0,24)==[(2,0)]
assert [(i%3,j%3) for i,j in logs(7,6,0,24)]==[(2,0)]
assert [(i%3,j%3) for i,j in logs(7,6,1,24)]==[(0,2)]
assert logs(5167,18,1,24)==[(9,11)]
for p,o in ((7,6),(31,3),(5167,18)):
    assert pow(5,o,p)==1 and all(pow(5,i,p)!=1 for i in range(1,o))
print("OK")
```
