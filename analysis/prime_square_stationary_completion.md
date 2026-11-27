# Prime-square stationary completion for the semiprime collision problem

Part of the [balanced-semiprime second moment](https://github.com/Samsen879/a303656/pull/71). Here (H) is the logarithm of the target height, and the interval under study tracks actual base-nine exponents; this is a spectral reduction, not a target coverage assertion.

The narrow Fourier mass from characters that miss either prime-square lifting digit is \(O(\sqrt H)\), below the required \(H/(\log H)^5\) scale. For characters primitive at both prime squares, completion gives an exact formula with one surviving coarse exponent per frequency. That formula also gives a counter to an absolute-value completion argument: even though the untwisted complete sum vanishes, the absolute completion bound is already of order \(H\) on an interval of length \(\asymp H\).

### The characters missing a lifting digit are controlled

Let \(H=\log X\), take balanced inert primes \(p,q\asymp\sqrt H\) in the same interval as before, and suppose \(9\) lifts at both prime squares. Write \(s=pq\), \(M=s^2\), \(r=\operatorname{ord}_s(9)\asymp H\), and \(R=sr=\operatorname{ord}_M(9)\). Let \(J\) be the actual \(O(H)\)-length exponent interval with the nonunit values \(1-9^e\) omitted. For \(G=(\mathbb Z/M\mathbb Z)^\times\), put
\[
S_J(\chi)=\sum_{e\in J}\chi(1-9^e).
\]

Fix **any** lifting digit of \(\chi\) at \(p\), allowing all other character components to vary. The resulting characters form a coset of the characters factoring through \(pq^2\). Orthogonality gives
\[
\frac1{|G|}\sum_{\chi\text{ with that digit}}|S_J(\chi)|^2
=\frac{|J|}{p}.
\]
Indeed, equality of the values \(1-9^e\bmod pq^2\) forces the exponent difference to be a multiple of \(qr\gg H\), so only equal exponents contribute. The same argument gives \(|J|/q\) at \(q\). Taking the zero digit at either prime bounds all imprimitive contributions by \(O(\sqrt H)\), even before restricting to the narrow frequency window.

### Exact completion for the doubly primitive characters

Write \(\chi(9)=e^{2\pi i\alpha/R}\). Split an exponent as \(e=e_0+ru\), where \(0\le e_0<r\). At a prime \(v=p,q\), this is an iterated step along the smaller local period \(r_v=\operatorname{ord}_v(9)\), since \(r_v\mid r\). For unit \(1-9^{e_0}\), the lifting digit changes exactly by
\[
F_v(1-9^{e_0+ru})-F_v(1-9^{e_0})
\equiv-rF_v(9)\frac{9^{e_0}}{1-9^{e_0}}\,u\pmod v.
\]
Here \(F_v(z)=(z^{v-1}-1)/v\bmod v\). This follows by expanding \(9^{ru}\) modulo \(v^2\). [Bourgain, Ford, Konyagin and Shparlinski, *On the divisibility of Fermat quotients*](https://doi.org/10.1307/mmj/1281531459)

Complete the sum over the \(R\)-cycle with twist \(e^{2\pi i\nu e/R}\), setting its summand to zero at nonunits. For a character primitive at both squares, the two lift sums over \(u\bmod p\) and \(u\bmod q\) vanish unless
\[
9^{e_0}\equiv\frac{\nu}{\nu+\alpha}\pmod s,
\]
with both \(\nu\) and \(\nu+\alpha\) units modulo \(s\). There is at most one such \(e_0\bmod r\). When it exists, the complete twisted coefficient is exactly
\[
s\,\chi(1-9^{e_0})e^{2\pi i\nu e_0/R}.
\]
In particular, the coefficient vanishes at \(\nu=0\) and at every frequency divisible by \(p\) or \(q\).

**Why absolute completion is insufficient.** In one block \(0\le\nu<s\), exactly \(r-r/r_p-r/r_q+1\asymp H\) frequencies survive. The correspondence is the bijection \(\nu=\alpha z/(1-z)\bmod s\) for the eligible \(z=9^{e_0}\). For an ordinary exponent interval \(I\) of length \(N\asymp H\) with \(N\le r/4\), its unnormalized Fourier coefficient has magnitude \(\gg N\) for \(0\le\nu<s\). Consequently, these frequencies alone contribute \(\gg Ns/R\cdot r\asymp H\) to the absolute-value completion bound. The cancellation needed for the narrow mass must involve the surviving phases.

More explicitly, let \(e_\nu\) denote the unique surviving exponent when it exists, and use the unnormalized interval transform \(\widehat{1_I}(\nu)=\sum_{e\in I}e^{-2\pi i\nu e/R}\). The remaining estimate is
\[
\frac1{|G|}
\sum_{\substack{\chi\ \mathrm{primitive\ at\ both\ squares}\\
                 \|\alpha/R\|\le(\log H)^5/H}}
\left|
\frac1r\sum_{\nu:\,e_\nu\ {\rm exists}}
\widehat{1_I}(\nu)\,\chi(1-9^{e_\nu})e^{2\pi i\nu e_\nu/R}
\right|^2
\ll \frac{H}{(\log H)^5}.
\]
This is a phase-sensitive estimate on the completed stationary contributions, with both prime axes coupled through \(e_\nu\). I did not establish it or the supply of lifted pairs needed for target coverage. [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### Exact inline replay

At \(p=19,q=23\), take the character whose phase is \(F_{19}(z)/19+F_{23}(z)/23\). Its restriction index is \(\alpha=16137\bmod43263\). In the block \(0\le\nu<437\), exactly \(80\) frequencies survive. At \(\nu=36\), the sole surviving coarse exponent is \(e_0=1\), and the two digit slopes are \(10\bmod19\) and \(9\bmod23\). The standard-library replay verifies these exact digit and frequency statements.

```python
from math import gcd

p, q, r = 19, 23, 99
s, R = p*q, p*q*r

def F(z, v):
    return (pow(z, v-1, v*v) - 1) // v % v

def slope(e, v):
    z = pow(9, e, v)
    return -r*F(9, v)*z*pow(1-z, -1, v) % v

def survivors(nu):
    return [e for e in range(r)
            if gcd(1-pow(9, e, s), s) == 1
            and all((slope(e, v) + nu*pow(s//v, -1, v)) % v == 0
                    for v in (p, q))]

assert [F(9, v) for v in (p, q)] == [17, 11]
assert [slope(1, v) for v in (p, q)] == [10, 9]
alpha = r*(q*17 + p*11) % R
assert alpha == 16137 and 36*pow(36+alpha, -1, s) % s == 9
assert survivors(36) == [1]
assert survivors(0) == survivors(p) == survivors(q) == []
assert sum(bool(survivors(nu)) for nu in range(s)) == 80
for v in (p, q):
    for u in range(s):
        assert (F(1-pow(9, 1+r*u, v*v), v)-F(1-9, v)) % v == slope(1, v)*u % v
```