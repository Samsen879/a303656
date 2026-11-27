# A true second label, but zero density in the fixed split-factor quadratic

At the fixed branch \(p=41q(t)\), \(q(t)=2132t^2+316t+11\), from [the prescribed split-factor construction](PRESCRIBED_SPLIT_FACTOR_BRIDGES.md), put \(m=p^2+2188\). The \(K=10940\) target \(5p^2+10940\) is always a genuine two-square norm. The second actual child label \((e,f)=(1,2)\) gives \(K=10942-5-9=10928\). At \(t=0\) both work at the same m:
\[
5\cdot451^2+10940=692^2+741^2,\qquad
5\cdot451^2+10928=1013^2+42^2.
\]
Stripping the split factor to \(p=11\) preserves the first norm but sends the second to \(19\cdot607\), with odd 19-adic valuation.

### Every fixed progression leaves an infinite obstruction

For \(k=13\), \(b=79+1066t\), \(C=k^2-547=-378\), we have \(kp=b^2+C\). Therefore \(5p^2+K\) is \(5/k^2\) times
\[
R(b)=(b^2+C)^2+k^2K/5.
\]
For \(K=10928\) this quartic is squarefree: neither b=0 nor \(b^2=-C\) is a repeated root since the relevant constant values are positive. It is not a polynomial norm over \(\mathbb Q(i)/\mathbb Q\). Indeed, if \(R=P^2+Q^2\) with rational polynomial coordinates, a constant rational rotation takes the leading vector to (1,0). The cubic coefficient gives \(P=b^2+v\); the linear coefficient requires \(Q\) either constant or a multiple of b. In the first case \(k^2K/5\) must be a rational square; it has 5-adic valuation -1. In the second \(Q=2u b\) gives \(k^2K/5=4u^2(u^2-C)\). The right side has nonnegative 5-adic valuation for \(v_5(u)\ge0\), or valuation \(4v_5(u)\) otherwise, again impossible.

A squarefree monic rational polynomial whose irreducible factors all split over \(\mathbb Q(i)\) is a polynomial norm, by pairing conjugates. Thus some irreducible factor of R remains irreducible over \(\mathbb Q(i)\). Its root field does not contain i. In a splitting field enlarged by i, there is an automorphism fixing that root but nontrivial on i, since the compositum over the root field is quadratic and the ambient extension is normal. By the [Chebotarev density theorem](https://websites.math.leidenuniv.nl/algebra/chebotarev.pdf), the corresponding Frobenius class supplies a positive-density set of primes \(\ell\equiv3\bmod4\) with a simple root, discarding the finite bad primes. In t-coordinates the root remains simple away from the step and the denominators. Each such \(\ell\) gives \(\ell-1\) residue classes modulo \(\ell^2\) with exact valuation one by lifting, hence actual failure. For any fixed parameter progression, avoiding its finitely many modulus primes leaves reciprocal sum divergent. Applying CRT to each finite subset and then taking that subset arbitrarily large bounds the relative upper density of true second labels by zero. This argument is within this particular quadratic parameter, not a statement about all integer m.

### First label alone among squarefree near-primes after any finite inert panel

Given any finite set S of inert primes to be checked on the second residual, prescribe \(t\equiv0\) at every member except 11. At those primes both the second residual (its \(t=0\) value is \(521\cdot1973\), with both primes split) and q are units. At 11 instead use \(t\equiv1\), where the two respective residues are 8 and 6. Impose also \(t\equiv0\bmod41\) to preserve the fixed split factor with no repetition. Add an outside failure prime \(\ell\) as above, avoiding the divisors of K. Its root for \(5p^2+K\) enforces \(q\not\equiv0\bmod\ell\). Choose a lift modulo \(\ell^2\) of exact valuation one and apply CRT. Along the resulting progression q is still irreducible with positive leading coefficient and no fixed prime divisor. Indeed the original discriminant 6048 is nonsquare and the polynomial has relatively prime coefficients, is always odd, and a nonzero quadratic cannot vanish identically at an odd prime. At primes newly in the progression's modulus we explicitly chose q to be a unit. By [Lemke Oliver, Theorem 1](https://lemkeoliver.github.io/papers/04-Quadratic.pdf#page=2), infinitely many q-values are squarefree with at most two prime factors. They give squarefree p with at most three factors and real first-label representations, but fail the second label on the same m while passing every prime in S.

This does not supply infinitely many same-point double successes, nor does it exclude a sparse infinite set of them or claim infinitude of prime q.

~~~python
from math import gcd, isqrt
q = lambda t: 2132*t*t + 316*t + 11
K = 10928
R = lambda t: 5*(41*q(t))**2 + K
assert q(0) == 11 and q(1) == 2459
assert 5*(41*q(0))**2 + 10940 == 692**2 + 741**2
assert R(0) == 1013**2 + 42**2 == 521*1973
assert 5*11**2 + 10940 == 84**2 + 67**2
assert 5*11**2 + K == 19*607 and 607 % 19 != 0
assert (R(1) % 11, q(1) % 11) == (8, 6)
assert K % 5 != 0
assert gcd(gcd(2132, 316), 11) == 1
disc = 316**2 - 4*2132*11
assert disc == 6048 and isqrt(disc)**2 != disc
for p in (521, 1973):
    assert p % 4 == 1 and all(p%d for d in range(2, isqrt(p)+1))
~~~
