# Growing sources give a summable zero-cancellation bound

Use the [aligned repair-line analysis](SINGLE_WITNESS_ALIGNED_REPAIR_GCD.md). Fix \(\alpha>0\) and a function \(\epsilon(q)\to0\). Consider actual integers affected by a constant-zero terminal \(q>Z\) that reads exactly the first digit of both axes at an ordinary source \(p\), where
\[
 (\log q)^\alpha\le p\le q^{\epsilon(q)}.
\]
The upper density of these integers is \(O_\alpha((\log Z)^{-\alpha})\) as \(Z\to\infty\), without assuming a distribution of common Wieferich primes. This is only one class of possible obstructions.

Indeed the terminal characters determine one slope \(m_{q,p}\). Setting \(A=3^c\bmod p,B=5^d\bmod p\), a zero-intercept matching line forces \(A/B=\rho=-m_{q,p} f_5/f_3\), with \(f_b=(b^{p-1}-1)/p\bmod p\), and
\[
 n\equiv[A]+[B]=(1+[\rho])[B]\pmod{p^2}.
\]
Thus at most \(p-1\) residues modulo \(p^2\) are possible, even if the other exponents may vary with \(n\); for \(\rho=-1\) there is just the zero residue. The observed zero terminal also requires \(q\mid n\). The CRT density for a pair is at most \(1/(qp)\).

In a dyadic interval \(X\le q<2X\), eventually all such \(p\le\sqrt X\), and \(p\mid q-1\). [Brun–Titchmarsh](https://doi.org/10.1112/S0025579300004708) on the class \(1\bmod p\), followed by the sum over \(p\ge(\log X)^\alpha\), bounds the pair weights by \(O((\log X)^{-1-\alpha})\). The dyadic sum from \(Z\) gives the asserted tail. To pass this to actual upper density, first restrict to \(q\le N^{1-\delta}\) when counting \(n\le N\). Then \(p\le N^{\delta/4}\) apart from finitely many pairs, CRT counts \(N/(qp)+O(p)\) as an upper bound, and the total error is \(O(N^{1-\delta/2})\). For greater \(q\le N\), simply count multiples of \(q\); the prime reciprocal sum over \(N^{1-\delta}<q\le N\) is \(O(\delta)+o(1)\). Let \(\delta\downarrow0\) after taking the upper density. This can even overcount all terminal primes without picking out the common ones.

## A standard gcd theorem also gives a pointwise order restriction

For \(L_q=|\langle3,5\bmod q\rangle|\) and \(\lambda_q=\min_b v_q(b^{q-1}-1)\),
\[
 (\lambda_q\log q)^2=o(L_q).
\]
Indeed a reduced basis of the modular kernel lattice has norms \(R_1\le R_2\) with product \(O(L_q)\). Its \(3,5\) monomials are multiplicatively independent and each relation lifts modulo \(q^{\lambda_q}\). The first numerator size therefore gives \(\lambda_q\log q=O(R_1)\). [Corvaja–Zannier, Corollary 1, Eq. (1.3)](https://arxiv.org/pdf/math/0311030) gives \(\lambda_q\log q=o(R_2)\): the \(S\)-unit group is fixed and only finitely many independent exceptional pairs occur for any fixed \(\epsilon>0\); each fixed pair supports finitely many primes. Multiply these bounds. This excludes order \(O((\log q)^2)\) along a growing sequence of matched primes, but is not a summable bound on large orders comparable to \(q\).

At the actual ordinary reader in the replay, one zero observation suffices to veto all 133 repair points when its own digit is frozen, and the same integer passes all three tests on releasing that digit. Thus requiring two ordinary sources does not alone require two distinct zero terminal conditions. This remains an ordinary control, not a genuinely common Wieferich obstruction.

~~~python
from math import isqrt

q, B = 1419643, 39669358871192962
n = 3 + B*B
assert q % 4 == 3 and all(q % j for j in range(2, isqrt(q)+1))
assert n % 133**2 == 0 and n % q**2 == q
assert all(pow(a, q-1, q*q) != 1 for a in (3, 5))

def exponent(values):
    x, step = 0, 1
    for a, mod in zip(values, (49, 361, q, (q-1)//133)):
        x += step*((a-x)*pow(step, -1, mod) % mod)
        step *= mod
    return x

def rem(c, d, mod):
    return (n-pow(3, c, mod)-pow(5, d, mod)) % mod

def exact2(c, d, p):
    return rem(c, d, p**3) in range(p*p, p**3, p*p)

for x in range(7):
    for z in range(19):
        c = exponent((x, z, 0, 32319))
        choices = [exponent((x+7*i, (11*z)%19+19*j, 0, 19152))
                   for i in (0, 1) for j in (0, 1)]
        d = next(d for d in choices if all(exact2(c, d, p) for p in (7, 19)))
        assert rem(c, d, q*q) == q

c, d = 151199743527567, 149165666260380
c += 133*(q-1)*841236
assert all(exact2(c, d, p) for p in (7, 19, q))

~~~
