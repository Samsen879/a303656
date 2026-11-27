# A square-gcd test for aligned zero-cancellation on repair lines

For two ordinary axes at inert source \(p\ge7\), use absolute exponent digits \(x=c\bmod p,\ y=d\bmod p\), with all other primary coordinates fixed. Write \(A,B\) for the two power residues modulo \(p\), and \([A],[B]\) for their torsion lifts to \(p^2\). Put \(f_a=(a^{p-1}-1)/p\bmod p\). The first repair digits under a collision satisfy
\[
 \frac{Af_3}{p-1}x+\frac{Bf_5}{p-1}y=\frac{n-[A]-[B]}p\bmod p.
\]
Indeed at zero absolute digit the unit power is torsion modulo \(p^2\); incrementing the digit by one can be realized with exponent increment \((p-1)\cdot (p-1)^{-1}\bmod p\), with the inverse taken modulo \(p\) and the increment a multiple of \(p-1\). Write the resulting line \(y=mx+b\). A second digit gives exact valuation two while leaving all first-digit-only readers untouched. If \(n=0\bmod p\), \(B=-A\), so \(m=f_3/f_5\) and \(b=0\) exactly when \(p^2\mid n\).

A later reader \(q\) that reads exactly one \(p\)-digit on both axes has shift along this line \(Cg^x+D h^b(h^m)^x\), with \(g,h\) of order \(p\), and \(C,D\) of order prime to \(p\) because the digits are absolute. This is constant only if \(g=h^m\) and \(C=-D h^b\), by independence of characters. Separating the coprime factors gives \(b=0\) and \(C=-D\). The constant is zero. In particular any group of such readers whose observation is zero can be avoided simultaneously unless one is identically zero on the chosen source domain: if the source is already a unit take \((x,y)=(0,1)\); if \(b\ne0\) on the repair line take \((0,b)\); if \(b=0\) take a nonzero \(x\), which avoids every nonaligned zero reader. This requires all other conditions either not to read the changed digits or to be included in the same check. For several sources with no mutual own-test reads, the same selection works provided each relevant zero reader reads both digits to depth one or neither at each source: a zero requires all of its primary character equalities at once as well as the prime-to-source factor matching.

Now suppose \(q\) is genuinely common Wieferich and \(\lambda_q=\min(v_q(3^{q-1}-1),v_q(5^{q-1}-1))\). Put \(M=\operatorname{lcm}(\operatorname{ord}_q(3),\operatorname{ord}_q(5))/p\), and choose positive \(u,v\) with \(u/v=m\bmod p\). From \(g=h^m\) get \(3^{Mv}=5^{Mu}\bmod q\); equality persists among the torsion lifts, giving
\[
 q^{\lambda_q}\mid\gcd(3^{pM}-1,\ 5^{pM}-1,\ 3^{Mv}-5^{Mu}).
\]
The condition remains necessary with a multiple of \(M\). On a constant-zero line all sums lock to zero through depth \(\lambda_q\); the locked line is killed exactly when the valuation of the observation is odd and below \(\lambda_q\). If the observation lies in the zero ball one can repair at the still free \(q\)-primary digit.

For example take source \(7\), \(n=0\bmod7\), with later readers all shallow on the two axes, observed zero, genuinely common Wieferich and \(M\mid54\). Here \(m=1\bmod7\), and the exact gcd computed below has no square factor of any such later prime; hence none can identically cancel, no matter how many readers of this kind are present. At ordinary reader 379 the same corresponding line can cancel modulo the prime while retaining seven distinct shifts modulo its square. The replay checks the latter case at the same \(n\), which also has a true representation at a different label. Neither claim addresses arbitrary reader orders, mixed depths, or density one.

~~~python
from math import gcd, isqrt

q, n = 379, 401189313
E = 54*q
assert all(all(p % j for j in range(2, isqrt(p)+1))
           for p in (7, 19, 109, q))
assert [(a**6-1)//7 % 7 for a in (3, 5)] == [6, 6]
assert gcd(3**378-1, 5**54-3**54) == 2**3*7**2*19*109*q
assert [next(k for k in range(1, q) if pow(a, k, q) == 1)
        for a in (3, 5)] == [378, 21]
assert all(pow(a, q-1, q*q) != 1 for a in (3, 5))
assert (n % 343, n % (q*q)) == (49, 0)

def S(x, y, mod):
    return (pow(3, 189+E*x, mod) + pow(5, 42+E*y, mod)) % mod

assert [(x, y) for x in range(7) for y in range(7)
        if (n-S(x, y, 49)) % 49 == 0] == [(x, x) for x in range(7)]
assert all(any((n-S(x, x+7*j, 343)) % 343 in range(49, 343, 49)
               for j in (0, 1)) for x in range(7))
V = [S(x, x, q*q) for x in range(7)]
assert V == [28046, 10612, 58366, 33731, 113700, 50786, 135682]
assert len(set(V)) == 7 and all(v and v % q == 0 for v in V)
assert pow(5, 7*E, q*q) == 1
assert n == 3+5**4+4262**2+19571**2

~~~
