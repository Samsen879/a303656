# Single-witness box misses: exact reduction to finite local obstructions

Let \(F\) be the [profinite limit for the single-witness count](SINGLE_WITNESS_PROFINITE_LIMIT.md), with both exponent axes unrestricted in their growing windows. In the Haar model, \(F=0\) almost everywhere precisely on the union of the finite local blockers defined below. Moreover the proportion of integers \(X<n\le 2X\) with no witness in those two windows actually converges to the measure of that union. This reduces density-one coverage **in the box** to excluding finite blockers. Blocking the box does not rule out a witness with indices outside it.

## A finite, exact test

Write the phase as \((c,d)\in\widehat{\mathbb Z}^2\). At a unit base use the true local power map; at 3 let the 3-power vanish, and at 5 let the 5-power vanish, as they do in the growing-index limit. For a finite panel of primes \(P\), take \(R\) to be the lcm of 2 and the orders of the unit bases modulo the primes in \(P\). For each odd \(p\in P\) put
\[
 k_p=v_p(R)+\min_{a\in\{3,5\},\,p\nmid a} v_p(a^{p-1}-1);
 \qquad k_2=v_2(R)+2
\]
when 2 is in the panel. At fixed \((c,d)\bmod R\), the shift ranges exactly over one ball modulo \(p^{k_p}\) at each \(p\). This follows from lifting the order and using the fastest unit axis; at 2 the axis \(5^R\) generates \(1+2^{k_2}\mathbb Z_2\), while \(3^R\) also lies in that group. Free \(p\)-primary coordinates can be used independently for the local balls: at another prime all \(p\)-parts of the orders were already absorbed by \(R\).

For each common phase modulo \(R\), compute the residue of \(n-3^c-5^d\) at each \(p^{k_p}\) using the power maps above. The tests are:
- Inert \(p\): the valuation below depth \(k_p\) is even, or the residue is zero at depth \(k_p\).
- Split \(p\): all residues qualify.
- At 2: either the residue is \(0\bmod2^{k_2-1}\) or its known odd part is \(1\bmod4\).

These are exactly the balls containing values where the local norm density is positive. This includes a positive-measure cylinder of exponent phases, since any good finite nonzero valuation and odd part can be realized on a clopen sub-ball. There is no issue of surviving only at a phase that exactly equals a root. The panel blocks if no single phase passes at every \(p\in P\), so its blocking event is a literal union of congruence classes modulo \(\prod_{p\in P}p^{k_p}\).

## Uniform conditional moment of the tail

Let \(\mathcal H_z\) be the observation of all \(p\)-adic coordinates of \(n\) for \(p\le z\), and write \(F_z=\mathbb E(F\mid\mathcal H_z)\). By finite-modulus projection and local \(L^2\) convergence this conditional mean is \(\pi\) times the phase average of the product of the full local norm densities at \(p\le z\). Hence \(F_z=0\) is exactly the above head blocker (up to null sets).

