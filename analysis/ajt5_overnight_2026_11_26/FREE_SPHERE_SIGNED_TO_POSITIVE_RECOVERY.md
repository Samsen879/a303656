# A free sphere parameter for signed-to-positive recovery

A free sphere coordinate gives **\(\gg_\epsilon X^{1/3-\epsilon}\) distinct targets \(n\le X\), all \(3\bmod4\), with both signed norms and a true positive representation**. At each constructed height \(B\), there are \(\gg_\epsilon B^{1/2-\epsilon}\) distinct targets. One branch has both positive exponents growing. The count uses the classical ineffective class-number lower bound. This extends the [two-power construction](https://github.com/Samsen879/a303656/commit/11c5f263ccecad0562eac567c82f788ee078ebe5) by allowing many targets at the same powers.

### Freeing one coordinate

For \(k\ge2\), use any of these three branches.

| Lower exponent \(d\) | \(Q\) | \(Z\) | Initial norm element |
|---|---:|---:|---|
| \(3^k\) | \(5^d\) | \(1\) | \(2\) |
| \(2\cdot3^k\) | \(5^d\) | \(3^d\) | \(4\) |
| \(4\cdot3^k\) | \(5^d\) | \(1\) | \(24+4\sqrt{-3}\) |

Set \(B=5Q\) and \(P=3Z\) for the signed powers. The positive powers will be \(Q,Z\). First construct
\[
4(Q-Z)=v^2+3t^2,\qquad t^2\asymp B.
\]
For odd \(a,b\), the identity
\[
a^2+ab+b^2=
\left(\frac{a-b}{2}\right)^2+
3\left(\frac{a+b}{2}\right)^2
\]
turns each factor of \(a^3-b^3=(a-b)(a^2+ab+b^2)\) into a norm. Start with \((a,b)=(5,1),(25,9),(625,1)\), respectively, and iterate cubing. The table supplies the norm of \(a-b\). Multiplying the resulting norm element by \(2\) gives the factor \(4\). The initial elements have even coefficients, and all cubing factors have integer coefficients, so this last multiplication gives \(4\mid t\).

The conjugation choices keep \(t\) large and give the needed ternary phase. For a fixed factor \(a_0+b_0\sqrt{-3}\) with both coordinates nonzero and remaining product \(A+C\sqrt{-3}\), the two imaginary coefficients are \(a_0C\pm b_0A\). Their larger absolute value is a fixed positive fraction of \(\sqrt B\). In the first branch every factor has imaginary coordinate divisible by \(3\). In the third, \(9\mid Q-1\) forces \(3\mid t\). In the second, each cubing factor has imaginary-to-real ratio \(1\bmod3\). Use the first two factors with equal signs if the remaining ratio is zero and opposite signs otherwise. Both conjugate choices then give \(3\nmid t\). The first two factors have coordinates (8,17) and (7448,8177); both same-sign and opposite-sign products have nonzero real and imaginary parts, so the same size argument applies.

Now put \(N=3t^2+6Z\), and take any integer solution
\[
x^2+y^2+r^2=N,\qquad r\text{ odd},\qquad S=x^2+y^2>P.
\]
The resulting target satisfies
\[
\boxed{n=B+P-S=Q+Z+v^2+r^2},\qquad 2P-S=r^2-3t^2.
\]
In particular \(Q<n<B\), and the positive residual is \(v^2+r^2>0\). The signed data are the negative of a Gaussian norm \(n-B-P=-S\), and the real quadratic norm \(n-B+P=r^2-3t^2\). We have \(N\equiv6\pmod8\) and \(N\equiv3\) or \(6\pmod9\), so each triple has exactly two odd coordinates and all three coordinates are units modulo \(3\). Thus \(S\equiv1\pmod4\), \(S\equiv2\pmod3\), and the **signed** ternary residual \(n-B=P-S\) is a unit.

### Counting and selecting targets

Gauss’s formula and Siegel’s bound give \(r_3(N)\gg_\epsilon N^{1/2-\epsilon}\) for \(N\equiv6\pmod8\), including nonsquarefree \(N\). Indeed, the primitive count is \(12h(-4N)\). Writing \(N=e f^2\) with \(e\) squarefree, the order class-number formula gives \(h(-4N)\ge h(-4e)\varphi(f)\gg_\epsilon N^{1/2-\epsilon}\). [Gauss’s formula](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_30) · [Siegel’s bound](https://bibliotekanauki.pl/articles/1395111)

Exactly two thirds of the ordered triples have \(r\) odd. For each \(|r|\) there are \(B^{o(1)}\) choices of \(x,y\), by the two-square divisor bound. Discarding \(S\le P\) loses only \(O(1+P/\sqrt B)\) possible values of \(|r|\), since they lie next to \(\sqrt N\). This is negligible because \(P\ll B^{\log3/\log5}\). Distinct \(|r|\) give distinct targets, proving the per-height count. Between \(3^k\) and \(3^{k+1}\), the lower exponents include \(4\cdot3^{k-1}\) and \(2\cdot3^k\). Consecutive ratios are at most \(3/2\), so the largest available \(B\le X\) is at least a fixed positive constant times \(X^{2/3}\) for large \(X\).

**Generation** chooses an admissible sphere coordinate \(r\). **Target selection** starts from \(n\), takes the least power \(B=5^D>n\), recognizes the branch from \(D-1\), and reconstructs \(v,t\) by a fixed sign convention. The positive witness is recovered by testing whether \(n-Q-Z-v^2\) is a square. Recognizing membership in the signed family additionally requires the Gaussian norm test for \(N-r^2\).

```python
# Two different targets at one height, and a control with both exponents moving.
for Q,Z,v,t,x,y,r in (
    (125, 1, 8, 12, 13, 10, 13),
    (125, 1, 8, 12, 7, 10, 17),
    (5**18, 3**18, 2859544, 1536256, 1555939, 1496890, 1555939),
):
    S = x*x + y*y
    n = 5*Q + 3*Z - S
    assert v*v + 3*t*t == 4*(Q-Z)
    assert 6*Z-S == r*r-3*t*t
    assert Q < n < 5*Q and n % 4 == 3 and (n-5*Q) % 3
    assert n == Q+Z+v*v+r*r
```


The listed arithmetic was independently replayed in BigInt, including conjugation choices through k=5 in all three branches. The class-number estimate is ineffective, and the construction does not find witnesses for arbitrary preassigned targets or produce a density-one conclusion.
