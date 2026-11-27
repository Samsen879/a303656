# Signed targets passing every modulus and unit-signature exclusions

**No finite tail modulus obstructs any target \(n=5^D-1\), \(D\ge1\).** This family contains targets with exact valuation one at actual doubly ordinary primes, including \(6823\), where an exponent pair can trigger a genuine odd-valuation veto. Divisibility and an active veto therefore do not by themselves force a gate into a minimal obstruction.

There is also a new restriction on the eighteen-source bound. For \(n\equiv2,3,6,11\pmod{12}\), all eighteen required common Wieferich sources can be required to be **coprime to \(n\)**.

### Excluding the signed targets

More generally, suppose
\[
n=5^{d_0}+3^{c_0}-S>1,\qquad S=x^2+y^2,\qquad 4\mid S,
\]
and \(n-5^{d_0}\) is zero or has even \(3\)-adic valuation. For **every** finite modulus \(M\) and threshold \(A\), there is a \(c\ge A\) for which \(n-3^c-5^{d_0}\) is a sum of two squares modulo \(M\).

To see this, take \(L\) to be the lcm of \(2\) and the orders of \(3\) at the inert prime-power factors of \(M\) above \(3\). Each of those orders has binary valuation at most one, so \(v_2(L)=1\). On \(c=c_0+Lj\), the residual remains \(-S\) at those odd factors and passes their valuation tests. Split factors always pass. Take \(c\ge v_3(M)\) to use the hypothesis at \(3\). At the binary factor, \(3^L\) generates the units congruent to \(1\bmod8\), by \(v_2(3^L-1)=3\). Thus the residual can be set to \(0\) or \(4\), whichever is congruent to \(-S\bmod8\). The chosen exponent class contains arbitrarily large \(c\), and CRT joins the square coordinates.

Take \(c_0=1,\ S=4,\ d_0=D\) to obtain \(n=5^D-1\). The residual for this fixed \(d_0\) is always the negative integer \(-1-3^c\). The construction therefore gives modular witnesses at every precision without claiming an integer representation from that column.

For any inert prime \(q>3\) ordinary to base \(5\), if \(w_q=\operatorname{ord}_q(5)\) divides \(D\), LTE gives \(v_q(5^D-1)=1+v_q(D)\). For a finite set of such primes, simultaneous valuation one is possible in this family exactly when no selected prime divides the base-5 order of another. The actual orders \(6,29,2274\) at \(7,59,6823\) give simultaneous valuation one at \(D=65946\). By contrast, \(\operatorname{ord}_{43}(5)=42\), so simultaneous divisibility by \(7,43\) in this family forces \(v_7(n)\ge2\).

### What the target signature can force

For an inert \(q>3\) dividing \(n\), let \(\chi_a=(a/q)\). On a prescribed parity pair \((b_c,b_d)\), a collision modulo \(q\) is possible exactly when
\[
\chi_3^{b_c}\chi_5^{b_d}=-1.
\]
Necessity follows by taking characters in \(3^c=-5^d\bmod q\). For sufficiency, \((q-1)/2\) is odd, so each power orbit with prescribed parity contains the sign \(\chi_a^{b}\) itself. In particular, for \(q\equiv11,59\pmod{60}\) both signs are positive for all exponents. Whenever such a \(q\) divides \(n\), its row is a unit everywhere and is absent from every divisor-minimal obstruction.

An opposite-sign parity allows a collision, but exact valuation still depends on the primary digits. At a collision put \(u=3^c\bmod q\) and \(\lambda_a=-(a^{q-1}-1)/q\bmod q\). Lifting the two opposite roots of unity modulo \(q^2\) gives
\[
\frac{n-3^c-5^d}{q}\equiv
\frac nq-u(\lambda_3c-\lambda_5d)\pmod q.
\]
An unread ordinary digit can set this expression to zero. A retained gate needs the order constraints from the other rows to prevent the repairs that would pass the whole panel. For example, at \(n=15624=5^6-1\), \((c,d)=(1,2)\) gives residual \(14\bmod49\), while \((1,20)\) repairs the same collision. The all-modulus argument above applies to this very target.

The sign test also enlarges the previous zero-seed set \(Z\). On the selected eighteen-source slice, adjoin every common prime dividing \(n\) for which the sign product is \(+1\). These rows are units on that slice regardless of their target valuation. For \(n\equiv2,3,6,11\pmod{12}\), the published muting schedule can use even \(c\) and even \(d\), so **every** common prime dividing \(n\) is excluded from the eighteen-source count. This sign exclusion is slice-specific. A row muted by parity can still be essential on a different parity, so the precision and terminal conclusions for the old valuation-defined \(Z\) do not automatically extend to it. [Target-adjusted eighteen-source theorem](https://github.com/Samsen879/a303656/commit/6fc94d72fc9c2b4728ef0ecae5a2146552ed2ef3)

### Replay

The standalone checker verifies the exact orders, both kinds of signature, and joins square coordinates on a composite panel.

```python
from math import lcm

assert (15624-3-pow(5,2,49)) % 49 == 14
assert (15624-3-pow(5,20,49)) % 49 == 0
assert pow(3,29,59) == pow(5,29,59) == 1

D = lcm(6,29,2274)
assert D == 65946
for q in (7,59,6823):
    assert (pow(5,D,q*q)-1) % q == 0
    assert pow(5,D,q*q) != 1

q = 6823
r = (pow(5,2274,q*q)-1-pow(3,3411,q*q)-1) % (q*q)
assert r == 960*q

M = 2**12 * 3**5 * 5**2 * 7**2 * 19**4 * 59**2 * 6823**2
c = 2856383663689615627
a, b = 8699954787926937336233986, 107682670830938563887104
assert (a*a+b*b+1+pow(3,c,M)) % M == 0
```

These results exclude finite obstructions for the signed family and restrict the sources for the four residue classes. They leave open whether an arbitrary hypothetical obstruction must contain some ordinary valuation-one gate.

In the signed criterion \(c_0,d_0\) are nonnegative. At an inert power, the sign of a genuine norm does not affect its valuation, so the negative residual modulo that prime power is admissible. At the binary factor \(v_2(L)=1\) gives \(v_2(3^L-1)=3\), and successive two-adic lifts fill exactly the needed \(1\bmod8\) coset. No positivity condition for the actual integer residual follows from these modular choices.
