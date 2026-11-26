# Two-source alignment and factorization-free gcd stripping

Extend the [single-source aligned repair test](SINGLE_WITNESS_ALIGNED_REPAIR_GCD.md) to two independent ordinary source primes \(p,r\). Suppose a later inert prime \(q\) reads exactly one digit on both axes at both sources. Write \(D=pr\), the terminal order lcm as \(DM\) with \(\gcd(M,D)=1\), and the two repair slopes as \(m_p,m_r\). Combine them to \(m\bmod D\) by CRT. Simultaneous constant-zero on both repair lines requires the zero intercept and prime-to-source sign conditions as before, and the two character matches now combine to \(3^M=(5^M)^m\bmod q\). At a common Wieferich reader, these relations persist modulo \(q^\lambda\), \(\lambda=\min_{b=3,5}v_q(b^{q-1}-1)\), by the uniqueness of torsion lifting.

The lattice \(\Lambda=\{(a,b):ma+b=0\bmod D\}\) has index \(D\). For any basis vectors, form the two corresponding integer differences representing \(3^{Ka}5^{Kb}=1\) (move negative powers across), where \(K\) is a multiple of \(M\) prime to \(D\). Their gcd \(G\) is divisible by \(q^\lambda\) in the aligned common Wieferich case. Conversely, for a prime factor of \(G\) not dividing \(15D\), the basis generates \((D,0),(0,D),(1,-m)\), and the two \(K\)-powered base orders divide \(D\) and meet the matching relation. Repeatedly remove the gcd of \(G\) with
\[
 15D\prod_{u=3^K,5^K}(u^p-1)(u^r-1).
\]
The retained part consists precisely of the prime powers of \(G\) at primes where **both** \(K\)-powered orders equal \(D\). This uses only modular exponentiation and gcd, not a prime factorization of \(G\). If the retained part is 1, even the matching at first residue is impossible; if it is prime, it contains no possible square factor for a common Wieferich alignment. The relation lattice itself does not eliminate the unbounded tame factor \(M\).

For sources 7,19 with zero observations modulo each source, the ordinary slopes are \(1,11\), giving \(m=106\bmod133\), with basis \((5,2),(-19,19)\). The exact arithmetic check below shows that the only possible unstripped prime for \(M\le3558\) is \(q=1419643\) at \(M=3558\), with multiplicity one; \(M\) divisible by 4 is impossible for inert \(q\). Thus no genuinely common Wieferich terminal fits that range. The ordinary positive control then gives distinct 133 shifted values modulo \(q^2\) with common first-digit zero, all at the same integer, while the two earlier repairs have exact valuation two. The high exponents of that local replay are not asserted to fit the actual height of the short witness. These results do not decide the unrestricted obstruction problem.

~~~python
from math import gcd, isqrt

def full(K):
    G = gcd(6075**K - 1, 5**(19*K) - 3**(19*K))
    T = 15 * 133
    for a in (3, 5):
        u = pow(a, K, G)
        for s in (7, 19):
            T = T * (pow(u, s, G) - 1) % G
    while (d := gcd(G, T)) > 1:
        G //= d
    return G

assert [(s, ((3**(s-1)-1)//s) % s, ((5**(s-1)-1)//s) % s)
        for s in (7, 19)] == [(7, 6, 6), (19, 18, 12)]
q = 1419643
assert [(M, g) for M in range(1, 3559)
        if M % 4 and gcd(M, 133) == 1 and (g := full(M)) != 1] == [(3558, q)]

assert all(all(s % j for j in range(2, isqrt(s)+1)) for s in (593, q))
L = 133 * 3558
assert all(pow(a, L, q) == 1 and
           all(pow(a, L//s, q) != 1 for s in (2, 3, 7, 19, 593))
           for a in (3, 5))
assert all(pow(a, q-1, q*q) != 1 for a in (3, 5))

n = 3 + 11842955847489559**2
assert n % ((133*q)**2) == 0

def exponent(values):
    x, step = 0, 1
    for a, mod in zip(values, (49, 361, q, (q-1)//133)):
        x += step * ((a-x) * pow(step, -1, mod) % mod)
        step *= mod
    return x

def remainder(c, d, mod):
    return (n - pow(3, c, mod) - pow(5, d, mod)) % mod

values = set()
for x in range(7):
    for z in range(19):
        c = exponent((x, z, 1, 32319))
        ds = [exponent((x+7*i, (11*z)%19+19*j, 0, 19152))
              for i in (0, 1) for j in (0, 1)]
        d = next(d for d in ds
                 if all(remainder(c, d, s**3) in range(s*s, s**3, s*s)
                        for s in (7, 19)))
        v = remainder(c, d, q*q)
        assert v and v % q == 0
        values.add(v)
assert len(values) == 133

~~~
