# Exact exception density for sublogarithmic distinct-exponent matchings

**The previously verified zero-atom identity (see [finite local blockers](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)) now gives the exact matching exception limit.** The zero atom of \(F\) equals the Haar measure of the full union of finite modular obstructions for eventual exponent phases.** Here “eventual” means that both exponents are sufficiently large for the modulus in question, as they are in the verified profinite rectangle. The proof gives a uniform conditional second-moment bound and an explicit modulus for each finite prime panel. [Verified profinite profile](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md)

Let \(B_Q\) be the union of residue classes modulo \(Q\) with no solution to
\[
n\equiv 3^c+5^d+x^2+y^2\pmod Q
\]
in the eventual exponent phases. Then, up to Haar-null sets,
\[
\boxed{\ \{F=0\}=\bigcup_{Q\ge1}B_Q.\ }
\]
A finite measured list gives a lower bound on this union. A numerical upper bound needs an exhaustion or a bound on the unmeasured part.

### Uniform conditional second moment

Let \(\mathcal G_z\) reveal the complete target coordinates \(n_p\) for primes \(p\le z\), and write \(F_z=\mathbb E(F\mid\mathcal G_z)\). With \(\theta=(c,d)\) Haar-uniform in \(\widehat{\mathbb Z}^2\), this is \(\pi\) times the exponent average of the product of the local norm densities for \(p\le z\). At its own prime, the term \(3^c\) or \(5^d\) has stabilized to zero. All the local weights in the panel depend only on the exponent components at primes \(\le z\), because the unit periods modulo \(p^k\) divide \(p^{k-1}(p-1)\).

For a pair of exponent choices, write \(h_q\) for their shift difference in \(\mathbb Z_q\). Integrating the two norm weights at a new prime gives the verified kernel
\[
K_q(h_q)=(1-q^{-2})\sum_{j=0}^{v_q(h_q)}q^{-j}
\le (1-1/q)^{-\mathbf1_{h_q\equiv0\ (q)}}.
\]
I claim that the expected product of these upper factors over any finite set of \(q>z\) is bounded by an **absolute constant**, uniformly after fixing both exponent pairs’ components at primes \(\le z\). No independence across the tail primes is needed.

Take \(z\ge5\). For \(z<q\le2z^{16}\), the product of *all* factors is bounded by Mertens’ theorem. In a dyadic block \(U<q\le2U\) with \(U\ge z^{16}\), separate two exceptional sets.

