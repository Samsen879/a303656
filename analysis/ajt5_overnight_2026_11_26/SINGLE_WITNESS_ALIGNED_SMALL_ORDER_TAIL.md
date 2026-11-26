# A summable aligned two-source tail for growing tame order

Fix the sources and slopes of the [two-source alignment lattice](SINGLE_WITNESS_TWO_SOURCE_GCD_LATTICE.md), writing \(D=pr\) and \(m\bmod D\) for the merged slope. At any matching reader \(q\), let the order lcm of \(3,5\) be \(DM\), with \((D,M)=1\). Let \(U,V\) be the two fixed rational numbers \(3^a5^b\) obtained from a basis of the relation lattice \(ma+b=0\bmod D\). They are multiplicatively independent. Their generated group modulo \(q\) has order exactly \(M\): reducing the original cyclic group of order \(DM\) onto its order-\(D\) primary quotient has precisely that lattice as preimage of the identity, by the slope relation and full order on both axes. The image of the lattice is then the kernel of order \(M\).

Write \(\lambda_q=\min_{b=3,5}v_q(b^{q-1}-1)\). All unit relations modulo \(q\) lift to \(q^{\lambda_q}\), and in fact
\[
 v_q\gcd(\operatorname{num}(U^M-1),\operatorname{num}(V^M-1))=\lambda_q.
\]
One direction is the lift. For the other, the lattice contains \((D,0),(0,D)\), so any shared divisibility at depth \(e\) implies that \(3^{DM},5^{DM}\) both equal 1 modulo \(q^e\). The exponent \(DM\) divides \(q-1\) with unit multiplier. An arbitrary larger exponent is not an exact proxy: replacing \(M\) by a multiple \(K\) adds \(v_q(K/M)\) to this gcd valuation by lifting.

For \(X\le q<2X,\ M\le Y\), compare the residues \(U^iV^j\) with \(0\le i,j\le \lfloor\sqrt Y\rfloor+1\). There are more residues in the list than group elements, so there is a nonzero integer relation \((a,b)\) with both absolute coordinates \(O(\sqrt Y)\). Its nonzero numerator \(\operatorname{num}(U^aV^b-1)\) is divisible by \(q^{\lambda_q}\). There are \(O(Y)\) possible relations and each numerator has logarithmic size \(O_{U,V}(\sqrt Y)\); multiplying them bounds the sum of \(\lambda_q\log q\) over all matched readers in the interval by \(O_{U,V}(Y^{3/2})\). This is an elementary short-relation order count with the exact square-lift multiplicity retained.

For any fixed \(\beta>0\) it follows by dyadic summation that
\[
 \sum_{\substack{q>Z,\ M\le q^{2/3}/(\log q)^\beta\\
                 \text{both slopes matched},\ \lambda_q\ge2}}\frac1q
 \ll_{U,V,\beta}(\log Z)^{-3\beta/2}.
\]
Indeed the contribution near \(X\) is \(O((\log X)^{-1-3\beta/2})\). This is a bound for a specified shape of possible readers, not for every common Wieferich prime. In a zero-observation cancellation scenario those readers matter only for \(q\mid n\); the same series bounds their Haar measure. If both earlier source observations are zero and their intercepts also vanish, \(p^2r^2\mid n\), so discarding a source above \(B\) costs at most \(\sum_{p>B}p^{-2}\). These statements do not control tame orders with \(M\) comparable to \(q\) or other reader shapes, and do not prove density one.

The real replay at \(1419643\) has short independent relations giving the full kernel modulo the prime, but both fail to lift to its square. This is an arithmetic boundary control for the specified lattice, not an actual common Wieferich prime.

~~~python
from math import isqrt

q, M, D = 1419643, 3558, 133
assert q % 4 == 3 and all(q % j for j in range(2, isqrt(q)+1))
L = D*M
assert all(pow(a, L, q) == 1 and
           all(pow(a, L//p, q) != 1 for p in (2, 3, 7, 19, 593))
           for a in (3, 5))
assert pow(3, M, q) == pow(5, 106*M, q)

Q = q*q
U, V = 6075, pow(5*pow(3, -1, Q), 19, Q)
z = U*V % q
assert pow(z, M, q) == 1
assert all(pow(z, M//p, q) != 1 for p in (2, 3, 593))
assert (U % q, V % q) == (pow(z, 2343, q), pow(z, 1216, q))

rows = [(-44, -3), (-2, -81)]
assert abs((-44)*(-81) - (-3)*(-2)) == M
assert all((2343*a + 1216*b) % M == 0 for a, b in rows)
assert [pow(U, a, Q)*pow(V, b, Q) % Q for a, b in rows] == [
    1+402667*q, 1+1109281*q]

~~~
