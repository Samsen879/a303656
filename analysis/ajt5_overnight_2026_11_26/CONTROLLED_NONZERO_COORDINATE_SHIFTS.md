# Controlled nonzero coordinate shifts

The least possible nonzero coordinate shift from \(S_0\) to \(S_2\) on the mod-\(11\) target phase is **exactly \(2\)**. More generally, every fixed signed shift in one of the six allowed residue classes produces a growing family of ordinary-height witnesses. This construction generates targets. At a prescribed target, the inverse is an exact square test, and an allowed shift can fail even when a different shift succeeds from the same first representation.

### Exact shifted-edge equation

Use \(A=3^a,\ B=5^b,\ W=\sqrt A\), \(S_0=A+25B\), \(S_2=81A+125B\), and \(e=(S_2-S_0)/4\). Start with \(n=S_0+L^2+t^2\) and seek a second representation with coordinate \(t-\sigma\). Its other coordinate \(M\) must satisfy
\[
(L-M)(L+M)=4e-2t\sigma+\sigma^2.
\]
For even \(\sigma\), the P2 factor-pair test therefore has adjusted product \(e-t\sigma/2+\sigma^2/4\) and retains sum \(L\). For any integer \(\sigma\), the exact inverse test is whether \(L^2-4e+2t\sigma-\sigma^2\) is a nonnegative integer square and \(n-(t-\sigma)^2\) lies in the ordinary window.

On the checked phase \(a\equiv2\bmod10,\ b\equiv64\bmod110,\ n\equiv36\bmod121\), the first two coordinates \(L,t\) are multiples of \(11\), while \(n-S_2\equiv8\bmod11\). The only ways to make \(8\) from two square residues are \(3+5,\ 4+4,\ 5+3\). Thus necessarily
\[
\sigma\bmod11\in\{\pm2,\pm4,\pm5\}.
\]
In particular, zero and unit shifts are impossible for **every** first representation on this target phase. [Checked mod-\(11\) setup](https://github.com/Samsen879/a303656/commit/da0424c5fc5231d0e929b10eb6351d5d41978314)

### Growing witnesses for every fixed allowed shift

Fix such a \(\sigma\). Put \(g=\gcd(2,\sigma)\), \(k=\sigma/g\), and choose a first-coordinate decrement \(h=gr\) with \(2.98W\le h\le3W\). Choose \(r\) by CRT so that \(h^2+\sigma^2\equiv8\bmod11\), \(r\equiv1\bmod |k|\), and \(r\) is odd if \(\sigma\) is odd. Then
\[
C=\frac{4e+h^2+\sigma^2}{22g}
\]
is integral. Choose \(x\equiv C/r\bmod |k|\) nearest to \(C/r\), and set \(y=(C-rx)/k\), \(L=11x\), \(t=11y\). The equation \(rx+ky=C\) gives the exact second representation with coordinates \(L-h,t-\sigma\).

For fixed \(\sigma\) and \(W\ge1100(|\sigma|+1)\), rounding gives \(31W<L<32W\) and \(|t|\le16.5W\). With \(n=S_0+L^2+t^2\), both individual heights lie in \((986A,1322A)\), inside the ordinary window. There are \(\asymp_\sigma W\) choices of \(r\). Their \(L\) values are distinct because \(2e/h+h/2+\sigma^2/(2h)\) decreases by more than the rounding spread between successive choices. The sum-of-two-squares representation bound then gives at least \(A^{1/2-o(1)}\) distinct targets for each fixed allowed shift. Signed shifts also give the stated absolute displacement once \(|t|>|\sigma|\). The discarded bounded values of \(t\) account for only \(A^{o(1)}\) offsets, since each forces \(r\mid4e+\sigma^2-2t\sigma\).

### Same-target positive and negative control

At a shift-\(2\) target from this construction, \(|t|\le8.25W\) and \(M=L-h>28W\). From that **same first representation**, shift \(4\) changes the successful square by \(4t-12\). This is nonzero because \(11\mid t\), and its absolute value is less than \(2M-1\). The new remainder lies strictly between consecutive squares even though it is a square residue modulo \(11\) and its candidate height is ordinary.

```python
a, b = 574422, 392104
W, B = 3**(a//2), 5**b
A = W*W
assert 39*A < 40*B and 125*B < 122*A
S0, S2, S3 = A+25*B, 81*A+125*B, 729*A+B
e = 20*A+25*B

# Construct the target with shift 2 and first-coordinate decrement 2*r.
r = 1 + 11*((3*W-2)//22)
C, rem = divmod(e+r*r+1, 11)
assert rem == 0
x = (2*C+r)//(2*r)
L, t = 11*x, 11*(C-r*x)
M = L-2*r
n = S0+L*L+t*t
assert n%121 == 36 and n-S2 == M*M+(t-2)**2
assert abs(abs(t)-abs(t-2)) == 2

# Try shift 4 at the same target, starting from the same (L,t).
D4 = n-S2-(t-4)**2
assert D4%11 == 3
assert D4-M*M == 4*t-12 and 0 < abs(D4-M*M) < 2*M-1
assert all(S3 < n-(t-s)**2 <= 729*A+625*B for s in (0,2,4))
```

At a prescribed \(n\), the square test is reversible once the initial representation and shift are supplied. The growing construction gives no guarantee that a requested shift will work for an arbitrary target.

### Uniformity and counting details

Take \(a=2+10u,\ b=64+110v\). There are arbitrarily large pairs with \(39/40<B/A<122/125\): the ratio of \(10\log 3\) to \(110\log 5\) is irrational by unique factorization, so the sequence of offsets modulo \(110\log 5\) is dense and visits this open interval at arbitrarily large \(u\), with \(v\) chosen accordingly. Fix one solution \(h\bmod11\) of the displayed square condition before choosing the progression for \(r\). Its step is \(11|k|\) for even \(\sigma\) and \(22|k|\) for odd \(\sigma\). The residue \(x\bmod |k|\) is \(C r^{-1}\bmod |k|\), with no restriction when \(|k|=1\). Integrality of \(C\) follows modulo 11 from the square condition; modulo 4 when both shifts are even, and modulo 2 when both are odd.

The center of the \(L\)-rounding is \(11 C/r=(2e+\sigma^2/2)/h+h/2\). Its derivative with respect to \(h\) is less than \(-9\) throughout the window. The rounding error is at most \(11|k|/2\), so points in the fixed CRT progression have distinct \(L\). Also \(|t|\le 11r/2\le16.5W/g\). In the height bound below, an error of \(A/20\) more than covers \(|2t\sigma-\sigma^2|\) for \(W\ge1100(|\sigma|+1)\). For each fixed target, the familiar divisor bound \(r_2(m)\le4\tau(m)=m^{o(1)}\) bounds multiplicity at \(m=n-S_0=O(A)\). The exceptional bounded coordinates require \(h\mid 4e+\sigma^2-2t\sigma\), a nonzero integer of size \(O(A)\) for sufficiently large \(A\). None of these counting arguments inverts the construction on an arbitrary prescribed target.
