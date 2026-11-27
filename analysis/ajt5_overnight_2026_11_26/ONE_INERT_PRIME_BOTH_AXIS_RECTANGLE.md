# A single inert prime can block a growing both-axis rectangle

One inert prime can block a growing rectangle of actual \(3,5\) labels at the **same prescribed target**, even after every label passes the previous small-prime panel. The rectangle has \(\Theta((\log n)^{3/2})\) distinct labels, all with \(v_{43}=1\). Counting a fresh odd-prime cost for each failed label therefore overcharges the contribution of \(43\).

The exact replay reproduces the previous 910,448-bit target. At that \(n\), all 14 labels in a \(2\times7\) rectangle fail at \(43\). A neighboring label retains the common split divisor, passes the same panel, and has \(v_{43}=0\). Its square-sum status is undetermined. [Baseline commit](https://github.com/Samsen879/a303656/commit/b12d2880f68d32fa707cd2f7562a5ee495a96b0d)

### Fixed-target construction

Write \(A=3^a,\ B=5^b\), with \(39/40<B/A<122/125\). Set
\[
S_0=A+25B,\qquad P=A+125B,\qquad S_3=729A+B,\qquad U=729A+625B.
\]
Use any of the prior targets for the panel \(\mathcal P=\{3,7,11,19,23,31\}\). Once \(n\) is supplied, hold it fixed. The hypotheses used are \(2S_3-P<n\le U\), the supplied \(S_0\) representation, and
\[
\gcd\!\left(n-P,\prod_{p\in\mathcal P}p\right)=1,\qquad v_{43}(n-P)=1.
\]

The large original power-of-five cofactor explains why changing both axes needs a smaller divisor. If \(5^j\) divides both remainders and the new label is \(3^x+5^y\) with \(y\ge j\), then \(4\cdot5^{j-1}\mid x-a\), by the order of \(3\) modulo \(5^j\). Every active label has \(x\le a+6\), so \(4\cdot5^{j-1}>a+6\) forces \(x=a\) in that range. If \(y<j\) and \(x\ne a\), comparing the two differences gives \(v_5(3^x-3^a)=y\), which bounds \(5^y\le 5(a+6)/4\).

Take the largest odd \(j\) with \(c^2\le a\), where \(c=5^j\). This keeps \(c\asymp\sqrt a\) and retains a common Gaussian divisor of norm \(c\) from the supplied representation. Put
\[
D=4c/5,\qquad L=27090,\qquad H=\operatorname{lcm}(D,L).
\]
Use the labels
\[
S_{u,v}=3^{a-Hu}+5^{b+3-Lv},
\qquad
1\le u\le \left\lfloor\frac{a-1}{H}\right\rfloor,\quad
1\le v\le \left\lfloor\frac{b}{2L}\right\rfloor.
\]
Keep \(u\equiv1,2\pmod{11}\). For each of these two row phases, find the column phase modulo \(11\), if any, that makes \(23\mid n-S_{u,v}\). Discard the union of those two forbidden phases from the column set for both row phases. There is at most one such phase per row because \(5^L\) has order \(11\) modulo \(23\), and \(3^{11H}\equiv1\pmod{23}\). At least nine column phases remain.

Both bases raised to \(L\) are \(1\) modulo \(7,11,19,31,43^2\). Modulo \(3\), the \(3\)-powers vanish and the \(5\)-exponents have unchanged parity. Thus all retained remainders pass \(\mathcal P\) and agree with \(n-P\) modulo \(43^2\). They are positive and divisible by \(c\). The labels are distinct as integers. If a collision involved different exponents on both axes, the \(3\)-power difference would have \(5\)-adic valuation at most \(1+\lfloor\log_5 a\rfloor\), while the \(5\)-power difference would have valuation at least \(b/2\).

The ordinary height condition leaves room for every label in the rectangle. If its quotient by \(c\) were \(h^2+k^2\), orient it with \(h\ge k\ge0\) and multiply \(h-ik\) by \(5^{(j-1)/2}(2+i)\). The first coordinate squared is at least \(4(n-S_{u,v})/5\). Its height key would therefore satisfy
\[
S_3<S_{u,v}+\tfrac45(n-S_{u,v})\le K\le n\le U.
\]
The actual failure is the exact odd valuation at \(43\).

Along the cofinal balanced family, the rectangle has \(\Theta(ab/c)=\Theta((\log n)^{3/2})\) cells. Its per-label witness product is \(43^{\Theta((\log n)^{3/2})}\), exceeding every fixed power of \(n\). The \(43\)-part of the least common multiple of those same quotients is exactly \(43\). On the unthinned grid with row step \(D\) and consecutive \(5\)-exponents, the same prime has exact depth one on between \(20/(21\cdot43)+o(1)\) and \(1/43+o(1)\) of all cells. In each row with \(n-3^x\not\equiv0\pmod{43}\), exactly 42 of the 1,806 exponent phases have depth one. The row residues cycle through 21 distinct values modulo \(43\), so at most one row phase is inactive.

This rules out a per-label independent-cost bound even with both exponents varying. A fixed-target escape theorem for the full menu would need to track which exponent phases each prime can cover. The rectangle leaves the original \(S_0\) witness intact and yields no counterexample to A303656.

### Standalone replay

```python
from math import gcd, lcm

a, b = 574422, 392104
A, B = 3**a, 5**b
R, V = 5**(b//4), 5**(b//2-b//4)
panel = (3, 7, 11, 19, 23, 31)
J = 3*7*11*19*23*31

def pair(z, m):
    sq = {i*i % m: i for i in range(m)}
    return next((i, sq[(z-i*i) % m])
                for i in range(m) if (z-i*i) % m in sq)

rows = [(20, 1, 0), (11, 0, 0)]
rows += [(p*p, *pair(d*R*R+p, p*p)) for p, d in [(43, 100), (47, 600)]]
for p in (3, 7, 19, 23, 31):
    z = next(z for z in range(p) if (z-100*R*R) % p and (z-600*R*R) % p)
    rows.append((p, *pair(z, p)))

X = Y = 0
M = 1
for m, u, v in rows:
    inv = pow(M, -1, m)
    X += M*((u-X)*inv % m)
    Y += M*((v-Y)*inv % m)
    M *= m
X = V*(X+M*((917*R//25-X)//M+1))
Y = V*(Y+M*((R//200-Y)//M+1))
S0, S3, U, P = A+25*B, 729*A+B, 729*A+625*B, A+125*B
n = S0+X*X+Y*Y
assert 39*A < 40*B and 125*B < 122*A
assert 2*S3-P < n <= U and S3 < S0+X*X and n % 121 == 36

L, c = 27090, 125
H = lcm(L, 4*c//5)
labels = {3**(a-H*u)+5**(b+3-L*v) for u in (1, 2) for v in range(1, 8)}
assert len(labels) == 14 and n.bit_length() == 910448
for S in labels:
    r = n-S
    assert 0 < S < S0 and 5*S+4*r > 5*S3 and r % c == 0
    assert gcd(r//c, J) == 1 and r % (43**2) in range(43, 43**2, 43)

S = 3**(a-H)+5**(b+3-L+990)
r = n-S
assert S not in labels and 0 < S < S0 and 5*S+4*r > 5*S3
assert r % c == 0 and gcd(r//c, 43*J) == 1
print("14 exact obstructions and one 43-free control at the same target")
```


Taking the union of the forbidden column phases retains one Cartesian product, rather than a row-dependent collection. Its ordinary placement follows already from \(4n/5>S_3\), since \(n>2S_3-P\) and \(3S_3/4>P\) throughout the strip. The 43-free finite control tests only the stated panel and is not certified as a square-sum norm.
