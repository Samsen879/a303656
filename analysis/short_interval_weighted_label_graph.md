# Robust weighted label graphs in short progressions

In the original power windows \(X^{1/8}\le3^c\le X^{1/4}\), \(X^{1/3}\le5^d\le X^{1/2}\), let \(Q=27\cdot2^k\), \(k\ge3\), \(X\le T\le2X\), and \(J=H/Q\). For a sufficiently large absolute constant \(C_0\), assume
\[
C_0 QX^{1/3}(\log X)^8\le H\le X .
\]
Then in every prescribed class \(b\bmod Q\), a positive proportion of its targets in \((T,T+H]\) each have the following graph property: after removing any at most \(\rho\log X\) exponent vertices, there are still \(\gg(\log X)^{5/4}\) distinct true two-square label edges and \(\gg(\log X)^{1/4}\) pairwise edge-disjoint matchings, each of size \(\gg\log X\). Constants here are absolute. This conservative threshold keeps the logarithmic loss from the original Tolev estimate; we do not claim the log-free endpoint, a squarefree core, or arbitrary-target coverage.

## Reduced classes and the lower first moment

For each \(b\bmod216\), use the elementary corrected phase in [the squarefree graph proof](https://github.com/Samsen879/a303656/pull/104). Explicitly, for odd \(b\) take \(D_0=1\), \(c\) odd iff \(b=1\bmod4\), and choose \(5^d\ne b\bmod3\). For even \(b\), the parity pair \((c,d)\) for \(b=0,2,4,6\bmod8\) is respectively (even,odd), (odd,odd), (even,even), (odd,even). Take \(D_0=2\) if the residual is a unit modulo 3. For the remaining four \(b=2,4,8,22\bmod24\), keep \(c=1,0,0,1\bmod2\) respectively, take \(D_0=18\), and solve \(5^d=b-18\bmod27\) using the full order 18. For large \(X\), \(c\ge3\). Both exponent axes have size \(\asymp L\), \(L=\log X\), and \(u_\lambda=(n-\lambda)/D_0\) for \(\lambda=3^c+5^d\) is positive, \(1\bmod4\), coprime to 3. It occupies one reduced class modulo \(q=Q/D_0=2^j3^i\), \(j\ge2,1\le i\le3\). The class can vary with the actual label. Distinct labels have distinct sums: a difference between two 5-powers is at least \(4X^{1/3}\), too large to be canceled by the 3-powers, and within each row the 3-powers are distinct.

Let \(R(u)=r_2(u)/4\) with all signed ordered representations counted. Then \(R\ge0\) is multiplicative and \(R(u)>0\) is exactly the desired norm criterion. Furthermore multiplying a represented core by \(D_0\in\{1,2,18\}\) preserves representation. For the actual reduced class, there are \(2^{j+1}\) modular pairs at 2 and \(4\cdot3^{i-1}\) at 3. At \(j=2\) this is checked directly; for \(j\ge3\), one coordinate is odd and there are exactly half of the even residues of the other coordinate giving a square \(1\bmod8\), with four odd roots. Thus the count is \(8q/3\). [Tolev, Eqs. (2), (10)](https://arxiv.org/pdf/1106.3474v2), at both ends of the residual interval of length \(H/D_0\), gives the first moment \((2\pi/3)J+O((q^{1/2}+X^{1/3})\tau(q)^4\log^4 X)\) for each label. Here \(q^{1/2}=O(X^{1/3})\) by \(H\le X\) and the lower bound on \(J\). Since \(\tau(q)\ll L\), choosing \(C_0\) large enough makes this \(\gg J\) uniformly.

## Upper moments uniformly in growing classes

Write \(n=b+Qm\) with \(0\le b<Q\). The reduced forms \(U_\lambda(m)=qm+(b-\lambda)/D_0\) are primitive because their constant terms are units modulo \(q\). The product of a pair has height \(O(X^2)\); the interval has base \(x\asymp X/Q\) and length \(y=J\), with \(x\gg X^{1/3}\). We apply [Henriot Theorem 5](https://arxiv.org/pdf/1102.1643) as restated in the [2014 erratum](https://doi.org/10.1017/S0305004114000280), with \(\alpha=1/4,\delta=1/8\) and growth parameter \(10^{-4}<\alpha/(50g(g+\delta^{-1}))\) for degree \(g\le2\). The weight \(R^s\) at fixed \(s\) satisfies the requisite multiplicative bounds because \(R(p^\nu)\le\nu+1\) and the divisor function has every fixed power-growth margin. The two-variable weight is the product of the one-variable weights. The height condition \(x\gg\|U\|^\delta\), and \(y\ge x^\alpha\), hold; split into two comparable subintervals if \(y>x\). No lower-bound variant of that theorem is used.

For one form the nonfixed prime has one root, and at an odd \(p\nmid q\) the local first-order factor is \(1+(R(p)^s-1)/p+O_s(1/p^2)\). It is \(R(p)=2\) at split primes and \(R(p)=0\) at inert primes. For two distinct forms the factor is \(1+2\chi_4(p)/p+O(1/p^2)\) outside primes dividing the difference \(h=\lambda-\mu\) and the leading coefficients. At \(p\mid q\) the forms are units, and the remaining bad factors are \(1+O(1/p)\): this follows from the corrected Corollaries 1–2, since for primitive linear forms with unit slope any nonempty congruence specifying at least one positive exponent has density at most \(1/p\). For clarity, \(h/D_0\) is integral and its prime divisors outside 2,3 coincide with those of \(h\). Using the prime Mertens estimates in the two odd classes gives
\[
\sum_m R(U_\lambda(m))^s\ll_s J L^{2^{s-1}-1}\quad(s=9/8,\,2),\qquad
\sum_m R(U_\lambda(m))R(U_\mu(m))\ll J\prod_{p\mid h}(1+C/p).
\]

The pair factor averages to a constant both over all label pairs and over distinct pairs of edges incident to any fixed vertex. Here is a direct order bound. The contributions of the finitely many primes dividing 30 are bounded constants; primes beyond \(L^2\) are harmless because \(\log|h|=O(L)\). Expand the remaining product over squarefree \(d\) with coefficients \(C^{\omega(d)}/d\). Vary one free exponent axis while fixing the other three exponents. For the vertex energy vary an axis *other than the fixed vertex's*, using base \(B_0=9,25,\) or \(5^{18}\) as appropriate, and ignore diagonal \(h=0\). An admissible congruence hits at most one class modulo \(\operatorname{ord}_d(B_0)\), so its average is at most \(1/\operatorname{ord}_d(B_0)+O(1/L)\). The second term sums to \(O((\log L)^C/L)\) by Mertens. For the first, all \(d\) of order at most \(U\) divide \(\prod_{j\le U}(B_0^j-1)\), of log-size \(O(U^2)\). Their coefficient sum is \(O((\log(2U))^{O(C)})\): split primes at that log-size, apply Mertens below the cutoff and bound the reciprocal sum of the larger prime divisors by a constant. Sum in dyadic order blocks to get a bounded average. This preserves the actual multiplicity of the differences.

## Truncation and same-target graph extraction

Discard edges of weight \(R(u)>L^{3/4}\). For each label the discarded mass is
\[
O(J L^{2^{1/8}-1-3/32})=o(J)
\]
by the \(9/8\)-th moment. Let \(W(n)\) be retained mass and \(E(n)=\sum_v (\sum_{e\ni v}R(u_e))^2\) using retained edges. The moment estimates and averages give \(\sum W\gg J L^2\), \(\sum W^2\ll J L^4\), \(\sum E\ll J L^3\). The diagonal contribution to the latter is \(O(JL^3)\) by \(s=2\); the off-diagonal follows from the fixed-vertex average. Cauchy–Schwarz and then Markov produce \(\gg J\) targets with \(W(n)\ge cL^2,\ E(n)\le C_1L^3\).

At any one such target, deleting at most \(\rho L\) vertices costs at most \(\sqrt{\rho L E(n)}\) weight, leaving \(\gg L^2\) for small enough \(\rho\). The maximum weight per edge is \(L^{3/4}\), proving the distinct-edge bound. The endpoints of any maximal matching cover the leftover edges. Hence weight \(\gg L^2\) and energy \(O(L^3)\) imply matching size \(\gg L\) by the same Cauchy–Schwarz bound. Select exactly \(\lfloor c_2L\rfloor\) edges per round; these cost at most \(c_2L^{7/4}\), so the construction continues for \(\gg L^{1/4}\) edge-disjoint rounds without exhausting the weight budget. All steps occur on the graph of that same target.

## Exact controls


```python
from math import isqrt
assert 35**8 > 2*32**8
assert (305-4)%12 == 1 and (305-4)%49 == 7
# The first has a genuine norm; the second is obstructed by v_7=1.
n = 10000016714
assert n-3**5-5**5 == 99111**2+13305**2
assert ((n-3**3-5**5)//18)%49 == 42
# A leading-coefficient prime creates no roots on these reduced classes.
for q in (12,24,36,72,108,216):
    for u in range(q):
        if u%4==1 and u%3:
            base={a*a%q:[b for b in range(q) if b*b%q==a*a%q]
                  for a in range(q)}
            assert sum(len(base.get((u-x*x)%q,())) for x in range(q))==8*q//3

```
