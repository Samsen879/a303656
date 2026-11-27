# Odd signed targets via Legendre-controlled parity switches

**A joint parity switch does extend the signed-target criterion to odd targets.** The exact test uses four signed residuals, selected by the two Legendre symbols at each inert prime. It gives an explicit target where switching both exponents succeeds and switching just the \(3\)-exponent fails. A real quadratic norm condition also gives growing families in both odd classes modulo \(4\). This extends the modular conclusion of the [even-target result](https://github.com/Samsen879/a303656/commit/7fbbfe8bc78f76d59ffa1d8acd8ac67ccb87d57c).

### Exact test with the odd parts of the orders fixed

Write an odd target as \(n=P+Q-S\), where \(P=3^{c_0}\), \(Q=5^{d_0}\), and \(S=x^2+y^2>0\). Since \(S\) is odd, \(S\equiv1\pmod4\). Keeping the original parity of \(c_0\) leaves the residual \(3\bmod4\), regardless of the parity of \(d\). The \(3\)-exponent must switch parity.

Let \(\eta=0\) retain the parity of \(d_0\), and let \(\eta=1\) switch it. A sufficient condition for **every modulus to admit a passing pair with arbitrarily large \(c\)** is that one choice of \(\eta\) satisfies both tests below. Zero passes each test.

- At every \(p>3\) with \(p\equiv3\pmod4\), the integer
  \[
  n-\left(\frac3p\right)P-\left(\frac5p\right)^\eta Q
  \]
  has even \(p\)-adic valuation.
- At \(3\), the integer \(n-(-1)^\eta Q\) has even \(3\)-adic valuation.

Indeed, at each inert prime power the unit orders have binary valuation at most one. Fixing the odd parts of the exponent orders and switching parity therefore multiplies the corresponding power by its Legendre symbol, at the **full prime-power precision**. At \(3\), take \(c\) large enough that \(3^c\) vanishes and apply the same rule to \(5^d\). The exponent constraints are compatible because the fixed periods are odd. At \(2\) the switch makes the odd residual \(1\bmod4\), which suffices at every binary precision. Split primes impose no condition. CRT then joins the local square coordinates.

The test is also necessary **for this fixed-odd-order method** across all moduli. If both choices fail, put one failing prime power for each choice into a panel containing \(4\). Those two failures eliminate both parity choices on the prescribed phases.

### Actual controls

- **Both switches are needed at \(n=117=1+5^3-3^2\).** Switching only \(c\) gives residual \(-7\) at \(7\). Switching both assigns \(-9,-7,241,243\) to the four sign patterns. The only inert prime above \(3\) that could veto this list is \(7\) on the \(-7\) branch, but both characters at \(7\) are negative, so its assigned residual is \(243\). The ternary residual is \(242\), a unit.
- **Both fixed choices fail at \(n=225=1+5^4-(1^2+20^2)\).** At \(19\), the orders modulo \(19^2\) are \(342\) and \(171\), so switching \(c\) forces its sign to change while either parity of \(d\) leaves the \(5\)-power unchanged. The residual is \(-399\equiv17\cdot19\pmod{361}\). Releasing just the \(19\)-primary digit permits \(c=135,d=4\), which preserves the switched phase modulo \(19\) and gives residual zero modulo \(361\). The failure concerns the frozen method.

### Growing odd families

For the single switch \(\eta=0\), it suffices that \(2P-S=r^2-3t^2\) and that the ternary test passes. The changed residual is used only at primes where \(3\) is a nonsquare. At such a prime, divisibility of \(r^2-3t^2\) forces divisibility of both coordinates, hence an even valuation.

Take \(u+v\sqrt3=(2+\sqrt3)^j\). Two resulting families are
\[
\begin{array}{c|c|c|c}
n\bmod4 & c_0 & S & 2P-S\\ \hline
1 & 0 & u^2+1\quad(j\text{ odd}) & -3v^2\\
3 & 1 & 4u^2+1 & 1-3(2v)^2 .
\end{array}
\]
In both cases \(n-Q\) is a ternary unit. If \(x=u\) or \(2u\) as appropriate, choose the least \(D\) with \(5^D\ge2x^2\) and take \(Q=5^D\). Then \(S\) grows proportionally to \(n\), and \(Q>n\). The resulting fixed-\(d\) congruence witnesses therefore have negative integer residuals throughout. They exclude finite tail obstructions without supplying a positive representation in that column.

```python
assert 117 == 1 + 5**3 - 3**2
M = 2**8 * 3**4 * 7**3 * 11**2 * 19**2 * 23**2 * 47**2
c, d = 498173445, 1494520338
x, y = 59255514439031296, 230627726001096205
assert (117 - pow(3,c,M) - pow(5,d,M) - x*x - y*y) % M == 0

for d in (4, 175):
    assert (225 - pow(3,171,361) - pow(5,d,361)) % 361 == 17*19
assert (225 - pow(3,135,361) - pow(5,4,361)) % 361 == 0

def ord(a,q):
    return next(i for i in range(1,q) if pow(a,i,q)==1)
assert (ord(3,361),ord(5,361))==(342,171)
assert pow(3,3,7)==pow(5,3,7)==6
assert [117-s-t*125 for s,t in [(1,1),(-1,1),(1,-1),(-1,-1)]]==[-9,-7,241,243]
assert all(241%p for p in range(2,16))
u,v=1,0
for j in range(1,10):
    u,v=2*u+3*v,u+2*v
    assert u*u-3*v*v==1
    for P,x,r,t,klass in ((1,u,0,v,1),(3,2*u,1,2*v,3)):
        if P==1 and j%2==0: continue
        S=x*x+1
        Q=1
        while Q<2*x*x: Q*=5
        n=P+Q-S
        assert n>1 and n%4==klass and (n-Q)%3 and Q>n
        assert 2*P-S==r*r-3*t*t
print("switches, sign branches and both Pell families passed")
```


For an inert prime \(p>3\), imposing the original residues modulo the odd parts of both full orders leaves one parity choice per axis; an order with nontrivial binary part has its unique order-two element at the sign \(-1\). The Chinese remainder choices can be taken arbitrarily large. In the real quadratic norm argument, divisibility by \(p\) at a prime where 3 is a nonsquare forces divisibility of both coordinates, so iteration gives even valuation. These modular witnesses are not positive representations at ordinary height.
