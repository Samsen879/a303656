# Torsion phase survival and resonant pruning

**There is a survivor bound that allows the higher producer digits to be chosen separately at each phase.** A shallow lower row with mismatched characters can prune only a few phases. A resonant lower row can prune almost all of them. In a real \(7\to7603\) handoff, row 379 leaves one of seven phases. A shift at the **same target** makes it remove all seven, while preserving the producer repairs and the receiving torsion family.

### A lower bound after pruning

Fix the target and the tail \(c\ge v_3(M)\). Start with a full first repair line at a doubly ordinary producer \(p\). Open all higher \(p\)-primary digits, preserving the other primary coordinates in the full exponent periods. Assume the receiving row \(R\) reads only the first \(p\)-digit, so choosing deeper producer lifts preserves its inherited order-\(p\) family. The gates in this bound are rows unchanged when \(R\) is opened. Rows that read \(R\) remain on the receiving side of the charge. [Branching charge baseline](https://github.com/Samsen879/a303656/commit/66b0b68c6f3fa63601d890dbb43442b6be45885e)

A row with **no \(p\)-digit in either full order** is constant at its full modulus. The pure \(p\)-steps are multiples of both row orders. Such a row passes throughout if it passes at one phase.

For a shallow row \(\ell\), write the two powers along the line as \(U\alpha^t,V\gamma^t\), with characters of order dividing \(p\). Count an exact veto only at an odd valuation below the row precision. The following collision bounds are conservative.

- A single moving character gives at most one collision. Two distinct nontrivial characters also give at most one when \(n\equiv0\pmod\ell\).
- For distinct nontrivial characters and \(n\not\equiv0\pmod\ell\), if there are \(b\) collisions, then \(b(b-1)\le p-1\). Two collisions at a given nonzero ordered separation determine the two power values by an invertible two-by-two system. Either power then identifies the first phase.
- Matching nontrivial characters give at most one collision unless \(n\equiv U+V\equiv0\pmod\ell\). In that resonant case all phases collide. At full precision the residual is \(n-(U+V)\alpha^t\). At equal odd valuation of \(n\) and \(U+V\), all but at most one phase veto. The exceptional phase can be zero, have even valuation, or still veto at a higher odd valuation.

Let \(F\) be the **union** of the exact shallow veto sets. Write \(\theta\) for the producer’s passing fraction among higher lifts at a first repair point. At precision two or three \(\theta=1\). At higher precision \(\theta>1-1/p\), from the valuation-two lifts and the zero class. A deeper gate \(\ell\) of maximum read depth \(D_\ell\) can veto at most \(p^{1-D_\ell}\) of a first point’s lifts. Holding the other axis fixed, collision restricts the deeper axis to at most one residue class. Thus a usable bound is
\[
k\ \ge\
\#\left\{t\notin F:
\sum_{\substack{\ell\ {\rm deep}\\ \text{can veto above }t}}
 p^{1-D_\ell}<\theta
\right\}.
\]
In particular, with fewer than \(p\) deep gates, **every first phase outside \(F\) has a passing lift**. This lets the receiving charge use a certified lower bound on \(k\), even when the lifted exponents differ between phases.

### Real pruning and row reuse

At \(n=162032070120662\), use the square-precision rows \(7,379,7603\). All seven producer phases pass \(7^2\), and the receiving residual is exactly \(7603\) on each. Row 379 collides modulo 379 on all seven, but its exact residual is \(379(1-T)\bmod379^2\). Six phases veto and \(T=1\) passes with residual zero. At the alternate anchor, all seven residuals equal 379. The target and orders are unchanged. The replay also includes \(31^3\), whose residual is constant because neither base order reads a 7-digit.

For accounting, key each row by its prime and each veto by the full physical exponent phase. Take the union of vetoes before deleting phases. A deleted phase creates no receiving-side repair demand. Across branches, a row may act in different roles, so lower bounds on row counts cannot be added without proving the rows distinct. The linked branching baseline supplies a row-431 example: a reader of 43 becomes a frozen gate when 98299 is opened.

```python
from itertools import product
from math import gcd, lcm

q,R = 379,7603
n = 162032070120662
c,C = 192727451007,295723497699
P = lcm(6,54*q,1086*R)
J = lcm(42,378*q,R-1)

def r(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

for m in (q*q,R*R):
    T=pow(3,P,m)
    assert T==pow(5,P,m) and T!=1 and pow(T,7,m)==1
assert all(pow(a,J,m)==1 for a in (3,5) for m in (49,q*q))
for start,S,wanted in ((c,q,[0]),(C,0,[])):
    assert r(start,P,49)==35 and r(start,P,q*q)%q and r(start,P,R*R)%R
    for x,y in product(range(7),repeat=2):
        assert (r(start+P*x,P*y,49)==0)==(x==y)
    good=[]
    for t in range(7):
        z=r(start+P*t,P*t,q*q)
        assert z==(q-S*pow(3,P*t,q*q))%(q*q) and z%q==0
        assert r(start+P*t,P*t,R*R)==R
        if z==0:
            good.append(t)
    assert good==wanted
I=lcm(P,30*31**2)
assert gcd(I,7)==1 and all(pow(a,I,31**3)==1 for a in (3,5))
assert {r(c+I*t,I*t,31**3) for t in range(7)}=={19049}
assert [r(c,4628*J,m) for m in (49,q*q,R*R)]==[0,0,0]
print("PASS")
```

The bound applies to a full opened producer chart. The real example rules out a uniformly positive survivor count from the torsion order alone. A global application would need to control resonant lower gates or prove that a minimal obstruction supplies a chart where enough phases survive. Moving \(c\) at small exponents still requires checking the ternary row separately.

The row-pruning argument counts a phase once even if multiple lower tests reject it. It assumes the full-period primary opening is legal and gives no unconditional count of admissible phases in an arbitrary minimal obstruction.