- If \(\operatorname{ord}_q(5)\le U^{1/3}\), then \(q\) divides \(\prod_{j\le U^{1/3}}(5^j-1)\). There are \(O(U^{2/3}/\log U)\) such primes, so their reciprocal sum over the blocks is bounded.
- Write \((q-1)_{\le z}\) for the part of \(q-1\) supported on primes \(\le z\). The primes with \((q-1)_{\le z}\ge U^{1/6}\) contribute \(O(\log(2z)/(\log U)^2)\) to the block’s reciprocal sum. Indeed, summing \(\log(q-1)_{\le z}\) over the block gives \(O(U\log(2z)/\log U)\). For prime powers \(r^j\le\sqrt U\), this follows by Brun–Titchmarsh and summing \(\log r/\varphi(r^j)\). For larger powers of a given \(r\le z\), use the first \(r^j>U^{1/4}\), which is still below \(\sqrt U\), to bound the number of primes involved, and charge at most \(\log(2U)\) per prime. The total of these larger-power contributions is \(O(Uz/U^{1/4})\). Markov’s inequality gives the stated reciprocal bound, which sums to \(O(1)\) from \(U\ge z^{16}\). [Montgomery–Vaughan, Brun–Titchmarsh bound](https://doi.org/10.1112/S0025579300004708)

At every remaining prime, the part of \(\operatorname{ord}_q(5)\) supported on primes \(>z\) exceeds \(U^{1/6}\). Holding the first shift and the second \(3\)-exponent fixed, equality of the two shifts modulo \(q\) fixes at most one class of the second \(5\)-exponent modulo its order. The free part gives conditional collision probability at most \(U^{-1/6}\). Expand the product of the good-prime factors by its largest selected prime. The preceding factors are bounded by \(O(\log q)\) by Mertens, so the conditional mean is at most
\[
1+O\!\left(\sum_q\frac{\log q}{q^{7/6}}\right).
\]
This proves the claim uniformly in the old exponent components.

The old local weights are nonnegative and measurable in precisely those components. Integrating the bound against the two old weights gives \(\mathbb E(F_w^2\mid\mathcal G_z)\le C F_z^2\) for every \(w\ge z\). Passing to the verified \(L^2\) limit yields
\[
\mathbb E(F^2\mid\mathcal G_z)\le C F_z^2.
\]
Conditional Cauchy–Schwarz now gives \(\Pr(F>0\mid\mathcal G_z)\ge C^{-1}\) wherever \(F_z>0\). These conditional probabilities converge almost surely to \(\mathbf1_{\{F>0\}}\). Thus on \(\{F=0\}\), some finite \(F_z\) must be zero. Conversely, a zero conditional mean of the nonnegative \(F\) forces \(F=0\) there.

### Exact finite modulus for a prime panel

Set
\[
L_z=\operatorname{lcm}\bigl(2,\{p-1:p\le z\}\bigr),\qquad
e_p=\min_{\substack{b\in\{3,5\}\\p\nmid b}}v_p(b^{L_z}-1),
\qquad Q_z=\prod_{p\le z}p^{e_p}.
\]
Condition on the two exponent residues modulo \(L_z\). For a unit base \(b\), the remaining \(p\)-primary exponent is Haar-uniform. The lifting-the-exponent identity shows that \(t\mapsto b^{a+L_zt}\) is uniform on the additive ball \(b^a+p^{v_p(b^{L_z}-1)}\mathbb Z_p\). The even factor in \(L_z\) handles \(p=2\). Adding the two power terms therefore gives a uniform ball of depth \(e_p\), with independent balls across the panel after fixing the coarse phases.

Averaging the local norm densities over these balls gives exactly the finite norm densities modulo \(p^{e_p}\). Hence \(F_z=F_{Q_z}\), and its zero classes are exactly \(B_{Q_z}\). Conversely, any \(B_Q\) lies in \(\{F=0\}\) almost surely by conditional expectation. This completes the comparison.

**Consequence for the matching problem.** For each fixed \(z\), a target in \(B_{Q_z}\) has zero witnesses in the verified rectangle for all sufficiently large \(X\). Together with the transferred upper bound, this gives an actual limit for the exceptional proportion for every \(1\le J(X)=o(\log X)\):
\[
\lim_{X\to\infty}\frac1X
\#\{X<n\le2X:\nu_X(n)<J(X)\}
=\mu\!\left(\bigcup_Q B_Q\right).
\]
An upper bound for single-witness misses in this **same rectangle** now bounds the matching exception limit. An estimate allowing small exponents outside the rectangle has a different scope. [Weighted matching transfer](https://github.com/Samsen879/a303656/commit/02f2daefba9bc131be23be39cdac08345e29a785)

### Short replay

For \(p\le7\), the exact panel modulus is \(5040\), with zero blocked residues. The last check shows why the eventual-power convention matters: in one fixed \(d\)-phase, a small \(3\)-exponent can give a true witness while the stabilized \(3\)-adic term is blocked.

```python
from math import lcm, prod

P = (2, 3, 5, 7)
L = lcm(2, *(p-1 for p in P))

def v(x, p):
    e = 0
    while x % p == 0:
        x //= p
        e += 1
    return e

mods = []
for p in P:
    depths = []
    for b in (3, 5):
        if b % p:
            e = v(b**L-1, p)
            depths.append(e)
            M = p**(e+2)
            assert {pow(b,L*t,M) for t in range(p*p)} == {
                1+j*p**e for j in range(p*p)
            }
    mods.append(p**min(depths))
Q = prod(mods)
assert L == 12 and mods == [16, 9, 5, 7] and Q == 5040

local = [{(x*x+y*y)%m for x in range(m) for y in range(m)} for m in mods]
norms = [n for n in range(Q) if all(n%m in S for m,S in zip(mods,local))]
shifts = {(pow(3,c,Q)+pow(5,d,Q))%Q
          for c in range(L,2*L) for d in range(L,2*L)}
assert len({(r+s)%Q for r in norms for s in shifts}) == Q

n = 1 + 5**6 + 2*901**2
assert 4*5**6 <= n and n % 9 == 4
assert n-1-5**6 == 901**2 + 901**2
assert v(n-3**2-5**6,3) == 1
```

### Numerical consequence in the audited rectangle

The existing [exact box-miss law](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md) supplies the zero-atom identification as well; the conditional argument above provides a direct alternative and an explicit, slightly larger panel modulus. The [active matched D=243 ledger](https://github.com/Samsen879/a303656/commit/47e9971cf4cdb8f0aac9e6e53a0b3d614c7aacb6) bounds misses in this growing two-axis box, as does the inherited [compensated density proof](SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md). Therefore for every integer function \(1\le J(X)=o(\log X)\) the displayed dyadic exception limit is **below 0.000062596085%**. In particular, a choice \(J(X)=\lfloor\log X/\log\log X\rfloor\) gives at least that many genuine representations with pairwise distinct labels on each axis for an asymptotic proportion above 99.999937403915%. This does not bound the exception proportion by zero or guarantee a witness for each specified integer.