Given the head, whenever \(F_z>0\), reweight the phase measure by those nonnegative head densities divided by their average. The reweighting depends only on \(z\)-smooth primary coordinates: each head norm reads powers with only such prime factors in their periods. For a finite tail panel the reweighting thus leads to a convex combination of tail centers averaged in individual phase classes modulo some \(z\)-smooth \(R'\). This is so even for the full-depth tail densities, since their orders at tail primes \(q>z\) have the same \(z\)-smooth part as the orders modulo \(q\). Bound the second moment uniformly for each such class and apply Jensen to the convex combination.

In one class, fix the first phase and the second \(c\). At each \(q>z\ge5\), the two shifts collide modulo \(q\) with probability at most \(1/\operatorname{ord}_q(5^{R'})\) over the other \(d\). The exact local pair correlation is \(1-q^{-2}\) without collision and at most \(1+1/q\) otherwise; the formulas hold also at coincident shifts by local \(L^2\). The average of the resulting product is bounded uniformly as follows.
- \(z<q\le 2z^4\) have bounded reciprocal sum by the prime-count upper bound. Small-order primes \(\operatorname{ord}_q(5)\le q^{1/4}\) have summable reciprocals by the [order-tail proof](AVERAGED_SHIFT_DISCRIMINANT.md).
- For the \(z\)-smooth part \((q-1)_{\le z}\ge q^{1/8}\), dyadically with \(q\in[Q,2Q]\) and \(Q\ge z^4\), the sum of \(\log r\) over \(r^a\mid q-1\), \(r\le z,\ r^a\le Q^{1/2}\), is at least \(\tfrac18\log Q\). If some power was clipped at \(Q^{1/2}\), its surviving part alone contributes at least \(\tfrac12\log Q-\log z\). Summing this weight over primes by [Montgomery–Vaughan Brun–Titchmarsh](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED) gives \(O(Q\log z/\log Q)\), using \(\sum_{r\le z}\sum_{a\ge1}\log r/\varphi(r^a)\ll\log z\). Thus their number is \(O(Q\log z/\log^2 Q)\), and the reciprocal sum over these dyadic intervals is \(O(1)\).
- Else the order in the class, \(\operatorname{ord}_q(5^{R'})\), is \(>q^{1/8}\). For the indicators \(I_q\) of collision, use Jensen for \(\exp(\sum_q I_q/q)\) with normalized weights proportional to \(1/(q\log q)\) as in the order-tail proof. The total weight before normalization is \(S_z=\sum_{q>z}1/(q\log q)=O(1/\log z)\). For sufficiently large \(z\) the resulting bound is \(1+O(\sum_{q>z}q^{-1+1/16}q^{-1/8})=O(1)\). Smaller \(z\) can charge a fixed initial prime interval by a constant.

It follows that for each finite tail panel the conditional second moment of the normalized tail center is \(O(1)\), independently of the head, \(R'\), and the panel. Increasing the tail panel and using conditional Fatou with the \(L^2\) martingale limit gives
\[
 \mathbb E(F^2\mid\mathcal H_z)\le C F_z^2.
\]
On \(F_z>0\), conditional Cauchy–Schwarz therefore gives \(\Pr(F>0\mid\mathcal H_z)\ge C^{-1}\). As \(z\) increases, the conditional probabilities converge to \(1_{\{F>0\}}\). On \(F=0\), some finite head must consequently block, almost surely; conversely a finite head blocker forces \(F=0\) there almost surely by nonnegativity.

## The ordinary density and remaining obstruction

Weak convergence gives the upper limit on box misses at most \(\Pr(F=0)\). For any fixed head blocker, the ordinary exponents in the box are eventually large enough that the two nonunit powers have stabilized at the modulus of that blocker; each integer in its classes is then indeed missed by the box. Taking larger heads gives the reverse lower limit, and therefore the exact box miss density.

The initial head \(2,3,5\) does not block any \(n\), as the finite replay below verifies: preserve the exhibited valuations/odd unit using \(c\bmod2\), \(d\bmod18\) and, at 2, its parity. At 5 all residues pass. A later inert prime \(q\) with an ordinary base (one of \(v_q(3^{q-1}-1),v_q(5^{q-1}-1)\) equal to one) cannot be the first blocker either. Starting from an older surviving phase, its \(q\)-primary coordinate on the ordinary axis is unread by smaller primes and can vary the single colliding residual through all lifts of its first residue. Thus a collision can be made even without hurting the earlier head. In particular any actual first blocker must occur at a common Wieferich inert prime. This is a necessary condition, not an exclusion of all such blockers.

~~~python
from itertools import product
for n in range(216):
    m,u = (4,1) if n%2 else (8,2)
    assert any((n-pow(3,c,m)-pow(5,d,m))%m == u
               and ((n-pow(5,d,27))%3 != 0 or
                    (n-pow(5,d,27))%27 in (9,18))
               for c,d in product((3,4),range(1,19)))
~~~
