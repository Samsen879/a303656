# A genuine fifth-power norm divisor gives an unconditional switched comparison

I obtained an unconditional signed lower bound on a cofinal subfamily of the original \(3,5\) grid. A genuine divisor of the shift reduces the prime and its partner remainder to the same scale, so Bombieri–Vinogradov suffices for the forward sieve. The signed count concerns **one blocked label** on each grid in this subfamily. The sign over all 147 phases remains open.

## The cofinal subfamily

Set
\[
a=5x,\qquad b=5y-2,\qquad x\equiv2\pmod6,\qquad y\equiv0\pmod6.
\]
Keep the original balance condition \(39/40<B/A<122/125\), where \(A=3^a,\ B=5^b\). Write
\[
S_0=A+25B,\quad S=3^x+5^y,\quad P=A+125B,\quad S_3=729A+B.
\]
Use the ordinary window \(2S_3-P<n\le729A+625B\), and compare \(n\equiv0\pmod{49}\) with
\[
n\equiv r_-:=3^{a+4}+5^{b+2}+7\pmod{49}.
\]
Require \(r_--S\not\equiv0\pmod{49}\). The difference is automatically zero modulo 7, so the alternative remainder has exact 7-adic depth one throughout the \(r_-\) class.

These conditions hold cofinally. On \(x\equiv20\pmod{42},\ y\equiv0\pmod{42}\) one has \(r_--S\equiv7\pmod{49}\). The balance strip then requires \(y\log5-x\log3\) to lie in a fixed open interval. Irrationality of \(\log3/\log5\) gives infinitely many hits in the two progressions. The label \((x,y)\) belongs to the original grid with steps \(4,2\) and also satisfies \(y\equiv b+2\pmod6\).

**For every sufficiently large member of this subfamily**, the class \(n\equiv0\pmod{49}\) contains
\[
\gg \frac{B^{4/5}}{\log B\sqrt{\log\log B}}
\]
distinct targets in the ordinary window for which both \(n-S_0\) and \(n-S\) are sums of two integer squares. The \(r_-\) class has zero such pairs for this label.

## Why the unconditional sieve works

Put \(d=S\) and \(M=B/d\asymp B^{4/5}\). The actual fifth-power identity gives
\[
S_0-S=45d\kappa,\qquad
\kappa=\frac{X^4-X^3Y+X^2Y^2-XY^3+Y^4-1}{45},
\qquad X=3^x,\quad Y=5^y.
\]
The numerator vanishes modulo \(5,9,8\), so \(\kappa\in8\mathbb Z\), and \(\kappa\asymp M\). Also \(d=(3^{x/2})^2+(5^{y/2})^2\) is a primitive sum of two squares. Mark targets by \(n=S_0+45dhp\), with \(p\equiv1\pmod4\) prime and \(h\le M^\eta\) supported on primes \(1\bmod4\), with \((h,\kappa)=1\). The anchor is a true norm. The alternative is a norm exactly when \(hp+\kappa\) is. For each \(h\), the window gives a prime interval of length and endpoints \(\asymp M/h\). The condition \(n\equiv0\pmod{49}\) selects a reduced class for \(p\bmod196\), since \(d\equiv3\) and \(S_0\equiv5\pmod7\).

