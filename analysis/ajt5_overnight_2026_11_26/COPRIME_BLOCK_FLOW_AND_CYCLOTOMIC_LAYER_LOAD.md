# Coprime-block routing and harmonic cyclotomic layer capacity

The protected-load test can be strengthened in two directions. **Coprime blocks let a max-flow calculation choose the assignments**, and **cyclotomic factor bounds give a uniform capacity estimate for growing order layers**. Exact even-valuation leaves have a sharp limitation: if a root fibre misses a lift modulo \(p^2\), one target residue makes the entire fibre have valuation one.

### Optimize the assignments with coprime blocks

On the chart \(c=c_0+Ax\), write \(m_p=\operatorname{ord}_p(3^A)\). Form the protected downward closure as before. **Seed it with every inert repair prime \(p>3\) dividing \(A\), and every row whose first native digit is otherwise unavailable**, as well as the nonordinary rows and designated terminals.

Choose pairwise coprime integers \(D_j>1\). A protected row \(p\) can use block \(j\) if \(D_j\mid m_p\). Give block \(j\) capacity \(D_j-1\). The exact assignment condition for these blocks is
\[
|T|\ \le\ \sum_{j:\,\exists p\in T,\ D_j\mid m_p}(D_j-1)
\qquad\text{for every set of protected rows }T .
\]
This is the capacitated Hall condition, checked by max flow. To see why it certifies survival, a collision at \(p\) is empty or a single class modulo \(m_p\). Its projection forbids at most one residue modulo the assigned \(D_j\). Each block therefore retains a residue, and CRT combines them. The ordinary rows outside the closure can then be repaired in increasing prime order. Composite blocks allow several primary factors to carry one row’s avoidance condition.

### A capacity bound for growing order layers

Suppose the ordinary ancestors and any small-order core rows have already been assigned, with load at most \(\alpha_\ell<1\) on primary prime \(\ell\). Consider the remaining protected nonordinary rows that can be routed to \(\ell\nmid A\) with
\[
\operatorname{ord}_p(3)=b\ell^e,\qquad
1\le b\le B<\ell,\qquad 1\le e\le K_\ell .
\]
Each such row costs \(\ell^{-e}\). Put \(C_B=\log(4)\sum_{b\le B}\varphi(b)\). Their **total** additional load is at most
\[
\frac{C_B}{2\log\ell}\,H_{K_\ell},
\qquad H_K=\sum_{e=1}^K\frac1e.
\]

Indeed, for fixed \(b,e\), every such nonordinary \(p\) contributes \(p^2\) to \(\Phi_{b\ell^e}(3)\). Exact order excludes the other cyclotomic factors of \(3^{b\ell^e}-1\). Also \(p\ge 2\ell^e+1\), and \(\log\Phi_{b\ell^e}(3)\le\varphi(b\ell^e)\log4\). Taking logarithms and dividing by \(\ell^e\) bounds the layer’s load by \(\varphi(b)\log4/(2e\log\ell)\). Summing proves the estimate. For a layer containing ordinary rows too, the same bound without the factor \(1/2\) applies.

Thus \(\alpha_\ell+C_BH_{K_\ell}/(2\log\ell)<1\) certifies the whole batch without counting its exceptional primes. For example, if \(\alpha_\ell\le1-\eta\) and \(B\) is fixed, depths \(K_\ell\le\ell^\delta\) are allowed for every fixed \(\delta<2\eta/C_B\) at sufficiently large owners. This is a sufficient condition for growing closed prefixes, with no bound on the number of ordinary rows outside their closures.

The order shape occurs at unbounded actual inert terminals. For primes \(\ell\equiv3\bmod4\), \((3^\ell+1)/4\equiv3\bmod4\), so it has an inert prime divisor \(q\). That divisor has order \(2\ell\) on base \(3\): order two would force \(q\mid4\). The remaining condition is on the **full closures** of these prefixes, including earlier exceptions and ordinary ancestors. I have not proved it for a cofinal family.

### Exact leaves and a \(3,5\) countercontrol

On a fixed mod-\(p\) collision fibre, suppose the attainable offsets modulo \(p^2\) omit one lift of that collision. Choosing \(n-5^d\) at the missing lift gives exact valuation one on the whole fibre. In particular, put \(w_p=v_p(3^{\operatorname{ord}_p(3)}-1)\). Any two exponents on the collision fibre differ by a multiple of \(\operatorname{lcm}(A,\operatorname{ord}_p(3))\), so their offsets agree modulo \(p^2\) whenever \(w_p+v_p(A)\ge2\). This includes both nonordinary rows and ordinary rows with \(p\mid A\). Adversarial readings at distinct rows can be imposed simultaneously by CRT. The usual ordinary repair requires the free first native digit. [Finite-obstruction and ordinary-repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Take \(A=168\), \(c\equiv0\bmod168\), \(d=2\), and terminal \(23\). The terminal reads \(11\), whose order on base \(3\) is \(5\). Neither order forces \(7\) into the closure. Omitting the stride rule would leave projected orders \(5,11\), which pass the assignment test. But \(7\) is ordinary and divides \(168\). At the target below, \(3^c\equiv1\bmod49\) throughout the chart, so the remainder has exact valuation one at \(7\) everywhere. The same target also gives exact valuation one at \(11\) on its collision class \(c\equiv0\bmod5\). The reduced panel passes at \(c=168\).

```python
from math import gcd

n = 640316598138243
a, b = 11889460, 22337353
A = 168

def order(p):
    return next(k for k in range(1, p) if pow(3, k, p) == 1)

assert [order(p) for p in (7, 11, 19, 23)] == [6, 5, 18, 11]
assert [order(p)//gcd(A, order(p)) for p in (7, 11, 23)] == [1, 5, 11]
assert pow(3, 6, 49) != 1 and pow(3, 5, 121) == 1
assert pow(3, A, 49) == 1 and (n-26) % 49 == 7
assert (n-26) % 121 == 11
assert (n % 4, n % 3) == (3, 0)
assert all((n-25-pow(3, A, p)) % p for p in (11, 19, 23))
assert n == a*a + b*b + 3**2 + 5**2 and n >= 4*25
```

The countercontrol blocks the anchored chart, while the same integer has a true quarter-box witness at \(c=d=2\). The growing-prefix criterion certifies local phases and gives no bound on their least integer exponent heights.

Independent BigInt verified the exact stride rigidity and true same-target witness and tested the unbounded-family terminal construction at six small inert owner primes. The Hall condition is exact for assigning the chosen blocks, but it is only a sufficient test for phase survival. The harmonic bound does not control arbitrary order shapes or an entire cofinal closure.
