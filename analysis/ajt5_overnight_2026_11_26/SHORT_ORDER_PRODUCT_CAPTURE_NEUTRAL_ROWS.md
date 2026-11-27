# Short-order product capture with an exact same-lift control

This is a structural prefilter for the finite neutral-chart problem, not a certificate for all remaining norms. It complements [the earlier neutral grid and complement bounds](https://github.com/Samsen879/a303656/commit/fc0e9f5ff1522aef4ba36697027bfa13959feb8e).

Let \(R>1\), let \(a\) be a unit modulo \(R\), and choose a positive integer \(B\). Form
\[
 P(X)=\prod_{i=0}^{B-1}(X-a^i)\pmod R,
 \qquad C=\prod_{j=1}^{B}P(a^{Bj})\pmod R.
\]
Then for every prime \(p\mid R\),
\[
 p\mid\gcd(R,C)\quad\Longleftrightarrow\quad\operatorname{ord}_p(a)\le B^2.
\]
The differences \(Bj-i\) run through \(1,\ldots,B^2\) exactly once. Over the field modulo \(p\), each \(a^{Bj}-a^i\) vanishes exactly when that order divides \(Bj-i\). This proves the equivalence even if there are repeated prime powers in \(R\). Their multiplicities in the gcd need not equal either their multiplicities in \(R\) or their valuations in any single difference. Dividing out the unit powers of \(a\) also identifies the product up to a unit with \(\prod_{k=1}^{B^2}(a^k-1)\). Evaluation is valid in the composite ring via the product definition; algorithms that divide by other quantities require separate unit checks.

In a composite neutral cofactor whose prime factors exceed \(Q=4\cdot10^9\), every prime divisor \(p\le R/Q\). The largest power \(H\) of 7 at most \(R/Q\) therefore kills the 7-primary part of every local unit order. This bound on \(H\) uses compositeness and the prime cutoff. Put \(L\) equal to the 7-free part of \(\operatorname{lcm}(1,\dots,20000)\), and take \(a=W^{LH}\) for a word \(W\) in the units 3 and 5. A particular captured order supplies a candidate exponent to strip the remaining prime-to-7 part on that factor, but the two axes still have to use the same 7-primary lift.

In the first exact control, the candidate \(\lambda=27\) is the unique lift in its residue class compatible with base 3 after exponent \(M\). Base 5 rejects that very lift, with gcd 1 on the captured divisor. The native root equation and exact order 343 on the row are checked. Independently, the second control has a true prime factor where all three tested projected words have exact prime order \(26{,}018{,}077>4096^2\); the length cutoff cannot capture it. This limit concerns those words and that cutoff, not all possible short-order tests. No aggregate counts or independently unverified speedups are asserted here.

```python
from math import gcd, isqrt, lcm

L = lcm(*range(1, 20001))
while L % 7 == 0:
    L //= 7

def H(R):
    h = 1
    while 7*h <= R//4_000_000_000:
        h *= 7
    return h

R, d, e = 456512878032408206350340694586451307581, 4892450967979, 342203
x = 416247695478217285797620981890141198829
M = L*e
assert pow(x,343,R) == 1 and gcd(pow(x,49,R)-1,R) == 1
assert (1+pow(x,41,R)-x-pow(x,294,R)) % R == 0
assert [gcd(R,pow(b,M*H(R),R)-1) for b in (3,5)] == [d,d]
assert [E for E in range(27,343,49)
        if pow(3,M,d) == pow(x,M*E % 343,d)] == [27]
assert gcd(pow(5,M,d)-pow(x,M*118*27 % 343,d),d) == 1

R, q, ell = 2777568164689467571666353977589920480563, 160635607399, 26018077
assert R % q == 0 and ell > 4096**2
assert all(all(n % j for j in range(2,isqrt(n)+1)) for n in (q,ell))
A, B = (pow(b,L*H(R),q) for b in (3,5))
assert all(w != 1 and pow(w,ell,q) == 1
           for w in (A,B,pow(A,8,q)*pow(B,9,q) % q))
assert all(d % j for j in range(2,isqrt(d)+1))
```