Take \(z=M^{1/2-\delta}\) for a small fixed \(\delta>0\) and \(0<\eta\le\delta/4\). Define \(F(w)=\prod_{q>2,\ q\mid w}(q-1)/(q-2)\), with \(F_I,F_+\) its inert and split parts. The forward half-dimensional sieve on \(hp+\kappa\) has local density \(1/(q-1)\) at inert \(q\nmid7\kappa\). The omitted 7 is already a unit, and any \(q\mid\kappa\) below \(z\) could only hit \(p=q\), outside the prime interval. Bombieri–Vinogradov gives level \(D=(M/h)^{1/2}/(\log M)^C\) with the fixed base modulus 196 absorbed. Thus \(s=\log D/\log z\ge1+c\delta\), and \(f_{1/2}(s)\gg\sqrt\delta\). The rough count is at least
\[
c_1\sqrt\delta\, F_I(\kappa)\frac{M}{h(\log M)^{3/2}},
\]
uniformly in \(h,\kappa\) for sufficiently large \(M\). The product over omitted inert divisors of \(\kappa\) above \(z\) is \(1+o(1)\) uniformly. [Half-dimensional sieve and remainder bound](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136) · [Explicit \(f_{1/2}\) near \(s=1\)](https://arxiv.org/html/2501.16723v1#S5)

A rough survivor that fails the norm test must be \(hp+\kappa=mq_1q_2\), with distinct inert primes \(z<q_1<q_2\) and \(m\ll M^{2\delta}\) split-supported. Indeed, \(hp+\kappa\equiv1\pmod4\) and \(z^3\gg M\). Fix \(m,q_1\). Both are coprime to \(h\kappa\), since a common prime with \(\kappa\) would have to equal \(p\). The exact switch is
\[
q_2=\alpha+ht,\qquad
p=mq_1t+\frac{mq_1\alpha-\kappa}{h},
\qquad mq_1\alpha\equiv\kappa\pmod h.
\]
Here \(t\) ranges inside an interval of length \(T\asymp M/(hmq_1)\gg z/h\). The two primitive linear forms have determinant \(-\kappa\) and coprime slopes. An elementary two-form Selberg upper sieve gives
\[
\ll \frac{M}{hmq_1(\log M)^2}\,F(h)F(\kappa)F(m)F(q_1).
\]
For uniformity, discard the prime 2 and sieve \(t\) by primes up to \(R^c\) with \(R=T^{1/20}\) and small absolute \(c>0\). There are two roots per prime except at divisors of \(hmq_1\kappa\), where there is one. The Selberg denominator truncated at \(R\) retains at least half its Euler product, since the logarithmic mean of the divisor under the full product is \(\sum_{q\le R^c}\rho(q)\log q/q\le \tfrac12\log R\). The root counts give the stated factors \(F\), and the elementary residue-count error is \(O(R^6)\) using \(|\lambda_j|\le3^{\omega(j)}\) and \(\rho(j)\le2^{\omega(j)}\). This step uses no prime distribution in a growing modulus.

The exceptional factors matter in the sum. For each split prime \(q\),
\[
1+\sum_{j\ge1}\frac{F(q^j)}{q^j}=F(q).
\]
As \((m,h\kappa)=1\), the Euler product for the \(m\)-sum cancels \(F(h)\) and the split factors of \(F(\kappa)\) up to \(O(M^{2\delta})\). The larger factors of \(F(\kappa)\) contribute \(1+o(1)\). The remaining split product is \(O(\sqrt{\delta\log M})\), and \(\sum_{z<q_1\ll\sqrt M}1/q_1=O(\delta)\). Hence the false survivors are at most
\[
c_2\delta^{3/2} F_I(\kappa)\frac{M}{h(\log M)^{3/2}}.
\]
Fixing \(\delta\) sufficiently small leaves a positive lower bound for **true** pairs.

Finally, \(\sum_h1/h\gg_\eta\sqrt{\log M}/F_+(\kappa)\) over the allowed \(h\). One way to see this is to take the split harmonic Euler product up to \(M^{c\eta}\), omit primes dividing \(\kappa\), and use the logarithmic mean to retain at least half the mass below \(M^\eta\). Mertens gives \(F_+(\kappa)\ll\sqrt{\log\log M}\). Since \(p\gg M^{1-\eta}\) implies \(p^2\gg B\), a target has at most one such marked prime. The resulting count is of distinct integers. The prime scale is \(B^{(4/5)(1-\eta)}\ll p\ll B^{4/5}\). The original \(2/3<\theta<3/4\) band and compensation by the other grid phases remain unresolved.

## Exact replay

The first check uses a genuine narrow-strip point. The two prime-certified controls use the same fifth-power construction and ordinary window at smaller \(x,y\), outside the narrow balance strip. Both anchors are true norms. The positive alternative has explicit square coordinates after division by \(45d\). The negative alternative has exact 7-adic depth one.

```python
from math import isqrt

def params(x, y):
    a, b = 5*x, 5*y-2
    A, B = 3**a, 5**b
    S0, P, S3 = A+25*B, A+125*B, 729*A+B
    d = 3**x + 5**y
    assert d == (3**(x//2))**2 + (5**(y//2))**2
    r = (pow(3, a+4, 49) + pow(5, b+2, 49) + 7) % 49
    assert (r-d) % 7 == 0 and (r-d) % 49 and d % 7 and S0 % 7
    return A, B, S0, d, 2*S3-P, 729*A+625*B, r

A, B, *_ = params(391622, 267324)
assert 39*A < 40*B and 125*B < 122*A

_, _, S0, d, lo, hi, r = params(140, 96)
k, rem = divmod(S0-d, 45*d)
assert rem == k % 8 == 0
ell = (lo-S0)//(45*d) + 1
Q = 1 << 446
f = 4*((isqrt(ell+k)+4)//4 + 1267)
rhs = ((k-f*f) % Q)//8
v, j = rhs % 2, 1
while j < 443:
    j = min(2*j, 443)
    m = 1 << j
    v = (v-(2*v*v+v-rhs)*pow(4*v+1, -1, m)) % m
c = Q//2-1-4*v
p0 = c*c+f*f-k

t = (ell-1+Q-1)//Q
s = ((r-S0)*pow(45*d, -1, 49)-1)*pow(Q, -1, 49) % 49
t += (s-t) % 49
t += 49*(1-t%2)
p1 = 1+Q*(t+98*245)

for p, witness, residue in [(p0, 11, 0), (p1, 3, r)]:
    assert 0 < p < Q*Q and p % Q == 1 and (p-1)//Q % 2 == 1
    assert pow(witness, (p-1)//2, p) == p-1  # Proth certificate
    n = S0+45*d*p
    assert lo < n <= hi and n % 49 == residue
assert p0+k == c*c+f*f
assert (45*d*(p1+k)) % 49 == 7
print(p0.bit_length(), p1.bit_length(), r)  # 891 891 24
```

Independent BigInt verified the narrow-strip sample, both 891-bit Proth certificates, the actual positive square coordinates, and the exact depth-one negative alternative. The theorem applies to one blocked label on cofinally many actual grids and the indicated prime band, not the full grid or the originally unresolved intermediate band.
